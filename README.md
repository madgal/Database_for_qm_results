# qmcpack_buddy
A database for retrieving and adding results generated via quantum package.
Also generates input and submission files for quantum package and qmcpack. 
 (Please note that script generation is not finished and may not work correctly)

Output files include: 
	
	Quantum Package Calculation:
	
	QMCPACK Calculation:
		generate_Conversion.py takes the arguments ()
		
		It will convert path/*.dump to :
				path/NoJastrow_1Det/*xml	
				path/Jastrow_1Det/*xml	
				path/NoJastrow_MultiDet/*xml	
				path/Jastrow_MultiDet/*xml	
				path/Jastrow_MultiDet_reoptCoeff/*xml	

		Within each it creates a DMC folder with a DMC.xml file (obtained by modifying either the PP or AE misc/DMC_*.xml template)
		
		1Det and no Jastrow: 	the optimization folder will not be created
		1Det and Jastrow:	the optimization folder will be created with the Opt_*.xml template, optimize_1Body2Body.py, optimize_3Body.py, and optimize_finish.py

		For the multideterminant calculations, cutoff directories will be generated in the main directories
		MultiDet and no Jastrow: 	the optimization folder will not be created
		MultiDet and Jastrow: 		the optimization folder will be created with the Opt_*.xml template, optimize_1Body2Body.py, optimize_3Body.py, and optimize_finish.py
		MultiDet, Jastrow, and reopt:	the optimization folder will be created with the Opt_*.xml template, optimize_1Body2Body.py, optimize_coeffs.py, optimize_3Body.py, and optimize_finish.py


		Utilities for visualization: 
			format_data.py will be added to DMC directories
			plot_OptProg.py will be added to Optimization directories

		
		Additionally:
			unpackXML.py will go through the optimization and dmc files to pull out the necessary parameters for later runs
			recreateXML.py goes through the database and pulls the necessary information to set up a qmc calculation
				if the data does not yet exist it will set up a bare bones calculation for the user

	
	Note that if NDET is not specified then the quantum package default of 10000 is used. 

	THE OPTIONS:
		There are two options for generation, from scratch (QP through QMC) or from a file that is ready for conversion (QP finished we have a dumpfile). 

		setup_QMC_calculation takes a file ready for conversion, and a few arguments, to generate the needed files and directories.

To use, the database may need to be reinitialized. 
On Linux:
	
	sqlite3 g2.db < g2.dump	


This code is based off code available at "https://github.com/TApplencourt/G2_TestSet_CLI.git"



