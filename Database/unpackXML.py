# -*- coding: utf-8 -*-

def pullDataFromWFS(filename,runNum):
	from lxml import etree

	tree = etree.parse(filename)
	wfs = tree.getroot()[0]

	for child in wfs:
                if child.tag=="determinantset":
                        detSet  = child
                        print detSet.tag
                        cuspCorrection=detSet.get("cuspCorrection")
                        for subChild in detSet:
                                if subChild.tag=="multideterminant":
                                        multidet="YES"
                                        mutlidet=multidet+",optimize="+subChild.get("optimize")
                                        multidet=multidet +",ndet="+subChild[0].get("size")
                                        multidet=multidet +",cutoff="+subChild[0].get("cutoff")
                elif child.tag=="jastrow" and child.get("name")=="J2":
                        j2list = "(function="+child.get("function") + ")"

                        for subChild in child:
                                j2list = j2list +"(rcut="               + subChild.get("rcut")
                                j2list = j2list +",size="               + subChild.get("size")
                                j2list = j2list +",id="                 + subChild[0].get("id")
                                j2list = j2list +"coefficients=\""      + subChild[0].text+"\")"


                elif child.tag=="jastrow" and child.get("name")=="J1":
                        j1list = "(function="+child.get("function") + ")"

                        for subChild in child:
                                j1list = j1list +"(rcut="               + subChild.get("rcut")
                                j1list = j1list +",size="               + subChild.get("size")
                                j1list = j1list +",id="                 + subChild[0].get("id")
                                j1list = j1list +"coefficients=\""      + subChild[0].text+"\")"

                elif child.tag=="jastrow" and child.get("name")=="J3":
                        j3list = "(function="+child.get("function") + ")"

                        for subChild in child:
                                j3list = j3list +"(rcut="               + subChild.get("rcut")
                                j3list = j3list +",isize="              + subChild.get("isize")
                                j3list = j3list +",esize="              + subChild.get("esize")
                                j3list = j3list +",id="                 + subChild[0].get("id")
                                j3list = j3list +"coefficients=\""      + subChild[0].text+"\")"

	wfsFile = etree.tostring(wfs)

	neededInfo = [cuspCorrection,multidet,j2list,j1list,j3list]

	return [neededInfo,wfsFile]


	

def pullDataFromPTCL(filename,runNum):
	from lxml import etree

	tree = etree.parse(filename)
	ptclset = tree.getroot()[0]

	ptclfile = etree.tostring(ptclset)
	return [ptclfile]


def pullDataFromOPT(filename,runNum):


	### There is no need to search through the optimization file parameters at the moment
	### SO these are mainly needed if you want to recreate results
	### Making the entire file a string will also make storing in the database easier
	
        from lxml import etree

	tree= etree.parse(filename)
	root = tree.getroot()
	
	optFile = etree.tostring(root)
	return [optFile]


def pullDataFromDMC(filename,runNum):

	### There is no need to search through the DMC file parameters at the moment
	### So these are mainly needed if you want to recreate results
	### Making the entire file a string will also make storing in the database easier
        from lxml import etree
	
	tree= etree.parse(filename)
	root = tree.getroot()

	dmcFile = etree.tostring(root)
	project = root[0]
	scalarDatfilename =project.set("id")
	
	return [dmcFile,scalarDatfilename]
