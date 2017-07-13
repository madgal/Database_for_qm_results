#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os 
import lxml
from lxml import etree
os.system("cp FULLDIR/FILEROOT.wfs.xml FULLDIR/FILEROOT.wfs.xml_initial")
myfile ="FULLDIR/FILEROOT.wfs.xml"

tree= etree.parse(myfile)
root = tree.getroot()
wavefunc = root[0]
determinantset = wavefunc[0]
up_det =  determinantset[1][0]
dn_det = determinantset[1][1]
MyCuspUp ="FULLDIR/CuspCorrection/updet.cuspInfo.xml"
sposet_up.set("cuspInfo",MyCuspUp)
MyCuspDn ="FULLDIR/CuspCorrection/downdet.cuspInfo.xml"
sposet_dn.set("cuspInfo",MyCuspDn)

j2Body= wavefunc[1]
j1Body= wavefunc[2]
for corr in j2Body:
    corr.set("rcut","10")
for corr in j1Body:
    corr.set("rcut","5")
j3Body= wavefunc[3]
for corr in j3Body:
    corr.set("rcut","3")

###### NOW WRITE THE MODIFICATIONS TO A FILE
tmpfile = myfile+".tmp"
f = open( tmpfile,"w")
f.write("<?xml version=\"1.0\"?>\n")
f.write(etree.tostring(root,pretty_print=True))
f.close()

os.system("mv " + tmpfile + " " + myfile)

os.chdir("FULLDIR/CuspCorrection")
os.system("./cusp.sh")
