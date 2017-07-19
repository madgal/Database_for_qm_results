#!/bin/bash

echo "Converting wavefunction"
chmod 744 converter_FILEROOT.py
./converter_FILEROOT.py

## if Cusp Correction
echo "Running cusp correction"
cd CuspCorrection
./modify_wfs_4_Cusp_multi.py  FILEROOT
cd ../


## if Multideterminants need to be tested for convergence
echo "Setting up cutoff directories"
./multiDet_convergence_setup.py


