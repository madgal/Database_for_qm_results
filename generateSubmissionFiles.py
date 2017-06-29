def generateCuspCorrection(directory,fileroot,sub_path,baseName):

    ##################################################################
    ### Cusp.xml
    ##################################################################
    main = "<?xml version=\"1.0\"?>\n"
    main = main + "<simulation>\n"
    main = main +"  <project id=\""+fileroot+"\" series=\"1\"/>\n"
    main = main +"  <!-- input from quantum package converter -->\n"
    main = main +"  <include href=\""+sub_path+"/"+baseName+"/"+fileroot+".ptcl.xml\"/>\n"
    main = main +"  <include href=\""+sub_path+"/"+baseName+"/"+fileroot+".wfs.xml\"/>\n"
    main = main +"  <!--  Hamiltonian -->\n"
    main = main +"  <hamiltonian name=\"h0\" type=\"generic\" target=\"e\">\n"
    main = main +"    <pairpot name=\"IonElec\" type=\"coulomb\" source=\"ion0\" target=\"e\"/>\n"
    main = main +"    <constant name=\"IonIon\" type=\"coulomb\" source=\"ion0\" target=\"ion0\"/>\n"
    main = main +"    <pairpot name=\"ElecElec\" type=\"coulomb\" source=\"e\" target=\"e\" physical=\"true\"/>\n"
    main = main +"  </hamiltonian>\n\n\n"
    main = main +" <init source=\"ion0\" target=\"e\"/>\n\n\n\n"
    main = main +"  <qmc method=\"vmc\" move=\"pbyp\" gpu=\"yes\">\n"
    main = main +"    <estimator name=\"LocalEnergy\" hdf5=\"no\"/>\n"
    main = main +"    <parameter name=\"walkers\">   1</parameter>\n"
    main = main +"    <parameter name=\"samplesperthread\">    1 </parameter>\n"
    main = main +"    <parameter name=\"stepsbetweensamples\">    10 </parameter>\n"
    main = main +"    <parameter name=\"substeps\">  30 </parameter>\n"
    main = main +"    <parameter name=\"warmupSteps\">  25 </parameter>\n"
    main = main +"    <parameter name=\"blocks\"> 10</parameter>\n"
    main = main +"    <parameter name=\"timestep\">  0.001 </parameter>\n"
    main = main +"    <parameter name=\"usedrift\">   no </parameter>\n"
    main = main +"  </qmc>\n\n"
    main = main +"</simulation>\n"

    thisfile = directory +"/CuspCorrection/Cusp.xml"
    with open(thisfile,"w") as fileOut:
	fileOut.write("%s" %main)

    ##################################################################
    ### cusp.sh
    ##################################################################
 
    main = "#!/bin/bash\n\n"
    main = main + "BINDIR=/soft/applications/qmcpack/github/build_Intel_real/bin\n"
    main = main + "FILEIN=/gpfs/mira-fs0/projects/PSFMat/mgalbraith/Equilibrium/DZ/120000Det_Jastrow/CuspCorrection/Cusp.xml\n\n"
    main = main + "$BINDIR/qmcpack $FILEIN \n"

    thisfile = directory +"/CuspCorrection/cusp.sh"
    with open(thisfile,"w") as fileOut:
	fileOut.write("%s" %main)

    ##################################################################
    ### cusp_submission.sh
    ##################################################################
 
    main = "#!/bin/bash\n"
    main = main + "NODES=1\n"
    main = main + "TIME=30\n"
    main = main + "ACCT=QMCPACK\n"
    main = main + "EMAIL=galbraithm@duq.edu\n"
    main = main + "OUTPUT=cusp_calc\n"
    main = main + "qsub -A $ACCT -t $TIME -n $NODES -M $EMAIL  -O $OUTPUT ./cusp.sh\n"

    thisfile = directory +"/CuspCorrection/cusp_submission.sh"
    with open(thisfile,"w") as fileOut:
	fileOut.write("%s" %main)

