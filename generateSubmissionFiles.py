def generateCalculationFileQP_SCF_FCI(path,filepath,basis,m,rootname,NDET,usePP):
	##############################################
	#### GENERATE THE CALCULATION FILE THAT WILL 
	#### BE CALLED IN THE SUBMISSION FILE
	##############################################
	ezfio_filename = path + "/"+rootname + ".ezfio"
	SCF_out_filename =path + "/"+ rootname + ".SCF.out"
	FCI_out_filename =path + "/"+ rootname + ".FCI.out"
	SCF_dump_filename =path + "/"+ rootname + ".SCF.dump"
	FCI_dump_filename =path + "/"+ rootname + ".FCI.dump"


	### BEGIN FILECREATION

	fileHeader="#!/usr/bin/env python \n"
	fileHeader=fileHeader + "# -*- coding: utf-8 -*- \n"
	fileHeader=fileHeader + "#THIS FILE CREATES THE EZFIO, RUNS THE SCF CALCULATION, AND THEN RUNS THE FCI CALCULATION \n \n"
	fileHeader=fileHeader + "import os \n"
	fileHeader=fileHeader + "import sys \n"
	fileHeader=fileHeader + "from ezfio import ezfio \n"
	fileHeader=fileHeader + "mpirun=sys.argv[1]\n"

	fileMain = "### first create the ezfio file\n"
	if usePP:
		fileMain =fileMain+ "os.system(\"qp_create_ezfio_from_xyz " + str(inputFile)+ " -b \'"+str(basis)+"\' -m "+str(m)+" -p "+str(usePP)+" -o " +ezfio_filename+"\")\n"
	else:
		fileMain =fileMain+ "os.system(\"qp_create_ezfio_from_xyz " + str(inputFile)+ " -b \'"+str(basis)+"\' -m "+str(m)+" -o " +ezfio_filename+"\")\n"
	fileMain = fileMain+"ezfio.set_file(\""+ezfio_filename+"\")\n"
	fileMain = fileMain +"ezfio.set_determinants_n_det_max("+str(NDET)+")\n"
	fileMain = fileMain +"ezfio.set_integrals_bielec_disk_access_ao_integrals(\"Write\")\n"
	fileMain = fileMain +"ezfio.set_integrals_bielec_disk_access_mo_integrals(\"Write\")\n"
	fileMain = fileMain +"ezfio.set_integrals_monoelec_disk_access_ao_one_integrals(\"Write\")\n"
	fileMain = fileMain +"ezfio.set_integrals_monoelec_disk_access_mo_one_integrals(\"Write\")\n"

	fileMain = fileMain +"### Now run the SCF calculation\n"
	fileMain = fileMain +"if mpirun.lower()[0]==\"t\":\n"
	fileMain = fileMain +"   os.system(\"./qp-mpirun.sh SCF "+ezfio_filename+"/ > "+SCF_out_filename+"\")\n"
	fileMain = fileMain +"   os.system(\"qp_run save_for_qmcpack "+ezfio_filename+"/ > "+SCF_dump_filename+"\")\n"
	fileMain = fileMain +"else:\n"
	fileMain = fileMain +"   os.system(\"qp_run SCF "+ezfio_filename+"/ > "+SCF_out_filename+"\")\n"
	fileMain = fileMain +"   os.system(\"qp_run save_for_qmcpack "+ezfio_filename+"/ > "+SCF_dump_filename+"\")\n"

	fileMain = fileMain +"### then run the cipsi calculation"
	## ONCE THE ITERATIVE IS ESTABLISHED IN QUANTUM PACKAGE UNCOMMENT THIS LINE
	#fileMain = fileMain +"ezfio.set_full_ci_zmq_iterative(True)\n"
	fileMain = fileMain +"if mpirun.lower()[0]==\"t\":\n"
	fileMain = fileMain +"   os.system(\"./qp-mpirun.sh fci_zmq "+ezfio_filename+"/ > "+FCI_out_filename+"\")\n"
	fileMain = fileMain +"   os.system(\"qp_run save_for_qmcpack "+ezfio_filename+"/ > "+FCI_dump_filename+"\")\n"
	fileMain = fileMain +"else:\n"
	fileMain = fileMain +"   os.system(\"qp_run fci_zmq "+ezfio_filename+"/ > "+FCI_out_filename+"\")\n"
	fileMain = fileMain +"   os.system(\"qp_run save_for_qmcpack "+ezfio_filename+"/ > "+FCI_dump_filename+"\")\n"

	fileoutName =path+"/"+ "qp_submission1_"+rootname+".py"
	with open(fileoutName,"w") as fileout:
		fileout.write("%s" %fileHeader)
		fileout.write("%s" %fileMain)

