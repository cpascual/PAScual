### Input parameters for PAScual.
### by Carlos Pascual-Izarra < cpascual [AT] users.sourceforge.net >  2007
### '''
### 	This file is part of PAScual.
###     PAScual: Positron Annihilation Spectroscopy data analysis
###     Copyright (C) 2007  Carlos Pascual-Izarra < cpascual [AT] users.sourceforge.net >
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


#########DO NOT TOUCH THIS BLOCK ##############################
from glob import glob as matchfilenames
from scipy import inf, array, arange, log, exp, concatenate, savetxt

############# END OF "DO-NOT-TOUCH" BLOCK #####################


######### In principle, this is the only file you need to touch for a regular calculation
######### You can modify the parameters below this line

######### IMPORTANT NOTES ON SYNTAX FOR THIS FILE:
# # 1- Regular Python syntax format applies. The hash "#" character is a comment. You can call Python functions and operators if you want.
# # 2- Parameters marked with (*1) can optionally be given as a list (for multiple spectra fit). 
# #    If a non-list value is provided it will be used for all the spectra.
# # 3- Parameters marked with (*2) are direct descriptions of fitting parameters. They can be one of the following values:
# #    a) a string being the name of a named parameter, with an optional "*" for making common parameters (see the named parameter section below)
# #    b) a single numerical value. This means that the parameter is FIXED (non-free).
# #    c) a tuple containing (value,minimum,maximum). This means it is a free parameter.
# # 4- Parameters marked with (*3) accept the same syntax as those with (*1) except in that they are extended over the number of 
# #    palssets (instead of the number of spectra). Note that the palssets are automatically created by optimally distributing the 
# #    given spectra. Therefore, the usage of lists for these parameters is only for very advanced users who know what they are doing

##=================================================================================================================================================
######Experimental data 
#### Indicate which experimental data is going to be analysed.  You can make use of a path variable. 
#### You can also use the matchfilenames() function in order to use wildcards: *, ?, [-],....
# expfilenames=['data/KansyA.dat'] 	#(*1) list of names (optionally with a path) for the experimental file(s) 
# expfilenames=['data/KansyA.dat','data/KansyB.dat','data/KansyC.dat','data/KansyD.dat']
# path="C:\Documents and Settings\pas064\My Documents\PALS\Aurelia\Al holder\PHYT_T20/selectedsums/"
# path="C:\Documents and Settings\pas064\My Documents\PALS\Aurelia\Al holder\PHYT_T20/"
path = './examples/'

# expfilenames=[]
# expfilenames=matchfilenames(path+'Pure*/??_???*sum.al2')
# expfilenames+=matchfilenames(path+'3%*/??_???*sum.al2')
# expfilenames+=(matchfilenames(path+'5%*/??_???*sum.al2')+matchfilenames(path+'5%*/05B_???.al2'))
# expfilenames+=matchfilenames(path+'8%*/08_???.al2')
# expfilenames+=matchfilenames(path+'11%*/??_???*sum.al2')
# expfilenames+=matchfilenames(path+'13/??_???.al2')
# expfilenames+=matchfilenames(path+'15/??_???*sum.al2')
# expfilenames+=matchfilenames(path+'17/??_???.al2')
# expfilenames+=matchfilenames(path+'19/??_???.al2')
# expfilenames+=matchfilenames(path+'22/??_???.al2')
# expfilenames+=matchfilenames(path+'25/??_???.al2')
# expfilenames+=matchfilenames(path+'26/??_???.al2')[:10]
# expfilenames+=matchfilenames(path+'27/??_???.al2')
# expfilenames+=matchfilenames(path+'28/??_???.al2')[:10]


expfilenames = matchfilenames(path + '*.dat')

# expfilenames+=matchfilenames(path+'CPI_A_*.dat')
# expfilenames=5*[None]

# skipfilenames=(matchfilenames(path+'28_1??.al2')) # list of file names names to ignore (useful if matchfilenames() returned some unwanted file names)
headerlines = 4  # (*1) Number of rows to skip when reading the exp file (to skip the header). Put to 0 if no header.

####### Calibration.
psperchannel = 50  # (*1) Channel width in picoseconds.

######ROI definition.
#### Any roi can be given. Just do an array (or list) containing channel numbers in the ROI. 
#### Examples:
# roi=arange(213,879)  				#roi between channels 10 and 800
# roi=range(10,200)+range(400,500)  #roi defined in by two subranges 							# (*1) The whole spectrum
#### OR, ALTERNATIVELY, instead of directly defining the roi, you can define the left_of_max and stopdat variables as in MELT. 
left_of_max = 5  # (*1) Start this much at the left of the channel with the max number of counts.
stopdat = 689  # (*1) Channel where the data stops.

####### Named parameters
#### For convenience, it is possible to assign a name to a parameter. 
#### This is done in a "dictionary": {'parname1':(val1,min1,max1), 'parname2':(val2,min2,max2),...}
#### The parameters defined here can be later referred to by their name.
#### When **referring** to the parameter, if just its name is used, a unique COPY of that parameter will be used and
#### therefore that parameter will be independent (as opposed to "common")
#### On the other hand, if a "*" is appended to the name when referring to it, a copy is NOT made (allowing to have common parameters)

