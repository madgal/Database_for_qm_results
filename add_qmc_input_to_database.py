#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
You can add_input

Usage:
  add_qmc_input_to_database.py (-h | --help)
  add_qmc_input_to_database.py add_input --path=<path> --wfs_flnm=<name_of_wavefunction_xml_file> --ptcl_flnm=<name_of_particle_xml_file> --opt_flnm=<name_of_optimization_xml_file> --dmc_flnm=<name_of_dmc_xml_file>
                     (--method=<method_name> --basis=<basis_name>
                      --geo=<geometry_name> --comment=<comment>|
                      --run_id=<id>)


"""

version = "0.0.2"

import sys

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

    l = [arguments[i] for i in ["--method",
                                "--basis",
                                "--geo",
                                "--comment"]]
    run_id = add_or_get_run(*l)

    print run_id,

    with open(arguments["--path"], "r") as f:
        data = [line for line in f.read().split("\n") if line]

    for line in data:

        list_ = line.split("#")[0].split()

        try:
            list_[0]
        except IndexError:
            continue

        name = list_[0]
        name = old_name_to_new[name] if name in old_name_to_new else name
        id_ = get_mol_id(name)
        print name, id_,

	############################################################
	############################################################
	############################################################
	############################################################
	############################################################
	############################################################

	''' Need :

		N_det = (integer)
		Jastrow = (true | false)
		CuspCorrection = (true | false)
		Version = (version number)
                vmc_preOpt
		Optimization_Block =???
                vmc_preDMC
		DMC_block = ???
                cutoff
                n_det
                pseudopotential
		basis
		geometry
		comments
		citation
		seed
		element
		initial_WF_generation_method
		
	
		'''

          '''
         <simulation>

          ...

          <qmc method="dmc" move="pbyp" checkpoint="-1" gpu="yes">
            <estimator name="LocalEnergy" hdf5="no"/>
            <parameter name="targetwalkers">4000</parameter>
            <parameter name="reconfiguration">   no </parameter>
            <parameter name="warmupSteps">  50 </parameter>
            <parameter name="timestep">  0.001 </parameter>
            <parameter name="steps">   30 </parameter>
            <parameter name="blocks">  200</parameter>
            <parameter name="nonlocalmoves">  yes </parameter>
          </qmc>
         </simulation>
         
        -----------
        The following commands print the results beneath:
          root.tag 
             > 'simulation'
          root[8].tag 
	     > 'qmc'
          root[8].attrib
	     > {'checkpoint': '-1', 'gpu': 'yes', 'move': 'pbyp', 'method': 'dmc'}


          tags = ""
          for x in root[8].attrib:
               tags = tags +x +'=' +root[8].attrib[x] +","
          print tags[:-1]

             >'method=dmc,move=pbyp,checkpoint=-1,gpu=yes'

          root[8][1].attrib
	     > {'name': 'targetwalkers'}
          root[8][1].text
             > '4000'
          root[8][1].attrib['name']
             > 'targetwalkers'
          root[8][1].attrib['name'] + '='
             > 'targetwalkers='
          root[8][1].attrib['name'] + '=' + root[8][1].text
             > 'targetwalkers=4000'


          params = ""
          for child in root[8]:
              if child.tag=='parameter':
                  params = params +child.attrib['name'] + '='+child.text.replace(" ","")  + ","... 
           print params[:-1]

              > targetwalkers=4000,reconfiguration=no,warmupSteps=50,timestep=0.001,steps=30,blocks=200,nonlocalmoves=yes


	'''


         ''' schema:
        

             qmc Tables:
          
                 wavefunction: 
  	                     id_num

                 particleset:
  	                     id_num

                 optimizationFile:
  	                     id_num
                             vmc_method_tags
			     vmc_estimator
			     vmc_parameters
			     opt_loop1_tags
                             opt_estimator1
			     opt_costFunc1
			     opt_parameter1
			     opt_loop2_tags	
                             opt_estimator2
			     opt_costFunc2
			     opt_parameter2

                 dmc file:
  	                     id_num
                             vmc_method_tags
			     vmc_estimator
			     vmc_parameters
                             dmc_method_tags
			     dmc_estimator
			     dmc_parameters
  
                 connectResults_to_input:
                              qmc_id_num
                              energy_location

 	'''
        wfsname  = arguments["--wfs_flnm"] 
        ptclname = arguments["--ptcl_flnm"]
        optname  = arguments["--opt_flnm"]
        dmcname  = arguments["--dmc_flnm"]

        from unpackXML import *

        runNum = getNum()
        pullDataFromWFS(wfsname,runNum)
        pullDataFromPTCL(ptclname,runNum)
        pullDataFromOPT(optname,runNum)
        pullDataFromDMC(dmcname,runNum)
	

        add_qmc_input_metadata()
                       

	message = "Added energy to database"
	#print "Please commit db/g2.dump changes to https://github.com/madgal/qmcpack_buddy"
	os.system("git add db/g2.dump")
	os.system("git commit -m \""+message+"\"")
	os.system("git push")
    conn.commit()
