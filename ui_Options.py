# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Documents and Settings\pas064\My Documents\src\PAScual-dev\Options.ui'
#
# Created: Wed Jun 25 22:51:45 2008
#      by: PyQt4 UI code generator 4.4.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Options(object):
    def setupUi(self, Options):
        Options.setObjectName("Options")
        Options.setWindowModality(QtCore.Qt.ApplicationModal)
        Options.resize(446,370)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/Icons/Icons/mine/PAScual-64x64.png"),QtGui.QIcon.Normal,QtGui.QIcon.Off)
        Options.setWindowIcon(icon)
        self.verticalLayout = QtGui.QVBoxLayout(Options)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtGui.QFrame(Options)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout = QtGui.QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_15 = QtGui.QLabel(self.frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_15.sizePolicy().hasHeightForWidth())
        self.label_15.setSizePolicy(sizePolicy)
        self.label_15.setMinimumSize(QtCore.QSize(70,70))
        self.label_15.setObjectName("label_15")
        self.horizontalLayout.addWidget(self.label_15)
        self.label_13 = QtGui.QLabel(self.frame)
        self.label_13.setMinimumSize(QtCore.QSize(311,0))
        self.label_13.setWordWrap(True)
        self.label_13.setObjectName("label_13")
        self.horizontalLayout.addWidget(self.label_13)
        self.verticalLayout.addWidget(self.frame)
        self.tabWidget = QtGui.QTabWidget(Options)
        self.tabWidget.setObjectName("tabWidget")
        self.LocalTab = QtGui.QWidget()
        self.LocalTab.setGeometry(QtCore.QRect(0,0,422,198))
        self.LocalTab.setObjectName("LocalTab")
        self.gridLayout = QtGui.QGridLayout(self.LocalTab)
        self.gridLayout.setObjectName("gridLayout")
        self.label_6 = QtGui.QLabel(self.LocalTab)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6,0,0,1,1)
        self.LOCAL_maxUnboundSB = QtGui.QSpinBox(self.LocalTab)
        self.LOCAL_maxUnboundSB.setObjectName("LOCAL_maxUnboundSB")
        self.gridLayout.addWidget(self.LOCAL_maxUnboundSB,0,1,1,1)
        spacerItem = QtGui.QSpacerItem(232,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem,0,2,1,1)
        self.tabWidget.addTab(self.LocalTab,"")
        self.SATab = QtGui.QWidget()
        self.SATab.setGeometry(QtCore.QRect(0,0,422,198))
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
        self.SA_directCB.setChecked(True)
        self.SA_directCB.setObjectName("SA_directCB")
        self.gridlayout.addWidget(self.SA_directCB,5,1,1,1)
        spacerItem1 = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem1,5,2,1,1)
        spacerItem2 = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem2,4,2,1,1)
        spacerItem3 = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem3,3,2,1,1)
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
        self.SA_stopTSB = QtGui.QDoubleSpinBox(self.SATab)
        self.SA_stopTSB.setAccelerated(True)
        self.SA_stopTSB.setMaximum(10000000000.0)
        self.SA_stopTSB.setProperty("value",QtCore.QVariant(0.1))
        self.SA_stopTSB.setObjectName("SA_stopTSB")
        self.gridlayout.addWidget(self.SA_stopTSB,1,1,1,1)
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
        spacerItem4 = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem4,0,2,1,1)
        spacerItem5 = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem5,1,2,1,1)
        spacerItem6 = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem6,2,2,1,1)
        self.tabWidget.addTab(self.SATab,"")
        self.BITab = QtGui.QWidget()
        self.BITab.setGeometry(QtCore.QRect(0,0,422,198))
        self.BITab.setObjectName("BITab")
        self.gridLayout_2 = QtGui.QGridLayout(self.BITab)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_7 = QtGui.QLabel(self.BITab)
        self.label_7.setObjectName("label_7")
        self.gridLayout_2.addWidget(self.label_7,0,0,1,1)
        self.BI_lengthLE = QtGui.QLineEdit(self.BITab)
        self.BI_lengthLE.setObjectName("BI_lengthLE")
        self.gridLayout_2.addWidget(self.BI_lengthLE,0,1,1,1)
        spacerItem7 = QtGui.QSpacerItem(86,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem7,0,2,1,2)
        self.label_8 = QtGui.QLabel(self.BITab)
        self.label_8.setObjectName("label_8")
        self.gridLayout_2.addWidget(self.label_8,1,0,1,1)
        self.BI_stabLE = QtGui.QLineEdit(self.BITab)
        self.BI_stabLE.setObjectName("BI_stabLE")
        self.gridLayout_2.addWidget(self.BI_stabLE,1,1,1,1)
        spacerItem8 = QtGui.QSpacerItem(100,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem8,1,2,1,2)
        self.label_9 = QtGui.QLabel(self.BITab)
        self.label_9.setObjectName("label_9")
        self.gridLayout_2.addWidget(self.label_9,2,0,1,1)
        self.BI_reportLE = QtGui.QLineEdit(self.BITab)
        self.BI_reportLE.setObjectName("BI_reportLE")
        self.gridLayout_2.addWidget(self.BI_reportLE,2,1,1,1)
        spacerItem9 = QtGui.QSpacerItem(100,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem9,2,2,1,2)
        self.BI_savehistCB = QtGui.QCheckBox(self.BITab)
        self.BI_savehistCB.setObjectName("BI_savehistCB")
        self.gridLayout_2.addWidget(self.BI_savehistCB,3,0,1,1)
        self.BI_savehistLE = QtGui.QLineEdit(self.BITab)
        self.BI_savehistLE.setEnabled(False)
        self.BI_savehistLE.setObjectName("BI_savehistLE")
        self.gridLayout_2.addWidget(self.BI_savehistLE,3,1,1,2)
        self.BI_savehistPB = QtGui.QToolButton(self.BITab)
        self.BI_savehistPB.setEnabled(False)
        self.BI_savehistPB.setObjectName("BI_savehistPB")
        self.gridLayout_2.addWidget(self.BI_savehistPB,3,3,1,1)
        self.tabWidget.addTab(self.BITab,"")
        self.pathsTab = QtGui.QWidget()
        self.pathsTab.setGeometry(QtCore.QRect(0,0,422,198))
        self.pathsTab.setObjectName("pathsTab")
        self.gridLayout_3 = QtGui.QGridLayout(self.pathsTab)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_11 = QtGui.QLabel(self.pathsTab)
        self.label_11.setObjectName("label_11")
        self.gridLayout_3.addWidget(self.label_11,0,0,1,1)
        self.workDirectoryLE = QtGui.QLineEdit(self.pathsTab)
        self.workDirectoryLE.setObjectName("workDirectoryLE")
        self.gridLayout_3.addWidget(self.workDirectoryLE,0,1,1,1)
        self.workDirectoryPB = QtGui.QToolButton(self.pathsTab)
        self.workDirectoryPB.setObjectName("workDirectoryPB")
        self.gridLayout_3.addWidget(self.workDirectoryPB,0,2,1,1)
        self.label_10 = QtGui.QLabel(self.pathsTab)
        self.label_10.setObjectName("label_10")
        self.gridLayout_3.addWidget(self.label_10,1,0,1,1)
        self.manualFileLE = QtGui.QLineEdit(self.pathsTab)
        self.manualFileLE.setObjectName("manualFileLE")
        self.gridLayout_3.addWidget(self.manualFileLE,1,1,1,1)
        self.manualFilePB = QtGui.QToolButton(self.pathsTab)
        self.manualFilePB.setObjectName("manualFilePB")
        self.gridLayout_3.addWidget(self.manualFilePB,1,2,1,1)
        self.tabWidget.addTab(self.pathsTab,"")
        self.miscTab = QtGui.QWidget()
        self.miscTab.setGeometry(QtCore.QRect(0,0,422,198))
        self.miscTab.setObjectName("miscTab")
        self.gridLayout_5 = QtGui.QGridLayout(self.miscTab)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.label_12 = QtGui.QLabel(self.miscTab)
        self.label_12.setObjectName("label_12")
        self.gridLayout_5.addWidget(self.label_12,0,0,1,1)
        self.seedLE = QtGui.QLineEdit(self.miscTab)
        self.seedLE.setObjectName("seedLE")
        self.gridLayout_5.addWidget(self.seedLE,0,1,1,1)
        spacerItem10 = QtGui.QSpacerItem(135,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridLayout_5.addItem(spacerItem10,0,2,1,1)
        self.gridLayout_4 = QtGui.QGridLayout()
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.label_14 = QtGui.QLabel(self.miscTab)
        self.label_14.setObjectName("label_14")
        self.gridLayout_4.addWidget(self.label_14,0,0,1,2)
        self.warning_chi2_lowSB = QtGui.QDoubleSpinBox(self.miscTab)
        self.warning_chi2_lowSB.setAccelerated(True)
        self.warning_chi2_lowSB.setDecimals(1)
        self.warning_chi2_lowSB.setMaximum(10000000000.0)
        self.warning_chi2_lowSB.setProperty("value",QtCore.QVariant(0.1))
        self.warning_chi2_lowSB.setObjectName("warning_chi2_lowSB")
        self.gridLayout_4.addWidget(self.warning_chi2_lowSB,0,2,1,1)
        spacerItem11 = QtGui.QSpacerItem(68,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem11,1,0,1,1)
        self.label_16 = QtGui.QLabel(self.miscTab)
        self.label_16.setObjectName("label_16")
        self.gridLayout_4.addWidget(self.label_16,1,1,1,1)
        self.warning_chi2_highSB = QtGui.QDoubleSpinBox(self.miscTab)
        self.warning_chi2_highSB.setAccelerated(True)
        self.warning_chi2_highSB.setDecimals(1)
        self.warning_chi2_highSB.setMaximum(10000000000.0)
        self.warning_chi2_highSB.setProperty("value",QtCore.QVariant(0.1))
        self.warning_chi2_highSB.setObjectName("warning_chi2_highSB")
        self.gridLayout_4.addWidget(self.warning_chi2_highSB,1,2,1,1)
        self.gridLayout_5.addLayout(self.gridLayout_4,1,0,1,2)
        spacerItem12 = QtGui.QSpacerItem(135,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridLayout_5.addItem(spacerItem12,1,2,1,1)
        self.tabWidget.addTab(self.miscTab,"")
        self.verticalLayout.addWidget(self.tabWidget)
        self.buttonBox = QtGui.QDialogButtonBox(Options)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok|QtGui.QDialogButtonBox.Reset)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Options)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.buttonBox,QtCore.SIGNAL("accepted()"),Options.accept)
        QtCore.QObject.connect(self.buttonBox,QtCore.SIGNAL("rejected()"),Options.reject)
        QtCore.QObject.connect(self.BI_savehistCB,QtCore.SIGNAL("toggled(bool)"),self.BI_savehistLE.setEnabled)
        QtCore.QObject.connect(self.BI_savehistCB,QtCore.SIGNAL("toggled(bool)"),self.BI_savehistPB.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(Options)
        Options.setTabOrder(self.tabWidget,self.LOCAL_maxUnboundSB)
        Options.setTabOrder(self.LOCAL_maxUnboundSB,self.SA_tolSB)
        Options.setTabOrder(self.SA_tolSB,self.SA_stopTSB)
        Options.setTabOrder(self.SA_stopTSB,self.SA_maxiterSB)
        Options.setTabOrder(self.SA_maxiterSB,self.SA_minaccratioSB)
        Options.setTabOrder(self.SA_minaccratioSB,self.SA_meltratioSB)
        Options.setTabOrder(self.SA_meltratioSB,self.SA_directCB)
        Options.setTabOrder(self.SA_directCB,self.BI_lengthLE)
        Options.setTabOrder(self.BI_lengthLE,self.BI_stabLE)
        Options.setTabOrder(self.BI_stabLE,self.BI_reportLE)
        Options.setTabOrder(self.BI_reportLE,self.BI_savehistCB)
        Options.setTabOrder(self.BI_savehistCB,self.BI_savehistLE)
        Options.setTabOrder(self.BI_savehistLE,self.BI_savehistPB)
        Options.setTabOrder(self.BI_savehistPB,self.buttonBox)

    def retranslateUi(self, Options):
        Options.setWindowTitle(QtGui.QApplication.translate("Options", "PAScual- Options", None, QtGui.QApplication.UnicodeUTF8))
        self.label_15.setText(QtGui.QApplication.translate("Options", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><img src=\":/Icons/icons/mine/advancedsettings.png\" /></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_13.setText(QtGui.QApplication.translate("Options", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"><span style=\" font-weight:600;\">IMPORTANT:</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\">The default settings should be OK for most uses.</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\">Wrong settings may affect the performance of PAScual. </p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\">If you mess things up, use the Reset button.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setToolTip(QtGui.QApplication.translate("Options", "Maximum number of unbound transitions to be performed during the LOCAL fit.", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("Options", "Max number of unbound iterations", None, QtGui.QApplication.UnicodeUTF8))
        self.LOCAL_maxUnboundSB.setToolTip(QtGui.QApplication.translate("Options", "Maximum number of unbound transitions to be performed during the LOCAL fit.", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.LocalTab), QtGui.QApplication.translate("Options", "Local", None, QtGui.QApplication.UnicodeUTF8))
        self.SA_minaccratioSB.setToolTip(QtGui.QApplication.translate("Options", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">The Simulated annealing will stop if the transition acceptance ratio gets lower than this value.</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.SA_minaccratioSB.setSpecialValueText(QtGui.QApplication.translate("Options", "No limit", None, QtGui.QApplication.UnicodeUTF8))
        self.SA_directCB.setToolTip(QtGui.QApplication.translate("Options", "Enable proposing asymetrical transitions (aka \"NNRLA-direct mode\") during the Simulated annealing.", None, QtGui.QApplication.UnicodeUTF8))
        self.SA_directCB.setText(QtGui.QApplication.translate("Options", "Asymetrical transitions", None, QtGui.QApplication.UnicodeUTF8))
        self.SA_meltratioSB.setToolTip(QtGui.QApplication.translate("Options", "The initial T value will be automatically raised during the \"melting\" stage (randomisation) until the transition acceptance ratio reaches this value", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setToolTip(QtGui.QApplication.translate("Options", "The initial T value will be automatically raised during the \"melting\" stage (randomisation) until the transition acceptance ratio reaches this value", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("Options", "Melting Ratio", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setToolTip(QtGui.QApplication.translate("Options", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">The Simulated annealing will stop if the transition acceptance ratio gets lower than this value.</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Options", "Min Acc Ratio", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setToolTip(QtGui.QApplication.translate("Options", "The Simulated annealing will stop after this many iterations.", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("Options", "Max Iter", None, QtGui.QApplication.UnicodeUTF8))
        self.SA_maxiterSB.setToolTip(QtGui.QApplication.translate("Options", "The Simulated annealing will stop after this many iterations.", None, QtGui.QApplication.UnicodeUTF8))
        self.SA_maxiterSB.setSpecialValueText(QtGui.QApplication.translate("Options", "No limit", None, QtGui.QApplication.UnicodeUTF8))
        self.SA_stopTSB.setToolTip(QtGui.QApplication.translate("Options", "The Simulated annealing will stop if the T parameter gets reaches this value.", None, QtGui.QApplication.UnicodeUTF8))
        self.SA_stopTSB.setSpecialValueText(QtGui.QApplication.translate("Options", "No limit", None, QtGui.QApplication.UnicodeUTF8))
        self.SA_tolSB.setToolTip(QtGui.QApplication.translate("Options", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">The Simulated annealing will stop if the Chi<span style=\" vertical-align:super;\">2</span> gets lower than this value.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setToolTip(QtGui.QApplication.translate("Options", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">The Simulated annealing will stop if the Chi<span style=\" vertical-align:super;\">2</span> gets lower than this value.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Options", "Tolerance", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setToolTip(QtGui.QApplication.translate("Options", "The Simulated annealing will stop if the T parameter gets reaches this value.", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Options", "Stop T", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.SATab), QtGui.QApplication.translate("Options", "SimAnn", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setToolTip(QtGui.QApplication.translate("Options", "Length of the Markov chain for the MCMC-BI algorithm\n"
" (this number will be multiplied by the number of free parameters)", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("Options", "Markov Chain Length", None, QtGui.QApplication.UnicodeUTF8))
        self.BI_lengthLE.setToolTip(QtGui.QApplication.translate("Options", "Length of the Markov chain for the MCMC-BI algorithm\n"
" (this number will be multiplied by the number of free parameters)", None, QtGui.QApplication.UnicodeUTF8))
        self.BI_lengthLE.setText(QtGui.QApplication.translate("Options", "50000", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setToolTip(QtGui.QApplication.translate("Options", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Length of the Markov chain for </span><span style=\" font-size:8pt; font-weight:600;\">stabilisation phase</span><span style=\" font-size:8pt;\"> of the MCMC-BI algorithm</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"> (this number will be multiplied by the number of free parameters)</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("Options", "Stabilisation length", None, QtGui.QApplication.UnicodeUTF8))
        self.BI_stabLE.setToolTip(QtGui.QApplication.translate("Options", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Length of the Markov chain for </span><span style=\" font-size:8pt; font-weight:600;\">stabilisation phase</span><span style=\" font-size:8pt;\"> of the MCMC-BI algorithm</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"> (this number will be multiplied by the number of free parameters)</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.BI_stabLE.setText(QtGui.QApplication.translate("Options", "5000", None, QtGui.QApplication.UnicodeUTF8))
        self.label_9.setToolTip(QtGui.QApplication.translate("Options", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">The MCMC-BI algorithm will update the output after accepting this many transitions</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\">(multiplied by the number of free parameters)</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_9.setText(QtGui.QApplication.translate("Options", "Report interval", None, QtGui.QApplication.UnicodeUTF8))
        self.BI_reportLE.setToolTip(QtGui.QApplication.translate("Options", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">The MCMC-BI algorithm will update the output after accepting this many transitions</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\">(multiplied by the number of free parameters)</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.BI_reportLE.setText(QtGui.QApplication.translate("Options", "500", None, QtGui.QApplication.UnicodeUTF8))
        self.BI_savehistCB.setToolTip(QtGui.QApplication.translate("Options", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\">Enable saving  the whole sampled solution space.</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\">This is required if a detailed analysis is to be done from the MCMC-BI results.</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"><span style=\" font-weight:600;\">Warning:</span> enabling this requires a lot of disk space and slows down the MCMC-BI.</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\">It is not needed to obtain the mean and the standard deviation of the sampled solution space.</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\">Enable only if you really need it.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.BI_savehistCB.setText(QtGui.QApplication.translate("Options", "Save history", None, QtGui.QApplication.UnicodeUTF8))
        self.BI_savehistLE.setToolTip(QtGui.QApplication.translate("Options", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\">File where the MCMC-BI sampled solution space is to be stored (if the save history option is enabled). This file can grow very large!.</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.BI_savehistLE.setText(QtGui.QApplication.translate("Options", "PAShist.txt", None, QtGui.QApplication.UnicodeUTF8))
        self.BI_savehistPB.setToolTip(QtGui.QApplication.translate("Options", "Select a \"history\" file...", None, QtGui.QApplication.UnicodeUTF8))
        self.BI_savehistPB.setText(QtGui.QApplication.translate("Options", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.BITab), QtGui.QApplication.translate("Options", "BI", None, QtGui.QApplication.UnicodeUTF8))
        self.label_11.setToolTip(QtGui.QApplication.translate("Options", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Base path for input/output. </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\">If you want to save results, make sure that the directory is user-writable.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_11.setText(QtGui.QApplication.translate("Options", "Base path", None, QtGui.QApplication.UnicodeUTF8))
        self.workDirectoryLE.setToolTip(QtGui.QApplication.translate("Options", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Base path for input/output. </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\">If you want to save results, make sure that the directory is user-writable.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.workDirectoryPB.setToolTip(QtGui.QApplication.translate("Options", "Select the Base path directory", None, QtGui.QApplication.UnicodeUTF8))
        self.workDirectoryPB.setText(QtGui.QApplication.translate("Options", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.label_10.setText(QtGui.QApplication.translate("Options", "Manual", None, QtGui.QApplication.UnicodeUTF8))
        self.manualFileLE.setToolTip(QtGui.QApplication.translate("Options", "Location of the main manual file", None, QtGui.QApplication.UnicodeUTF8))
        self.manualFilePB.setToolTip(QtGui.QApplication.translate("Options", "Browse for the User Manual file", None, QtGui.QApplication.UnicodeUTF8))
        self.manualFilePB.setText(QtGui.QApplication.translate("Options", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.pathsTab), QtGui.QApplication.translate("Options", "Paths", None, QtGui.QApplication.UnicodeUTF8))
        self.label_12.setToolTip(QtGui.QApplication.translate("Options", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Fixed seed for pseudo-random number generator. If you leave this field blank, the seed will be different each time you start PAScual.</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_12.setText(QtGui.QApplication.translate("Options", "Seed (Random gen.)", None, QtGui.QApplication.UnicodeUTF8))
        self.seedLE.setToolTip(QtGui.QApplication.translate("Options", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Fixed seed for pseudo-random number generator. If you leave this field blank, the seed will be different each time you start PAScual.</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_14.setToolTip(QtGui.QApplication.translate("Options", "The results table will warn that the fit is suspicious (by turning the row red) if the chi2 is outside the range set here.", None, QtGui.QApplication.UnicodeUTF8))
        self.label_14.setText(QtGui.QApplication.translate("Options", "Visual warning if chi2 is less than", None, QtGui.QApplication.UnicodeUTF8))
        self.warning_chi2_lowSB.setToolTip(QtGui.QApplication.translate("Options", "The results table will warn that the fit is suspicious (by turning the row red) if the chi2 is outside the range set here.", None, QtGui.QApplication.UnicodeUTF8))
        self.warning_chi2_lowSB.setSpecialValueText(QtGui.QApplication.translate("Options", "No limit", None, QtGui.QApplication.UnicodeUTF8))
        self.label_16.setToolTip(QtGui.QApplication.translate("Options", "The results table will warn that the fit is suspicious (by turning the row red) if the chi2 is outside the range set here.", None, QtGui.QApplication.UnicodeUTF8))
        self.label_16.setText(QtGui.QApplication.translate("Options", "or more than", None, QtGui.QApplication.UnicodeUTF8))
        self.warning_chi2_highSB.setToolTip(QtGui.QApplication.translate("Options", "The results table will warn that the fit is suspicious (by turning the row red) if the chi2 is outside the range set here.", None, QtGui.QApplication.UnicodeUTF8))
        self.warning_chi2_highSB.setSpecialValueText(QtGui.QApplication.translate("Options", "No limit", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.miscTab), QtGui.QApplication.translate("Options", "Misc.", None, QtGui.QApplication.UnicodeUTF8))

import PAScual_rc
