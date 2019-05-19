# -*- coding: utf-8 -*-
"""
	PAScualGUI: Graphical User Interface for PAScual
    PAScual: Positron Annihilation Spectroscopy data analysis
    Copyright (C) 2007  Carlos Pascual-Izarra < cpascual [AT] users.sourceforge.net >

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
"""

# TODO: Add a reverse selection button to the Spectra selection list
# TODO: (General) save queue to file before starting and delete file when finished. Check for existence of old files indicating unfinished calcs and offer resume.
# TODO: (General) implement summary view of sets. A list containing which sets with which spectra each, which fitmode and number of free parameters and names of common parameters
# TODO: (General) (UPDATE: after v9.9 this seems no longer an issue) . Make more robust localmin (this is to PAScual.py) possibly use pre-fit with leastsq and poor convergence criterion, if that fails, go to pre-fit with bruteforce.
# TODO: (General) make more robust SA (this is to PAScual.py) possibly using resets to best fits
# TODO: (General) implement plot from columns in results table
# TODO: (General) Allow set parameters from a row of results table
# TODO: (General) (UPDATE: with the wizard, it is no longer an issue) offset should be calculated automatically if not set (possible warning).
# TODO: (General) (UPDATE: Done by Wizard) same for background (e.g. use last 1% of ROI). Call if ROI is set AND the background is not already assigned
# TODO: (General) (UPDATE: not urgent since Wizard remembers the lims) Implement passing default values to left and right lims in ROISelector. Pass [-5rel,end] for ROI and [ROIright-max(5,0.01*(ROIright-ROIleft)), ROIright] for bgROI
# TODO: (General) add an animation in the status bar indicating "fit in progress" (possibly the pPs.gif)
# TODO: (General) add estimated time for fit (or at least for BI command)
# TODO: (General) Incorporate plothistory.py to the GUI. It could also be used to display ellipses taken from the covariance matrix when no history has been stored
# TODO: (General) make installer?


import platform
import sys

from qwt import qt
from qwt.qt.QtCore import *
from qwt.qt.QtGui import *

if qt.API == 'pyqt':
    # Avoid segfaults on exit when using PyQt4
    import sip
    sip.setdestroyonexit(False)

elif qt.API == 'pyqt5':
    import traceback

    def excepthook(etype, value, tb):
        traceback.print_exception(etype, value, tb)

    sys.excepthook = excepthook


from qt_filedlg import getOpenFileName, getSaveFileName

from PAScual import *
import CommandsTableMV as CMDTMV
import ComponentTableMV as CTMV
import PASCommandProcess as PCP
import PASoptions
import SpecFiles
import SpectraTableMV as STMV
from ui import UILoadable
from PlotGraphWidget import PALSplot, ResPlot
from ROISelectorDlg import ROISelectorDialog
from release import __version__, __homepage__, __citation_html__


defaultFitModesDict = {'LOCAL-connected': ('LOAD', 'LOCAL', 'SAVE'),
                       'LOCAL': ('LOCAL',),
                       'SA': ('SA',),
                       'BI': ('BI',),
                       'SA+BI': ('SA', 'BI',),
                       'SA+LOCAL': ('SA', 'LOCAL',),
                       'LOCAL+BI': ('LOCAL', 'BI',),
                       'SA+LOCAL+BI': ('SA', 'LOCAL', 'BI',),
                       '<user>': ('END',),
                       '*NOFIT*': ('END',),
                       }
defaultFitMode = 'LOCAL-connected'

@UILoadable
class FitparWidget(QWidget):
    """A composite widget that defines fitpars.
    It contains: a label, an "auto" button, a "value" edit box, "fixed" and "common" check boxes, minimum and maximum edits and an Apply button
    """

    def __init__(self, fpkey, parent=None, label="", callbackApply=None,
                 callbackAuto=None):
        """The parameters for initialisation are:
        the fpkey is the key for the __dict__ of the spectrum that will contain this fitpar: e.g. spectrum.__dict__[fpkey]=...
        the label to be shown
        The callback for the apply button (the button is disabled if this is None)
        The callback for the auto button (the button is disabled if this is None)
        Note, the widget is not laid out. Use addtoGridLayout to stack various widgets of this type
        """
        super(FitparWidget, self).__init__(parent)
        self.loadUi()
        self._fpkey = fpkey
        self.label.setText(label)
        self.setMinimumHeight(1.5 * self.LEValue.minimumHeight())
        # connect the Apply and auto buttons to their respective callbacks
        # (or disable them)
        self._callbackApply = callbackApply
        self._callbackAuto = callbackAuto

        if callbackApply is None:
            self.BTApply.setDisabled(True)
        else:
            # it returns self to the callback
            self.BTApply.clicked.connect(self._onApply)
        if callbackAuto is None:
            self.BTAutoFill.setDisabled(True)
        else:
            self.BTAutoFill.clicked.connect(self._onAuto)
        # set up validators
        for widget in [self.LEValue, self.LEMin, self.LEMax]:
            widget.setValidator(QDoubleValidator(self))

    def _onApply(self):
        self._callbackApply(self)

    def _onAuto(self):
        self._callbackAuto(self)

    def addtoGridLayout(self, gridlayout=None, row=None):
        """gridlayout is used for stacking several FitParWidgets,
        row is the row at which we want the widget to be set. If it is None,
        it defaults to the last
        """
        if gridlayout is None: gridlayout = QGridLayout()
        if row is None: row = gridlayout.rowCount()
        for widget, col in zip(
                [self.label, self.BTAutoFill, self.LEValue, self.CBFix,
                 self.CBCommon, self.LEMin, self.LEMax, self.BTApply],
                range(8)):
            gridlayout.addWidget(widget, row, col)

    def removefromGridLayout(self, gridlayout=None, row=None):
        if gridlayout is None: gridlayout = QGridLayout()
        if row is None: row = gridlayout.rowCount()
        for widget in [self.label, self.BTAutoFill, self.LEValue, self.CBFix,
                       self.CBCommon, self.LEMin, self.LEMax, self.BTApply]:
            gridlayout.removeWidget(widget)
            widget.close()

    def getFitpar(self):
        """returns a fitpar object based on the widgets selections"""
        # TODO: validate input
        name = str(self.label.text()).split('[')[0]
        try:
            val = float(str(self.LEValue.text()))
            free = not self.CBFix.isChecked()
            minval = str(self.LEMin.text())
            maxval = str(self.LEMax.text())
            if len(minval) == 0:
                minval = None
            else:
                minval = float(minval)
            if len(maxval) == 0:
                maxval = None
            else:
                maxval = float(maxval)
        except ValueError:
            return None
        return fitpar(val=val, name=name, minval=minval, maxval=maxval,
                      free=free)

    def showFitpar(self, fp):
        """returns a fitpar object based on the widgets selections"""
        if fp is None:
            self.LEValue.setText('')
            self.LEMin.setText('')
            self.LEMax.setText('')
            self.CBFix.setChecked(False)
            return
        self.LEValue.setText(str(fp.val))
        self.CBFix.setChecked(not (fp.free))
        if fp.minval is None:
            self.LEMin.setText('')
        else:
            self.LEMin.setText(str(fp.minval))
        if fp.maxval is None:
            self.LEMax.setText('')
        else:
            self.LEMax.setText(str(fp.maxval))

    @staticmethod
    def addHeader(gridlayout, row=None):
        if row is None: row = gridlayout.rowCount() - 1
        hdrVal = QLabel("Value")
        hdrFix = QLabel("F")
        hdrCom = QLabel("C")
        hdrMin = QLabel("Min")
        hdrMax = QLabel("Max")
        gridlayout.addWidget(hdrVal, row, 2)
        gridlayout.addWidget(hdrFix, row, 3)
        gridlayout.addWidget(hdrCom, row, 4)
        gridlayout.addWidget(hdrMin, row, 5)
        gridlayout.addWidget(hdrMax, row, 6)

