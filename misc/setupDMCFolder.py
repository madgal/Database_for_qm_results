import os
################################################
#### Generate : DMC.xml
################################################
import lxml
from lxml import etree

import sys

outerDir=sys.argv[1]
fileroot=sys.argv[2]
filename = sys.argv[3]
usepp = sys.argv[4]

if usepp:
    template_Name = "DMC_PP.xml"
else:
    template_Name = "DMC_AE.xml"
    
DMC_dir = outerDir + "/DMC"
if not(os.path.isdir(DMC_dir)):
    os.mkdir(DMC_dir)
os.system("cp misc/"+template_Name+" " +DMC_dir+"/DMC.xml")
os.system("cp utils/format_data.py " +DMC_dir)

myFile = DMC_dir+"/DMC.xml"
tree = etree.parse(myFile)
root = tree.getroot()

project = root[0]
icld_ptcl = root[2]
icld_wfs = root[3]

projName = "DMC-"+filename
project.set("id",projName)

ptclFile = fileroot+".ptcl.xml"
wfsFile =  fileroot +".wfs.xml"
icld_ptcl.set("href",ptclFile)
icld_wfs.set("href",wfsFile)

###### NOW WRITE THE MODIFICATIONS TO A FILE
tmpfile = myFile+".tmp"
f = open( tmpfile,"w")
f.write("<?xml version=\"1.0\"?>\n")
f.write(etree.tostring(root,pretty_print=True))
f.close()

os.system("mv " + tmpfile + " " + myFile)

os.system("cp misc/bgq-DMC.sh "+DMC_dir)
