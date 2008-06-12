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

import sys,time
from PyQt4.QtCore import *
from PyQt4.QtGui import *

__DEFAULTCHECKINTERVAL__=14 # Interval between checks by default
__RETRYONERROR__=1 #In case of error downloading, the next check will be scheduled in this many days (set to a very high value to disable this)

class updater(QDialog):
	def __init__(self, parent=None, WindowTitle=None, text='', currver='0.0.0',url=''):
		super(updater,self).__init__(parent)
		self.currver=currver
		self.url=url
		if WindowTitle is not None:self.setWindowTitle(WindowTitle)
		self.text=QLabel(text)
		self.daysSB=QSpinBox()
		self.daysSB.setRange(0,365)
		self.daysSB.setValue(__DEFAULTCHECKINTERVAL__)
		self.buttonBox=QDialogButtonBox(QDialogButtonBox.Yes | QDialogButtonBox.No)
		QObject.connect(self.buttonBox,SIGNAL("accepted()"),self.check_for_Updates)
		QObject.connect(self.buttonBox,SIGNAL("rejected()"),self.reject)
		QObject.connect(self,SIGNAL("finished(int)"),self.onClose)
		layout2=QHBoxLayout()
		layout2.addWidget(QLabel("(you will be reminded again in "))			
		layout2.addWidget(self.daysSB)
		layout2.addWidget(QLabel(" days) "))			
		layout=QVBoxLayout()
		layout.addWidget(self.text)
		layout.addLayout(layout2)
		layout.addWidget(self.buttonBox)
		self.setLayout(layout)		
		
	def setCurrVer(self,currverr):
		self.currver=currver
		
	def checkLastReleaseVersion(self,url):
		'''returns the version string found in the provided url (or None if there was a problem)'''
		import socket
		import urllib2
		socket.setdefaulttimeout(10)
		try: f=urllib2.urlopen(url)
		except:
			#raise	 #uncomment this line for debug
			return None #return None if something went wrong
		return f.read().strip()
		
	def compareversions(self, v1, v2):
		'''Compares the major and minor version numbers from version strings. Returns -1 if v1<v2, 0 if v1=v2 and 1 if v1>v2'''
		v1=v1.split('.',2)
		v2=v2.split('.',2)
		cmpmajor=cmp(int(v1[0]),int(v2[0]))
		if cmpmajor!=0:	return cmpmajor
		else: return cmp(int(v1[1]),int(v2[1]))

	def check_for_Updates(self,url=None):
		if url is None: url=self.url
		answer=QMessageBox.Retry
		lastrls=None
		while(answer==QMessageBox.Retry):
			lastrls=self.checkLastReleaseVersion(url)
			if lastrls is not None: break #if we get something, stop trying
			answer=QMessageBox.warning(self, "Update Check Failed","""PAScual could not fetch the latest release information"""
																	"""<p>Typical causes are: <ul>"""
																	"""<li>A problem with the server</li>"""
																	"""<li>Your firewall blocking PAScual</li></ul></p>""",QMessageBox.Retry|QMessageBox.Cancel)
		#we are out of the loop. It can be either that we have a version or that the user aborted.
		if lastrls is None: 
			self.daysSB.setValue(__RETRYONERROR__)
		else:
			if self.compareversions(self.currver,lastrls)<0: 
				QMessageBox.information(self, "Update recommended","""<p>You are currently running v%s.</p>"""
																"""<p>A newer version (v%s) is available.</p>"""
																"""<p>Newer versions correct bugs and introduce more features and documentation</p>"""
																"""<p><b>Updating is recommended</b></p>"""
																"""<p>Click <a href="%s">here</a> to download the newest version</p>"""%(self.currver,lastrls,url[:-3]+"php"))
			else:
				QMessageBox.information(self, "Current version is up-to-date","""<p>The version that you are running (v%s) seems up-to-date.</p>"""
																			"""<p>If you want to be informed of new releases of PAScual,"""
																			"""consider joining the <a href="https://lists.sourceforge.net/lists/listinfo/pascual-info">PAScual-Info mailing list</a>.</p>"""%(self.currver))
			self.accept() #close the updater dialog
			
	def onClose(self,result=None):
		self.nextupdatechk=int(time.time()+3600*24*self.daysSB.value()) #schedule next check
		
		
		
if __name__ == "__main__":
 	app = QApplication(sys.argv)
	form = updater(None,"Updater","Do you want to check for updates?","1.0.1","http://pascual.sf.net/lastrls.txt")
	form.show()
	sys.exit(app.exec_())