@UILoadable
class PAScualGUI(QMainWindow):

    regenerateSets = pyqtSignal(bool)
    updateParamsView = pyqtSignal(object)

    def __init__(self, parent=None):
        super(PAScualGUI, self).__init__(parent)
        self.loadUi()

        self.tauFPWlist = []
        self.ityFPWlist = []
        self.dirtysets = True
        self.dirtyresults = False
        self.palssetsdict = {}
        self.settings = QSettings()  # This  gets the settings from wherever they are stored (the storage point is plattform dependent)
        # 		self.settings.clear()

        ###add hand-coded widgets and modifications to ui_ widgets here

        # The fitter thread
        self.fitter = PCP.fitter(self)

        # FitparWidgets
        layout1 = QGridLayout()
        FitparWidget.addHeader(layout1)
        self.fwhmFitparWidget = FitparWidget("fwhm", label="FWHM [ps]",
                                             callbackApply=self.applyFitpar,
                                             callbackAuto=None)
        self.fwhmFitparWidget.addtoGridLayout(gridlayout=layout1)
        self.bgFitparWidget = FitparWidget("bg", label="Background [cts]",
                                           callbackApply=self.applyFitpar,
                                           callbackAuto=self.autobackground)
        self.bgFitparWidget.addtoGridLayout(gridlayout=layout1)
        self.c0FitparWidget = FitparWidget("c0", label="Offset [ch]",
                                           callbackApply=self.applyFitpar,
                                           callbackAuto=self.autoc0)
        self.c0FitparWidget.addtoGridLayout(gridlayout=layout1)
        self.FitparFrame.setLayout(layout1)

        # components
        self.compModel = CTMV.PAScomponentsTableModel()
        self.compTable.setModel(self.compModel)
        for c in [CTMV.FIX, CTMV.COMMON]:
            self.compTable.resizeColumnToContents(c)

        # spectraTable
        self.spectraModel = STMV.PASspectraTableModel()
        self.spectraTable.setModel(self.spectraModel)
        self.spectraTable.resizeColumnsToContents()

        # Plot dock
        plotlayout = QVBoxLayout()
        self.pplot = PALSplot()
        plotlayout.addWidget(self.pplot)
        self.plotFrame.setLayout(plotlayout)

        # fitmodes
        self.fitmodesdict = copy.deepcopy(
            defaultFitModesDict)  # global dict storing hardcoded default FitModes
        self.fitModeFileName = str(self.settings.value("fitModeFileName",
                                                       "CustomFitmodes.pck"))
        self.fitmodesdict.update(self.loadCustomFitModes(self.fitModeFileName))
        self.fitModeCB.insertItems(0, sorted(self.fitmodesdict.keys()))
        self.commandsModel = CMDTMV.CommandTableModel()
        self.commandsDelegate = CMDTMV.commandDelegate(self)
        self.commandsTable.setModel(self.commandsModel)
        self.commandsTable.setItemDelegate(self.commandsDelegate)

        # PreviousFits Log
        self.currentOutputKey = None
        self.previousOutputDict = {}
        self.previousOutputTE.hide()

        # Other, misc
        self.optionsDlg = None
        self.saveFilesDlg = None
        self.plotfitDlg = None
        self.LEpsperchannel.setValidator(QDoubleValidator(0, S.inf, 3,
                                                          self))  # add validator to the psperchannel edit
        # 		self.resultsTable.addActions([self.actionCopy_Results_Selection,self.actionSave_results_as]) #context menu
        self.resultsTable.addActions(
            [self.actionCopy_Results_Selection, self.actionPlotFit])
        self.resultslist = []
        self.resultsdplist = []
        self.results_min_ncomp = 0
        self.resultsHeader = []

        # Add connections here
        self.actionLoad_Spectra.triggered.connect(self.loadSpectra)
        self.actionAbout.triggered.connect(self.helpAbout)
        self.actionLicense.triggered.connect(self.showlicense)
        self.actionSum_Spectra.triggered.connect(self.sumspectra)
        self.actionTao_Eldrup_Calculator.triggered.connect(self.launchTEcalc)
        self.actionWhat_s_This.triggered.connect(QWhatsThis.enterWhatsThisMode)
        self.actionPlotFit.triggered.connect(self._onPlotSelectedFit)
        self.actionSimulate_spectrum.triggered.connect(self.createFakeSpectrum)
        self.actionCopy_Results_Selection.triggered.connect(self.copy_Results_Selection)
        self.actionShow_hide_Plot.triggered.connect(self.show_hidePlot)
        self.actionShowSpectraSel.triggered.connect(self.showSpectraList)
        self.actionManual.triggered.connect(self.showManual)
        self.actionSave_Output_as.triggered.connect(self.onSaveOutput_as)
        self.actionParamWizard.triggered.connect(self.onParamWizard)
        self.actionOptions.triggered.connect(self.onOptions)
        self.actionSave_Spectra_as.triggered.connect(self.onSaveSpectra)

        self.spectraTable.doubleClicked.connect(self.onSpectraTableDoubleClick)
        self.spectraTable.selectionModel().selectionChanged.connect(self.onspectraSelectionChanged)
        self.SBoxNcomp.valueChanged[int].connect(self.changeNcomp)
        self.roiPB.clicked.connect(self.setROI)
        self.BTpsperchannel.clicked.connect(self.setpsperchannel)
        self.showtauRB.toggled.connect(self.onShowTauToggled)
        self.spectraModel.selectionChanged.connect(self.changePPlot)
        self.updateParamsView.connect(self.onUpdateParamsView)
        self.selectAllTB.clicked.connect(self.spectraModel.checkAll)
        self.selectNoneTB.clicked.connect(self.spectraModel.uncheckAll)
        self.selectMarkedTB.clicked.connect(self.onSelectMarked)
        self.removeSpectraTB.clicked.connect(self.onRemoveChecked)
        self.applycompsBT.clicked.connect(self.onApplyComps)
        self.applyAllParametersPB.clicked.connect(self.onApplyAllParameters)
        self.resetParametersPB.clicked.connect(self.onResetParameters)
        self.actionRegenerateSets.triggered.connect(self._onRegenerateSetsAction)
        self.tabWidget.currentChanged.connect(self.onTabChanged)
        self.regenerateSets.connect(self.onRegenerateSets)
        self.fitModeCB.currentIndexChanged[str].connect(self.onFitModeCBChange)
        self.applyFitModeBT.clicked.connect(self.assignFitModes)
        self.goFitBT.clicked.connect(self.onGoFit)
        self.stopFitBT.clicked.connect(self.onStopFit)
        self.skipCommandBT.clicked.connect(self.onSkipFit)
        self.fitter.endrun.connect(self.onFitterFinished)
        self.fitter.command_done.connect(self.setPBar.setValue)
        self.commandsModel.dataChanged.connect(self.onFitModeEdit)
        self.hideResultsBT.clicked.connect(self.onHideResults)
        self.showResultsBT.clicked.connect(self.onShowResults)
        self.saveResultsBT.clicked.connect(self.onSaveResults)
        self.resultsTable.doubleClicked.connect(self._onPlotFitIndex)
        self.resultsFileSelectBT.clicked.connect(self.onResultsFileSelectBT)
        self.previousOutputCB.currentIndexChanged[str].connect(self.onPreviousOutputCBChange)
        self.outputFileSelectBT.clicked.connect(self.onOutputFileSelect)
        self.saveOutputBT.clicked.connect(self.onSaveOutput_as)
        self.saveFitmodeBT.clicked.connect(self.saveFitMode)
        self.loadParametersPB.clicked.connect(self.loadParameters)
        self.saveParametersPB.clicked.connect(self.saveParameters)
        self.plotFitBT.clicked.connect(self._onPlotSelectedFit)

        # Restore last session Window state
        size = self.settings.value("MainWindow/Size", QSize(800, 600))
        self.resize(size)
        position = self.settings.value("MainWindow/Position", QPoint(0, 0))
        self.move(position)
        self.restoreState(self.settings.value("MainWindow/State", QByteArray()))
        self.fitModeCB.setCurrentIndex(self.fitModeCB.findText(defaultFitMode))

        # Launch low-priority initializations (to speed up load time)
        QTimer.singleShot(0, self.createParamWizard)  # create the parameters Wizard
        QTimer.singleShot(0, self.loadOptions)  # create the Options dialog
        QTimer.singleShot(0, self.createOpenFilesDlg) # create the OpenFiles dialog

    def notImplementedWarning(self, featurename=None):
        if featurename is None: featurename = 'this function'
        return QMessageBox.warning(self, "Not implemented",
                                   "Sorry, %s is not yet implemented" % featurename)

    def loadOptions(self):
        """create the self.options object from values stored in the settings"""
        self.options = PASoptions.Options()
        for opt, dflt in zip(self.options.optlist, self.options.dfltlist):
            _type = type(dflt)
            v = self.settings.value('Options/' + opt, dflt)
            if _type == bool and not isinstance(v, bool):
                v = (v.lower() == 'true')
            else:
                v = _type(v)  # cast to same type as dflt
            setattr(self.options, opt, v)
        # self.options._pprint()
        S.random.seed(int(self.options.seed))  # Seeding the random generators.

    def createParamWizard(self):
        from ParamWizard import ParamWizard
        self.paramWizard = ParamWizard(None)
        app.focusChanged.connect(self.paramWizard.ROIPage.ROIsel.onFocusChanged)  # manage the focus events (needed for mouse selection in ROI)

    def createOpenFilesDlg(self):
        # General OpenFile Dialog (it is never closed, just hidden)
        self.openFilesDlg = QFileDialog(
            self, "%s - Open spectra" % QApplication.applicationName(),
            "./", ""
        )
        # instantiate file loaders and store them in a dict
        fileloaders = {
            'ASCII': SpecFiles.ASCIIfileloader(
                'ASCII', '*.dat *.txt *.al2 *.chn', 0, 'ASCII without header'),
            'ASCII-custom': SpecFiles.ASCIIfileloader(
                'ASCII-custom', '*', None, 'ASCII with user-selected header',
                'qt', self),
            'LT': SpecFiles.ASCIIfileloader(
                'LT', '*.dat *.txt *.al2 *.chn', 4,
                'ASCII with a 4 rows header'),
            'L80': SpecFiles.ASCIIfileloader(
                'L80', '*.80', 0, 'multicolumn ASCII with no header'),
            'MAESTRO': SpecFiles.MAESTROfileLoader('MAESTRO'),
            'PAScual': SpecFiles.PAScualfileLoader('PAScual')
        }
        fileloaders['ASCII-custom'].needExtraInput = True
        filefilters = ["%s (%s)" % (fileloaders[k].name,
                                     fileloaders[k].filenamefilter
                                     ) for k in sorted(fileloaders.keys())
        ]
        self.openFilesDlg.setFileMode(QFileDialog.ExistingFiles)
        self.openFilesDlg.setViewMode(QFileDialog.Detail)
        self.openFilesDlg.setNameFilters(filefilters)
        self.openFilesDlg.setDirectory(self.options.workDirectory)
        selectedfilter = self.settings.value("openfilefilter",
            fileloaders['ASCII'].name)
        self.openFilesDlg.selectNameFilter(selectedfilter)
        # needed as a workaround to a bug in selectedNameFilter in the linux dialog
        self.openFilesDlg.setOption(self.openFilesDlg.DontUseNativeDialog)

        # Add the fileloaders as a member of the openFilesDlg
        self.openFilesDlg.specFileLoaderDict = fileloaders

    def onOptions(self):
        """Shows the options dialog and saves any changes if accepted"""
        if self.optionsDlg is None:
            # create the dialog if not already done
            self.optionsDlg = PASoptions.OptionsDlg(self)
        # make sure that the Dlg is in sync with the options
        self.optionsDlg.setOptions(self.options)
        # launch the options dialog
        if self.optionsDlg.exec_():
            # get the options from the dialog
            self.options = self.optionsDlg.getOptions()
        else:
            # reset previous options
            self.optionsDlg.setOptions(self.options)
        self.saveOptions()

    def saveOptions(self):
        # store the option as settings
        for opt in self.options.optlist:
            val = getattr(self.options, opt)
            self.settings.setValue("Options/" + opt, val)
        self.settings.sync()

    def copy_Results_Selection(self):
        """copies the selected results to the clipboard"""
        string = ''
        selecteditems = self.resultsTable.selectedItems()
        for i in range(self.resultsTable.rowCount()):
            emptyrow = True
            for j in range(self.resultsTable.columnCount()):
                if self.resultsTable.item(i, j) in selecteditems:
                    if emptyrow:
                        string += '\n%s' % self.resultsTable.item(i, j).text()
                    else:
                        string += '\t%s' % self.resultsTable.item(i, j).text()
                    emptyrow = False
        QApplication.clipboard().setText(string.strip())

    def onResultsFileSelectBT(self):
        filename, _ = getSaveFileName(
            self, "Results File Selection",
            self.options.workDirectory + '/PASresults.txt',
            "ASCII (*.txt)\nAll (*)",
            QFileDialog.DontConfirmOverwrite | QFileDialog.DontUseNativeDialog)
        if filename: self.resultsFileLE.setText(filename)

    def onOutputFileSelect(self):
        ofile, _ = getSaveFileName(
            self, "Output File Selection",
            self.outputFileLE.text(),
            "ASCII (*.txt)\nAll (*)",
            QFileDialog.DontConfirmOverwrite | QFileDialog.DontUseNativeDialog)
        if ofile:
            self.outputFileLE.setText(ofile)
        return ofile

    def onSaveOutput_as(self):
        # Make sure only finished outputs are saved
        if self.outputTE.isVisible():
            QMessageBox.warning(self, "Cannot save unfinished fit",
                                "You can only save the output from finished fits. Output won't be written\n Select a different output from the list.")
            return
        # if a file is not given, prompt the user for a file name
        ofile = self.onOutputFileSelect()
        if not ofile:
            return  # failed to get a valid filename

        # Manage the file
        if not isinstance(ofile, file):
            ofile = str(ofile)
            openmode = 'a'
            if os.path.exists(ofile):
                answer = QMessageBox.question(self, "Append data?",
                                              "'%s' already exists.\nAppend data?\n (Yes for Append. No for Overwrite)" % os.path.basename(
                                                  ofile),
                                              QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
                if answer == QMessageBox.Yes:
                    openmode = 'a'
                elif answer == QMessageBox.No:
                    openmode = 'w'
                else:
                    return
            try:
                ofile = open(ofile, openmode)
            except IOError:
                QMessageBox.warning(self, "Error opening file",
                                    "Error opening file. Output won't be written")
                return
        # Write the output to the file
        print >> ofile, "\n" + str(
            self.previousOutputTE.toPlainText()) + "\n"
        ofile.close()

    def _onPlotSelectedFit(self):
        row = self.resultsTable.currentRow()  # this is -1 if there is no table
        self.plotfit(row)

    def _onPlotFitIndex(self, index):
        row = index.row()
        self.plotfit(row)

    def _onNextPlotFit(self):
        self.plotfit(self.dprow + 1)

    def _onPrevPlotFit(self):
        self.plotfit(self.dprow - 1)

    def plotfit(self, dprow=0, dplist=None):
        """Shows a dialog containing: the spectrum, the fit (with separated components), the residuals and the text report.
		It does this for a list of discretepals objects that can be browsed in order.
		dplist is the list of discretepals objects. dprow is the index of that list that is to be reported."""
        # TODO: This function has grown too much. It should be encapsulated  in a class (suggested name: reportDlg).
        if dplist is None: dplist = self.resultsdplist
        self.dprow = dprow
        if len(dplist) < 1:
            QMessageBox.warning(self, "Nothing to report",
                                """There are no results to report. Do the fits first!""")
            return  # mcheck that the list is not empty
        self.dprow = max(0, min(self.dprow, len(
            dplist) - 1))  # make sure that the row is within limits
        dp = dplist[self.dprow]

        if self.plotfitDlg is None:
            self.plotfitDlg = QDialog(self)
            self.plotfitDlg.resize(600, 600)
            self.plotfitDlg.fitplot = PALSplot()
            self.plotfitDlg.resplot = ResPlot()
            self.plotfitDlg.textTE = QTextEdit()
            self.plotfitDlg.textTE.setReadOnly(True)
            self.plotfitDlg.nextPB = QPushButton(">")
            self.plotfitDlg.nextPB.setToolTip("Next result")
            self.plotfitDlg.prevPB = QPushButton("<")
            self.plotfitDlg.prevPB.setToolTip("Previous result")
            layout2 = QHBoxLayout()
            layout2.addWidget(self.plotfitDlg.prevPB)
            layout2.addWidget(self.plotfitDlg.nextPB)
            self.plotfitDlg.layout = QVBoxLayout()
            self.plotfitDlg.layout.addWidget(self.plotfitDlg.fitplot)
            self.plotfitDlg.layout.addWidget(self.plotfitDlg.resplot)
            self.plotfitDlg.layout.addWidget(self.plotfitDlg.textTE)
            self.plotfitDlg.layout.addLayout(layout2)
            self.plotfitDlg.setLayout(self.plotfitDlg.layout)
            self.plotfitDlg.prevPB.clicked.connect(self._onPrevPlotFit)
            self.plotfitDlg.nextPB.clicked.connect(self._onNextPlotFit)
        else:
            self.plotfitDlg.fitplot.reset()
            self.plotfitDlg.resplot.reset()
            self.plotfitDlg.textTE.clear()
        # Enable/disable the buttons
        self.plotfitDlg.prevPB.setEnabled(self.dprow > 0)
        self.plotfitDlg.nextPB.setEnabled(self.dprow < len(dplist) - 1)
        # Fit of the exp, sim, bg and components
        self.plotfitDlg.fitplot.attachCurve(S.arange(dp.exp.size), dp.exp,
                                            name=dp.name, pen=QPen(
                self.plotfitDlg.fitplot.autocolor.next(), 4), style="Dots")
        self.plotfitDlg.fitplot.attachCurve(dp.roi, dp.sim, name='fit',
                                            pen=QPen(
                                                self.plotfitDlg.fitplot.autocolor.next(),
                                                2))
        self.plotfitDlg.fitplot.attachCurve(dp.roi,
                                            S.ones(dp.sim.size) * dp.bg.val,
                                            name='bkgnd')
        ity = dp.normalizeity()
        for i in xrange(dp.ncomp):
            area = dp.M_dot_a.sum()
            comp = ((dp.exparea - dp.bg.val * S.size(dp.sim)) / area) * dp.M[:,
                                                                        i] * \
                   ity[i]
            self.plotfitDlg.fitplot.attachCurve(dp.roi, comp,
                                                name='Comp%i' % (i + 1))
        # plot of the residuals
        residuals = (dp.sim - dp.exp[dp.roi]) / dp.deltaexp[dp.roi]
        self.plotfitDlg.resplot.attachCurve(dp.roi, residuals, name=dp.name,
                                            pen=QPen(Qt.red, 2))
        self.plotfitDlg.setWindowTitle("%s - Fitted Spectrum '%s'" % (
        QApplication.applicationName(), dp.name))
        self.plotfitDlg.show()
        # show the spectrum report
        self.plotfitDlg.textTE.setPlainText(dp.showreport(silent=True))

    def saveFitCurves(self, globalprefix=''):
        """
		Write the fit data as ASCII tables. For each spectrum, a file
		ended in _fit.dat is created containing the total fit,
		the background, the components and the residuals
		"""

        for dp in self.resultsdplist:
            prefix, _ = os.path.splitext(os.path.basename(dp.name))
            fname = "%s%s_fit.dat" % (globalprefix, prefix)
            fit = S.zeros(
                (dp.roi.size, dp.ncomp + 4))  # ch + fit + bg + comp + res
            header = 'Channel Fit Bkgnd'
            fit[:, 0] = dp.roi
            fit[:, 1] = dp.sim
            fit[:, 2] = S.ones(dp.sim.size) * dp.bg.val
            ity = dp.normalizeity()
            for i in xrange(dp.ncomp):
                header += ' Comp%i' % (i + 1)
                area = dp.M_dot_a.sum()
                fit[:, 3 + i] = ((dp.exparea - dp.bg.val * S.size(
                    dp.sim)) / area) * dp.M[:, i] * ity[i]
            header += ' Res'
            fit[:, -1] = (dp.sim - dp.exp[dp.roi]) / dp.deltaexp[dp.roi]
            S.savetxt(fname, fit, header=header)

    def onHideResults(self):
        indexes = self.resultsColumnsListWidget.selectedIndexes()
        for idx in indexes:
            self.resultsTable.hideColumn(idx.row())
            self.resultsColumnsListWidget.itemFromIndex(idx).setForeground(
                QBrush(Qt.gray))
        #		self.resultsColumnsListWidget.reset()

    def onShowResults(self):
        indexes = self.resultsColumnsListWidget.selectedIndexes()
        for idx in indexes:
            self.resultsTable.showColumn(idx.row())
            self.resultsColumnsListWidget.itemFromIndex(idx).setForeground(
                QBrush(Qt.black))
        #		self.resultsColumnsListWidget.reset()

    def onFitModeEdit(self, *args):
        fmname = '<user>'
        self.fitmodesdict[fmname] = tuple(
            ["%s %s" % (c.cmd, c.args) for c in self.commandsModel.dumpData()])
        self.fitModeCB.setCurrentIndex(self.fitModeCB.findText(fmname))
        self.saveFitmodeBT.setEnabled(True)
        self.assignFitModes()

    def saveFitMode(self):
        fmname = str(
            QInputDialog.getText(self, "Name?", "Name of custom Fit Mode:",
                                 QLineEdit.Normal, "", Qt.Dialog)[0])
        self.fitModeCB.addItem(fmname)
        # copy the <user> entry under a different name and restore the original value of the <user> fit mode
        self.fitmodesdict[fmname] = copy.deepcopy(self.fitmodesdict['<user>'])
        self.fitmodesdict['<user>'] = copy.deepcopy(
            defaultFitModesDict['<user>'])
        pickle.dump(self.fitmodesdict, open(self.fitModeFileName, 'wb'), -1)

    def onFitterFinished(self, completed):
        # I think that it is safe to use the completed variable, since it came via the signal mechanism... But if it causes problems, check this
        if completed:  # If the fitter finished its job (i.e. it was not aborted) update things
            if self.fitter.isRunning():  # extra safety check. Make sure that fitter is not running at this moment
                if not self.fitter.wait(1000):
                    QMessageBox.critical(self, "Race condition",
                                         "Something went wrong. \nThis may be a bug. If you can reproduce it, please report it to the author (REF: RACE1)\nThe fit needs to be stopped and re-started manually",
                                         QMessageBox.Ok)
                    raise RuntimeError(
                        'onFitterFinished: self.fitter is still running!')
                # we know fitter is not running, so we safely access its internal palsset and status
            ps = copy.deepcopy(self.fitter.ps)
            # 			completed=copy.deepcopy(self.fitter.completed) #deepcopy makes little sense here but... who cares?
            # We add the ps to a list for later use
            self.resultslist.append(ps)
            # now we can use our copies to insert data into the summary
            self.dirtyresults = True
            row = self.resultsTable.rowCount()
            for dp in ps.spectralist:
                self.resultsdplist.append(dp)
                self.resultsTable.insertRow(row)
                rowitems = (
                dp.showreport_1row(file=None, min_ncomp=self.results_min_ncomp,
                                   silent=True)).split()
                if (self.options.warning_chi2_low < dp.chi2 / dp.dof < self.options.warning_chi2_high):
                    bgbrush = QBrush(Qt.white)  # is chi2 value ok?
                else:
                    bgbrush = QBrush(
                        Qt.red)  # highlight if chi2 is out of normal values
                for c, s in zip(range(len(rowitems)), rowitems):
                    item = QTableWidgetItem(s)
                    item.setBackground(bgbrush)
                    self.resultsTable.setItem(row, c, item)
                row += 1
            self.resultsTable.resizeColumnsToContents()
        # regardless of it being finished or not, pass to the next in the queue
        self.advanceFitQueue()
        return completed

    @pyqtSlot(str)
    def onFitModeCBChange(self, fitmodename):
        fitmodename = str(fitmodename)
        fitmode = self.fitmodesdict[fitmodename]
        self.commandsModel.loadData(fitmode, None)
        self.commandsTable.resizeColumnsToContents()
        # assign:
        self.assignFitModes()

    def assignFitModes(self):
        commands = self.commandsModel.dumpData()
        if self.selectedSetsOnlyCB.isChecked():  # Assign only to the selected sets if the box is checked
            selectedSets = self.setsTree.selectedItems()
            for item in selectedSets:
                key = str(item.text(0))
                self.palssetsdict[key].commands = commands
        else:  # if the box is not checked, assign the current fitmode to all the sets
            for ps in self.palssetsdict.values(): ps.commands = commands

    def advanceFitQueue(self, key=None):
        if self.fitter.isRunning():  # extra safety check. Make sure that fitter is not running at this moment
            if not self.fitter.wait(1000):  # give it some time to finish
                QMessageBox.critical(self, "Race condition",
                                     "Something went wrong. \nThis may be a bug. If you can reproduce it, please report it to the author (REF: RACE2)\nThe fit needs to be stopped and re-started manually",
                                     QMessageBox.Ok)
                raise RuntimeError(
                    'onFitterFinished: self.fitter is still running!')
            return
        if len(self.fitqueuekeys) == 0:
            self.onStopFit()
            self.totalPBar.setValue(0)
            return
        else:
            if key is None:
                i = 0
            else:
                i = self.fitqueuekeys.index(key)
            # get the palsset
            ps = self.fitqueuedict.pop(self.fitqueuekeys.pop(
                i))  # the key and the ps are removed from the list and dict respectively
            # deal with progressbars
            self.setPBar.reset()
            self.setPBar.setMaximum(len(ps.commands))
            self.totalPBar.setValue(-len(self.fitqueuekeys) - 1)
            # start a new fit
            self.fitter.initialize(ps, self.outputfile, self.options)
            self.fitter.start()
            # Show message in status Bar
            self.statusbar.showMessage("Fitting %s..." % ps.name, 0)

    def generatequeue(self):
        if self.fitter.isRunning():
            print 'DEBUG: cannot regenerate the queue while one fit is running'  # TODO: handle this properly
            return
        # create a filtered version of palssetsdict (remove those which have no commands)
        rejected = {}
        accepted = {}
        for ps in self.palssetsdict.values():
            if len(ps.commands) == 1 and ps.commands[0].cmd.upper() == 'END':
                rejected[ps.name] = ps
            else:
                accepted[ps.name] = ps
        # Build a queue, sorting the keys in the palssetsdict (the queue is a deepcopy!)
        self.fitqueuedict = copy.deepcopy(accepted)  # The queue is a copy!
        self.fitqueuekeys = sorted(
            self.fitqueuedict.keys())  # note: at some point this could be used to implement user defined sorting (by assigning a preffix that affects the sort)
        return accepted, rejected  # returns both dictionaries. IMPORTANT: they contain references to the palssets in palssetsdict, not copies!

    def stopFitter(self, timeout=10000, offerForce=False):
        """Tries to stop the fitter nicely. If offerforce==True, it also offers to send a terminate signal to the fitter"""
        # Ask the fitter thread to stop and wait till it does stop
        self.fitter.stop()
        self.statusbar.showMessage(
            "Giving the Fit %i seconds to finish nicely..." % (timeout / 1000),
            0)
        if self.fitter.wait(timeout):
            self.statusbar.showMessage("Fit stopped", 0)
            return True
        if offerForce:
            answer = QMessageBox.warning(self, "Fit not responding",
                                         """The fit is not responding to the stop request."""
                                         """Your options Are: <ul>"""
                                         """<p><li>To force fit termination (<b>the program may crash!</b>)</li>"""
                                         """<li>To wait till the fit responds (You cannot do more fits till it finishes, but you can save results)</li></ul></p>"""
                                         """<p>Play Russian roulette?  (i.e., force fit termination?)</p>"""
                                         , QMessageBox.Yes | QMessageBox.No)
            if answer == QMessageBox.Yes:
                self.statusbar.showMessage(
                    "Risky business: trying to force the fit to stop...", 0)
                self.fitter.terminate()
                self.regenerateFitter(abort)
                self.statusbar.showMessage("Fit killed!", 0)
                return True
        # If we reach this point is because we failed to stop the fit (although we requested a stop which may succeed at any moment)
        self.statusbar.showMessage("The fit may finish at any moment...", 0)
        return False

    def regenerateFitter(self, abortobject):
        """Restores a the self.fitter object and its connections (use in case of having terminated the fitter thread)
		abortobject is the handler containing the abortRequested() to which we assign the fitter.isStopped()"""
        self.fitter = PCP.fitter(self)
        self.fitter.endrun.connect(self.onFitterFinished)
        self.fitter.connect(self.setPBar.setValue)
        emitter.initCommandPBar.connect(self.commandPBar.setRange)
        emitter.commandPBarValue.connect(self.commandPBar.setValue)
        emitter.teeOutput.connect(self.outputTE.insertPlainText)
        abortobject.abortRequested = self.fitter.isStopped  # reassign the  abortRequested() method from the abort object defined in PAScual

    def onSkipFit(self):
        """Skips the current fit"""
        skipped = self.stopFitter(offerForce=False)
        while not skipped:
            answer = QMessageBox.warning(self, "Fit not responding",
                                         """The fit is not responding to the skip request. Do you want to try to <b>stop</b> the fit?""",
                                         QMessageBox.Yes | QMessageBox.No)
            if answer == QMessageBox.Yes:
                self.onStopFit()
                return
            skipped = self.stopFitter(offerForce=False)
        print "\nCurrent fit skipped\n"

    def onStopFit(self):
        """Stops the current fit"""
        # delete the queue
        self.fitqueuedict = {}
        self.fitqueuekeys = []
        # try to stop the fit
        stopped = self.stopFitter(offerForce=True)
        if stopped:
            # activate the startbutton
            self.goFitBT.setEnabled(True)
            # Copy the current output box to the Previous Fits box and then clear the current one
            if not self.currentOutputKey is None:
                self.previousOutputDict[
                    self.currentOutputKey] = self.outputTE.document().clone()  # store the previous output in the dict
                self.previousOutputCB.insertItem(0,
                                                 self.currentOutputKey)  # put a new entry in the combo box
                self.outputTE.clear()
                self.previousOutputCB.setCurrentIndex(
                    0)  # switch the view to thelast to the last

    def onGoFit(self):
        """launches the fit"""
        # populate the queue (generates self.fitqueuedict )
        self.generatequeue()
        if len(self.fitqueuedict) == 0:
            QMessageBox.information(self, "Nothing to do",
                                    "There are no sets to fit", QMessageBox.Ok)
            return
        # check the common itys for each set in the queue
        for ps in self.fitqueuedict.values():
            answer = None
            if not ps.goodItyErrors():
                answer = QMessageBox.warning(self,
                                             "Estimation of covariance may fail in LOCAL",
                                             "<p>The estimation of uncertainties for <b>intensities</b> in %s may not be good if:</p>"
                                             "<p>a) you use LOCAL minimisation <b>and</b></p>"
                                             "<p>b) some spectra have common intensities, <b>and</b></p>"
                                             "<p>c) not <b>all</b> of the intensities are common for the set."
                                             "<p>Note 1: the uncertainties estimated by the Bayesian Inference algorithm are not affected by this problem</p>"
                                             "<p>Note 2: in any case, the uncertainties given by LOCAL are based on the covariance matrix and should not be blindly trusted (more about this in the help files)</p>"
                                             "<p>(if you choose to ignore, this warning won't be repeated for this fit)<p>" % ps.name
                                             ,
                                             QMessageBox.Ignore | QMessageBox.Cancel)
                break  # regardless of the answer, there is no need to continue checking
        if answer == QMessageBox.Cancel: return  # if the user chose to cancel, do no more.
        # checks before starting
        if self.dirtyresults:
            answer = QMessageBox.question(self, "Unsaved results",
                                          "There are previous unsaved results. \nSave them before continuing?",
                                          QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            if answer == QMessageBox.Yes:
                self.onSaveResults()
            elif answer == QMessageBox.No:
                pass
            else:
                return  # cancel the "goFit"
        # deactivate the startbutton
        self.goFitBT.setEnabled(False)
        # initialise a tee for output
        if self.autosaveOutputCB.isChecked():
            self.outputfile = open(str(self.outputFileLE.text()), 'a')
        else:
            self.outputfile = None
        mytee = tee(sys.__stdout__, self.outputfile)
        mytee.setEmitEnabled(True)
        # Update the current Output key
        self.currentOutputKey = str(time.strftime('%Y/%m/%d %H:%M:%S'))
        # show the current output
        self.previousOutputCB.setCurrentIndex(
            self.previousOutputCB.findText("Current",
                                           Qt.MatchExactly | Qt.MatchCaseSensitive))
        sys.stdout = mytee
        # reset the saved results
        self.resultslist = []
        self.resultsdplist = []
        # reset the saveslots
        self.fitter.saveslot = self.fitter.saveslot_auto = self.fitter.saveslot_user = None
        # Prepare the results table
        self.resultsTable.clear()
        self.resultsTable.setRowCount(0)
        spectra = []
        for ps in self.fitqueuedict.values(): spectra += ps.spectralist
        self.results_min_ncomp = max([ob.ncomp for ob in spectra])
        self.resultsHeader = ["name", "chi2", "autocorr", "Set", "ROImin",
                              "ROImax", "ROIch", "Integral", "FWHM", "dev",
                              "c0", "dev", "bg", "dev"]
        for i in range(1, self.results_min_ncomp + 1): self.resultsHeader += [
            "ity%i" % i, "dev"]
        for i in range(1, self.results_min_ncomp + 1): self.resultsHeader += [
            "tau%i" % i, "dev"]
        self.resultsTable.setColumnCount(len(self.resultsHeader))
        self.resultsTable.setHorizontalHeaderLabels(self.resultsHeader)
        # populate the column list
        self.resultsColumnsListWidget.clear()
        self.resultsColumnsListWidget.addItems(self.resultsHeader)
        # set the initial state of the progress bars
        self.totalPBar.reset()
        self.totalPBar.setRange(-len(self.fitqueuedict), 0)
        self.commandPBar.reset()
        self.setPBar.reset()
        # Print a message to indicate a new calculation
        print 60 * '*'
        print time.asctime()
        print 60 * '*'
        # Start the fit
        self.advanceFitQueue()

    def onPreviousOutputCBChange(self, key):
        """prints the previous output in a pop up window)"""
        key = str(key)
        if key == "All":
            self.previousOutputTE.clear()
            for k in sorted(self.previousOutputDict.keys()):
                self.previousOutputTE.insertPlainText(
                    self.previousOutputDict[k].toPlainText())
            self.outputTE.hide()
            self.previousOutputTE.show()
        elif key == "Current":
            self.previousOutputTE.hide()
            self.outputTE.show()
        else:
            self.previousOutputTE.clear()
            self.previousOutputTE.insertPlainText(
                self.previousOutputDict[key].toPlainText())
            self.outputTE.hide()
            self.previousOutputTE.show()
        # disable the posibility of saving output from current fit
        self.saveOutputBT.setEnabled(not (self.outputTE.isVisible()))

    def loadCustomFitModes(self, file=None):
        try:
            customFitModesdict = pickle.load(open(self.fitModeFileName, 'rb'))
        except IOError:
            #			printwarning("No custom FitModes loaded")
            customFitModesdict = {}
        return customFitModesdict

    def closeEvent(self, event):
        """This event handler receives widget close events"""
        # save current window state before closing
        self.settings.setValue("MainWindow/Size", self.size())
        self.settings.setValue("MainWindow/Position", self.pos())
        self.settings.setValue("MainWindow/State", self.saveState())
        self.settings.setValue("fitModeFileName", self.fitModeFileName)
        self.settings.setValue("openfilefilter", self.openFilesDlg.selectedNameFilter())
        self.saveOptions()

    def onTabChanged(self, tabindex):
        if tabindex == 1: self.regenerateSets.emit(False)

    def _onRegenerateSetsAction(self):
        self.onRegenerateSets(force=True)

    def onRegenerateSets(self, force=False):
        # only regenerate if there is a chance of change (or if we explicitely force it)
        if not self.dirtysets and not force:
            return
        # get a copy of the list of spectra
        temp = self.spectraModel.dumpData()  # note that this is a deepcopy
        # filter the list separating the ready ones from the not-yet-ready
        spectra = []
        failed = []
        for dp in temp:
            realinit = dp.initifready(force=True)
            if realinit:
                spectra.append(dp)
            else:
                failed.append(dp)
        # distribute the ready ones into sets
        palssetslist = distributeinsets(spectra)
        # create a dict containing the sets by their names and the queue list
        self.palssetsdict = {}
        for ps in palssetslist:    self.palssetsdict[ps.name] = ps
        # Populate the sets TreeWidget
        self.setsTree.clear()
        for ps in palssetslist:
            item = QTreeWidgetItem(self.setsTree, [ps.name, str(
                len(ps.spectralist))])
            item.addChildren(
                [QTreeWidgetItem([dp.name]) for dp in ps.spectralist])
        # Show the number of failed (unasigned) spectra
        self.unasignedLE.setText(str(len(failed)))
        # readjust columns in TreeWidget
        self.setsTree.setColumnWidth(0,
                                     max(40, int(0.7 * self.setsTree.width())))
        # assign fitmode to the newly created sets
        self.assignFitModes()
        # mark that the sets are freshly calculated (not dirty)
        self.dirtysets = False

    def onSelectMarked(self):
        indexes = self.spectraTable.selectionModel().selectedIndexes()
        if indexes == []: return
        for idx in indexes:
            if not self.spectraModel.data(idx, Qt.UserRole).selected:
                self.spectraModel.setData(self.spectraModel.index(idx.row(),
                                                                  STMV.SEL)
                                          )

    def onRemoveChecked(self):
        answer = QMessageBox.question(self, "Removal confirmation",
                                      "The checked spectra will be removed from the list.\nProceed?",
                                      QMessageBox.Ok | QMessageBox.Cancel)
        if answer == QMessageBox.Ok:
            self.spectraModel.removeChecked()
        # Maybe the selection changed?
        self.onspectraSelectionChanged()
        # mark that the sets might be dirty now
        self.dirtysets = True
        # signal recalculation of sets
        self.regenerateSets.emit(False)

    def sumspectra(self):
        """Sums the checked spectra and offers to save them. It inserts the sum in the list"""
        # TODO: needs more work on interface
        # Todo: implement Duplatre's suggestion on fitting with non-poisson noise from splitted spectra:
        #	Introduce take into account non-poisson noise
        #	This solves issues with the short lifetime artifacts
        #	split acq in 500k counts spectra.
        #	find stdev of each channel among the chunks
        #	find the ratio of real stdev to poisson error of the average spectrum
        #	apply the ratio to the deltaexp vector when analysing each spectrum.
        # alternatively... (think about this):
        #   take s1,s2,...sn: construct a spectrum with exp=mean(s1.exp, s2.exp,...) and deltaexp=stdev(s1.exp,s2.exp,...) (channel by channel)
        # another possibility:
        #   Fit s1,s2,sn,...them all simultaneously with ALL parameters common putting deltaexp=nonpoissonratio*poisson for each of them
        selected, indexes = self.spectraModel.getselectedspectra()
        if len(selected) < 2:
            QMessageBox.warning(self, "At least 2 spectra needed",
                                """You must select at least 2 spectra for summing""")
            return
        dpsum = copy.deepcopy(selected[0])
        dpsum.name = dpsum.name.rsplit('.', 1)[0] + "_%isum" % len(selected)
        try:
            for dp in selected[1:]:
                dpsum.exp += dp.exp
        except ValueError:
            QMessageBox.warning(self, "Spectra cannot be added ",
                                " When summing spectra, they must have the same number of channels.\n Aborting.""")
            return
        dpsum.initifready(force=True)
        self.savespectrum(dpsum)
        self.spectraModel.insertRows(position=None, rows=1, dps=[dpsum])
        for idx in indexes:
            idx = self.spectraModel.index(idx.row(), STMV.PSPC)
            self.spectraModel.dataChanged.emit(idx, idx)
        return True

    def onSpectraTableDoubleClick(self, index):
        if index.column() == STMV.SEL: return
        self.spectraModel.uncheckAll()
        self.spectraModel.setData(
            self.spectraModel.index(index.row(), STMV.SEL))

    # 		print "DEBUG:", index.row(), index.column()

    def onspectraSelectionChanged(self, a=None, b=None):
        selrows = self.spectraTable.selectionModel().selectedRows()
        nselrows = len(selrows)
        if nselrows == 0:
            self.updateParamsView.emit(discretepals())
        elif nselrows == 1:
            self.updateParamsView.emit(self.spectraModel.data(selrows[0],
                                                              role=Qt.UserRole)
                                       )
        else:
            self.updateParamsView.emit(None)

    def onShowTauToggled(self, checked):
        self.compModel.showtau = checked
        self.compModel.beginResetModel()
        self.compModel.endResetModel()

    def changeNcomp(self, ncomp):
        old = len(self.compModel.components)
        change = ncomp - old
        if change > 0:
            self.compModel.insertRows(old, rows=change)
        else:
            self.compModel.removeRows(ncomp, rows=-change)

    def setpsperchannel(self):
        selected, indexes = self.spectraModel.getselectedspectra()
        if selected == []: return
        for dp in selected:
            if len(str(self.LEpsperchannel.text())) == 0:
                QMessageBox.warning(self, "Invalid input",
                                    " The channel width must be a positive number""")
                return False
            dp.psperchannel = float(self.LEpsperchannel.text())
        for idx in indexes:
            idx = self.spectraModel.index(idx.row(), STMV.PSPC)
            self.spectraModel.dataChanged.emit(idx, idx)
        # mark that the sets might be dirty now
        self.dirtysets = True
        return True

    def onUpdateParamsView(self, dp=None):
        if dp is None:
            return
        self.bgFitparWidget.showFitpar(dp.bg)
        self.c0FitparWidget.showFitpar(dp.c0)
        self.fwhmFitparWidget.showFitpar(dp.fwhm)
        if dp.psperchannel is None:
            self.LEpsperchannel.setText('')
        else:
            self.LEpsperchannel.setText(str(dp.psperchannel))
        if dp.taulist is None:
            self.SBoxNcomp.setValue(0)
            return
        self.SBoxNcomp.setValue(
            len(dp.taulist))  # this puts the right number of comps
        for i in xrange(len(dp.taulist)):
            self.compModel.components[i].tau = copy.deepcopy(dp.taulist[i])
            self.compModel.components[i].ity = copy.deepcopy(dp.itylist[i])
            self.compModel.components[i].tau.common = self.compModel.components[
                i].ity.common = False
        self.compModel.beginResetModel()
        self.compModel.endResetModel()

    # TODO: update what is shown in the fitpars Do this by calling a separate function:
    ##If only one is selected, show the fitpars that are set
    ##If more than one is selected, show only those which are common and mark in a different way those which are different amongst selection
    ##Possibly use a color code for background of the LE's: white for those not set, yellow for those set (and same among selection), magenta for those which have different values among selection
    ##Possibly check if they have common settings and show those

    def setROI(self):
        selected, indexes = self.spectraModel.getselectedspectra()
        if selected == []: return
        ROIselector = ROISelectorDialog(self, selected, "ROI")
        app.focusChanged.connect(ROIselector.onFocusChanged)
        if ROIselector.exec_():
            for dp, bgroi in zip(selected, ROIselector.roilist): dp.roi = bgroi
            self.spectraTable.resizeColumnToContents(STMV.ROI)
        # mark that the sets might be dirty now
        self.dirtysets = True

    def applyFitpar(self, caller, selected=None, indexes=None):
        if indexes is None:
            if not (selected is None): raise ValueError(
                'applyFitpar: Ignoring "selected" because "indexes" were not passed')
            selected, indexes = self.spectraModel.getselectedspectra()
        if selected == []: return False  # if it is empty, then nothing is selected so do nothing
        #		print "DEBUG: Apply:",caller.label.text()
        fp = caller.getFitpar()
        if fp is None:
            QMessageBox.warning(self, "Invalid input",
                                "'Value' must be a number.\n 'Min' and 'Max' must either be numbers or be empty.""")
            return False
        fp.forcelimits()
        for dp in selected:
            if caller.CBCommon.isChecked():
                dp.__dict__[caller._fpkey] = fp
            else:
                dp.__dict__[caller._fpkey] = copy.deepcopy(fp)
        # Send signals notifying the changes
        ncol = self.spectraModel.columnCount()
        for idx in indexes:
            idx1 = self.spectraModel.index(idx.row(), 0)
            idx2 = self.spectraModel.index(idx.row(), ncol)
            self.spectraModel.dataChanged.emit(idx1, idx2)
        #		print "DEBUG:",fp.name, fp.val, fp.minval, fp.maxval, fp.free, type(fp), caller._fpkey
        # mark that the sets might be dirty now
        self.dirtysets = True
        return True

    def onApplyComps(self):
        selected, indexes = self.spectraModel.getselectedspectra()
        if selected == []:
            return False  # if it is empty, then nothing is selected so do nothing
        answer = None
        # check if the components are already set for this spectrum (TODO: possibly suggest to apply only selected components )
        ncomps = self.compModel.rowCount()
        nspect = len(selected)
        applymatrix = S.zeros((nspect, ncomps),
                              dtype='bool')  # The applymatrix is a boolean matrix that says whether to apply a given component to a given spectrum
        for i in range(applymatrix.shape[0]):  # go through rows
            dp = selected[i]
            if dp.taulist is None:
                applymatrix[i,
                :] = True  # Apply all components to this spectrum
                dp.taulist = ncomps * [None]  # wipe taulist for this dp
                dp.itylist = ncomps * [None]
            elif len(dp.taulist) == ncomps:
                applymatrix[i, :] = True  # Apply all (we don't ask)
            elif answer == QMessageBox.YesToAll:
                applymatrix[i, :] = True
                dp.taulist = ncomps * [None]  # wipe taulist for this dp
                dp.itylist = ncomps * [None]
            elif answer == QMessageBox.NoToAll:
                applymatrix[i, :] = False
            else:
                answer = QMessageBox.warning(self,
                                             "Components numbers do not match",
                                             "Spectrum %s has %i components already defined\n Discard them?" % (
                                             dp.name, len(dp.taulist)),
                                             QMessageBox.Yes | QMessageBox.YesToAll | QMessageBox.No | QMessageBox.NoToAll)
                if answer == QMessageBox.Yes or answer == QMessageBox.YesToAll:
                    applymatrix[i, :] = True
                    dp.taulist = ncomps * [None]  # wipe taulist for this dp
                    dp.itylist = ncomps * [None]
                else:
                    applymatrix[i, :] = False
            if len(dp.taulist) == 0: dp.taulist = dp.itylist = None
        # At this point we have an applymatrix and taulist of the correct size. So we can apply the components
        for j in xrange(ncomps):
            cp = self.compModel.components[j]
            # We regenerate the components instead of using the existing fitpar because we want to reinitialize them!
            tau = fitpar(val=cp.tau.val, name='Tau%i' % (j + 1),
                         minval=cp.tau.minval, maxval=cp.tau.maxval,
                         free=cp.tau.free)
            ity = fitpar(val=cp.ity.val, name='Ity%i' % (j + 1),
                         minval=cp.ity.minval, maxval=cp.ity.maxval,
                         free=cp.ity.free)
            for i in xrange(nspect):
                dp = selected[i]
                if applymatrix[i, j]:
                    if not cp.tau.common: tau = copy.deepcopy(
                        tau)  # if they are common, we use the same object. If not, we use a copy
                    if not cp.ity.common: ity = copy.deepcopy(ity)
                    dp.taulist[j], dp.itylist[j] = tau, ity
        # mark that the sets might be dirty now
        self.dirtysets = True
        #		dp.taulist=[c.tau for c in self.compModel.components]
        #		dp.itylist=[c.ity for c in self.compModel.components]
        #		for dp in selected: print "DEBUG: onApplyComps", dp.name,dp.taulist
        # notify of the changes
        for idx in indexes:
            idx = self.spectraModel.index(idx.row(), STMV.COMP)
            self.spectraModel.dataChanged.emit(idx, idx)
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

    def autoc0(self, caller):
        selected, indexes = self.spectraModel.getselectedspectra()
        if selected == []: return
        self.statusbar.showMessage("AutoOffset working...", 0)
        if caller.CBCommon.isChecked():
            answer = QMessageBox.warning(self, "Incompatible input",
                                         str(
                                             "The AutoOffset function is not compatible with a common Offset parameter\n"
                                             "If you continue, the 'common' option will be unchecked."),
                                         QMessageBox.Ok | QMessageBox.Cancel)
            if answer == QMessageBox.Ok:
                caller.CBCommon.setCheckState(Qt.Unchecked)
            else:
                self.statusbar.showMessage("AutoOffset Cancelled", 0)
                return  # abort the autoc0
        nerror = error = ignoreerror = False
        for dp in selected:
            if dp.psperchannel is None:
                error = "The channel width for this spectrum must be defined in order to use AutoOffset\n"
            elif dp.fwhm is None:
                error = "The resolution (FWHM) for this spectrum must be defined in order to use AutoOffset\n"
            else:
                error = False
            if error:
                nerror += 1
                if ignoreerror:
                    continue  # skip this one if it was previously chosen to ignore all
                else:
                    answer = QMessageBox.warning(self,
                                                 "Input error in %s" % dp.name,
                                                 "Input error in %s :\n %s \nContinue? (skipping this)" % (
                                                 dp.name, error),
                                                 QMessageBox.Yes | QMessageBox.YesToAll | QMessageBox.No)
                    if answer == QMessageBox.No:
                        self.statusbar.showMessage("AutoOffset Cancelled", 0)
                        return  # stop processing and return without accepting the dialog
                    elif answer == QMessageBox.YesToAll:
                        ignoreerror = True  # it won t ask anymore
            else:
                val = dp.exp.argmax(0)  # a coarse approx of the time 0 channel
                temp = max(1., dp.fwhm.val * 2. / dp.psperchannel)
                minval = val - temp
                maxval = val + temp
                dp.c0 = fitpar(val=val, name='c0', minval=minval, maxval=maxval,
                               free=not (caller.CBFix.isChecked()))
                dp.c0.forcelimits()
        self.onUpdateParamsView(dp)  # update what is shown
        for idx in indexes:
            idx = self.spectraModel.index(idx.row(), STMV.C0)
            self.spectraModel.dataChanged.emit(idx, idx)
        self.statusbar.showMessage(
            "AutoOffset Finished (with %i warnings)" % nerror, 0)

    def autobackground(self, caller):
        selected, indexes = self.spectraModel.getselectedspectra()
        if selected == []: return
        # Check if the 'common' option is checked
        if caller.CBCommon.isChecked():
            answer = QMessageBox.warning(self, "Incompatible input",
                                         str(
                                             "The Auto Background function is not compatible with a common background parameter\n"
                                             "If you continue, the 'common' option will be unchecked."),
                                         QMessageBox.Ok | QMessageBox.Cancel)
            if answer == QMessageBox.Ok:
                caller.CBCommon.setCheckState(Qt.Unchecked)
            else:
                return  # abort the autobackground
        # launch the dialog in modal mode and execute some code if accepted
        BGselector = ROISelectorDialog(self, selected, "Background")
        app.focusChanged.connect(BGselector.onFocusChanged)
        if BGselector.exec_():
            for dp, bgroi in zip(selected, BGselector.roilist):
                val = dp.exp[bgroi].mean()
                std10 = 10 * max(10, S.sqrt(val), dp.exp[bgroi].std())
                # The bg is directly updated!
                dp.bg = fitpar(val=val, name='Bg(auto)',
                               minval=max(0, val - std10), maxval=val + std10,
                               free=not (caller.CBFix.isChecked()))
                dp.bg.forcelimits()
            # Notify of the changes
            for idx in indexes:
                idx = self.spectraModel.index(idx.row(), STMV.BG)
                self.spectraModel.dataChanged.emit(idx, idx)
            self.onUpdateParamsView(dp)

    def changePPlot(self, dp, index=None, replot=True):
        if dp.selected:
            self.pplot.attachCurve(S.arange(dp.exp.size), dp.exp, name=dp.name)
        else:
            self.pplot.detachCurve(dp.name)
        if replot: self.pplot.replot()

    def loadSpectra(self):
        # Todo: do an inteligent identification of files (LT header present?) possibly also get data from the LT header (psperchannel and fwhm)
        fileNames = []
        self.openFilesDlg.setDirectory(self.options.workDirectory)
        if not self.openFilesDlg.exec_():
            return
        self.options.workDirectory = self.openFilesDlg.directory().path()  # update the working directory
        self.settings.setValue("Options/workDirectory", self.options.workDirectory)  # save the new working directory
        fileNames = [str(item) for item in
                     self.openFilesDlg.selectedFiles()]
        dps = []
        answer = None
        progress = QProgressDialog("Loading Files...", "Abort load", 0,
                                   len(fileNames), self)
        progress.setWindowModality(Qt.WindowModal)
        #		progress.setMinimumDuration(1000)
        ifl = 0
        for fname in fileNames:
            # manage the progress dialog
            ifl += 1
            progress.setValue(ifl)
            app.processEvents()
            if progress.wasCanceled(): break
            # read data
            selectedfilter = str(
                self.openFilesDlg.selectedNameFilter()).split('(')[0].strip()
            fileloader = self.openFilesDlg.specFileLoaderDict[selectedfilter]
            try:
                tempdp = fileloader.getDiscretePals(fname)
                if tempdp is None: expdata = fileloader.expdata(fname)
            except:
                expected = fileloader.name
                QMessageBox.warning(self, "Wrong file format",
                                    "Unexpected format in: %s\n (expected %s format)" % (
                                    os.path.basename(fname), expected))
                # 				raise #uncomment for debug, but comment out for release to avoid the progress dialog to remain after failure in loading
                break
            # find a unique key for this file
            usednames = [dp.name for dp in self.spectraModel.spectra]
            basename_ = basename = os.path.basename(fname)
            i = 1
            while basename in usednames:
                i += 1
                basename = "%s(%i)" % (basename_, i)
            # append the spectrum to the list
            if tempdp is None: tempdp = discretepals(expdata=expdata)
            tempdp.name = basename
            dps.append(copy.deepcopy(tempdp))

        # Make sure the progress dialog is closed (In case the load didn't finish normally)
        progress.done(0)
        # Once (if) we have the list of new spectra, make necessary changes in the GUI
        if len(dps) > 0:
            # Uncheck previously checked spectra
            self.spectraModel.uncheckAll()
            # insert the just created dps in the list
            self.spectraModel.insertRows(position=None, rows=len(dps), dps=dps)
            self.spectraTable.resizeColumnToContents(STMV.NAME)
            # Maybe the "soft" selection changed?
            self.onspectraSelectionChanged()
            # mark that the sets might be dirty now
            self.dirtysets = True
            # signal regeneration of sets
            self.regenerateSets.emit(False)
            self.statusbar.showMessage("Done", 0)
            # Launch Wizard
            if self.options.autoWizardOnLoad:
                self.onParamWizard()

    def savespectrum(self, spectrum, filename=None, columns=1,
                     selectedfilter=None):
        if filename is None:
            if self.saveFilesDlg is None:
                self.saveFilesDlg = QFileDialog(
                    self,
                    "%s - Save spectrum '%s'" % (
                        QApplication.applicationName(), spectrum.name),
                    "./", ""
                )
                fileloadersdict = self.openFilesDlg.specFileLoaderDict
                filefilters = ["%s (%s)" % (
                    fileloadersdict[k].name,
                    fileloadersdict[k].filenamefilter) for k in
                               ['PAScual', 'ASCII', 'LT']
                ]
                # needed as a workaround to a bug in selectedNameFilter in the linux dialog
                self.saveFilesDlg.setOption(QFileDialog.DontUseNativeDialog)
                self.saveFilesDlg.setNameFilters(filefilters)
                self.saveFilesDlg.selectNameFilter(fileloadersdict['PAScual'].name)
            self.saveFilesDlg.setWindowTitle("%s - Save spectrum '%s'" % (
            QApplication.applicationName(), spectrum.name))
            # TODO: horrible hack to deselect previously selected files. Any alternative?
            self.saveFilesDlg.setDirectory(self.options.workDirectory + ' ')
            self.saveFilesDlg.selectFile(
                spectrum.name.split('.', 1)[0] + '.ps1')
            # re-select filter to make sure that the extensions is the appropriate
            self.saveFilesDlg.selectNameFilter(self.saveFilesDlg.selectedNameFilter())
            self.saveFilesDlg.setAcceptMode(QFileDialog.AcceptSave)
            self.saveFilesDlg.setViewMode(QFileDialog.Detail)
            if not self.saveFilesDlg.exec_():
                return None
            filename = str(self.saveFilesDlg.selectedFiles()[0])
            selectedfilter = str(
                self.saveFilesDlg.selectedNameFilter()).split('(')[0].strip()
        if selectedfilter is None:
            if filename.endswith(".ps1"):
                selectedfilter = "PAScual"
            else:
                selectedfilter = "ASCII"
        try:
            if selectedfilter.startswith("ASCII"):
                spectrum.saveAs_ASCII(filename)
            elif selectedfilter.startswith("LT"):
                spectrum.saveAs_LT(filename)
            elif selectedfilter.startswith("PAScual"):
                # The PAScual format is just a pickled discretepals object!
                pickle.dump(spectrum, open(filename, 'wb'), -1)
            else:
                raise ValueError('Filter not supported')
        except IOError:
            QMessageBox.warning(
                self, "Error saving file",
                "Error saving file. Spectrum won't be written")
            return None
        return filename

    def onSaveSpectra(self):
        """saves all selected spectra"""
        selected, indexes = self.spectraModel.getselectedspectra()
        if selected == []:
            QMessageBox.warning(
                self, "No spectrum selected",
                "You must select (check) the spectra that you want to save")
            return
        for dp in selected:
            self.savespectrum(dp)

    def onSaveResults(self):
        # Manage the file
        ofile = str(self.resultsFileLE.text())
        if not isinstance(ofile, file):
            ofile = str(ofile)
            openmode = 'a'
            if os.path.exists(ofile):
                answer = QMessageBox.question(
                    self, "Append data?",
                    ("The selected results File Exists.\n" +
                     "Append data?\n" +
                     " (Yes for Append. No for Overwrite)"
                     ),
                    QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
                if answer == QMessageBox.Yes:
                    openmode = 'a'
                elif answer == QMessageBox.No:
                    openmode = 'w'
                else:
                    return
            try:
                ofile = open(ofile, openmode)
            except IOError:
                QMessageBox.warning(self, "Error opening file",
                                    "Error opening file. Results won't be written")
                return
        # Check if there are hidden cells
        hidden = 0
        saveall = True
        for i in xrange(self.resultsTable.columnCount()): hidden += int(
            self.resultsTable.isColumnHidden(i))
        if hidden:
            answer = QMessageBox.question(
                self, "Hidden Results",
                "Some results are not shown. \nSave them too?",
                QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            if answer == QMessageBox.Yes:
                saveall = True
            elif answer == QMessageBox.No:
                saveall = False
            else:
                return
        # prompt for a description of the results
        (customdescription, ok) = QInputDialog.getText(self, "Description?",
                                                       "Description:",
                                                       QLineEdit.Normal, "",
                                                       Qt.Dialog)
        # Write the results to the file
        widths = [20, 14, 14, 9, 6, 6, 6, 14, 9, 9, 9, 9, 9,
                  9] + 4 * self.results_min_ncomp * [9]
        print >> ofile, "\n"
        print >> ofile, "# " + time.asctime()
        print >> ofile, "# " + customdescription
        for col in xrange(self.resultsTable.columnCount()):
            if saveall or not self.resultsTable.isColumnHidden(col):
                fmt = "%%%is\t" % widths[col]
                ofile.write(fmt % self.resultsHeader[col])
        for row in xrange(self.resultsTable.rowCount()):
            ofile.write("\n")
            for col in xrange(self.resultsTable.columnCount()):
                if saveall or not self.resultsTable.isColumnHidden(col):
                    fmt = "%%%is\t" % widths[col]
                    ofile.write(
                        fmt % str(self.resultsTable.item(row, col).text()))
        ofile.close()
        self.dirtyresults = False

        # offer saving the fit
        globalpreffix = "%s_" % os.path.splitext(ofile.name)[0]
        self.saveFitCurves(globalpreffix)

    def createFakeSpectrum(self, area=None, roi=S.arange(1024), name=None):
        #		if roi is None: roi=S.arange(1024)
        # get the parameters
        try:
            bg = self.bgFitparWidget.getFitpar()
            c0 = self.c0FitparWidget.getFitpar()
            fwhm = self.fwhmFitparWidget.getFitpar()
            psperchannel = float(self.LEpsperchannel.text())
            taulist = []
            itylist = []
            ncomps = self.compModel.rowCount()
            for j in xrange(ncomps):
                cp = self.compModel.components[j]
                taulist.append(fitpar(val=cp.tau.val, name='Tau%i' % (j + 1),
                                      minval=cp.tau.minval,
                                      maxval=cp.tau.maxval, free=cp.tau.free))
                itylist.append(fitpar(val=cp.ity.val, name='Ity%i' % (j + 1),
                                      minval=cp.ity.minval,
                                      maxval=cp.ity.maxval, free=cp.ity.free))
        except(ValueError):
            QMessageBox.warning(self, "Input error",
                                "Incomplete or bad values for the parameters.\nFill the parameters fields with the desired values\nSimulation aborted")
            self.statusbar.showMessage("Simulation aborted", 0)
            return
        if area is None:
            area, okflag = QInputDialog.getDouble(self, "Area?",
                                                  "Number of counts in simulated spectrum:",
                                                  1e6, 0, 1e99, 3)
            if not okflag:
                self.statusbar.showMessage("Simulation aborted", 0)
                return

            # construct the discretepals
        dp = discretepals(name='fake', expdata=None, roi=roi, taulist=taulist,
                          itylist=itylist, bg=bg, fwhm=fwhm, c0=c0,
                          psperchannel=psperchannel, area=area, fake=True)
        # save it
        self.savespectrum(dp)

    def launchTEcalc(self):
        from TEcalcGUI import TEcalcDialog
        self.TEcalc = TEcalcDialog()
        self.TEcalc.show()

    def show_hidePlot(self):
        self.plotDockWidget.setVisible(not (self.plotDockWidget.isVisible()))

    def showSpectraList(self):
        self.spectraDockWidget.setVisible(
            not (self.spectraDockWidget.isVisible()))

    def onParamWizard(self):
        """Launches the wizard and applies changes afterwards"""
        selected, indexes = self.spectraModel.getselectedspectra()
        if selected == []:
            QMessageBox.warning(self, "No spectrum selected",
                                """No spectrum is selected. The Wizard applies to selected spectra only""")
            return
        # Reset the selected list and launch the wizard
        self.paramWizard.restart()
        self.paramWizard.setSelected(selected)
        try:
            self.paramWizard.restorelast()
        except:
            pass
        if not self.paramWizard.exec_(): return  # if rejected, stop here
        # If the wizard was accepted, retrieve the settings and apply the parameters
        w = self.paramWizard
        # ROI
        for dp, bgroi in zip(selected, w.roilist): dp.roi = bgroi
        self.spectraTable.resizeColumnToContents(STMV.ROI)
        # psperchannel
        self.LEpsperchannel.setText(str(w.psperchannel))
        self.setpsperchannel()
        # FWHM
        self.fwhmFitparWidget.LEValue.setText(str(w.FWHM))
        self.fwhmFitparWidget.BTApply.click()
        # Bg
        for dp, val, std10 in zip(selected, w.bg, w.deltabg):
            dp.bg = fitpar(val=val, name='Bg(auto)',
                           minval=max(0, val - std10), maxval=val + std10,
                           free=not (self.bgFitparWidget.CBFix.isChecked()))
            dp.bg.forcelimits()
        for idx in indexes:
            idx = self.spectraModel.index(idx.row(), STMV.BG)
            self.spectraModel.dataChanged.emit(idx, idx)
        self.onUpdateParamsView(dp)
        # c0
        self.autoc0(self.c0FitparWidget)
        # components
        self.SBoxNcomp.setValue(w.taus.size)
        for dp in selected:  # wipe the taulist and itylist
            dp.taulist = w.taus.size * [None]
            dp.itylist = w.taus.size * [None]
        for j in xrange(w.taus.size):
            cp = self.compModel.components[j]
            # We regenerate the components instead of using the existing fitpar because we want to reinitialize them!
            tau = fitpar(val=w.taus[j], name='Tau%i' % (j + 1),
                         minval=w.mintaus[j], maxval=w.maxtaus[j], free=True)
            ity = fitpar(val=.1, name='Ity%i' % (j + 1), minval=0, maxval=1,
                         free=True)
            for dp in selected:
                tau = copy.deepcopy(tau)
                ity = copy.deepcopy(ity)
                dp.taulist[j], dp.itylist[j] = tau, ity
        # notify of the changes
        for idx in indexes:
            idx = self.spectraModel.index(idx.row(), STMV.COMP)
            self.spectraModel.dataChanged.emit(idx, idx)
        self.compModel.beginResetModel()
        self.compModel.endResetModel()
        # select the last of the checked spectra (so that the parameters are shown)
        self.spectraTable.clearSelection()
        self.spectraTable.selectRow(indexes[-1].row())
        # recalculate sets
        self.dirtysets = True
        self.regenerateSets.emit(False)

    def loadParameters(self):
        """uses a dp to fill the parameters. If no spectra si given, it asks to load a file which is expected to contain a pickled discretepals"""


        filename, _ = getOpenFileName(
            self, "Load parameters from...",
            self.options.workDirectory,
            "(*.par *.ps1)", '',
            QFileDialog.DontUseNativeDialog)
        if filename:
            loader = SpecFiles.PAScualfileLoader()
            dp = loader.getDiscretePals(filename)
            self.spectraTable.clearSelection()
            self.onUpdateParamsView(dp)
            return dp
        return None

    def saveParameters(self):
        filename, _ = getSaveFileName(
            self, "Save parameters in...",
            self.options.workDirectory + '/PASparams.par',
            "Parameters File (*.par)", '',
            QFileDialog.DontUseNativeDialog)

        if filename:
            bg = self.bgFitparWidget.getFitpar()
            c0 = self.c0FitparWidget.getFitpar()
            fwhm = self.fwhmFitparWidget.getFitpar()
            psperchannel = float(self.LEpsperchannel.text())
            taulist = []
            itylist = []
            ncomps = self.compModel.rowCount()
            for j in xrange(ncomps):
                cp = self.compModel.components[j]
                taulist.append(fitpar(val=cp.tau.val, name='Tau%i' % (j + 1),
                                      minval=cp.tau.minval,
                                      maxval=cp.tau.maxval, free=cp.tau.free))
                itylist.append(fitpar(val=cp.ity.val, name='Ity%i' % (j + 1),
                                      minval=cp.ity.minval,
                                      maxval=cp.ity.maxval, free=cp.ity.free))
            # construct the discretepals
            dp = discretepals(name='PARAMETERS', expdata=None, roi=None,
                              taulist=taulist, itylist=itylist, bg=bg,
                              fwhm=fwhm, c0=c0, psperchannel=psperchannel)
            # Save the parameters as a pickled discretepals object
            print 'DEBUG:', filename
            pickle.dump(dp, open(str(filename), 'wb'), -1)
            return dp
        return None

    def showManual(self):
        """Shows the User Manual in a window"""
        onlinecopy = "http://pascual.wiki.sourceforge.net/User+Manual"
        localcopy = "file:" + self.options.manualFile
        self.manualBrowser = QDialog()
        self.manualBrowser.setWindowTitle("PAScual User Manual")
        manualTB = QTextBrowser()
        manualTB.setOpenExternalLinks(True)
        extLinkLabel = QLabel(
            """For the most up-to-date version of the manual, check the <a href="%s">Online User Manual</a>. You can also <a href="%s">open the local copy in your browser.</a>""" % (
            onlinecopy, localcopy))
        extLinkLabel.setOpenExternalLinks(True)
        layout = QVBoxLayout()
        layout.addWidget(manualTB)
        layout.addWidget(extLinkLabel)
        self.manualBrowser.setLayout(layout)
        self.manualBrowser.resize(1000, 400)
        self.manualBrowser.show()
        if os.path.exists(self.options.manualFile):
            manualTB.setSource(QUrl(localcopy))
        else:
            errormessage = """<h1> ERROR: User Manual File not found</h1>
							<p> Check the setting at:</p>
							<p>Tools--&gt;options--&gt;Path--&gt;Manual</p>"""
            manualTB.setText(errormessage)

    def helpAbout(self):
        QMessageBox.about(self, "About PAScual",
                          """<b>PAScual</b> v %s
							<p>Author: Carlos Pascual-Izarra. <cpascual [AT] users.sourceforge.net>
							<p>Home page: <a href='%s'>%s</a>
							<p>Copyright &copy; 2008 All rights reserved.
							<p>See CREDITS.txt for acknowledgements
							<p>
							<p>If you use PAScual for your research, please cite:
							<p>%s
							<p>
							<p>Python %s - Qt %s - PyQt %s on %s""" % (
                              __version__, __homepage__, __homepage__,
                              __citation_html__, platform.python_version(),
                              QT_VERSION_STR, PYQT_VERSION_STR,
                              platform.system()))

    def showlicense(self):
        QMessageBox.about(self, "Licensing terms",
                          """<b>PAScual</b> v %s
							<p>
							<p>PAScual and PAScualGUI
							<p>by Carlos Pascual-Izarra <cpascual [AT] users.sourceforge.net>  2007

						    <p>Positron Annihilation Spectroscopy data analysis
						    <p>Copyright (C) 2007  Carlos Pascual-Izarra < cpascual [AT] users.sourceforge.net >

						    <p>This program is free software: you can redistribute it and/or modify
						    it under the terms of the GNU General Public License as published by
						    the Free Software Foundation, either version 3 of the License, or
						    (at your option) any later version.

						    <p>This program is distributed in the hope that it will be useful,
						    but WITHOUT ANY WARRANTY; without even the implied warranty of
						    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
						    GNU General Public License for more details.

						    <p>You should have received a copy of the GNU General Public License
						    along with this program.  If not, see  <a href='http://www.gnu.org/licenses/'> http://www.gnu.org/licenses/</a>.

						    <p><b>Important:</b> If you use PAScual for your research, please cite:
						    <p>%s
							""" % (__version__, __citation_html__))



def main():
    global app
    app = QApplication(sys.argv)
    app.setOrganizationName("CPI")
    app.setApplicationName("PAScual")
    app.setApplicationVersion(__version__)
    form = PAScualGUI()
    form.show()

    emitter.initCommandPBar.connect(form.commandPBar.setRange)
    emitter.commandPBarValue.connect(form.commandPBar.setValue)
    emitter.teeOutput.connect(form.outputTE.insertPlainText)

    # reassign the  abortRequested() method from the abort object
    # defined in PAScual
    abort.abortRequested = form.fitter.isStopped

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
