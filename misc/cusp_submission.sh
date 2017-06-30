#!/bin/bash
NODES=1
TIME=30
ACCT=QMCPACK
EMAIL=galbraithm@duq.edu
OUTPUT=cusp_calc
qsub -A $ACCT -t $TIME -n $NODES -M $EMAIL  -O $OUTPUT ./cusp.sh
