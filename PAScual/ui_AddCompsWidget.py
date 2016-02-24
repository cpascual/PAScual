# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Documents and Settings\pas064\My Documents\src\PAScual-dev\AddCompsWidget.ui'
#
# Created: Wed Jul 02 16:05:17 2008
#      by: PyQt4 UI code generator 4.4.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui


class Ui_AddCompsWidget(object):
    def setupUi(self, AddCompsWidget):
        AddCompsWidget.setObjectName("AddCompsWidget")
        AddCompsWidget.resize(400, 300)
        self.gridLayout = QtGui.QGridLayout(AddCompsWidget)
        self.gridLayout.setObjectName("gridLayout")
        self.addpPsBT = QtGui.QPushButton(AddCompsWidget)
        self.addpPsBT.setObjectName("addpPsBT")
        self.gridLayout.addWidget(self.addpPsBT, 0, 0, 1, 2)
        self.selectionsTE = QtGui.QTextEdit(AddCompsWidget)
        self.selectionsTE.setObjectName("selectionsTE")
        self.gridLayout.addWidget(self.selectionsTE, 0, 2, 5, 1)
        self.addDirectBT = QtGui.QPushButton(AddCompsWidget)
        self.addDirectBT.setObjectName("addDirectBT")
        self.gridLayout.addWidget(self.addDirectBT, 1, 0, 1, 2)
        self.addoPsBT = QtGui.QPushButton(AddCompsWidget)
        self.addoPsBT.setObjectName("addoPsBT")
        self.gridLayout.addWidget(self.addoPsBT, 2, 0, 1, 2)
        self.addCustomBT = QtGui.QPushButton(AddCompsWidget)
        self.addCustomBT.setObjectName("addCustomBT")
        self.gridLayout.addWidget(self.addCustomBT, 3, 0, 1, 1)
        self.customTauSB = QtGui.QSpinBox(AddCompsWidget)
        self.customTauSB.setAccelerated(False)
        self.customTauSB.setMinimum(1)
        self.customTauSB.setMaximum(143000)
        self.customTauSB.setProperty("value", QtCore.QVariant(1000))
        self.customTauSB.setObjectName("customTauSB")
        self.gridLayout.addWidget(self.customTauSB, 3, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(72, 163, QtGui.QSizePolicy.Minimum,
                                       QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 4, 0, 2, 1)
        self.resetBT = QtGui.QPushButton(AddCompsWidget)
        self.resetBT.setObjectName("resetBT")
        self.gridLayout.addWidget(self.resetBT, 5, 2, 1, 1)

        self.retranslateUi(AddCompsWidget)
        QtCore.QObject.connect(self.resetBT, QtCore.SIGNAL("clicked()"),
                               self.selectionsTE.clear)
        QtCore.QMetaObject.connectSlotsByName(AddCompsWidget)

    def retranslateUi(self, AddCompsWidget):
        AddCompsWidget.setWindowTitle(
            QtGui.QApplication.translate("AddCompsWidget", "Form", None,
                                         QtGui.QApplication.UnicodeUTF8))
        self.addpPsBT.setText(
            QtGui.QApplication.translate("AddCompsWidget", "Add pPs (125 ps)",
                                         None, QtGui.QApplication.UnicodeUTF8))
        self.selectionsTE.setToolTip(
            QtGui.QApplication.translate("AddCompsWidget",
                                         "Add components using the buttons on the left or enter them manually.\n"
                                         "Format: lifetime [, min, max]", None,
                                         QtGui.QApplication.UnicodeUTF8))
        self.addDirectBT.setText(QtGui.QApplication.translate("AddCompsWidget",
                                                              "Add Direct (400 ps)",
                                                              None,
                                                              QtGui.QApplication.UnicodeUTF8))
        self.addoPsBT.setText(
            QtGui.QApplication.translate("AddCompsWidget", "Add oPs (2000 ps)",
                                         None, QtGui.QApplication.UnicodeUTF8))
        self.addCustomBT.setText(
            QtGui.QApplication.translate("AddCompsWidget", "Add custom", None,
                                         QtGui.QApplication.UnicodeUTF8))
        self.resetBT.setText(
            QtGui.QApplication.translate("AddCompsWidget", "Reset", None,
                                         QtGui.QApplication.UnicodeUTF8))
