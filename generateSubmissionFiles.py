class generateSubmissionFiles:
	def __init__(self,path,rootname,inputFile,basis,multiplicity,pseudo,num_det):
		self.path = path
		self.rootname = rootname
		self.inputFile = inputFile
		self.basis = basis
		self.multiplicity = multiplicity
		self.pseudo = pseudo
		self.num_determinants = num_det
		### ezfio_filename
		### fci_dumpname
		### scf_dumpname
		### hamiltonian_rootname
		### qmc_rootname
		### ezfio_filename
		### SCF_out_filename


	def generateHamiltonian(self,hamiltonian_rootname):
		#################################################
		#### GENERATE THE HAMILTONIAN IN ITS OWN XML FILE
		#################################################
		
        	
		self.hamiltonian_rootname = hamiltonian_rootname 
		path = self.path
        	
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
         
	def generateOptBlocks(self,append):
		path = self.path
		qmc_rootname = self.qmc_rootname+str(append)
		hamName = self.hamiltonian_rootname
		##########################################
		#### GENERATE THE QMC RUN FOR OPTIMIZATION
        	##########################################
		header= "<xml version=\"1.0\" ?>\n"
		header=header+ "<simulation>\n"
		header = header+" <project id=\"opt\" series= \"0\">\n"
        	header = header+" </project>\n"
	        header=header+ "<include href=\""+qmc_rootname+".wfs.xml\"/>  <!-- define trial wavefunction --> \n"
	        header=header+ "<include href=\""+qmc_rootname+".ptcl.xml\"/>  <!-- define particlesets: ions and e --> \n"
		header=header + "<include href=\""+hamName+".ham.xml\"/>  <!-- define hamiltonian --> \n"
	
                ## generate the optimization block
		optimizationBlock=""
		ending = "</simulation>\n"
	
        	fileOutName = path+"/"+qmc_rootname+".opt.xml"
		with open(fileOutName,"w") as fileOut:
			fileOut.write("%s" %header)
			fileOut.write("%s" %optimizationBlock)
        		fileOut.write("%s" %ending)

	def generateDMCBlocks(self,append):
		path = self.path
		qmc_name = self.qmc_rootnam+str(append)e
		hamName = self.hamiltonian_rootname
		##########################################
        	#### GENERATE THE DMC RUN BLOCK     ######
		##########################################
		header= "<xml version=\"1.0\" ?>\n"
		header=header+ "<simulation>\n"
        	header = header+" <project id=\"dmc\" series= \"0\">\n"
		header = header+" </project>\n"
	        header=header+ "<include href=\""+qmc_name+".wfs.xml\"/>  <!-- define trial wavefunction --> \n"
	        header=header+ "<include href=\""+qmc_name+".ptcl.xml\"/>  <!-- define particlesets: ions and e --> \n"
        	header=header + "<include href=\""+hamName+".ham.xml\"/>  <!-- define hamiltonian --> \n"
		
	
		### default to generate optimization and dmc blocks
                dmcBlock=""
		ending = "</simulation>\n"
		fileOutName = path +"/"+qmc_name+".dmc.xml"
		with open(fileOutName,"w") as fileOut:
        		fileOut.write("%s" %header)
			fileOut.write("%s" %dmcBlock)
			fileOut.write("%s" %ending)
	
        def generateVMCBlocks(self,append):
		path = self.path
		qmc_name = self.qmc_rootname+str(append)
		hamName = self.hamiltonian_rootname
		##########################################
		#### GENERATE THE VMC RUN BLOCK     ######
		##########################################
        	header= "<xml version=\"1.0\" ?>\n"
		header=header+ "<simulation>\n"
		header = header+" <project id=\"vmc\" series= \"0\">\n"
		header = header+" </project>\n"
                header=header+ "<include href=\""+qmc_name+".wfs.xml\"/>  <!-- define trial wavefunction --> \n"
	        header=header+ "<include href=\""+qmc_name+".ptcl.xml\"/>  <!-- define particlesets: ions and e --> \n"
		header=header + "<include href=\""+hamName+".ham.xml\"/>  <!-- define hamiltonian --> \n"
		
        	## generate optimization blocks and vmc blocks
		vmcBlock=""
		ending = "</simulation>\n"
		fileOutName = path+"/"+qmc_name+".vmc.xml"
        	with open(fileOutName,"w") as fileOut:
			fileOut.write("%s" %header)
			fileOut.write("%s" %vmcBlock)
			fileOut.write("%s" %ending)

	  
	def generateMasterSubmissionFile(self):
		path = self.path
		rootname  = self.rootname
		##########################################
        	#### GENERATE THE MASTER SUBMISSION FILE # 
		#### THIS WILL BE ABLE TO EXECUTE THE CALCULATION
		#### FROM SCF INPUT TO QMC OUTPUT
		##########################################

		file = "#!/bin/bash\nACCT=QMCPACK\n"
	
		##################################
        	### CREATE THE EZFIO AND RUN SCF
		##################################
	
		qp_calculation1()
        	qp_submission1()
	
		file = file+ "TIME=12:00:00\nNODES=8\n\n"
		file =file + "OUTPUT="+rootname+"_scf_output\n"
        	subFile = path+"/"+"qp_submission1_"+rootname+".sh"
		file =file+ "qsub -A $ACCT -t $TIME -n $NODES -O OUTPUT ./"+subFile
	
	
        	##################################
		### DO THE AO TO MO TRANSFORMATION
		##################################
	
        	qp_calculation2()
		qp_submission2()
	
		file = file+ "TIME=1:00:00\nNODES=1\n\n"
        	file =file + "OUTPUT="+rootname+"_ao2mo_output\n"
		subFile = path+"/"+"qp_submission2_"+rootname+".sh"
		file =file+ "qsub -A $ACCT -t $TIME -n $NODES -O OUTPUT ./"+subFile
	
        
		##################################
		### RUN THE FCI_ZMQ CALCULATION 
		##################################

		qp_calculation3()
		qp_submission3()
	
        	file = file+ "TIME=12:00:00\nNODES=8\n\n"
		file =file + "OUTPUT="+rootname+"_fci_output\n"
		subFile = path+"/"+"qp_submission3_"+rootname+".sh"
		file =file+ "qsub -A $ACCT -t $TIME -n $NODES -O OUTPUT ./"+subFile

	
		##################################
		### DO THE CONVERSIONS FOR QMCPACK
        	##################################
		
		qp_calculation4()
		qp_submission4()

		file = file+ "TIME=1:00:00\nNODES=1\n\n"
		file =file + "OUTPUT="+rootname+"_conversion_output\n"
		subFile = path+"/"+"qp_submission4_"+rootname+".sh"
        	file =file+ "qsub -A $ACCT -t $TIME -n $NODES -O OUTPUT ./"+subFile
	
	
		
        	submissionFile = path+"/"+"masterSubmission_"+rootname+".sh"
		with open(submissionFile,"w") as fileOut:
			fileOut.write(header)
			fileOut.write(outputline)
        		fileOut.write(qsubline)
	
	
	def qp_submission1(self):
        	#### THIS FUNCTION CREATES THE SUBMISSION FILE FOR THE SCF CALCULATION
		rootname = self.rootname
	
		header =" #!/bin/bash\n"
		header = header+ "source /soft/applications/quantum_package/quantum_package.rc\n"
        	header = header+"MPIRUN=True\n"
		header = header+"chmod 744 qp_submission1_"+rootname+".py\n"
		header = header+"./qp_submission1_"+rootname+".py $MPIRUN\n"
	
        	### CREATE SUBMISSION FILE FOR QP calcs
		subFile =path +"/"+ "qp_submission1_"+rootname+".sh"
		with open(subFile, "w") as fileOut:
			fileOut.write("%s" %header)
        
	def qp_calculation1(self):

		path = self.path
		rootname = self.rootname
		inputFile = self.inputFile
		basis = self.basis
		m = self.multiplicity
		psuedo= self.pseudo
		##############################################
		#### GENERATE THE CALCULATION FILE THAT WILL 
        	#### BE CALLED IN THE SUBMISSION FILE
		##############################################
		ezfio_filename = path + "/"+rootname + ".ezfio"
		SCF_out_filename =path + "/"+ rootname + ".SCF.out"

		self.ezfio_filename = ezfio_filename
		self.SCF_out_filename = SCF_out_filename
        
		### BEGIN FILECREATION
		fileHeader="#!/usr/bin/env python \n# -*- coding: utf-8 -*- \n"
		fileHeader=fileHeader + "
        	fileHeader=fileHeader + "#THIS FILE CREATES THE EZFIO AND RUNS THE SCF CALCULATION \n \n"
		fileHeader=fileHeader + "import os \nimport sys \nfrom ezfio import ezfio \n"
		fileHeader=fileHeader + "mpirun=sys.argv[1]\n"
	
        	fileMain = "### first create the ezfio file\n"
		if usePP:
			fileMain =fileMain+ "os.system(\"qp_create_ezfio_from_xyz " + str(inputFile)+ " -b \'"+str(basis)+"\' -m "+str(m)+" -p "+str(usePP)+" -o " +ezfio_filename+"\")\n"
		else:
        		fileMain =fileMain+ "os.system(\"qp_create_ezfio_from_xyz " + str(inputFile)+ " -b \'"+str(basis)+"\' -m "+str(m)+" -o " +ezfio_filename+"\")\n"
		fileMain = fileMain+"ezfio.set_file(\""+ezfio_filename+"\")\n"
		fileMain = fileMain +"ezfio.set_determinants_n_det_max(1)\n"
		fileMain = fileMain +"ezfio.set_integrals_bielec_disk_access_ao_integrals(\"Write\")\n"
        	fileMain = fileMain +"ezfio.set_integrals_bielec_disk_access_mo_integrals(\"Write\")\n"
		fileMain = fileMain +"ezfio.set_integrals_monoelec_disk_access_ao_one_integrals(\"Write\")\n"
		fileMain = fileMain +"ezfio.set_integrals_monoelec_disk_access_mo_one_integrals(\"Write\")\n"
	
        	fileMain = fileMain +"### Now run the SCF calculation\n"
		fileMain = fileMain +"if mpirun.lower()[0]==\"t\":\n"
		fileMain = fileMain +"   os.system(\"./qp-mpirun.sh SCF "+ezfio_filename+"/ > "+SCF_out_filename+"\")\n"
		fileMain = fileMain +"else:\n"
        	fileMain = fileMain +"   os.system(\"qp_run SCF "+ezfio_filename+"/ > "+SCF_out_filename+"\")\n"
	
		fileoutName =path+"/"+ "qp_submission1_"+rootname+".py"
		with open(fileoutName,"w") as fileout:
        		fileout.write("%s" %fileHeader)
			fileout.write("%s" %fileMain)
	
	def qp_submission2(self):
        	##############################################
		#### GENERATE THE SUBMISSION FILE FOR AO 2 MO
		##############################################
		rootname = self.rootname
		path = self.path	

        	header =" #!/bin/bash\n"
		header = header+ "source /soft/applications/quantum_package/quantum_package.rc\n"
		header = header+"MPIRUN=False\n"
		header = header+"chmod 744 qp_submission2_"+rootname+".py\n"
        	header = header+"./qp_submission2_"+rootname+".py $MPIRUN\n"
	
		### CREATE SUBMISSION FILE FOR AO 2 MO TRANSFORMATION
		subFile =path +"/"+ "qp_submission2_"+rootname+".sh"
        	with open(subFile, "w") as fileOut:
			fileOut.write("%s" %header)
	
	def qp_calculation2(path,rootname,NDET):
        	##############################################
		#### GENERATE THE CALCULATION FILE THAT WILL 
		#### BE CALLED IN THE SUBMISSION FILE
		##############################################
		path = self.path
		rootname= self.rootname
		NDET = self.num_determinants
        	ezfio_filename = self.ezfio_filename
		dump_filename =path + "/"+ rootname + ".1det.dump"
		self.scf_dumpname = dump_filename
		A2M_out_filename =path + "/"+ rootname + ".ao2mo.out"
		


	
        	### BEGIN FILECREATION
	
		fileHeader="#!/usr/bin/env python \n# -*- coding: utf-8 -*- \n"
		fileHeader=fileHeader + "#THIS FILE CREATES THE EZFIO, RUNS THE SCF CALCULATION, AND THEN RUNS THE FCI CALCULATION \n \n"
        	fileHeader=fileHeader + "import os \nimport sys \nfrom ezfio import ezfio \n\n"
	
		fileMain = fileMain+"ezfio.set_file(\""+ezfio_filename+"\")\n"
	
        	fileMain = fileMain +"### convert the ao to mo"
		## ONCE THE ITERATIVE IS ESTABLISHED IN QUANTUM PACKAGE UNCOMMENT THIS LINE
		#fileMain = fileMain +"ezfio.set_full_ci_zmq_iterative(True)\n"
		fileMain = fileMain +"os.system(\"qp_run fci_zmq "+ezfio_filename+"/ > "+A2M_out_filename+"\")\n"
        	fileMain = fileMain +"### Now save the 1 det system for qmcpack\n"
		fileMain = fileMain +""os.system(\"qp_run save_for_qmcpack "+ezfio_filename+"/ > "+dump_filename+"\")\n"
		fileMain = fileMain +"ezfio.set_determinants_n_det_max("+str(NDET)+")\n"
		fileMain = fileMain +"ezfio.set_determinants_read_wf(True)\n"
        	
		fileoutName =path+"/"+ "qp_submission2_"+rootname+".py"
		with open(fileoutName,"w") as fileout:
			fileout.write("%s" %fileHeader)
        		fileout.write("%s" %fileMain)
	
	def qp_submission3(self):

		##############################################
        	#### GENERATE THE SUBMISSION FILE FOR FCI CALC
		##############################################
		path = self.path
		rootname = self.rootname
		header =" #!/bin/bash\n"
		header = header+ "source /soft/applications/quantum_package/quantum_package.rc\n"
        	header = header+"MPIRUN=True\n"
		header = header+"chmod 744 qp_submission3_"+rootname+".py\n"
		header = header+"./qp_submission3_"+rootname+".py $MPIRUN\n"
	
        	### CREATE SUBMISSION FILE FOR QP calcs
		subFile =path +"/"+ "qp_submission3_"+rootname+".sh"
		with open(subFile, "w") as fileOut:
			fileOut.write("%s" %header)

	def qp_calculation3(path,rootname):
		##############################################
		#### GENERATE THE CALCULATION FILE THAT WILL 
        	#### BE CALLED IN THE SUBMISSION FILE
		##############################################
		path = self.path
		rootname = self.rootname
		ezfio_filename =self.ezfio_filename 
		FCI_out_filename =path + "/"+ rootname + ".FCI.out"

		### BEGIN FILECREATION
		fileHeader="#!/usr/bin/env python \n# -*- coding: utf-8 -*- \n"
		fileHeader=fileHeader + "#THIS FILE CREATES THE EZFIO, RUNS THE SCF CALCULATION, AND THEN RUNS THE FCI CALCULATION \n \n"
        	fileHeader=fileHeader + "import os \nimport sys \nfrom ezfio import ezfio \n"
		fileHeader=fileHeader + "mpirun=sys.argv[1]\n"
	
		fileMain = fileMain+"ezfio.set_file(\""+ezfio_filename+"\")\n"

		fileMain = fileMain +"### run the cipsi calculation"
		fileMain = fileMain +"if mpirun.lower()[0]==\"t\":\n"
		fileMain = fileMain +"   os.system(\"./qp-mpirun.sh fci_zmq "+ezfio_filename+"/ > "+FCI_out_filename+"\")\n"
        	fileMain = fileMain +"else:\n"
		fileMain = fileMain +"   os.system(\"qp_run fci_zmq "+ezfio_filename+"/ > "+FCI_out_filename+"\")\n"
	
		fileoutName =path+"/"+ "qp_submission3_"+rootname+".py"
        	with open(fileoutName,"w") as fileout:
			fileout.write("%s" %fileHeader)
			fileout.write("%s" %fileMain)
	
        def qp_submission4(path,rootname):
		##############################################
		#### GENERATE THE SUBMISSION FILE FOR QP CALC
		#### AND THEN CONVERSION TO QMC
        	##############################################
		path = self.path
		rootname = self.rootname
		header =" #!/bin/bash\n"
		header = header+ "source /soft/applications/quantum_package/quantum_package.rc\n"
		header = header+"MPIRUN=True\n"
        	header = header+"chmod 744 qp_submission4_"+rootname+".py\n"
		header = header+"./qp_submission4_"+rootname+".py $MPIRUN\n"
	
		### CREATE SUBMISSION FILE FOR QP calcs
        	subFile =path +"/"+ "qp_submission4_"+rootname+".sh"
		with open(subFile, "w") as fileOut:
			fileOut.write("%s" %header)
	
        def calculation4(scf_rootname,rootname):

		##############################################
		#### GENERATE THE CALCULATION FILE THAT WILL 
		#### BE CALLED IN THE SUBMISSION FILE
        	##############################################
		path = self.path
		rootname = self.rootname
		ezfio_filename = self.ezfio_filename
		SCF_dump_filename = self.scf_dumpname
		FCI_dump_filename = rootname + ".FCI.dump"
		self.fci_dumpname = FCI_dump_filename
        
		BINDIR=/soft/applications/qmcpack/github/build_Intel_real/bin 
	
		### BEGIN FILECREATION

		fileHeader="#!/usr/bin/env python \n# -*- coding: utf-8 -*- \n"
		fileHeader=fileHeader + "#THIS FILE MAKES THE INPUT FILES TO QMCPACK \n \n"
		fileHeader=fileHeader + "import os \nimport sys \nfrom ezfio import ezfio \n"
        
		fileMain ="os.system(\"qp_run save_for_qmcpack "+ezfio_filename+"/ > "+FCI_dump_filename+"\")\n"
		### NO JASTROW AND 1 DET		
		main = "os.system(\""+BINDIR+"/convert4qmc -QP "+SCF_dump_filename+" -addCusp\" )\n"
        	main = main+"os.system(\"mv sample.Gaussian-G2.xml " +scf_rootname+"_1Det_NoJastrow.wfs.xml\")\n"
		main = main+"os.system(\"mv sample.Gaussian-G2.ptcl.xml " +scf_rootname+"_1Det_NoJastrow.ptcl.xml\")\n"
	
		### PLAIN JASTROW AND 1 DET		
        	main = main+"os.system(\""+BINDIR+"/convert4qmc -QP "+SCF_dump_filename+" -add3BodyJ -addCusp\" )\n"
		main = main+"os.system(\"mv sample.Gaussian-G2.xml " +scf_rootname+"_1Det_Jastrow.wfs.xml\")\n"
		main = main+"os.system(\"mv sample.Gaussian-G2.ptcl.xml " +scf_rootname+"_1Det_Jastrow.ptcl.xml\")\n"
	
        	### NO JASTROW AND MULTI-DETERMINANT
		main = main+"os.system(\""+BINDIR+"/convert4qmc -QP "+FCI_dump_filename+" -addCusp \" )\n"
		main = main+"os.system(\"mv sample.Gaussian-G2.xml " +rootname+"_NoJastrow.wfs.xml\")\n"
		main = main+"os.system(\"mv sample.Gaussian-G2.ptcl.xml " +rootname+"_NoJastrow.ptcl.xml\")\n"
        
		### PLAIN JASTROW AND MULTI-DETERMINANT
		main = main+"os.system(\""+BINDIR+"/convert4qmc -QP "+FCI_dump_filename+" -add3BodyJ -addCusp\" )\n"
		main = main+"os.system(\"mv sample.Gaussian-G2.xml " +rootname+"_Jastrow.wfs.xml\")\n"
        	main = main+"os.system(\"mv sample.Gaussian-G2.ptcl.xml " +rootname+"_Jastrow.ptcl.xml\")\n"
	
		### OPTIMIZED JASTROW AND MULTI-DETERMINANT
		main = main+"os.system(\""+BINDIR+"/convert4qmc -QP "+FCI_dump_filename+" -add3BodyJ -addCusp\" )\n"
        	main = main+"os.system(\"mv sample.Gaussian-G2.xml " +rootname+"_ReOptJastrow.wfs.xml\")\n"
		main = main+"os.system(\"mv sample.Gaussian-G2.ptcl.xml " +rootname+"_ReOptJastrow.ptcl.xml\")\n"
	
	
        	fileoutName =path+"/"+ "qp_submission4_"+rootname+".py"
		with open(fileoutName,"w") as fileout:
			fileout.write("%s" %fileHeader)
			fileout.write("%s" %fileMain)
