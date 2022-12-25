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


# set names for column numbers
_ncolumns = 2
[CMD, ARGS] = list(range(_ncolumns))
knowncommands = ["END", "LOCAL", "SA", "BI", "LOG", "LOAD", "SAVE"]


class command(object):
    def __init__(self, cmd="", args=""):
        self.cmd = str(cmd).strip().upper()
        self.args = str(args)
        if self.cmd not in knowncommands:
            raise KeyError("Unknown fitting command (%s)" % cmd)


# Commands Table Model
class CommandTableModel(Qt.QAbstractTableModel):
    def __init__(self, commandlist=[], argslist=None):
        super(CommandTableModel, self).__init__()
        self.loadData(commandlist, argslist)
        self.ncolumns = _ncolumns

    def loadData(self, commandlist, argslist=None):
        """commands must be a list of strings! (not a string)"""
        if argslist is None:
            argslist = [""] * len(commandlist)
        if len(commandlist) != len(argslist):
            raise ValueError(
                "CommandTableModel.loadData: commands and args must be the same len"
            )
        self.beginResetModel()
        self.commands = [command(c, a) for c, a in zip(commandlist, argslist)]
        self.endResetModel()

    def dumpData(self):
        # 		for c in self.commands: print 'DEBUG:',c.cmd
        return copy.deepcopy(self.commands)

    def rowCount(self, index=Qt.QModelIndex()):
        return len(self.commands)

    def columnCount(self, index=Qt.QModelIndex()):
        return self.ncolumns

    def data(self, index, role=Qt.Qt.DisplayRole):
        if not index.isValid() or not (0 <= index.row() < self.rowCount()):
            return None
        row = index.row()
        column = index.column()
        # Display Role
        if role == Qt.Qt.DisplayRole:
            if column == CMD:
                return self.commands[row].cmd
            elif column == ARGS:
                return self.commands[row].args
        # Alignment
        # 		elif role == Qt.Qt.TextAlignmentRole:
        # 			return int(Qt.Qt.AlignHCenter|Qt.Qt.AlignVCenter)
        # Background Color
        elif role == Qt.Qt.TextColorRole:
            if column == ARGS:
                return Qt.QColor(Qt.Qt.darkGray)
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
            if section == CMD:
                return "Command"
            elif section == ARGS:
                return "Args"
            return None
        else:
            return int(section + 1)

    def flags(self, index):  # use this to set the editable flag when fix is selected
        if not index.isValid():
            return Qt.Qt.ItemIsEnabled
        return Qt.Qt.ItemFlags(Qt.Qt.ItemIsEnabled | Qt.Qt.ItemIsEditable)

    def setData(self, index, value=None, role=Qt.Qt.EditRole):
        if index.isValid() and (0 <= index.row() < self.rowCount()):
            row = index.row()
            column = index.column()
            value = str(value)
            if column == CMD:
                self.commands[row].cmd = value
                if value == "END":
                    self.removeRows(row + 1, rows=self.rowCount() - row)
                elif row == (self.rowCount() - 1):
                    self.insertRows(position=self.rowCount(), rows=1)
                self.setData(self.index(row, ARGS), value="")  # clear the args
            elif column == ARGS:
                self.commands[row].args = value
            self.dataChanged.emit(index, index)
            return True
        return False

    def insertRows(self, position=None, rows=1, index=Qt.QModelIndex()):
        self.beginInsertRows(Qt.QModelIndex(), position, position + rows - 1)
        for row in range(rows):
            self.commands.insert(position + row, command("END"))
        self.endInsertRows()
        return True

    def removeRows(self, position, rows=1, index=Qt.QModelIndex()):
        self.beginRemoveRows(Qt.QModelIndex(), position, position + rows - 1)
        self.commands = self.commands[:position] + self.commands[position + rows :]
        self.endRemoveRows()
        self.beginResetModel()
        self.endResetModel()
        return True


class commandDelegate(Qt.QItemDelegate):
    def __init__(self, parent=None):
        super(commandDelegate, self).__init__(parent)

    def createEditor(self, parent, option, index):
        if index.column() == CMD:
            combobox = Qt.QComboBox(parent)
            combobox.addItems(knowncommands)
            return combobox
        else:
            return Qt.QItemDelegate.createEditor(self, parent, option, index)

    def setEditorData(self, editor, index):
        text = index.model().data(index, Qt.Qt.DisplayRole)
        if index.column() == CMD:
            i = editor.findText(text)
            if i == -1:
                i = 0
            editor.setCurrentIndex(i)
        else:
            Qt.QItemDelegate.setEditorData(self, editor, index)

    def setModelData(self, editor, model, index):
        if index.column() == CMD:
            model.setData(index, editor.currentText())
        else:
            Qt.QItemDelegate.setModelData(self, editor, model, index)


class demo(Qt.QDialog):
    def __init__(self, parent=None):
        super(demo, self).__init__(parent)
        # generate fake commands
        commands = ["LOCAL", "SA", "BI", "LOG", "LOAD", "SAVE"]
        self.table = Qt.QTableView(self)
        self.model = CommandTableModel(commands)
        self.table.setModel(self.model)
        self.table.setItemDelegate(commandDelegate(self))

        self.posSB = Qt.QSpinBox()
        self.newSB = Qt.QSpinBox()
        self.addBT = Qt.QPushButton("Add")
        self.remBT = Qt.QPushButton("Rem")
        self.dataBT = Qt.QPushButton("Data")
        self.allBT = Qt.QPushButton("Check All")

        mainLayout = Qt.QGridLayout()
        mainLayout.addWidget(self.table, 0, 0, 1, 2)
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
        # 		Qt.QObject.connect(self.allBT,SIGNAL("clicked()"),self.model.checkAll)
        self.table.resizeColumnsToContents()
        # 		self.tree.resizeColumnsToContents()
        self.table.setShowGrid(False)
        self.table.setSelectionBehavior(Qt.QAbstractItemView.SelectRows)

    def onAdd(self):
        self.model.insertRows(position=self.posSB.value(), rows=self.newSB.value())

    def onRem(self):
        self.model.removeRows(position=self.posSB.value(), rows=self.newSB.value())

    def onData(self):
        cmds = self.model.dumpData()
        for c in cmds:
            print(c.cmd, c.args)


if __name__ == "__main__":
    app = Qt.QApplication(sys.argv)
    form = demo()
    # 	form.resize(800, 400)
    form.show()
    sys.exit(app.exec())
