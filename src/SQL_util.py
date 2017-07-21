#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

try:
    import sqlite3
    from sqlit import connect4git
except:
    print "Please make sure sqlite3 is installed"
    sys.exit(1)

#  _
# /  ._ _   _. _|_  _     _     ._ _  _  ._
# \_ | (/_ (_|  |_ (/_   (_ |_| | _> (_) |
#

dump_path = os.path.abspath(os.path.dirname(__file__) + "/../db/g2.dump")
db_path = os.path.abspath(os.path.dirname(__file__) + "/../db/g2.db")
#dump_path ="https://github.com/madgal/qmcpack_buddy/blob/master/db/g2.dump" 
#db_path ="https://github.com/madgal/qmcpack_buddy/blob/master/db/g2.db" 



try:
    conn = connect4git(dump_path, db_path)
except sqlite3.Error as e:
    print "{0} is not a SQLite3 database file".fomat(db_path)
    sys.exit(1)

c = conn.cursor()

conn.row_factory = sqlite3.Row
c_row = conn.cursor()


def cond_sql_or(table_name, l_value):
    # Create the OR condition for a WHERE filter

    l = []
    dmy = " OR ".join(['%s GLOB "%s"' % (table_name, i) for i in l_value])
    if dmy:
        l.append("(%s)" % dmy)

    return l


#  _____      _
# |  __ \    | |
# | |  \/ ___| |_
# | | __ / _ \ __|
# | |_\ \  __/ |_
#  \____/\___|\__|
#
def get_coord(id, atom, geo):
    # Only work if, id, atom, already exist
    c.execute(''' SELECT x,y,z FROM coord_tab NATURAL JOIN geo_tab
                WHERE id =?  AND
                      atom=? AND
                      name = ?''', [id, atom, geo])

    return c.fetchall()


def get_mol_id(name):
    # Only work if name already exist
    c.execute("SELECT id FROM id_tab WHERE name=?", [name])
    return c.fetchone()[0]


def get_method_id(name):
    # Only work if name already exist
    c.execute("SELECT method_id FROM method_tab WHERE name=?", [name])
    return c.fetchone()[0]


def get_basis_id(name):
    # Only work if name already exist
    c.execute("SELECT basis_id FROM basis_tab WHERE name=?", [name])
    return c.fetchone()[0]


def get_geo_id(name):
    # Only work if name already exist
    c.execute("SELECT geo_id FROM geo_tab WHERE name=?", [name])
    return c.fetchone()[0]


def get_run_id(method, basis, geo, comments):
    # Only work if method,basis,geo already exist
    method_id = get_method_id(method)
    basis_id = get_basis_id(basis)
    geo_id = get_geo_id(geo)

    c.execute("""SELECT run_id FROM run_tab
                WHERE method_id =(?) AND
                      basis_id = (?) AND
                      geo_id = (?)   AND
                      comments =(?)""", [method_id, basis_id, geo_id, comments])

    return c.fetchone()[0]


def list_geo(where_cond='(1)'):
    c.execute('''SELECT DISTINCT geo_tab.name
                            FROM coord_tab
                    NATURAL JOIN geo_tab
                      INNER JOIN id_tab
                              ON coord_tab.id = id_tab.id
                           WHERE {where_cond}'''.format(where_cond=where_cond))
    return [i[0] for i in c.fetchall()]


def list_ele(where_cond='(1)'):
    c.execute('''SELECT DISTINCT id_tab.name
                            FROM coord_tab
                    NATURAL JOIN geo_tab
                      INNER JOIN id_tab
                              ON coord_tab.id = id_tab.id
                           WHERE {where_cond}'''.format(where_cond=where_cond))
    return [i[0] for i in c.fetchall()]


# ______ _      _
# |  _  (_)    | |
# | | | |_  ___| |_
# | | | | |/ __| __|
# | |/ /| | (__| |_
# |___/ |_|\___|\__|
#
def full_dict(geo_name=None, only_neutral=True):
    d = dict_raw()

    for i, dic_ele in d.items():

        if only_neutral:
            if "+" in i or "-" in i:
                del d[i]
                continue

        # Formula = [('H', 2), ('O', 1)]
        # formula_flat = ['H', 'H', 'O']
        formula_flat = []
        a = []
        for [atom, nb] in dic_ele["formula"]:
            for l in range(0, nb):
                formula_flat.append(atom)

            if geo_name:
                list_ = get_coord(dic_ele["id"], atom, geo_name)
                if not list_:
                    del d[i]
                    break
                else:
                    a += list_

        dic_ele["formula_flat"] = formula_flat

        if geo_name:
            dic_ele["list_xyz"] = a

    return dict(d)


