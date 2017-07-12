#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
import os 
import sys 
from ezfio import ezfio 
ezfio.set_file("ezfio_filename")

### convert the ao to mo
ezfio.set_determinants_n_det_max(1)
### Now save the 1 det system for qmcpack
os.system("qp_run save_for_qmcpack ezfio_filename/ > scf_dumpname")
os.system("qp_run fci_zmq ezfio_filename/ > A2M_out_filename")
ezfio.set_determinants_read_wf(True)
ezfio.set_determinants_n_det_max("NDET")
