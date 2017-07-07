#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import lxml
from lxml import etree

fileroot=sys.argv[1]
cwd = sys.argv[2]
cutoff = sys.argv[3]


if os.path.exists("../"+fileroot+"_"+str(cutoff)+".wfs.xml"):
    print "Error this file already exists. Please check that this is the file you want to modify"
else:
    os.system("./cutoff_gen.py "+ fileroot + " " + cutoff)

    myFile = "DMC.xml"
    tree = etree.parse(myFile)
    root = tree.getroot()

    project = root[0]
    icld_wfs = root[3]
    
    projName = "DMC-"+fileroot+"_"+str(cutoff)
    project.set("id",projName)

    wfsFile =  cwd+"/"+fileroot+"_"+str(cutoff)+".wfs.xml"
    icld_wfs.set("href",wfsFile)

    ###### NOW WRITE THE MODIFICATIONS TO A FILE
    tmpfile = myFile+".tmp"
    f = open( tmpfile,"w")
    f.write("<?xml version=\"1.0\"?>\n")
    f.write(etree.tostring(root,pretty_print=True))
    f.close()

    os.system("mv " + tmpfile + " " + myFile)
    
   run = raw_input("Are you certain you want to run DMC (yes/no)? \n > ")
   if run[0].lower()=="y": 
	print "Submitting the job"
	os.system("./bgq.sh")


