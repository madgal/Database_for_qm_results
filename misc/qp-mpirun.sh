#!/bin/bash
source /soft/applications/quantum_package/quantum_package.rc
RANKS_PER_NODE=1
NODES=`cat $COBALT_NODEFILE | wc -l`
PROCS=$(($NODES * $RANKS_PER_NODE))
QPIN=$2
QPTYPE0=$1
QPTYPE1="-slave qp_ao_ints"
QPBIN=qp_run

MPIRUN=mpirun
MPIFLAGS="-f $COBALT_NODEFILE -n $PROCS"


let SLAVES=${PROCS}-1
$MPIRUN -F $COBALT_NODEFILE -n 1 $QPBIN $QPTYPE0 $QPIN &
sleep 10
$MPIRUN -f $COBALT_NODEFILE -n $SLAVES $QPBIN $QPTYPE1 $QPIN
wait

