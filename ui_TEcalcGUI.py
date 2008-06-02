# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Documents and Settings\pas064\My Documents\src\PAScual-dev\TEcalcGUI.ui'
#
# Created: Mon Jun 02 15:00:48 2008
#      by: PyQt4 UI code generator 4.4.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_TEcalcGUI(object):
    def setupUi(self, TEcalcGUI):
        TEcalcGUI.setObjectName("TEcalcGUI")
        TEcalcGUI.resize(487,574)
        icon = QtGui.QIcon()
        icon.addFile(":/Icons/icons/mine/TaoEldrup64x64.png")
        TEcalcGUI.setWindowIcon(icon)
        self.vboxlayout = QtGui.QVBoxLayout(TEcalcGUI)
        self.vboxlayout.setObjectName("vboxlayout")
        self.groupBox_2 = QtGui.QGroupBox(TEcalcGUI)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridlayout = QtGui.QGridLayout(self.groupBox_2)
        self.gridlayout.setObjectName("gridlayout")
        self.frame = QtGui.QFrame(self.groupBox_2)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.vboxlayout1 = QtGui.QVBoxLayout(self.frame)
        self.vboxlayout1.setObjectName("vboxlayout1")
        self.label = QtGui.QLabel(self.frame)
        self.label.setObjectName("label")
        self.vboxlayout1.addWidget(self.label)
        self.nsRB = QtGui.QRadioButton(self.frame)
        self.nsRB.setChecked(True)
        self.nsRB.setObjectName("nsRB")
        self.vboxlayout1.addWidget(self.nsRB)
        self.psRB = QtGui.QRadioButton(self.frame)
        self.psRB.setObjectName("psRB")
        self.vboxlayout1.addWidget(self.psRB)
        self.gridlayout.addWidget(self.frame,0,0,1,1)
        self.frame_3 = QtGui.QFrame(self.groupBox_2)
        self.frame_3.setEnabled(False)
        self.frame_3.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.vboxlayout2 = QtGui.QVBoxLayout(self.frame_3)
        self.vboxlayout2.setObjectName("vboxlayout2")
        self.label_2 = QtGui.QLabel(self.frame_3)
        self.label_2.setObjectName("label_2")
        self.vboxlayout2.addWidget(self.label_2)
        self.kelvinRB = QtGui.QRadioButton(self.frame_3)
        self.kelvinRB.setChecked(True)
        self.kelvinRB.setObjectName("kelvinRB")
        self.vboxlayout2.addWidget(self.kelvinRB)
        self.celsiusRB = QtGui.QRadioButton(self.frame_3)
        self.celsiusRB.setChecked(False)
        self.celsiusRB.setObjectName("celsiusRB")
        self.vboxlayout2.addWidget(self.celsiusRB)
        self.gridlayout.addWidget(self.frame_3,0,1,1,1)
        self.groupBox = QtGui.QGroupBox(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred,QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setMinimumSize(QtCore.QSize(0,0))
        self.groupBox.setObjectName("groupBox")
        self.vboxlayout3 = QtGui.QVBoxLayout(self.groupBox)
        self.vboxlayout3.setObjectName("vboxlayout3")
        self.GeomSphereRB = QtGui.QRadioButton(self.groupBox)
        self.GeomSphereRB.setChecked(True)
        self.GeomSphereRB.setObjectName("GeomSphereRB")
        self.vboxlayout3.addWidget(self.GeomSphereRB)
        self.GeomEquivSphRB = QtGui.QRadioButton(self.groupBox)
        self.GeomEquivSphRB.setEnabled(True)
        self.GeomEquivSphRB.setChecked(False)
        self.GeomEquivSphRB.setObjectName("GeomEquivSphRB")
        self.vboxlayout3.addWidget(self.GeomEquivSphRB)
        self.GeomCubeRB = QtGui.QRadioButton(self.groupBox)
        self.GeomCubeRB.setObjectName("GeomCubeRB")
        self.vboxlayout3.addWidget(self.GeomCubeRB)
        self.GeomChannelRB = QtGui.QRadioButton(self.groupBox)
        self.GeomChannelRB.setObjectName("GeomChannelRB")
        self.vboxlayout3.addWidget(self.GeomChannelRB)
        self.GeomSheetRB = QtGui.QRadioButton(self.groupBox)
        self.GeomSheetRB.setObjectName("GeomSheetRB")
        self.vboxlayout3.addWidget(self.GeomSheetRB)
        self.softwallsCB = QtGui.QCheckBox(self.groupBox)
        self.softwallsCB.setObjectName("softwallsCB")
        self.vboxlayout3.addWidget(self.softwallsCB)
        self.gridlayout.addWidget(self.groupBox,0,2,2,1)
        self.tauTE = QtGui.QTextEdit(self.groupBox_2)
        self.tauTE.setObjectName("tauTE")
        self.gridlayout.addWidget(self.tauTE,1,0,1,1)
        self.TempTE = QtGui.QTextEdit(self.groupBox_2)
        self.TempTE.setEnabled(False)
        self.TempTE.setObjectName("TempTE")
        self.gridlayout.addWidget(self.TempTE,1,1,1,1)
        self.sameTempCB = QtGui.QCheckBox(self.groupBox_2)
        self.sameTempCB.setEnabled(False)
        self.sameTempCB.setObjectName("sameTempCB")
        self.gridlayout.addWidget(self.sameTempCB,2,1,1,1)
        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setObjectName("hboxlayout")
        spacerItem = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem)
        self.ClearPB = QtGui.QPushButton(self.groupBox_2)
        self.ClearPB.setObjectName("ClearPB")
        self.hboxlayout.addWidget(self.ClearPB)
        self.gridlayout.addLayout(self.hboxlayout,2,2,1,1)
        self.vboxlayout.addWidget(self.groupBox_2)
        self.groupBox_3 = QtGui.QGroupBox(TEcalcGUI)
        self.groupBox_3.setObjectName("groupBox_3")
        self.vboxlayout4 = QtGui.QVBoxLayout(self.groupBox_3)
        self.vboxlayout4.setObjectName("vboxlayout4")
        self.resultsTable = QtGui.QTableWidget(self.groupBox_3)
        self.resultsTable.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.resultsTable.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.resultsTable.setSortingEnabled(False)
        self.resultsTable.setObjectName("resultsTable")
        self.vboxlayout4.addWidget(self.resultsTable)
        self.vboxlayout.addWidget(self.groupBox_3)
        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setObjectName("hboxlayout1")
        spacerItem1 = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout1.addItem(spacerItem1)
        self.CalculatePB = QtGui.QPushButton(TEcalcGUI)
        self.CalculatePB.setObjectName("CalculatePB")
        self.hboxlayout1.addWidget(self.CalculatePB)
        self.vboxlayout.addLayout(self.hboxlayout1)
        self.actionCopy_Results_Selection = QtGui.QAction(TEcalcGUI)
        icon = QtGui.QIcon()
        icon.addFile(":/Icons/icons/mine/TaoEldrup64x64.png")
        self.actionCopy_Results_Selection.setIcon(icon)
        self.actionCopy_Results_Selection.setObjectName("actionCopy_Results_Selection")

        self.retranslateUi(TEcalcGUI)
        QtCore.QObject.connect(self.ClearPB,QtCore.SIGNAL("clicked()"),self.TempTE.clear)
        QtCore.QObject.connect(self.ClearPB,QtCore.SIGNAL("clicked()"),self.tauTE.clear)
        QtCore.QObject.connect(self.GeomSphereRB,QtCore.SIGNAL("toggled(bool)"),self.TempTE.setDisabled)
        QtCore.QObject.connect(self.GeomSphereRB,QtCore.SIGNAL("toggled(bool)"),self.sameTempCB.setDisabled)
        QtCore.QObject.connect(self.GeomSphereRB,QtCore.SIGNAL("toggled(bool)"),self.frame_3.setDisabled)
        QtCore.QObject.connect(self.ClearPB,QtCore.SIGNAL("clicked()"),self.resultsTable.clearContents)
        QtCore.QMetaObject.connectSlotsByName(TEcalcGUI)

    def retranslateUi(self, TEcalcGUI):
        TEcalcGUI.setWindowTitle(QtGui.QApplication.translate("TEcalcGUI", "Tao-Eldrup Calculator", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("TEcalcGUI", "Inputs", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("TEcalcGUI", "Lifetimes", None, QtGui.QApplication.UnicodeUTF8))
        self.nsRB.setText(QtGui.QApplication.translate("TEcalcGUI", "ns", None, QtGui.QApplication.UnicodeUTF8))
        self.psRB.setText(QtGui.QApplication.translate("TEcalcGUI", "ps", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("TEcalcGUI", "Temperatures", None, QtGui.QApplication.UnicodeUTF8))
        self.kelvinRB.setText(QtGui.QApplication.translate("TEcalcGUI", "Kelvin", None, QtGui.QApplication.UnicodeUTF8))
        self.celsiusRB.setText(QtGui.QApplication.translate("TEcalcGUI", "Celsius", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("TEcalcGUI", "Pore geometry", None, QtGui.QApplication.UnicodeUTF8))
        self.GeomSphereRB.setToolTip(QtGui.QApplication.translate("TEcalcGUI", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\">Spherical pores. </p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\">The <span style=\" font-weight:600;\">original</span> Tao-Eldrup model is used.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.GeomSphereRB.setText(QtGui.QApplication.translate("TEcalcGUI", "Sphere (TE)", None, QtGui.QApplication.UnicodeUTF8))
        self.GeomEquivSphRB.setToolTip(QtGui.QApplication.translate("TEcalcGUI", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\">The rectangular Tao-Eldrup model is used to obtain a cubic pore size. Then the cube size is converted to an sphere of equivalent mean free path.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.GeomEquivSphRB.setText(QtGui.QApplication.translate("TEcalcGUI", "Equiv Sphere (RTE)", None, QtGui.QApplication.UnicodeUTF8))
        self.GeomCubeRB.setToolTip(QtGui.QApplication.translate("TEcalcGUI", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Cubic pore.</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">The <span style=\" font-weight:600;\">Rectangular</span> Tao-Eldrup mode is used.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.GeomCubeRB.setText(QtGui.QApplication.translate("TEcalcGUI", "Cube", None, QtGui.QApplication.UnicodeUTF8))
        self.GeomChannelRB.setToolTip(QtGui.QApplication.translate("TEcalcGUI", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Infinitelly long, square section channel.</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">The <span style=\" font-weight:600;\">Rectangular</span> Tao-Eldrup mode is used.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.GeomChannelRB.setText(QtGui.QApplication.translate("TEcalcGUI", "Square Channel", None, QtGui.QApplication.UnicodeUTF8))
        self.GeomSheetRB.setToolTip(QtGui.QApplication.translate("TEcalcGUI", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Infinitelly wide, planar pore.</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\">The <span style=\" font-weight:600;\">Rectangular</span> Tao-Eldrup mode is used.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.GeomSheetRB.setText(QtGui.QApplication.translate("TEcalcGUI", "Sheet", None, QtGui.QApplication.UnicodeUTF8))
        self.softwallsCB.setToolTip(QtGui.QApplication.translate("TEcalcGUI", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\">The TE model (as well as the RTE) introduce the concept of \"soft potential walls\". </p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\">If this option is checked, the \"soft wall\" width will be included in the reported size.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.softwallsCB.setText(QtGui.QApplication.translate("TEcalcGUI", "Include \"soft walls\"", None, QtGui.QApplication.UnicodeUTF8))
        self.tauTE.setToolTip(QtGui.QApplication.translate("TEcalcGUI", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Fill with lifetime values.</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Lists of values can be separated by spaces, carriage returns, tabulators or semicolons</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.TempTE.setToolTip(QtGui.QApplication.translate("TEcalcGUI", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Fill with temperature values if you are using the Rectangular Tao-Eldrup model.</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Lists of values can be separated by spaces, carriage returns, tabulators or semicolons.</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">If you want to calculate many lifetimes for the same temperature, enter a single value here and check the \"Same temp.\" option below.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.TempTE.setHtml(QtGui.QApplication.translate("TEcalcGUI", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\">0</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.sameTempCB.setToolTip(QtGui.QApplication.translate("TEcalcGUI", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Enable this if you want to use a single temperature value for all the calculations.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.sameTempCB.setText(QtGui.QApplication.translate("TEcalcGUI", "Same temp. for all", None, QtGui.QApplication.UnicodeUTF8))
        self.ClearPB.setToolTip(QtGui.QApplication.translate("TEcalcGUI", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Clear the Lifetime and Temperature inputs, as well as the results.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.ClearPB.setText(QtGui.QApplication.translate("TEcalcGUI", "Clear", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_3.setTitle(QtGui.QApplication.translate("TEcalcGUI", "Output", None, QtGui.QApplication.UnicodeUTF8))
        self.resultsTable.setToolTip(QtGui.QApplication.translate("TEcalcGUI", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Results.</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">You can copy them all by selecting the desired results and using the context menu option.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.resultsTable.clear()
        self.resultsTable.setColumnCount(3)
        self.resultsTable.setRowCount(0)
        headerItem = QtGui.QTableWidgetItem()
        headerItem.setText(QtGui.QApplication.translate("TEcalcGUI", "Lifetime (ns)", None, QtGui.QApplication.UnicodeUTF8))
        self.resultsTable.setHorizontalHeaderItem(0,headerItem)
        headerItem1 = QtGui.QTableWidgetItem()
        headerItem1.setText(QtGui.QApplication.translate("TEcalcGUI", "Temperature (K)", None, QtGui.QApplication.UnicodeUTF8))
        self.resultsTable.setHorizontalHeaderItem(1,headerItem1)
        headerItem2 = QtGui.QTableWidgetItem()
        headerItem2.setText(QtGui.QApplication.translate("TEcalcGUI", "Size (nm)", None, QtGui.QApplication.UnicodeUTF8))
        self.resultsTable.setHorizontalHeaderItem(2,headerItem2)
        self.CalculatePB.setText(QtGui.QApplication.translate("TEcalcGUI", "Calculate", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCopy_Results_Selection.setText(QtGui.QApplication.translate("TEcalcGUI", "Copy_Results_Selection", None, QtGui.QApplication.UnicodeUTF8))

import PAScual_rc
