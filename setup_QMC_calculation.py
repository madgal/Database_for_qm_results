#!/usr/bin/env python
# -*- coding: utf-8 -*-

## This code generates input to QMCPack by using quantum_package code

""" 
Usage: 
  setup_QMC_calculation.py (-h | --help)
  setup_QMC_calculation.py setup --filename=<filename.ext>
			--method=<QP>
			[--noJastrow=<True,False>]
			[--3BodyJ=<True,False>]

Example of use:
	./setup_QMC_calculation.py setup  --filename=qp_dumpfilename --method=QP
"""

### defaults to adding 3BodyJ

version="0.0.1"
import os
import sys
  
try:
except:
    print "File is corupted. Git reset may fix the issues"
    sys.exit(1)

if __name__ == '__main__':

    arguments = docopt(__doc__, version='G2 Api ' + version)

    ### Retrieve the arguments passed by the user
    if not (arguments["--filename"] and arguments["--method"]):
	print "The filename and conversionType are required"
	sys.exit(1)
    else:
	filename= arguments["--filename"]
	method  = arguments["--method"]

	if arguments["--noJastrow"]:
		nojastrow = arguments["--noJastrow"]
	else:
		nojastrow = False

	if arguments["--3BodyJ"]:
		use3Body = arguments["--3BodyJ"]
	else:
		use3Body = True

	from setupMethods import *
	if method=="QP":
		setupMethods.useQuantumPackageMethod(filename,nojastrow,use3Body)
