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
    tmpfile = myfile+".tmp"
    f = open( tmpfile,"w")
    f.write("<?xml version=\"1.0\"?>\n")
    f.write(etree.tostring(root,pretty_print=True))
    f.close()

    os.system("mv " + tmpfile + " " + myfile)


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
    wfsFile =  sub_path+"/"+baseName+"/"+fileroot+".wfs.xml"
    icld_ptcl.set("href",ptclFile)
    icld_wfs.set("href",wfsFile)

    ###### NOW WRITE THE MODIFICATIONS TO A FILE
    tmpfile = myfile+".tmp"
    f = open( tmpfile,"w")
    f.write("<?xml version=\"1.0\"?>\n")
    f.write(etree.tostring(root,pretty_print=True))
    f.close()

    os.system("mv " + tmpfile + " " + myfile)

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

    myFile = directory+"/DMC/DMC.xml"
    tree = etree.parse(myFile)
    ## Modify Cusp.xml for your system

    root = tree.getroot()

    project = root[0]
    icld_ptcl = root[2]
    icld_wfs = root[3]
    
    projName = "DMC-"+fileroot
    project.set("id",projName)

    ptclFile = sub_path+"/"+baseName+"/"+fileroot+".ptcl.xml"
    wfsFile =  sub_path+"/"+baseName+"/"+fileroot+".wfs.xml"
    icld_ptcl.set("href",ptclFile)
    icld_wfs.set("href",wfsFile)

    ###### NOW WRITE THE MODIFICATIONS TO A FILE
    tmpfile = myfile+".tmp"
    f = open( tmpfile,"w")
    f.write("<?xml version=\"1.0\"?>\n")
    f.write(etree.tostring(root,pretty_print=True))
    f.close()

    os.system("mv " + tmpfile + " " + myfile)

    ################################################
    ### Generate bgq-DMC.sh
    ################################################
    os.system("cp misc/bgq-DMC.sh "+directory+"/DMC/")
