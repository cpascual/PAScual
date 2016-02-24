'''
	plothistory: script for plotting projections of multivariate solution spaces.
	
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

import pylab
import scipy as S

# TODO: include zipped file support
# TODO: make a GUI (and integrate it as a PAScual tool)

####################################################
## OPTIONS:
histfile = 'PAShist.txt'  # file to load
itys = S.array([3, 4, 5])  # indexes of the itys that we want to normalise
binning = 50  # number of bins for 2dhist (this is squared for 1d hists)

###################################################
# open the file and read the parameter names
f = open(histfile, "r")
f.readline()
f.readline()
p = f.readline().strip()[4:-1]
p = p.split(",")
# for i,name in zip(range(len(p)),p): print i, name;
# raw_input()

# load the history
print "Reading '%s' This may take a while..." % histfile
M = S.loadtxt(f)
# Mbck=M.copy()
f.close()

# calculate relative intensities in %
M[itys, :] *= 100. / M[itys, :].sum(axis=0)


# 2D histograms (interactive)
def make2dhist(fill=True, bins=30, ncolors=64):
    print "************"
    for i, name in zip(range(len(p)), p): print i, name
    print
    i = int(raw_input("parX?"))
    if i < 0: return False
    j = int(raw_input("parY?"))
    if j < 0: return False
    if fill:
        plotcont = pylab.contourf
    else:
        plotcont = pylab.contour
    pylab.clf()
    if i == j:
        pylab.hist(M[i, :], bins=bins ** 2)
    else:
        h2, xb, yb = S.histogram2d(M[i, :], M[j, :], bins=bins)
        xb = 0.5 * (xb[:-1] + xb[1:])
        yb = 0.5 * (yb[:-1] + yb[1:])
        plotcont(xb, yb, h2, ncolors)
        pylab.colorbar()
        # calculate mode:
        imax = h2.argmax()
        ii, jj = imax % h2.shape[0], imax / h2.shape[0]
        print "mode:", xb[ii], yb[jj]
    pylab.show()
    return True


if __name__ == '__main__':
    while make2dhist(fill=True, bins=binning, ncolors=100): pass
    print 'To start again, type: "while make2dhist(fill=False, bins=binning):pass"'