namedparameters = {
    'fwhm': (270, 100, 500),
    'c0': (30, 10, 100),
    'bg': (20, 1, 1000),
    'tau_pPs': (125, 50, 250), 'tau_drt': (400, 250, 600),
    'tau_oPs': (3000, 600, 142e3),
    'tau1': (125, 50, 350), 'tau2': (400, 150, 600), 'tau3': (1900, 500, 142e3),
    'tau': (300, psperchannel, 142e3), 'tauKansy': (300, psperchannel, 142e3),
    'ity': (1, 0, None), 'ityKansy': (1, 0, None),
    'tau4': (1300, 800, 5000), 'at1': (1500, 1000, 4000), 'at2': 1.7,
    'tausrc': 1630, 'itysrc': .066, 'tauH2O': (1800, 1600, 2000),
    'tauPHYT': (2800, 2000, 3500)}

######Background.
####Note: unless you fix the background, it doesn't really matter to give a precise value.
# bg=(100,0,1e4)			# (*1)(*2) 
#### ALTERNATIVELY: If the baseline is present in a region of your spectrum, you can just give its starting and end channels
####                In this case, it is assumed to be free non-common parameter(s)  and the min and max will be automatically calculated
startbg = 660  # (*1) first bin for background initialisation
stopbg = 680  # (*1) last bin for background initialisation
# bg=(20,1,200)
# bg=25*5
# bg=[5e-5*1e6*float(a) for a in areaList ]
# print bg
# raw_input()

###### FWHM. 
#### Resolution function Full Width Half Maximum in ps (assuming Gaussian shape)
# fwhm=(300,200,400)  # (*1)(*2) FWHM
# fwhm="fwhm"
fwhm = (280, None, None)
# fwhm=270

###### Offset. 
#### Channel for time 0. 
# c0=(100,10,500)  # (*1)(*2)  Calibration offset. If omitted, it will be assumed to be a free non-common parameter and (val,min,max) will be automatically calculated
# c0=[20,"c0","c0",20]
# c0=100


####### Lifetimes
#### Define the lifetimes as a TUPLE of fitpar descriptors, i.e., as (t1,t2,t3,...),  where ti is one of the cases described by (*2)
#### note that a "list of tuples of descriptors" is also possible just following (*1)
tau = ((100, 50, 200), (400, 200, 500), (
1000, 500, 1.42e5))  # (*1)(*2) lifetimes in ps.  Note, min>0 and max<1.42e5ps
# tau=[("tau1","tau2","tau3",1000), ("tau1","tau2","tau3",1050)]+2*[(234,"Ctau2")]
# tau=[("tau1","tau2","tau3","tau4")]+2*[(234,"Ctau2")]
# tau=('tau1*','tau2*','tau3*',(1140,50,150000))
# tau=[((100,psperchannel,142e3),(300,psperchannel,142e3),(500,psperchannel,142e3),(5000,psperchannel,142e3))]+3*[('tau','tau')]
# tau=[((100,psperchannel,142e3),(300,psperchannel,142e3),(500,psperchannel,142e3),(5000,psperchannel,142e3))]
# tau=[('tau','tau','tau','tau')]+3*[('tauKansy*','tau')]
# tau=[((100,50,180),(180,170,300))]
# tau=[('tau','tau')]
# tau=[('tau','tau','tau','tau')]
# tau=(125,"tau_drt","tau_oPs","tauPHYT")
# tau=(125,"tau_drt","tau_oPs",1905,418)
# tau=(125, (400,1,142e3), 1800, (3000,1,142e3))
# ity=('ity','ity',.05,'ity')
# tau=[(125, 'tau_drt', 'tauH2O', t) for t in tarray]
# ity=(.15,  .20 , .05,   .60)
# ity=(.20,.60,.20)
# ity=(.25,.25,.25,.25)
# tau=(125,'tau','tau')


####### Intensities
#### You can define the lifetimes as a tuple, including common parameters
# ity=None		# (*1)(*2) Same syntax as for tau. (if omitted, it will be initialised as val=1,min=0,max=inf)
# ity=[('ity','ity','ity','ity')]+3*[('ityKansy*','ity*')]
# ity=('ity','ity','ity','ity',)
# ity=('ity','ity','ity',0.035,0.155)
##=================================================================================================================================================

####### Fitology:
#### These parameters control the way the fitting is done. 
#### Three tools are implemented for fitting: Simulated annealing (SA), Bayesian Inference (BI) and Local Search (LOCAL). 
#### Read the documentation to find out about each of them.
#### Rougthly speaking: SA is good to find the global minimum but it is slow (use it as an initialisation tool).
####					BI should be run after the global minimum is found in order to calculate the errors. Use it after SA
####					LOCAL is not robust but it is fast once you are near the minimum. Use it after SA. 

