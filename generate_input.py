#!/usr/bin/env python
# -*- coding: utf-8 -*-

## This code generates input to QMCPack by using quantum_package code

""" 
Usage: 
  generate_input.py (-h | --help)
  generate_input.py dmc --ele=<element_name> 
			--basis=<basis_set>  
			--geo=<geometry>
			[--submit_path=<path_name>] 
			[--write_path=<path_name>] 
			[--pseudopotential=<name_of_pp>]
			[--n_det=<max_number_of_determinants>]

Example of use:
	./generate_input.py dmc --ele=C2 --basis="cc-pvdz" --geo=Experiment --pseudopotential=True
"""

version="0.0.1"
import os
import sys
  
try:
    from src.docopt import docopt
    from src.SQL_util import cond_sql_or, list_geo, list_ele, dict_raw
    from src.SQL_util import get_xyz, get_g09
    from generateSubmissionFiles import *
except:
    print "File in misc is corupted. Git reset may fix the issues"
    sys.exit(1)

if __name__ == '__main__':

    arguments = docopt(__doc__, version='G2 Api ' + version)

    if not (arguments["--ele"] and arguments["--basis"]):
	print "The element name and basis set are required"
	sys.exit(1)
    else:
	element = arguments["--ele"]
	geometry = arguments["--geo"]
	basis   = arguments["--basis"]
        mainDirectory = element + "_"+geometry +"_"+basis

    if arguments["--pseudopotential"]:
	pp = arguments["--pseudopotential"]
	print "The system is: \n \t element: %s \n \t basis: %s \n \t geometry: %s \n \t pp: %s" %(element, basis, geometry,pp)
    else:
	pp=False
	print "The system is: \n \t element: %s \n \t basis: %s \n \t geometry: %s \n \t No pp" %(element, basis, geometry)


    ### Now grab/create the xyz file
    from collections import namedtuple
    
    get_general = namedtuple('get_general', ['get','ext'])
    g = get_general(get=get_xyz,ext='.xyz')

    to_print=[]
    try:
        xyz = g.get(geometry,element)
    except KeyError:
	print "Error: Please generate an xyz file and update the database"
        pass
    else:
        to_print.append(xyz)
    if len(to_print)>1:
	print "Warning: There are multiple xyz files being generated"
	print "         To fix this try adding a specific geometry"

    str_ = "\n\n".join(to_print)
    
    if arguments["--write_path"]:
         path = arguments["--write_path"]
	 path = path +"/"+mainDirectory
	 if not os.path.exists(path):
 	     os.system("mkdir "+path)
         inputFile= "_".join([element, geometry])
	 inputFile=inputFile+ g.ext
         filepath = path +"/"+ inputFile
	 #print filepath
    else:
         #path = "_".join([".".join(l_geo), ".".join(l_ele)])
	 path="/tmp/"+mainDirectory
	 if not os.path.exists(path):
	     os.system("mkdir "+path)
         inputFile= "_".join([element, geometry])
	 inputFile=inputFile+ g.ext
         filepath = path + inputFile
    with open(filepath, 'w') as f:
         f.write(str_ + "\n")
    print "Files will be placed in  %s" %path

    if arguments["--submit_path"]:
	sub_path = arguments["--submit_path"]
    else:
        sub_path=path



    ### Now obtain the multiplicity etc... 
    try:
        m = dict_raw()[element]["multiplicity"]
    except KeyError:
        pass
    else:
        print m

    if arguments["--n_det"]:
	NDET=arguments["--n_det"]
    else:
	#### otherwise set it to the quantum package default
	NDET=10000


    def buildQMCDirectories(baseDir,fileroot):
	directory = path + "/"+ baseDir
	if not(os.path.isdir(directory)):
	    os.system("mkdir " +directory)
	if not(os.path.isdir(directory+"/CuspCorrection")):
	    os.system("mkdir " + directory+"/CuspCorrection")
	generateCuspCorrection(directory,fileroot,sub_path,baseDir)
	if not(os.path.isdir(directory+"/Optimization")):
    	    os.system("mkdir " + directory+"/Optimization")
	generateOptimization(directory,fileroot,sub_path,baseDir)
	if not(os.path.isdir(directory+"/DMC")):
	    os.system("mkdir " + directory+"/DMC")
	generateDMC(directory,fileroot,sub_path,baseDir)


    #####################################################################
    ### Now define the variables that will be needed in all of the calls
    #####################################################################
    rootname = str(element)+"_"+geometry+"_"+str(basis)
    rootname = rootname.replace(" ","")

    scf_rootname= rootname + "_1"
    scf_rootname = scf_rootname.replace(" ","")
    scf_dumpname = scf_rootname + ".dump"
    #SCF_out_filename =path + "/"+ rootname + ".SCF.out"
    SCF_out_filename = rootname + ".SCF.out"

    fci_rootname= rootname+ "_"+ str(NDET)
    fci_rootname = fci_rootname.replace(" ","")
    fci_dumpname = fci_rootname + ".dump"
    #FCI_out_filename =path + "/"+ rootname + ".FCI.out"
    FCI_out_filename = fci_rootname + ".FCI.out"

    #ezfio_filename = path + "/"+rootname + ".ezfio"
    ezfio_filename = rootname + ".ezfio"
    #inputFile = filepath
    qmc_rootname = rootname
    #A2M_out_filename =path + "/"+ rootname + ".ao2mo.out"
    A2M_out_filename =rootname + ".ao2mo.out"

    pythonCalculationFilename1 ="setup_and_runscf_"+rootname+".py"
    pythonCalculationFilename2 ="ao_2_mo_"+rootname+".py"
    pythonCalculationFilename3 ="run_fci_"+rootname+".py"
    pythonCalculationFilename4= "conversion_" +rootname+".py"

    doSCF=True
    if os.path.exists(path+"/1Det_NoJastrow"):
	doSCF=False

    if doSCF:
	noJ_1det_base = "1Det_noJastrow"
        noJ_1det_path = path +"/"+noJ_1det_base
        noJ_1det_fileroot = rootname+"_"+noJ_1det_base
        buildQMCDirectories(noJ_1det_base,noJ_1det_fileroot)

	J_1det_base = "1Det_Jastrow"
        J_1det_path = path +"/"+J_1det_base
        J_1det_fileroot = rootname+"_"+ J_1det_base
        buildQMCDirectories(J_1det_base,J_1det_fileroot)

    noJ_Multidet_base = str(NDET)+"Det_NoJastrow" 
    noJ_Multidet_path = path +"/"+noJ_Multidet_base
    noJ_Multidet_fileroot=rootname +"_"+noJ_Multidet_base
    buildQMCDirectories(noJ_Multidet_base,noJ_Multidet_fileroot)

    J_Multidet_base =str(NDET)+"Det_Jastrow"
    J_Multidet_path = path +"/"+J_Multidet_base
    J_Multidet_fileroot=rootname +"_"+J_Multidet_base
    buildQMCDirectories(J_Multidet_base,J_Multidet_fileroot)

    J_Multidet_reopt_base =str(NDET)+"Det_Jastrow_reOpt"
    J_Multidet_reopt_path = path +"/"+J_Multidet_reopt_base
    J_Multidet_reopt_fileroot = rootname +"_"+J_Multidet_reopt_base
    buildQMCDirectories(J_Multidet_reopt_base,J_Multidet_reopt_fileroot)
	

    def generateMasterFile():
	
        if doSCF:
            generate_QP_SCFCalculation()
            generate_scfDump_ao2moTransform()
        generate_fciCalculation()
	generate_fciDump_conversions_qmcBlocks()
	"""if arguments["vmc"]: 
		generate_fciDump_conversions_qmcBlocks("vmc")
	else:
		generate_fciDump_conversions_qmcBlocks("dmc")
	"""

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
    


    def generate_QP_SCFCalculation():
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
	     fileMain =fileMain+ "os.system(\"qp_create_ezfio_from_xyz " + str(inputFile)+ " -b \'"+str(basis)+"\' -m "+str(m)+" -p "+str(pp)+" -o " +ezfio_filename+"\")\n"
	else:
             fileMain =fileMain+ "os.system(\"qp_create_ezfio_from_xyz " + str(inputFile)+ " -b \'"+str(basis)+"\' -m "+str(m)+" -o " +ezfio_filename+"\")\n"
	fileMain = fileMain+"ezfio.set_file(\""+ezfio_filename+"\")\n"
        fileMain = fileMain+ "#Setup calculation for running SCF and ao to mo transformation\n"
	#fileMain = fileMain +"ezfio.set_integrals_bielec_disk_access_ao_integrals(\"Write\")\n"
        #fileMain = fileMain +"ezfio.set_integrals_bielec_disk_access_mo_integrals(\"Write\")\n"
	#fileMain = fileMain +"ezfio.set_integrals_monoelec_disk_access_ao_one_integrals(\"Write\")\n"
	#fileMain = fileMain +"ezfio.set_integrals_monoelec_disk_access_mo_one_integrals(\"Write\")\n"

       	fileMain = fileMain +"### Now run the SCF calculation\n"
	fileMain = fileMain +"if mpirun.lower()[0]==\"t\":\n"
	fileMain = fileMain +"   os.system(\"./qp-mpirun.sh SCF "+ezfio_filename+"/ > "+SCF_out_filename+"\")\n"
	fileMain = fileMain +"else:\n"
       	fileMain = fileMain +"   os.system(\"qp_run SCF "+ezfio_filename+"/ > "+SCF_out_filename+"\")\n"

	fileoutName = path + "/" +pythonCalculationFilename1
	with open(fileoutName,"w") as fileout:
       	    fileout.write("%s" %fileHeader)
	    fileout.write("%s" %fileMain)
	
    def generate_scfDump_ao2moTransform():
        ##############################################
        ### GENERATE THE CALCULATION FILE THAT WILL 
        ### BE CALLED IN THE SUBMISSION FILE
        #############################################
        	
        ### BEGIN FILECREATION
        
        fileHeader="#!/usr/bin/env python \n# -*- coding: utf-8 -*- \n"
        fileHeader=fileHeader + "#THIS FILE CREATES THE EZFIO, RUNS THE SCF CALCULATION, AND THEN RUNS THE FCI CALCULATION \n \n"
        fileHeader=fileHeader + "import os \nimport sys \n"
        #fileHeader=fileHeader + "from ezfio import ezfio \n\n"
        
	fileMain=""
        #fileMain = fileMain+"ezfio.set_file(\""+ezfio_filename+"\")\n"

        fileMain = fileMain +"### convert the ao to mo\n"
	#fileMain = fileMain +"ezfio.set_determinants_n_det_max(1)\n"
        fileMain = fileMain +"### Now save the 1 det system for qmcpack\n"
        fileMain = fileMain +"os.system(\"qp_run save_for_qmcpack "+ezfio_filename+"/ > "+scf_dumpname+"\")\n"
        #fileMain = fileMain +"os.system(\"qp_run fci_zmq "+ezfio_filename+"/ > "+A2M_out_filename+"\")\n"
          
       	fileoutName = path + "/" +pythonCalculationFilename2
	with open(fileoutName,"w") as fileout:
    	   fileout.write("%s" %fileHeader)
    	   fileout.write("%s" %fileMain)

    def generate_fciCalculation():
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
        #fileMain = fileMain +"ezfio.set_determinants_read_wf(True)\n"
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
 
    def generate_fciDump_conversions_qmcBlocks():
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
	if doSCF:
	    ### NO JASTROW AND 1 DET		
  	    main = main+"os.system(\""+BINDIR+"/convert4qmc -QP "+scf_dumpname+" -addCusp\" )\n"
	    main = main+"os.system(\"mv sample.Gaussian-G2.xml\"+ baseDir+\"/" +noJ_1det_base+"/"+noJ_1det_fileroot+".wfs.xml\")\n"
	    main = main+"os.system(\"mv sample.Gaussian-G2.ptcl.xml \"+ baseDir+\"/" +noJ_1det_base+"/"+noJ_1det_fileroot+".ptcl.xml\")\n\n"

	    ### PLAIN JASTROW AND 1 DET		
	    main = main+"os.system(\""+BINDIR+"/convert4qmc -QP "+scf_dumpname+" -add3BodyJ -addCusp\" )\n"
	    main = main+"os.system(\"mv sample.Gaussian-G2.xml \"+ baseDir+\"/" +J_1det_base+"/"+J_1det_fileroot+".wfs.xml\")\n"
	    main = main+"os.system(\"mv sample.Gaussian-G2.ptcl.xml \"+ baseDir+\"/" +J_1det_base+"/"+J_1det_fileroot+".ptcl.xml\")\n\n"

	### NO JASTROW AND MULTI-DETERMINANT
	main = main+"os.system(\""+BINDIR+"/convert4qmc -QP "+fci_dumpname+" -addCusp \" )\n"
	main = main+"os.system(\"mv sample.Gaussian-G2.xml \"+ baseDir+\"/" +noJ_Multidet_base+"/"+noJ_Multidet_fileroot+".wfs.xml\")\n"
	main = main+"os.system(\"mv sample.Gaussian-G2.ptcl.xml \"+ baseDir+\"/" +noJ_Multidet_base+"/"+noJ_Multidet_fileroot+".ptcl.xml\")\n\n"

	### PLAIN JASTROW AND MULTI-DETERMINANT
	main = main+"os.system(\""+BINDIR+"/convert4qmc -QP "+fci_dumpname+" -add3BodyJ -addCusp\" )\n"
	main = main+"os.system(\"mv sample.Gaussian-G2.xml \"+ baseDir+\"/" +J_Multidet_base+"/"+J_Multidet_fileroot+".wfs.xml\")\n"
	main = main+"os.system(\"mv sample.Gaussian-G2.ptcl.xml \"+ baseDir+\"/" +J_Multidet_base+"/"+J_Multidet_fileroot+".ptcl.xml\")\n\n"

	### OPTIMIZED JASTROW AND MULTI-DETERMINANT
	main = main+"os.system(\""+BINDIR+"/convert4qmc -QP "+fci_dumpname+" -add3BodyJ -addCusp\" )\n"
	main = main+"os.system(\"mv sample.Gaussian-G2.xml \"+ baseDir+\"/" +J_Multidet_reopt_base+"/"+J_Multidet_reopt_fileroot+".wfs.xml\")\n"
	main = main+"os.system(\"mv sample.Gaussian-G2.ptcl.xml \"+ baseDir+\"/" +J_Multidet_reopt_base+"/"+J_Multidet_reopt_fileroot+".ptcl.xml\")\n\n"
	
       	fileoutName = path + "/" +pythonCalculationFilename4
	with open(fileoutName,"w") as fileout:
		fileout.write("%s" %fileHeader)
		fileout.write("%s" %fileMain)
		fileout.write("%s" %main)


    generateMasterFile()
