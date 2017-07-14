#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

try:
	Directory = "FULLDIR"
        myfile =Directory+"/FILEROOT.wfs.xml"
	os.system("cp "+ myfile +" " +myfile + "_12_coeff")

	os.system("OptProgress.pl *scalar.dat > opt_1b2b_coef.dat")


	series=[]
	energies=[]
	with open("opt_1b2b_coef.dat","r") as fileIn:
		for row in fileIn:
			row = row.split("  ")
			series.append(row[0])
			if int(row[0]) >43:
				energies.append(float(row[1]))
			else:	
				energies.append(100.0)
		
	
	index = energies.index(min(energies))

	os.system("cp Opt-FILEROOT.s"+series[index]+".opt.xml "+myfile)


	import lxml
	from lxml import etree

	tree= etree.parse(myfile)
	root = tree.getroot()
	wavefunc = root[0]
	determinantset = wavefunc[0]
	j3Body = wavefunc[3]
	for corr in j3Body:
		corr[0].set("optimize","yes")

	tmpfile = myfile+".tmp"
	f = open( tmpfile,"w")
	f.write("<?xml version=\"1.0\"?>\n")
	f.write(etree.tostring(root,pretty_print=True))
	f.close()

	os.system("mv " + tmpfile + " " + myfile)

   	### update where the series will start
	myfile = Directory+"/Optimization/Opt.xml"
   	tree= etree.parse(myfile)
	root = tree.getroot()
	root[0].set("series","87")

	tmpfile = myfile+".tmp"
	f = open( tmpfile,"w")
	f.write("<?xml version=\"1.0\"?>\n")
	f.write(etree.tostring(root,pretty_print=True))
	f.close()

	os.system("mv " + tmpfile + " " + myfile)

 
except Exception:
	print "Please check filenames and existence of files" 
else:
	print "Submitting Optimization of coefficients with 1 and 2 body Jastrows"
	os.system("./bgq-Opt.sh")