def dict_raw():
    c.execute(
        '''SELECT id,name,formula,charge,multiplicity,num_atoms,num_elec,symmetry FROM id_tab''')

    d = {}
    for i in c.fetchall():
        d[str(i[1])] = {"id": str(i[0]),
                        "formula": eval(i[2]),
                        "charge": int(i[3]),
                        "multiplicity": int(i[4]),
                        "num_atoms": int(i[5]),
                        "symmetry": str(i[6])}

    return d


#   ___      _     _
#  / _ \    | |   | |
# / /_\ \ __| | __| |
# |  _  |/ _` |/ _` |
# | | | | (_| | (_| |
# \_| |_/\__,_|\__,_|
#
def add_new_run(method, basis, geo, comments):
    # Only work id method,basis,geo already exist
    method_id = get_method_id(method)
    basis_id = get_basis_id(basis)
    geo_id = get_geo_id(geo)

    c.execute("""INSERT INTO run_tab(method_id,basis_id,geo_id,comments)
        VALUES (?,?,?,?)""", [method_id, basis_id, geo_id, comments])
    conn.commit()


def add_or_get_run(method, basis, geo, comments):

    try:
        return get_run_id(method, basis, geo, comments)
    except TypeError:
        add_new_run(method, basis, geo, comments)
    finally:
        return get_run_id(method, basis, geo, comments)


def add_simple_energy(run_id, id_, e, overwrite=False, commit=False):

    if overwrite:
        cmd = """INSERT OR REPLACE INTO simple_energy_tab(run_id,id,energy)
                  VALUES (?,?,?)"""
    else:
        cmd = """INSERT INTO simple_energy_tab(run_id,id,energy)
                  VALUES (?,?,?)"""

    c.execute(cmd, [run_id, id_, e])

    if commit:
        conn.commit()


def add_cipsi_energy(run_id, id_, e, pt2, overwrite=False, commit=False):

    if overwrite:
        cmd = """INSERT OR REPLACE INTO cipsi_energy_tab(run_id,id,energy,pt2)
                  VALUES (?,?,?,?)"""
    else:
        cmd = """INSERT INTO cipsi_energy_tab(run_id,id,energy,pt2)
                  VALUES (?,?,?,?)"""

    c.execute(cmd, [run_id, id_, e, pt2])

    if commit:
        conn.commit()


def add_qmc_energy(run_id, id_, e, err, overwrite=False, commit=False):

    if overwrite:
        cmd = """INSERT OR REPLACE INTO qmc_energy_tab(run_id,id,energy,err)
                  VALUES (?,?,?,?)"""
    else:
        cmd = """INSERT INTO qmc_energy_tab(run_id,id,energy,err)
                  VALUES (?,?,?,?)"""

    #c.execute(cmd, [run_id, id_, e, err])

    if commit:
        conn.commit()


def add_energy_cispi_output(url, run_id, name,
                            true_pt2=False, debug=False):
    # Add a cipsi energy containt in a log file to the run_id

    # Try if the file is existing
    if not os.path.isfile(url):
        raise Exception("%s not existing" % url)
    else:
        with open(url, "r") as f:
            s = f.read()

    # If true_pt2 check if Final step is in the data
    if true_pt2 and s.find("Final step") == -1:
        raise Exception("%s have not a true PT2" % url)
    else:
        s = s[s.rfind(' N_det'):]

    # Now get the data
    s = s.splitlines()

    e = ndet = pt2 = time = None

    for i in s:
        if "N_det " in i:
            ndet = i.split("=")[-1].strip()
        if " PT2      =" in i:
            pt2 = i.split("=")[-1].strip()
        if "E   " in i:
            e = i.split("=")[-1].strip()
        if "Wall" in i:
            time = i.split(":")[-1].strip()

    # If a data is missing continue
    if not all([ndet, e, time]):
        raise Exception("%s file is buggy" % url)

    id_ = get_mol_id(name)

    print name, run_id, id_, ndet, pt2, e, time

    if not debug:
        try:
            c.execute('''INSERT OR REPLACE INTO
                        cipsi_energy_tab(run_id,id,ndet,energy,pt2,time)
                        VALUES (?,?,?,?,?,?)''', [run_id, id_, ndet, e, pt2, time])

            conn.commit()
        except:
            raise Exception('Cannot add to the db')


