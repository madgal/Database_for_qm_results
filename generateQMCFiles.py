def generateCuspCorrection(directory,fileroot,sub_path,baseName):
    import os

    ################################################
    #### Generate : Cusp.xml
    ################################################
    import lxml
    from lxml import etree

    os.system("cp misc/Cusp.xml " +directory +"/CuspCorrection/")

    myFile = directory+"/CuspCorrection/Cusp.xml"
    tree = etree.parse(myFile)
    ## Modify Cusp.xml for your system

    root = tree.getroot()

    project = root[0]
    icld_ptcl = root[2]
    icld_wfs = root[3]
    
    project.set("id",fileroot)

    ptclFile = sub_path+"/"+baseName+"/"+fileroot+".ptcl.xml"
    wfsFile =  sub_path+"/"+baseName+"/"+fileroot+".wfs.xml"
    icld_ptcl.set("href",ptclFile)
    icld_wfs.set("href",wfsFile)

    ###### NOW WRITE THE MODIFICATIONS TO A FILE
    tmpfile = myFile+".tmp"
    f = open( tmpfile,"w")
    f.write("<?xml version=\"1.0\"?>\n")
    f.write(etree.tostring(root,pretty_print=True))
    f.close()

    os.system("mv " + tmpfile + " " + myFile)


    ################################################
    #### Generate : cusp.sh
    ################################################
    main = "#!/bin/bash\n\n"

    main = main +"BINDIR=/soft/applications/qmcpack/github/build_intel_real/bin\n"
    main = main +"FILEIN="+sub_path+"/"+baseName+"/CuspCorrection/Cusp.xml\n"
    main = main +"$BINDIR/qmcpack $FILEIN \n"

    thisfile = directory +"/CuspCorrection/cusp.sh"
    with open(thisfile,"w") as fileOut:
	fileOut.write("%s" %main)

    ################################################
    #### Generate : cusp_submission.sh
    ################################################
    os.system("cp misc/cusp_submission.sh "+directory+"/CuspCorrection/")


