'''
TEcalc, Tao-Eldrup calculator (text mode interface).

Translates oPs lifetime into pore size using the Tao-Eldrup model and also the "Rectangular Tao-Eldrup model"

See: TL Dull et al., J. Phys Chem B 105, 4657 (2001) 
'''
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

from pyTaoEldrup import *


def raw_inputdflt(prompt, dflt=None):
    """Like  raw_input() but it accepts a default answer.
    """
    if dflt:
        prompt = "%s[%s] " % (prompt, dflt)
        res = raw_input(prompt)
    if not res and dflt:
        return dflt
    return res


# ////////////////////////////////MAIN FUNCTION\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

def TEcalc():
    print 'Tao-Eldrup Calculator, v0.3'
    print '(C) 2007 Carlos Pascual-Izarra\n'
    T = 298.
    cont = True
    while (cont):
        try:
            tau = float(raw_input('oPs lifetime? (ns) (enter 0 to finish) '))
        except ValueError:
            continue
        if tau > 0:
            T = float(raw_inputdflt('Temperature? (Kelvin)', T))
            if tau < 15.:
                R = TE_radius(tau)
                print '\nOriginal TE model: Sphere radius= %.5lg nm or %.5lg nm (hard sphere) ' % (
                R, R + TE_softwall)
            else:
                print 'Original TE model: (out of range)'
            a = RTE_cube(tau, T)
            print 'RTE model: Cube side= %.5lg nm' % a
            R = a / 2. - TE_softwall
            print 'RTE model: Equivalent sphere radius= %.5lg nm or %.5lg nm (hard sphere) ' % (
            R, R + TE_softwall)
            print 'RTE model: Square channel side= %.5lg nm' % RTE_channel(tau,
                                                                           T)
            print 'RTE model: Sheet spacing= %.5lg nm\n' % RTE_sheet(tau, T)
        else:
            cont = False


def PlotCurves():
    try:
        import pylab
    except ImportError:
        print '\nError: you need http://matplotlib.sourceforge.net/ installed on your computer for PlotCurves to work'
        print 'See http://matplotlib.sourceforge.net/\n'
        return
    T = 298.
    mfp = S.concatenate(
        (S.arange(.3, 10, .1), S.arange(10, 100, 1.), S.arange(100, 500, 10)))
    R = (3. / 4.) * mfp - TE_softwall
    a_cube = mfp * 1.5
    a_chann = mfp
    a_sheet = 0.5 * mfp
    v_RTE = S.vectorize(RectangularTaoEldrup)
    v_TE = S.vectorize(TaoEldrup)
    lim = 25
    pylab.ylabel('oPs lifetime (ns)')
    pylab.xlabel('Mean free path(nm)')
    pylab.gca().set_xscale('log')
    pylab.plot(mfp[:lim], v_TE(R[:lim]), 'r-.')
    pylab.plot(mfp, v_RTE(a_cube, a_cube, a_cube, T), '-')
    pylab.plot(mfp, v_RTE(a_chann, a_chann, S.inf, T), ':')
    pylab.plot(mfp, v_RTE(a_sheet, S.inf, S.inf, T), '--')
    pylab.show()


if __name__ == '__main__':
    TEcalc()
# 	PlotCurves()
