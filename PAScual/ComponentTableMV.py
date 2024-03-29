"""
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
"""

import sys

from PyQt5 import Qt

from .PAScual import fitpar

# set names for column numbers
_ncolumns = 5
[VAL, FIX, COMMON, MINVAL, MAXVAL] = list(range(_ncolumns))


class componentTableRow(object):
    def __init__(self, tau=None, ity=None, commonTau=False, commonIty=False):
        if tau is None:
            tau = fitpar(minval=1, maxval=142e3, free=True)
        if ity is None:
            ity = fitpar(val=0.1, minval=0, maxval=None, free=True)
        self.tau = tau
        self.ity = ity
        self.tau.common = commonTau
        self.ity.common = commonIty

    def tauority(self, showtau=True):
        if showtau:
            return self.tau
        else:
            return self.ity


# MY model
class PAScomponentsTableModel(Qt.QAbstractTableModel):
    def __init__(self, components=[]):
        super(PAScomponentsTableModel, self).__init__()
        self.components = components
        self.ncolumns = _ncolumns
        self.showtau = True

    def rowCount(self, index=Qt.QModelIndex()):
        return len(self.components)

    def columnCount(self, index=Qt.QModelIndex()):
        return self.ncolumns

    def data(self, index, role=Qt.Qt.DisplayRole):
        if not index.isValid() or not (0 <= index.row() < self.rowCount()):
            return None
        cp = self.components[index.row()]
        fp = cp.tauority(self.showtau)
        column = index.column()
        # Display Role
        if role == Qt.Qt.DisplayRole:
            if column == VAL:
                if self.showtau:
                    return float(fp.val)
                return float(100.0 * fp.val)
            elif column == MINVAL:
                if self.showtau:
                    return float(fp.minval)
                    #  changing ity limits is not allowed => this will always be 0
                return float(100.0 * fp.minval)
            elif column == MAXVAL:
                if self.showtau:
                    return float(fp.maxval)
                return float(100)
                # Showing "100" is just aesthetics. Since the itys are normalised,
                #  the real maxval is None.
        # CheckState Role
        elif role == Qt.Qt.CheckStateRole:
            if column == FIX:
                return not fp.free
            elif column == COMMON:
                return fp.common
        # Alignment
        elif role == Qt.Qt.TextAlignmentRole:
            return int(Qt.Qt.AlignHCenter | Qt.Qt.AlignVCenter)
        # Background Color
        elif role == Qt.Qt.TextColorRole:
            if column == MINVAL or column == MAXVAL:
                if not fp.free:
                    return Qt.QColor(Qt.Qt.gray)
        elif role == Qt.Qt.UserRole:
            return self.components[index.row()]
        return None

    def headerData(self, section, orientation, role=Qt.Qt.DisplayRole):
        if role == Qt.Qt.TextAlignmentRole:
            if orientation == Qt.Qt.Horizontal:
                return int(Qt.Qt.AlignLeft | Qt.Qt.AlignVCenter)
            return int(Qt.Qt.AlignRight | Qt.Qt.AlignVCenter)
        if role != Qt.Qt.DisplayRole:
            return None
        # So this is DisplayRole...
        if orientation == Qt.Qt.Horizontal:
            if section == VAL:
                if self.showtau:
                    return "Value (ps)"
                else:
                    return "Value (%)"
            elif section == FIX:
                return "F"
            elif section == COMMON:
                return "C"
            elif section == MINVAL:
                return "Min"
            elif section == MAXVAL:
                return "Max"
        else:
            if self.showtau:
                return "Tau%i" % (section + 1)
            else:
                return "Ity%i" % (section + 1)

    def flags(self, index):  # use this to set the editable flag when fix is selected
        if not index.isValid():
            return Qt.Qt.ItemIsEnabled
        fp = self.components[index.row()].tauority(self.showtau)
        column = index.column()
        if (column == MINVAL or column == MAXVAL or column == COMMON) and not fp.free:
            return Qt.Qt.ItemFlags()  # disbled!
        if (column == MINVAL or column == MAXVAL) and not self.showtau:
            return Qt.Qt.ItemFlags()  # disbled! (ity limits cannot be changed)
        elif column == FIX or column == COMMON:
            return Qt.Qt.ItemFlags(Qt.Qt.ItemIsEnabled | Qt.Qt.ItemIsUserCheckable)
        return Qt.Qt.ItemFlags(
            Qt.QAbstractTableModel.flags(self, index) | Qt.Qt.ItemIsEditable
        )

    def setData(self, index, value, role=Qt.Qt.EditRole):
        if index.isValid() and (0 <= index.row() < self.rowCount()):
            cp = self.components[index.row()]
            fp = cp.tauority(self.showtau)
            column = index.column()
            if column == VAL:
                fp.val = float(value)
                if not self.showtau:
                    fp.val *= 0.01
            if column == MINVAL:
                fp.minval = float(value)
                if not self.showtau:
                    fp.minval *= 0.01
            if column == MAXVAL:
                fp.maxval = float(value)
                if not self.showtau:
                    fp.maxval *= 0.01
            elif column == FIX:
                fp.free = not fp.free
                for i in [COMMON, MINVAL, MAXVAL]:
                    otherindex = Qt.QAbstractTableModel.index(self, index.row(), i)
                    self.dataChanged.emit(
                        otherindex, otherindex
                    )  # note: a similar thing can be used to update the whole row
            elif column == COMMON:
                fp.common = not fp.common
            # 			print fp.showreport()
            self.dataChanged.emit(index, index)
            return True
        return False

    def insertRows(self, position, rows=1, index=Qt.QModelIndex()):
        self.beginInsertRows(Qt.QModelIndex(), position, position + rows - 1)
        for row in range(rows):
            self.components.insert(position + row, componentTableRow())
        self.endInsertRows()
        return True

    def removeRows(self, position, rows=1, index=Qt.QModelIndex()):
        self.beginRemoveRows(Qt.QModelIndex(), position, position + rows - 1)
        self.components = (
            self.components[:position] + self.components[position + rows :]
        )
        self.endRemoveRows()
        return True


