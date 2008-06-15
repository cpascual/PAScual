'''
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
'''


import sys
import scipy as S
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from ROISelectorDlg import ROISelectorDialog
import PAScual_rc

class GainAndFWHMPage(QWizardPage):
	def __init__(self, parent=None, psperchannel=50., FWHM=300.):
		super(QWizardPage, self).__init__(parent)
		self.setTitle("Channel Width")
		self.setSubTitle("""Please enter the Channel width (aka "ps per channel" or "gain") and the resolution (aka "FWHM") for your experimental set-up.""")
		
		#The spinbox
		self.psperchannelSB=QDoubleSpinBox()
		self.psperchannelSB.setRange(0,1000)
		self.psperchannelSB.setDecimals (1)
		self.psperchannelSB.setValue(psperchannel)
		
		self.FWHMSB=QDoubleSpinBox()
		self.FWHMSB.setRange(0,9999)
		self.FWHMSB.setDecimals (1)
		self.FWHMSB.setValue(FWHM)
		
		layout=QGridLayout()
		layout.addWidget(QLabel("Channel width [ps/ch]: "), 0, 0, 1, 1, Qt.AlignRight)
		layout.addWidget(self.psperchannelSB, 0, 1, 1, 1, Qt.AlignLeft)
		layout.addWidget(QLabel("FWHM [ps]: "), 1, 0, 1, 1, Qt.AlignRight)			
		layout.addWidget(self.FWHMSB, 1, 1, 1, 1, Qt.AlignLeft)
		self.setLayout(layout)
		
		#register fields
		self.registerField("psperchannel",self.psperchannelSB, "value","valueChanged()")
		self.registerField("FWHM",self.FWHMSB, "value","valueChanged()")
	
	def validatePage(self):
		w=self.wizard()
		w.psperchannel=self.field("psperchannel")
		w.FWHM=self.field("FWHM")
		return True
		
class ROIPage(QWizardPage):
	def __init__(self, parent=None, selected=None):
		super(QWizardPage, self).__init__(parent)
		
		self.setTitle("Region of Interest")
		self.setSubTitle("""Please set the required Region Of Interest for the spectra.""")
		
		self.ROIsel=ROISelectorDialog(selected=selected, widgetmode=True)
		self.ROIsel.buttonBox.setVisible(False) # We don't want the OK|Cancel buttons of the ROI selector. We use the wizard ones instead
		self.connect(self.ROIsel,SIGNAL('rejected()'), parent, SLOT("reject()")) #if the user rejects the selector (e.g. ESC key pressed), the signal is passed to the wizard
		
		layout=QHBoxLayout()
		layout.addWidget(self.ROIsel)
		self.setLayout(layout)
		
		#set default values:
		self.ROIsel.lowerlimRelCB.setChecked(True)
		self.ROIsel.lowerlimSB.setMinimum(-5)
		self.ROIsel.lowerlimSB.setValue(-5)
		
		#register fields
		self.registerField("lowerlimRel",self.ROIsel.lowerlimRelCB, "checked","toggled()")
		self.registerField("lowerlim",self.ROIsel.lowerlimSB, "value","valueChanged()")
		self.registerField("upperlimRel",self.ROIsel.upperlimRelCB, "checked","toggled()")
		self.registerField("upperlim",self.ROIsel.upperlimSB, "value","valueChanged()")

		
	def validatePage(self):
		w=self.wizard()
		w.lowerlim=self.field("lowerlim")
		w.lowerlimRel=self.field("lowerlimRel")
		w.upperlim=self.field("upperlim")
		w.upperlimRel=self.field("upperlimRel")
		return self.ROIsel.checkAndApply()
		
		
