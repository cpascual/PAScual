'''
	This file is part of PAScual.
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
'''

from qwt.qt.QtCore import *
from qwt.qt.QtGui import *
from qt_filedlg import getOpenFileName, getSaveFileName

from ui import UILoadable

class Options(object):
    def __init__(self):
        # variables and default values
        self.optlist = ['LOCAL_maxUnbound',
                        'SA_minaccratio', 'SA_tol', 'SA_stopT',
                        'SA_maxiter', 'SA_meltratio', 'SA_direct',
                        'BI_stab', 'BI_length', 'BI_report',
                        'BI_savehist', 'BI_histFile',
                        'workDirectory',
                        'manualFile',
                        'seed',
                        'warning_chi2_low', 'warning_chi2_high',
                        'autoWizardOnLoad']
        self.dfltlist = [0,
                         0.0, 0.0, 0.1,
                         0, 0.97, True,
                         5e3, 5e4, 5e2,
                         False, '',
                         str(QDir.currentPath()),
                         str(QDir.currentPath()) + '/html/User Manual.html',
                         12345,
                         0.6,  1.4,
                         True]
        self.reset()

    def reset(self):
        for opt, dflt in zip(self.optlist, self.dfltlist):
            setattr(self, opt, dflt)

    def _pprint(self):
        print str(self)
        for opt, dflt in zip(self.optlist, self.dfltlist):
            v = getattr(self,opt)
            print "\t%s, %s %r (default=%s %r)" % (opt, type(v), v, type(dflt),
                                                   dflt)

@UILoadable
class OptionsDlg(QDialog):
    '''Dialog containing options for PAScual. The options are members of this object.'''

    def __init__(self, parent=None):
        super(OptionsDlg, self).__init__(parent)
        self.loadUi()
        # set validators
        self.BI_lengthLE.setValidator(QDoubleValidator(self))
        self.BI_stabLE.setValidator(QDoubleValidator(self))
        self.BI_reportLE.setValidator(QDoubleValidator(self))
        self.seedLE.setValidator(QIntValidator(self))
        # connections
        self.buttonBox.clicked.connect(self.onclicked)
        self.manualFilePB.clicked.connect(self.onChangeManualFile)
        self.workDirectoryPB.clicked.connect(self.onChangeWorkDirectory)
        self.BI_savehistPB.clicked.connect(self.onChangeHistoryFile)

        # set options
        self.reset()

    def onChangeWorkDirectory(self):
        filename = QFileDialog.getExistingDirectory(self,
                                                    "Select work directory (it must be user-writable)",
                                                    self.workDirectoryLE.text())
        if filename: self.workDirectoryLE.setText(filename)

    def onChangeManualFile(self):
        filename, _ = getOpenFileName(self, "Select User Manual File",
                                     self.manualFileLE.text(),
                                     "(*.html *.htm)")
        if filename:
            self.manualFileLE.setText(filename)

    def onChangeHistoryFile(self):
        filename, _ = getSaveFileName(
            self, "BI history File Selection",
            self.BI_savehistLE.text(),
            "ASCII (*.txt)\nAll (*)",
            QFileDialog.DontConfirmOverwrite | QFileDialog.DontUseNativeDialog
        )
        if filename: self.BI_savehistLE.setText(filename)

    def onclicked(self, button):
        if self.buttonBox.buttonRole(button) == QDialogButtonBox.ResetRole:
            self.reset()

    def reset(self):
        self.setOptions(Options())

    def getOptions(self):
        '''returns an options object filled with values from the dialog'''
        options = Options()
        # LOCAL
        options.LOCAL_maxUnbound = int(self.LOCAL_maxUnboundSB.value())  # Max number of unbound LMA runs between L-BFGS-B optimisations (this only takes place if first LMA is outside bounds)
        # SA
        options.SA_minaccratio = float(self.SA_minaccratioSB.value())  # If the acceptance ratio drps below this value, the SA stops.
        options.SA_tol = float(self.SA_tolSB.value())  # Tolerance for stopping the SA
        options.SA_stopT = float(self.SA_stopTSB.value())  # Stop temperature for SA (put to 0 to disable). (SA_stopT>1 is not recommended)
        options.SA_maxiter = int(self.SA_maxiterSB.value())  # Max number of iterations in the SimAnn fit
        options.SA_meltratio = float(self.SA_meltratioSB.value())  # The "melting" phase of the SA will stop when this acceptance ratio is reached
        options.SA_direct = bool(self.SA_directCB.isChecked())  # Whether to use the direct mode in NNRLA for SA (asymetrical transit prob).
        # BI
        options.BI_stab = float(self.BI_stabLE.text()) # This many steps (multiplied by the order of the searching space!) of BI will be done and not considered for statistical purposes. Put this to 0 to skip stabilisation.
        options.BI_length = float(self.BI_lengthLE.text())  # This many steps (multiplied by the order of the searching space) will be calculated by BI.
        options.BI_report = float(self.BI_reportLE.text())  # A report will be shown every this steps during BI (put to -1 for no reports). Be Careful: too much reports may slow down the calc.
        # This controls wheter the fitpar history should be saved (=FileName) or not (=False).
        # Caution!: this will increase the RAM requeriments. Approximately by 11Bytes*BI_length*(3+2*NC)^2 , where NC is the number of components!
        options.BI_savehist = bool(self.BI_savehistCB.isChecked())
        options.BI_histFile = str(self.BI_savehistLE.text())
        # PATHS
        options.workDirectory = str(self.workDirectoryLE.text())
        options.manualFile = str(self.manualFileLE.text())
        # MISC
        options.seed = int(self.seedLE.text()) # Seed for pseudorandom generator
        options.warning_chi2_low = float(self.warning_chi2_lowSB.value())
        options.warning_chi2_high = float(self.warning_chi2_highSB.value())
        options.autoWizardOnLoad = bool(self.autoWizardOnLoadCB.isChecked())
        return options

    def setOptions(self, options):
        '''set dialog values from the passed options object'''
        # LOCAL
        self.LOCAL_maxUnboundSB.setValue(int(options.LOCAL_maxUnbound))
        # SA
        self.SA_minaccratioSB.setValue(float(options.SA_minaccratio))
        self.SA_tolSB.setValue(float(options.SA_tol))
        self.SA_stopTSB.setValue(float(options.SA_stopT))
        self.SA_maxiterSB.setValue(int(options.SA_maxiter))
        self.SA_meltratioSB.setValue(float(options.SA_meltratio))
        self.SA_directCB.setChecked(bool(options.SA_direct))
        # BI
        self.BI_stabLE.setText('%g' % float(options.BI_stab))
        self.BI_lengthLE.setText('%g' % float(options.BI_length))
        self.BI_reportLE.setText('%g' % float(options.BI_report))
        self.BI_savehistCB.setChecked(bool(options.BI_savehist))
        self.BI_savehistLE.setText(str(options.BI_histFile))
        # PATHS
        self.workDirectoryLE.setText(str(options.workDirectory))
        self.manualFileLE.setText(str(options.manualFile))
        # MISC
        self.seedLE.setText(str(options.seed))
        self.warning_chi2_lowSB.setValue(float(options.warning_chi2_low))
        self.warning_chi2_highSB.setValue(float(options.warning_chi2_high))
        self.autoWizardOnLoadCB.setChecked(bool(options.autoWizardOnLoad))




if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    form = OptionsDlg(None)
    form.show()
    sys.exit(app.exec_())