def generateOptimization(directory,fileroot,sub_path,baseName):

    main = "<?xml version=\"1.0\"?>\n"
    main = main + "<simulation>\n"
    main = main +"  <project id=\"Opt-"+fileroot+"\" series=\"1\"/>\n"
    main = main +"  <!-- input from quantum package converter -->\n"
    main = main +"  <include href=\""+sub_path+"/"+baseName+"/"+fileroot+".ptcl.xml\"/>\n"
    main = main +"  <include href=\""+sub_path+"/"+baseName+"/"+fileroot+".wfs.xml\"/>\n"
    main = main +"  <!--  Hamiltonian -->\n"
    main = main +"  <hamiltonian name=\"h0\" type=\"generic\" target=\"e\">\n"
    main = main +"    <pairpot name=\"IonElec\" type=\"coulomb\" source=\"ion0\" target=\"e\"/>\n"
    main = main +"    <constant name=\"IonIon\" type=\"coulomb\" source=\"ion0\" target=\"ion0\"/>\n"
    main = main +"    <pairpot name=\"ElecElec\" type=\"coulomb\" source=\"e\" target=\"e\" physical=\"true\"/>\n"
    main = main +"  </hamiltonian>\n\n\n"
    main = main +" <init source=\"ion0\" target=\"e\"/>\n"
    main = main +"  <qmc method=\"vmc\" move=\"pbyp\" checkpoint=\"-1\" gpu=\"yes\">\n"
    main = main +"    <estimator name=\"LocalEnergy\" hdf5=\"no\"/>\n"
    main = main +"    <parameter name=\"walkers\">   1</parameter>\n"
    main = main +"    <parameter name=\"step\">    1</parameter>\n"
    main = main +"    <parameter name=\"substeps\">  5 </parameter>\n"
    main = main +"    <parameter name=\"warmupSteps\">  10 </parameter>\n"
    main = main +"    <parameter name=\"blocks\"> 50</parameter>\n"
    main = main +"    <parameter name=\"timestep\">  0.5 </parameter>\n"
    main = main +"    <parameter name=\"usedrift\">   no </parameter>\n"
    main = main +"  </qmc>\n\n"

    main = main +"<loop max=\"2\">\n"
    main = main +"  <qmc method=\"linear\" move=\"pbyp\" checkpoint=\"-1\" gpu=\"yes\">\n"
    main = main +"    <parameter name=\"blocks\"> 20</parameter>\n"
    main = main +"    <parameter name=\"warmupSteps\">  40</parameter>\n"
    main = main +"    <parameter name=\"substeps\">  20 </parameter>\n"
    main = main +"    <parameter name=\"timestep\">  0.5 </parameter>\n"
    main = main +"    <parameter name=\"walkers\">   1</parameter>\n"
    main = main +"    <parameter name=\"minwalkers\">  0.001 </parameter>\n"
    main = main +"    <parameter name=\"usedrift\">   no </parameter>\n"
    main = main +"    <estimator name=\"LocalEnergy\" hdf5=\"no\"/>\n"
    main = main +"    <cost name=\"energy\">                   0.9 </cost>\n"
    main = main +"    <cost name=\"unreweightedvariance\">     0.0 </cost>\n"
    main = main +"    <cost name=\"reweightedvariance\">       0.1 </cost>\n"
    main = main +"    <parameter name=\"MinMethod\">OneShiftOnly</parameter>\n"
    main = main +"    <parameter name=\"nonlocalpp\">yes</parameter>\n"
    main = main +"    <parameter name=\"useBuffer\">no</parameter>\n"
    main = main +"  </qmc>\n"
    main = main +"</loop>\n"

    main = main +"<loop max=\"40\">\n"
    main = main +"  <qmc method=\"linear\" move=\"pbyp\" checkpoint=\"-1\" gpu=\"yes\">\n"
    main = main +"    <parameter name=\"blocks\"> 40</parameter>\n"
    main = main +"    <parameter name=\"warmupSteps\">  40</parameter>\n"
    main = main +"    <parameter name=\"substeps\">  20 </parameter>\n"
    main = main +"    <parameter name=\"timestep\">  0.5 </parameter>\n"
    main = main +"    <parameter name=\"walkers\">   1</parameter>\n"
    main = main +"    <parameter name=\"minwalkers\">  0.5 </parameter>\n"
    main = main +"    <parameter name=\"usedrift\">   no </parameter>\n"
    main = main +"    <estimator name=\"LocalEnergy\" hdf5=\"no\"/>\n"
    main = main +"    <cost name=\"energy\">                   0.9 </cost>\n"
    main = main +"    <cost name=\"unreweightedvariance\">     0.0 </cost>\n"
    main = main +"    <cost name=\"reweightedvariance\">       0.1 </cost>\n"
    main = main +"    <parameter name=\"MinMethod\">OneShiftOnly</parameter>\n"
    main = main +"    <parameter name=\"nonlocalpp\">yes</parameter>\n"
    main = main +"    <parameter name=\"useBuffer\">no</parameter>\n"
    main = main +"    <parameter name=\"shift_i\"> 0.1</parameter>\n"
    main = main +"  </qmc>\n"
    main = main +"</loop>\n"

    main = main +"</simulation>\n"
    thisfile = directory +"/Optimization/Opt.xml"
    with open(thisfile,"w") as fileOut:
	fileOut.write("%s" %main)
    ### bgq.sh
    main=""
    main = main+"#!/bin/bash\n"
    main = main+"queue=default\n"
    main = main+"acct=PSFMat\n"
    main = main+"time=60\n"
    main = main+"EMAIL=\"galbraithm@duq.edu\"\n"
    main = main+"nodes=128\n"
    main = main+"nthreads=32\n"
    main = main+"mode=c1\n"
    main = main+"bin=qmcpack\n"
    main = main+"bindir=/soft/applications/qmcpack/current/build_XL_real/bin\n"
    main = main+"intemplate=Opt-HF.xml\n"
    main = main+"title=bgq.Opt-QP-HF-${mode}_p${nodes}x${nthreads}.`date +\"%m-%d-%y_%H%M\"`\n"
    main = main+"qmcin=$intemplate\n"
    main = main+"qmcout=${title}\n"
    main = main+"qsub -A $acct -M $EMAIL -q $queue -n $nodes -t $time -O ${qmcout} --mode $mode --env BG_SHAREDMEMSIZE=32:OMP_NUM_THREADS=${nthreads} $bindir/$bin $qmcin\n"

    thisfile = directory +"/Optimization/bgq.sh"
    with open(thisfile,"w") as fileOut:
	fileOut.write("%s" %main)