def generateSubmissionFileQP_SCF_FCI(path,scf_rootname,rootname):
	##############################################
	#### GENERATE THE SUBMISSION FILE FOR QP CALC
	#### AND THEN CONVERSION TO QMC
	##############################################
	SCF_dump_filename = rootname + ".SCF.dump"
	FCI_dump_filename = rootname + ".FCI.dump"

	header =" #!/bin/bash\n"
	header = header+ "source /soft/applications/quantum_package/quantum_package.rc\n"
	header = header+"MPIRUN=True\n"
	header = header+"chmod 744 qp_submission1_"+rootname+".py\n"
	header = header+"./qp_submission1_"+rootname+".py $MPIRUN\n"

	##### CONVERT THE RESULTS FROM CIPSI/HF METHODS INTO QMC INPUT
	##### ONLY THE WAVEFUNCTION AND PARTICLESET


	### NO JASTROW AND 1 DET		
	main = "os.system(\"convert4qmc -QP "+SCF_dump_filename+" -nojastrow \" )\n"
	main = main+"os.system(\"mv sample.Gaussian-g2.xml " +scf_rootname+"_1Det_NoJastrow.wfs.xml\")\n"
	main = main+"os.system(\"mv sample.Gaussian-g2.ptcl.xml " +scf_rootname+"_1Det_NoJastrow.ptcl.xml\")\n"

	### PLAIN JASTROW AND 1 DET		
	main = main+"os.system(\"convert4qmc -QP "+SCF_dump_filename+"\" )\n"
	main = main+"os.system(\"mv sample.Gaussian-g2.xml " +scf_rootname+"_1Det_Jastrow.wfs.xml\")\n"
	main = main+"os.system(\"mv sample.Gaussian-g2.ptcl.xml " +scf_rootname+"_1Det_Jastrow.ptcl.xml\")\n"

	### NO JASTROW AND MULTI-DETERMINANT
	main = main+"os.system(\"convert4qmc -QP "+FCI_dump_filename+" -nojastrow \" )\n"
	main = main+"os.system(\"mv sample.Gaussian-g2.xml " +rootname+"_NoJastrow.wfs.xml\")\n"
	main = main+"os.system(\"mv sample.Gaussian-g2.ptcl.xml " +rootname+"_NoJastrow.ptcl.xml\")\n"

	### PLAIN JASTROW AND MULTI-DETERMINANT
	main = main+"os.system(\"convert4qmc -QP "+FCI_dump_filename+"\" )\n"
	main = main+"os.system(\"mv sample.Gaussian-g2.xml " +rootname+"_Jastrow.wfs.xml\")\n"
	main = main+"os.system(\"mv sample.Gaussian-g2.ptcl.xml " +rootname+"_Jastrow.ptcl.xml\")\n"

	### OPTIMIZED JASTROW AND MULTI-DETERMINANT
	main = main+"os.system(\"convert4qmc -QP "+FCI_dump_filename+"\" )\n"
	main = main+"os.system(\"mv sample.Gaussian-g2.xml " +rootname+"_ReOptJastrow.wfs.xml\")\n"
	main = main+"os.system(\"mv sample.Gaussian-g2.ptcl.xml " +rootname+"_ReOptJastrow.ptcl.xml\")\n"

	### CREATE SUBMISSION FILE FOR QP calcs
	subFile =path +"/"+ "qp_submission1_"+rootname+".sh"
	with open(subFile, "w") as fileOut:
		fileOut.write("%s" %header)
		fileOut.write("%s" %main)

def generateHamiltonian(path,rootname):
	#################################################
	#### GENERATE THE HAMILTONIAN IN ITS OWN XML FILE
	#################################################
    
	hamiltonian_rootname = rootname

	header = "<?xml version=\"1.0\"?>\n"
	header =header+ "<!-- paripot@type=(coulomb, pseudo) -->\n"
	header = header + "<qmcsystem>\n"
        header = header+ "<hamiltonian name=\"h0\" type=\"generic\" target=\"e\">\n"
	header = header+ "<pairpot name=\"ElecElec\" type=\"coulomb\" source=\"e\" target=\"e\"/>\n"
	header = header + "<pairpot name=\"ElecIon\" type=\"coulomb\" source=\"ion0\" target=\"e\"/>\n"
	header = header+ "<pairpot name=\"IonIon\" type=\"coulomb\" source=\"ion0\" target=\"ion0\"/>\n"
        header = header+ "</hamiltonian>\n"
	header = header+ "</qmcsystem>\n"
	
	hamiltonian_filename =path+"/"+ hamiltonian_rootname+".ham.xml"

	print hamiltonian_filename
	with open(hamiltonian_filename,"w") as fileOut:
		fileOut.write("%s" %header)
 
