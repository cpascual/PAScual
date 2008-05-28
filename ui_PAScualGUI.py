# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Documents and Settings\pas064\My Documents\src\PAScual-dev\PAScualGUI.ui'
#
# Created: Wed May 28 18:32:21 2008
#      by: PyQt4 UI code generator 4.3.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_PAScual(object):
    def setupUi(self, PAScual):
        PAScual.setObjectName("PAScual")
        PAScual.resize(QtCore.QSize(QtCore.QRect(0,0,804,638).size()).expandedTo(PAScual.minimumSizeHint()))

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(PAScual.sizePolicy().hasHeightForWidth())
        PAScual.setSizePolicy(sizePolicy)
        PAScual.setWindowIcon(QtGui.QIcon(":/Icons/Icons/mine/PAScual-64x64.png"))

        self.centralwidget = QtGui.QWidget(PAScual)
        self.centralwidget.setObjectName("centralwidget")

        self.vboxlayout = QtGui.QVBoxLayout(self.centralwidget)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setMargin(9)
        self.vboxlayout.setObjectName("vboxlayout")

        self.tabWidget = QtGui.QTabWidget(self.centralwidget)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred,QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setObjectName("tabWidget")

        self.parametersTab = QtGui.QWidget()
        self.parametersTab.setEnabled(True)
        self.parametersTab.setObjectName("parametersTab")

        self.vboxlayout1 = QtGui.QVBoxLayout(self.parametersTab)
        self.vboxlayout1.setSpacing(6)
        self.vboxlayout1.setMargin(9)
        self.vboxlayout1.setObjectName("vboxlayout1")

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setObjectName("hboxlayout")

        self.label = QtGui.QLabel(self.parametersTab)
        self.label.setObjectName("label")
        self.hboxlayout.addWidget(self.label)

        self.LEpsperchannel = QtGui.QLineEdit(self.parametersTab)
        self.LEpsperchannel.setMaximumSize(QtCore.QSize(100,16777215))
        self.LEpsperchannel.setAlignment(QtCore.Qt.AlignRight)
        self.LEpsperchannel.setObjectName("LEpsperchannel")
        self.hboxlayout.addWidget(self.LEpsperchannel)

        self.BTpsperchannel = QtGui.QToolButton(self.parametersTab)
        self.BTpsperchannel.setIcon(QtGui.QIcon(":/Icons/Icons/mine/CRbutton_ok.png"))
        self.BTpsperchannel.setObjectName("BTpsperchannel")
        self.hboxlayout.addWidget(self.BTpsperchannel)

        spacerItem = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem)

        self.roiPB = QtGui.QPushButton(self.parametersTab)
        self.roiPB.setObjectName("roiPB")
        self.hboxlayout.addWidget(self.roiPB)
        self.vboxlayout1.addLayout(self.hboxlayout)

        self.FitparFrame = QtGui.QFrame(self.parametersTab)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred,QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.FitparFrame.sizePolicy().hasHeightForWidth())
        self.FitparFrame.setSizePolicy(sizePolicy)
        self.FitparFrame.setMinimumSize(QtCore.QSize(450,150))
        self.FitparFrame.setMaximumSize(QtCore.QSize(16777215,120))
        self.FitparFrame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.FitparFrame.setFrameShadow(QtGui.QFrame.Raised)
        self.FitparFrame.setObjectName("FitparFrame")
        self.vboxlayout1.addWidget(self.FitparFrame)

        self.componentsGroupBox = QtGui.QGroupBox(self.parametersTab)
        self.componentsGroupBox.setMinimumSize(QtCore.QSize(450,150))
        self.componentsGroupBox.setObjectName("componentsGroupBox")

        self.vboxlayout2 = QtGui.QVBoxLayout(self.componentsGroupBox)
        self.vboxlayout2.setSpacing(6)
        self.vboxlayout2.setMargin(9)
        self.vboxlayout2.setObjectName("vboxlayout2")

        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setSpacing(6)
        self.hboxlayout1.setMargin(0)
        self.hboxlayout1.setObjectName("hboxlayout1")

        self.label_5 = QtGui.QLabel(self.componentsGroupBox)
        self.label_5.setObjectName("label_5")
        self.hboxlayout1.addWidget(self.label_5)

        self.SBoxNcomp = QtGui.QSpinBox(self.componentsGroupBox)
        self.SBoxNcomp.setMinimum(0)
        self.SBoxNcomp.setProperty("value",QtCore.QVariant(0))
        self.SBoxNcomp.setObjectName("SBoxNcomp")
        self.hboxlayout1.addWidget(self.SBoxNcomp)

        self.hboxlayout2 = QtGui.QHBoxLayout()
        self.hboxlayout2.setSpacing(6)
        self.hboxlayout2.setMargin(0)
        self.hboxlayout2.setObjectName("hboxlayout2")

        self.showtauRB = QtGui.QRadioButton(self.componentsGroupBox)
        self.showtauRB.setChecked(True)
        self.showtauRB.setObjectName("showtauRB")
        self.hboxlayout2.addWidget(self.showtauRB)

        self.showityRB = QtGui.QRadioButton(self.componentsGroupBox)
        self.showityRB.setObjectName("showityRB")
        self.hboxlayout2.addWidget(self.showityRB)
        self.hboxlayout1.addLayout(self.hboxlayout2)

        spacerItem1 = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout1.addItem(spacerItem1)

        self.applycompsBT = QtGui.QToolButton(self.componentsGroupBox)
        self.applycompsBT.setIcon(QtGui.QIcon(":/Icons/Icons/mine/CRbutton_ok.png"))
        self.applycompsBT.setObjectName("applycompsBT")
        self.hboxlayout1.addWidget(self.applycompsBT)
        self.vboxlayout2.addLayout(self.hboxlayout1)

        self.compTable = QtGui.QTableView(self.componentsGroupBox)
        self.compTable.setObjectName("compTable")
        self.vboxlayout2.addWidget(self.compTable)
        self.vboxlayout1.addWidget(self.componentsGroupBox)

        self.hboxlayout3 = QtGui.QHBoxLayout()
        self.hboxlayout3.setSpacing(6)
        self.hboxlayout3.setMargin(0)
        self.hboxlayout3.setObjectName("hboxlayout3")

        spacerItem2 = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout3.addItem(spacerItem2)

        self.resetParametersPB = QtGui.QPushButton(self.parametersTab)
        self.resetParametersPB.setObjectName("resetParametersPB")
        self.hboxlayout3.addWidget(self.resetParametersPB)

        self.applyAllParametersPB = QtGui.QPushButton(self.parametersTab)
        self.applyAllParametersPB.setIcon(QtGui.QIcon(":/Icons/Icons/mine/CRbutton_ok.png"))
        self.applyAllParametersPB.setObjectName("applyAllParametersPB")
        self.hboxlayout3.addWidget(self.applyAllParametersPB)
        self.vboxlayout1.addLayout(self.hboxlayout3)
        self.tabWidget.addTab(self.parametersTab,"")

        self.fittingTab = QtGui.QWidget()
        self.fittingTab.setObjectName("fittingTab")

        self.vboxlayout3 = QtGui.QVBoxLayout(self.fittingTab)
        self.vboxlayout3.setSpacing(6)
        self.vboxlayout3.setMargin(9)
        self.vboxlayout3.setObjectName("vboxlayout3")

        self.groupBox = QtGui.QGroupBox(self.fittingTab)
        self.groupBox.setObjectName("groupBox")

        self.gridlayout = QtGui.QGridLayout(self.groupBox)
        self.gridlayout.setMargin(9)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")

        self.hboxlayout4 = QtGui.QHBoxLayout()
        self.hboxlayout4.setSpacing(6)
        self.hboxlayout4.setMargin(0)
        self.hboxlayout4.setObjectName("hboxlayout4")

        self.label_8 = QtGui.QLabel(self.groupBox)
        self.label_8.setObjectName("label_8")
        self.hboxlayout4.addWidget(self.label_8)

        self.unasignedLE = QtGui.QLineEdit(self.groupBox)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.unasignedLE.sizePolicy().hasHeightForWidth())
        self.unasignedLE.setSizePolicy(sizePolicy)
        self.unasignedLE.setMinimumSize(QtCore.QSize(30,0))
        self.unasignedLE.setReadOnly(True)
        self.unasignedLE.setObjectName("unasignedLE")
        self.hboxlayout4.addWidget(self.unasignedLE)

        spacerItem3 = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout4.addItem(spacerItem3)
        self.gridlayout.addLayout(self.hboxlayout4,2,1,1,1)

        self.hboxlayout5 = QtGui.QHBoxLayout()
        self.hboxlayout5.setSpacing(6)
        self.hboxlayout5.setMargin(0)
        self.hboxlayout5.setObjectName("hboxlayout5")

        self.applyFitModeBT = QtGui.QToolButton(self.groupBox)
        self.applyFitModeBT.setIcon(QtGui.QIcon(":/Icons/Icons/mine/CRbutton_ok.png"))
        self.applyFitModeBT.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.applyFitModeBT.setObjectName("applyFitModeBT")
        self.hboxlayout5.addWidget(self.applyFitModeBT)

        self.selectedSetsOnlyCB = QtGui.QCheckBox(self.groupBox)
        self.selectedSetsOnlyCB.setObjectName("selectedSetsOnlyCB")
        self.hboxlayout5.addWidget(self.selectedSetsOnlyCB)
        self.gridlayout.addLayout(self.hboxlayout5,0,1,1,1)

        self.setsTree = QtGui.QTreeWidget(self.groupBox)
        self.setsTree.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.setsTree.setColumnCount(2)
        self.setsTree.setObjectName("setsTree")
        self.gridlayout.addWidget(self.setsTree,1,1,1,1)

        self.commandsTable = QtGui.QTableView(self.groupBox)
        self.commandsTable.setShowGrid(False)
        self.commandsTable.setObjectName("commandsTable")
        self.gridlayout.addWidget(self.commandsTable,1,0,1,1)

        self.hboxlayout6 = QtGui.QHBoxLayout()
        self.hboxlayout6.setSpacing(6)
        self.hboxlayout6.setMargin(0)
        self.hboxlayout6.setObjectName("hboxlayout6")

        self.fitModeCB = QtGui.QComboBox(self.groupBox)
        self.fitModeCB.setObjectName("fitModeCB")
        self.hboxlayout6.addWidget(self.fitModeCB)

        self.saveFitmodeBT = QtGui.QToolButton(self.groupBox)
        self.saveFitmodeBT.setEnabled(False)
        self.saveFitmodeBT.setIcon(QtGui.QIcon(":/Icons/Icons/mine/CRfilesave.png"))
        self.saveFitmodeBT.setObjectName("saveFitmodeBT")
        self.hboxlayout6.addWidget(self.saveFitmodeBT)
        self.gridlayout.addLayout(self.hboxlayout6,0,0,1,1)
        self.vboxlayout3.addWidget(self.groupBox)

        self.groupBox_2 = QtGui.QGroupBox(self.fittingTab)
        self.groupBox_2.setObjectName("groupBox_2")

        self.gridlayout1 = QtGui.QGridLayout(self.groupBox_2)
        self.gridlayout1.setMargin(9)
        self.gridlayout1.setSpacing(6)
        self.gridlayout1.setObjectName("gridlayout1")

        self.hboxlayout7 = QtGui.QHBoxLayout()
        self.hboxlayout7.setSpacing(6)
        self.hboxlayout7.setMargin(0)
        self.hboxlayout7.setObjectName("hboxlayout7")

        self.goFitBT = QtGui.QToolButton(self.groupBox_2)
        self.goFitBT.setIcon(QtGui.QIcon(":/Icons/Icons/mine/CRplayer_play.png"))
        self.goFitBT.setObjectName("goFitBT")
        self.hboxlayout7.addWidget(self.goFitBT)

        self.skipCommandBT = QtGui.QToolButton(self.groupBox_2)
        self.skipCommandBT.setIcon(QtGui.QIcon(":/Icons/Icons/mine/CRplayer_end.png"))
        self.skipCommandBT.setObjectName("skipCommandBT")
        self.hboxlayout7.addWidget(self.skipCommandBT)

        self.stopFitBT = QtGui.QToolButton(self.groupBox_2)
        self.stopFitBT.setIcon(QtGui.QIcon(":/Icons/Icons/mine/CRplayer_stop.png"))
        self.stopFitBT.setObjectName("stopFitBT")
        self.hboxlayout7.addWidget(self.stopFitBT)
        self.gridlayout1.addLayout(self.hboxlayout7,2,2,1,1)

        self.totalPBar = QtGui.QProgressBar(self.groupBox_2)
        self.totalPBar.setProperty("value",QtCore.QVariant(0))
        self.totalPBar.setOrientation(QtCore.Qt.Horizontal)
        self.totalPBar.setObjectName("totalPBar")
        self.gridlayout1.addWidget(self.totalPBar,2,1,1,1)

        self.setPBar = QtGui.QProgressBar(self.groupBox_2)
        self.setPBar.setProperty("value",QtCore.QVariant(0))
        self.setPBar.setOrientation(QtCore.Qt.Horizontal)
        self.setPBar.setObjectName("setPBar")
        self.gridlayout1.addWidget(self.setPBar,1,1,1,1)

        self.commandPBar = QtGui.QProgressBar(self.groupBox_2)
        self.commandPBar.setProperty("value",QtCore.QVariant(0))
        self.commandPBar.setOrientation(QtCore.Qt.Horizontal)
        self.commandPBar.setObjectName("commandPBar")
        self.gridlayout1.addWidget(self.commandPBar,0,1,1,1)

        self.label_7 = QtGui.QLabel(self.groupBox_2)
        self.label_7.setObjectName("label_7")
        self.gridlayout1.addWidget(self.label_7,2,0,1,1)

        self.label_6 = QtGui.QLabel(self.groupBox_2)
        self.label_6.setObjectName("label_6")
        self.gridlayout1.addWidget(self.label_6,1,0,1,1)

        self.label_4 = QtGui.QLabel(self.groupBox_2)
        self.label_4.setObjectName("label_4")
        self.gridlayout1.addWidget(self.label_4,0,0,1,1)
        self.vboxlayout3.addWidget(self.groupBox_2)
        self.tabWidget.addTab(self.fittingTab,"")

        self.ResultsTab = QtGui.QWidget()
        self.ResultsTab.setObjectName("ResultsTab")

        self.gridlayout2 = QtGui.QGridLayout(self.ResultsTab)
        self.gridlayout2.setMargin(9)
        self.gridlayout2.setSpacing(6)
        self.gridlayout2.setObjectName("gridlayout2")

        self.hboxlayout8 = QtGui.QHBoxLayout()
        self.hboxlayout8.setSpacing(6)
        self.hboxlayout8.setMargin(0)
        self.hboxlayout8.setObjectName("hboxlayout8")

        self.hideResultsBT = QtGui.QToolButton(self.ResultsTab)
        self.hideResultsBT.setObjectName("hideResultsBT")
        self.hboxlayout8.addWidget(self.hideResultsBT)

        self.showResultsBT = QtGui.QToolButton(self.ResultsTab)
        self.showResultsBT.setObjectName("showResultsBT")
        self.hboxlayout8.addWidget(self.showResultsBT)
        self.gridlayout2.addLayout(self.hboxlayout8,1,0,1,1)

        self.resultsColumnsListWidget = QtGui.QListWidget(self.ResultsTab)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred,QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.resultsColumnsListWidget.sizePolicy().hasHeightForWidth())
        self.resultsColumnsListWidget.setSizePolicy(sizePolicy)
        self.resultsColumnsListWidget.setMaximumSize(QtCore.QSize(100,16777215))
        self.resultsColumnsListWidget.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.resultsColumnsListWidget.setObjectName("resultsColumnsListWidget")
        self.gridlayout2.addWidget(self.resultsColumnsListWidget,0,0,1,1)

        self.resultsTable = QtGui.QTableWidget(self.ResultsTab)
        self.resultsTable.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.resultsTable.setObjectName("resultsTable")
        self.gridlayout2.addWidget(self.resultsTable,0,1,1,1)

        self.hboxlayout9 = QtGui.QHBoxLayout()
        self.hboxlayout9.setSpacing(6)
        self.hboxlayout9.setMargin(0)
        self.hboxlayout9.setObjectName("hboxlayout9")

        self.label_9 = QtGui.QLabel(self.ResultsTab)
        self.label_9.setObjectName("label_9")
        self.hboxlayout9.addWidget(self.label_9)

        self.resultsFileLE = QtGui.QLineEdit(self.ResultsTab)
        self.resultsFileLE.setObjectName("resultsFileLE")
        self.hboxlayout9.addWidget(self.resultsFileLE)

        self.resultsFileSelectBT = QtGui.QToolButton(self.ResultsTab)
        self.resultsFileSelectBT.setObjectName("resultsFileSelectBT")
        self.hboxlayout9.addWidget(self.resultsFileSelectBT)

        self.saveResultsBT = QtGui.QToolButton(self.ResultsTab)
        self.saveResultsBT.setIcon(QtGui.QIcon(":/Icons/Icons/mine/CRfilesave.png"))
        self.saveResultsBT.setObjectName("saveResultsBT")
        self.hboxlayout9.addWidget(self.saveResultsBT)
        self.gridlayout2.addLayout(self.hboxlayout9,1,1,1,1)

        self.residualsFrame = QtGui.QFrame(self.ResultsTab)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.residualsFrame.sizePolicy().hasHeightForWidth())
        self.residualsFrame.setSizePolicy(sizePolicy)
        self.residualsFrame.setMinimumSize(QtCore.QSize(400,150))
        self.residualsFrame.setMaximumSize(QtCore.QSize(16777215,200))
        self.residualsFrame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.residualsFrame.setFrameShadow(QtGui.QFrame.Raised)
        self.residualsFrame.setObjectName("residualsFrame")
        self.gridlayout2.addWidget(self.residualsFrame,2,0,1,2)
        self.tabWidget.addTab(self.ResultsTab,"")

        self.OutputTab = QtGui.QWidget()
        self.OutputTab.setObjectName("OutputTab")

        self.vboxlayout4 = QtGui.QVBoxLayout(self.OutputTab)
        self.vboxlayout4.setObjectName("vboxlayout4")

        self.groupBox_3 = QtGui.QGroupBox(self.OutputTab)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred,QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_3.sizePolicy().hasHeightForWidth())
        self.groupBox_3.setSizePolicy(sizePolicy)
        self.groupBox_3.setObjectName("groupBox_3")

        self.hboxlayout10 = QtGui.QHBoxLayout(self.groupBox_3)
        self.hboxlayout10.setObjectName("hboxlayout10")

        self.previousOutputCB = QtGui.QComboBox(self.groupBox_3)
        self.previousOutputCB.setObjectName("previousOutputCB")
        self.hboxlayout10.addWidget(self.previousOutputCB)

        self.showPreviousOutputBT = QtGui.QToolButton(self.groupBox_3)
        self.showPreviousOutputBT.setObjectName("showPreviousOutputBT")
        self.hboxlayout10.addWidget(self.showPreviousOutputBT)
        self.vboxlayout4.addWidget(self.groupBox_3)

        self.groupBox_4 = QtGui.QGroupBox(self.OutputTab)
        self.groupBox_4.setObjectName("groupBox_4")

        self.vboxlayout5 = QtGui.QVBoxLayout(self.groupBox_4)
        self.vboxlayout5.setObjectName("vboxlayout5")

        self.outputTE = QtGui.QTextEdit(self.groupBox_4)
        self.outputTE.setLineWrapMode(QtGui.QTextEdit.NoWrap)
        self.outputTE.setReadOnly(True)
        self.outputTE.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.outputTE.setObjectName("outputTE")
        self.vboxlayout5.addWidget(self.outputTE)
        self.vboxlayout4.addWidget(self.groupBox_4)

        self.hboxlayout11 = QtGui.QHBoxLayout()
        self.hboxlayout11.setSpacing(6)
        self.hboxlayout11.setMargin(0)
        self.hboxlayout11.setObjectName("hboxlayout11")

        self.label_2 = QtGui.QLabel(self.OutputTab)
        self.label_2.setObjectName("label_2")
        self.hboxlayout11.addWidget(self.label_2)

        self.outputFileLE = QtGui.QLineEdit(self.OutputTab)
        self.outputFileLE.setObjectName("outputFileLE")
        self.hboxlayout11.addWidget(self.outputFileLE)

        self.outputFileSelectBT = QtGui.QToolButton(self.OutputTab)
        self.outputFileSelectBT.setObjectName("outputFileSelectBT")
        self.hboxlayout11.addWidget(self.outputFileSelectBT)

        self.saveOutputBT = QtGui.QToolButton(self.OutputTab)
        self.saveOutputBT.setIcon(QtGui.QIcon(":/Icons/Icons/mine/CRfilesave.png"))
        self.saveOutputBT.setObjectName("saveOutputBT")
        self.hboxlayout11.addWidget(self.saveOutputBT)
        self.vboxlayout4.addLayout(self.hboxlayout11)
        self.tabWidget.addTab(self.OutputTab,"")
        self.vboxlayout.addWidget(self.tabWidget)
        PAScual.setCentralWidget(self.centralwidget)

        self.menubar = QtGui.QMenuBar(PAScual)
        self.menubar.setGeometry(QtCore.QRect(0,0,804,21))
        self.menubar.setObjectName("menubar")

        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")

        self.menuView = QtGui.QMenu(self.menubar)
        self.menuView.setObjectName("menuView")

        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        PAScual.setMenuBar(self.menubar)

        self.statusbar = QtGui.QStatusBar(PAScual)
        self.statusbar.setObjectName("statusbar")
        PAScual.setStatusBar(self.statusbar)

        self.spectraDockWidget = QtGui.QDockWidget(PAScual)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding,QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spectraDockWidget.sizePolicy().hasHeightForWidth())
        self.spectraDockWidget.setSizePolicy(sizePolicy)
        self.spectraDockWidget.setMinimumSize(QtCore.QSize(300,272))
        self.spectraDockWidget.setFloating(False)
        self.spectraDockWidget.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea|QtCore.Qt.NoDockWidgetArea|QtCore.Qt.RightDockWidgetArea)
        self.spectraDockWidget.setObjectName("spectraDockWidget")

        self.dockWidgetContents = QtGui.QWidget(self.spectraDockWidget)
        self.dockWidgetContents.setObjectName("dockWidgetContents")

        self.vboxlayout6 = QtGui.QVBoxLayout(self.dockWidgetContents)
        self.vboxlayout6.setSpacing(6)
        self.vboxlayout6.setMargin(9)
        self.vboxlayout6.setObjectName("vboxlayout6")

        self.spectraTable = QtGui.QTableView(self.dockWidgetContents)
        self.spectraTable.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.spectraTable.setShowGrid(False)
        self.spectraTable.setObjectName("spectraTable")
        self.vboxlayout6.addWidget(self.spectraTable)

        self.hboxlayout12 = QtGui.QHBoxLayout()
        self.hboxlayout12.setSpacing(6)
        self.hboxlayout12.setMargin(0)
        self.hboxlayout12.setObjectName("hboxlayout12")

        self.selectAllTB = QtGui.QToolButton(self.dockWidgetContents)
        self.selectAllTB.setIcon(QtGui.QIcon(":/Icons/Icons/mine/checkall.png"))
        self.selectAllTB.setObjectName("selectAllTB")
        self.hboxlayout12.addWidget(self.selectAllTB)

        self.selectNoneTB = QtGui.QToolButton(self.dockWidgetContents)
        self.selectNoneTB.setIcon(QtGui.QIcon(":/Icons/Icons/mine/checknone.png"))
        self.selectNoneTB.setObjectName("selectNoneTB")
        self.hboxlayout12.addWidget(self.selectNoneTB)

        self.selectMarkedTB = QtGui.QToolButton(self.dockWidgetContents)
        self.selectMarkedTB.setIcon(QtGui.QIcon(":/Icons/Icons/mine/checkmarked.png"))
        self.selectMarkedTB.setObjectName("selectMarkedTB")
        self.hboxlayout12.addWidget(self.selectMarkedTB)

        spacerItem4 = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout12.addItem(spacerItem4)

        self.removeSpectraTB = QtGui.QToolButton(self.dockWidgetContents)
        self.removeSpectraTB.setIcon(QtGui.QIcon(":/Icons/Icons/mine/CRdelete.png"))
        self.removeSpectraTB.setObjectName("removeSpectraTB")
        self.hboxlayout12.addWidget(self.removeSpectraTB)
        self.vboxlayout6.addLayout(self.hboxlayout12)
        self.spectraDockWidget.setWidget(self.dockWidgetContents)
        PAScual.addDockWidget(QtCore.Qt.DockWidgetArea(1),self.spectraDockWidget)

        self.plotDockWidget = QtGui.QDockWidget(PAScual)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding,QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.plotDockWidget.sizePolicy().hasHeightForWidth())
        self.plotDockWidget.setSizePolicy(sizePolicy)
        self.plotDockWidget.setMinimumSize(QtCore.QSize(300,272))
        self.plotDockWidget.setFloating(False)
        self.plotDockWidget.setAllowedAreas(QtCore.Qt.AllDockWidgetAreas)
        self.plotDockWidget.setObjectName("plotDockWidget")

        self.dockWidgetContents_2 = QtGui.QWidget(self.plotDockWidget)
        self.dockWidgetContents_2.setObjectName("dockWidgetContents_2")

        self.vboxlayout7 = QtGui.QVBoxLayout(self.dockWidgetContents_2)
        self.vboxlayout7.setSpacing(6)
        self.vboxlayout7.setMargin(9)
        self.vboxlayout7.setObjectName("vboxlayout7")

        self.plotFrame = QtGui.QFrame(self.dockWidgetContents_2)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding,QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.plotFrame.sizePolicy().hasHeightForWidth())
        self.plotFrame.setSizePolicy(sizePolicy)
        self.plotFrame.setMinimumSize(QtCore.QSize(100,205))
        self.plotFrame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.plotFrame.setFrameShadow(QtGui.QFrame.Raised)
        self.plotFrame.setObjectName("plotFrame")
        self.vboxlayout7.addWidget(self.plotFrame)
        self.plotDockWidget.setWidget(self.dockWidgetContents_2)
        PAScual.addDockWidget(QtCore.Qt.DockWidgetArea(1),self.plotDockWidget)

        self.toolBar = QtGui.QToolBar(PAScual)
        self.toolBar.setOrientation(QtCore.Qt.Horizontal)
        self.toolBar.setObjectName("toolBar")
        PAScual.addToolBar(QtCore.Qt.TopToolBarArea,self.toolBar)

        self.actionLoad_Spectra = QtGui.QAction(PAScual)
        self.actionLoad_Spectra.setIcon(QtGui.QIcon(":/Icons/Icons/mine/CRfileopen.png"))
        self.actionLoad_Spectra.setObjectName("actionLoad_Spectra")

        self.actionAbout = QtGui.QAction(PAScual)
        self.actionAbout.setIcon(QtGui.QIcon(":/Icons/Icons/mine/PAScual-64x64.png"))
        self.actionAbout.setObjectName("actionAbout")

        self.actionShow_hide_Plot = QtGui.QAction(PAScual)
        self.actionShow_hide_Plot.setObjectName("actionShow_hide_Plot")

        self.actionRegenerateSets = QtGui.QAction(PAScual)
        self.actionRegenerateSets.setIcon(QtGui.QIcon(":/Icons/Icons/mine/yellowbullet.png"))
        self.actionRegenerateSets.setObjectName("actionRegenerateSets")

        self.actionSave_Output_as = QtGui.QAction(PAScual)
        self.actionSave_Output_as.setIcon(QtGui.QIcon(":/Icons/Icons/mine/CRfilesave.png"))
        self.actionSave_Output_as.setObjectName("actionSave_Output_as")

        self.actionSave_results_as = QtGui.QAction(PAScual)
        self.actionSave_results_as.setIcon(QtGui.QIcon(":/Icons/Icons/mine/CRfilesave.png"))
        self.actionSave_results_as.setObjectName("actionSave_results_as")

        self.actionWhat_s_This = QtGui.QAction(PAScual)
        self.actionWhat_s_This.setIcon(QtGui.QIcon(":/Icons/Icons/mine/questionmark.png"))
        self.actionWhat_s_This.setObjectName("actionWhat_s_This")

        self.actionManual = QtGui.QAction(PAScual)
        self.actionManual.setObjectName("actionManual")

        self.actionLicense = QtGui.QAction(PAScual)
        self.actionLicense.setObjectName("actionLicense")

        self.actionSum_Spectra = QtGui.QAction(PAScual)
        self.actionSum_Spectra.setIcon(QtGui.QIcon(":/Icons/Icons/mine/sigma.png"))
        self.actionSum_Spectra.setObjectName("actionSum_Spectra")

        self.actionLoad_Parameters = QtGui.QAction(PAScual)
        self.actionLoad_Parameters.setObjectName("actionLoad_Parameters")

        self.actionSimulate_spectrum = QtGui.QAction(PAScual)
        self.actionSimulate_spectrum.setObjectName("actionSimulate_spectrum")

        self.actionSave_Parameters = QtGui.QAction(PAScual)
        self.actionSave_Parameters.setObjectName("actionSave_Parameters")

        self.actionCopy_Results_Selection = QtGui.QAction(PAScual)
        self.actionCopy_Results_Selection.setObjectName("actionCopy_Results_Selection")
        self.menuFile.addAction(self.actionLoad_Spectra)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSave_Output_as)
        self.menuFile.addAction(self.actionSave_results_as)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSum_Spectra)
        self.menuFile.addAction(self.actionSimulate_spectrum)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionLoad_Parameters)
        self.menuFile.addAction(self.actionSave_Parameters)
        self.menuView.addAction(self.actionShow_hide_Plot)
        self.menuHelp.addAction(self.actionWhat_s_This)
        self.menuHelp.addAction(self.actionManual)
        self.menuHelp.addSeparator()
        self.menuHelp.addAction(self.actionLicense)
        self.menuHelp.addSeparator()
        self.menuHelp.addAction(self.actionAbout)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.toolBar.addAction(self.actionLoad_Spectra)
        self.toolBar.addAction(self.actionSum_Spectra)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionWhat_s_This)
        self.toolBar.addAction(self.actionAbout)

        self.retranslateUi(PAScual)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(PAScual)

    def retranslateUi(self, PAScual):
        PAScual.setWindowTitle(QtGui.QApplication.translate("PAScual", "PAScual", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setWhatsThis(QtGui.QApplication.translate("PAScual", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal; text-decoration:none;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\">The main window tabs give access to most functions of the program</p>\n"
        "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"></p>\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"><span style=\" font-weight:600;\">Parameters</span> Tab: here you can set the initial values for the fitting parameters for each spectrum (background, lifetimes, intensities). You can also set variation limits.</p>\n"
        "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"></p>\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"><span style=\" font-weight:600;\">Fitting</span> Tab: here you can select the type of fit (FitMode) and you launch/stop the fit</p>\n"
        "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"></p>\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"><span style=\" font-weight:600;\">Results</span> Tab: As soon as a set is fitted, the results appear in this tab. You can show/hide parameters.</p>\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\">Selecting a row will show the residuals for that spectrum.</p>\n"
        "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"></p>\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"><span style=\" font-weight:600;\">Output</span> Tab: all the verbose output from the fitting algorithms appears here.</p>\n"
        "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"></p>\n"
        "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"></p>\n"
        "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("PAScual", "Channel width [ps/ch]", None, QtGui.QApplication.UnicodeUTF8))
        self.LEpsperchannel.setToolTip(QtGui.QApplication.translate("PAScual", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal; text-decoration:none;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Picoseconds per Channel</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.BTpsperchannel.setToolTip(QtGui.QApplication.translate("PAScual", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal; text-decoration:none;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\">Apply </p>\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\">Applies this parameter to the selected spectra.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.BTpsperchannel.setText(QtGui.QApplication.translate("PAScual", "A", None, QtGui.QApplication.UnicodeUTF8))
        self.roiPB.setText(QtGui.QApplication.translate("PAScual", " Set ROI", None, QtGui.QApplication.UnicodeUTF8))
        self.componentsGroupBox.setTitle(QtGui.QApplication.translate("PAScual", "Components", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("PAScual", "Number of components", None, QtGui.QApplication.UnicodeUTF8))
        self.showtauRB.setText(QtGui.QApplication.translate("PAScual", "Lifetimes", None, QtGui.QApplication.UnicodeUTF8))
        self.showityRB.setText(QtGui.QApplication.translate("PAScual", "Intensities", None, QtGui.QApplication.UnicodeUTF8))
        self.applycompsBT.setText(QtGui.QApplication.translate("PAScual", "A", None, QtGui.QApplication.UnicodeUTF8))
        self.resetParametersPB.setText(QtGui.QApplication.translate("PAScual", "Reset", None, QtGui.QApplication.UnicodeUTF8))
        self.applyAllParametersPB.setText(QtGui.QApplication.translate("PAScual", "Apply All", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.parametersTab), QtGui.QApplication.translate("PAScual", "Parameters", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("PAScual", "Commands", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("PAScual", "Unasigned:", None, QtGui.QApplication.UnicodeUTF8))
        self.applyFitModeBT.setText(QtGui.QApplication.translate("PAScual", "Apply Fit Mode", None, QtGui.QApplication.UnicodeUTF8))
        self.selectedSetsOnlyCB.setText(QtGui.QApplication.translate("PAScual", "To Selected Only", None, QtGui.QApplication.UnicodeUTF8))
        self.setsTree.setToolTip(QtGui.QApplication.translate("PAScual", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal; text-decoration:none;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Select the sets to which you will apply the commands.</p>\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">If none is selected, It will be applied to All</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.setsTree.headerItem().setText(0,QtGui.QApplication.translate("PAScual", "Set", None, QtGui.QApplication.UnicodeUTF8))
        self.setsTree.headerItem().setText(1,QtGui.QApplication.translate("PAScual", "spectra", None, QtGui.QApplication.UnicodeUTF8))
        self.fitModeCB.setToolTip(QtGui.QApplication.translate("PAScual", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal; text-decoration:none;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\">Select a Fit Mode.</p>\n"
        "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"></p>\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\">A fit mode is a collection of commands that, together, perform a fit. </p>\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\">You can edit a Fit Mode using the table below and save it for re-use.</p>\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\">Each set (on the right) needs to be assigned a Fit Mode.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.saveFitmodeBT.setToolTip(QtGui.QApplication.translate("PAScual", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal; text-decoration:none;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Save the Fit Mode</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.saveFitmodeBT.setText(QtGui.QApplication.translate("PAScual", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("PAScual", "Execution", None, QtGui.QApplication.UnicodeUTF8))
        self.goFitBT.setText(QtGui.QApplication.translate("PAScual", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.skipCommandBT.setText(QtGui.QApplication.translate("PAScual", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.stopFitBT.setText(QtGui.QApplication.translate("PAScual", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("PAScual", "Total", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("PAScual", "Set", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("PAScual", "Command", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.fittingTab), QtGui.QApplication.translate("PAScual", "Fitting", None, QtGui.QApplication.UnicodeUTF8))
        self.hideResultsBT.setText(QtGui.QApplication.translate("PAScual", "Hide", None, QtGui.QApplication.UnicodeUTF8))
        self.showResultsBT.setText(QtGui.QApplication.translate("PAScual", "Show", None, QtGui.QApplication.UnicodeUTF8))
        self.resultsColumnsListWidget.setToolTip(QtGui.QApplication.translate("PAScual", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal; text-decoration:none;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\">You can hide/show columns in the results table</p>\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"> (on the right) by selecting them in this list and</p>\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"> using the Hide/Show buttoms below.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.resultsTable.clear()
        self.resultsTable.setColumnCount(0)
        self.resultsTable.setRowCount(0)
        self.label_9.setText(QtGui.QApplication.translate("PAScual", "Results File", None, QtGui.QApplication.UnicodeUTF8))
        self.resultsFileLE.setText(QtGui.QApplication.translate("PAScual", "PASlog.txt", None, QtGui.QApplication.UnicodeUTF8))
        self.resultsFileSelectBT.setText(QtGui.QApplication.translate("PAScual", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.saveResultsBT.setToolTip(QtGui.QApplication.translate("PAScual", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal; text-decoration:none;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Save the results table to an ASCII file.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.saveResultsBT.setText(QtGui.QApplication.translate("PAScual", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.ResultsTab), QtGui.QApplication.translate("PAScual", "Results", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_3.setTitle(QtGui.QApplication.translate("PAScual", "Previous fits", None, QtGui.QApplication.UnicodeUTF8))
        self.previousOutputCB.addItem(QtGui.QApplication.translate("PAScual", "All fits", None, QtGui.QApplication.UnicodeUTF8))
        self.showPreviousOutputBT.setText(QtGui.QApplication.translate("PAScual", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_4.setTitle(QtGui.QApplication.translate("PAScual", "Current Fit", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("PAScual", "Output File", None, QtGui.QApplication.UnicodeUTF8))
        self.outputFileLE.setText(QtGui.QApplication.translate("PAScual", "PASoutput.txt", None, QtGui.QApplication.UnicodeUTF8))
        self.outputFileSelectBT.setText(QtGui.QApplication.translate("PAScual", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.saveOutputBT.setText(QtGui.QApplication.translate("PAScual", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.OutputTab), QtGui.QApplication.translate("PAScual", "Output", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setTitle(QtGui.QApplication.translate("PAScual", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.menuView.setTitle(QtGui.QApplication.translate("PAScual", "View", None, QtGui.QApplication.UnicodeUTF8))
        self.menuHelp.setTitle(QtGui.QApplication.translate("PAScual", "Help", None, QtGui.QApplication.UnicodeUTF8))
        self.spectraDockWidget.setWhatsThis(QtGui.QApplication.translate("PAScual", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal; text-decoration:none;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Spectra Selection Panel.</p>\n"
        "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p>\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">The loaded spectra appear here.</p>\n"
        "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p>\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">You can <span style=\" font-weight:600; font-style:italic;\">highlight</span> them (by single clicks or block selections) and you can <span style=\" font-weight:600; font-style:italic;\">(un)check</span> them (by clicking on the box, or double-clicking, or using the check/uncheck buttons).</p>\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Any action on the Parameters tab will affect <span style=\" font-style:italic;\">only to the checked</span> spectra.</p>\n"
        "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p>\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">You can add spectra to this panel by loading them.</p>\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">You can remove spectra from this panel by using the remove spectrum button.</p>\n"
        "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.spectraDockWidget.setWindowTitle(QtGui.QApplication.translate("PAScual", "Spectra selection", None, QtGui.QApplication.UnicodeUTF8))
        self.selectAllTB.setToolTip(QtGui.QApplication.translate("PAScual", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal; text-decoration:none;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Check <span style=\" font-weight:600;\">All</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.selectAllTB.setText(QtGui.QApplication.translate("PAScual", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.selectNoneTB.setToolTip(QtGui.QApplication.translate("PAScual", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal; text-decoration:none;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Uncheck All</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.selectNoneTB.setText(QtGui.QApplication.translate("PAScual", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.selectMarkedTB.setToolTip(QtGui.QApplication.translate("PAScual", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal; text-decoration:none;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Check Marked</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.selectMarkedTB.setText(QtGui.QApplication.translate("PAScual", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.removeSpectraTB.setToolTip(QtGui.QApplication.translate("PAScual", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal; text-decoration:none;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Remove checked spectra from list</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.removeSpectraTB.setText(QtGui.QApplication.translate("PAScual", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.plotDockWidget.setWhatsThis(QtGui.QApplication.translate("PAScual", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal; text-decoration:none;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\">Plot panel</p>\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\">This panel shows the graphs for the selected spectra.</p>\n"
        "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"></p>\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\">Note that \"selected\" means \"checked\" in the Spectra Selection pannel, not just highlighted.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.plotDockWidget.setWindowTitle(QtGui.QApplication.translate("PAScual", "Plot", None, QtGui.QApplication.UnicodeUTF8))
        self.actionLoad_Spectra.setText(QtGui.QApplication.translate("PAScual", "Load Spectra", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAbout.setText(QtGui.QApplication.translate("PAScual", "About", None, QtGui.QApplication.UnicodeUTF8))
        self.actionShow_hide_Plot.setText(QtGui.QApplication.translate("PAScual", "Show/hide Plot", None, QtGui.QApplication.UnicodeUTF8))
        self.actionRegenerateSets.setText(QtGui.QApplication.translate("PAScual", "RegenerateSets", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave_Output_as.setText(QtGui.QApplication.translate("PAScual", "Save Output as...", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave_results_as.setText(QtGui.QApplication.translate("PAScual", "Save results  as:", None, QtGui.QApplication.UnicodeUTF8))
        self.actionWhat_s_This.setText(QtGui.QApplication.translate("PAScual", "What\'s This?", None, QtGui.QApplication.UnicodeUTF8))
        self.actionManual.setText(QtGui.QApplication.translate("PAScual", "Manual", None, QtGui.QApplication.UnicodeUTF8))
        self.actionLicense.setText(QtGui.QApplication.translate("PAScual", "License", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSum_Spectra.setText(QtGui.QApplication.translate("PAScual", "Sum Spectra", None, QtGui.QApplication.UnicodeUTF8))
        self.actionLoad_Parameters.setText(QtGui.QApplication.translate("PAScual", "Load Parameters", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSimulate_spectrum.setText(QtGui.QApplication.translate("PAScual", "Simulate spectrum", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave_Parameters.setText(QtGui.QApplication.translate("PAScual", "Save Parameters", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCopy_Results_Selection.setText(QtGui.QApplication.translate("PAScual", "Copy Results (Selection)", None, QtGui.QApplication.UnicodeUTF8))

import PAScual_rc
