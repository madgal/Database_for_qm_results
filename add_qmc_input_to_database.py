#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
You can add_input

Usage:
  add_qmc_input_to_database.py (-h | --help)
  add_qmc_input_to_database.py add_input --path=<path>
                     (--method=<method_name> --basis=<basis_name>
                      --geo=<geometry_name> --comment=<comment>|
                      --run_id=<id>)


"""

version = "0.0.2"

import sys

try:
    from src.docopt import docopt
    from src.SQL_util import add_or_get_run, get_mol_id
    from src.SQL_util import add_qmc_input_metadata
    from src.SQL_util import conn
    from src.misc_info import old_name_to_new
except:
    raise
    print "File in misc is corupted. Git reset may fix the issues"
    sys.exit(1)

if __name__ == '__main__':

    arguments = docopt(__doc__, version='G2 Api ' + version)

    l = [arguments[i] for i in ["--method",
                                "--basis",
                                "--geo",
                                "--comment"]]
    run_id = add_or_get_run(*l)

    print run_id,

    with open(arguments["--path"], "r") as f:
        data = [line for line in f.read().split("\n") if line]

    for line in data:

        list_ = line.split("#")[0].split()

        try:
            list_[0]
        except IndexError:
            continue

        name = list_[0]
        name = old_name_to_new[name] if name in old_name_to_new else name
        id_ = get_mol_id(name)
        print name, id_,

	############################################################
	############################################################
	############################################################
	############################################################
	############################################################
	############################################################

	''' Need :

		N_det = (integer)
		Jastrow = (true | false)
		CuspCorrection = (true | false)
		Version = (version number)
		Optimization_Block =???
		DMC_block = ???
		basis
		geometry
		comments
		citation
		seed
		element
		initial_WF_generation_method
		
	
		'''
	

        add_qmc_input_metadata()
                       

	print "Please commit db/g2.dump changes to https://github.com/madgal/qmcpack_buddy"
    conn.commit()
