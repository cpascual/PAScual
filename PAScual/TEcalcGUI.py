"""
TEcalcGUI: Graphical User Interface for the Tao Eldrup Calculator
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
import sys
import numpy as np
from PyQt5 import Qt


from .pyTaoEldrup import (
    TE_radius,
    TE_softwall,
    RTE_channel,
    RTE_cube,
    RTE_sheet,
    RTE_softwall,
)

from .ui import UILoadable


@UILoadable()
class TEcalcDialog(Qt.QDialog):
    def __init__(self, parent=None):
        super(TEcalcDialog, self).__init__(parent)
        self.loadUi()
        # 		self.resultsTable.clear()

        # Adding actions
        self.resultsTable.addActions(
            [self.actionCopy_Results_Selection]
        )  # context menu

        # connections
        self.CalculatePB.clicked.connect(self.onCalculate)
        self.actionCopy_Results_Selection.triggered.connect(self.copy_Results_Selection)

    def onCalculate(self):
        """Launches the calculation"""
        # read the input
        tau = (
            str(self.tauTE.toPlainText()).replace(";", " ").split()
        )  # semicolons are also valid separators (apart from blank space)
        T = (
            str(self.TempTE.toPlainText()).replace(";", " ").split()
        )  # semicolons are also valid separators (apart from blank space)
        try:
            tau = np.array([float(elem) for elem in tau], dtype="d")
            T = np.array([float(elem) for elem in T], dtype="d")
        except ValueError:
            Qt.QMessageBox.critical(
                self,
                "Bad input",
                (
                    " The input for the lifetime/temperature must be a number or"
                    + " sequence of numbers"
                ),
            )
            return
        # Check input lengths
        if tau.size == 0:
            Qt.QMessageBox.critical(
                self, "No input", " You must provide at least one lifetime value"
            )
            return
        if self.GeomSphereRB.isChecked():
            T = np.zeros(tau.size)  # Temp is not used in this model
        if T.size == 0:
            Qt.QMessageBox.critical(
                self,
                "No input",
                " You must provide at least one temperature value for this geometry",
            )
            return
        if tau.size > 1 and T.size == 1 and not self.sameTempCB.isChecked():
            answer = Qt.QMessageBox.warning(
                self,
                "Same temperature?",
                "Do you want to use T=%g for all the lifetimes?" % T[0],
                Qt.QMessageBox.Yes | Qt.QMessageBox.Cancel,
            )
            if answer == Qt.QMessageBox.Yes:
                self.sameTempCB.setChecked(True)
            else:
                return
        if self.sameTempCB.isChecked() and self.sameTempCB.isEnabled():
            if T.size == 1:
                T = T[0] * np.ones(tau.size)
            else:
                Qt.QMessageBox.critical(
                    self,
                    "Bad Input",
                    """Give an unique temperature or uncheck the "same temp" option""",
                )
                return

        if T.size != tau.size:
            Qt.QMessageBox.critical(
                self,
                "Bad input",
                (
                    f" The number of lifetimes ({tau.size}) does not match the "
                    + "number of temperatures ({T.size})"
                ),
            )
            return

        # Deal with units (the pyTaoEldrup module works internally with ns and Kelvin
        if self.psRB.isChecked():
            tau *= 1e-3
        if self.celsiusRB.isChecked():
            T += 273.0

        # check for unphysical inputs
        if tau.min() < 0.5 or T.min() < 0 or tau.max() > 142:
            Qt.QMessageBox.critical(
                self,
                "Bad input",
                (
                    " One or more inputs are unphysical \n"
                    + "(check for negative absolute temperatures or lifetimes outside"
                    + " the 1-142 ns range) "
                ),
            )
            return

        # Do the calculations
        size = np.zeros(tau.size)
        badcalcsflag = False
        for i in range(tau.size):
            try:
                if self.GeomSphereRB.isChecked():
                    size[i] = TE_radius(tau[i])
                    if self.softwallsCB.isChecked():
                        size[i] += TE_softwall
                elif self.GeomEquivSphRB.isChecked():
                    a = RTE_cube(tau[i], T[i])
                    # this gives the radius of an sphere with equivalent mean free path
                    # to the calculated cube
                    size[i] = a / 2.0 - TE_softwall
                    if self.softwallsCB.isChecked():
                        size[i] += TE_softwall
                elif self.GeomCubeRB.isChecked():
                    size[i] = RTE_cube(tau[i], T[i])
                    if not self.softwallsCB.isChecked():
                        size[i] -= 2 * RTE_softwall
                elif self.GeomChannelRB.isChecked():
                    size[i] = RTE_channel(tau[i], T[i])
                    if not self.softwallsCB.isChecked():
                        size[i] -= 2 * RTE_softwall
                elif self.GeomSheetRB.isChecked():
                    size[i] = RTE_sheet(tau[i], T[i])
                    if not self.softwallsCB.isChecked():
                        size[i] -= 2 * RTE_softwall
            except Exception:
                badcalcsflag = True

        if size.min() < 0:
            badcalcsflag = True

        if badcalcsflag:
            Qt.QMessageBox.warning(
                self,
                "Possible bad results",
                (
                    " One or more results may not be correct due to bad inversion"
                    + " of the (R)TE formula"
                ),
            )

        # Show the calculation:

        # headers
        self.resultsHeader = 3 * [""]
        if self.psRB.isChecked():
            self.resultsHeader[0] = "Lifetime (ps)"
            tau *= 1000
        else:
            self.resultsHeader[0] = "Lifetime (ns)"
        if self.celsiusRB.isChecked():
            self.resultsHeader[1] = "Temperature (C)"
            T -= 273
        else:
            self.resultsHeader[1] = "Temperature (K)"

        if self.GeomSphereRB.isChecked():
            self.resultsHeader[2] = "TE Sphere radius (nm)"
        elif self.GeomEquivSphRB.isChecked():
            self.resultsHeader[2] = "RTE Equivalent radius (nm)"
        elif self.GeomCubeRB.isChecked():
            self.resultsHeader[2] = "Cube side (nm)"
        elif self.GeomChannelRB.isChecked():
            self.resultsHeader[2] = "Sq. channel side (nm)"
        elif self.GeomSheetRB.isChecked():
            self.resultsHeader[2] = "Sheet spacing (nm)"

        # 		print tau,T,size

        # fill table
        self.resultsTable.clear()
        self.resultsTable.setHorizontalHeaderLabels(self.resultsHeader)
        self.resultsTable.resizeColumnsToContents()
        self.resultsTable.setRowCount(tau.size)
        for i in range(tau.size):
            self.resultsTable.setItem(i, 0, Qt.QTableWidgetItem("%g" % tau[i]))
            self.resultsTable.setItem(i, 1, Qt.QTableWidgetItem("%g" % T[i]))
            self.resultsTable.setItem(i, 2, Qt.QTableWidgetItem("%g" % size[i]))

    def copy_Results_Selection(self):
        """copies the selected results to the clipboard"""
        string = ""
        selecteditems = self.resultsTable.selectedItems()
        for i in range(self.resultsTable.rowCount()):
            emptyrow = True
            for j in range(self.resultsTable.columnCount()):
                if self.resultsTable.item(i, j) in selecteditems:
                    if emptyrow:
                        string += "\n%s" % self.resultsTable.item(i, j).text()
                    else:
                        string += "\t%s" % self.resultsTable.item(i, j).text()
                    emptyrow = False
        Qt.QApplication.clipboard().setText(string.strip())


def main():
    app = Qt.QApplication(sys.argv)
    form = TEcalcDialog()
    form.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
