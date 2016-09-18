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

import scipy as S
import sys

from qwt.qt.QtCore import *
from qwt.qt.QtGui import *

from PlotGraphWidget import PALSplot


class ROISelectorDialog(QDialog):
    def __init__(self, parent=None, selected=None, title="ROI",
                 widgetmode=False):
        ''' defines a roi for each selected spectra from a dictionary.
        "selected" is a list of spectra which are to be assigned a ROI
        The selected items are expected to have at least the .exp member defined
        It stores the chosen ROIs for each spectra in a list (self.roilist) in the same order as selected.
        self.roidict[i]==None if there was a problem with the spectrum in selected[i]
        widgetmode can be set to True to use the dialog as a widget
        '''
        super(ROISelectorDialog, self).__init__(parent)
        # 		if selected is None: return
        self.selected = None
        self.widgetmode = widgetmode
        self.refspectrum = None
        # 		self.selected=sorted(selected)

        # initialise widgets
        self.plotarea = PALSplot()

        self.ctrlsGB = QGroupBox("%s Limits" % title)

        refspectrumLabel = QLabel("Re&ference Spectrum:")
        self.refspectrumCB = QComboBox()

        refspectrumLabel.setBuddy(self.refspectrumCB)
        self.cmaxLabel = QLabel("")

        lowerlimLB = QLabel("Lower lim:")
        upperlimLB = QLabel("Upper lim:")
        self.lowerlimSB = QSpinBox()
        self.lowerlimSB.setAccelerated(True)
        self.lowerlimRelCB = QCheckBox("Relative to max")
        self.upperlimSB = QSpinBox()
        self.upperlimSB.setAccelerated(True)
        self.upperlimRelCB = QCheckBox("Relative to max")
        self.buttonBox = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        mainLayout = QVBoxLayout()

        refLayout = QHBoxLayout()
        refLayout.addWidget(refspectrumLabel)
        refLayout.addWidget(self.refspectrumCB)
        refLayout.addWidget(self.cmaxLabel)
        refLayout.addStretch()

        self.ctrlsLayout = QGridLayout()
        self.ctrlsLayout.addLayout(refLayout, 0, 0, 1, 7)
        self.ctrlsLayout.addWidget(lowerlimLB, 1, 0)
        self.ctrlsLayout.addWidget(self.lowerlimSB, 1, 1)
        self.ctrlsLayout.addWidget(self.lowerlimRelCB, 1, 2)
        self.ctrlsLayout.setColumnStretch(3, 1)
        self.ctrlsLayout.addWidget(upperlimLB, 1, 4)
        self.ctrlsLayout.addWidget(self.upperlimSB, 1, 5)
        self.ctrlsLayout.addWidget(self.upperlimRelCB, 1, 6)
        self.ctrlsGB.setLayout(self.ctrlsLayout)

        mainLayout.addWidget(self.plotarea)
        mainLayout.addWidget(self.ctrlsGB)
        mainLayout.addWidget(self.buttonBox)
        self.setLayout(mainLayout)
        self.setWindowTitle("%s Selection" % title)

        self.resetSelected(selected)

        # Connect signals to slots:
        self.refspectrumCB.currentIndexChanged.connect(self.onrefspectraChange)
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.accepted.connect(self.checkAndApply)
        self.lowerlimRelCB.stateChanged.connect(self.onlowerlimRelChange)
        self.upperlimRelCB.stateChanged.connect(self.onupperlimRelChange)
        # self.plotarea.picker.selected.connect(self.onselection)

        self.selectiondestination = self.upperlimRelCB

    def resetSelected(self, selected):
        if selected is self.selected: return
        self.selected = selected
        self.refspectrumCB.clear()
        self.refspectrumCB.addItems([dp.name for dp in self.selected])
        # Clear prev spectra
        self.plotarea.reset()
        # Show spectra
        for dp in self.selected:
            y = dp.exp
            x = S.arange(y.size)
            self.plotarea.attachCurve(x, y, name=dp.name)
        self.roilist = []
        if selected is not None:
            self.onrefspectraChange(self.refspectrumCB.currentIndex())
            self.lowerlimSB.setMaximum(self.refspectrum.exp.size)
            self.upperlimSB.setMaximum(self.refspectrum.exp.size)
            self.upperlimSB.setValue(self.refspectrum.exp.size)

    def onFocusChanged(self, old, new):
        if new is self.lowerlimSB or new is self.upperlimSB: self.selectiondestination = new

    def onselection(self, point):
        if self.selectiondestination is self.lowerlimSB:
            rel = bool(self.lowerlimRelCB.isChecked())
        elif self.selectiondestination is self.upperlimSB:
            rel = bool(self.upperlimRelCB.isChecked())
        else:
            return
        self.selectiondestination.setValue(point.x() - self.cmax * rel)
        self.selectiondestination.setFocus()
        self.selectiondestination.selectAll()

    def onrefspectraChange(self, itemindex):
        self.refspectrum = self.selected[itemindex]
        self.cmax = self.refspectrum.exp.argmax(0)
        self.cmaxLabel.setText("(the maximum is at channel %i)" % self.cmax)
        if self.lowerlimRelCB.isChecked():
            self.lowerlimSB.setMinimum(-self.cmax)
            self.lowerlimSB.setMaximum(self.refspectrum.exp.size - self.cmax)
        if self.upperlimRelCB.isChecked():
            self.upperlimSB.setMinimum(-self.cmax)
            self.upperlimSB.setMaximum(self.refspectrum.exp.size - self.cmax)

    def onlowerlimRelChange(self, checked):
        if self.refspectrum is None: return
        if checked:
            self.lowerlimSB.setMinimum(-self.cmax)
            self.lowerlimSB.setValue(self.lowerlimSB.value() - self.cmax)
            self.lowerlimSB.setMaximum(self.refspectrum.exp.size - self.cmax)
        else:
            self.lowerlimSB.setMaximum(self.refspectrum.exp.size)
            self.lowerlimSB.setValue(self.lowerlimSB.value() + self.cmax)
            self.lowerlimSB.setMinimum(0)

    def onupperlimRelChange(self, checked):
        if self.refspectrum is None: return
        if checked:
            self.upperlimSB.setMinimum(-self.cmax)
            self.upperlimSB.setValue(self.upperlimSB.value() - self.cmax)
            self.upperlimSB.setMaximum(self.refspectrum.exp.size - self.cmax)
        else:
            self.upperlimSB.setMaximum(self.refspectrum.exp.size)
            self.upperlimSB.setValue(self.upperlimSB.value() + self.cmax)
            self.upperlimSB.setMinimum(0)

    def checkAndApply(self, acceptonexit=True):
        error = ignoreerror = False
        self.roilist = []
        for dp in self.selected:
            self.roimin = self.lowerlimSB.value()
            if self.lowerlimRelCB.isChecked(): self.roimin += dp.exp.argmax(0)
            self.roimax = self.upperlimSB.value()
            if self.upperlimRelCB.isChecked(): self.roimax += dp.exp.argmax(0)
            if self.roimin >= self.roimax:
                error = "Lower limit (=%i) must be less than upper limit (=%i)\n" % (
                self.roimin, self.roimax)
            elif self.roimax > dp.exp.size:
                error = "The upper limit (%i) cannot be larger than the number of channels (%i)" % (
                self.roimax, dp.exp.size)
            else:
                error = False
            if error:
                if ignoreerror:
                    continue  # skip this one if it was previously chosen to ignore all
                else:
                    answer = QMessageBox.warning(self,
                                                 "Input error in %s" % dp.name,
                                                 "Input error in %s :\n %s \nContinue? (skipping this)" % (
                                                 dp.name, error),
                                                 QMessageBox.Yes | QMessageBox.YesToAll | QMessageBox.No)
                    if answer == QMessageBox.No:
                        return False  # stop processing and return without accepting the dialog (and return False)
                    elif answer == QMessageBox.YesToAll:
                        ignoreerror = True  # it won t ask anymore
                self.roilist.append(None)
            else:
                self.roilist.append(S.arange(self.roimin, self.roimax,
                                             dtype='i'))  # put the selected roi in the dict
        if not self.widgetmode: self.accept()  # if no errors (or all errors were skipped) the dialog is accepted
        return True


def make(app=None):
    from PAScual import discretepals
    # fake data
    dp1 = discretepals(expdata=S.arange(1024))
    dp2 = discretepals(name="fake2", expdata=S.arange(1024) * 2)
    dp3 = discretepals(name="fake3", expdata=S.arange(1024) * 3)
    dp4 = discretepals(name="fake4", expdata=S.arange(1024) * 4)
    dp2.exp[22] = 22000
    dp3.exp[33] = 33000
    dp4.exp[44] = 44000
    selected = [dp2, dp3]
    # initialisation
    demo = ROISelectorDialog(selected=selected)
    app.focusChanged.connect(demo.onFocusChanged)
    demo.exec_()
    demo.resetSelected([dp3, dp4])
    demo.exec_()
    print demo.result()
    return demo


# make()


def main(args):
    app = QApplication(args)
    demo = make(app)
    sys.exit(app.exec_())


# main()


# Admire
if __name__ == '__main__':
    main(sys.argv)
