def conversion_and_qmcInput(path, submit_path,fileroot,pp,multiDet,noJastrow,Jastrow3Body,xyz_file,reopt=False):
	'''
	Path: 		the directory to write the files to
	submit_path:	the directory where the job submission will be done from ( may be the same  as the path)
	fileroot:  	Element_geometry_basis_numberDet
	pp:		Type of pseudopotential (or False) must know for addition of cusp correction
	multiDet: 	True if not an SCF calculation
	noJastrow:	True if no jastrow is added to calculation
	Jastrow3Body: 	True if 1,2, and 3 body jastrows are used
	reopt: 		Default of false, true if we are reoptimizing multideterminants coefficients

	'''

	import os
	### generate the wavefunction with appropriate flags

	## flags will be the string added at the end of the convert4qmc command
	## and will have -addCusp  -nojastrow  or -add3BodyJ
	flags = ""
	directory=""
	if noJastrow:
		flags = " -nojastrow"
		directory =  "NoJastrow"
		
	if Jastrow3Body:	
		flags = " -add3BodyJ"
		directory ="Jastrow"
	if not(pp):	
		flags = flags + " -addCusp"


	if multiDet and reopt:
		directory =directory + "_MultiDet_reoptCoeff"
		newDir = path +"/" + directory
		if not(os.path.isdir(newDir)):
			os.mkdir(newDir)
		### generate the cutoff directories which will 
		###  have the optimization and dmc runs in them 
		__generateCutoff__(newDir,fileroot,submit_path,directory,reopt,pp,Jastrow3Body,xyz_file)
		filepath = directory + "/" + fileroot

	elif multiDet:
		directory =directory + "_MultiDet"
		newDir = path +"/" + directory
		if not(os.path.isdir(newDir)):
			os.mkdir(newDir)
		### generate the cutoff directories which will 
		###  have the optimization and dmc runs in them 
		__generateCutoff__(newDir,fileroot,submit_path,directory,reopt,pp,Jastrow3Body,xyz_file)
		filepath = directory + "/" + fileroot

	else:
		directory =directory + "_1Det"
		newDir = path +"/" + directory
		if not(os.path.isdir(newDir)):
			os.mkdir(newDir)
		### generate the DMC files because there is not optimization
		__generateDMC__(newDir,fileroot,fileroot,submit_path,directory,pp)
		filepath = directory + "/" + fileroot
		if Jastrow3Body:
			__generateOpt__(newDir,fileroot,fileroot,submit_path,directory,pp)
			__optJ12__(newDir,submit_path,directory,fileroot,multi=False)
			__optJ3__(newDir,submit_path,directory,fileroot)
			__finishOpt__(newDir,submit_path,directory,fileroot)
		if pp:
	        	__grabPseudo_makeHam__(newDir,newDir,submit_path,directory,Jastrow3Body,xyz_file)


	if not(pp):
		__generateCusp__(newDir,fileroot,submit_path,directory,multiDet)


	conversion_template= "misc/converter.py"
	dump_filename = fileroot + ".dump"
	dictionary = {"DUMPNAME":dump_filename,"FLAGS":flags, "FileName":filepath,"ABSPATH":submit_path}

        newFile=[]
        with open(conversion_template,"r") as fileIn:
                for line in fileIn:
                        for key in dictionary:
                                if key in line:
                                        line = line.replace(key,dictionary[key])

                	newFile.append(line)

        newFilename = newDir+ "/converter_"+fileroot+".py"
        with open(newFilename,"w") as fileOut:
                for line in newFile:
                        fileOut.write("%s" %line)


