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
			[--c=<charge_of_atom>]
			[--d=<dummy_atoms>]
			[--cart=<transform_to_cartesian>]

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
    from generateQP_and_ConversionFiles import generateQP_and_ConversionFiles
    #from recreateXML import *
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

    otherArguments = ""
    if arguments["--c"]:
	charge = arguments["--c"]
	otherArguments = otherArguments + " -c " +charge + " "
    if arguments["--d"]:
	dummy_atom= arguments["--d"]
	otherArguments = otherArguments + " -d " +dummy_atom + " "
    if arguments["--cart"]:
	otherArguments = otherArguments + " -cart "


    if arguments["--pseudopotential"]:
	pp = arguments["--pseudopotential"]
	print "The system is: \n \t element: %s \n \t basis: %s \n \t geometry: %s \n \t pp: %s \n \t Other args: %s" %(element, basis, geometry,pp,otherArguments)
    else:
	pp=False
	print "The system is: \n \t element: %s \n \t basis: %s \n \t geometry: %s \n \t No pp\n \t Other args: %s" %(element, basis, geometry,otherArguments)


    #######################################################################
    #### CHECK IF THERE IS INPUT/ENERGIES FOR THIS RUN IN THE DATABASE ####
    #######################################################################

    '''
    if qmc_input_exists():
    	grabFiles=True
    else:
	grabFiles =False
    '''
    grabFiles=False

    if grabFiles:
	### get the files from the database
	#get_qmc_input_metadata()
	filename, runNum = qmc_input_retrieve()
	recreate_wfs(filename,runNum)
	recreate_ptcl(filename,runNum)
	recreate_Opt(filename,runNum)
	recreate_DMC(filename,runNum)


    else:
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
     	     os.mkdir(path)
          inputFile= "_".join([element, geometry])
    	  inputFile=inputFile+ g.ext
          filepath = path +"/"+ inputFile
    	 #print filepath
        else:
          #path = "_".join([".".join(l_geo), ".".join(l_ele)])
    	  path="/tmp/"+mainDirectory
      	  if not os.path.exists(path):
    	     os.mkdir(path)
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
        #qmc_rootname = rootname
        #A2M_out_filename =path + "/"+ rootname + ".ao2mo.out"
        A2M_out_filename =rootname + ".ao2mo.out"

        pythonCalculationFilename1 ="setup_and_runscf_"+rootname+".py"
        pythonCalculationFilename2 ="ao_2_mo_"+rootname+".py"
        pythonCalculationFilename3 ="run_fci_"+rootname+".py"
        pythonCalculationFilename4= "conversion_" +rootname+".py"


        ### generate all the files
        main_filepath_args = [path,rootname,sub_path,ezfio_filename]
        filename1_args     = [scf_dumpname,SCF_out_filename,fci_dumpname,FCI_out_filename,A2M_out_filename]
        filename2_args     = [pythonCalculationFilename1,pythonCalculationFilename2,pythonCalculationFilename3,pythonCalculationFilename4]
        parameters_args    = [inputFile, NDET,basis, m,pp,otherArguments]

        myFile = generateQP_and_ConversionFiles(main_filepath_args,filename1_args,filename2_args,parameters_args)
        myFile.generateMasterFile()
	#add_qmc_input_metadata()
