### Advanced fitting parameters for PAScual.
### by Carlos Pascual-Izarra <carlos.pascual-izarra@csiro.au>  2007
### '''
### 	This file is part of PAScual.
###     PAScual: Positron Annihilation Spectroscopy data analysis
###     Copyright (C) 2007  Carlos Pascual-Izarra <carlos.pascual-izarra@csiro.au>
###
###     This program is free software: you can redistribute it and/or modify
###     it under the terms of the GNU General Public License as published by
###     the Free Software Foundation, either version 3 of the License, or
###     (at your option) any later version.
###
###     This program is distributed in the hope that it will be useful,
###     but WITHOUT ANY WARRANTY; without even the implied warranty of
###     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
###     GNU General Public License for more details.
###
###     You should have received a copy of the GNU General Public License
###     along with this program.  If not, see <http://www.gnu.org/licenses/>.
### '''

from scipy import inf

#### IMPORTANT:
#### The following parameters are not supposed to be changed by regular users. They deal with internal algorithmical choices.
#### The default values are generally correct. Don't mess with them if you don't know exactly what you are doing

SA_tol=1e-5			#(*3)Tolerance for stopping the SA
SA_stopT=.1 		#(*3)Stop temperature for SA (put to 0 to disable). (SA_stopT>1 is not recommended)
SA_maxiter=inf		#(*3)Max number of iterations in the SimAnn fit
SA_direct=True 		#(*3)Whether to use the direct mode in NNRLA for SA. Note: If SA_NNRLA=False (or <=0), SA_direct is ignored.
SA_meltratio=0.97	#(*3)The "melting" phase of the SA will stop when this acceptance ratio is reached

LOCAL_tol=0			#(NOT USED) (*3)Local search tolerance (the lower, the more time it will take). Put this to 0 to skip Local search and ~1e-5 for calculating
LOCAL_maxiter=1e5	#(NOT USED) (*3)Max number of iterations in the LOCAL fit. 
LOCAL_maxunbound=10 # Max number of unbound LMA runs between L-BFGS-B optimisations (this only takes place if first LMA is outside bounds)

BI_stab=5000		#(*3)This much steps (multiplied by the order of the searching space!) of BI will be done and not considered for statistical purposes. Put this to 0 to skip stabilisation.
BI_length=50000	#(*3)This much steps (multiplied by the order of the searching space) will be calculated by BI.
BI_savehist=False 	#This controls wheter the fitpar history should be saved (=FileName) or not (=False). 
					#Caution!: this will increase the RAM requeriments. Approximately by 11Bytes*BI_length*(3+2*NC)^2 , where NC is the number of components!
# BI_savehist='PAShist.txt'


seed=1345 		#Seed for pseudorandom generator 

##
BI_report=500		#A report will be shown every this steps during BI (put to -1 for no reports). Be Careful: too much reports may slow down the calc.
