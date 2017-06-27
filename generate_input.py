#!/usr/bin/env python
# -*- coding: utf-8 -*-

## This code generates input to QMCPack by using quantum_package code

""" 
Usage: 
  generate_input.py (-h | --help)
  generate_input.py dmc --ele=<element_name> 
			--basis=<basis_set>  
			--geo=<geometry>
			[--path=<path_name>] 
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
    #from generateSubmissionFiles import *
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
    
    if arguments["--path"]:
         path = arguments["--path"]
         inputFile= "_".join([element, geometry])
         filepath = path +"/"+ inputFile+ g.ext
	 print filepath
    else:
         #path = "_".join([".".join(l_geo), ".".join(l_ele)])
	 path="/tmp/"
         inputFile= "_".join([element, geometry])
         filepath = "/tmp/" + inputFile+ g.ext
    with open(filepath, 'w') as f:
         f.write(str_ + "\n")
    print path



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
    FCI_out_filename = rootname + ".FCI.out"

    #ezfio_filename = path + "/"+rootname + ".ezfio"
    ezfio_filename = rootname + ".ezfio"
    #inputFile = filepath
    qmc_rootname = rootname
    #A2M_out_filename =path + "/"+ rootname + ".ao2mo.out"
    A2M_out_filename =rootname + ".ao2mo.out"

    noJ_1det_path = path +"/1Det_NoJastrow/" +rootname
    J_1det_path = path +"/1Det_Jastrow/" +rootname
    noJ_Multidet_path = path +"/"+str(NDET)+"Det_Jastrow/" +rootname
    J_Multidet_path = path +"/"+str(NDET)+"Det_Jastrow/" +rootname
    J_Multidet_reopt_path = path +"/"+str(NDET)+"Det_Jastrow_reOpt/" +rootname
	

    def generateMasterFile():
	
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
       	#### GENERATE THE MASTER SUBMISSION FILE # 
	#### THIS WILL BE ABLE TO EXECUTE THE CALCULATION
	#### FROM SCF INPUT TO QMC OUTPUT
	##########################################

	file = "#!/bin/bash\nACCT=QMCPACK\n"
	file = file+ "source /soft/applications/quantum_package/quantum_package.rc\n\n"

	##################################
	### CREATE THE EZFIO AND RUN SCF
	##################################
	file = file+ "\nTIME=12:00:00\nNODES=8\n"
	file =file + "OUTPUT="+rootname+"_scf_output\n"
	subFile = "setup_and_runscf_"+rootname+".sh"
	file =file+ "qsub -A $ACCT -t $TIME -n $NODES -O OUTPUT ./"+subFile + "\n\n"


	##################################
	### DO THE AO TO MO TRANSFORMATION
	##################################
	file = file+ "TIME=1:00:00\nNODES=1\n"
	file =file + "OUTPUT="+rootname+"_ao2mo_output\n"
	subFile = "ao_2_mo_"+rootname+".sh"
	file =file+ "qsub -A $ACCT -t $TIME -n $NODES -O OUTPUT ./"+subFile + "\n\n"


	##################################
	### RUN THE FCI_ZMQ CALCULATION 
	##################################
	file = file+ "TIME=12:00:00\nNODES=8\n"
	file =file + "OUTPUT="+rootname+"_fci_output\n"
	subFile = "run_fci_"+rootname+".sh"
	file =file+ "qsub -A $ACCT -t $TIME -n $NODES -O OUTPUT ./"+subFile + "\n\n"


	##################################
	### DO THE CONVERSIONS FOR QMCPACK
	##################################
	file = file+ "TIME=1:00:00\nNODES=1\n"
	file =file + "OUTPUT="+rootname+"_conversion_output\n"
	subFile = "conversion_"+rootname+".sh"
	file =file+ "qsub -A $ACCT -t $TIME -n $NODES -O OUTPUT ./"+subFile


	
	submissionFile = path+"/"+"masterSubmission_"+rootname+".sh"
	with open(submissionFile,"w") as fileOut:
		fileOut.write(file)

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
	     fileMain =fileMain+ "os.system(\"create_ezfio_from_xyz " + str(inputFile)+ " -b \'"+str(basis)+"\' -m "+str(m)+" -p "+str(pp)+" -o " +ezfio_filename+"\")\n"
	else:
             fileMain =fileMain+ "os.system(\"create_ezfio_from_xyz " + str(inputFile)+ " -b \'"+str(basis)+"\' -m "+str(m)+" -o " +ezfio_filename+"\")\n"
	fileMain = fileMain+"ezfio.set_file(\""+ezfio_filename+"\")\n"
        fileMain = fileMain+ "#Setup calculation for running SCF and ao to mo transformation"
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

	fileoutName =path+"/"+ "setup_and_runscf_"+rootname+".py"
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
        fileHeader=fileHeader + "import os \nimport sys \nfrom ezfio import ezfio \n\n"
        
	fileMain=""
        fileMain = fileMain+"ezfio.set_file(\""+ezfio_filename+"\")\n"

        fileMain = fileMain +"### convert the ao to mo"
        ## ONCE THE ITERATIVE IS ESTABLISHED IN QUANTUM PACKAGE UNCOMMENT THIS LINE
        #fileMain = fileMain +"ezfio.set_full_ci_zmq_iterative(True)\n"
        fileMain = fileMain +"os.system(\"qp_run fci_zmq "+ezfio_filename+"/ > "+A2M_out_filename+"\")\n"
        fileMain = fileMain +"### Now save the 1 det system for qmcpack\n"
        fileMain = fileMain +"os.system(\"qp_run save_for_qmcpack "+ezfio_filename+"/ > "+scf_dumpname+"\")\n"
        fileMain = fileMain +"ezfio.set_determinants_n_det_max("+str(NDET)+")\n"
        fileMain = fileMain +"ezfio.set_determinants_read_wf(True)\n"
        
        fileoutName =path+"/"+ "ao_2_mo_"+rootname+".py"
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
	fileHeader=fileHeader + "import os \nimport sys \nfrom ezfio import ezfio \n"
	fileHeader=fileHeader + "mpirun=sys.argv[1]\n"

	fileMain=""
	fileMain = fileMain+"ezfio.set_file(\""+ezfio_filename+"\")\n"

	fileMain = fileMain +"### run the cipsi calculation"
	fileMain = fileMain +"if mpirun.lower()[0]==\"t\":\n"
	fileMain = fileMain +"   os.system(\"./qp-mpirun.sh fci_zmq "+ezfio_filename+"/ > "+FCI_out_filename+"\")\n"
	fileMain = fileMain +"else:\n"
	fileMain = fileMain +"   os.system(\"qp_run fci_zmq "+ezfio_filename+"/ > "+FCI_out_filename+"\")\n"

	fileoutName =path+"/"+ "run_fci_"+rootname+".py"
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
	fileHeader=fileHeader + "convertDir=/soft/applications/qmcpack/github/build_Intel_real/bin\n"

	BINDIR="/soft/applications/qmcpack/github/build_Intel_real/bin"


	### BEGIN FILECREATION

	fileHeader="#!/usr/bin/env python \n# -*- coding: utf-8 -*- \n"
	fileHeader=fileHeader + "#THIS FILE MAKES THE INPUT FILES TO QMCPACK \n \n"
	fileHeader=fileHeader + "import os \nimport sys \nfrom ezfio import ezfio \n"

	fileMain ="os.system(\"qp_run save_for_qmcpack "+ezfio_filename+"/ > "+FCI_dump_filename+"\")\n"
	### NO JASTROW AND 1 DET		
	main = "os.system(\""+BINDIR+"/convert4qmc -QP "+SCF_dump_filename+" -addCusp\" )\n"
	main = main+"os.system(\"mv sample.Gaussian-G2.xml " +noJ_1det_path+"/"+rootname+"_1Det_NoJastrow.wfs.xml\")\n"
	main = main+"os.system(\"mv sample.Gaussian-G2.ptcl.xml " +noJ_1det_path+"/"+rootname+"_1Det_NoJastrow.ptcl.xml\")\n"

	### PLAIN JASTROW AND 1 DET		
	main = main+"os.system(\""+BINDIR+"/convert4qmc -QP "+SCF_dump_filename+" -add3BodyJ -addCusp\" )\n"
	main = main+"os.system(\"mv sample.Gaussian-G2.xml " +J_1det_path+"/"+rootname+"_1Det_Jastrow.wfs.xml\")\n"
	main = main+"os.system(\"mv sample.Gaussian-G2.ptcl.xml " +J_1det_path+"/"+rootname+"_1Det_Jastrow.ptcl.xml\")\n"

	### NO JASTROW AND MULTI-DETERMINANT
	main = main+"os.system(\""+BINDIR+"/convert4qmc -QP "+FCI_dump_filename+" -addCusp \" )\n"
	main = main+"os.system(\"mv sample.Gaussian-G2.xml " +noJ_Multidet_path+"/"+rootname+"_"+str(NDET)+"_NoJastrow.wfs.xml\")\n"
	main = main+"os.system(\"mv sample.Gaussian-G2.ptcl.xml " +noJ_Multidet_path+"/"+rootname+"_"+str(NDET)+"_NoJastrow.ptcl.xml\")\n"

	### PLAIN JASTROW AND MULTI-DETERMINANT
	main = main+"os.system(\""+BINDIR+"/convert4qmc -QP "+FCI_dump_filename+" -add3BodyJ -addCusp\" )\n"
	main = main+"os.system(\"mv sample.Gaussian-G2.xml " +J_Multidet_path+"/"+rootname+"_"+str(NDET)+"_Jastrow.wfs.xml\")\n"
	main = main+"os.system(\"mv sample.Gaussian-G2.ptcl.xml " +J_Multidet_path+"/"+rootname+"_"+str(NDET)+"_Jastrow.ptcl.xml\")\n"

	### OPTIMIZED JASTROW AND MULTI-DETERMINANT
	main = main+"os.system(\""+BINDIR+"/convert4qmc -QP "+FCI_dump_filename+" -add3BodyJ -addCusp\" )\n"
	main = main+"os.system(\"mv sample.Gaussian-G2.xml " +J_Multidet_reopt_path+"/"+rootname+"_"+str(NDET)+"_ReOptJastrow.wfs.xml\")\n"
	main = main+"os.system(\"mv sample.Gaussian-G2.ptcl.xml " +J_Multidet_reopt_path+"/"+rootname+"_"+str(NDET)+"_ReOptJastrow.ptcl.xml\")\n"
	

        fileoutName = path + "/"+ "conversion_" +rootname+".py"
	with open(fileoutName,"w") as fileout:
		fileout.write("%s" %fileHeader)
		fileout.write("%s" %fileMain)

    generateMasterFile()
