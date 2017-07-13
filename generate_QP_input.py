def  fromScratch(geometry,element,basis,NDET,otherArguments,write_path,mainDirectory,submit_path):
        from src.SQL_util import cond_sql_or, list_geo, list_ele, dict_raw
        from src.SQL_util import get_xyz, get_g09
	### Now grab/create the xyz file from the database
        from collections import namedtuple
	import os
 
        get_general = namedtuple('get_general', ['get','ext'])
        g = get_general(get=get_xyz,ext='.xyz')

        to_print=[]
        try:
            xyz = g.get(geometry,element)
        except KeyError:
    	    print "Error: Please generate an xyz file and update the database"
            pass
        else:
            to_print.append(xyz)
        if len(to_print)>1:
       	    print "Warning: There are multiple xyz files being generated"

        str_ = "\n\n".join(to_print)
        
        if write_path:
          path = write_path
    	  path = path +"/"+mainDirectory
    	  if not os.path.exists(path):
     	     os.mkdir(path)
          inputFile= "_".join([element, geometry])
    	  inputFile=inputFile+ g.ext
          filepath = path +"/"+ inputFile
        else:
    	  path="/tmp/"+mainDirectory
      	  if not os.path.exists(path):
    	     os.mkdir(path)
          inputFile= "_".join([element, geometry])
    	  inputFile=inputFile+ g.ext
          filepath = path + inputFile
        with open(filepath, 'w') as f:
             f.write(str_ + "\n")
        print "Files will be placed in  %s" %path

        if submit_path:
    	    sub_path = submit_path + "/" + mainDirectory
        else:
            sub_path=path

        ### Now obtain the multiplicity from the database 
        try:
            m = dict_raw()[element]["multiplicity"]
        except KeyError:
            pass
        else:
            print m

        rootname = str(element)+"_"+geometry+"_"+str(basis)
        rootname = rootname.replace(" ","")

	param_args = [inputFile,basis,m,otherArguments]
        __generate_ezfio__(path,rootname,param_args)
        __do_a2m_trans__(path,rootname,NDET)
        __do_fci_calc__(path,rootname,NDET)
        __save4qmc__(path,rootname,NDET)


	return [path,sub_path]

def __generate_ezfio__(path,rootname,param_args):
        [inputFile,basis,m,otherArguments]= param_args
        SCF_out_filename = rootname + ".SCF.out"
        ezfio_filename = rootname + ".ezfio"
	fileName= "setup_and_run_qp"
	dictionary = {"inputFile":inputFile,"basis":basis,"multiplicity":str(m),"otherArguments":otherArguments,"ezfio_filename":ezfio_filename,"SCF_out_filename":SCF_out_filename}

	fileTemplate = "misc/" +fileName + ".py"
	newFile=[]
	with open(fileTemplate,"r") as fileIn:
		for line in fileIn:
			for key in dictionary:
				if key in line:
					line = line.replace(key,dictionary[key])

			newFile.append(line)

        newFilename = path + "/"+fileName +"_"+rootname+".py"
	with open(newFilename,"w") as fileOut:
		for line in newFile:
			fileOut.write("%s" %line)

def  __do_a2m_trans__(path,rootname,N_det):

        ezfio_filename = rootname + ".ezfio"
        scf_dumpname = rootname + "_1.dump"
	A2M_out_filename =rootname + ".ao2mo.out"
	dictionary = {"ezfio_filename":ezfio_filename,"scf_dumpname":scf_dumpname,"A2M_out_filename":A2M_out_filename,"NDET":N_det}
	fileName = "a2m_trans"

	fileTemplate = "misc/" +fileName + ".py"
        newFile=[]
        with open(fileTemplate,"r") as fileIn:
                for line in fileIn:
                        for key in dictionary:
                                if key in line:
                                        line = line.replace(key,dictionary[key])

	                newFile.append(line)

        newFilename = path + "/"+fileName +"_"+rootname+".py"
        with open(newFilename,"w") as fileOut:
                for line in newFile:
                        fileOut.write("%s" %line)

def __do_fci_calc__(path,rootname,NDET):

        ezfio_filename = rootname + ".ezfio"
        FCI_out_filename = rootname +"_"+str(NDET)+ ".FCI.out"
	dictionary = {"ezfio_filename":ezfio_filename,"FCI_out_filename":FCI_out_filename}
	fileName = "run_fci"

	fileTemplate = "misc/" +fileName + ".py"
        newFile=[]
        with open(fileTemplate,"r") as fileIn:
                for line in fileIn:
                        for key in dictionary:
                                if key in line:
                                        line = line.replace(key,dictionary[key])

       		        newFile.append(line)

        newFilename = path + "/"+fileName +"_"+rootname+".py"
        with open(newFilename,"w") as fileOut:
                for line in newFile:
                        fileOut.write("%s" %line)
def __save4qmc__(path,rootname,NDET):

        ezfio_filename = rootname + ".ezfio"
        fci_dumpname = rootname +"_"+str(NDET)+ ".dump"

	dictionary = {"ezfio_filename":ezfio_filename,"fci_dumpname":fci_dumpname}
	fileName = "save_fci_4_qmc"

	fileTemplate = "misc/" +fileName + ".py"
        newFile=[]
        with open(fileTemplate,"r") as fileIn:
                for line in fileIn:
                        for key in dictionary:
                                if key in line:
                                        line = line.replace(key,dictionary[key])

	                newFile.append(line)

        newFilename = path + "/"+fileName +"_"+rootname+".py"
        with open(newFilename,"w") as fileOut:
                for line in newFile:
                        fileOut.write("%s" %line)
