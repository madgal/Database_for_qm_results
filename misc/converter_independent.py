#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
#THIS FILE CONVERTS FOR QMCPACK INPUT 
import os 
import sys

method=sys.argv[1]
dumpfile = sys.argv[2]
filename = sys.argv[3]
flags = sys.argv[4]

BINDIR ="/soft/applications/qmcpack/github/build_Intel_real/bin"

os.system(BINDIR+"/convert4qmc -"+method+" "+dumpfile +" "+ flags )
os.rename("sample.Gaussian-G2.xml",filename+".wfs.xml")
os.rename("sample.Gaussian-G2.ptcl.xml",filename+".ptcl.xml")

	