def generateOptimization(directory,fileroot,sub_path,baseName):
    import os
    ################################################
    #### Generate : Opt.xml
    ################################################
    import lxml
    from lxml import etree

    os.system("cp misc/Opt.xml " +directory +"/Optimization/")
    os.system("cp utils/plot_OptProg.py " +directory +"/Optimization/")

    myFile = directory+"/Optimization/Opt.xml"
    tree = etree.parse(myFile)
    ## Modify Cusp.xml for your system

    root = tree.getroot()

    project = root[0]
    icld_ptcl = root[2]
    icld_wfs = root[3]
    
    projName = "Opt-"+fileroot
    project.set("id",projName)

    ptclFile = sub_path+"/"+baseName+"/"+fileroot+".ptcl.xml"
    wfsFile =  sub_path+"/"+baseName+"/"+fileroot+"_0.01.wfs.xml"
    icld_ptcl.set("href",ptclFile)
    icld_wfs.set("href",wfsFile)

    ###### NOW WRITE THE MODIFICATIONS TO A FILE
    tmpfile = myFile+".tmp"
    f = open( tmpfile,"w")
    f.write("<?xml version=\"1.0\"?>\n")
    f.write(etree.tostring(root,pretty_print=True))
    f.close()

    os.system("mv " + tmpfile + " " + myFile)
   
    #################################################
    os.system("cp misc/cutoff_gen.py "  +directory +"/Optimization/")
    
    #################################################
    ### Generate: setup_OptFile1.py
    #################################################
    main  = ""
    main = main +"#!/usr/bin/env python\n"
    main = main +"# -*- coding: utf-8 -*- \n"
    main = main + "import os\n\n"
    main = main + "cutoff=0.01\n"
    main = main + "os.system(\"./cutoff_gen.py "+fileroot + " \"+str(cutoff))\n"
 
    filename = directory +"/Optimization/setup_OptFile1.py"
    with open(filename,"w") as f:
	f.write("%s" %main)

    #################################################
    ### Generate: setup_OptFile2.py
    #################################################
    main  = ""
    main = main +"#!/usr/bin/env python\n"
    main = main +"# -*- coding: utf-8 -*- \n"
    main = main + "import os\n"
    main = main + "import sys\n"
    main = main + "import lxml\n"
    main = main + "from lxml import etree \n\n"

    main = main + "myfile =\"../"+fileroot+"_0.01.wfs.xml\"\n"
    main = main +"os.system(\"cp \" + myfile + \" \" + myfile+\"_BAK \")\n\n"

    main = main + "series = sys.argv[1]\n"
    main = main + "optfile = \"" + fileroot  + "_0.01.s\" + series +\".opt.xml\"\n"
    main = main + "os.system(\"cp \" +optfile +\" \" + myfile)\n"


    main = main + "tree= etree.parse(myfile)\n"
    main = main + "root = tree.getroot()\n"
    main = main + "wavefunc = root[0]\n"
    main = main + "j3Body= wavefunc[3]\n"
    main = main + "for corr in j3Body:\n"
    main = main + "    corr[0].set(\"optimize\",\"yes\")\n"

    main = main +"###### NOW WRITE THE MODIFICATIONS TO A FILE\n"
    main = main +"tmpfile = myfile+\".tmp\"\n"
    main = main +"f = open( tmpfile,\"w\")\n"
    main = main +"f.write(\"<?xml version=\\\"1.0\\\"?>\\n\")\n"
    main = main +"f.write(etree.tostring(root,pretty_print=True))\n"
    main = main +"f.close()\n"

    main = main +"os.system(\"mv \" + tmpfile + \" \" + myfile)\n"


    main = main +"###### NOW WRITE THE MODIFICATIONS TO A FILE\n"
    main = main +"tmpfile = myfile+\".tmp\"\n"
    main = main + "myfile =\"Opt.xml\"\n"
    main = main + "tree= etree.parse(myfile)\n"
    main = main + "root = tree.getroot()\n"
    main = main + "proj = root[0]\n"
    main = main + "proj.set(\"series\",\"44\")\n"
    main = main +"tmpfile = myfile+\".tmp\"\n"
    main = main +"f = open( tmpfile,\"w\")\n"
    main = main +"f.write(\"<?xml version=\\\"1.0\\\"?>\\n\")\n"
    main = main +"f.write(etree.tostring(root,pretty_print=True))\n"
    main = main +"f.close()\n"

    main = main +"os.system(\"mv \" + tmpfile + \" \" + myfile)\n"

 
    filename = directory +"/Optimization/setup_OptFile2.py"
    with open(filename,"w") as f:
	f.write("%s" %main)

    ################################################
    ### Generate bgq-Opt.sh
    ################################################
    os.system("cp misc/bgq-Opt.sh "+directory+"/Optimization/")

