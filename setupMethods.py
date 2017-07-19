def useQuantumPackageMethod(filename,nojastrow,use3Body):
	'''
	 The function that will take the dump file from quantum package
		 and generate the needed files to run QMC with qmcpack
	'''
	import os,sys

	numDetMatch = "Number of determinants"
	dirName =""
	flags=""
	if nojastrow:
		dirName=dirName+"NoJastrow_"
		flags = flags+ "-nojastrow "
	elif use3Body:
		dirName=dirName+"Jastrow123_"
		flags = flags+"-add3BodyJ "
	else:
		dirName=dirName+"Jastrow12_"
	with open(filename, "r") as fileIn:
		for line in fileIn:
			if  numDetMatch in line:
				line = line[len(numDetMatch)+2:]
				numDet = int(line)
			elif "QMCPACK" in line:
				line = line[1:]
				line = line.split("->")
				convertType = line[0].replace(" ","")
			elif "do_pseudo" in line:
				line=line.split(" ")
				doPseudo=line[1][0].lower()=="t"
			elif "multi_det" in line:
				line=line.split(" ")
				multidet=line[1][0].lower()=="t"


	if convertType !="QP":
		print "There is an error: Are you sure this was generated with quantum package?"
    		sys.exit(1)
		
	#print numDet
	#print convertType
	#print doPseudo
	#print multidet


	fileroot = filename.split('.')[0]
	#print fileroot

	if not(doPseudo):
		flags = flags +"-addCusp "

	if multidet:
		dirName = dirName +"MultiDet"
	else:
		dirName = dirName +"1Det"

	
	os.mkdir(dirName)
	local_fileroot = dirName +"/"+fileroot
	print "The input files will be place in ",local_fileroot

	os.system("./converter_independent.py "+convertType+" "+ filename+" "+ local_fileroot+" "+ flags)


	absfileroot = os.getcwd() + "/"+dirName + "/"+ fileroot
	os.system("./misc/setupCuspCorrection.py "+dirName+ " " + absfileroot,multidet)
	
	if multidet:
		### this will call another program which will generate
		### cutoff directories containing 
		### optimization and DMC folders
		os.system("./misc/generateCutoffDirs4QMC.py")
	else:
		### generate the DMC and Optimization folders
		os.system("./misc/setupDMCFolder.py " + dirName + " " + absfileroot + " " +fileroot + "  " +doPseudo)

'''
	### create the DMC folder
	### create this first because if the system uses a pseudopotential
	### we will modify the hamiltonian in later steps
	os.system("./misc/setupDMCFolder.py " +dirName +" "+ fileroot)
	

	### setup the Optimization folder if needed
	if not(nojastrow):
		### must optimize jastrows
		os.system("./misc/setupOptFolder.py ")
		
	if not(doPseudo):
		### must create CuspCorrection folder
		os.system("./misc/setupCuspFolder.py ")

	else:
		## only modify the Opt.xml and DMC.xml files because the Cusp.xml is only generated for AE calcs.
		os.system("./misc/modifyHamiltonians.py")

'''
