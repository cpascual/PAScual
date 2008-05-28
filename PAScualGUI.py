'''
	PAScualGUI: Graphical User Interface for PAScual
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

#TODO: (General) implement load/save of discretepals and of palssets
#TODO: (General) save queue to file before starting and delete file when finished. Check for existence of old files indicating unfinished calcs and offer resume.
#TODO: (General) implement summary view of sets. A list containing which sets with which spectra each, which fitmode and nuber of free parameters and names of common parameters
#TODO: (General) (UPDATE: after v9.9 this seems no longer an issue) . Make more robust localmin (this is to PAScual.py) possibly use pre-fit with leastsq and poor convergence criterion, if that fails, go to pre-fit with bruteforce.
#TODO: (General) make more robust SA (this is to PAScual.py) possibly using resets to best fits
#TODO: (General) implement plot from columns in results table 
#TODO: (General) If a single spectrum is selected and a fit is already done, plot the fit and each component
#TODO: (General) Allow set parameters from a row of results table
#TODO: (General) If ROI is not set, issue a warning saying that the whole spectrum is going to be used
#TODO: (General) offset should be calculated automatically if not set (possible warning). 
#TODO: (General) same for background (e.g. use last 1% of ROI). Call if ROI is set AND the background is not already assigned)
#TODO: (General) Implement passing default values to left and right lims in ROISelector. Pass [-5rel,end] for ROI and [ROIright-max(5,0.01*(ROIright-ROIleft)), ROIright] for bgROI
#TODO: (General) add an animation in thestatus bar indicating "fit in progress" (possibly the pPs.gif)
#TODO: (General) add estimated time for fit (or at least for BI command)
#TODO: (General) Incorporate plothistory.py to the GUI. It could also be used to display ellipses taken from the covariance matrix when no history has been stored
#TODO: (General) make installer?


import sys, os, copy, platform
import cPickle as pickle
import scipy as S
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import ui_PAScualGUI, ui_FitparWidget
from PlotGraphWidget import PALSplot, ResPlot
from ROISelectorDlg import ROISelectorDialog
import ComponentTableMV as CTMV
import SpectraTableMV as STMV
import CommandsTableMV as CMDTMV
import CHNfiles
import PASCommandProcess as PCP
# import AdvOpt as advopt

__version__="1.0.0"
__homepage__="http://pascual.sourceforge.net"
__citation__="C. Pascual-Izarra et al., <i>Characterisation of Amphiphile Self-Assembly Materials using Positron Annihilation Lifetime Spectroscopy (PALS)-Part1: Advanced Fitting Algorithms for Data Analysis</i>, Journal of Physical Chemistry B,  [in review], 2008. <p>see %s for up-to-date information about citing</p>"%__homepage__



defaultFitModesDict={'LOCAL-connected':		('LOAD','LOCAL','SAVE'),
					'LOCAL':		('LOCAL',),
					'SA':			('SA',),
					'BI':			('BI',),
					'SA+BI':		('SA','BI',),
					'SA+LOCAL':		('SA','LOCAL',),
					'LOCAL+BI':		('LOCAL','BI',),
					'SA+LOCAL+BI':	('SA','LOCAL','BI',),
					'<user>':		('END',),
					'*NOFIT*':		('END',),
					}
defaultFitMode='LOCAL-connected'

class FitparWidget(QWidget, ui_FitparWidget.Ui_FitparWidget):
	'''A composite widget that defines fitpars. 
		It contains: a label, an "auto" button, a "value" edit box, "fixed" and "common" check boxes, minimum and maximum edits and an Apply button
		'''
	def __init__(self, fpkey, parent=None, label="", callbackApply=None, callbackAuto=None):
		'''The parameters for initialisation are:
		the fpkey is the key for the __dict__ of the spectrum that will contain this fitpar: e.g. spectrum.__dict__[fpkey]=...
		the label to be shown
		The callback for the apply button (the button is disabled if this is None) 
		The callback for the auto button (the button is disabled if this is None)
		Note, the widget is not laid out. Use addtoGridLayout to stack various widgets of this type'''
		super(FitparWidget,self).__init__(parent)
		self.setupUi(self)
#		self.__close=self.close
		self._fpkey=fpkey
		self.label.setText(QString(label))
		self.setMinimumHeight(1.5*self.LEValue.minimumHeight())
#		self.setSizePolicy ( QSizePolicy.Preferred,QSizePolicy.Minimum)
		#connect the Apply and auto buttons to their respective callbacks (or disable them)
		if callbackApply is None: self.BTApply.setDisabled(True)
		else: QObject.connect(self.BTApply,SIGNAL("clicked()"),lambda: callbackApply(self)) #it returns self to the callback
		if callbackAuto is None: self.BTAutoFill.setDisabled(True)
		else: QObject.connect(self.BTAutoFill,SIGNAL("clicked()"),lambda: callbackAuto(self))
		#set up validators
		for widget in [self.LEValue,self.LEMin,self.LEMax]: widget.setValidator(QDoubleValidator(self))
	def addtoGridLayout(self, gridlayout=None, row=None):
		'''gridlayout is used for stacking several FitParWidgets,
		row is the row at which we want the widget to be set. If it is None, it defaults to the last'''
		if gridlayout is None: gridlayout=QGridLayout()
		if row is None: row=gridlayout.rowCount()
		for widget,col in zip ([self.label,self.BTAutoFill,self.LEValue,self.CBFix,self.CBCommon,self.LEMin,self.LEMax,self.BTApply],range(8)):
			gridlayout.addWidget(widget, row,col)
	def removefromGridLayout(self, gridlayout=None, row=None):
		if gridlayout is None: gridlayout=QGridLayout()
		if row is None: row=gridlayout.rowCount()
		for widget in [self.label,self.BTAutoFill,self.LEValue,self.CBFix,self.CBCommon,self.LEMin,self.LEMax,self.BTApply]:
			gridlayout.removeWidget(widget)
			widget.close()
		
	def getFitpar(self):
		'''returns a fitpar object based on the widgets selections'''
		#TODO: validate input
		name=unicode(self.label.text()).split('[')[0]
		try: 
			val=float(unicode(self.LEValue.text()))
			free= not self.CBFix.isChecked()
			minval=unicode(self.LEMin.text())
			maxval=unicode(self.LEMax.text())
			if len(minval)==0:minval=None
			else: minval=float(minval)
			if len(maxval)==0:maxval=None
			else: maxval=float(maxval)
		except ValueError:
			return None
		return fitpar(val=val, name=name, minval=minval, maxval=maxval, free=free)
	def showFitpar(self,fp):
		'''returns a fitpar object based on the widgets selections'''
		if fp is None:
			self.LEValue.setText(QString())
			self.LEMin.setText(QString())
			self.LEMax.setText(QString())
			self.CBFix.setChecked(False)
			return	
		self.LEValue.setText(QString.number(fp.val))
		self.CBFix.setChecked(not(fp.free))
		if fp.minval is None: self.LEMin.setText(QString())
		else: self.LEMin.setText(QString.number(fp.minval))
		if fp.maxval is None: self.LEMax.setText(QString())
		else: self.LEMax.setText(QString.number(fp.maxval))

	@staticmethod
	def addHeader(gridlayout, row=None):
		if row is None: row=gridlayout.rowCount()-1
		hdrVal=QLabel("Value")
		hdrFix=QLabel("F")
		hdrCom=QLabel("C")
		hdrMin=QLabel("Min")
		hdrMax=QLabel("Max")
		gridlayout.addWidget(hdrVal, row,2)
		gridlayout.addWidget(hdrFix, row,3)
		gridlayout.addWidget(hdrCom, row,4)
		gridlayout.addWidget(hdrMin, row,5)
		gridlayout.addWidget(hdrMax, row,6)
		

class PAScualGUI(QMainWindow, ui_PAScualGUI.Ui_PAScual):
	def __init__(self, parent=None):
		super(PAScualGUI,self).__init__(parent)
		self.setupUi(self)
		
		self.tauFPWlist=[]
		self.ityFPWlist=[]
		self.dirtysets=True
		self.dirtyresults=False
		self.palssetsdict={}
		settings = QSettings()  #This  gets the settings from wherever they are stored (the storage point is plattform dependent)
		
		###add hand-coded widgets and modifications to ui_ widgets here
		
		#General OpenFile Dialog (it is never closed, just hidden)
		WorkDirectory= settings.value("WorkDirectory", QVariant(QDir.homePath())).toString()
		self.openFilesDlg=QFileDialog(self, "%s - Open spectra"%QApplication.applicationName(), "./",
		        									 "LT files (*.dat *.txt *.al2 *.chn)\n"+
		        									 "L80 files (*.l80)\n"+
											         "ASCII Files with NO HEADER (*.dat *.txt *.al2 *.chn)\n"+
											         "MAESTRO Binary files (*.chn)\n"+
											         "All (*)")
		self.openFilesDlg.setFileMode(QFileDialog.ExistingFiles)
		self.openFilesDlg.setViewMode(QFileDialog.Detail )
		self.openFilesDlg.setDirectory(WorkDirectory)
		
		#The fitter thread
		self.fitter=PCP.fitter(self)
		
		#FitparWidgets
		layout1=QGridLayout()
		FitparWidget.addHeader(layout1)
		self.fwhmFitparWidget=FitparWidget("fwhm",label="FWHM [ps]", callbackApply=self.applyFitpar, callbackAuto=None)
		self.fwhmFitparWidget.addtoGridLayout(gridlayout=layout1)
		self.bgFitparWidget=FitparWidget("bg",label="Background [cts]", callbackApply=self.applyFitpar, callbackAuto=self.autobackground)
		self.bgFitparWidget.addtoGridLayout(gridlayout=layout1)
		self.c0FitparWidget=FitparWidget("c0",label="Offset [ch]", callbackApply=self.applyFitpar, callbackAuto=self.autoc0)
		self.c0FitparWidget.addtoGridLayout(gridlayout=layout1)
		self.FitparFrame.setLayout(layout1)
		
		#components
		self.compModel=CTMV.PAScomponentsTableModel()
		self.compTable.setModel(self.compModel)
		for c in [CTMV.FIX,CTMV.COMMON]: self.compTable.resizeColumnToContents(c)
		
		#spectraTable
		self.spectraModel=STMV.PASspectraTableModel()
		self.spectraTable.setModel(self.spectraModel)
		self.spectraTable.resizeColumnsToContents()
		
		#Plot dock
		plotlayout=QVBoxLayout()
		self.pplot=PALSplot()
		plotlayout.addWidget(self.pplot)
		self.plotFrame.setLayout(plotlayout)
		
		#Residuals
		reslayout=QHBoxLayout()
		self.resplot=ResPlot()
		self.resplot.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
		reslayout.addWidget(self.resplot)
		self.residualsFrame.setLayout(reslayout)
		
		#fitmodes
		self.fitmodesdict=defaultFitModesDict #global dict storing hardcoded default FitModes
		self.fitModeFileName=unicode(settings.value("fitModeFileName", QVariant(QString("fitmode.pck"))).toString())
		self.fitmodesdict.update(self.loadCustomFitModes(self.fitModeFileName))
		self.fitModeCB.insertItems(0,sorted(self.fitmodesdict.keys()))
		self.commandsModel=CMDTMV.CommandTableModel()
		self.commandsDelegate=CMDTMV.commandDelegate(self)
		self.commandsTable.setModel(self.commandsModel)
		self.commandsTable.setItemDelegate(self.commandsDelegate)
		
		#PreviousFits Log
		self.currentOutputKey=None
		self.previousOutputDict={}  
		
		#Other, misc
		self.LEpsperchannel.setValidator(QDoubleValidator(0,S.inf,3,self)) #add validator to the psperchannel edit	
		self.resultsTable.addActions([self.actionCopy_Results_Selection,self.actionSave_results_as]) #context menu
		self.outputWriteMode=unicode(settings.value("outputWriteMode", QVariant(QString("a"))).toString()) #get user prefs regarding the output file management #TODO: include this in options menu
		self.warning_chi2_low=settings.value("warning_chi2_low", QVariant(0.6)).toDouble()[0] #TODO: include this in options menu
		self.warning_chi2_high=settings.value("warning_chi2_high", QVariant(1.4)).toDouble()[0] #TODO: include this in options menu
		
		#Add connections here
		QObject.connect(self.actionLoad_Spectra,SIGNAL("triggered()"),self.loadSpectra)
		QObject.connect(self.actionAbout,SIGNAL("triggered()"),self.helpAbout)
		QObject.connect(self.actionLicense,SIGNAL("triggered()"),self.showlicense)
		QObject.connect(self.actionSum_Spectra,SIGNAL("triggered()"),self.sumspectra)
		QObject.connect(self.actionWhat_s_This,SIGNAL("triggered()"),lambda:QWhatsThis.enterWhatsThisMode())
		QObject.connect(self.actionLoad_Parameters,SIGNAL("triggered()"), self.loadParameters)
		QObject.connect(self.actionSimulate_spectrum,SIGNAL("triggered()"), self.createFakeSpectrum)
		QObject.connect(self.actionCopy_Results_Selection,SIGNAL("triggered()"), self.copy_Results_Selection)	
		QObject.connect(self.actionShow_hide_Plot,SIGNAL("triggered()"), self.plotDockWidget.toggleViewAction().toggle)	
		
#		QObject.connect(self.actionSaveResults,SIGNAL("triggered()"),self.onSaveResults)
		QObject.connect(self.spectraTable,SIGNAL("doubleClicked(QModelIndex)"),self.onSpectraTableDoubleClick)
		QObject.connect(self.spectraTable.selectionModel(),SIGNAL("selectionChanged(QItemSelection,QItemSelection)"),self.onspectraSelectionChanged)
		QObject.connect(self.SBoxNcomp,SIGNAL("valueChanged(int)"),self.changeNcomp)
		QObject.connect(self.roiPB,SIGNAL("clicked()"),self.setROI)
		QObject.connect(self.BTpsperchannel,SIGNAL("clicked()"),self.setpsperchannel)
		QObject.connect(self.showtauRB,SIGNAL("toggled(bool)"),self.onShowTauToggled)
		QObject.connect(self.spectraModel,SIGNAL("selectionChanged"),self.changePPlot)
		QObject.connect(self,SIGNAL("updateParamsView"),self.onUpdateParamsView)
		QObject.connect(self.selectAllTB,SIGNAL("clicked()"),self.spectraModel.checkAll)		
		QObject.connect(self.selectNoneTB,SIGNAL("clicked()"),lambda: self.spectraModel.checkAll(False))
		QObject.connect(self.selectMarkedTB,SIGNAL("clicked()"),self.onSelectMarked) 
		QObject.connect(self.removeSpectraTB,SIGNAL("clicked()"), self.onRemoveChecked)
		QObject.connect(self.applycompsBT,SIGNAL("clicked()"),self.onApplyComps) 
		QObject.connect(self.applyAllParametersPB,SIGNAL("clicked()"),self.onApplyAllParameters)
		QObject.connect(self.resetParametersPB,SIGNAL("clicked()"),self.onResetParameters)
		QObject.connect(self.actionRegenerateSets,SIGNAL("triggered()"),lambda: self.onRegenerateSets(force=True))
		QObject.connect(self.tabWidget,SIGNAL("currentChanged(int)"),self.onTabChanged)
		QObject.connect(self,SIGNAL("regenerateSets"),self.onRegenerateSets)
		QObject.connect(self.fitModeCB,SIGNAL("currentIndexChanged(const QString&)"),self.onFitModeCBChange)
		QObject.connect(self.applyFitModeBT,SIGNAL("clicked()"),self.assignFitModes)
		QObject.connect(self.goFitBT,SIGNAL("clicked()"),self.onGoFit)
		QObject.connect(self.stopFitBT,SIGNAL("clicked()"),self.onStopFit)
# 		QObject.connect(self.skipCommandBT,SIGNAL("clicked()"),self.advanceFitQueue)
		QObject.connect(self.fitter,SIGNAL("endrun(bool)"), self.onFitterFinished)
		QObject.connect(self.fitter,SIGNAL("command_done(int)"), self.setPBar,SLOT("setValue(int)"))
		QObject.connect(self.commandsModel,SIGNAL("dataChanged(QModelIndex,QModelIndex)"),self.onFitModeEdit)
		QObject.connect(self.hideResultsBT,SIGNAL("clicked()"),self.onHideResults)
		QObject.connect(self.showResultsBT,SIGNAL("clicked()"),self.onShowResults)
		QObject.connect(self.saveResultsBT,SIGNAL("clicked()"),self.onSaveResults)
		QObject.connect(self.resultsTable,SIGNAL("doubleClicked(QModelIndex)"),self.onResultsTableDoubleClick)
		QObject.connect(self.resultsFileSelectBT,SIGNAL("clicked()"),self.onResultsFileSelectBT)
		QObject.connect(self.outputFileSelectBT,SIGNAL("clicked()"),self.onOutputFileSelectBT)
		QObject.connect(self.showPreviousOutputBT,SIGNAL("clicked()"),self.onShowPreviousOutputBT)
		
		
# 		QObject.connect(self.saveOutputBT,SIGNAL("clicked()"),self.onSaveOutput)
		
		
		#Restore last session Window state
		size = settings.value("MainWindow/Size", QVariant(QSize(800, 600))).toSize()
		self.resize(size)
		position = settings.value("MainWindow/Position", QVariant(QPoint(0, 0))).toPoint()
		self.move(position)
		self.restoreState(settings.value("MainWindow/State").toByteArray())
		self.fitModeCB.setCurrentIndex(self.fitModeCB.findText(defaultFitMode))
#		self.plotDockWidget.show()
		
	def copy_Results_Selection(self):
		'''copies the selected results to the clipboard'''
		string=''
		selecteditems=self.resultsTable.selectedItems()
		for i in range(self.resultsTable.rowCount()):
			emptyrow=True
			for j in range(self.resultsTable.columnCount()):
				if self.resultsTable.item(i,j) in selecteditems: 
					if emptyrow: string+='\n%s'%self.resultsTable.item(i,j).text()
					else:string+='\t%s'%self.resultsTable.item(i,j).text()
					emptyrow=False
		QApplication.clipboard().setText(string.strip())
#		print string.strip()	

	def onResultsFileSelectBT(self):
		filename=QFileDialog.getSaveFileName ( self, "Results File Selection", self.openFilesDlg.directory().path()+'/PASresults.txt',
											"ASCII (*.txt)"+
											"All (*)",'',QFileDialog.DontConfirmOverwrite)
		if filename: self.resultsFileLE.setText(filename)
	def onOutputFileSelectBT(self):
		filename=QFileDialog.getSaveFileName ( self, "Output File Selection", self.openFilesDlg.directory().path()+'/PASoutput.txt',
											"ASCII (*.txt)"+
											"All (*)",'',QFileDialog.DontConfirmOverwrite)
		if filename: self.outputFileLE.setText(filename)	
	
	def onResultsTableDoubleClick(self,index):
		self.plotresiduals(self.resultsdplist[index.row()])
	
	def plotresiduals(self,dp):
		self.resplot.reset()
		residuals=(dp.sim-dp.exp[dp.roi])/dp.deltaexp[dp.roi]
		self.resplot.attachCurve(dp.roi,residuals,name=dp.name, pen=QPen(Qt.red,2))
	def onHideResults(self):
		indexes=self.resultsColumnsListWidget.selectedIndexes()
		for idx in indexes: 
			self.resultsTable.hideColumn(idx.row())
			self.resultsColumnsListWidget.itemFromIndex(idx).setForeground(QBrush(Qt.gray))
#		self.resultsColumnsListWidget.reset()
	def onShowResults(self):
		indexes=self.resultsColumnsListWidget.selectedIndexes()
		for idx in indexes: 
			self.resultsTable.showColumn(idx.row())
			self.resultsColumnsListWidget.itemFromIndex(idx).setForeground(QBrush(Qt.black))
#		self.resultsColumnsListWidget.reset()
		
	def onFitModeEdit(self,*args):
		fmname='<user>'
		self.fitmodesdict[fmname]=tuple(["%s %s"%(c.cmd,c.args) for c in self.commandsModel.dumpData()])
		self.fitModeCB.setCurrentIndex(self.fitModeCB.findText(fmname))
		#TODO: add to the combobox and enable the save button
		self.saveFitmodeBT.setEnabled(True)
		self.assignFitModes()
		
	def onFitterFinished(self,completed):
		if self.fitter.isRunning(): 
#			QMessageBox.warning(self, "Race condition","A possible race condition occurred. \nThis may be a bug. If you can reproduce it, please report it to the author\nThe fit will be resumed automatically",QMessageBox.Ok)
			if not self.fitter.wait(1000):
				QMessageBox.critical(self, "Race condition","Something went wrong. \nThis may be a bug. If you can reproduce it, please report it to the author\nThe fit needs to be stopped and re-started manually",QMessageBox.Ok)
				raise RuntimeError('onFitterFinished: self.fitter is still running!') 
		#we know fitter is not running, so we safely access its internal palsset and status
		ps=copy.deepcopy(self.fitter.ps) 
		completed=copy.deepcopy(self.fitter.completed) #deepcopy makes little sense here but... who cares?
		#We add the ps to a list for later use
		self.resultslist.append(ps)
		#now we can use our copies to insert data into the summary
		if completed:
			self.dirtyresults=True
			row=self.resultsTable.rowCount()
			for dp in ps.spectralist:
				self.resultsdplist.append(dp) 
				self.resultsTable.insertRow(row)
				rowitems=(dp.showreport_1row(file=None, min_ncomp=self.results_min_ncomp,silent=True)).split()
#				print "DEBUG:", self.warning_chi2_low,dp.chi2,self.warning_chi2_high
				if (self.warning_chi2_low<dp.chi2/dp.dof<self.warning_chi2_high): bgbrush=QBrush(Qt.white) #is chi2 value ok?
				else: bgbrush=QBrush(Qt.red) #highlight if chi2 is out of normal values
				for c,s in zip(range(len(rowitems)),rowitems):
					item=QTableWidgetItem(s)
					item.setBackground(bgbrush)
					self.resultsTable.setItem(row,c,item)				
				row+=1
			self.resultsTable.resizeColumnsToContents()
			self.advanceFitQueue()
		return completed
	
	def onFitModeCBChange(self,fitmodename):
		fitmodename=unicode(fitmodename)
		fitmode=self.fitmodesdict[fitmodename]
		self.commandsModel.loadData(fitmode,None)
		self.commandsTable.resizeColumnsToContents()
		#assign:
		self.assignFitModes()
		
	def assignFitModes(self):
		commands=self.commandsModel.dumpData()
		if self.selectedSetsOnlyCB.isChecked(): #Assign only to the selected sets if the box is checked
			selectedSets=self.setsTree.selectedItems()
			for item in selectedSets: 
				key=unicode(item.text(0))
				self.palssetsdict[key].commands=commands
		else:#if the box is not checked, assign the current fitmode to all the sets
			for ps in self.palssetsdict.values(): ps.commands=commands


	def advanceFitQueue(self, key=None):
		if self.fitter.isRunning(): 
			print 'DEBUG: cannot launch another fit while one fit is running' #TODO: handle this properly
			return
		if len (self.fitqueuekeys)==0:
			self.onStopFit()
			self.totalPBar.setValue(0)
			return
		else:
			if key is None: i=0
			else: i=self.fitqueuekeys.index(key)
			#get the palsset
			ps=self.fitqueuedict.pop(self.fitqueuekeys.pop(i)) #the key and the ps are removed from the list and dict respectively
			#deal with progressbars
			self.setPBar.reset()
			self.setPBar.setMaximum(len(ps.commands))
			self.totalPBar.setValue(-len(self.fitqueuekeys)-1)
			#start a new fit
			self.fitter.initialize(ps,self.outputfile)
			self.fitter.start()
			#Show message in status Bar
			self.statusbar.showMessage("Fitting %s..."%ps.name, 0) 
			
	def generatequeue(self):
		if self.fitter.isRunning(): 
			print 'DEBUG: cannot regenerate the queue while one fit is running' #TODO: handle this properly
			return
		#create a filtered version of palssetsdict (remove those which have no commands)
		rejected={}
		accepted={}
		for ps in self.palssetsdict.values():
			if len(ps.commands)==1 and ps.commands[0].cmd.upper()=='END': rejected[ps.name]=ps
			else: accepted[ps.name]=ps
		#Build a queue, sorting the keys in the palssetsdict (the queue is a deepcopy!)
		self.fitqueuedict=copy.deepcopy(accepted) #The queue is a copy!
		self.fitqueuekeys=sorted(self.fitqueuedict.keys()) #note: at some point this could be used to implement user defined sorting (by assigning a preffix that affects the sort) 
		return accepted,rejected #returns both dictionaries. IMPORTANT: they contain references to the palssets in palssetsdict, not copies!
	
	def onStopFit(self):
		#delete the queue
		self.fitqueuedict={}
		self.fitqueuekeys=[]
		#Ask the fitter thread to stop and wait till it does stop
		self.fitter.stop()
		self.statusbar.showMessage("Waiting for the fit to finish...", 0) 
		self.fitter.wait()
		self.statusbar.showMessage("Fitting finished", 0) 
		#activate the startbutton
		self.goFitBT.setEnabled(True)
		
	def onGoFit(self):
		'''launches the fit'''
		#populate the queue (generates self.fitqueuedict )
		self.generatequeue()
		if len(self.fitqueuedict)==0: 
			QMessageBox.information(self, "Nothing to do","There are no sets to fit",QMessageBox.Ok)
			return								
		#check the common itys for each set in the queue
		for ps in self.fitqueuedict.values():
			answer=None
			if not ps.goodItyErrors(): 
				answer=QMessageBox.warning(self, "Estimation of covariance may fail in LOCAL",
												"<p>The estimation of uncertainties for <b>intensities</b> in %s may not be good if:</p>"
												"<p>a) you use LOCAL minimisation <b>and</b></p>"
												"<p>b) some spectra have common intensities, <b>and</b></p>"
												"<p>c) not <b>all</b> of the intensities are common for the set."
												"<p>Note 1: the uncertainties estimated by the Bayesian Inference algorithm are not affected by this problem</p>"
												"<p>Note 2: in any case, the uncertainties given by LOCAL are based on the covariance matrix and should not be blindly trusted (more about this in the help files)</p>"
												"<p>(if you choose to ignore, this warning won't be repeated for this fit)<p>"%ps.name
												,QMessageBox.Ignore|QMessageBox.Cancel)
				break #regardless of the answer, there is no need to continue checking
		if answer==QMessageBox.Cancel: return  #if the user chose to cancel, do no more.
		#checks before starting
		if self.dirtyresults:
			answer=QMessageBox.question(self, "Unsaved results","There are previous unsaved results. \nSave them before continuing?",QMessageBox.Yes|QMessageBox.No|QMessageBox.Cancel)
			if answer==QMessageBox.Yes: self.onSaveResults()
			elif answer==QMessageBox.No: pass
			else: return #cancel the "goFit"
		#deactivate the startbutton
		self.goFitBT.setEnabled(False)
		#initialise a tee for output 
		self.outputfile=open(unicode(self.outputFileLE.text()),self.outputWriteMode)#self.outputWriteMode is one of  'w' or 'a'
		mytee=tee(sys.__stdout__, self.outputfile)
		mytee.setEmitEnabled(True)
		#Copy the current output box to the Previous Fits box and then clear the current one
		if not self.currentOutputKey is None: 
			self.previousOutputDict[self.currentOutputKey]=self.outputTE.document().clone() #store the previous output in the dict
			self.previousOutputCB.insertItem(0,self.currentOutputKey) #put a new entry in the combo box
		self.currentOutputKey=unicode(time.strftime('%Y/%m/%d %H:%M:%S')) #Update the current Output key
		
		
# 		'DEBUG: >>>>>>>>>',unicode(self.outputTE.toPlainText()),'<<<<<<<<<<<<<<'
# 		self.previousOutputDict[self.currentOutputKey]=self.outputTE.document().clone()
# 		self.currentOutputKey=time.strftime('%Y/%m/%d %H:%M:%S') #This is the key where  this 
# 		self.previousOutputDict[key]
		#reset the output box if the overwrite mode is on
		if self.outputWriteMode=="w": self.outputTE.clear()
#		QObject.connect(emitter,SIGNAL("teeOutput"), self.kk)
#		mytee.addQTextEdit(self.outputTE)
		sys.stdout=mytee
		#reset the saved results
		self.resultslist=[]
		self.resultsdplist=[]
		#reset the saveslots
		self.fitter.saveslot=self.fitter.saveslot_auto=self.fitter.saveslot_user=None
		#Prepare the results table
		self.resultsTable.clear()
		self.resultsTable.setRowCount(0)
		spectra=[]
		for ps in self.fitqueuedict.values():spectra+=ps.spectralist
		self.results_min_ncomp=max([ob.ncomp for ob in spectra])
		self.resultsHeader=["name","chi2","autocorr","Set","ROImin","ROImax","ROIch","Integral","FWHM","dev","c0","dev","bg","dev"]
		for i in range(1,self.results_min_ncomp+1):self.resultsHeader+=["ity%i"%i,"dev"]
		for i in range(1,self.results_min_ncomp+1):self.resultsHeader+=["tau%i"%i,"dev"]
		self.resultsTable.setColumnCount(len(self.resultsHeader))
		self.resultsTable.setHorizontalHeaderLabels(self.resultsHeader)
		#populate the column list
		self.resultsColumnsListWidget.clear()
		self.resultsColumnsListWidget.addItems(self.resultsHeader)
		#set the initial state of the progress bars	
		self.totalPBar.reset()
		self.totalPBar.setRange(-len(self.fitqueuedict),0)
		self.commandPBar.reset()
		self.setPBar.reset()
		#Print a message to indicate a new calculation
		print 60*'*'
		print time.asctime()
		print 60*'*'
		#Start the fit
		self.advanceFitQueue()
		
	def onShowPreviousOutputBT(self):
		'''prints the previous output in a pop up window)'''
		key=unicode(self.previousOutputCB.currentText())
		if key=="All":
			pass
		else: 
			doc=self.previousOutputDict[key]
		
		
			
	def loadCustomFitModes(self,file=None):
		try: customFitModesdict=pickle.load(open(self.fitModeFileName,'rb'))
		except IOError: 
#			printwarning("No custom FitModes loaded")
			customFitModesdict={}
		return customFitModesdict
		
	def closeEvent(self,event):
		'''This event handler receives widget close events'''
		#save current window state before closing
		settings = QSettings()
		settings.setValue("MainWindow/Size", QVariant(self.size()))
		settings.setValue("MainWindow/Position",QVariant(self.pos()))
		settings.setValue("MainWindow/State",QVariant(self.saveState()))
		settings.setValue("MainWindow/Position",QVariant(QString(self.fitModeFileName)))
		settings.setValue("outputWriteMode",QVariant(QString(self.outputWriteMode)))
		settings.setValue("WorkDirectory",QVariant(self.openFilesDlg.directory().path()))
		settings.setValue("warning_chi2_low",QVariant(self.warning_chi2_low)) 
		settings.setValue("warning_chi2_high",QVariant(self.warning_chi2_high))
		
		
	def onTabChanged(self,tabindex):
		if tabindex==1: self.emit(SIGNAL("regenerateSets"),False)	

	def onRegenerateSets(self, force=False):
		#only regenerate if there is a chance of change (or if we explicitely force it)
		if not self.dirtysets and not force:return
		#get a copy of the list of spectra
		temp=self.spectraModel.dumpData() #note that this is a deepcopy
		#filter the list separating the ready ones from the not-yet-ready
		spectra=[]
		failed=[]
		for dp in temp:
			realinit=dp.initifready(force=True)
			if realinit:spectra.append(dp) 
			else: failed.append(dp)
		#distribute the ready ones into sets
		palssetslist=distributeinsets(spectra)
		#create a dict containing the sets by their names and the queue list
		self.palssetsdict={}
		for ps in palssetslist:	self.palssetsdict[ps.name]=ps		
		#Populate the sets TreeWidget
		self.setsTree.clear()
		for ps in palssetslist:
			item=QTreeWidgetItem(self.setsTree, [ps.name,QString.number(len(ps.spectralist))] )
		item.addChildren ( [QTreeWidgetItem([dp.name]) for dp in ps.spectralist] )
		#Show the number of failed (unasigned) spectra
		self.unasignedLE.setText(QString.number(len(failed)))
		#readjust columns in TreeWidget
		self.setsTree.setColumnWidth(0,max(40,int(0.7*self.setsTree.width())))
		#assign fitmode to the newly created sets
		self.assignFitModes()
		#mark that the sets are freshly calculated (not dirty)
		self.dirtysets=False
	
	def onSelectMarked(self):
		indexes=self.spectraTable.selectionModel().selectedIndexes()
		if indexes ==[]: return
		for idx in indexes:
			if not self.spectraModel.data(idx,Qt.UserRole).selected: self.spectraModel.setData(self.spectraModel.index(idx.row(),STMV.SEL))
	
	def onRemoveChecked(self):
		answer=QMessageBox.question(self, "Removal confirmation","The checked spectra will be removed from the list.\nProceed?",QMessageBox.Ok|QMessageBox.Cancel)
		if answer==QMessageBox.Ok: self.spectraModel.removeChecked()
		#Maybe the selection changed?
		self.onspectraSelectionChanged()
		#mark that the sets might be dirty now
		self.dirtysets=True	
		#signal recalculation of sets
		self.emit(SIGNAL("regenerateSets"),False)
	
	def sumspectra(self):
		'''Sums the checked spectra and offers to save them. It inserts the sum in the list'''
		selected,indexes=self.spectraModel.getselectedspectra()
		if len(selected)<2:return
		dpsum=copy.deepcopy(selected[0])
		dpsum.name= dpsum.name.rsplit('.',1)[0]+"_%isum"%len(selected)
		try:
			for dp in selected[1:]:
				dpsum.exp+=dp.exp
		except ValueError:
			QMessageBox.warning(self, "Spectra cannot be added "," When summing spectra, they must have the same number of channels.\n Aborting.""")
			return
		dpsum.initifready(force=True)
		self.savespectrum(dpsum)		
		self.spectraModel.insertRows(position=None,rows=1,dps=[dpsum])
		for idx in indexes:
			idx=self.spectraModel.index(idx.row(),STMV.PSPC)	
			self.spectraModel.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"),idx, idx)
		return True			
		
	def onSpectraTableDoubleClick(self, index):	
		if index.column()==STMV.SEL:return
		self.spectraModel.checkAll(False)
		self.spectraModel.setData(self.spectraModel.index(index.row(),STMV.SEL))
# 		print "DEBUG:", index.row(), index.column()	
	
	def onspectraSelectionChanged(self,a=None,b=None):
		selrows=self.spectraTable.selectionModel().selectedRows()
		nselrows=len(selrows)
		if nselrows==0:	self.emit(SIGNAL("updateParamsView"),discretepals())
		elif nselrows==1:	self.emit(SIGNAL("updateParamsView"),self.spectraModel.data(selrows[0], role=Qt.UserRole))
		else: self.emit(SIGNAL("updateParamsView"),None)
		
	def onShowTauToggled(self,checked):
		self.compModel.showtau=checked
		self.compModel.reset()
		
	def changeNcomp(self, ncomp):
		old=len(self.compModel.components)
		change=ncomp-old
		if change>0: 
			self.compModel.insertRows(old,rows=change)
		else: 
			self.compModel.removeRows(ncomp,rows=-change)
			
	def setpsperchannel(self):
		selected,indexes=self.spectraModel.getselectedspectra()
		if selected ==[]: return
		for dp in selected:
			if len(unicode(self.LEpsperchannel.text()))==0:
				QMessageBox.warning(self, "Invalid input"," The channel width must be a positive number""")
				return False
			dp.psperchannel=float(self.LEpsperchannel.text())
		for idx in indexes:
			idx=self.spectraModel.index(idx.row(),STMV.PSPC)	
			self.spectraModel.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"),idx, idx)
		#mark that the sets might be dirty now
		self.dirtysets=True	
		return True
			
	def onUpdateParamsView(self,dp=None):
		if dp is None: 
#			self.parametersTab.setEnabled(False)
			return
#		else:self.parametersTab.setEnabled(True) 
		self.bgFitparWidget.showFitpar(dp.bg)
		self.c0FitparWidget.showFitpar(dp.c0)
		self.fwhmFitparWidget.showFitpar(dp.fwhm)
		if dp.psperchannel is None: self.LEpsperchannel.setText(QString())
		else: self.LEpsperchannel.setText(QString.number(dp.psperchannel))
		
		if dp.taulist is None: return  #TODO !!!!  maybe: self.SBoxNcomp.setValue(0)
		self.SBoxNcomp.setValue(len(dp.taulist)) #this puts the right number of comps
		for i in xrange(len(dp.taulist)):
			self.compModel.components[i].tau=copy.deepcopy(dp.taulist[i])
			self.compModel.components[i].ity=copy.deepcopy(dp.itylist[i])
			self.compModel.components[i].tau.common=self.compModel.components[i].ity.common=False
		self.compModel.reset()
		#TODO: update what is shown in the fitpars Do this by calling a separate function:
		##If only one is selected, show the fitpars that are set
		##If more than one is selected, show only those which are common and mark in a different way those which are different amongst selection
		##Possibly use a color code for background of the LE's: white for those not set, yellow for those set (and same among selection), magenta for those which have different values among selection
		##Possibly check if they have common settings and show those 
	
	def setROI(self):
		selected,indexes=self.spectraModel.getselectedspectra()
		if selected ==[]: return
		ROIselector=ROISelectorDialog(self, selected,"ROI")
		ROIselector.connect(app,SIGNAL('focusChanged(QWidget *, QWidget *)'),ROIselector.onFocusChanged)
		if ROIselector.exec_():
			for dp,bgroi in zip(selected,ROIselector.roilist): dp.roi=bgroi
			self.spectraTable.resizeColumnToContents(STMV.ROI)
		#mark that the sets might be dirty now
		self.dirtysets=True			
		
	def applyFitpar(self, caller, selected=None, indexes=None):
		if indexes is None:
			if not(selected is None): raise ValueError('applyFitpar: Ignoring "selected" because "indexes" were not passed')
			selected,indexes=self.spectraModel.getselectedspectra() 
		if selected == []: return False#if it is empty, then nothing is selected so do nothing
#		print "DEBUG: Apply:",caller.label.text()
		fp=caller.getFitpar()
		if fp is None: 
			QMessageBox.warning(self, "Invalid input","'Value' must be a number.\n 'Min' and 'Max' must either be numbers or be empty.""")
			return False
		fp.forcelimits()
		for dp in selected:
			if caller.CBCommon.isChecked(): dp.__dict__[caller._fpkey]=fp
			else: dp.__dict__[caller._fpkey]= copy.deepcopy(fp)
		#Send signals notifying the changes
		ncol=self.spectraModel.columnCount()
		for idx in indexes:
			idx1=self.spectraModel.index(idx.row(),0)
			idx2=self.spectraModel.index(idx.row(),ncol)			
			self.spectraModel.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"),idx1, idx2)
#		print "DEBUG:",fp.name, fp.val, fp.minval, fp.maxval, fp.free, type(fp), caller._fpkey
		#mark that the sets might be dirty now
		self.dirtysets=True				
		return True
	
	def onApplyComps(self,selected=None, indexes=None):
		if indexes is None:
			if not(selected is None): raise ValueError('applyFitpar: Ignoring "selected" because "indexes" were not passed')
			selected,indexes=self.spectraModel.getselectedspectra() 
		if selected == []: return False #if it is empty, then nothing is selected so do nothing
		answer=None  
		#check if the components are already set for this spectrum (TODO: possibly suggest to apply only selected components )
		ncomps=self.compModel.rowCount()
		nspect=len(selected)
		applymatrix=S.zeros((nspect,ncomps),dtype='bool') #The applymatrix is a boolean matrix that says whether to apply a given component to a given spectrum
		for i in range(applymatrix.shape[0]):	#go through rows
			dp=selected[i]
			if dp.taulist is None: 
				applymatrix[i,:]=True #Apply all components to this spectrum
				dp.taulist=ncomps*[None] #wipe taulist for this dp
				dp.itylist=ncomps*[None]
			elif len(dp.taulist)==ncomps: applymatrix[i,:]=True #Apply all (we don't ask)
			elif answer==QMessageBox.YesToAll: 
				applymatrix[i,:]=True
				dp.taulist=ncomps*[None] #wipe taulist for this dp
				dp.itylist=ncomps*[None]
			elif answer==QMessageBox.NoToAll: applymatrix[i,:]=False
			else: 
				answer=QMessageBox.warning(self, "Components numbers do not match","Spectrum %s has %i components already defined\n Discard them?"%(dp.name,len(dp.taulist)),QMessageBox.Yes|QMessageBox.YesToAll|QMessageBox.No|QMessageBox.NoToAll)
				if answer==QMessageBox.Yes or answer==QMessageBox.YesToAll: 
					applymatrix[i,:]=True
					dp.taulist=ncomps*[None] #wipe taulist for this dp
					dp.itylist=ncomps*[None]
				else: applymatrix[i,:]=False				
			if len(dp.taulist)==0: dp.taulist=dp.itylist=None
		#At this point we have an applymatrix and taulist of the correct size. So we can apply the components
		for j in xrange(ncomps):
			cp=self.compModel.components[j]
			#We regenerate the components instead of using the existing fitpar because we want to reinitialize them!
			tau=fitpar(val=cp.tau.val, name='Tau%i'%(j+1), minval=cp.tau.minval, maxval=cp.tau.maxval, free=cp.tau.free)
			ity=fitpar(val=cp.ity.val, name='Ity%i'%(j+1), minval=cp.ity.minval, maxval=cp.ity.maxval, free=cp.ity.free)
			for i in xrange(nspect):
				dp=selected[i]
				if applymatrix[i,j]:
					if not cp.tau.common:tau=copy.deepcopy(tau) #if they are common, we use the same object. If not, we use a copy
					if not cp.ity.common: ity=copy.deepcopy(ity)
					dp.taulist[j],dp.itylist[j]=tau,ity	
		#mark that the sets might be dirty now
		self.dirtysets=True				
#		dp.taulist=[c.tau for c in self.compModel.components]
#		dp.itylist=[c.ity for c in self.compModel.components]

#		for dp in selected: print "DEBUG: onApplyComps", dp.name,dp.taulist
		#notify of the changes
		for idx in indexes:
			idx=self.spectraModel.index(idx.row(),STMV.COMP)
			self.spectraModel.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"),idx, idx)
		return True
	
	def onApplyAllParameters(self):
		self.applyFitpar(self.bgFitparWidget)
		self.applyFitpar(self.c0FitparWidget)
		self.applyFitpar(self.fwhmFitparWidget)
		self.setpsperchannel()
		self.onApplyComps()
	def onResetParameters(self):
		self.SBoxNcomp.setValue(0)
		self.bgFitparWidget.showFitpar(None)
		self.c0FitparWidget.showFitpar(None)
		self.fwhmFitparWidget.showFitpar(None)
		self.LEpsperchannel.setText("")
#		self.setpsperchannel !!! AND ROI
		
	def autoc0(self,caller):
		selected,indexes=self.spectraModel.getselectedspectra()
		if selected ==[]: return 
		self.statusbar.showMessage("AutoOffset working...", 0) 
		if caller.CBCommon.isChecked():
			answer=QMessageBox.warning(self, "Incompatible input",
								unicode("The AutoOffset function is not compatible with a common Offset parameter\n"
										"If you continue, the 'common' option will be unchecked."),QMessageBox.Ok|QMessageBox.Cancel)
			if answer==QMessageBox.Ok:
				caller.CBCommon.setCheckState(Qt.Unchecked)
			else:
				self.statusbar.showMessage("AutoOffset Cancelled", 0) 
				return  #abort the autoc0
		#TODO: CHECK THAT fwhm and psperchannel are set for all selected ones. If not, abort
		nerror=error=ignoreerror=False
		for dp in selected:
			if dp.psperchannel is None: error="The channel width for this spectrum must be defined in order to use AutoOffset\n"
			elif dp.fwhm is None: error="The resolution (FWHM) for this spectrum must be defined in order to use AutoOffset\n"
			else: error=False
			if error:
				nerror+=1
				if  ignoreerror: continue #skip this one if it was previously chosen to ignore all
				else: 
					answer=QMessageBox.warning(self, "Input error in %s"%dp.name, 
												"Input error in %s :\n %s \nContinue? (skipping this)"%(dp.name,error),
										  		QMessageBox.Yes|QMessageBox.YesToAll|QMessageBox.No)
					if answer==QMessageBox.No: 
						self.statusbar.showMessage("AutoOffset Cancelled", 0)
						return #stop processing and return without accepting the dialog
					elif answer==QMessageBox.YesToAll: ignoreerror=True #it won t ask anymore
			else:	
				val=dp.exp.argmax(0)#a coarse approx of the time 0 channel
				temp=max(1.,dp.fwhm.val*2./dp.psperchannel) 
				minval=val-temp
				maxval=val+temp
				dp.c0=fitpar(val=val, name='c0', minval=minval,maxval=maxval,free=not(caller.CBFix.isChecked()))
				dp.c0.forcelimits()
		self.onUpdateParamsView(dp) #update what is shown
		for idx in indexes:
			idx=self.spectraModel.index(idx.row(),STMV.C0)
			self.spectraModel.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"),idx, idx)
		self.statusbar.showMessage("AutoOffset Finished (with %i warnings)"%nerror, 0)

	def autobackground(self,caller):
		selected,indexes=self.spectraModel.getselectedspectra()
		if selected == []: return
		#Check if the 'common' option is checked
		if caller.CBCommon.isChecked():
			answer=QMessageBox.warning(self, "Incompatible input",
								unicode("The Auto Background function is not compatible with a common background parameter\n"
										"If you continue, the 'common' option will be unchecked."),QMessageBox.Ok|QMessageBox.Cancel)
			if answer==QMessageBox.Ok:
				caller.CBCommon.setCheckState(Qt.Unchecked)
			else: return  #abort the autobackground 
		#launch the dialog in modal mode and execute some code if accepted
		BGselector=ROISelectorDialog(self, selected,"Background")
		BGselector.connect(app,SIGNAL('focusChanged(QWidget *, QWidget *)'),BGselector.onFocusChanged)
		if BGselector.exec_():
			for dp,bgroi in zip(selected,BGselector.roilist):
				val=dp.exp[bgroi].mean()
				std10=10*max(10,S.sqrt(val),dp.exp[bgroi].std())
				#The bg is directly updated!
				dp.bg=fitpar(val=val, name=u'Bg(auto)', minval=max(0,val-std10), maxval=val+std10, free=not(caller.CBFix.isChecked()))
				dp.bg.forcelimits()
			#Notify of the changes
			for idx in indexes:
				idx=self.spectraModel.index(idx.row(),STMV.BG)
				self.spectraModel.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"),idx, idx)
			self.onUpdateParamsView(dp)
			
	def changePPlot(self, dp, index=None, replot=True):
		if dp.selected: self.pplot.attachCurve(S.arange(dp.exp.size),dp.exp,name=dp.name)
		else: self.pplot.detachCurve(dp.name)
		if replot: self.pplot.replot()

	def loadSpectra(self):
		#Todo: do an inteligent identification of files (LT header present?) possibly also get data from the LT header (psperchannel and fwhm)
		fileNames=[]
		if not self.openFilesDlg.exec_(): return

		fileNames = [unicode(item) for item in self.openFilesDlg.selectedFiles()]
		filetype=unicode(self.openFilesDlg.selectedFilter())
#		print "DEBUG: loadSpectra:", type(filetype), filetype
		if filetype.startswith("LT"): filetype,hdrlns=1,4
		elif filetype.startswith("L80"): filetype,hdrlns=2,0
		elif filetype.startswith("ASCII"): filetype,hdrlns=3,0
		elif filetype.startswith("MAESTRO"): filetype,hdrlns=4,0
		else: filetype,hdrlns=0,0
		
		dps=[]
		answer=None
		progress=QProgressDialog("Loading Files...", "Abort load", 0, len(fileNames), self)
		progress.setWindowModality(Qt.WindowModal)
#		progress.setMinimumDuration(1000)
		ifl=0
		for fname in fileNames:
			#manage the progress dialog
			ifl+=1
			progress.setValue(ifl)
			app.processEvents()
			if progress.wasCanceled(): break
			#read data
			if filetype==4: 
				hdr,expdata=CHNfiles.CHN.readCHN(fname)
				expdata=S.array(expdata, dtype='d')
			else:
				try: 
					expdata=S.loadtxt(fname,skiprows=hdrlns,dtype='d').flatten()
				except ValueError:
					if answer!=QMessageBox.YesToAll:
						answer=QMessageBox.warning(self, "Wrong file format",
													"Unexpected format in: %s\n"
													"Maybe the file was modified to include an LT header?\n"
													"Do you want to try to load it as an LT file?"%os.path.basename(fname),
													QMessageBox.Yes|QMessageBox.YesToAll|QMessageBox.Cancel)	
					if answer==QMessageBox.Yes or answer==QMessageBox.YesToAll: expdata=S.loadtxt(fname,skiprows=4,dtype='d').flatten()
					if answer==QMessageBox.Cancel: break
			#find a unique key for this file
			usednames=[dp.name for dp in self.spectraModel.spectra]
			basename_=basename=os.path.basename(fname)
			i=1
			while basename in usednames: 
				i+=1
				basename="%s(%i)"%(basename_,i)	
			#create a discretepals with this basename 
			dps.append(discretepals(name=basename, expdata=expdata))
		#Uncheck previously checked spectra
		self.spectraModel.checkAll(False)
		#insert the just created dps in the list
		self.spectraModel.insertRows(position=None,rows=len(dps),dps=dps)
		self.spectraTable.resizeColumnToContents(STMV.NAME)
		#Maybe the "soft" selection changed?
		self.onspectraSelectionChanged()
		#mark that the sets might be dirty now
		self.dirtysets=True	
		#signal regeneration of sets
		self.emit(SIGNAL("regenerateSets"),False)
		self.statusbar.showMessage("Done", 0) 
		#propose to set the ROI
		answer=QMessageBox.question(self, "Set ROI?",
									"Do you want to set the Region Of Interest (ROI) for the loaded spectra now?\n"
									"(It can also be done later, with the Set ROI button)"
									,QMessageBox.Yes|QMessageBox.No, QMessageBox.Yes)	
		if answer==QMessageBox.Yes: self.setROI()

		
	def savespectrum(self,spectrum, filename=None, columns=1, fileformat=None):
		#TODO: save in different formats
		if filename is None:
			filename=unicode(self.openFilesDlg.directory().path())+'/'+spectrum.name+'.dat'
			filename=unicode(QFileDialog.getSaveFileName ( self, "Save spectrum", filename,
														"LT files (*.dat *.txt *.al2 *.chn)\n"+
														"L80 files (*.l80)\n"+
														"ASCII Files with NO HEADER (*.dat *.txt *.al2 *.chn)\n"+
														"All (*)"))
		if filename:
			try:
				spectrum.name=os.path.basename(filename)
				S.savetxt(filename,spectrum.exp,fmt='%i')
				spectrum
			except IOError:
				QMessageBox.warning(self, "Error saving file","Error saving file. Spectrum won't be written")
				return None
			return filename
		return None
		
		
	def onSaveResults(self,ofile=None):
		#Manage the file
		if ofile is None: ofile=unicode(self.resultsFileLE.text())
		if not isinstance(ofile,file): 
			ofile=unicode(ofile)
			openmode='a'
			if os.path.exists(ofile):
				answer=QMessageBox.question(self, "Append data?","The selected results File Exists.\nAppend data?\n (Yes for Append. No for Overwrite)",QMessageBox.Yes|QMessageBox.No|QMessageBox.Cancel)	
				if answer==QMessageBox.Yes: openmode='a'
				elif answer==QMessageBox.No: openmode='w'
				else: return
			try:
				ofile=open(ofile,openmode)
			except IOError:
				QMessageBox.warning(self, "Error opening file","Error opening file. Results won't be written")
				return
		#Check if there are hidden cells
		hidden=0
		saveall=True
		for i in xrange(self.resultsTable.columnCount()):hidden+=int(self.resultsTable.isColumnHidden(i))
		if hidden:
			answer=QMessageBox.question(self, "Hidden Results","Some results are not shown. \nSave them too?",QMessageBox.Yes|QMessageBox.No|QMessageBox.Cancel)	
			if answer==QMessageBox.Yes: saveall=True
			elif answer==QMessageBox.No: saveall=False
			else: return
		#prompt for a description of the results
		(customdescription,ok)= QInputDialog.getText (self,"Description?", "Description:", QLineEdit.Normal, u"",  Qt.Dialog)
#		customdescription,ok= QInputDialog.getText( const QString & title, const QString & label, QLineEdit::EchoMode echo = QLineEdit::Normal, const QString & text = QString(), bool * ok = 0, QWidget * parent = 0, const char * name = 0, Qt::WindowFlags f = 0 )
		#Write the results to the file
		widths=[20,14,14,9,6,6,6,14,9,9,9,9,9,9]+4*self.results_min_ncomp*[9]
		print >>ofile, "\n"
		print >>ofile, "# "+ time.asctime()
		print >>ofile, "# "+ customdescription  
		for col in xrange(self.resultsTable.columnCount()):
			if saveall or not self.resultsTable.isColumnHidden(col): 
				fmt="%%%is\t"%widths[col]
				ofile.write(fmt%self.resultsHeader[col])
		for row in xrange(self.resultsTable.rowCount()):
			ofile.write("\n")
			for col in xrange(self.resultsTable.columnCount()):
				if saveall or not self.resultsTable.isColumnHidden(col):
					fmt="%%%is\t"%widths[col]
					ofile.write(fmt%unicode(self.resultsTable.item(row,col).text()))					
		ofile.close()
		self.dirtyresults=False
		
	def createFakeSpectrum(self, area=None, roi=S.arange(1024), name=None):
#		if roi is None: roi=S.arange(1024)
		#get the parameters
		if area is None: 
			area,okflag= QInputDialog.getDouble (self,"Area?", "Number of counts in simulated spectrum:", 1e6, 0, 1e99, 3)
			if not okflag: 
				self.statusbar.showMessage("Simulation aborted"%ps.name, 0) 
				return
		bg=self.bgFitparWidget.getFitpar()
		c0=self.c0FitparWidget.getFitpar()
		fwhm=self.fwhmFitparWidget.getFitpar()
		psperchannel=float(self.LEpsperchannel.text())
		taulist=[]
		itylist=[]
		ncomps=self.compModel.rowCount()
		for j in xrange(ncomps):
			cp=self.compModel.components[j]
			taulist.append(fitpar(val=cp.tau.val, name='Tau%i'%(j+1), minval=cp.tau.minval, maxval=cp.tau.maxval, free=cp.tau.free))
			itylist.append(fitpar(val=cp.ity.val, name='Ity%i'%(j+1), minval=cp.ity.minval, maxval=cp.ity.maxval, free=cp.ity.free))
		#construct the discretepals
		dp=discretepals(name='fake', expdata=None, roi=roi, taulist=taulist, itylist=itylist, bg=bg, fwhm=fwhm, c0=c0, psperchannel=psperchannel, area=area, fake=True)
		#save it
		self.savespectrum(dp)	
		
	def loadParameters(self,dp=None):
		'''uses a dp to fill the parameters. If no spectra si given, it asks to load a file which is expected to contain a pickled discretepals'''
		pass #TODO
	
	def helpAbout(self):
		QMessageBox.about(self, "About PAScual",
							"""<b>PAScual</b> v %s
							<p>Author: Carlos Pascual-Izarra. carlos.pascual-izarra@csiro.au
							<p>Home page: <a href='%s'>%s</a>
							<p>Copyright &copy; 2008 All rights reserved. 
							<p>See Credits.txt for acknowledgements
							<p>
							<p>If you use PAScual for your research, please cite:
							<p>%s
							<p>
							<p>Python %s - Qt %s - PyQt %s on %s""" % (
							__version__,__homepage__,__homepage__,__citation__, platform.python_version(),
							QT_VERSION_STR, PYQT_VERSION_STR, platform.system()))
	def showlicense(self):
		QMessageBox.about(self, "Licensing terms",
							"""<b>PAScual</b> v %s
							<p>	
							<p>PAScual and PAScualGUI
							<p>by Carlos Pascual-Izarra carlos.pascual-izarra@csiro.au  2007
							
						    <p>Positron Annihilation Spectroscopy data analysis
						    <p>Copyright (C) 2007  Carlos Pascual-Izarra <carlos.pascual-izarra@csiro.au>
						
						    <p>This program is free software: you can redistribute it and/or modify
						    it under the terms of the GNU General Public License as published by
						    the Free Software Foundation, either 
						    <a href='http://www.gnu.org/licenses/old-licenses/gpl-2.0.html'> version 2</a> 
						    of the License, or (at your option) any <a href='http://www.gnu.org/licenses/gpl.html'>later version</a>.
						
						    <p>This program is distributed in the hope that it will be useful,
						    but WITHOUT ANY WARRANTY; without even the implied warranty of
						    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
						    GNU General Public License for more details.
						
						    <p>You should have received a copy of the GNU General Public License
						    along with this program.  If not, see <a href='http://www.gnu.org/licenses/'> http://www.gnu.org/licenses/</a>
						    
						    <p><b>Note:</b> Regardless of what version of the license you choose for PAScual, 
						    you may still be subject to the conditions of the licenses of the libraries
						    from PAScual. For example, note that if you use the GPLv2-only version of TrollTech QT,
						    you may not have other option than to accept the GPLv2 for PAScual as well.	
						    
						    <p><b>Important:</b> If you use PAScual for your research, please cite:
						    <p>%s
							""" % (__version__,__citation__))

			
		
#	def getselectedkeys(self):
#		if self.selectedChanged: 
#			self.selected=[unicode(item.text()) for item in self.listWidget.selectedItems()]
#			self.selectedChanged=False
#		if len(self.selected)==0: 
#			QMessageBox.warning(self, "Empty selection"," You must select at least one spectrum")
#			return None
#		else: return self.selected


if __name__ == "__main__":
	app = QApplication(sys.argv)
	app.setOrganizationName("CSIRO")
	app.setOrganizationDomain("csiro.au")
	app.setApplicationName("PAScual")
#	app.setWindowIcon(QIcon(":/icon.png"))

	form = PAScualGUI()
	form.show()
	from PAScual import *
	QObject.connect(emitter,SIGNAL("initCommandPBar(int,int)"), form.commandPBar.setRange)
	QObject.connect(emitter,SIGNAL("commandPBarValue(int)"), form.commandPBar,SLOT("setValue(int)"))
	QObject.connect(emitter,SIGNAL("teeOutput"), form.outputTE.insertPlainText)
	abort.abortRequested=form.fitter.isStopped  #reassign the  abortRequested() method from the abort object defined in PAScual
	sys.exit(app.exec_())
