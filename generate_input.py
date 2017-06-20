#!/usr/bin/env python
# -*- coding: utf-8 -*-

## This code generates input to QMCPack by using quantum_package code

""" 
Usage: 
  generate_input.py (-h | --help)
  generate_input.py (dmc | vmc) --ele=<element_name> 
			--basis=<basis_set>  
			--geo=<geometry>
			[--path=<path_name>] 
			[--pseudopotential=<True_or_False>]
			[--n_det=<max_number_of_determinants>]

  generate_input.py vmc --ele=<element_name> 
			--basis=<basis_set>  
			--geo=<geometry>
			[--path=<path_name>] 
			[--pseudopotential=<bfd>]
			[--n_det=<max_number_of_determinants>]

Example of use:
	./generate_input.py dmc --ele=C2 --basis="cc-pvdz" --geo=Experiment --pseudopotential=True
	./generate_input.py vmc --ele=C2 --basis="cc-pvdz" --geo=Experiment --pseudopotential=True
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
	" The element is " , element
	basis   = arguments["--basis"]

    if arguments["--pseudopotential"]:
	pp = arguments["pseudopotential"]


    ### Now grab/create the xyz file
    from collections import namedtuple
    
    get_general = namedtuple('get_general', ['get','ext'])
    g = get_general(get=get_xyz,ext='.xyz')
    #l_geo = arguments["--geo"]
    #l_ele = arguments["--ele"]
    #l_geo = [geometry]
    #l_ele = [element]

    to_print=[]
    try:
        xyz = g.get(geometry,element)
    except KeyError:
        pass
    else:
        to_print.append(xyz)
    if len(to_print)>1:
	print "Warning: There are multiple xyz files being generated"
	print "         To fix this try adding a specific geometry"

    str_ = "\n\n".join(to_print)
    
    if arguments["--path"]:
         path = arguments["--path"]
         filepath = path
    else:
         #path = "_".join([".".join(l_geo), ".".join(l_ele)])
         filepath = "_".join([geometry, element])
         filepath = "/tmp/" + path + g.ext
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

    #################################################################
    ### Now create the ezfio file for submission to quantum_package
    ### Convert to qmcpack input format 
    #################################################################
    rootname = path+"/"+str(element)+"_"+geometry+"_"+str(basis)+"_"+str(NDET)
    rootname = rootname.replace(" ","")

    ### YOU CAN UNCOMMENT THESE LINES IF WANT TO RETURN TO SPLITTING UP
    ### SCF AND CIPSI CALCULATIONS
    generateCalculationFileQP_SCF_FCI(filepath,basis,m,rootname,NDET)
    
    scf_rootname= path+"/"+str(element)+"_"+geometry+"_"+str(basis)
    scf_rootname = scf_rootname.replace(" ","")
    ### fci_rootname is the same as the rootname
    generateSubmissionFileQP_SCF_FCI(scf_rootname,rootname)

    ################################################################
    ####   GENERATE THE HAMILTONIAN FOR THE MOLECULES
    ################################################################
    hamiltonian_rootname=path+"/"+str(element)+"_"+geometry+"_"+str(basis)
    hamiltonian_rootname = hamiltonian_rootname.replace(" ","")
    generateHamiltonian(hamiltonian_rootname)

    #################################################################
    ### Also generate the appropriate blocks
    #################################################################

    #generateOptBlocks(scf_rootname+"_1Det_NoJastrow",hamiltonian_rootname)
    #generateOptBlocks(scf_rootname+"_1Det_Jastrow",hamiltonian_rootname)
    #generateOptBlocks(rootname+"_NoJastrow",hamiltonian_rootname)
    #generateOptBlocks(rootname+"_Jastrow",hamiltonian_rootname)
    generateOptBlocks(rootname+"_ReOptJastrow",hamiltonian_rootname)

    if arguments["dmc"]:
    	generateDMCBlocks(scf_rootname+"_1Det_NoJastrow",hamiltonian_rootname)
    	generateDMCBlocks(scf_rootname+"_1Det_Jastrow",hamiltonian_rootname)
    	generateDMCBlocks(rootname+"_NoJastrow",hamiltonian_rootname)
    	generateDMCBlocks(rootname+"_Jastrow",hamiltonian_rootname)
    	generateDMCBlocks(rootname+"_ReOptJastrow",hamiltonian_rootname)

    elif arguments["vmc"]:
 	generateVMCBlocks(scf_rootname+"_1Det_NoJastrow",hamiltonian_rootname)
    	generateVMCBlocks(scf_rootname+"_1Det_Jastrow",hamiltonian_rootname)
    	generateVMCBlocks(rootname+"_NoJastrow",hamiltonian_rootname)
    	generateVMCBlocks(rootname+"_Jastrow",hamiltonian_rootname)
    	generateVMCBlocks(rootname+"_ReOptJastrow",hamiltonian_rootname)

    ################################################################
    #### NOW GENERATE THE SUBMISSION FILES   
    #### AND THE MASTER SUBMISSION FILE
    ################################################################
    generateMasterSubmissionFile(rootname)
