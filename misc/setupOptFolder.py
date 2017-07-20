import os
################################################
#### Generate : Opt.xml
################################################
import lxml
from lxml import etree

import sys

outerDir=sys.argv[1]
info = outerDir.split("_")
if len(info)==3:
	[Jtype, multi,reopt] = info
	reopt = reopt=="reopt"
else:
	[Jtype, multi] = info
	reopt=False
	
Jtype = Jtype.replace("Jastrow","")
multi = multi=="MultiDet"

if Jtype!="No":
	fileroot=sys.argv[2]
	filename = sys.argv[3]
	usepp = sys.argv[4]

	if usepp:
	    template_Name = "Opt_PP.xml"
	else:
	    template_Name = "Opt_AE.xml"
    
	Opt_dir = outerDir + "/Optimization"
	if not(os.path.isdir(Opt_dir)):
	    os.mkdir(Opt_dir)
	os.system("cp misc/"+template_Name+" " +Opt_dir+"/Opt.xml")
	os.system("cp utils/plot_OptProg.py " +Opt_dir)

	myFile = Opt_dir+"/Opt.xml"
	tree = etree.parse(myFile)
	root = tree.getroot()

	project = root[0]
	icld_ptcl = root[2]
	icld_wfs = root[3]

	projName = "Opt-"+wfsFile
	project.set("id",projName)

	ptclFile = fileroot +".ptcl.xml"
	wfsFile =  fileroot +".wfs.xml"
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
	### Generate bgq-DMC.sh
	################################################
	os.system("cp misc/bgq-Opt.sh "+directory+"/Optimization/")
	


	if multi:
	    fileName= "optimize_1Body2Body_multi"
	else:
	    fileName= "optimize_1Body2Body_single"
	os.system("cp misc/"+fileName+".py "+Opt_dir)
	    
	if reopt:
		os.system("cp misc/optimize_coeffs.py "+Opt_dir)

	if "3" in  Jtype:
		os.system("cp misc/optimize_3Body.py "+Opt_dir)

	os.system("cp misc/optimize_finish.py "+Opt_dir)
