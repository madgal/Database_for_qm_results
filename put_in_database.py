#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
You can create or modify a run_id and add_results.

Usage:
  put_in_database.py (-h | --help)
  put_in_database.py add_results --path=<path>
                     (--method=<method_name> --basis=<basis_name>
                      --geo=<geometry_name> --comment=<comment>|
                      --run_id=<id>)
                     (--simple | --cipsi [--epp] | --qmc)
                     [--overwrite]

Example of input file for a simple run (molecule,energy):

F                             -24.1891722605
CH2_1A1                        -6.7152075579
NH                            -10.4245101299
SiH2_3B1                       -4.9754588687
CH3                            -7.4164102812

Example of input file for a CIPSI run (molecule,energy,pt2):

F                             -24.1891722605      0.0003183747
CH2_1A1                        -6.7152075579      0.0003207809
NH                            -10.4245101299      0.0003317405
SiH2_3B1                       -4.9754588687      0.0003413844
CH3                            -7.4164102812      0.0003798976

Example of input file for a QMC run (molecule,energy, error):

F                             -24.1891722605      0.0003183747
CH2_1A1                        -6.7152075579      0.0003207809
NH                            -10.4245101299      0.0003317405
SiH2_3B1                       -4.9754588687      0.0003413844
CH3                            -7.4164102812      0.0003798976


"""

version = "0.0.2"

import sys

try:
    from src.docopt import docopt
    from src.SQL_util import add_or_get_run, get_mol_id
    from src.SQL_util import add_simple_energy, add_cipsi_energy, add_qmc_energy
    from src.SQL_util import conn
    from src.misc_info import old_name_to_new
except:
    raise
    print "File in misc is corupted. Git reset may fix the issues"
    sys.exit(1)

if __name__ == '__main__':

    arguments = docopt(__doc__, version='G2 Api ' + version)

    if arguments["--run_id"]:
        run_id = arguments["--run_id"]
    else:
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

        if arguments["--simple"]:
            e = list_[1]

            print e
            add_simple_energy(run_id, id_, e,
                              overwrite=arguments["--overwrite"])

        elif arguments["--cipsi"]:
            e, pt2 = list_[1:]
            if arguments["--epp"]:
                pt2 = float(pt2) - float(e)

            print e, pt2
            add_cipsi_energy(run_id, id_, e, pt2,
                             overwrite=arguments["--overwrite"])

        elif arguments["--qmc"]:
            e, err = list_[1:]

            print e, err
            add_qmc_energy(run_id, id_, e, err,
                           overwrite=arguments["--overwrite"])

	print "Please commit db/g2.dump changes to https://github.com/madgal/qmcpack_buddy"
    conn.commit()
