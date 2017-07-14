#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
#THIS FILE CONVERTS FOR QMCPACK INPUT 
import os 
import sys 
from ezfio import ezfio


NAME="FILEROOT"
NAME2 = NAME+"_NDET"
os.system("qp_run save_for_qmcpack "+NAME+".ezfio/ > "+NAME2+".dump")

