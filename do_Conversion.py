def qp2qmc(write_path, submit_path,mainDirectory,fileroot,pp,multiDet,noJastrow,3BodyJastrow,reopt):

	import os
	### generate the wavefunction with appropriate flags
	submit_path = submit_path + "/"+ mainDirectory

	flags = ""
	directory=""
	if noJastrow:
		flags = " -nojastrow"
		directory =  "NoJastrow"
		
	if 3BodyJastrow:	
		flags = " -add3BodyJ"
		directory ="Jastrow"
	if pp:	
		dmc_templateName = "DMC_PP.xml"
		opt_templateName = "Opt_PP.xml"
	else:
		flags = flags + " -addCusp"
		dmc_templateName = "DMC_AE.xml"
		opt_templateName = "Opt_AE.xml"


	if multiDet and reopt:
		directory =directory + "_MultiDet_reoptCoeff"
		newDir = path +"/" + mainDirectory + "/" +directory
		os.mkdir(newDir)
		### generate the cutoff directories which will 
		###  have the optimization and dmc runs in them 
		__generateCutoff__(newDir,fileroot,submit_path,directory)
		filepath = directory + "/" + fileroot

	elif multiDet:
		directory =directory + "_MultiDet"
		newDir = path +"/" + mainDirectory + "/" +directory
		os.mkdir(newDir)
		### generate the cutoff directories which will 
		###  have the optimization and dmc runs in them 
		__generateCutoff__(newDir,fileroot,submit_path,directory)
		filepath = directory + "/" + fileroot

	else:
		directory =directory + "_1Det"
		newDir = path +"/" + mainDirectory + "/" +directory
		os.mkdir(newDir)
		### generate the DMC files because there is not optimization
		__generateDMC__(newDir,fileroot,submit_path,directory,dmc_templateName)
		filepath = directory + "/" + fileroot



	dump_filename = fileroot + ".dump"
	dictionary = {"DUMPNAME":dump_filename,"FLAGS":flags, "absFileName":filepath)

	conversion_template= "misc/converter.py"
        newFile=[]
        with open(conversion_Template,"r") as fileIn:
                for line in filein:
                        for key in dictionary:
                                if key in line:
                                        line = line.replace(key,dictionary[key])

                newFile.append(line)

        newFilename = newDir+ "/converter_"+rootname+".py"
        with open(newFilename,"w") as fileOut:
                for line in newFile:
                        fileOut.write("%s\n" %line)


def __generateCutoff__(directory,fileroot,sub_path,baseName,reopt):

	import os
	cutoffs = [0.01,0.008,0.006,0.004,0.002,0.0009,0.0007,0.0005,0.0003,0.0001,0.00008,0.00006,0.00004]


	if reopt:
		for value in cutoffs:	
			os.mkdir(directory + "/"+baseName + "/cutoff_"+str(value))
			local_baseName = baseName + "/cutoff_"+str(value)

			__generateDMC__(directory,fileroot,sub_path,local_baseName,template_Name)
			__optCoeffsAndJastrows__(directory,fileroot,sub_path,local_baseName)

	### 
	else:
		for value in cutoffs:	
			os.mkdir(directory + "/"+baseName + "/cutoff_"+str(value))
			local_baseName = baseName + "/cutoff_"+str(value)

			__generateDMC__(directory,fileroot,sub_path,local_baseName,template_Name)
			__optJastrows__(directory,fileroot,sub_path,local_baseName)

def __generateDMC__(directory,fileroot,sub_path,baseName,template_Name):
    import os
    ################################################
    #### Generate : Opt.xml
    ################################################
    import lxml
    from lxml import etree

    os.system("cp misc/"+template_Name+" " +directory +"/DMC/DMC.xml")
    os.system("cp utils/format_data.py " +directory +"/DMC/")

    myFile = directory+"/DMC/DMC.xml"
    tree = etree.parse(myFile)
    ## Modify Cusp.xml for your system

    root = tree.getroot()

    project = root[0]
    icld_ptcl = root[2]
    icld_wfs = root[3]
    
    projName = "DMC-"+fileroot
    project.set("id",projName)

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

    ################################################
    ### Generate bgq-DMC.sh
    ################################################
    os.system("cp misc/bgq-DMC.sh "+directory+"/DMC/")


