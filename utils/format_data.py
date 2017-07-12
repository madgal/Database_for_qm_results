#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os



'''
Standard OptProgress.pl output: 

['HF_cc-pvDz-DMC_0.0007', '', 'series', '1', '', '-100.333720', '+/-', '0.014640', '', '', '7.055517', '+/-', '0.375961', '', '', '0.0703', '\n']
'''

seriesName =[]
dmcEnergy =[]
dmcEnErr =[]
dmcVar =[]
dmcVarErr =[]
ratio =[]
ndet=[]

os.system("qmca -q ev *scalar.dat > convergence.dat")
os.system("grep \"detlist size=\" ../*wfs.xml > grepped_dets.dat")

count=0
filename = "convergence.dat"
with open(filename, "r") as filein:
	for row in filein:
		row = row.split(" ")
		#print row
		if count>1 and len(row)>2 and int(row[3])==2:
			#print row
			#print row[0],row[5],row[7],row[10],row[12],row[15]
			seriesName.append(row[0])
			dmcEnergy.append(row[5])
			dmcEnErr.append(row[7])
			dmcVar.append(row[10])
			dmcVarErr.append(row[12])
			ratio.append(row[15])
		count+=1

filename = "grepped_dets.dat"
with open(filename, "r") as filein:
	for row in filein:
		row = row.split(" ")
		row = row[9]
		ndet.append( row[6:-1])

filename2 ="convergence_formatted.dat"
with open(filename2,"w") as fileOut:
	fileOut.write("%s" %"Name,DMC_Energy,DMC_EnergyErr,DMC_Var,DMC_VarErr,Ratio,Ndet")
	for i in range(len(seriesName)):
		fileOut.write("\n%s," %seriesName[i])
		fileOut.write("%s," %dmcEnergy[i])
		fileOut.write("%s," %dmcEnErr[i])
		fileOut.write("%s," %dmcVar[i])
		fileOut.write("%s," %dmcVarErr[i])
		fileOut.write("%s," %ratio[i])
		fileOut.write("%s" %ndet[i])
