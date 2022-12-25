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
import copy
import sys

from PyQt5 import Qt

from .PAScual import discretepals

# set names for column numbers
_ncolumns = 8
[SEL, NAME, ROI, PSPC, FWHM, BG, C0, COMP] = list(range(_ncolumns))


# Spectra Table Model
class PASspectraTableModel(Qt.QAbstractTableModel):

    # this is a custom signal to warn that the 'hard' selection changed
    selectionChanged = Qt.pyqtSignal(object, object)

    def __init__(self, spectra=[]):
        super(PASspectraTableModel, self).__init__()
        self.spectra = spectra
        self.ncolumns = _ncolumns

        self.redbulletIcon = Qt.QIcon("icons:redbullet.png")
        self.greenbulletIcon = Qt.QIcon("icons:greenbullet.png")

    def rowCount(self, index=Qt.QModelIndex()):
        return len(self.spectra)

    def columnCount(self, index=Qt.QModelIndex()):
        return self.ncolumns

    def data(self, index, role=Qt.Qt.DisplayRole):
        if not index.isValid() or not (0 <= index.row() < self.rowCount()):
            return None
        dp = self.spectra[index.row()]
        column = index.column()
        # Display Role
        if role == Qt.Qt.DisplayRole:
            if column == NAME:
                return dp.name
            elif column == ROI:
                if dp.roi is None:
                    return "-"
                else:
                    return int(dp.roi.size)
            elif column == COMP:
                if dp.taulist is None:
                    ncomp = 0
                else:
                    ncomp = len(dp.taulist)
                return ncomp
        # CheckState Role
        elif role == Qt.Qt.CheckStateRole:
            if column == SEL:
                return dp.selected

        elif role == Qt.Qt.DecorationRole:
            if column == PSPC:
                bad = dp.psperchannel is None
            elif column == FWHM:
                bad = dp.fwhm is None
            elif column == C0:
                bad = dp.c0 is None
            elif column == BG:
                bad = dp.bg is None
            else:
                return None
            if bad:
                return self.redbulletIcon
            else:
                return self.greenbulletIcon
        # Alignment
        # 		elif role == Qt.Qt.TextAlignmentRole:
        # 			int(Qt.Qt.AlignHCenter|Qt.Qt.AlignVCenter)
        # Background Color
        elif role == Qt.Qt.TextColorRole:
            if column == NAME:
                if dp.isready():
                    return Qt.QColor(Qt.Qt.darkGreen)
            if column == COMP:
                if dp.taulist is None:
                    return Qt.QColor(Qt.Qt.red)
                elif len(dp.taulist) == 0:
                    return Qt.QColor(Qt.Qt.red)
                else:
                    return Qt.QColor(Qt.Qt.green)
        elif role == Qt.Qt.UserRole:
            return dp
        return None

    def headerData(self, section, orientation, role=Qt.Qt.DisplayRole):
        if role == Qt.Qt.TextAlignmentRole:
            if orientation == Qt.Qt.Horizontal:
                return int(Qt.Qt.AlignLeft | Qt.Qt.AlignVCenter)
            return int(Qt.Qt.AlignRight | Qt.Qt.AlignVCenter)
        # 		elif role == Qt.Qt.CheckStateRole :
        # 			if not orientation == Qt.Qt.Horizontal: return True
        if role != Qt.Qt.DisplayRole:
            return None
        # So this is DisplayRole...
        if orientation == Qt.Qt.Horizontal:
            if section == SEL:
                return "Sel"
            elif section == NAME:
                return "Spectrum Name"
            elif section == ROI:
                return "ROI"
            elif section == PSPC:
                return "CW"
            elif section == C0:
                return "c0"
            elif section == BG:
                return "Bg"
            elif section == FWHM:
                return "R"
            elif section == COMP:
                return "C"
            return None
        else:
            return None

    def flags(self, index):  # use this to set the editable flag when fix is selected
        if not index.isValid():
            return Qt.Qt.ItemIsEnabled
        column = index.column()
        if column == NAME:
            return Qt.Qt.ItemFlags(Qt.QAbstractTableModel.flags(self, index))
        if column == SEL:
            return Qt.Qt.ItemFlags(Qt.Qt.ItemIsEnabled | Qt.Qt.ItemIsUserCheckable)
        return Qt.Qt.ItemFlags(Qt.Qt.ItemIsEnabled)

    def setData(self, index, value=None, role=Qt.Qt.EditRole):
        if index.isValid() and (0 <= index.row() < self.rowCount()):
            dp = self.spectra[index.row()]
            column = index.column()
            if column == SEL:
                dp.selected = not dp.selected
                self.selectionChanged.emit(dp, index)
            self.dataChanged.emit(index, index)
            return True
        return False

    def insertRows(self, position=None, rows=1, index=Qt.QModelIndex(), dps=None):
        if position is None:
            position = self.rowCount()
        self.beginInsertRows(Qt.QModelIndex(), position, position + rows - 1)
        if dps is None:
            dps = []
            for row in range(rows):
                dps.append(discretepals(name="new"))
        for row in range(rows):
            # 			dp=discretepals(name="new")
            self.spectra.insert(position + row, dps[row])
            self.selectionChanged.emit(dps[row], self.index(position + row, SEL))
        self.endInsertRows()
        return True

    def removeRows(self, position, rows=1, index=Qt.QModelIndex()):
        self.beginRemoveRows(Qt.QModelIndex(), position, position + rows - 1)
        self.spectra = self.spectra[:position] + self.spectra[position + rows :]
        self.endRemoveRows()
        return True

    def getselectedspectra(self):
        seldp = []
        seldpi = []
        for r in range(self.rowCount()):
            if self.spectra[r].selected:
                seldp.append(self.spectra[r])
                seldpi.append(self.index(r, NAME))
        return seldp, seldpi

    def _checkAll(self, check):
        if self.spectra == []:
            return
        indexlist = [self.index(i, SEL) for i in range(len(self.spectra))]
        for dp, idx in zip(self.spectra, indexlist):
            if dp.selected != check:
                dp.selected = check
                self.selectionChanged.emit(dp, idx)
        self.dataChanged.emit(indexlist[0], indexlist[-1])

    def checkAll(self):
        self._checkAll(True)

    def uncheckAll(self):
        self._checkAll(False)

    def removeChecked(self):
        temp = []
        for dp in self.spectra:
            if dp.selected:
                dp.selected = False
                self.selectionChanged.emit(dp, None)
            else:
                temp.append(dp)
        self.spectra = temp
        self.beginResetModel()
        self.endResetModel()

    def dumpData(self):
        return copy.deepcopy(self.spectra)

    def loadData(self, data):
        self.spectra = data
        self.beginResetModel()
        self.endResetModel()


