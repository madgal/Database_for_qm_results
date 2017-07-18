# -*- coding: utf-8 -*-

def pullDataFromWFS(filename,runNum):
	from lxml import etree

	tree = etree.parse(filename)
	wfs = tree.getroot()[0]

	detset = ""
	jastrow =""
	## set default num determinants to 1 so we only need to update if its a multireference system
	ndet=1
	for child in wfs:
		if child.tag =="determinantset":
		for sub_child in child:
			if sub_child.tag=="multideterminant":
				optimize = sub_child.get("optimize")
				for next_child in sub_child:
					if next_child.tag=="detlist":
						ndet=next_child.get("size")
						cutoff=next_child.get("cutoff")
		j2=False
		j1=False
		j3=False
		elif child.tag=="jastrow":
			if child.get("name")=="J2":
				j2=True
				j2_func = child.get("function")
				j2_rcut = child[0].get("rcut")
			elif child.get("name")=="J1":
				j1=True
				j1_func = child.get("function")
				j1_rcut = child[0].get("rcut")
			elif child.get("name")=="J3":
				j3=True
				j3_func = child.get("function")
				j3_rcut = child[0].get("rcut")

	detset = "(optimize="+optimize+",N_det="+ndet+",cutoff="+cutoff+")"
	if j2:
		jastrow = "(use_J2="+j2+",function="+j2_func+",rcut="+j2_rcut
	else:
		jastrow = "(use_J2="+j2
	if j1:
		jastrow = ",use_J1="+j1+",function="+j1_func+",rcut="+j1_rcut
	else:
		jastrow = ",use_J1="+j1
	
	if j3:
		jastrow = ",use_J3="+j3+",function="+j3_func+",rcut="+j3_rcut+")"
	else:
		jastrow = ",use_J3="+j3+")"
	

#def pullDataFromPTCL(filename,runNum):
def pullDataFromOPT(filename,runNum):
        from lxml import etree

	tree= etree.parse(filename)
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

        for child in root:
            if child.tag=='qmc':
		for x in child.attrib:
		    vmc_method_tags = vmc_method_tags +x+ '='+child.attrib[x]+","	
		for y in child:
	  	    if y.tag=="estimator":
			for x in y.attrib:
			    vmc_estimator = vmc_estimator + x + "="+ y.attrib[x] + ","
	 	    else:
			vmc_parameters = vmc_parameters + y.attrib['name'] + "="+ y.text.replace(" ","") + "," 
            elif child.tag =="loop":
		if len(opt_loop1_tag)<1:#This is the first opt loop
			opt_loop1_tag = "max=" + child.attrib["max"]
                        for x in child[0].attrib:
				opt_loop1_qmc = opt_loop1_qmc + x + "=" + child[0].attrib[x]+","

                       	for y in child[0]:
				if y.tag =="estimator":
					for x in y.attrib:
						opt_estimator1 = opt_estimator1 + x+ "=" + y.attrib[x] + ","
				elif y.tag =="cost":
					opt_costFunc1 = opt_costFunc1 + y.attrib['name']+ "=" + y.text.replace(" ","")+","
				else:
					opt_parameter1 = opt_parameter1 + y.attrib['name']+ "=" + y.text.replace(" ","")+ ","
            	else: # this is the second opt loop
			opt_loop2_tag = "max=" + child.attrib["max"]
                        for x in child[0].attrib:
				opt_loop2_qmc = opt_loop2_qmc + x + "=" + child[0].attrib[x]+","

			for y in child[0]:
				if y.tag =="estimator":
					for x in y.attrib:
						opt_estimator2 = opt_estimator2 + x+ "=" + y.attrib[x] + ","
				elif y.tag =="cost":
					opt_costFunc2 = opt_costFunc2 + y.attrib['name']+ "=" + y.text.replace(" ","")+","
				else:
					opt_parameter2 = opt_parameter2 + y.attrib['name']+ "=" + y.text.replace(" ","")+ ","

                                     
	vmc_method_tags = vmc_method_tags[:-1]
	vmc_estimator = vmc_estimator[:-1]
	vmc_parameters= vmc_parameters[:-1]
	opt_loop1_qmc = opt_loop1_qmc[:-1]
	opt_estimator1 = opt_estimator1[:-1]
	opt_costFunc1 = opt_costFunc1[:-1]
	opt_parameter1 = opt_parameter1[:-1]
	opt_loop2_qmc = opt_loop2_qmc[:-1]
	opt_estimator2 = opt_estimator2[:-1]
	opt_costFunc2 = opt_costFunc2[:-1]
	opt_parameter2 = opt_parameter2[:-1]

	
	vmc_line = "("+vmc_method_tags+")"
	vmc_line = vmc_line + "("+vmc_estimator+")"
	vmc_line = vmc_line + "("+vmc_parameters+")"
	vmc_line = vmc_line + "("+vmc_parameters+")"
	vmc_line = vmc_line + "("+opt_loop1_qmc+")"
	vmc_line = vmc_line + "("+opt_estimator1+")"
	vmc_line = vmc_line + "("+opt_costFunc1+")"
	vmc_line = vmc_line + "("+opt_parameter1+")"
	vmc_line = vmc_line + "("+opt_loop2_qmc+")"
	vmc_line = vmc_line + "("+opt_estimator2+")"
	vmc_line = vmc_line + "("+opt_costFunc2+")"
	vmc_line = vmc_line + "("+opt_parameter2+")"



