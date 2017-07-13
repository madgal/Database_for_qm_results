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


sposet_up = determinantset[1]
sposet_dn = determinantset[2]
MyCuspUp="FULLDIR/CuspCorrection/spo-up.cuspInfo.xml"
sposet_up.set("cuspInfo",MyCuspUp)
MyCuspDn="FULLDIR/CuspCorrection/spo-dn.cuspInfo.xml"
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
