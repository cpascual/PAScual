'''
	This file is part of PAScual.
    PAScual: Positron Annihilation Spectroscopy data analysis
    Copyright (C) 2007  Carlos Pascual-Izarra <carlos.pascual-izarra@csiro.au>

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
'''
import sys, os, copy
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PAScual import discretepals,palsset


#set names for column numbers 
_ncolumns=8
[SEL,NAME,ROI,PSPC,FWHM,BG,C0,COMP]=range(_ncolumns)

import qrc_PAScual

#Spectra Table Model			
class PASspectraTableModel(QAbstractTableModel):	
	def __init__(self,spectra=[]):
		super(PASspectraTableModel,self).__init__()
		self.spectra=spectra
		self.ncolumns=_ncolumns
		self.redbulletIcon=QIcon(":/Icons/Icons/mine/redbullet.png")
		self.greenbulletIcon=QIcon(":/Icons/Icons/mine/greenbullet.png")
	def rowCount(self,index=QModelIndex()):
		return len(self.spectra)
	def columnCount(self,index=QModelIndex()):
		return self.ncolumns
		
	def data(self, index, role=Qt.DisplayRole):
		if not index.isValid() or not (0 <= index.row() < self.rowCount()):
			return QVariant()
		dp = self.spectra[index.row()]
		column = index.column()
		#Display Role
		if role == Qt.DisplayRole:
			if column == NAME: return QVariant(QString(dp.name))
			elif column == ROI: 
				if dp.roi is None: return QVariant("-")
				else: return QVariant(QString.number(dp.roi.size))
			elif column == COMP: 
				if dp.taulist is None: ncomp=0
				else: ncomp=len(dp.taulist)
				return QVariant(QString.number(ncomp))
		#CheckState Role
		elif role == Qt.CheckStateRole :
			if column == SEL: return QVariant(dp.selected)

		elif role == Qt.DecorationRole:
			if column == PSPC: bad= (dp.psperchannel is None)
			elif column == FWHM:  bad= (dp.fwhm is None)
			elif column == C0:  bad= (dp.c0 is None)
			elif column == BG:  bad= (dp.bg is None)
			else: return QVariant()
			if bad: return QVariant(self.redbulletIcon)
			else: return QVariant(self.greenbulletIcon)
		#Alignment 
# 		elif role == Qt.TextAlignmentRole:
# 			return QVariant(int(Qt.AlignHCenter|Qt.AlignVCenter))
		#Background Color
		elif role == Qt.TextColorRole:
			if column == NAME:
				if dp.isready(): return QVariant(QColor(Qt.darkGreen))
			if column == COMP:
				if dp.taulist is None:	return QVariant(QColor(Qt.red))
				elif len(dp.taulist)==0: return QVariant(QColor(Qt.red))
				else: 	return QVariant(QColor(Qt.green))
		elif role == Qt.UserRole :
			return dp					
		return QVariant()

	def headerData(self, section, orientation, role=Qt.DisplayRole):
		if role == Qt.TextAlignmentRole:
			if orientation == Qt.Horizontal:
				return QVariant(int(Qt.AlignLeft|Qt.AlignVCenter))
			return QVariant(int(Qt.AlignRight|Qt.AlignVCenter))
# 		elif role == Qt.CheckStateRole :
# 			if not orientation == Qt.Horizontal: return QVariant(True)
		if role != Qt.DisplayRole:
			return QVariant()
		#So this is DisplayRole...
		if orientation == Qt.Horizontal:
			if section == SEL: return QVariant("Sel")
			elif section == NAME: return QVariant("Spectrum Name")
			elif section == ROI: return QVariant("ROI")
			elif section == PSPC:	return QVariant("CW")
			elif section == C0:	return QVariant("c0")
			elif section == BG:	return QVariant("Bg")
			elif section == FWHM:	return QVariant("R")
			elif section == COMP:	return QVariant("C")
			return QVariant()
		else: 
			return QVariant()
 					
	def flags(self, index): #use this to set the editable flag when fix is selected
		if not index.isValid():
			return Qt.ItemIsEnabled
		column=index.column()
		if column == NAME: return Qt.ItemFlags(QAbstractTableModel.flags(self, index) )
		if column == SEL: return Qt.ItemFlags(Qt.ItemIsEnabled|Qt.ItemIsUserCheckable)
		return Qt.ItemFlags(Qt.ItemIsEnabled) 
	
		
	def setData(self, index, value=None, role=Qt.EditRole):
		if index.isValid() and (0 <= index.row() < self.rowCount()):
			dp = self.spectra[index.row()]
			column=index.column()
			if column==SEL:	
				dp.selected=not dp.selected
				self.emit(SIGNAL("selectionChanged"),dp,index) #this is a custom signal to warn that the 'hard' selection changed
			self.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"),index, index)
			return True
		return False
	def insertRows(self, position=None,rows=1,index=QModelIndex(),dps=None):
		if position is None: position=self.rowCount()
		self.beginInsertRows(QModelIndex(), position, position + rows - 1)
		if dps is None:
			dps=[]
			for row in range(rows): dps.append(discretepals(name=u"new"))
		for row in range(rows):
