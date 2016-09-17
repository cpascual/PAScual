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

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from ui import UILoadable

class Options(object):
    def __init__(self):
        # variables and default values
        self.optlist = ['LOCAL_maxUnbound',
                        'SA_minaccratio', 'SA_tol', 'SA_stopT', 'SA_maxiter',
                        'SA_meltratio', 'SA_direct',
                        'BI_stab', 'BI_length', 'BI_report', 'BI_savehist',
                        'workDirectory', 'manualFile', 'seed',
                        'warning_chi2_low', 'warning_chi2_high',
                        'autoWizardOnLoad']
        self.dfltlist = [0,
                         0.0, 0.0, 0.1, 0, 0.97, True,
                         5e3, 5e4, 5e2, '',
                         unicode(QDir.currentPath()), unicode(
                QDir.currentPath()) + '/html/User Manual.html', 12345, 0.6,
                         1.4, True]
        self.reset()

    def reset(self):
        for opt, dflt in zip(self.optlist, self.dfltlist): setattr(self, opt,
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
        self.manualFilePB.clicked[()].connect(self.onChangeManualFile)
        self.workDirectoryPB.clicked[()].connect(self.onChangeWorkDirectory)
        self.BI_savehistPB.clicked[()].connect(self.onChangeHistoryFile)

        # set options
        self.reset()

    def onChangeWorkDirectory(self):
        filename = QFileDialog.getExistingDirectory(self,
                                                    "Select work directory (it must be user-writable)",
                                                    self.workDirectoryLE.text())
        if filename: self.workDirectoryLE.setText(filename)

    def onChangeManualFile(self):
        filename = QFileDialog.getOpenFileName(self, "Select User Manual File",
                                               self.manualFileLE.text(),
                                               "(*.html *.htm)")
        if filename: self.manualFileLE.setText(filename)

    def onChangeHistoryFile(self):
        filename = QFileDialog.getSaveFileName(self, "BI history File Selection",
                                               self.BI_savehistLE.text(),
                                               "ASCII (*.txt)\nAll (*)",
                                               '',
                                               QFileDialog.DontConfirmOverwrite | QFileDialog.DontUseNativeDialog)
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
        options.LOCAL_maxUnbound = self.LOCAL_maxUnboundSB.value()  # Max number of unbound LMA runs between L-BFGS-B optimisations (this only takes place if first LMA is outside bounds)
        # SA
        options.SA_minaccratio = self.SA_minaccratioSB.value()  # If the acceptance ratio drps below this value, the SA stops.
        options.SA_tol = self.SA_tolSB.value()  # Tolerance for stopping the SA
        options.SA_stopT = self.SA_stopTSB.value()  # Stop temperature for SA (put to 0 to disable). (SA_stopT>1 is not recommended)
        options.SA_maxiter = self.SA_maxiterSB.value()  # Max number of iterations in the SimAnn fit
        options.SA_meltratio = self.SA_meltratioSB.value()  # The "melting" phase of the SA will stop when this acceptance ratio is reached
        options.SA_direct = self.SA_directCB.isChecked()  # Whether to use the direct mode in NNRLA for SA (asymetrical transit prob).
        # BI
        options.BI_stab, ok = self.BI_stabLE.text().toDouble()  # This many steps (multiplied by the order of the searching space!) of BI will be done and not considered for statistical purposes. Put this to 0 to skip stabilisation.
        options.BI_length, ok = self.BI_lengthLE.text().toDouble()  # This many steps (multiplied by the order of the searching space) will be calculated by BI.
        options.BI_report, ok = self.BI_reportLE.text().toDouble()  # A report will be shown every this steps during BI (put to -1 for no reports). Be Careful: too much reports may slow down the calc.
        # This controls wheter the fitpar history should be saved (=FileName) or not (=False).
        # Caution!: this will increase the RAM requeriments. Approximately by 11Bytes*BI_length*(3+2*NC)^2 , where NC is the number of components!
        if self.BI_savehistCB.isChecked():
            options.BI_savehist = unicode(self.BI_savehistLE.text())
        else:
            options.BI_savehist = ''
        # PATHS
        options.workDirectory = unicode(self.workDirectoryLE.text())
        options.manualFile = unicode(self.manualFileLE.text())
        # MISC
        options.seed, ok = self.seedLE.text().toInt()  # Seed for pseudorandom generator
        options.warning_chi2_low = self.warning_chi2_lowSB.value()
        options.warning_chi2_high = self.warning_chi2_highSB.value()
        options.autoWizardOnLoad = self.autoWizardOnLoadCB.isChecked()
        return options

    def setOptions(self, options):
        '''set dialog values from the passed options object'''
        # LOCAL
        self.LOCAL_maxUnboundSB.setValue(options.LOCAL_maxUnbound)
        # SA
        self.SA_minaccratioSB.setValue(options.SA_minaccratio)
        self.SA_tolSB.setValue(options.SA_tol)
        self.SA_stopTSB.setValue(options.SA_stopT)
        self.SA_maxiterSB.setValue(options.SA_maxiter)
        self.SA_meltratioSB.setValue(options.SA_meltratio)
        self.SA_directCB.setChecked(options.SA_direct)
        # BI
        self.BI_stabLE.setText('%g' % options.BI_stab)
        self.BI_lengthLE.setText('%g' % options.BI_length)
        self.BI_reportLE.setText('%g' % options.BI_report)
        if bool(options.BI_savehist):
            self.BI_savehistCB.setChecked(True)
            self.BI_savehistLE.setText(options.BI_savehist)
        else:
            self.BI_savehistCB.setChecked(False)
            self.BI_savehistLE.setText(u'')
        # PATHS
        self.workDirectoryLE.setText(options.workDirectory)
        self.manualFileLE.setText(options.manualFile)
        # MISC
        self.seedLE.setText(unicode(options.seed))
        self.warning_chi2_lowSB.setValue(options.warning_chi2_low)
        self.warning_chi2_highSB.setValue(options.warning_chi2_high)
        self.autoWizardOnLoadCB.setChecked(options.autoWizardOnLoad)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    form = OptionsDlg(None)
    form.show()
    sys.exit(app.exec_())