def __generateCutoff__(directory,fileroot,sub_path,baseName,reopt,usepp,optimize,xyz_file):
	""" Make directories to look at the convergence of the energy as the cutoff increases"""

	import os
	cutoffs = [0.01,0.008,0.006,0.004,0.002,0.0009,0.0007,0.0005,0.0003,0.0001,0.00008,0.00006,0.00004]


	thisdir = sub_path + "/"+baseName
	dictionary = {"MAINDIR":thisdir, "FILEROOT":fileroot}


	fileName= "multiDet_convergence_setup"
	fileTemplate = "misc/" +fileName + ".py"
	newFile=[]
	with open(fileTemplate,"r") as fileIn:
		for line in fileIn:
			for key in dictionary:
				if key in line:
					line = line.replace(key,dictionary[key])
	        	newFile.append(line)
	    		
	
	newFilename = directory + "/" + fileName + ".py"
	with open(newFilename,"w") as fileOut:
		for line in newFile:
			fileOut.write("%s" %line)



	for value in cutoffs:	
		thisDir=directory + "/cutoff_"+str(value)
		if not(os.path.isdir(thisDir)):
			os.mkdir(thisDir)
		local_baseName = baseName + "/cutoff_"+str(value)
		cutoffroot = fileroot + "_" + str(value)

		__generateDMC__(thisDir,cutoffroot,fileroot,sub_path,local_baseName,usepp)
		if optimize:
			__generateOpt__(thisDir,cutoffroot,fileroot,sub_path,local_baseName,usepp)
			__optJ12__(thisDir,sub_path,local_baseName,cutoffroot,multi=True)
			if reopt:
				__optCoeffsAndJastrows__(thisDir,sub_path,local_baseName,cutoffroot)
			__optJ3__(thisDir,sub_path,local_baseName,cutoffroot)
			__finishOpt__(thisDir,sub_path,local_baseName,cutoffroot)
		if usepp:
	        	__grabPseudo_makeHam__(thisDir,directory,sub_path,baseName,optimize,xyz_file)

def __generateCusp__(directory,fileroot,sub_path,baseName,multiDet):
    import os
    ################################################
    #### Generate : Cusp.xml
    ################################################
    import lxml
    from lxml import etree

    if not(os.path.isdir(directory+"/CuspCorrection/")):
	    os.mkdir(directory+"/CuspCorrection/")
    os.system("cp misc/Cusp.xml " +directory +"/CuspCorrection/")

    myFile = directory+"/CuspCorrection/Cusp.xml"
    tree = etree.parse(myFile)
    ## Modify Cusp.xml for your system

    root = tree.getroot()

    project = root[0]
    icld_ptcl = root[2]
    icld_wfs = root[3]
    
    project.set("id",fileroot)

    ptclFile = sub_path+"/"+baseName+"/"+fileroot+".ptcl.xml"
    wfsFile =  sub_path+"/"+baseName+"/"+fileroot+".wfs.xml"
    icld_ptcl.set("href",ptclFile)
    icld_wfs.set("href",wfsFile)

    ###### NOW WRITE THE MODIFICATIONS TO A FILE
    tmpfile = myFile+".tmp"
    f = open( tmpfile,"w")
    f.write("<?xml version=\"1.0\"?>\n")
    f.write(etree.tostring(root,pretty_print=True))
    f.close()

    os.system("mv " + tmpfile + " " + myFile)


    if multiDet:
	fileName = "modify_wfs_4_Cusp_multi"
    else:
	fileName = "modify_wfs_4_Cusp_single"

    fulldir = 	 sub_path+"/"+baseName
    dictionary = {"FULLDIR":fulldir,"FILEROOT":fileroot}

    fileTemplate = "misc/" +fileName + ".py"
    newFile=[]
    with open(fileTemplate,"r") as fileIn:
    	for line in fileIn:
    		for key in dictionary:
    			if key in line:
    				line = line.replace(key,dictionary[key])
	    	newFile.append(line)

    newFilename = directory + "/CuspCorrection/"+fileName + ".py"
    with open(newFilename,"w") as fileOut:
	for line in newFile:
		fileOut.write("%s" %line)


    os.system("cp misc/cusp.sh " +directory + "/CuspCorrection/cusp.sh") 