class SummaryPage(QWizardPage):
	def __init__(self, parent=None, selected=None):
		super(QWizardPage, self).__init__(parent)
			
		self.setTitle("Summary")
		self.setSubTitle("""Review the results from your choices and finish if you agree""")
		
		self.summary=QTextEdit("!!!!")
		self.summary.setReadOnly(True)
		
		layout=QVBoxLayout()
		layout.addWidget(self.summary)		
		
		self.setLayout(layout)
		
	def initializePage(self):
		w=self.wizard()
		#retrieve / calculate all the parameters
		w.roilist=w.ROIPage.ROIsel.roilist
		w.bg=S.zeros(len(w.selected))
		w.deltabg=S.zeros(len(w.selected))
		for i in xrange(len(w.selected)):
			nbgroi=min(10,0.1*w.roilist[i].size)
			w.bg[i]=w.selected[i].exp[w.roilist[i][-nbgroi:]].mean()
			w.deltabg[i]=10*max(10,S.sqrt(w.bg[i]),w.selected[i].exp[w.roilist[i][-nbgroi:]].std())
		#set the summary
		self.summary.setText(self.buildSummary())
		
	def buildSummary(self):
		w=self.wizard()
		summary="According to your selections, the following parameters will be set:<ul>"
		for i in xrange(len(w.selected)):
			summary+="<li><b>%s</b>: %.1f ps/ch  ; FWHM=%.1f; ROI: %i-%i  ; bg=%.0f  </li>"%(w.selected[i].name, w.psperchannel.toDouble()[0], w.FWHM.toDouble()[0], w.roilist[i][0], w.roilist[i][-1], w.bg[i])
		summary+="</ul>"
		return summary	
	

		
		
class ParamWizard(QWizard):
	def __init__(self, parent, selected=None, psperchannel=50., FWHM=300.):
		'''A wizard for setting some parameters of spectra.
		selected is a list containing spectra to which the settings will apply'''
		super(ParamWizard, self).__init__(parent)
		self.setWindowTitle("PAScual- Parameter setting wizard")
# 		self.setWindowIcon(QIcon("qrc:/icons/Icons/mine/PAScual-64x64.png"))
# 		self.setWizardStyle(self.ModernStyle)
# 		logo=QPixmap()
# 		logo.load("qrc:/Icons/mine/PAScual-64x64.png")
# 		self.setPixmap(self.LogoPixmap, logo)
		
		self.selected=selected
		self.roilist=None
		self.bg=None
		self.deltabg=None
		
 		
 		self.launchOnLoad=True
 		
		#Insert pages
		self.GainAndFWHMPage=GainAndFWHMPage(psperchannel=psperchannel,FWHM=FWHM)
		self.ROIPage=ROIPage(parent=self, selected=self.selected)
		self.SummaryPage=SummaryPage(selected=selected)
		
		self.addPage(self.GainAndFWHMPage)
		self.addPage(self.ROIPage)
		self.addPage(self.SummaryPage)
		
	def setSelected(self,selected):
		self.selected=selected
		self.ROIPage.ROIsel.resetSelected(selected)
				
	def restorelast(self):
		self.setField("psperchannel",self.psperchannel)
		self.setField("FWHM",self.FWHM)
		self.setField("lowerlimRel",self.lowerlimRel)
		self.setField("lowerlim",self.lowerlim)
		self.setField("upperlimRel",self.upperlim)
		self.setField("upperlim",self.upperlim)
		
		
		
if __name__ == "__main__":
	from PAScual import discretepals
	#fake data
	dp2=discretepals(name="fake2",expdata=S.arange(1024)*2)
	dp3=discretepals(name="fake3",expdata=S.arange(1024)*3)
	dp2.exp[22]=22000
	dp3.exp[33]=33000
	selected=[dp2,dp3]
	
 	app = QApplication(sys.argv)
	form = ParamWizard(None,selected)
	form.connect(app,SIGNAL('focusChanged(QWidget *, QWidget *)'),form.ROIPage.ROIsel.onFocusChanged) #manage the focus events (needed for mouse selection in ROI)
	form.show()
	sys.exit(app.exec_())
