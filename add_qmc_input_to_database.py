#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
You can add_input

Usage:
  add_qmc_input_to_database.py (-h | --help)
  add_qmc_input_to_database.py add_input --path=<path> --wfs_flnm=<name_of_wavefunction_xml_file> --ptcl_flnm=<name_of_particle_xml_file> --opt_flnm=<name_of_optimization_xml_file> --dmc_flnm=<name_of_dmc_xml_file>
				  	      [--method=<wfs_method_name>...]
                                              [--basis=<basis_name>...]
                                              [--geo=<geometry_name>...]
                                              [--comments=<comments>...]

"""

version = "0.0.2"


try:
    import sys,os
    from src.docopt import docopt
    #from src.SQL_util import add_or_get_run, get_mol_id
    from src.SQL_util import add_qmc_input_metadata
    from src.SQL_util import conn
    #from src.misc_info import old_name_to_new
except:
    raise
    print "File in misc is corupted. Git reset may fix the issues"
    sys.exit(1)

if __name__ == '__main__':

    arguments = docopt(__doc__, version='G2 Api ' + version)

    if arguments["add_input"]:
        ############################################################

        """
        Need :

    	N_det = (integer)
    	Jastrow = (true | false)
    	CuspCorrection = (true | false)
            cutoff
            pseudopotential
    	basis
    	geometry
    	comments
    	citation
    	element
    	initial_WF_generation_method
    	Optimization_File
    	DMC_File
    	wfs_file
    	ptcl_file
	"""
    		
        path = arguments["--path"]
        wfsname  = path +"/"+arguments["--wfs_flnm"] 
        ptclname = path +"/"+arguments["--ptcl_flnm"]
        optname  = path +"/"+arguments["--opt_flnm"]
        dmcname  = path +"/"+arguments["--dmc_flnm"]
	
	if arguments["--method"]:
		wfs_method = arguments["--method"]
	else:
		wfs_method=""
	if arguments["--basis"]:
		basis = arguments["--basis"]
	else:
		basis=""
	if arguments["--geo"]:
		geometry = arguments["--geo"]
	else:
		geometry=""
	if arguments["--comments"]:
		comments = arguments["--comments"]
	else:
		comments=""
	
	additionalInfo = [wfs_method,basis,geometry,comments]




        from unpackXML import *

        #runNum = getNum()
        runNum=1
        [wfsInfo,wfsFile]   =pullDataFromWFS(wfsname,runNum)
        [ptclFile]	   =pullDataFromPTCL(ptclname,runNum)
        [optFile]	   =pullDataFromOPT(optname,runNum)
        [dmcFile,projectId]=pullDataFromDMC(dmcname,runNum)
    	

        files4Database = [optFile,dmcFile,wfsFile,ptclFile]

        add_qmc_input_metadata(wfsInfo,files4Database,additionalInfo)

        conn.commit()
        ## Now grab the energy from the DMC *scalar.dat file
                           

        message = "Added input files and energy to database"
        #print "Please commit db/g2.dump changes to https://github.com/madgal/qmcpack_buddy"
        #os.system("git add db/g2.dump")
        #os.system("git commit -m \""+message+"\"")
        #os.system("git push")
