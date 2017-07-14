#! /usr/bin/env python
# -*- coding: utf-8 -*- 

import os
cutoffs = [0.01,0.008,0.006,0.004,0.002,0.0009,0.0007,0.0005,0.0003,0.0001,0.00008,0.00006,0.00004]

prevDet=0

for value in cutoffs:
	mainDir = "MAINDIR"
	thisDir = mainDir+"/cutoff_"+str(value)
        if not(os.path.exists(thisDir)):
               print "%s does not exist " %thisDir 
	
	newfilename=thisDir + "/FILEROOT_" + str(value)
	initialfilename =mainDir  +"/FILEROOT"
        os.system("cp "+initialfilename+".wfs.xml "+newfilename+".wfs.xml")
        os.system("cp "+initialfilename+".ptcl.xml "+thisDir+"/")


        match = "<ci id="
        match =match.replace(" ","")
        qc_match = "qc_coeff="

	cutoffroot =  newfilename +".wfs.xml"
        tmpFilenam = cutoffroot +".tmp"
        tmpFile = open(tmpFilenam,"w")
        dets=0
        with open (cutoffroot,"r") as fileIn:
                for row in fileIn:
                        line = row.replace(" ","")
                        if line[0:3] ==match[0:3]:
                                line = row.split(" ")
                                for el in line:
                                        if el[0:8] == qc_match[0:8]:
                                                if abs(float(el[10:-1])) >= value:
                                                        tmpFile.write(row)
                                                        dets+=1
                                                break

                        else:
                                tmpFile.write(row)

        tmpFile.close()
        os.system("mv " + tmpFilenam + " " +cutoffroot)


        import lxml
        from lxml import etree

        tree = etree.parse(cutoffroot)
        root = tree.getroot()
        wavefunc = root[0]
        determinantset = wavefunc[0]
        multidet = determinantset[3]
        multidet[0].set("size",str(dets))
        multidet[0].set("cutoff",str(value))

        f = open(tmpFilenam,"w")
        f.write("<?xml version=\"1.0\"?>\n")
        f.write(etree.tostring(root,pretty_print=True))
        f.close()

        os.system("mv " + tmpFilenam + " " +cutoffroot)
