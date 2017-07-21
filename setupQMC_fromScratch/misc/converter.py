#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
#THIS FILE CONVERTS FOR QMCPACK INPUT 
import os 

BINDIR ="/soft/applications/qmcpack/github/build_Intel_real/bin"

FILEPATH = "ABSPATH"
os.system(BINDIR+"/convert4qmc -QP "+FILEPATH+"/DUMPNAME FLAGS" )
os.rename("sample.Gaussian-G2.xml",FILEPATH+"/FileName.wfs.xml")
os.rename("sample.Gaussian-G2.ptcl.xml",FILEPATH+"/FileName.ptcl.xml")

	