def generateOptBlocks(path,rootname,hamName):
	##########################################
	#### GENERATE THE QMC RUN FOR OPTIMIZATION
	##########################################
	header= "<xml version=\"1.0\" ?>\n"
	header=header+ "<simulation>\n"
	header = header+" <project id=\"opt\" series= \"0\">\n"
	header = header+" </project>\n"
        header=header+ "<include href=\""+rootname+".wfs.xml\"/>  <!-- define trial wavefunction --> \n"
        header=header+ "<include href=\""+rootname+".ptcl.xml\"/>  <!-- define particlesets: ions and e --> \n"
	header=header + "<include href=\""+hamName+".ham.xml\"/>  <!-- define hamiltonian --> \n"
	
        ## generate the optimization block
	optimizationBlock=""
	ending = "</simulation>\n"

	fileOutName = path+"/"+rootname+".opt.xml"
	with open(fileOutName,"w") as fileOut:
		fileOut.write("%s" %header)
		fileOut.write("%s" %optimizationBlock)
		fileOut.write("%s" %ending)

def generateDMCBlocks(path,rootname,hamName):
	##########################################
	#### GENERATE THE DMC RUN BLOCK     ######
	##########################################
	header= "<xml version=\"1.0\" ?>\n"
	header=header+ "<simulation>\n"
	header = header+" <project id=\"dmc\" series= \"0\">\n"
	header = header+" </project>\n"
        header=header+ "<include href=\""+rootname+".wfs.xml\"/>  <!-- define trial wavefunction --> \n"
        header=header+ "<include href=\""+rootname+".ptcl.xml\"/>  <!-- define particlesets: ions and e --> \n"
	header=header + "<include href=\""+hamName+".ham.xml\"/>  <!-- define hamiltonian --> \n"
	

	### default to generate optimization and dmc blocks
        dmcBlock=""
	ending = "</simulation>\n"
	fileOutName = path +"/"+rootname+".dmc.xml"
	with open(fileOutName,"w") as fileOut:
		fileOut.write("%s" %header)
		fileOut.write("%s" %dmcBlock)
		fileOut.write("%s" %ending)

def generateVMCBlocks(path,rootname,hamName):
	##########################################
	#### GENERATE THE VMC RUN BLOCK     ######
	##########################################
	header= "<xml version=\"1.0\" ?>\n"
	header=header+ "<simulation>\n"
	header = header+" <project id=\"vmc\" series= \"0\">\n"
	header = header+" </project>\n"
        header=header+ "<include href=\""+rootname+".wfs.xml\"/>  <!-- define trial wavefunction --> \n"
        header=header+ "<include href=\""+rootname+".ptcl.xml\"/>  <!-- define particlesets: ions and e --> \n"
	header=header + "<include href=\""+hamName+".ham.xml\"/>  <!-- define hamiltonian --> \n"
	
	## generate optimization blocks and vmc blocks
	vmcBlock=""
	ending = "</simulation>\n"
	fileOutName = path+"/"+rootname+".vmc.xml"
	with open(fileOutName,"w") as fileOut:
		fileOut.write("%s" %header)
		fileOut.write("%s" %vmcBlock)
		fileOut.write("%s" %ending)

  
def generateMasterSubmissionFile(path,rootname):
	##########################################
	#### GENERATE THE MASTER SUBMISSION FILE # 
	#### THIS WILL BE ABLE TO EXECUTE THE CALCULATION
	#### FROM SCF INPUT TO QMC OUTPUT
	##########################################
	subFile = path+"/"+"qp_submission1_"+rootname+".sh"

	######################################################
	### CREATE CONVERSION FILE FOR QMC
	
	header = "#!/bin/bash\nACCT=QMCPACK\nTIME=12:00:00\nNODES=8\n\n"
	outputline = "OUTPUT="+rootname+"_output\n"
	qsubline = "qsub -A $ACCT -t $TIME -n $NODES -O OUTPUT ./"+subFile
	
	submissionFile = path+"/"+"masterSubmission_"+rootname+".sh"
	with open(submissionFile,"w") as fileOut:
		fileOut.write(header)
		fileOut.write(outputline)
		fileOut.write(qsubline)


