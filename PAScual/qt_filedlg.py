
from qwt.qt import API
from qwt.qt.QtGui import QFileDialog

if API == 'pyqt5':
    getSaveFileName = QFileDialog.getSaveFileName
    getOpenFileName = QFileDialog.getOpenFileName

elif API == 'pyqt':
    getSaveFileName = QFileDialog.getSaveFileNameAndFilter
    getOpenFileName = QFileDialog.getOpenFileNameAndFilter