def generateDMC(directory,fileroot,sub_path,baseName):
    import os
    ################################################
    #### Generate : Opt.xml
    ################################################
    import lxml
    from lxml import etree

    os.system("cp misc/DMC.xml " +directory +"/DMC/")
    os.system("cp utils/format_data.py " +directory +"/DMC/")

    myFile = directory+"/DMC/DMC.xml"
    tree = etree.parse(myFile)
    ## Modify Cusp.xml for your system

    root = tree.getroot()

    project = root[0]
    icld_ptcl = root[2]
    icld_wfs = root[3]
    
    projName = "DMC-"+fileroot+"_0.01"
    project.set("id",projName)

    ptclFile = sub_path+"/"+baseName+"/"+fileroot+".ptcl.xml"
    wfsFile =  sub_path+"/"+baseName+"/"+fileroot+"_0.01.wfs.xml"
    icld_ptcl.set("href",ptclFile)
    icld_wfs.set("href",wfsFile)

    ###### NOW WRITE THE MODIFICATIONS TO A FILE
    tmpfile = myFile+".tmp"
    f = open( tmpfile,"w")
    f.write("<?xml version=\"1.0\"?>\n")
    f.write(etree.tostring(root,pretty_print=True))
    f.close()

    os.system("mv " + tmpfile + " " + myFile)

    ###############################################
    ### generate massive script for convergence
    ###############################################

    main="#!/bin/bash\n"
    main= main +"NAME=" +fileroot+"\n"
    main= main +"DIR=" +sub_path+"\n" 
    main = main +"./bgq-DMC.sh   #0.01\n"
    main = main + "#./runDMC.py $NAME $DIR 0.008\n"
    main = main +"#./runDMC.py $NAME $DIR 0.006\n"
    main = main + "#./runDMC.py $NAME $DIR 0.004\n"
    main = main +"#./runDMC.py $NAME $DIR 0.002\n"
    main = main + "#./runDMC.py $NAME $DIR 0.0009\n"
    main =  main +"#./runDMC.py $NAME $DIR 0.0007\n"
    main =  main +"#./runDMC.py $NAME $DIR 0.0005\n"
    main = main + "#./runDMC.py $NAME $DIR 0.0003\n"
    main = main + "#./runDMC.py $NAME $DIR 0.0001\n"
    main =  main +"#./runDMC.py $NAME $DIR 0.00008\n"
    main =  main +"#./runDMC.py $NAME $DIR 0.00006\n"
    main = main + "#./runDMC.py $NAME $DIR 0.00004\n"
    main =  main +"#./runDMC.py $NAME $DIR 0.00002\n"
   
    filename = directory + "/DMC/converge.sh"
    with open(filename,"w") as f:
         f.write("%s" %main)
   

    os.system("cp misc/runDMC.py " + directory+"/DMC")
    os.system("cp misc/cutoff_gen.py " + directory+"/DMC")


    ################################################
    ### Generate bgq-DMC.sh
    ################################################
    os.system("cp misc/bgq-DMC.sh "+directory+"/DMC/")

def generateSystemSetup(directory,fileroot,sub_path,baseDir):

    ##############################################
    #### Generate system setup
    #############################################
    main = ""
    main = main + "#!/usr/bin/env python\n"
    main = main + "# -*- coding: utf-8 -*-\n\n"
    main = main + "import os \n"
    main = main + "os.system(\"cp "+fileroot+".wfs.xml "+fileroot+".wfs.xml_initial\")\n\n"
    main = main + "import lxml\n"
    main = main + "from lxml import etree\n\n"
    main = main + "myfile =\""+fileroot+".wfs.xml\"\n"
    main = main + "tree= etree.parse(myfile)\n"
    main = main + "root = tree.getroot()\n"
    main = main + "wavefunc = root[0]\n"
    main = main + "determinantset = wavefunc[0]\n"
    main = main + "sposet_up= determinantset[1]\n"
    main = main + "sposet_dn= determinantset[2]\n"
    main = main + "multidet = determinantset[3]\n"
    main = main + "MyCuspUp =\""+sub_path +"/"+baseDir+"/CuspCorrection/spo-up.cuspInfo.xml\"\n"
    main = main + "sposet_up.set(\"cuspInfo\",MyCuspUp)\n"
    main = main + "MyCuspDn =\""+sub_path +"/"+baseDir+"/CuspCorrection/spo-dn.cuspInfo.xml\"\n"
    main = main + "sposet_dn.set(\"cuspInfo\",MyCuspDn)\n"
    main = main + "multidet.set(\"optimize\",\"no\")\n\n"
    main = main + "rcut_12 = 10\n"
    main = main + "j2Body= wavefunc[1]\n"
    main = main + "j1Body= wavefunc[2]\n"
    main = main + "for corr in j2Body:\n"
    main = main + "    corr.set(\"rcut\",str(rcut_12))\n"
    main = main + "for corr in j1Body:\n"
    main = main + "    corr.set(\"rcut\",str(rcut_12))\n\n"
    main = main + "j3Body= wavefunc[3]\n"
    main = main + "for corr in j3Body:\n"
    main = main + "    corr.set(\"rcut\",\"3\")\n"
    main = main + "    corr[0].set(\"optimize\",\"no\")\n"

    main = main +"###### NOW WRITE THE MODIFICATIONS TO A FILE\n"
    main = main +"tmpfile = myfile+\".tmp\"\n"
    main = main +"f = open( tmpfile,\"w\")\n"
    main = main +"f.write(\"<?xml version=\\\"1.0\\\"?>\\n\")\n"
    main = main +"f.write(etree.tostring(root,pretty_print=True))\n"
    main = main +"f.close()\n"

    main = main +"os.system(\"mv \" + tmpfile + \" \" + myfile)\n"
    main = main + "os.system(\"cp \"+myfile+\" "+fileroot+".wfs.xml_template\")\n"
    
    filename = directory + "/setupSystemInitial.py"
    with open (filename,"w") as f:
         f.write("%s" %main)