def generateDMC(directory,fileroot,sub_path,baseName):


    main = "<?xml version=\"1.0\"?>\n"
    main = main + "<simulation>\n"
    main = main +"  <project id=\"DMC-"+fileroot+"\" series=\"1\"/>\n"
    main = main +"  <!-- input from quantum package converter -->\n"
    main = main +"  <include href=\""+sub_path+"/"+baseName+"/"+fileroot+".ptcl.xml\"/>\n"
    main = main +"  <include href=\""+sub_path+"/"+baseName+"/"+fileroot+".wfs.xml\"/>\n"
    main = main +"  <!--  Hamiltonian -->\n"
    main = main +"  <hamiltonian name=\"h0\" type=\"generic\" target=\"e\">\n"
    main = main +"    <pairpot name=\"IonElec\" type=\"coulomb\" source=\"ion0\" target=\"e\"/>\n"
    main = main +"    <constant name=\"IonIon\" type=\"coulomb\" source=\"ion0\" target=\"ion0\"/>\n"
    main = main +"    <pairpot name=\"ElecElec\" type=\"coulomb\" source=\"e\" target=\"e\" physical=\"true\"/>\n"
    main = main +"  </hamiltonian>\n\n\n"
    main = main +" <init source=\"ion0\" target=\"e\"/>\n"
    main = main +"  <qmc method=\"vmc\" move=\"pbyp\" gpu=\"yes\">\n"
    main = main +"    <estimator name=\"LocalEnergy\" hdf5=\"no\"/>\n"
    main = main +"    <parameter name=\"walkers\">   1</parameter>\n"
    main = main +"    <parameter name=\"samplesperthread\">    1 </parameter>\n"
    main = main +"    <parameter name=\"stepsbetweensamples\">    10 </parameter>\n"
    main = main +"    <parameter name=\"substeps\">  30 </parameter>\n"
    main = main +"    <parameter name=\"warmupSteps\"> 100 </parameter>\n"
    main = main +"    <parameter name=\"blocks\"> 10</parameter>\n"
    main = main +"    <parameter name=\"timestep\">  0.5 </parameter>\n"
    main = main +"    <parameter name=\"usedrift\">   no </parameter>\n"
    main = main +"  </qmc>\n\n\n"
    main = main +"  <qmc method=\"dmc\" move=\"pbyp\" checkpoint=\"-1\" gpu=\"yes\">\n"
    main = main +"    <estimator name=\"LocalEnergy\" hdf5=\"no\"/>\n"
    main = main +"    <parameter name=\"targetwalkers\">4000</parameter>\n"
    main = main +"    <parameter name=\"reconfiguration\">   no </parameter>\n"
    main = main +"    <parameter name=\"warmupSteps\">  50 </parameter>\n"
    main = main +"    <parameter name=\"timestep\">  0.001 </parameter>\n"
    main = main +"    <parameter name=\"steps\">   30 </parameter>\n"
    main = main +"    <parameter name=\"blocks\">  100</parameter>\n"
    main = main +"    <parameter name=\"nonlocalmoves\">  yes </parameter>\n"
    main = main +"  </qmc>\n"
    main = main +"</simulation>\n"
    thisfile = directory +"/DMC/DMC.xml"
    with open(thisfile,"w") as fileOut:
	fileOut.write("%s" %main)


    ### bgq.sh
    main=""
    main = main+"#!/bin/bash\n"
    main = main+"queue=default\n"
    main = main+"acct=PSFMat\n"
    main = main+"time=60\n"
    main = main+"EMAIL=\"galbraithm@duq.edu\"\n"
    main = main+"nodes=128\n"
    main = main+"nthreads=32\n"
    main = main+"mode=c1\n"
    main = main+"bin=qmcpack\n"
    main = main+"bindir=/soft/applications/qmcpack/current/build_XL_real/bin\n"
    main = main+"intemplate=DMC-HF.xml\n"
    main = main+"title=bgq.DMC-QP-HF-${mode}_p${nodes}x${nthreads}.`date +\"%m-%d-%y_%H%M\"`\n"
    main = main+"qmcin=$intemplate\n"
    main = main+"qmcout=${title}\n"
    main = main+"qsub -A $acct -M $EMAIL -q $queue -n $nodes -t $time -O ${qmcout} --mode $mode --env BG_SHAREDMEMSIZE=32:OMP_NUM_THREADS=${nthreads} $bindir/$bin $qmcin\n"

    thisfile = directory +"/DMC/bgq.sh"
    with open(thisfile,"w") as fileOut:
	fileOut.write("%s" %main)


