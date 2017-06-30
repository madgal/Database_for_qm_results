def generateCuspCorrection(directory,fileroot,sub_path,baseName):
    import os

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


    #### cusp.sh
    main = "#!/bin/bash\n\n"

    main = main +"BINDIR=/soft/applications/qmcpack/github/build_intel_real/bin\n"
    main = main +"FILEIN="+sub_path+"/"+baseName+"/CuspCorrection/cusp.xml\n"
    main = main +"$BINDIR/qmcpack $FILEIN \n"

    thisfile = directory +"/CuspCorrection/cusp.sh"
    with open(thisfile,"w") as fileOut:
	fileOut.write("%s" %main)

    os.system("cp misc/cusp_submission.sh "+directory+"/CuspCorrection/")


def generateOptimization(directory,fileroot,sub_path,baseName):
    import os

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

    os.system("cp misc/bgq-Opt.sh "+directory+"/Optimization/")

def generateDMC(directory,fileroot,sub_path,baseName):
    import os


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

    os.system("cp misc/bgq-DMC.sh "+directory+"/DMC/")