# def parent(self, index):
# 		if index.row()%2: return


# 	def getselectedspectraindexes(self):
# 		seldpi=[]
# 		for r in range(self.rowCount()):
# 			if self.spectra[r].selected: seldpi.append(self.index(r,NAME))
# 		return seldpi

# 	#Delegate
# class mydelegate(Qt.QItemDelegate):
# 	def __init__(self, parent=None):
# 		super(mydelegate,self).__init__(parent)
# 	def createEditor(self,parent,option,index):
# 		print 'AAAAAAAAAAA',index.column()
# 		if index.column()==0:
# 			print '!!'
# 			return Qt.QItemDelegate.createEditor(self,parent,option,index)
# 		else:
# 			return Qt.QItemDelegate.createEditor(self,parent,option,index)


class demo(Qt.QDialog):
    def __init__(self, parent=None):
        super(demo, self).__init__(parent)
        # generate fake spectra
        spectra = []
        for i in range(4):
            spectra.append(discretepals(name="spect%i" % i))

        self.table = Qt.QTableView(self)
        self.model = PASspectraTableModel(spectra)
        self.table.setModel(self.model)

        self.tree = Qt.QTreeWidget(self)
        self.tree.setColumnCount(1)
        self.tree.setHeaderLabels(["Name"])
        # 		sets

        # 		self.table.setItemDelegate(mydelegate(self))

        self.posSB = Qt.QSpinBox()
        self.newSB = Qt.QSpinBox()
        self.addBT = Qt.QPushButton("Add")
        self.remBT = Qt.QPushButton("Rem")
        self.dataBT = Qt.QPushButton("Data")
        self.allBT = Qt.QPushButton("Check All")

        mainLayout = Qt.QGridLayout()
        mainLayout.addWidget(self.table, 0, 0)
        mainLayout.addWidget(self.tree, 0, 1)
        mainLayout.addWidget(self.posSB, 1, 0)
        mainLayout.addWidget(self.newSB, 1, 1)
        mainLayout.addWidget(self.addBT, 2, 0)
        mainLayout.addWidget(self.remBT, 2, 1)
        mainLayout.addWidget(self.dataBT, 3, 0)
        mainLayout.addWidget(self.allBT, 3, 1)
        self.setLayout(mainLayout)

        self.addBT.clicked.connect(self.onAdd)
        self.remBT.clicked.connect(self.onRem)
        self.dataBT.clicked.connect(self.onData)
        self.allBT.clicked.connect(self.model.checkAll)
        self.table.resizeColumnsToContents()
        # 		self.tree.resizeColumnsToContents()
        self.table.setShowGrid(False)
        self.table.setSelectionBehavior(Qt.QAbstractItemView.SelectRows)

    def onAdd(self):
        self.model.insertRows(position=self.posSB.value(), rows=self.newSB.value())

    def onRem(self):
        self.model.removeRows(position=self.posSB.value(), rows=self.newSB.value())

    def onData(self):
        s = self.table.selectionModel().selectedRows()
        for idx in s:
            dp = self.model.data(idx, role=Qt.Qt.UserRole)
            print(dp.name)


if __name__ == "__main__":
    app = Qt.QApplication(sys.argv)
    form = demo()
    # 	form.resize(800, 400)
    form.show()
    sys.exit(app.exec())