fitmode = ('LOCAL', 'LOG ' + path + 'results.txt')
# fitmode=('LOAD','SA','LOCAL','BI','SAVE')
# fitmode=('LOAD','BI','REPORT','SAVE')
# fitmode=[('SA','SAVE kk0_SA','BI','SAVE kk0_BI','LOCAL','SAVE kk0_LOCAL'),('SA','SAVE kk1_SA','BI','SAVE kk1_BI','LOCAL','SAVE kk1_LOCAL'),('SA','SAVE kk2_SA','BI','SAVE kk2_BI','LOCAL','SAVE kk2_LOCAL'),('SA','SAVE kk3_SA','BI','SAVE kk3_BI','LOCAL','SAVE kk3_LOCAL')]
# fitmode=[('LOAD kk0_SA','REPORT','LOAD kk0_BI','REPORT'),('LOAD kk1_SA','REPORT','LOAD kk1_BI','REPORT'),('LOAD kk2_SA','REPORT','LOAD kk2_BI','REPORT'),('LOAD kk3_SA','REPORT','LOAD kk3_BI','REPORT')]
# fitmode=('LOAD','LOCAL','SAVE','LOG '+path+'dp-allfree.dat')
# fitmode=('SA','LOG '+path+'kk.dat')					
# fitmode=[('SA','SAVE','LOCAL','LOG '+path+'kk.dat',)]+[('LOAD','LOCAL','LOG '+path+'kk.dat',)]*(len(expfilenames)-1)
# fitmode=('LOAD','LOCAL','SAVE','LOG '+path+'results.txt')					
# fitmode=[('LOCAL','LOG '+path+'results.txt','SAVE %s_SA.sav'%fn) for fn in expfilenames]	
# fitmode=('SA','LOG '+path+'results.txt')					
# fitmode=[('FAKE 2e7 %sCPI_A_%03i.dat'%(path,i+1),'LOG %sCPI_A_perfect.txt'%path) for i in range(len(expfilenames))]
# fitmode=[('FAKE 2e6 %sCPI_D_%03i.dat'%(path,i+1),'LOG %sCPI_D_perfect.txt'%path) for i in range(len(expfilenames))]
# fitmode=[('FAKE 5e5 %sCPI_G_%03i.dat'%(path,i),'LOG %sCPI_G_perfect.txt'%path) for i in T]
# fitmode=[('FAKE 5e5 %sCPI_G_%03i_%03i.dat'%(path,T[i],i%nrepeats),'LOG %sCPI_G_perfect.txt'%path) for i in xrange(T.size)]
# fitmode=[('FAKE 25e5 %sCPI_J_%02i_%03i.dat'%(path,int(ity4[i]*100),i%nrepeats),'LOG %sCPI_J_perfect.txt'%path) for i in xrange(ity4.size)]
# fitmode=[('FAKE %f %sCPI_F_%s.dat'%(float(A)*1e6,path,A),'LOG %sCPI_F_perfect.txt'%path) for A in areaList]
# fitmode=('LOAD','LOCAL NOLIMITS','SAVE','LOG '+path+'CPI_A_results.txt')
# fitmode=('LOCAL NOLIMITS','LOG '+path+'CPI_A_results.txt')
# fitmode=('LOCAL','LOG kk')	

######Output 
###Output data file. See following examples:
# outputfile=path+'output.txt' #a name
outputfile = None  # no output file creation
# outputfile=expfilename.rsplit('.',1)[0]+'.out' #same as the experimental but with .out extension
# outputfile=expfilename.rsplit('.',1)[0]+'20.out'
BI_report = 500  # A report will be shown every this steps during BI (put to -1 for no reports). Be Careful: too much reports may slow down the calc.

####Advanced fitting parameters
#### IMPORTANT:
#### The following parameters are not supposed to be changed by regular users. They deal with internal algorithmical choices.
#### The default values are generally correct. Don't mess with them if you don't know exactly what you are doing
SA_tol = 1e-5  # (*3)Tolerance for stopping the SA
SA_stopT = .1  # (*3)Stop temperature for SA (put to 0 to disable). (SA_stopT>1 is not recommended)
SA_maxiter = inf  # (*3)Max number of iterations in the SimAnn fit
SA_direct = True  # (*3)Whether to use the direct mode in NNRLA for SA. Note: If SA_NNRLA=False (or <=0), SA_direct is ignored.
SA_meltratio = 0.97  # (*3)The "melting" phase of the SA will stop when this acceptance ratio is reached

LOCAL_tol = 0  # (NOT USED) (*3)Local search tolerance (the lower, the more time it will take). Put this to 0 to skip Local search and ~1e-5 for calculating
LOCAL_maxiter = 1e5  # (NOT USED) (*3)Max number of iterations in the LOCAL fit.

BI_stab = 5000  # (*3)This much steps (multiplied by the order of the searching space!) of BI will be done and not considered for statistical purposes. Put this to 0 to skip stabilisation.
BI_length = 50000  # (*3)This much steps (multiplied by the order of the searching space) will be calculated by BI.
seed = 1345  # Seed for pseudorandom generator

if __name__ == '__main__':
    from PAScual import *

    try:
        import pylab
    except:
        print >> sys.stderr, "Pylab could not be imported. Graphical output won't be supported"
    safemain()