def __grabPseudo_makeHam__(directory,outerDir,sub_path,baseName,opt,xyz_name):

	import lxml
	import os
	from lxml import etree

	count=0
	element=[]
	with open(xyz_name,"r") as fileIn:	
		for line in fileIn:
			if count >1:
				line.split(" ")
				if line[0] not in element:
					element.append(line[0])
			count+=1
	for el in element:
		os.system("cp ~/qmcpack-3.0.0/pseudopotentials/BFD/"+el + ".BFD.xml " + outerDir)

	### modify DMC.xml hamiltonian to include PP
	myFile = directory + "/DMC/DMC.xml"
	tree = etree.parse(myFile)
	root = tree.getroot()
	hamilt   = root[5] 
	pairPot1 = hamilt[0]

	count=0
	for el in element:
		pairPot1.append(etree.Element("pseudo"))
		pseudo = pairPot1[count]
		pseudo.set("elementType",el)
		el_path =sub_path + "/"+baseName + "/"+el+".BFD.xml"
		pseudo.set("href",el_path)
		count+=1
		
	###### NOW WRITE THE MODIFICATIONS TO A FILE
	tmpfile = myFile+".tmp"
	f = open( tmpfile,"w")
	f.write("<?xml version=\"1.0\"?>\n")
	f.write(etree.tostring(root,pretty_print=True))
	f.close()

	os.system("mv " + tmpfile + " " + myFile)

	if opt:
		## Modify Opt.xml hamiltonian to include PP
	    	myFile = directory + "/Optimization/Opt.xml"
		tree = etree.parse(myFile)
		root = tree.getroot()
		hamilt   = root[5] 
		pairPot1 = hamilt[0]
	
		count=0
		for el in element:
			pairPot1.append(etree.Element("pseudo"))
			pseudo = pairPot1[count]
			pseudo.set("elementType",el)
			el_path =sub_path + "/"+baseName + "/"+el+".BFD.xml"
			pseudo.set("href",el_path)
			count+=1
		
		###### NOW WRITE THE MODIFICATIONS TO A FILE
		tmpfile = myFile+".tmp"
		f = open( tmpfile,"w")
		f.write("<?xml version=\"1.0\"?>\n")
		f.write(etree.tostring(root,pretty_print=True))
		f.close()

		os.system("mv " + tmpfile + " " + myFile)

	
def __generateDMC__(directory,wfsFile,ptclFile,sub_path,baseName,usepp):
    import os
    ################################################
    #### Generate : DMC.xml
    ################################################
    import lxml
    from lxml import etree

    if usepp:
	template_Name = "DMC_PP.xml"
    else:
	template_Name = "DMC_AE.xml"
	

    if not(os.path.isdir(directory +"/DMC")):
        os.mkdir(directory +"/DMC")
    os.system("cp misc/"+template_Name+" " +directory +"/DMC/DMC.xml")
    os.system("cp utils/format_data.py " +directory +"/DMC/")

    myFile = directory+"/DMC/DMC.xml"
    tree = etree.parse(myFile)
    root = tree.getroot()

    project = root[0]
    icld_ptcl = root[2]
    icld_wfs = root[3]
    
    projName = "DMC-"+wfsFile
    project.set("id",projName)

    ptclFile = sub_path+"/"+baseName+"/"+ptclFile+".ptcl.xml"
    wfsFile =  sub_path+"/"+baseName+"/"+wfsFile +".wfs.xml"
    icld_ptcl.set("href",ptclFile)
    icld_wfs.set("href",wfsFile)

    ###### NOW WRITE THE MODIFICATIONS TO A FILE
    tmpfile = myFile+".tmp"
    f = open( tmpfile,"w")
    f.write("<?xml version=\"1.0\"?>\n")
    f.write(etree.tostring(root,pretty_print=True))
    f.close()

    os.system("mv " + tmpfile + " " + myFile)

    ################################################
    ### Generate bgq-DMC.sh
    ################################################
    os.system("cp misc/bgq-DMC.sh "+directory+"/DMC/")