class demo(Qt.QDialog):
    def __init__(self, parent=None):
        super(demo, self).__init__(parent)
        # generate fake components
        components = []
        for i in range(4):
            components.append(componentTableRow())

        self.table = Qt.QTableView(self)
        self.model = PAScomponentsTableModel(components)
        self.table.setModel(self.model)
        # 		self.table.setItemDelegate(mydelegate(self))

        self.posSB = Qt.QSpinBox()
        self.newSB = Qt.QSpinBox()
        self.addBT = Qt.QPushButton("Add")
        self.remBT = Qt.QPushButton("Rem")
        self.dumpBT = Qt.QPushButton("Dump")
        self.tauorityBT = Qt.QPushButton("Swtich to Ity")
        self.tauorityBT.setCheckable(True)

        mainLayout = Qt.QVBoxLayout()
        mainLayout.addWidget(self.table)
        mainLayout.addWidget(self.posSB)
        mainLayout.addWidget(self.newSB)
        mainLayout.addWidget(self.addBT)
        mainLayout.addWidget(self.remBT)
        mainLayout.addWidget(self.dumpBT)
        mainLayout.addWidget(self.tauorityBT)
        self.setLayout(mainLayout)

        self.addBT.clicked.connect(self.onAdd)
        self.remBT.clicked.connect(self.onRem)
        self.tauorityBT.toggled.connect(self.onTItoggled)
        self.dumpBT.clicked.connect(self.showreport)

    def onAdd(self):
        self.model.insertRows(position=self.posSB.value(), rows=self.newSB.value())

    def onRem(self):
        self.model.removeRows(position=self.posSB.value(), rows=self.newSB.value())

    def onTItoggled(self, toggled):
        self.model.showtau = not (toggled)
        self.beginResetModel()
        self.endResetModel()
        if toggled:
            self.tauorityBT.setText("Swtich to Tau")
        else:
            self.tauorityBT.setText("Swtich to Ity")

    def showreport(self):
        print("-------------------------------")
        for cp in self.model.components:
            cp.tau.showreport()
            cp.ity.showreport()
        print("-------------------------------")


if __name__ == "__main__":
    app = Qt.QApplication(sys.argv)
    form = demo()
    form.resize(600, 400)
    form.show()
    sys.exit(app.exec())
