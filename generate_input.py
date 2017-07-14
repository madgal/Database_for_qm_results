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
    #from recreateXML import *
except:
    print "File in misc is corupted. Git reset may fix the issues"
    sys.exit(1)

if __name__ == '__main__':

    arguments = docopt(__doc__, version='G2 Api ' + version)

    ### Retrieve the arguments passed by the user
    if not (arguments["--ele"] and arguments["--basis"] and arguments["--geo"] ):
	print "The element name, basis set, and geometry are required"
	sys.exit(1)
    else:
	element = arguments["--ele"]
	geometry = arguments["--geo"]
	basis   = arguments["--basis"]
        rootname = element + "_"+geometry +"_"+basis

   
        #### Check if the user wants to change the default number of determinants
        if arguments["--n_det"]:
    	    NDET=arguments["--n_det"]
        else:# set it to the quantum package default
    	    NDET=10000

    ### Check for additional QP arguments
    otherArguments = " "
    if arguments["--c"]:
	charge = arguments["--c"]
	otherArguments = otherArguments + " -c " +charge + " "
    if arguments["--d"]:
	dummy_atom= arguments["--d"]
	otherArguments = otherArguments + " -d " +dummy_atom + " "
    if arguments["--cart"]:
	otherArguments = otherArguments + " -cart "


    ## Check to see if we will use a pseudopotential
    if arguments["--pseudopotential"]:
	pp = arguments["--pseudopotential"]
	otherArguments = otherArguments + " -p " +pp
	print "The system is: \n \t element: %s \n \t basis: %s \n \t geometry: %s \n \t pp: %s \n \t Additional args: %s" %(element, basis, geometry,pp,otherArguments)
    else:
	pp=False #set the value to false so that it exists but  will not be used
	print "The system is: \n \t element: %s \n \t basis: %s \n \t geometry: %s \n \t No pp\n \t Additional args: %s" %(element, basis, geometry,otherArguments)

    ### Check if the user wants to write to specific location
    if arguments["--write_path"]:
	write_path = arguments["--write_path"]
    else:
        write_path=False
    if arguments["--submit_path"]:
	submit_path = arguments["--submit_path"]
    else:
        submit_path=False



    #######################################################################
    #### CHECK IF THERE IS INPUT/ENERGIES FOR THIS RUN IN THE DATABASE ####
    #######################################################################

    '''
    if qmc_input_exists():## check database to see if the run exists
    	grabFiles=True
    else:
	grabFiles =False
    '''
    grabFiles=False

    if grabFiles:
	### get the files from the database
	filename, runNum = qmc_input_retrieve()
	recreate_wfs(filename,runNum)
	recreate_ptcl(filename,runNum)
	recreate_Opt(filename,runNum)
	recreate_DMC(filename,runNum)


    else:

	#####################################################################
        ### Now define the variables that will be needed in all of the calls
        #####################################################################
	import generate_QP_input
        [path,sub_path] = generate_QP_input.fromScratch(geometry,element,basis,NDET,otherArguments,write_path,rootname,submit_path)
	
	import generate_qp_through_qmc


	#### THe following is specific to my project and needs to be fixed
	fileroot = rootname + "_1Det"
	multiDet = False
	noJastrow = True
	Jastrow3B =False
	generate_qp_through_qmc.conversion_and_qmcInput(path, sub_path,fileroot,pp,multiDet,noJastrow,Jastrow3B)
	noJastrow = False
	Jastrow3B =True
	generate_qp_through_qmc.conversion_and_qmcInput(path, sub_path,fileroot,pp,multiDet,noJastrow,Jastrow3B)

	fileroot = rootname + "_" + str(NDET)
	multiDet = True 
	noJastrow = True
	Jastrow3B =False
	generate_qp_through_qmc.conversion_and_qmcInput(path, sub_path,fileroot,pp,multiDet,noJastrow,Jastrow3B)
	multiDet = True 
	noJastrow =False 
	Jastrow3B =True
	generate_qp_through_qmc.conversion_and_qmcInput(path, sub_path,fileroot,pp,multiDet,noJastrow,Jastrow3B)
	multiDet = True 
	noJastrow =False
	Jastrow3B = True
	reopt=True
	generate_qp_through_qmc.conversion_and_qmcInput(path, sub_path,fileroot,pp,multiDet,noJastrow,Jastrow3B,reopt)