def __generateOpt__(directory,wfsFile,ptclFile,sub_path,baseName,usepp):
    import os
    ################################################
    #### Generate : Opt.xml
    ################################################
    import lxml
    from lxml import etree

    if usepp:
	template_Name = "Opt_PP.xml"
    else:
	template_Name = "Opt_AE.xml"
	
    if not(os.path.isdir(directory + "/Optimization")):
        os.mkdir(directory + "/Optimization")
    os.system("cp misc/"+template_Name+" " +directory +"/Optimization/Opt.xml")
    os.system("cp utils/plot_OptProg.py " +directory +"/Optimization/")

    myFile = directory+"/Optimization/Opt.xml"
    tree = etree.parse(myFile)
    root = tree.getroot()

    project = root[0]
    icld_ptcl = root[2]
    icld_wfs = root[3]
    
    projName = "Opt-"+wfsFile
    project.set("id",projName)

    ptclFile = sub_path+"/"+baseName+"/"+ptclFile+".ptcl.xml"
    wfsFile =  sub_path+"/"+baseName+"/"+wfsFile +".wfs.xml"
    icld_ptcl.set("href",ptclFile)
    icld_wfs.set("href",wfsFile)


    ###### NOW WRITE THE MODIFICATIONS TO A FILE
    tmpfile = myFile+".tmp"
    f = open( tmpfile,"w")
    f.write("<?xml version=\"1.0\"?>\n")
    f.write(etree.tostring(root,pretty_print=True))
    f.close()

    os.system("mv " + tmpfile + " " + myFile)

    ################################################
    ### Generate bgq-DMC.sh
    ################################################
    os.system("cp misc/bgq-Opt.sh "+directory+"/Optimization/")



def __optJ12__(directory,sub_path,baseName,fileroot,multi):

    fulldir = 	 sub_path+"/"+baseName
    dictionary = {"FULLDIR":fulldir,"FILEROOT":fileroot}

    fileName= "optimize_1Body2Body"
    fileTemplate = "misc/" +fileName + ".py"
    newFile=[]
    with open(fileTemplate,"r") as fileIn:
    	for line in fileIn:
    		for key in dictionary:
    			if key in line:
    				line = line.replace(key,dictionary[key])
		if multi:
	    		newFile.append(line)
		elif not("multidet" in line):## make sure we arent tryingt to optimize a multideterminant with only 1det in wfs
	    		newFile.append(line)
			

    newFilename = directory + "/Optimization/" + fileName + ".py"
    with open(newFilename,"w") as fileOut:
	for line in newFile:
		fileOut.write("%s" %line)

	
def __optCoeffsAndJastrows__(directory,sub_path,baseName,fileroot):
    fulldir = 	 sub_path+"/"+baseName
    dictionary = {"FULLDIR":fulldir,"FILEROOT":fileroot}

    fileName= "optimize_coeffs"
    fileTemplate = "misc/" +fileName + ".py"
    newFile=[]
    with open(fileTemplate,"r") as fileIn:
    	for line in fileIn:
    		for key in dictionary:
    			if key in line:
    				line = line.replace(key,dictionary[key])
	    	newFile.append(line)
			

    newFilename = directory + "/Optimization/" + fileName + ".py"
    with open(newFilename,"w") as fileOut:
	for line in newFile:
		fileOut.write("%s" %line)

def __optJ3__(directory,sub_path,baseName,fileroot):
    fulldir = 	 sub_path+"/"+baseName
    dictionary = {"FULLDIR":fulldir,"FILEROOT":fileroot}

    fileName= "optimize_3Body"
    fileTemplate = "misc/" +fileName + ".py"
    newFile=[]
    with open(fileTemplate,"r") as fileIn:
    	for line in fileIn:
    		for key in dictionary:
    			if key in line:
	    			line = line.replace(key,dictionary[key])
	    	newFile.append(line)
			

    newFilename = directory + "/Optimization/" + fileName + ".py"
    with open(newFilename,"w") as fileOut:
	for line in newFile:
		fileOut.write("%s" %line)

def __finishOpt__(directory,sub_path,baseName,fileroot):
    fulldir = 	 sub_path+"/"+baseName
    dictionary = {"FULLDIR":fulldir,"FILEROOT":fileroot}

    fileName= "optimize_finish"
    fileTemplate = "misc/" +fileName + ".py"
    newFile=[]
    with open(fileTemplate,"r") as fileIn:
    	for line in fileIn:
    		for key in dictionary:
    			if key in line:
    				line = line.replace(key,dictionary[key])
	    	newFile.append(line)
			

    newFilename = directory + "/Optimization/" + fileName + ".py"
    with open(newFilename,"w") as fileOut:
	for line in newFile:
		fileOut.write("%s" %line)


