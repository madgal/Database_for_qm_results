# -*- coding: utf-8 -*-

def recreate_wfs(filename,runNum):
def recreate_ptcl(filename,runNum):
def recreate_Opt(filename,runNum):
        from lxml import etree
	
	tree = etree.parse("misc/Opt_template.xml")
	root = tree.getroot()
	id_num=runNum
	vmc_method_tags = ""
   	vmc_estimator = "" 
   	vmc_parameters= "" 
	opt_loop1_tag = ""
	opt_loop1_qmc  = ""
	opt_estimator1 = ""
	opt_costFunc1 = ""
	opt_parameter1 = ""
	opt_loop2_tag = ""
	opt_loop2_qmc  = ""
	opt_estimator2 = ""
        opt_costFunc2  = ""                  
        opt_parameter2   = ""                    

        vmc = etree.SubElement(root, "qmc")
	mydict = vmc_method_tags.split(",")
	for val in mydict:
            pair = val.split("=")
    	    vmc.set(pair[0],pair[1])

	mydict = vmc_estimator.split(",")
	est = etree.SubElement(vmc,"estimator")
	for val in mydict:
            pair = val.split("=")
    	    est.set(pair[0],pair[1])

        mydict = vmc_parameters.split(",")
	for val in mydict:
	    parm = etree.SubElement(vmc,"parameter")
	    pair = val.split("=")
	    parm.set("name",pair[0])
	    parm.text = pair[1]


	loop1 = etree.SubElement(root,"loop")
	opt_loop1_tag = opt_loop1_tag.split("=")
	loop1.set("max",opt_loop1_tag[1])
	opt1 = etree.SubElement(loop1,"qmc")
	mydict = opt_loop1_qmc.split(",")
	for val in mydict:
            pair = val.split("=")
    	    opt1.set(pair[0],pair[1])

	mydict = opt_estimator1.split(",")
	est = etree.SubElement(loop1,"estimator")
	for val in mydict:
            pair = val.split("=")
    	
        mydict = opt_parameter1.split(",")
	for val in mydict:
	    parm = etree.SubElement(loop1,"parameter")
	    pair = val.split("=")
	    parm.set("name",pair[0])
	    parm.text = pair[1]

        mydict = opt_costFunc1.split(",")
	for val in mydict:
	    parm = etree.SubElement(loop1,"cost")
	    pair = val.split("=")
	    parm.set("name",pair[0])
	    parm.text = pair[1]


	loop2 = etree.SubElement(root,"loop")
	opt_loop2_tag = opt_loop2_tag.split("=")
	loop2.set("max",opt_loop2_tag[1])
	opt2 = etree.SubElement(loop2,"qmc")
	mydict = opt_loop2_qmc.split(",")
	for val in mydict:
            pair = val.split("=")
    	    opt2.set(pair[0],pair[1])

	mydict = opt_estimator2.split(",")
	est = etree.SubElement(loop2,"estimator")
	for val in mydict:
            pair = val.split("=")
    	
        mydict = opt_parameter2.split(",")
	for val in mydict:
	    parm = etree.SubElement(loop2,"parameter")
	    pair = val.split("=")
	    parm.set("name",pair[0])
	    parm.text = pair[1]

        mydict = opt_costFunc2.split(",")
	for val in mydict:
	    parm = etree.SubElement(loop2,"cost")
	    pair = val.split("=")
	    parm.set("name",pair[0])
	    parm.text = pair[1]

def recreate_DMC(filename,runNum):