def finalizeTemplate(directory, fileroot):

    main  = ""
    main = main +"#!/usr/bin/env python\n"
    main = main +"# -*- coding: utf-8 -*- \n"
    main = main + "import os\n"
    main = main + "import sys\n"
    main = main + "from copy import deepcopy\n"
    main = main + "import lxml\n"
    main = main + "from lxml import etree \n\n"

    main = main + "optFile =\"../"+fileroot+"_0.01.wfs.xml\"\n"
    main = main +"os.system(\"cp \" + optFile + \" \" + optFile+\"_BAK2\")\n\n"
    main = main + "series = sys.argv[1]\n"
    main = main + "optFinal= \"" + fileroot  + "_0.01.s\" + series +\".opt.xml\"\n"
    main = main + "os.system(\"cp \" +optFinal+\" \" + optFile)\n"

    main = main + "template =\"../"+fileroot+".wfs.xml_template\"\n\n"

    main = main + "tree= etree.parse(optFile)\n"
    main = main + "root = tree.getroot()\n"
    main = main + "wavefunc = root[0]\n"
    main = main + "j2Body= wavefunc[1]\n"
    main = main + "j1Body= wavefunc[2]\n"
    main = main + "j3Body= wavefunc[3]\n\n"


    main = main +"## replace the old jastrows\n" 
    main = main +"tree2= etree.parse(template)\n"
    main = main +"root2 = tree2.getroot()\n"
    main = main + "wavefunc2 = root2[0]\n"
    main = main + "j2Body2= wavefunc2[1]\n"
    main = main + "j1Body2= wavefunc2[2]\n"
    main = main + "j3Body2= wavefunc2[3]\n\n"

    main = main +"wavefunc2.remove(j2Body2)\n"
    main = main +"wavefunc2.remove(j1Body2)\n"
    main = main +"wavefunc2.remove(j3Body2)\n\n"
    main = main +"wavefunc2.append(deepcopy(j2Body))\n"
    main = main +"wavefunc2.append(deepcopy(j1Body))\n"
    main = main +"wavefunc2.append(deepcopy(j3Body))\n"
	
    

    main = main +"###### NOW WRITE THE MODIFICATIONS TO A FILE\n"
    main = main +"tmpfile = template+\".tmp\"\n"
    main = main +"f = open( tmpfile,\"w\")\n"
    main = main +"f.write(\"<?xml version=\\\"1.0\\\"?>\\n\")\n"
    main = main +"f.write(etree.tostring(root,pretty_print=True))\n"
    main = main +"f.close()\n"

    main = main +"os.system(\"mv \" + tmpfile + \" \" + template)\n"
    
    filename = directory +"/Optimization/finalize_template.py"
    with open(filename, 'w') as f:
	f.write("%s" %main)
 
 
