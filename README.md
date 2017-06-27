# qmcpack_buddy
A database for retrieving and adding results generated via quantum package.
Also generates input and submission files for quantum package and qmcpack. 

Output files include: 
	
	Quantum Package Calculation:
	qp_submission1_Element_Geometry_Basis_NDET.py <- The file containing the actual code
	qp_submission1_Element_Geometry_Basis_NDET.sh <- The submission files
	
	QMCPACK Calculation:
	Element_Geometry_Basis.ham.xml <- hamiltonian for qmc 
	Note that the wfs and ptcl xml files will be created during the run (i.e. in the qp_submission1*.sh submission)
	Element_Geometry_Basis_NDET_NoJastrow.opt.xml <- Optimization file for multideterminant without Jastrow
	Element_Geometry_Basis_NDET_Jastrow.opt.xml   <- Optimization file for multideterminant with Jastrow
	Element_Geometry_Basis_NDET_ReOptJastrow.opt.xml   <- Optimization file for multideterminant with reoptimized Jastrow
	Element_Geometry_Basis_1Det_NoJastrow.opt.xml   <- Optimization file for single determinant without Jastrow
	Element_Geometry_Basis_1Det_Jastrow.opt.xml   <- Optimization file for single determinant with Jastrow
	
	The same *.dmc.xml or *.vmc.xml files will be generated depending on whether the dmc or vmc arguments were used. 
	Note that if NDET is not specified then the quantum package default of 10000 is used. 

To use, the database may need to be reinitialized. 
On Linux:
	
	sqlite3 g2.db < g2.dump	


This code is based off code available at "https://github.com/TApplencourt/G2_TestSet_CLI.git"



