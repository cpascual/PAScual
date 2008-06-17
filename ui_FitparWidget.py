# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Documents and Settings\pas064\My Documents\src\PAScual-dev\FitparWidget.ui'
#
# Created: Wed Jun 18 03:48:06 2008
#      by: PyQt4 UI code generator 4.4.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_FitparWidget(object):
    def setupUi(self, FitparWidget):
        FitparWidget.setObjectName("FitparWidget")
        FitparWidget.resize(657,33)
        self.CBFix = QtGui.QCheckBox(FitparWidget)
        self.CBFix.setGeometry(QtCore.QRect(240,0,20,16))
        self.CBFix.setMinimumSize(QtCore.QSize(0,0))
        self.CBFix.setObjectName("CBFix")
        self.CBCommon = QtGui.QCheckBox(FitparWidget)
        self.CBCommon.setGeometry(QtCore.QRect(260,0,16,18))
        self.CBCommon.setObjectName("CBCommon")
        self.LEMax = QtGui.QLineEdit(FitparWidget)
        self.LEMax.setGeometry(QtCore.QRect(450,0,108,20))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(7),QtGui.QSizePolicy.Policy(0))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.LEMax.sizePolicy().hasHeightForWidth())
        self.LEMax.setSizePolicy(sizePolicy)
        self.LEMax.setMinimumSize(QtCore.QSize(70,20))
        self.LEMax.setAlignment(QtCore.Qt.AlignRight)
        self.LEMax.setObjectName("LEMax")
        self.LEMin = QtGui.QLineEdit(FitparWidget)
        self.LEMin.setGeometry(QtCore.QRect(340,0,108,20))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(7),QtGui.QSizePolicy.Policy(0))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.LEMin.sizePolicy().hasHeightForWidth())
        self.LEMin.setSizePolicy(sizePolicy)
        self.LEMin.setMinimumSize(QtCore.QSize(70,20))
        self.LEMin.setAlignment(QtCore.Qt.AlignRight)
        self.LEMin.setObjectName("LEMin")
        self.label = QtGui.QLabel(FitparWidget)
        self.label.setGeometry(QtCore.QRect(11,1,84,20))
        self.label.setMinimumSize(QtCore.QSize(0,20))
        self.label.setObjectName("label")
        self.LEValue = QtGui.QLineEdit(FitparWidget)
        self.LEValue.setGeometry(QtCore.QRect(128,1,108,20))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(7),QtGui.QSizePolicy.Policy(0))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.LEValue.sizePolicy().hasHeightForWidth())
        self.LEValue.setSizePolicy(sizePolicy)
        self.LEValue.setMinimumSize(QtCore.QSize(70,20))
        self.LEValue.setBaseSize(QtCore.QSize(0,20))
        self.LEValue.setAlignment(QtCore.Qt.AlignRight)
        self.LEValue.setObjectName("LEValue")
        self.BTApply = QtGui.QToolButton(FitparWidget)
        self.BTApply.setGeometry(QtCore.QRect(560,0,20,20))
        icon = QtGui.QIcon()
        icon.addFile(":/Icons/Icons/mine/CRbutton_ok.png")
        self.BTApply.setIcon(icon)
        self.BTApply.setObjectName("BTApply")
        self.BTAutoFill = QtGui.QToolButton(FitparWidget)
        self.BTAutoFill.setEnabled(True)
        self.BTAutoFill.setGeometry(QtCore.QRect(101,1,21,20))
        icon = QtGui.QIcon()
        icon.addFile(":/Icons/Icons/mine/CRcalc.png")
        self.BTAutoFill.setIcon(icon)
        self.BTAutoFill.setObjectName("BTAutoFill")

        self.retranslateUi(FitparWidget)
        QtCore.QObject.connect(self.CBFix,QtCore.SIGNAL("toggled(bool)"),self.LEMax.setDisabled)
        QtCore.QObject.connect(self.CBFix,QtCore.SIGNAL("toggled(bool)"),self.LEMin.setDisabled)
        QtCore.QObject.connect(self.CBFix,QtCore.SIGNAL("toggled(bool)"),self.CBCommon.setDisabled)
        QtCore.QMetaObject.connectSlotsByName(FitparWidget)

    def retranslateUi(self, FitparWidget):
        FitparWidget.setWindowTitle(QtGui.QApplication.translate("FitparWidget", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.CBFix.setToolTip(QtGui.QApplication.translate("FitparWidget", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal; text-decoration:none;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\">Fixed parameter?</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\">If checked, this paramer won\'t be fitted.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.CBCommon.setToolTip(QtGui.QApplication.translate("FitparWidget", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal; text-decoration:none;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Common Parameter?</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">If multiple spectra are selected, this parameter will be <span style=\" font-weight:600;\">common</span> to all of them, grouping them in the same set.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.LEMax.setToolTip(QtGui.QApplication.translate("FitparWidget", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal; text-decoration:none;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Maximum</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.LEMin.setToolTip(QtGui.QApplication.translate("FitparWidget", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal; text-decoration:none;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Minimum</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.LEMin.setText(QtGui.QApplication.translate("FitparWidget", "0", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("FitparWidget", "Parameter [units]", None, QtGui.QApplication.UnicodeUTF8))
        self.LEValue.setToolTip(QtGui.QApplication.translate("FitparWidget", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal; text-decoration:none;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Value</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.BTApply.setToolTip(QtGui.QApplication.translate("FitparWidget", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal; text-decoration:none;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\">Apply </p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\">Applies this parameter to the selected spectra.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.BTApply.setText(QtGui.QApplication.translate("FitparWidget", "A", None, QtGui.QApplication.UnicodeUTF8))
        self.BTAutoFill.setToolTip(QtGui.QApplication.translate("FitparWidget", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal; text-decoration:none;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Alternative setting</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))

import PAScual_rc
