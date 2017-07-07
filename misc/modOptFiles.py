#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import lxml
from lxml import etree

os.system("OptProgress.pl *scalar.dat > opt_info.tmp")
filename = "opt_info.tmp"
fileIn = open(filename,"r") 
for row in fileIn:
    

SERIES=s000
cp ../"+fileroot+".wfs.xml ../"+fileroot+".wfs.xml_BAK
cp "+projName+".${SERIES}.opt.xml ../"+fileroot+".wfs.xml
