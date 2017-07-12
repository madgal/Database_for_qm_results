#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
#THIS FILE CONVERTS FOR QMCPACK INPUT 
import os 

BINDIR ="/soft/applications/qmcpack/github/build_Intel_real/bin"

os.system(BINDIR+"/convert4qmc -QP DUMPNAME FLAGS" )
os.rename("sample.Gaussian-G2.xml","absFileName.wfs.xml")
os.rename("sample.Gaussian-G2.ptcl.xml","absFileName.ptcl.xml")

	
