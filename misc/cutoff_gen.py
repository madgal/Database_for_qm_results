# -*- coding:utf-8 -*-

import os
import sys

fileroot = sys.argv[1]
cutoffValue = float(sys.argv[2])

myfile = "../"+fileroot+".wfs.xml_template"
mycutoff = "../"+fileroot+"_"+cutoffValue+".wfs.xml"
os.system("cp "+myfile+ " "+ mycutoff)

match = "<ci id="
match =match.replace(" ","")
qc_match = "qc_coeff="

tmpFilenam = mycutoff +".tmp"
tmpFile = open(tmpFilenam,"w")
dets=0
with open (mycutoff,"r") as fileIn:
        for row in fileIn:
                line = row.replace(" ","")
                if line[0:3] ==match[0:3]:
                        line = row.split(" ")
                        for el in line:
                                if el[0:8] == qc_match[0:8]:
                                        if abs(float(el[10:-1])) >= cutoffValue:
                                                tmpFile.write(row)
						dets+=1
                                        break

                else:
                        tmpFile.write(row)

tmpFile.close()


os.system("mv " + tmpFilenam + " " + mycutoff)



import lxml
from lxml import etree

tree = etree.parse(mycutoff)
root = tree.getroot()
wavefunc = root[0]
multidet = determinantset[3]
multidet[0].set("size",str(dets))
multidet[0].set("cutoff",str(cutoffValue))

tmpfile = mycutoff + ".tmp"
f = open(tmpfile,"w")
f.write("<?xml version=\"1.0\"?>\n")
f.write(etree.tostring(root,pretty_print=True))
f.close()

os.system("mv " + tmpfile + " " + mycutoff)

