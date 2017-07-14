#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
import os 
import sys 
from ezfio import ezfio 

NAME="FILEROOT"

ezfio.set_file(NAME+".ezfio")
### convert the ao to mo
ezfio.set_determinants_n_det_max(1)
### Now save the 1 det system for qmcpack
os.system("qp_run save_for_qmcpack "+NAME+".ezfio/ > "+NAME+"_1.dump")
os.system("qp_run fci_zmq "+NAME+".ezfio/ > "+NAME+".ao2mo.out")
ezfio.set_determinants_read_wf(True)
ezfio.set_determinants_n_det_max("NDET")
