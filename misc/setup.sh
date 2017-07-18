#!/bin/bash


echo "Convert the quantum package *dump file to the *wfs.xml and *ptcl.xml files"
chmod 744 converter*py &&
./converter*py &&


echo "Change to CuspCorrection directory and build the correction files"
cd CuspCorrection/ &&
chmod 744 modify*py cusp.sh &&
./modify*py &&


echo "Return to outer directory and build the cutoff directories with *wfs.xml files that have the appropriate cutoffs/number of determinants"
cd ../ &&
chmod 744 mulitDet_convergence_setup.py &&
./mulitDet_convergence_setup.py 