# 			dp=discretepals(name=u"new")
			self.spectra.insert(position + row, dps[row])
			self.emit(SIGNAL("selectionChanged"),dps[row],self.index(position + row, SEL))
		self.endInsertRows()
		return True
	def removeRows(self, position,rows=1,index=QModelIndex()):
		self.beginRemoveRows(QModelIndex(), position, position + rows - 1)
		self.spectra= self.spectra[:position]+self.spectra[position+rows:]
		self.endRemoveRows()
		return True
	def getselectedspectra(self):
		seldp=[]
		seldpi=[]
		for r in range(self.rowCount()):
			if self.spectra[r].selected: 
				seldp.append(self.spectra[r])
				seldpi.append(self.index(r,NAME))
		return seldp,seldpi
	def checkAll(self,value=True):
		if self.spectra==[]:return
		indexlist=[self.index(i,SEL) for i in range(len(self.spectra))]
		for dp,idx in zip (self.spectra, indexlist):
			if dp.selected!=value:
				dp.selected=value
				self.emit(SIGNAL("selectionChanged"),dp,idx)
		self.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"),indexlist[0], indexlist[-1])
	def removeChecked(self):
		temp=[]
		for dp in self.spectra:
			if dp.selected: 
				dp.selected=False
				self.emit(SIGNAL("selectionChanged"),dp,None)
			else: temp.append(dp)
		self.spectra=temp
		self.reset()
	def dumpData(self):
		return copy.deepcopy(self.spectra)
	def loadData(self,data):
		self.spectra=data
		self.reset()
# 	def parent(self, index):
# 		if index.row()%2: return
		
		
# 	def getselectedspectraindexes(self):
# 		seldpi=[]
# 		for r in range(self.rowCount()):
# 			if self.spectra[r].selected: seldpi.append(self.index(r,NAME))
# 		return seldpi
		
# 	#Delegate
# class mydelegate(QItemDelegate):
# 	def __init__(self, parent=None):
# 		super(mydelegate,self).__init__(parent)
# 	def createEditor(self,parent,option,index):
# 		print 'AAAAAAAAAAA',index.column()
# 		if index.column()==0:
# 			print '!!'
# 			return QItemDelegate.createEditor(self,parent,option,index)
# 		else: 
# 			return QItemDelegate.createEditor(self,parent,option,index)
		
class demo(QDialog):
	def __init__(self, parent=None):
		super(demo,self).__init__(parent)
		#generate fake spectra
		spectra=[]
		for i in range(4): spectra.append(discretepals(name=u"spect%i"%i))
		
		self.table=QTableView(self)
		self.model=PASspectraTableModel(spectra)
		self.table.setModel(self.model)
		
		self.tree=QTreeWidget(self)
		self.tree.setColumnCount(1)
		self.tree.setHeaderLabels(["Name"])
# 		sets
		
# 		self.table.setItemDelegate(mydelegate(self))
		
		self.posSB=QSpinBox()
		self.newSB=QSpinBox()
		self.addBT=QPushButton(u"Add")	
		self.remBT=QPushButton(u"Rem")		
		self.dataBT=QPushButton(u"Data")
		self.allBT=QPushButton(u"Check All")
		
		mainLayout=QGridLayout()
		mainLayout.addWidget(self.table,0,0)
		mainLayout.addWidget(self.tree,0,1)
		mainLayout.addWidget(self.posSB,1,0)
		mainLayout.addWidget(self.newSB,1,1)
		mainLayout.addWidget(self.addBT,2,0)
		mainLayout.addWidget(self.remBT,2,1)
		mainLayout.addWidget(self.dataBT,3,0)
		mainLayout.addWidget(self.allBT,3,1)
		self.setLayout(mainLayout)
		
		QObject.connect(self.addBT,SIGNAL("clicked()"),self.onAdd)
		QObject.connect(self.remBT,SIGNAL("clicked()"),self.onRem)
		QObject.connect(self.dataBT,SIGNAL("clicked()"),self.onData)
		QObject.connect(self.allBT,SIGNAL("clicked()"),self.model.checkAll)
		self.table.resizeColumnsToContents()
# 		self.tree.resizeColumnsToContents()
		self.table.setShowGrid(False)
		self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
	def onAdd(self):
		self.model.insertRows(position=self.posSB.value(),rows=self.newSB.value())
	def onRem(self):
		self.model.removeRows(position=self.posSB.value(),rows=self.newSB.value())
	def onData(self):
		s=self.table.selectionModel().selectedRows()
		for idx in s:
			dp=self.model.data(idx, role=Qt.UserRole)
			print dp.name

if __name__ == "__main__":
 	app = QApplication(sys.argv)
	form = demo()
# 	form.resize(800, 400)
	form.show()
	sys.exit(app.exec_())
