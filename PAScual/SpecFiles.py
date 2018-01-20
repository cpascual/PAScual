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

'''
Some convenience classes are defined to work with loading spectra in various formats.
'''

import scipy as S


class spectrumFileLoader(object):
    '''This is an abstract class for implementing derived File Loader classes'''

    def __init__(self, name=''):
        self.name = name
        self.formatDescription = ''
        self.filenamefilter = '*'
        self.needExtraInput = False

    def expdata(self, fname):
        '''This function has to be implemented in the derived classes.
        It gets the file name of the file to read
        It must return an array of doubles containing the spectrum yields (or None if it couldn t load)'''
        return None

    def getDiscretePals(self, fname):
        '''This function has to be implemented in the derived classes.
        It gets the file name of the file to read
        It must return discretepals object (or None if it couldn t load)'''
        return None

    def askExtraInput(self):
        pass


class MAESTROfileLoader(spectrumFileLoader):
    def __init__(self, name='MAESTRO'):
        spectrumFileLoader.__init__(self, name)
        self.formatDescription = 'Binary format from Ortec'
        self.filenamefilter = '*.chn'

    def expdata(self, fname):
        import CHNfiles
        hdr, expdata = CHNfiles.CHN.readCHN(fname)
        return S.array(expdata, dtype='d')


class ASCIIfileloader(spectrumFileLoader):
    def __init__(self, name='ASCII', filenamefilter='*', hdrlines=None,
                 description=None, askmode='t', Qtparent=None):
        spectrumFileLoader.__init__(self, name)
        self.filenamefilter = filenamefilter
        if description is None:
            self.formatDescription = 'File containing yields separated by any blank space'
        else:
            self.formatDescription = description
        self.hdrlns = hdrlines
        if self.hdrlns is None: self.needExtraInput = True
        self.askmode = askmode
        self.Qtparent = Qtparent

    def expdata(self, fname):
        if self.hdrlns is None: self.needExtraInput = True
        if self.needExtraInput: self.askExtraInput()
        expdata = S.loadtxt(fname, skiprows=self.hdrlns, dtype='d').flatten()
        return expdata

    def askExtraInput(self, mode='t'):
        '''It asks for the header lines to skip using either text (mode="t")or Qt (mode="qt") interface.'''
        if self.askmode == 't':
            # asks in text mode
            self.hdrlns = self.int(
                raw_input('Number of lines to skip in the header?'))
            okflag = True
        if self.askmode == 'qt':
            # Asks via a qt dialog. This assumes that Qt is installed. You must provide a parent for the dialog
            from qwt.qt.QtGui import QInputDialog
            if self.hdrlns is None:
                dflt = 0
            else:
                dflt = self.hdrlns
            self.hdrlns, okflag = QInputDialog.getInteger(
                self.Qtparent, "Header lines?",
                "Number of lines to skip in the header:", dflt, 0, 999, 1)
        return okflag


class PAScualfileLoader(spectrumFileLoader):
    def __init__(self, name='PAScual'):
        spectrumFileLoader.__init__(self, name)
        self.formatDescription = 'Pickled Spectrum from PAScual'
        self.filenamefilter = '*.ps1'

    def getDiscretePals(self, fname):
        import pickle
        dp = pickle.load(open(fname, 'rb'))
        return dp

    def expdata(self, fname):
        dp = self.getDiscretePals(fname)
        return S.array(dp.exp, dtype='d')
