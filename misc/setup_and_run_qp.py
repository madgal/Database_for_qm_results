#!/usr/bin/env python 
# -*- coding: utf-8 -*-
#THIS FILE CREATES THE EZFIO AND RUNS THE SCF CALCULATION
import os 
import sys 
from ezfio import ezfio
mpirun=sys.argv[1]
### first create the ezfio file
NAME="FILEROOT"

os.system("qp_create_ezfio_from_xyz inputFile -b basis -m multiplicity otherArguments -o "+NAME+".ezfio")
ezfio.set_file(NAME+".ezfio")
#Setup calculation for running SCF and ao to mo transformation
ezfio.set_integrals_bielec_disk_access_ao_integrals("Write")
ezfio.set_integrals_bielec_disk_access_mo_integrals("Write")
ezfio.set_integrals_monoelec_disk_access_ao_one_integrals("Write")
ezfio.set_integrals_monoelec_disk_access_mo_one_integrals("Write")

### Now run the SCF calculation\n"

if mpirun.lower()[0]=="t":
   os.system("./qp-mpirun.sh SCF "+NAME+".ezfio/ > " +NAME+".SCF.out") 
else:
   os.system("qp_run SCF "+NAME+".ezfio/ > " +NAME+".SCF.out")
