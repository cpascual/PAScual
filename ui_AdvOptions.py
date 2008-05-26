# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Documents and Settings\pas064\My Documents\src\PAScual\AdvOptions.ui'
#
# Created: Mon Oct 01 15:29:53 2007
#      by: PyQt4 UI code generator 4.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        Dialog.resize(QtCore.QSize(QtCore.QRect(0,0,400,300).size()).expandedTo(Dialog.minimumSizeHint()))

        self.vboxlayout = QtGui.QVBoxLayout(Dialog)
        self.vboxlayout.setMargin(9)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setObjectName("vboxlayout")

        self.tabWidget = QtGui.QTabWidget(Dialog)
        self.tabWidget.setObjectName("tabWidget")

        self.LocalTab = QtGui.QWidget()
        self.LocalTab.setObjectName("LocalTab")

        self.label_6 = QtGui.QLabel(self.LocalTab)
        self.label_6.setGeometry(QtCore.QRect(10,20,46,14))
        self.label_6.setObjectName("label_6")
        self.tabWidget.addTab(self.LocalTab,"")

        self.SATab = QtGui.QWidget()
        self.SATab.setObjectName("SATab")

        self.gridlayout = QtGui.QGridLayout(self.SATab)
        self.gridlayout.setMargin(9)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")

        self.SA_minaccratioSB = QtGui.QDoubleSpinBox(self.SATab)
        self.SA_minaccratioSB.setAccelerated(True)
        self.SA_minaccratioSB.setMaximum(1.0)
        self.SA_minaccratioSB.setSingleStep(0.01)
        self.SA_minaccratioSB.setObjectName("SA_minaccratioSB")
        self.gridlayout.addWidget(self.SA_minaccratioSB,3,1,1,1)

        self.SA_directCB = QtGui.QCheckBox(self.SATab)
        self.SA_directCB.setObjectName("SA_directCB")
        self.gridlayout.addWidget(self.SA_directCB,5,1,1,1)

        spacerItem = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem,5,2,1,1)

        spacerItem1 = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem1,4,2,1,1)

        spacerItem2 = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem2,3,2,1,1)

        self.SA_meltratioSB = QtGui.QDoubleSpinBox(self.SATab)
        self.SA_meltratioSB.setAccelerated(True)
        self.SA_meltratioSB.setMaximum(1.0)
        self.SA_meltratioSB.setSingleStep(0.01)
        self.SA_meltratioSB.setProperty("value",QtCore.QVariant(0.97))
        self.SA_meltratioSB.setObjectName("SA_meltratioSB")
        self.gridlayout.addWidget(self.SA_meltratioSB,4,1,1,1)

        self.label_5 = QtGui.QLabel(self.SATab)
        self.label_5.setObjectName("label_5")
        self.gridlayout.addWidget(self.label_5,4,0,1,1)

        self.label_3 = QtGui.QLabel(self.SATab)
        self.label_3.setObjectName("label_3")
        self.gridlayout.addWidget(self.label_3,3,0,1,1)

        self.label_4 = QtGui.QLabel(self.SATab)
        self.label_4.setObjectName("label_4")
        self.gridlayout.addWidget(self.label_4,2,0,1,1)

        self.SA_maxiterSB = QtGui.QSpinBox(self.SATab)
        self.SA_maxiterSB.setAccelerated(True)
        self.SA_maxiterSB.setObjectName("SA_maxiterSB")
        self.gridlayout.addWidget(self.SA_maxiterSB,2,1,1,1)

        self.SA_StopTSB = QtGui.QDoubleSpinBox(self.SATab)
        self.SA_StopTSB.setAccelerated(True)
        self.SA_StopTSB.setMaximum(10000000000.0)
        self.SA_StopTSB.setProperty("value",QtCore.QVariant(0.1))
        self.SA_StopTSB.setObjectName("SA_StopTSB")
        self.gridlayout.addWidget(self.SA_StopTSB,1,1,1,1)

        self.SA_tolSB = QtGui.QDoubleSpinBox(self.SATab)
        self.SA_tolSB.setAccelerated(True)
        self.SA_tolSB.setObjectName("SA_tolSB")
        self.gridlayout.addWidget(self.SA_tolSB,0,1,1,1)

        self.label = QtGui.QLabel(self.SATab)
        self.label.setObjectName("label")
        self.gridlayout.addWidget(self.label,0,0,1,1)

        self.label_2 = QtGui.QLabel(self.SATab)
        self.label_2.setObjectName("label_2")
        self.gridlayout.addWidget(self.label_2,1,0,1,1)

        spacerItem3 = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem3,0,2,1,1)

        spacerItem4 = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem4,1,2,1,1)

        spacerItem5 = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem5,2,2,1,1)
        self.tabWidget.addTab(self.SATab,"")

        self.BITab = QtGui.QWidget()
        self.BITab.setObjectName("BITab")
        self.tabWidget.addTab(self.BITab,"")
        self.vboxlayout.addWidget(self.tabWidget)

        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.NoButton|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.vboxlayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.buttonBox,QtCore.SIGNAL("accepted()"),Dialog.accept)
        QtCore.QObject.connect(self.buttonBox,QtCore.SIGNAL("rejected()"),Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Advanced Options", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("Dialog", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.LocalTab), QtGui.QApplication.translate("Dialog", "Local", None, QtGui.QApplication.UnicodeUTF8))
        self.SA_minaccratioSB.setSpecialValueText(QtGui.QApplication.translate("Dialog", "No limit", None, QtGui.QApplication.UnicodeUTF8))
        self.SA_directCB.setText(QtGui.QApplication.translate("Dialog", "Direct?", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("Dialog", "Melting Ratio", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Dialog", "Min Acc Ratio", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("Dialog", "Max Iter", None, QtGui.QApplication.UnicodeUTF8))
        self.SA_maxiterSB.setSpecialValueText(QtGui.QApplication.translate("Dialog", "No limit", None, QtGui.QApplication.UnicodeUTF8))
        self.SA_StopTSB.setSpecialValueText(QtGui.QApplication.translate("Dialog", "No limit", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "Tolerance", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Dialog", "Stop T", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.SATab), QtGui.QApplication.translate("Dialog", "SimAnn", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.BITab), QtGui.QApplication.translate("Dialog", "BI", None, QtGui.QApplication.UnicodeUTF8))