def add_energies_cispi(run_list, geo_list, basis_list, path, tail,
                       true_pt2=False, compatibility=False, debug=False):
    # Add a list of cipsi log to the run_id (check for all name)

    from .misc_info import new_name_to_old

    index = 0
    for geo in geo_list:

        dict_ = full_dict(geo)

        for basis in basis_list:
            for name, dic in dict_.iteritems():

                if compatibility and name in new_name_to_old:
                    name_path = new_name_to_old[name]
                else:
                    name_path = name

                url = "".join([path, name_path, "_", basis, "_", geo, tail])

                run_id = run_list[index]
                try:
                    add_energy_cispi_output(url, run_id, name, true_pt2, debug)
                except:
                    pass

            index += 1

def add_qmc_input_metadata(wfsInfo,filesForInput,additionalInfo,debug=False):
    # Add input files to database so that others can verify/recreate results
    print "Add qmc info"
    
    # input the files for recreation
    [optFile,dmcFile,wfsFile,ptclFile] = filesForInput

    ## input the metadata for other scientists benefits
    [cuspCorrection,multidet,ndet,reoptCoeff,cutoff,j2list,j1list,j3list]= wfsInfo
    [wfs_method,basis,geometry,comments] = additionalInfo

    run_id = 10
    id_ =  10

    print run_id, id_

    if not debug:
        try:
            c.execute('''INSERT OR REPLACE INTO
                        qmc_input_tab(id,name,optfile,dmcfile,wfsfile,ptclfile,cuspCorrection,multideterminant,Ndet,reoptCoeff,coeffCutoff,J2,J1,J3,wfs_method,basis,geometry,comments)
                        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', [run_id, id_,optFile,dmcFile,wfsFile,ptclFile,cuspCorrection,multidet,ndet,reoptCoeff,cutoff,j2list,j1list,j3list,wfs_method,basis,geometry,comments])

            c.execute('''INSERT OR REPLACE INTO
                        qmc_input_tab( id, name , optfile, dmcfile, wfsfile, ptclfile, cuspCorrection, multideterminant, J2, J1, J3, Ndet, reoptCoeff, coeffCutoff, wfs_method, basis, geometry,comments)
                        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', [run_id, id_,optFile,dmcFile,wfsFile,ptclFile,cuspCorrection,multidet,j2list,j1list,j3list,ndet,reoptCoeff,cutoff,wfs_method,basis,geometry,comments])



            conn.commit()
        except Exception as err:
            #raise Exception('Cannot add to the db')
            print err

# ______                         _
# |  ___|                       | |
# | |_ ___  _ __ _ __ ___   __ _| |_
# |  _/ _ \| '__| '_ ` _ \ / _` | __|
# | || (_) | |  | | | | | | (_| | |_
# \_| \___/|_|  |_| |_| |_|\__,_|\__|
#
def get_xyz(geo, ele, only_neutral=True):
    b = full_dict(geo, only_neutral)

    dic_ = b[ele]

    xyz_file_format = [dic_["num_atoms"]]

    line = " ".join(map(str, [ele,
                              "Geo:", geo,
                              "Mult:", dic_["multiplicity"],
                              "symmetry:", dic_["symmetry"]]))
    xyz_file_format.append(line)

    for atom, xyz in zip(dic_["formula_flat"], dic_["list_xyz"]):
        line_xyz = "    ".join(map(str, xyz))
        line = "    ".join([atom, line_xyz])

        xyz_file_format.append(line)

    return "\n".join(map(str, xyz_file_format))


def get_g09(geo, ele, only_neutral=True):
    b = full_dict(geo, only_neutral)

    dic_ = b[ele]

    line = " ".join(map(str, [ele,
                              "Geo:", geo,
                              "Mult:", dic_["multiplicity"],
                              "symmetry:", dic_["symmetry"]]))

    method = "RHF" if dic_["multiplicity"] == 1 else "ROHF"

    g09_file_format = ["# cc-pvdz %s" % (method), "", line, "",
                       "%d %d" % (dic_["charge"], dic_["multiplicity"])]

    for atom, xyz in zip(dic_["formula_flat"], dic_["list_xyz"]):
        line_xyz = "    ".join(map(str, xyz)).replace("e", ".e")
        line = "    ".join([atom, line_xyz])

        g09_file_format.append(line)
    g09_file_format.append("\n\n\n")
    return "\n".join(map(str, g09_file_format))
