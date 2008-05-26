'''
	This file is part of PAScual.
    PAScual: Positron Annihilation Spectroscopy data analysis
    Copyright (C) 2007  Carlos Pascual-Izarra <carlos.pascual-izarra@csiro.au>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''



# import sys
import copy
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import AdvOpt as advopt
from PAScual import printwarning
import cPickle as pickle


class fitter(QThread):
	'''The fitter is an object that will fit sets of spectra (one set at a time) in a different thread to that of the main program'''
	def __init__(self, parent=None):
		super(fitter, self).__init__(parent)
		self.stopped = False
		self.mutex = QMutex()  #this mutex is used to ensure that the self.stopped variable is accessed properly
		self.ps = None
		self.completed = False
		self.saveslot=self.saveslot_auto=self.saveslot_user=None
	
	def initialize(self, ps, outputfile, warningslog=[]):
		self.stopped = False
		self.ps = ps
		self.outputfile=outputfile
		self.completed = False
		self.warningslog=warningslog
		
	def stop(self):
		try:
			self.mutex.lock()
			self.stopped = True
		finally:
			self.mutex.unlock()	
	def isStopped(self):
		try:
			self.mutex.lock()
			return self.stopped #even with this 'return' here, the 'finally:' block is executed before exiting!
		finally:
			self.mutex.unlock()	
	def run(self):
 		self.launchFit(self.ps)
		self.stop()
		self.emit(SIGNAL("endrun(bool)"), self.completed)
	
	def launchFit(self,ps):
		'''This launches the fit (called via the run method). For the given palsset, it interpretes the commands and calls the appropriate functions''' 
		for ob,icmd in zip(ps.commands,range(len(ps.commands))):
			if self.isStopped(): return  #This makes possible to respond to a request of stopping the fit
			cmd=ob.cmd
			args=ob.args
			#SA command	
			if cmd=='SA':
				print '\n********* Performing Simulated Annealing **************\n'
				ps.simann(minaccratio=0.1, direct=advopt.SA_direct, stopT=advopt.SA_stopT, maxiter=advopt.SA_maxiter, tolerance=advopt.SA_tol, meltratio=advopt.SA_meltratio)
			elif cmd=='LOCAL':
				print '\n********* Performing Local search **************\n'
				if args:
					args=args.strip().upper()
					forcelimits=(args!='NOLIMITS')
				else: forcelimits=True
				temp=copy.deepcopy(ps)
				try: ps.localmin(maxunbound=advopt.LOCAL_maxunbound, ireport=True, forcelimits=forcelimits)
				except ValueError: 
					self.warningslog+=printwarning("LOCAL minimisation of %s failed. Skipping!"%ps.name)
					ps=temp #recovering original from backup
			#BI command	
			elif cmd=='BI'	:
				print '\n********* Performing Bayesian Inference **************\n'
				ps.BI(LM=advopt.BI_length, stabilisation=advopt.BI_stab, ireport=advopt.BI_report,iemit=1, savehist=advopt.BI_savehist)
			#LOAD command
			elif cmd=='LOAD':
				print '\n********* Loading previous results **************\n'
				if args: #load from file
					print "\nPrevious status loaded from '%s'\n"%args
					try: self.saveslot=pickle.load(open(args,'rb'))
					except IOError: self.saveslot=None
				else: self.saveslot=self.saveslot_user #load from saveslot_user slot
				if self.saveslot: #check if there is something to load 
					temp=copy.deepcopy(ps)
					success=ps.importvalues(self.saveslot, onlyfree=False, flexicomp=False)#import the values
					if not success: # if the import was not satisfactory, undo changes
						self.warningslog+=printwarning("Cannot LOAD. %s is not compatible with %s"%(ps.name,self.saveslot.name))
						ps=copy.deepcopy(temp)
				else: self.warningslog+=printwarning("Cannot LOAD. Nothing previously saved")
				ps.calculate_chi2()
				ps.confirm()
				ps.clearstats()
			#SAVE command	
			elif cmd=='SAVE':
				print '\n********* Saving results **************\n'
				self.saveslot_user=copy.deepcopy(ps)
				self.saveslot_user.name="Saved(%s)"%ps.name
				if args: 
					pickle.dump(self.saveslot_user,open(args,'wb'),-1) #if a filename is provided, save a copy there
					print "\nCurrent status saved in '%s'\n"%args
# 			#LOG command
# 			elif cmd=='LOG':
# 				header=False
# 				if args:
# 					if args in self.logfilesdict: logfile=self.logfilesdict[args]
# 					else:
# 						logfile=open(args,'a') #the file is opened in append mode
# 						self.logfilesdict[args]=logfile
# 						header=True
# 				else: logfile=None
# 				ps.showreport_1row(file=logfile, min_ncomp=max([ob.ncomp for ob in spectra]), header=header)
# 			#REPORT command
# 			elif cmd=='REPORT':
# 				print '\n********* Reporting **************\n'
# 				ps.showreport(verbosity=1)
# 				if args:
# 					if args.upper().strip()=='G': ps.graph_report() 
# 			#FAKE command.
# 			elif cmd=='FAKE':
# 				print '\n********* Generating fake spectra **************\n'
# 				filename=None
# 				if args:
# 					args=args.split(None,1)
# 					area=float(args[0])
# 					if len(args)==2: filename=args[1]					
# 				else: area=1e6
# 				temp=copy.deepcopy(ps)
# 				for sp in temp.spectralist:
# 					sp.exp[sp.roi]=sp.fake(area=area)
# 					sp.exparea=sp.exp[sp.roi].sum()
# 					sp.deltaexp=S.where(sp.exp<4,2.,S.sqrt(sp.exp))
# 					sp.recalculate_chi2(forcecalc=True)
# 				temp.showreport(verbosity=1) 
# 				temp.graph_report() 
# 				if filename:
# 					suffix=''
# 					for sp in temp.spectralist: 
# 						if len(temp.spectralist)>1: suffix=sp.name
# 						print "\nFake spectrum written in '%s'\n"%(filename+suffix)
# 						pylab.save(filename+suffix,sp.exp)
# 						#ADDCOMPONENT command				
# 			#ADDCOMPONENT command				
# 			elif cmd=='ADDCOMPONENT':
# 				ps=ps.addcomponent() #TODO
			#END command
			elif cmd=='END':
				pass
			#UNRECOGNISED command
			else: 
				self.warningslog+=printwarning("Command not recognised (%s). Skipping\n"%cmd)
			#after each command, autosave the last state of the palsset 
			self.saveslot_auto=copy.deepcopy(ps)
			#flush the output
			if self.outputfile: self.outputfile.flush()
			#emit a signal of command done
			self.emit(SIGNAL("command_done(int)"),icmd+1)
		self.completed = True

