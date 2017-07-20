#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from misc/modify_multiDet_wfs4cutoff import *
import sys

thisDir = sys.argv[1]
absfileroot = sys.argv[2]
fileroot = sys.argv[3]
doPseudo = sys.argv[4]
elementList = sys.argv[5]

cutoffs = [0.01,0.008,0.006,0.004,0.002,0.0009,0.0007,0.0005,0.0003,0.0001,0.00008,0.00006,0.00004]

for value in cutoffs:

	cutoffDir = thisDir +"/cutoff_"+str(value)
	if not(os.path.isdir(cutoffDir)):
		os.mkdir(cutoffDir)
	fileroot_wfs = fileroot+"_"+str(value)


	modify_wfs_4_cutoff(cutoffDir,thisDir,fileroot,wfs_fileroot,value):

	abs_wfsfile = absfileroot + "_"+str(value)
	os.system("./misc/setupDMCFolder.py " + cutoffDir + " " + absfileroot + " " + abs_wfsfile+" " +fileroot + "  " +doPseudo + " " +elementList)
	os.system("./misc/setupOptFolder.py " + cutoffDir + " " + absfileroot + " " + abs_wfsfile+" " +fileroot + "  " +doPseudo + " " +elementList)
