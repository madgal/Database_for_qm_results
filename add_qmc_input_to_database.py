#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
You can add_input

Usage:
  add_qmc_input_to_database.py (-h | --help)
  add_qmc_input_to_database.py add_input --path=<path> --wfs_flnm=<name_of_wavefunction_xml_file> --ptcl_flnm=<name_of_particle_xml_file> --opt_flnm=<name_of_optimization_xml_file> --dmc_flnm=<name_of_dmc_xml_file>  --mol_name=<name_of_molecule>
				  	      (--method=<wfs_method_name>
                                               --basis=<basis_name>
                                               --geo=<geometry_name>
                                               --comments=<comments>  |
					       --run_id=<id>)
					       [--overwrite]

"""

version = "0.0.2"


import sys,os
try:
    from src.docopt import docopt
    from src.SQL_util import add_or_get_run, get_mol_id
    from src.SQL_util import add_qmc_input_metadata
    from src.SQL_util import conn
    from src.misc_info import old_name_to_new
except:
    raise
    print "File in misc is corupted. Git reset may fix the issues"
    sys.exit(1)

if __name__ == '__main__':

    arguments = docopt(__doc__, version='G2 Api ' + version)

    if arguments["--run_id"]:
	run_id=arguments["--run_id"]
    else:
	l=[arguments[i] for i in ["--method",
				  "--basis",
				  "--geo",
				  "--comments"]]

    
    run_id = add_or_get_run(*l)


    name = arguments["--mol_name"]
    id_=get_mol_id(name)


    if arguments["add_input"]:
        ############################################################

    		
        path = arguments["--path"]
        wfsname  = path +"/"+arguments["--wfs_flnm"] 
        ptclname = path +"/"+arguments["--ptcl_flnm"]
        optname  = path +"/"+arguments["--opt_flnm"]
        dmcname  = path +"/"+arguments["--dmc_flnm"]
	

        from unpackXML import *

        #runNum = getNum()
        runNum=1
        [wfsInfo,wfsFile]   =pullDataFromWFS(wfsname,runNum)
        [ptclFile]	   =pullDataFromPTCL(ptclname,runNum)
        [optFile]	   =pullDataFromOPT(optname,runNum)
        [dmcFile,projectId]=pullDataFromDMC(dmcname,runNum)
    	

	print arguments["--method"]
	print "FILE:" ,wfsInfo
 	wfsInfo.insert(0,arguments["--method"])
	print "FILE:" ,wfsInfo


        files4Database = [optFile,dmcFile,wfsFile,ptclFile]

        add_qmc_input_metadata(run_id,id_,wfsInfo,files4Database,overwrite=arguments["--overwrite"])

        conn.commit()
        ## Now grab the energy from the DMC *scalar.dat file
                           

        message = "Added input files and energy to database"
        #print "Please commit db/g2.dump changes to https://github.com/madgal/qmcpack_buddy"
        #os.system("git add db/g2.dump")
        #os.system("git commit -m \""+message+"\"")
        #os.system("git push")
