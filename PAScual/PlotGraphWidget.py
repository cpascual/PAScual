#!/usr/bin/env python

'''
PlotGraphWidget: Widget for plotting spectra. Originally based on an example code from Qwt documentation

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

# import qwt.qt.Qwt5 as Qwt
import qwt as Qwt
import sys
from qwt.qt import QtCore, QtGui
from numpy import *
from qt_filedlg import getSaveFileName

plotcolors_bright = [QtCore.Qt.black, QtCore.Qt.red, QtCore.Qt.blue, QtCore.Qt.magenta,
                     QtCore.Qt.green, QtCore.Qt.cyan, QtCore.Qt.yellow, QtCore.Qt.gray, ]
plotcolors_dark = [QtCore.Qt.darkRed, QtCore.Qt.darkBlue, QtCore.Qt.darkMagenta,
                   QtCore.Qt.darkGreen, QtCore.Qt.darkCyan, QtCore.Qt.darkYellow,
                   QtCore.Qt.darkGray]


class cycliclist(object):
    '''this class provides an effectively cyclic list.
    It can be used, e.g., for storing colors or pen properties to be changed automatically in a plot'''

    def __init__(self, itemlist=[]):
        self.setItemList(itemlist)

    def setItemList(self, itemlist):
        '''sets the item list'''
        self.itemlist = itemlist
        self.index = -1
        self.nitems = len(self.itemlist)

    def current(self):
        '''returns current item'''
        try:
            return self.itemlist[
                self.index % self.nitems]  # makes the list effectively cyclic
        except ZeroDivisionError:
            raise IndexError('cyclic list is empty')

    def setItemIndex(self, index):
        '''sets current item to index and returns it'''
        self.index = index
        return self.current()

    def next(self):
        '''advances one item in the list and returns it'''
        self.index += 1
        return self.current()

    def previous(self):
        '''goes one item back in the list and returns it'''
        self.index -= 1
        return self.current()


# class PlotImage
class PALSplot(Qwt.QwtPlot):
    def __init__(self, *args):
        Qwt.QwtPlot.__init__(self, *args)
        self.YscaleMax = 0
        self.YscaleMin = inf
        self.setAxisScaleEngine(Qwt.QwtPlot.yLeft, Qwt.QwtLogScaleEngine())
        # self.plotLayout().setMargin(0)
        self.plotLayout().setCanvasMargin(0)
        self.plotLayout().setAlignCanvasToScales(True)
        # set a cyclic list of colors to be used for plotting
        self.autocolor = cycliclist(plotcolors_bright)
        # set legend
        legend = Qwt.QwtLegend()
        # legend.setItemMode(Qwt.QwtLegend.ClickableItem)
        self.insertLegend(legend, Qwt.QwtPlot.RightLegend)
        # set axis titles
        self.setAxisTitle(Qwt.QwtPlot.xBottom, 'Channel #')
        self.setAxisTitle(Qwt.QwtPlot.yLeft, 'Yield (Cts)')
        # attach a grid
        grid = Qwt.QwtPlotGrid()
        grid.attach(self)
        grid.setPen(QtGui.QPen(QtCore.Qt.black, 0, QtCore.Qt.DotLine))
        # Connect clicks on toolbar to toggleVisibility
        #self.legendClicked.connect(self.toggleVisibility)
        # replot
        self.replot()
        # set zoomer
        # self.zoomer = Qwt.QwtPlotZoomer(Qwt.QwtPlot.xBottom,
        #                                 Qwt.QwtPlot.yLeft,
        #                                 Qwt.QwtPicker.DragSelection,
        #                                 Qwt.QwtPicker.AlwaysOff,
        #                                 self.canvas())
        # self.zoomer.setRubberBandPen(QtGui.QPen(QtCore.Qt.green))
        # # set picker
        # self.picker = Qwt.QwtPlotPicker(Qwt.QwtPlot.xBottom,
        #                                 Qwt.QwtPlot.yLeft,
        #                                 Qwt.QwtPicker.PointSelection,
        #                                 Qwt.QwtPlotPicker.CrossRubberBand,
        #                                 Qwt.QwtPicker.AlwaysOn,
        #                                 self.canvas())
        # self.picker.setTrackerPen(QtGui.QPen(QtCore.Qt.red))
        self._plotdict = {}
        # 		self.picker.selected.connect( pointselected)
        self.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self._exportPdfAction = QtGui.QAction("Export plot to PDF...", self)
        self._exportPdfAction.triggered.connect(self.exportPdf)
        self.addAction(self._exportPdfAction)

    def attachCurve(self, x, y, name='', pen=None, style="Lines"):
        if pen is None: pen = QtGui.QPen(self.autocolor.next())
        self.YscaleMax = max(self.YscaleMax, 1.2 * max(y))
        self.YscaleMin = min(self.YscaleMin, max(1, 0.5 * min(y)))
        curve = Qwt.QwtPlotCurve(name)
        curve.attach(self)
        curve.setPen(pen)
        curve.setStyle(getattr(Qwt.QwtPlotCurve, style))
        curve.setData(x, where(y == 0, 1e-99, y))
        self._plotdict[name] = curve
        self.clearZoomStack()
        return curve

    def detachCurve(self, name):
        self._plotdict.pop(name).detach()

    def reset(self, *args):
        self._plotdict = {}
        self.autocolor.setItemIndex(-1)

    def toggleVisibility(self, plotItem):
        """Toggle the visibility of a plot item
        """
        plotItem.setVisible(not plotItem.isVisible())
        self.replot()

    def clearZoomStack(self):
        """Auto scale and clear the zoom stack
        """
        self.setAxisAutoScale(Qwt.QwtPlot.xBottom)
        self.setAxisScale(Qwt.QwtPlot.yLeft, self.YscaleMin, self.YscaleMax)
        self.replot()
        # self.zoomer.setZoomBase()

    def exportPdf(self, fileName=None):
        """Export the plot to a PDF. slot for the _exportPdfAction.

        :param fileName: (str) The name of the file to which the plot will be
                         exported. If None given, the user will be prompted for
                         a file name.
        """
        if fileName is None:
            fileName, _ = getSaveFileName(
                self, 'Export File Name',
                'plot.pdf',
                'PDF Documents (*.pdf)',
                '',
                QtGui.QFileDialog.DontUseNativeDialog
            )
        fileName = str(fileName)
        if fileName:
            try:  # check if the file is actually writable
                f = open(fileName, 'w')
                f.close()
            except:
                self.error("Can't write to '%s'" % fileName)
                QtGui.QMessageBox.warning(self, "File Error",
                                       "Can't write to\n'%s'" % fileName,
                                       QtGui.QMessageBox.Ok)
                return
            printer = QtGui.QPrinter()
            printer.setOutputFormat(QtGui.QPrinter.PdfFormat)
            printer.setOrientation(QtGui.QPrinter.Landscape)
            printer.setOutputFileName(fileName)
            printer.setCreator('PAScual')
            self.print_(printer)


class ResPlot(Qwt.QwtPlot):
    def __init__(self, *args):
        Qwt.QwtPlot.__init__(self, *args)
        self.YscaleMax = 2
        self.YscaleMin = -2
        self.setAxisScale(Qwt.QwtPlot.yLeft, self.YscaleMin, self.YscaleMax)
        # self.plotLayout().setMargin(0)
        self.plotLayout().setCanvasMargin(0)
        self.plotLayout().setAlignCanvasToScales(True)
        # set a cyclic list of colors to be used for plotting
        self.autocolor = cycliclist(plotcolors_bright)
        # 		# set legend
        # 		legend = Qwt.QwtLegend()
        # 		legend.setItemMode(Qwt.QwtLegend.ClickableItem)
        # 		self.insertLegend(legend, Qwt.QwtPlot.RightLegend)
        # set axis titles
        self.setAxisTitle(Qwt.QwtPlot.xBottom, 'Channel #')
        self.setAxisTitle(Qwt.QwtPlot.yLeft, '(Y-f)/DY')
        # attach a grid
        grid = Qwt.QwtPlotGrid()
        grid.attach(self)
        grid.setPen(QtGui.QPen(QtCore.Qt.black, 0, QtCore.Qt.DotLine))
        # 		# Connect clicks on toolbar to toggleVisibility
        # 		self.connect(self,
        # 		             Qt.SIGNAL("legendClicked(QwtPlotItem*)"),
        # 		             self.toggleVisibility)
        # replot
        self.replot()
        # set zoomer
        # self.zoomer = Qwt.QwtPlotZoomer(Qwt.QwtPlot.xBottom,
        #                                 Qwt.QwtPlot.yLeft,
        #                                 Qwt.QwtPicker.DragSelection,
        #                                 Qwt.QwtPicker.AlwaysOff,
        #                                 self.canvas())
        # self.zoomer.setRubberBandPen(QtGui.QPen(QtCore.Qt.green))
        # 		# set picker
        # 		self.picker = Qwt.QwtPlotPicker(Qwt.QwtPlot.xBottom,
        # 									Qwt.QwtPlot.yLeft,
        # 									Qwt.QwtPicker.PointSelection,
        # 									Qwt.QwtPlotPicker.CrossRubberBand,
        # 									Qwt.QwtPicker.AlwaysOn,
        # 									self.canvas())
        # 		self.picker.setTrackerPen(QtGui.QPen(QtCore.Qt.red))
        self._plotdict = {}
        # 		self.picker.selected.connect( pointselected)
        self.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self._exportPdfAction = QtGui.QAction("Export plot to PDF...", self)
        self._exportPdfAction.triggered.connect(
                     self.exportPdf)
        self.addAction(self._exportPdfAction)

    def attachCurve(self, x, y, name='', pen=None):
        if pen is None: pen = QtGui.QPen(self.autocolor.next(), 2)
        self.YscaleMax = min(10, 1.2 * max(y))
        self.YscaleMin = max(-10, 1.2 * min(y))
        curve = Qwt.QwtPlotCurve(name)
        curve.attach(self)
        curve.setPen(pen)
        curve.setStyle(Qwt.QwtPlotCurve.Dots)
        curve.setData(x, where(y == 0, 1e-99, y))
        self._plotdict[name] = curve
        self.clearZoomStack()
        return curve

    def detachCurve(self, name):
        self._plotdict.pop(name).detach()

    def reset(self, *args):
        self._plotdict = {}
        self.autocolor.setItemIndex(-1)

    # 	def toggleVisibility(self, plotItem):
    # 		"""Toggle the visibility of a plot item
    # 		"""
    # 		plotItem.setVisible(not plotItem.isVisible())
    # 		self.replot()
    def clearZoomStack(self):
        """Auto scale and clear the zoom stack
        """
        self.setAxisAutoScale(Qwt.QwtPlot.xBottom)
        self.setAxisScale(Qwt.QwtPlot.yLeft, self.YscaleMin, self.YscaleMax)
        self.replot()
        # self.zoomer.setZoomBase()

    def sizeHint(self):
        return QtCore.QSize(300, 150)

    def exportPdf(self, fileName=None):
        """Export the plot to a PDF. slot for the _exportPdfAction.

        :param fileName: (str) The name of the file to which the plot will be
                         exported. If None given, the user will be prompted for
                         a file name.
        """
        if fileName is None:
            fileName, _ = getSaveFileName(
                self, 'Export File Name',
                'plot.pdf',
                'PDF Documents (*.pdf)',
                '',
                QtGui.QFileDialog.DontUseNativeDialog
            )
        fileName = str(fileName)
        if fileName:
            try:  # check if the file is actually writable
                f = open(fileName, 'w')
                f.close()
            except:
                self.error("Can't write to '%s'" % fileName)
                QtGui.QMessageBox.warning(self, "File Error",
                                       "Can't write to\n'%s'" % fileName,
                                       QtGui.QMessageBox.Ok)
                return
            printer = QtGui.QPrinter()
            printer.setOutputFormat(QtGui.QPrinter.PdfFormat)
            printer.setOrientation(QtGui.QPrinter.Landscape)
            printer.setOutputFileName(fileName)
            printer.setCreator('PAScual')
            self.print_(printer)


def make():
    demo = PALSplot()
    demo.resize(600, 400)
    # Some fake data
    x = arange(-2 * pi, 2 * pi, 0.01)
    y = 10 + pi * sin(x)
    y[-1] = 0  # to check the log
    z = 10 + 4 * pi * cos(x) * cos(x) * sin(x)
    demo.attachCurve(x, z, name='y = 10+4*pi*sin(x)*cos(x)**2',
                     pen=QtGui.QPen(QtCore.Qt.black, 2), style='Dots')
    demo.attachCurve(x, y, name='y = 10+pi*sin(x)')
    demo.attachCurve(x, 2 * z, name='y = 20+8*pi*sin(x)*cos(x)**2')
    demo.show()

    demo2 = ResPlot()
    y = sin(10 * x)
    demo2.attachCurve(x, y)
    demo2.show()

    return demo


# make()

def pointselected(pos):
    print pos.x()


def main(args):
    app = QtGui.QApplication(args)
    demo = make()
    sys.exit(app.exec_())


# main()


# Admire
if __name__ == '__main__':
    main(sys.argv)

# Local Variables: ***
# mode: python ***
# End: ***
