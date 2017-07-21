#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
#THIS FILE RUNS THE FCI CALCULATION 
import os 
import sys
mpirun=sys.argv[1]

NAME="FILEROOT"
NAME2 = NAME+"_NDET"


### run the cipsi calculation
if mpirun.lower()[0]=="t":
   os.system("./qp-mpirun.sh fci_zmq " +NAME+".ezfio/ > "+NAME2+".FCI.out")
else:
   os.system("qp_run fci_zmq " +NAME+".ezfio/ > "+NAME2+".FCI.out")
