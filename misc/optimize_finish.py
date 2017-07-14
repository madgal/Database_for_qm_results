#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
Directory = "FULLDIR"
myfile =Directory+"/FILEROOT.wfs.xml"

os.system("cp "+myfile+" " +myfile+"_3b")


os.system("OptProgress.pl *scalar.dat > opt_3b.dat")


series=[]
energies=[]
with open("opt_3b.dat","r") as fileIn:
	for row in fileIn:
		row = row.split("  ")
		series.append(row[0])
		if int(row[0]) >86:
			energies.append(float(row[1]))
		else:	
			energies.append(100.0)
	

index = energies.index(min(energies))

os.system("cp Opt-FILEROOT.s"+series[index]+".opt.xml "+myfile)
