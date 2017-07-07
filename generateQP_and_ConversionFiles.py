import os
from generateQMCFiles import *
class generateQP_and_ConversionFiles:     
    def __init__(self,main_filepath_args,filename1_args,filename2_args,parameters_args):

        self.main_filepath_args=main_filepath_args
	self.filename1_args=filename1_args
	self.filename2_args =filename2_args
	self.parameters_args=parameters_args

	#self.path,self.rootname,self.sub_path,self.ezfio_filename = main_filepath_args
        #self.scf_dumpname,self.SCF_out_filename,self.fci_dumpname,self.FCI_out_filename,self.A2M_out_filename=filename1_args     
        #self.pythonCalculationFilename1,self.pythonCalculationFilename2,self.pythonCalculationFilename3,self.pythonCalculationFilename4=filename2_args 
        #self.inputFile, self.NDET,self.basis, self.m,self.pp,self.otherArguments=parameters_args


	### Within the defs use the following declarations
   	#####path,rootname,sub_path,ezfio_filename = self.main_filepath_args
        #####scf_dumpname,SCF_out_filename,fci_dumpname,FCI_out_filename,A2M_out_filename=self.filename1_args     
        #####pythonCalculationFilename1,pythonCalculationFilename2,pythonCalculationFilename3,pythonCalculationFilename4=self.filename2_args 
        #####inputFile, NDET,basis, m,pp,otherArguments=self.parameters_args




    def __buildQMCDirectories__(self,baseDir,fileroot):
	
	path,rootname,sub_path,ezfio_filename = self.main_filepath_args

	directory = path + "/"+ baseDir
	if not(os.path.isdir(directory)):
	    os.mkdir(directory)
	if not(os.path.isdir(directory+"/CuspCorrection")):
	    os.mkdir(directory+"/CuspCorrection")
	generateCuspCorrection(directory,fileroot,sub_path,baseDir)
	if not(os.path.isdir(directory+"/Optimization")):
    	    os.mkdir(directory+"/Optimization")
	generateOptimization(directory,fileroot,sub_path,baseDir)
	if not(os.path.isdir(directory+"/DMC")):
	    os.mkdir(directory+"/DMC")
	generateDMC(directory,fileroot,sub_path,baseDir)
        generateSystemSetup(directory,fileroot,sub_path)
        finalizeTemplate(directory, fileroot)


    def generateMasterFile(self):
   	path,rootname,sub_path,ezfio_filename = self.main_filepath_args
        pythonCalculationFilename1,pythonCalculationFilename2,pythonCalculationFilename3,pythonCalculationFilename4=self.filename2_args 
        inputFile, NDET,basis, m,pp,otherArguments=self.parameters_args

 
        doSCF=True
        if os.path.exists(path+"/1Det_NoJastrow"):
       	    doSCF=False

	self.doSCF=doSCF
        if doSCF:
    	    noJ_1det_base = "1Det_noJastrow"
            noJ_1det_path = path +"/"+noJ_1det_base
            noJ_1det_fileroot = rootname+"_"+noJ_1det_base
            self.__buildQMCDirectories__(noJ_1det_base,noJ_1det_fileroot)

    	    J_1det_base = "1Det_Jastrow"
            J_1det_path = path +"/"+J_1det_base
            J_1det_fileroot = rootname+"_"+ J_1det_base
            self.__buildQMCDirectories__(J_1det_base,J_1det_fileroot)

        noJ_Multidet_base = str(NDET)+"Det_NoJastrow" 
        noJ_Multidet_path = path +"/"+noJ_Multidet_base
        noJ_Multidet_fileroot=rootname +"_"+noJ_Multidet_base
        self.__buildQMCDirectories__(noJ_Multidet_base,noJ_Multidet_fileroot)

        J_Multidet_base =str(NDET)+"Det_Jastrow"
        J_Multidet_path = path +"/"+J_Multidet_base
        J_Multidet_fileroot=rootname +"_"+J_Multidet_base
        self.__buildQMCDirectories__(J_Multidet_base,J_Multidet_fileroot)

        J_Multidet_reopt_base =str(NDET)+"Det_Jastrow_reOpt"
        J_Multidet_reopt_path = path +"/"+J_Multidet_reopt_base
        J_Multidet_reopt_fileroot = rootname +"_"+J_Multidet_reopt_base
        self.__buildQMCDirectories__(J_Multidet_reopt_base,J_Multidet_reopt_fileroot)


	self.qmc_files = [noJ_1det_fileroot,noJ_1det_base,J_1det_base,J_1det_fileroot,noJ_Multidet_base,noJ_Multidet_fileroot,J_Multidet_base,J_Multidet_fileroot,J_Multidet_reopt_base,J_Multidet_reopt_fileroot]

		
        if doSCF:
            self.__generate_QP_SCFCalculation__()
            self.__generate_scfDump_ao2moTransform__()
        self.__generate_fciCalculation__()
	self.__generate_fciDump_conversions_qmcBlocks__()
	"""if arguments["vmc"]: 
		self.__generate_fciDump_conversions_qmcBlocks__("vmc")
	else:
		self._generate_fciDump_conversions_qmcBlocks__("dmc")
	"""

	os.system("cp misc/qp-mpirun.sh " +path +"/")

	### now output them into a master script

	##########################################
       	#### GENERATE THE SUBMISSION FILES  
	#### THIS WILL BE ABLE TO EXECUTE THE CALCULATION
	#### FROM SCF INPUT TO QMC OUTPUT
	##########################################


	##################################
	### CREATE THE EZFIO AND RUN SCF
	##################################
	file1 = "#!/bin/bash\nACCT=QMCPACK\n"
	file1 = file1+ "\nTIME=12:00:00\nNODES=8\n"
	file1 =file1 + "OUTPUT="+rootname+"_scf\n\n"
	subFile1 = "setup_and_runscf_"+rootname+".sh"
	file1 =file1+ "qsub -A $ACCT -t $TIME -n $NODES -O $OUTPUT ./"+subFile1 
	submissionFile1 = path+"/"+"submission1_"+rootname+".sh"
	with open(submissionFile1,"w") as fileOut:
		fileOut.write(file1)

        pyfile1 = "#!/bin/bash\n"
	pyfile1 = pyfile1 + "source /soft/applications/quantum_package/quantum_package.rc\n"
	pyfile1 = pyfile1 +"MPIRUN=True\n\n"
	pyfile1 = pyfile1 +"./"+pythonCalculationFilename1+" $MPIRUN"
	fileoutName = path +"/"+subFile1
	with open(fileoutName,"w") as fileOut:
		fileOut.write(pyfile1)
    

	##################################
	### DO THE AO TO MO TRANSFORMATION
	##################################
	file2 = "#!/bin/bash\nACCT=QMCPACK\n\n"
	file2 = file2+ "TIME=1:00:00\nNODES=1\n"
	file2 =file2 + "OUTPUT="+rootname+"_ao2mo\n\n"
	subFile2 = "ao_2_mo_"+rootname+".sh"
	file2 =file2+ "qsub -A $ACCT -t $TIME -n $NODES -O $OUTPUT ./"+subFile2 
	submissionFile2 = path+"/"+"submission2_"+rootname+".sh"
	with open(submissionFile2,"w") as fileOut:
		fileOut.write(file2)

        pyfile2 = "#!/bin/bash\n"
	pyfile2 = pyfile2 + "source /soft/applications/quantum_package/quantum_package.rc\n\n"
	pyfile2 = pyfile2 +"./"+pythonCalculationFilename2
	fileoutName = path +"/"+subFile2
	with open(fileoutName,"w") as fileOut:
		fileOut.write(pyfile2)
    


	##################################
	### RUN THE FCI_ZMQ CALCULATION 
	##################################
	file3 = "#!/bin/bash\nACCT=QMCPACK\n\n"
	file3 = file3+ "TIME=12:00:00\nNODES=8\n"
	file3 =file3 + "OUTPUT="+rootname+"_fci\n\n"
	subFile3 ="run_fci_"+rootname+".sh"
	file3 =file3+ "qsub -A $ACCT -t $TIME -n $NODES -O $OUTPUT ./"+subFile3 
	submissionFile3 = path+"/"+"submission3_"+rootname+".sh"
	with open(submissionFile3,"w") as fileOut:
		fileOut.write(file3)

        pyfile3 = "#!/bin/bash\n"
	pyfile3 = pyfile3 + "source /soft/applications/quantum_package/quantum_package.rc\n"
	pyfile3 = pyfile3 +"MPIRUN=True\n\n"
	pyfile3 = pyfile3 +"./"+pythonCalculationFilename3+" $MPIRUN"
	fileoutName = path +"/"+subFile3
	with open(fileoutName,"w") as fileOut:
		fileOut.write(pyfile3)
    
	##################################
	### DO THE CONVERSIONS FOR QMCPACK
	##################################
	file4 = "#!/bin/bash\nACCT=QMCPACK\n\n"
	file4 = file4+ "TIME=1:00:00\nNODES=1\n"
	file4 =file4 + "OUTPUT="+rootname+"_conversion\n\n"
	subFile4 = "conversion_"+rootname+".sh"
	file4 =file4+ "qsub -A $ACCT -t $TIME -n $NODES -O $OUTPUT ./"+subFile4
	submissionFile4 = path+"/"+"submission4_"+rootname+".sh"
	with open(submissionFile4,"w") as fileOut:
		fileOut.write(file4)

        pyfile4 = "#!/bin/bash\n"
	pyfile4 = pyfile4 + "source /soft/applications/quantum_package/quantum_package.rc\n\n"
	pyfile4 = pyfile4 +"./"+pythonCalculationFilename4
	fileoutName = path +"/"+subFile4
	with open(fileoutName,"w") as fileOut:
		fileOut.write(pyfile4)
    


    def __generate_QP_SCFCalculation__(self):
   	path,rootname,sub_path,ezfio_filename = self.main_filepath_args
        scf_dumpname,SCF_out_filename,fci_dumpname,FCI_out_filename,A2M_out_filename=self.filename1_args     
        pythonCalculationFilename1=self.filename2_args[0]
        inputFile, NDET,basis, m,pp,otherArguments=self.parameters_args
	##############################################
	#### GENERATE THE CALCULATION FILE THAT WILL 
        #### BE CALLED IN THE SUBMISSION FILE
	##############################################
	fileHeader="#!/usr/bin/env python \n# -*- coding: utf-8 -*- \n"
        fileHeader=fileHeader + "#THIS FILE CREATES THE EZFIO AND RUNS THE SCF CALCULATION \n \n"
	fileHeader=fileHeader + "import os \nimport sys \nfrom ezfio import ezfio \n"
	fileHeader=fileHeader + "mpirun=sys.argv[1]\n"
        fileMain = "### first create the ezfio file\n"
	if pp:
	     fileMain =fileMain+ "os.system(\"qp_create_ezfio_from_xyz " + str(inputFile)+ " -b \'"+str(basis)+"\' -m "+str(m)+" -p "+str(pp)+otherArguments+" -o " +ezfio_filename+"\")\n"
	else:
             fileMain =fileMain+ "os.system(\"qp_create_ezfio_from_xyz " + str(inputFile)+ " -b \'"+str(basis)+"\' -m "+str(m)+otherArguments+" -o " +ezfio_filename+"\")\n"
	fileMain = fileMain+"ezfio.set_file(\""+ezfio_filename+"\")\n"
        fileMain = fileMain+ "#Setup calculation for running SCF and ao to mo transformation\n"
	fileMain = fileMain +"ezfio.set_integrals_bielec_disk_access_ao_integrals(\"Write\")\n"
        fileMain = fileMain +"ezfio.set_integrals_bielec_disk_access_mo_integrals(\"Write\")\n"
	fileMain = fileMain +"ezfio.set_integrals_monoelec_disk_access_ao_one_integrals(\"Write\")\n"
	fileMain = fileMain +"ezfio.set_integrals_monoelec_disk_access_mo_one_integrals(\"Write\")\n"

       	fileMain = fileMain +"### Now run the SCF calculation\n"
	fileMain = fileMain +"if mpirun.lower()[0]==\"t\":\n"
	fileMain = fileMain +"   os.system(\"./qp-mpirun.sh SCF "+ezfio_filename+"/ > "+SCF_out_filename+"\")\n"
	fileMain = fileMain +"else:\n"
       	fileMain = fileMain +"   os.system(\"qp_run SCF "+ezfio_filename+"/ > "+SCF_out_filename+"\")\n"

	fileoutName = path + "/" +pythonCalculationFilename1
	with open(fileoutName,"w") as fileout:
       	    fileout.write("%s" %fileHeader)
	    fileout.write("%s" %fileMain)
	
    def __generate_scfDump_ao2moTransform__(self):
   	path,rootname,sub_path,ezfio_filename = self.main_filepath_args
        scf_dumpname,SCF_out_filename,fci_dumpname,FCI_out_filename,A2M_out_filename=self.filename1_args     
        pythonCalculationFilename2=self.filename2_args[1]
        ##############################################
        ### GENERATE THE CALCULATION FILE THAT WILL 
        ### BE CALLED IN THE SUBMISSION FILE
        #############################################
        	
        ### BEGIN FILECREATION
        
        fileHeader="#!/usr/bin/env python \n# -*- coding: utf-8 -*- \n"
        fileHeader=fileHeader + "#THIS FILE CREATES THE EZFIO, RUNS THE SCF CALCULATION, AND THEN RUNS THE FCI CALCULATION \n \n"
        fileHeader=fileHeader + "import os \nimport sys \n"
        fileHeader=fileHeader + "from ezfio import ezfio \n\n"
        
	fileMain=""
        fileMain = fileMain+"ezfio.set_file(\""+ezfio_filename+"\")\n"

        fileMain = fileMain +"### convert the ao to mo\n"
	fileMain = fileMain +"ezfio.set_determinants_n_det_max(1)\n"
        fileMain = fileMain +"### Now save the 1 det system for qmcpack\n"
        fileMain = fileMain +"os.system(\"qp_run save_for_qmcpack "+ezfio_filename+"/ > "+scf_dumpname+"\")\n"
        fileMain = fileMain +"os.system(\"qp_run fci_zmq "+ezfio_filename+"/ > "+A2M_out_filename+"\")\n"
          
       	fileoutName = path + "/" +pythonCalculationFilename2
	with open(fileoutName,"w") as fileout:
    	   fileout.write("%s" %fileHeader)
    	   fileout.write("%s" %fileMain)

    def __generate_fciCalculation__(self):
   	path,rootname,sub_path,ezfio_filename = self.main_filepath_args
        scf_dumpname,SCF_out_filename,fci_dumpname,FCI_out_filename,A2M_out_filename=self.filename1_args     
        pythonCalculationFilename3=self.filename2_args[2]
        inputFile, NDET,basis, m,pp,otherArguments=self.parameters_args
   	##############################################
	#### GENERATE THE FCI CALCULATION FILE THAT WILL 
       	#### BE CALLED IN THE SUBMISSION FILE
	##############################################

	### BEGIN FILECREATION
	fileHeader="#!/usr/bin/env python \n# -*- coding: utf-8 -*- \n"
	fileHeader=fileHeader + "#THIS FILE RUNS THE FCI CALCULATION \n \n"
	fileHeader=fileHeader + "import os \nimport sys \nfrom ezfio import ezfio\n"
	fileHeader=fileHeader + "mpirun=sys.argv[1]\n"

	fileMain=""
        fileMain = fileMain+"ezfio.set_file(\""+ezfio_filename+"\")\n"
        fileMain = fileMain +"ezfio.set_determinants_read_wf(True)\n"
        fileMain = fileMain +"ezfio.set_determinants_n_det_max("+str(NDET)+")\n"

	fileMain = fileMain +"### run the cipsi calculation\n"
	fileMain = fileMain +"if mpirun.lower()[0]==\"t\":\n"
	fileMain = fileMain +"   os.system(\"./qp-mpirun.sh fci_zmq "+ezfio_filename+"/ > "+FCI_out_filename+"\")\n"
	fileMain = fileMain +"else:\n"
	fileMain = fileMain +"   os.system(\"qp_run fci_zmq "+ezfio_filename+"/ > "+FCI_out_filename+"\")\n"

       	fileoutName = path + "/" +pythonCalculationFilename3
	with open(fileoutName,"w") as fileout:
		fileout.write("%s" %fileHeader)
		fileout.write("%s" %fileMain)
 
    def __generate_fciDump_conversions_qmcBlocks__(self):
   	path,rootname,sub_path,ezfio_filename = self.main_filepath_args
        scf_dumpname,SCF_out_filename,fci_dumpname,FCI_out_filename,A2M_out_filename=self.filename1_args     
        pythonCalculationFilename4=self.filename2_args[3]
	noJ_1det_fileroot,noJ_1det_base,J_1det_base,J_1det_fileroot,noJ_Multidet_base,noJ_Multidet_fileroot,J_Multidet_base,J_Multidet_fileroot,J_Multidet_reopt_base,J_Multidet_reopt_fileroot=self.qmc_files
        ##############################################
	####  GENERATE CONVERSION FILE  #############
        ##############################################

	### BEGIN FILECREATION
	fileHeader="#!/usr/bin/env python \n# -*- coding: utf-8 -*- \n"
	fileHeader=fileHeader + "#THIS FILE CONVERTS FOR QMCPACK INPUT \n \n"
	fileHeader=fileHeader + "import os \nimport sys \nfrom ezfio import ezfio \n"

	BINDIR="/soft/applications/qmcpack/github/build_Intel_real/bin"


	### BEGIN FILECREATION

	fileHeader="#!/usr/bin/env python \n# -*- coding: utf-8 -*- \n"
	fileHeader=fileHeader + "#THIS FILE MAKES THE INPUT FILES TO QMCPACK \n \n"
	fileHeader=fileHeader + "import os \nimport sys \n"

	fileMain ="os.system(\"qp_run save_for_qmcpack "+ezfio_filename+"/ > "+fci_dumpname+"\")\n\n"
	main=""

	fileMain = fileMain + "baseDir=\""+sub_path+"\"\n"
	if self.doSCF:
	    ### NO JASTROW AND 1 DET		
  	    main = main+"os.system(\""+BINDIR+"/convert4qmc -QP "+scf_dumpname+" -addCusp\" )\n"
	    main = main+"os.rename(\"sample.Gaussian-G2.xml\",baseDir+\"/" +noJ_1det_base+"/"+noJ_1det_fileroot+".wfs.xml\")\n"
	    main = main+"os.rename(\"sample.Gaussian-G2.ptcl.xml \", baseDir+\"/" +noJ_1det_base+"/"+noJ_1det_fileroot+".ptcl.xml\")\n\n"

	    ### PLAIN JASTROW AND 1 DET		
	    main = main+"os.system(\""+BINDIR+"/convert4qmc -QP "+scf_dumpname+" -add3BodyJ -addCusp\" )\n"
	    main = main+"os.rename(\"sample.Gaussian-G2.xml \", baseDir+\"/" +J_1det_base+"/"+J_1det_fileroot+".wfs.xml\")\n"
	    main = main+"os.rename(\"sample.Gaussian-G2.ptcl.xml \", baseDir+\"/" +J_1det_base+"/"+J_1det_fileroot+".ptcl.xml\")\n\n"

	### NO JASTROW AND MULTI-DETERMINANT
	main = main+"os.system(\""+BINDIR+"/convert4qmc -QP "+fci_dumpname+" -addCusp \" )\n"
	main = main+"os.rename(\"sample.Gaussian-G2.xml \", baseDir+\"/" +noJ_Multidet_base+"/"+noJ_Multidet_fileroot+".wfs.xml\")\n"
	main = main+"os.rename(\"sample.Gaussian-G2.ptcl.xml \", baseDir+\"/" +noJ_Multidet_base+"/"+noJ_Multidet_fileroot+".ptcl.xml\")\n\n"

	### PLAIN JASTROW AND MULTI-DETERMINANT
	main = main+"os.system(\""+BINDIR+"/convert4qmc -QP "+fci_dumpname+" -add3BodyJ -addCusp\" )\n"
	main = main+"os.rename(\"sample.Gaussian-G2.xml \", baseDir+\"/" +J_Multidet_base+"/"+J_Multidet_fileroot+".wfs.xml\")\n"
	main = main+"os.rename(\"sample.Gaussian-G2.ptcl.xml \", baseDir+\"/" +J_Multidet_base+"/"+J_Multidet_fileroot+".ptcl.xml\")\n\n"

	### OPTIMIZED JASTROW AND MULTI-DETERMINANT
	main = main+"os.system(\""+BINDIR+"/convert4qmc -QP "+fci_dumpname+" -add3BodyJ -addCusp\" )\n"
	main = main+"os.rename(\"sample.Gaussian-G2.xml \", baseDir+\"/" +J_Multidet_reopt_base+"/"+J_Multidet_reopt_fileroot+".wfs.xml\")\n"
	main = main+"os.rename(\"sample.Gaussian-G2.ptcl.xml \", baseDir+\"/" +J_Multidet_reopt_base+"/"+J_Multidet_reopt_fileroot+".ptcl.xml\")\n\n"
	
       	fileoutName = path + "/" +pythonCalculationFilename4
	with open(fileoutName,"w") as fileout:
		fileout.write("%s" %fileHeader)
		fileout.write("%s" %fileMain)
		fileout.write("%s" %main)


