#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
#THIS FILE RUNS THE FCI CALCULATION 
import os 
import sys
mpirun=sys.argv[1]


### run the cipsi calculation
if mpirun.lower()[0]=="t":
   os.system("./qp-mpirun.sh fci_zmq ezfio_filename/ > FCI_out_filename")
else:
   os.system("qp_run fci_zmq ezfio_filename/ > FCI_out_filename")