'''
	print "id_num=",runNum
	print "vmc_method_tags =",vmc_method_tags
   	print "vmc_estimator=",vmc_estimator
   	print "vmc_parameters=",vmc_parameters
	print "opt_loop1_tag =",opt_loop1_tag 
	print "opt_loop1_qmc=",opt_loop1_qmc
	print "opt_estimator1=",opt_estimator1
	print "opt_costFunc1 =",opt_costFunc1 
	print "opt_parameter1=",opt_parameter1
	print "opt_loop2_tag =",opt_loop2_tag 
	print "opt_loop2_qmc =",opt_loop2_qmc 
	print "opt_estimator2=",opt_estimator2
        print "opt_costFunc2 =",opt_costFunc2 
        print "opt_parameter2=",opt_parameter2

'''



def pullDataFromDMC(filename,runNum):
        from lxml import etree
	
	tree= etree.parse(filename)
	root = tree.getroot()
 	
  	id_num=runNum
        vmc_method_tags=""
   	vmc_estimator = "" 
   	vmc_parameters= "" 
        dmc_method_tags=""
   	dmc_estimator = "" 
   	dmc_parameters= "" 


        for child in root:
            if child.tag=='qmc':
                if child.attrib["method"]=="vmc":
		    for x in child.attrib:
			vmc_method_tags = vmc_method_tags +x+ '='+child.attrib[x]+","	
		    for y in child:
			if y.tag=="estimator":
				for x in y.attrib:
				    vmc_estimator = vmc_estimator + x + "="+ y.attrib[x] + ","
			else:
				vmc_parameters = vmc_parameters + y.attrib['name'] + "="+ y.text.replace(" ","") + "," 

                elif child.attrib["method"]=="dmc":
		    for x in child.attrib:
			dmc_method_tags = dmc_method_tags +x+ '='+child.attrib[x]+","

		    for y in child:
			if y.tag=="estimator":
				for x in y.attrib:
				    dmc_estimator = dmc_estimator + x + "="+ y.attrib[x] + ","
			else:
				dmc_parameters = dmc_parameters + y.attrib['name'] + "="+ y.text.replace(" ","") + "," 
	
	vmc_method_tags = vmc_method_tags[:-1]
	vmc_estimator = vmc_estimator[:-1]
	vmc_parameters= vmc_parameters[:-1]
	dmc_method_tags = dmc_method_tags[:-1]
	dmc_estimator = dmc_estimator[:-1]
	dmc_parameters= dmc_parameters[:-1]

        '''
	print "vmc_method_tags =",vmc_method_tags
   	print "vmc_estimator=",vmc_estimator
   	print "vmc_parameters=",vmc_parameters
	print "dmc_method_tags =",dmc_method_tags
   	print "dmc_estimator=",dmc_estimator
   	print "dmc_parameters=",dmc_parameters
        '''
	dmc_line = "("+vmc_method_tags+")"
	dmc_line =dmc_line + "("+vmc_estimator+")"
	dmc_line =dmc_line + "("+vmc_parameters+")"
	dmc_line =dmc_line + "("+dmc_method_tags+")"
	dmc_line =dmc_line + "("+dmc_estimator+")"
	dmc_line =dmc_line + "("+dmc_parameters+")"

