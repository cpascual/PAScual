#!c:\Python25\python.exe
###!/usr/bin/env python
##Make sure to use the appropriate shebang line for your system (check the path to the python binary!).
'''
pyTaoEldrup, Collection of Python functions for (extended) Tao-Eldrup calculations.
pyTaoEldrup is used by the TEcalc, webTEcalc and TEcalcGUI applications.

by Carlos Pascual-Izarra < cpascual [AT] users.sourceforge.net >  (2007)

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
import scipy as S
import scipy.optimize

# Import Psyco if available (Psyco is a optimization compiler)
try:
    import psyco

    psyco.full()
except ImportError:
    pass

TE_softwall = 0.1656
RTE_softwall = 0.19


def TaoEldrup(R, deltaR=0.1656):
    '''The Tao-Eldrup formula. R is in nm, tau is returned in ns
    deltaR is an empirical parameter for the T-E model, normally=0.1656nm
    Note: A constant is used: spin averaged Ps annihilation rate=(Ls+Lt)/4=2.0053 ns^-1
        where Ls and Lt are the vacuum annihilation rates for pPs and oPs, respectively
    '''
    x = float(R) / float(R + deltaR)
    G = (1. - x + 0.5 * S.sin(2. * S.pi * x) / S.pi)
    rate = 2.0053 * G
    return 1. / rate


def TE_radius(tau, Rguess=0.3, deltaR=0.1656):
    '''returns the spherical pore radius (in nm) for a given tau (oPs lifetime, in ns),
    by numerically solving the Tao-Eldrup equation (Newton method)
    deltaR is an empirical parameter for the T-E model, normally=0.1656nm
    Rguess is an initial guess for the R value (dont bother to change the default)
    Note, it has been tested for values of tau in the 0.68-13 ns range
    '''

    def f(R, tau, deltaR):
        '''function whose root is to be found'''
        return TaoEldrup(R, deltaR) - tau

    return S.optimize.newton(f, Rguess, args=(tau, deltaR))


def RTE_F(x, T, delta=0.19, tol=1e-10, maxorder=100):
    '''Calculates the F function of pg 4659 of TL Dull et al., J. Phys Chem B 105, 4657 (2001)
    x is the dimension (in nm)
    delta is the free parameter (0.18-0.19 nm)
    T is temperature in Kelvin
    order is the summation order (it should be inf)
    note, in the exponential, a constant value (2181.647 K nm^2) is used which is beta/k, where  beta=(h**2)/16m= 0.188 eV nm^2 and k=8.617343e-5 eV/K

    NOTE: this routine may need to be rewritten, specially for performing the sums of F in inverse order, to get rid of the finite precision errors in the sumation
    '''
    if not S.isfinite(x): return 1.
    F = 1. - 2. * delta / x
    try:
        beta_over_x2kT = 2181.647 / (T * x ** 2)
    except ZeroDivisionError:
        beta_over_x2kT = S.inf
    # calculate the maximum order for the sums
    order = S.floor(S.sqrt(1 - S.log(tol) / beta_over_x2kT))
    order = min(maxorder, int(order))
    convergence = False
    den_sum = 0.
    num_sum = 0.
    i = 0
    if order > 1:
        while (not convergence and i < order):
            i += 1
            den_i = S.exp(-beta_over_x2kT * (i ** 2))
            num_i = den_i * S.sin(2.0 * S.pi * delta * i / x) / (i * S.pi)
            den_sum += den_i
            num_sum += num_i
            term = num_sum / den_sum
            convergence = ((den_i / den_sum < tol and abs(num_i) / abs(
                num_sum) < tol) or term / F < tol) or not S.isfinite(term)
    else:
        term = S.sin(2.0 * S.pi * delta / x) / (S.pi)
    F += term
    return F


def RectangularTaoEldrup(a, b, c, T, delta=0.19):
    '''The Rectangular Tao Eldrup Formula: see TL Dull et al., J. Phys Chem B 105, 4657 (2001)
    Note: the enhancements of this model over the original Tao-Eldrup are:
        1.-Cuboid pores are considered (hence allowing for channel or lamellar-like geometries to be calculated)
        2.-Explicit temperature dependence
        3.-Includes the finite oPs self-annihilation time in vacuum (142ns)

    a,b and c are the dimensions of the cuboid pore (in nm)
    T is the temperature (in Kelvin)
    delta is an empirical parameter for the T-E model, normally=0.19nm  (calculated to fit the TE model for R<1nm)

    Note: Two constants are used:
        1.-spin averaged Ps annihilation rate=(Ls+Lt)/4=2.0053 ns^-1
        2.-(Ls-Lt)/4=1.9982 ns^-1
        where Ls and Lt are the vacuum annihilation rates for pPs and oPs, respectively

    Note: The mean free path in a cube with side a=2*(R+deltaR) is the same as in a sphere of radius R+deltaR
    '''
    rate = 2.0053 - 1.9982 * RTE_F(a, delta=delta, T=T) * RTE_F(b, delta=delta,
                                                                T=T) * RTE_F(c,
                                                                             delta=delta,
                                                                             T=T)
    return 1. / rate


def RTE_cube(tau, T, guess=3., delta=0.19):
    '''returns the cubic pore size (in nm) for a given tau (oPs lifetime, in ns),
    by numerically solving the Rectangular Tao-Eldrup equation (Newton method)
    delta is an empirical parameter for the RTE model, normally=0.19nm
    guess is an initial guess for the a value (dont bother to change the default)
    Note, it has been tested for values of tau in the ??? ns range and values of T in the range of ???
    '''

    def f(a, T, tau, delta):
        '''function whose root is to be found'''
        return RectangularTaoEldrup(a, a, a, T, delta) - tau

    return S.optimize.newton(f, guess, args=(T, tau, delta))


def RTE_channel(tau, T, guess=3., delta=0.19):
    '''returns the square channel size (in nm) for a given tau (oPs lifetime, in ns),
    by numerically solving the Rectangular Tao-Eldrup equation (Newton method)
    delta is an empirical parameter for the RTE model, normally=0.19nm
    guess is an initial guess for the a value (dont bother to change the default)
    Note, it has been tested for values of tau in the ??? ns range and values of T in the range of ???
    '''

    def f(a, T, tau, delta):
        '''function whose root is to be found'''
        return RectangularTaoEldrup(a, a, S.inf, T, delta) - tau

    return S.optimize.newton(f, guess, args=(T, tau, delta))


def RTE_sheet(tau, T, guess=3., delta=0.19):
    '''returns the sheet pore spacing (in nm) for a given tau (oPs lifetime, in ns),
    by numerically solving the Rectangular Tao-Eldrup equation (Newton method)
    delta is an empirical parameter for the RTE model, normally=0.19nm
    guess is an initial guess for the a value (dont bother to change the default)
    Note, it has been tested for values of tau in the ??? ns range and values of T in the range of ???
    '''

    def f(a, T, tau, delta):
        '''function whose root is to be found'''
        return RectangularTaoEldrup(a, S.inf, S.inf, T, delta) - tau

    return S.optimize.newton(f, guess, args=(T, tau, delta))
