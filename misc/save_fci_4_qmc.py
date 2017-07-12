#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
#THIS FILE CONVERTS FOR QMCPACK INPUT 
import os 
import sys 
from ezfio import ezfio


os.system("qp_run save_for_qmcpack ezfio_filename/ > fci_dumpname")

