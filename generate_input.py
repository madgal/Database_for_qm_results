#!/usr/bin/env python
# -*- coding: utf-8 -*-

## This code generates input to QMCPack by using quantum_package code

""" 
Usage: 
  generate_input.py (-h | --help)
  generate_input.py optimization --ele=<element_name> 
				 --basis=<basis_set> 
				 --geo=<geometry>
				 [--path=<path_name>] 
				 [--pseudopotential=<True_or_False>]
  generate_input.py dmc --ele=<element_name> ...
				 --basis=<basis_set>  ...
				 [--pseudopotential=<True_or_False>]

  generate_input.py vmc --ele=<element_name> ...
				 --basis=<basis_set>  ...
				 [--pseudopotential=<bfd>]

Note: It defaults to generating optimzation and dmc blocks
Example of use:

	./generate_input.py dmc --ele=C2 --basis="cc-pvdz" --pseudopotential=True
"""

version="0.0.1"
import sys
  
try:
    from src.docopt import docopt
    from src.SQL_util import cond_sql_or, list_geo, list_ele, dict_raw
    from src.SQL_util import get_xyz, get_g09
except:
    print "File in misc is corupted. Git reset may fix the issues"
    sys.exit(1)

if __name__ == '__main__':

    arguments = docopt(__doc__, version='G2 Api ' + version)

    if not (arguments["--ele"] and arguments["--basis"]):
	print "The element name and basis set are required"
	sys.exit(1)
    else:
	element = arguments["--ele"][0]
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
    l_geo = [geometry]
    l_ele = [element]

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
    else:
         path = "_".join([".".join(l_geo), ".".join(l_ele)])
         path = "/tmp/" + path + g.ext
    with open(path, 'w') as f:
         f.write(str_ + "\n")
    print path



    ### Now obtain the multiplicity etc... 
    try:
        m = dict_raw()[element]["multiplicity"]
    except KeyError:
        pass
    else:
        print m

""" 
    ### Now create the ezfio file for submission to quantum_package
    
    ### Now run CIPSI
   
    ### Convert to qmcpack input format 
   
    ### Also generate the appropriate blocks

    echo "<?xml version="1.0">"
    echo "<simulation>"
    echo "<include href=Mypath.wfs.xml>"
    echo "<include href=Mypath.ptcl.xml>"
    if arguments["optimization"]:
	## only generate the optimization block
	echo "  <project id="opt" series="0">"
	echo "  </project>"
	echo "  <qmcsystem>"
	echo "  </qmcsystem>"
	echo optimizationBlock 
    elif arguments["vmc"]:
	## generate optimization blocks and vmc blocks
	echo "  <project id="vmc" series="0">"
	echo "  </project>"
	echo "  <qmcsystem>"
	echo "  </qmcsystem>"
	echo vmcBlock 
    else: # if arguments["dmc"]
	### default to generate optimization and dmc blocks
	echo "  <project id="dmc" series="0">"
	echo "  </project>"
	echo "  <qmcsystem>"
	echo "  </qmcsystem>"
	echo dmcBlock 

    echo "  </simulation>"

"""
