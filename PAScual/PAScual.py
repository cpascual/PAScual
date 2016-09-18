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

from release import __version__

import cPickle as pickle
import copy
import os
import random
import scipy as S
import string
import sys
import time
from scipy import optimize
from scipy.special import erfc
from shutil import copy2

# FWHM = SIGMA*(2*sqrt(2*log(2))) = SIGMA*2.3548200450309493
FWHM2SIGMA = 1. / (2 * S.sqrt(2 * S.log(2)))


# if qt is present, we will use it to emit signals
from qwt.qt.QtCore import QObject, pyqtSignal

class _Emitter(QObject):

    # signal for updating the progress bar
    commandPBarValue = pyqtSignal(int)
    # signal for setting up the progress bar
    initCommandPBar = pyqtSignal(int,int)
    # signal for writing in the tee
    teeOutput = pyqtSignal(str)

emitter = _Emitter()


class aborthelper(object):
    '''A class that provides a method for requesting the calculation to finish'''

    def abortRequested(self):
        '''This is a dummy function that can be overwritten by an external module that wants to stop a calculation in the middle.
		Note: do not reimplement the method definition in the class. Do it in a specific instance instead.'''
        return False


abort = aborthelper()  # this object is the instance whose abortRequested() method should be changed externally if needed


class newcolor(object):
    def __init__(self, i0=0):
        self.i = i0
        self.colorlist = ['black', 'white', 'red', 'blue', 'green', 'brown',
                          'orange', 'cyan', 'purple', 'violet', 'khaki']
        self.i0 = i0

    def next(self):
        result = self.colorlist[self.i]
        self.i += 1
        if self.i >= len(self.colorlist): self.i = self.i0
        return self.colorlist[self.i]


class tee(object):
    '''defines tee like object. Allows to print to various files simultaneously'''

    def __init__(self, *fileobjects):
        self.fileobjects = []
        for ob in fileobjects:
            if isinstance(ob, file): self.fileobjects.append(ob)
        self.qtextedit = []
        self.emitEnabled = False

    #		for ob in self.fileobjects:
    #			if isinstance(ob,str): ob=open(ob,'w')
    def setEmitEnabled(self, flag):
        '''use this to set the tee to emit a QT signal with the string whenever write() is called'''
        self.emitEnabled = flag

    def prnt(self, string):
        '''this method is useful if you dont want to permanently redirect sys.stdout but want a print-like behaviour'''
        for fileobject in self.fileobjects:
            print >> fileobject, string

    def write(self, string):
        '''This method is useful for making sys.stdout=tee(sys.__stdout__,logfile)
		That is, to redirect all stdout to a list of file objects'''
        for fileobject in self.fileobjects:
            fileobject.write(string)
        if self.emitEnabled: emitter.teeOutput.emit(copy.deepcopy(string))

    def flush(self):
        for fileobject in self.fileobjects: fileobject.flush()


def updatestats(m_old, S2_old, n, x_new):
    '''Calculates the new mean and variance after adding a new state
		See algorithm III in http://en.wikipedia.org/wiki/Algorithms_for_calculating_variance (20060919), or
	   Donald E. Knuth (1998). The Art of Computer Programming, volume 2: Seminumerical Algorithms, 3rd edn., p. 232. Boston: Addison-Wesley.
	   IMPORTANT: We are calculating the variance, which is the "error" squared. In other words. the result for a parameter should be quoted as mean "+/- sqrt(S2)" '''
    delta = (x_new - m_old) * 1.
    mean = m_old + delta / (n + 1)
    S2 = (S2_old * (n - 1) + (x_new - mean) * delta) / n
    return mean, S2


def objectindex(object, listtosearch):
    i = 0
    for ob in listtosearch:
        if ob is object: break
        i += 1
    if i >= len(listtosearch): raise ValueError("Object not in list")
    return i


def unique(s):
    '''returns a list of unique elements, where the uniqueness is established via its repr() string'''
    try:
        return list(set(s))
    except TypeError:
        u = []
        repr_u = []
        for x in s:
            repr_x = repr(x)
            if repr_x not in repr_u:
                u.append(x)
                repr_u.append(repr_x)
        return u


class fitable(object):
    def __init__(self, free=True, name=None, npertmin=1, npertmax=4):
        self.name = name
        self.free = free
        self.undo_lock = False
        self.updatelist = []
        self.undolist = []
        self.perturbablelist = []
        self.fixedpertlist = []
        self.npertmin = npertmin
        self.npertmax = npertmax

    def _register_perturbable_(self, pert):
        if isinstance(pert, list):
            for ob in pert:
                if ob.free:
                    self.perturbablelist.append(ob)
                else:
                    self.fixedpertlist.append(ob)
        else:
            if pert.free:
                self.perturbablelist.append(pert)
            else:
                self.fixedpertlist.append(pert)
        return

    def _update_(self, caller):
        '''This takes care of notifying that this object changed to any other object that might depend on it'''
        failcount = 0
        for ob in self.updatelist:
            failcount += ob.on_update(self)
        return failcount

    def _confirm_(self, savehist=False):
        '''This method should not be redefined by children. Modify confirm() instead'''
        self.undolist = []
        for ob in self.perturbablelist:
            ob.confirm(savehist)

    def confirm(self, savehist=False):
        self._confirm_()

    def _undo_(self):
        '''This method should not be redefined by children. Modify undo() instead'''
        count = 1
        self.undo_lock = True
        self.undolist = unique(self.undolist)
        # follow the chain of undo functions
        while (len(self.undolist)):
            count += self.undolist.pop().undo()
        # and call for an undo of any dependent objects too!
        for ob in self.updatelist:
            count += ob.undo()
        self.undo_lock = False
        return count

    def undo(self):
        if self.undo_lock or not self.changed(): return 0
        return self._undo_()

    def on_update(self, caller):
        if self.undo_lock or not self.changed(): return 0
        self.undolist.append(caller)
        return 1

    def changed(self):
        if self.undolist:
            return True
        else:
            return False

    def perturbate(self, npert=1, fitmember=[], direct=False):
        '''Produces a change in a fitable member of the spectrum (same probability to all)
		fitmember , if passed, must be a list. All of the objects in fitmember will be perturbated, but in a random order.
		TODO: in the case of passing a fitmember not in the perturbablelist, it should raise a warning'''
        if not npert: npert = random.randint(self.npertmin, self.npertmax)
        changedobjectlist = []
        if fitmember:
            shuffled = fitmember * 1  # makes a copy so that the original is not shuffled
            random.shuffle(shuffled)
            for ob in shuffled: changedobjectlist += ob.perturbate(npert=npert,
                                                                   direct=direct)
        else:
            for i in range(npert):
                changedobjectlist += random.choice(
                    self.perturbablelist).perturbate(direct=direct)
        self.undolist += changedobjectlist
        return changedobjectlist

    def unfold_perturbablelist(self):
        li = []
        for ob in self.perturbablelist:
            li += ob.unfold_perturbablelist()
        return unique(li)

    def _save_best_(self):
        for ob in self.perturbablelist:    ob.save_best()

    def save_best(self):
        self._save_best_()


class fitpar_original(fitable):
    def __init__(self, val=0., minval=0., maxval=None, free=False, mstep=0.,
                 sstep=0., name=None):
        fitable.__init__(self, free=free, name=name)
        #		super(fitpar_original,self).__init__(free=free,name=name) # This line is a more elegant way of doing: fitable.__init__(self,free=free,name=name)
        self.val = val
        self.minval = minval
        self.maxval = maxval
        self.mstep = mstep
        self.sstep = sstep
        self.old = val
        if self.minval > self.maxval and self.maxval is not None: raise ValueError(
            'minval cannot be larger than maxval')

    def __cmp__(self, other):
        return cmp(self.val, self.val)

    def forcelimits(self):
        '''forces val to be within minval and maxval'''
        if self.val < self.minval:
            self.val = self.minval
            return -1
        if self.val > self.maxval and self.maxval is not None:
            self.val = self.maxval
            return 1
        return 0

    def confirm(self, savehist=False):
        '''forgets the old value (as the current one is confirmed)'''
        self.old = self.val

    def undo(self):
        '''reverts to the old state'''
        if self.undo_lock or not self.changed(): return 0
        self.val = self.old
        return self._undo_()

    def perturbate(self, npert=1, direct=False):
        random.choice([self.randsum, self.randmult])()
        self.forcelimits()
        return [self]

    def randsum(self):
        '''symmetric additive random change. Does not actually change, but only generates a proposed self.new. See confirmnew()'''
        self.val = random.gauss(self.val, self.sstep)
        return [self]

    def randmult(self):
        '''symmetric multiplicative random change. Does not actually change, but only generates a proposed self.new. See confirmnew()'''
        gauss_rnd = random.gauss(0, self.mstep)
        if gauss_rnd > 0.:
            self.val = self.val * (1. + gauss_rnd)
        else:
            self.val = self.val / (1. - gauss_rnd)
        return [self]

    def changed(self):
        return self.val != self.old

    def unfold_perturbablelist(self):
        if self.free:
            return [self]
        else:
            return []

    def get_initargs(self):
        '''returns a tuple that can be used to initialyse a fitpar "similar" to this one'''
        return self.val, self.minval, self.maxval, self.free, self.mstep, self.sstep, self.name

    def save_best(self):
        self.best = self.val


class fitpar(fitpar_original):
    def __init__(self, val=0., minval=0., maxval=None, free=False, name=""):
        fitpar_original.__init__(self, val=val, minval=minval, maxval=maxval,
                                 free=free, name=name)
        #		super(fitpar,self).__init__(val=val,minval=minval, maxval=maxval, free=free,name=name)
        self.clearstats()
        self.NNRLA_delta = 0.
        self.NNRLA_sigma = 0.1 * val
        self.NNRLA_diff = 0.
        self.NNRLA_maxstep = 0.1 * val
        self.NNRLA_sigmamult = .5
        self.hist = None
        if free:
            self.freetag = "*"
        else:
            self.freetag = " "

    def perturbate(self, npert=1, direct=True):
        '''produces a NNRLA perturbation.
		Note that it is always direct, so self.NNRLA_delta must be 0 in case a symmetric perturbation is desired
		NOTE: direct and npert are ignored here (only one perturbation and always "direct" since the non-direct is a particular case of direct with self.NNRLA_delta=0!!'''
        self.val = random.gauss(self.val + self.NNRLA_delta,
                                self.NNRLA_sigma * self.NNRLA_sigmamult)
        self.forcelimits()
        return [self]

    def updatestats(self, savehist=False):
        self.mean, self.var = updatestats(self.mean, self.var, self.n, self.val)
        if savehist:
            try:
                self.hist[self.n - 1] = self.val
            except:
                raise  # TODO: using this exception control, a disk dump could be implemented.
        self.n += 1

    def clearstats(self):
        self.mean = self.val
        self.var = 0
        self.n = 1
        self.best = None

    def showreport(self):
        print "%s: %.3e (%.3e) [%s - %s]\n\tFree=%s NNRLA: %.3e (%.3e)\n\t%s" % (
        self.name, self.val, S.sqrt(self.var), self.minval, self.maxval,
        self.free, self.NNRLA_delta, self.NNRLA_sigma, self)

    def importval(self, val, onlyfree=False):
        '''Changes the value only if it is within limits. If onlyfree is True, the parameter is only changed if it is free
		returns True if it was changed. False otherwise'''
        if (onlyfree and not self.free): return False
        temp = self.val
        self.val = val
        lim = self.forcelimits()
        if lim: self.val = temp  # undo the change
        return not lim


class discretepals(fitable):
    def __init__(self, name=None, expdata=None, roi=None, taulist=None,
                 itylist=None, bg=None, fwhm=None, c0=None, psperchannel=None,
                 area=None, fake=False):
        #		self.checklist={'name'=(3>4),
        '''This is a pre-initialisation method. The real init is called __real_init(), and is called if all the needed parameters are present.
		This allows to perform initialisation in various steps'''
        self.name = name
        self.exp = expdata
        self.roi = roi
        self.taulist = taulist
        self.itylist = itylist
        self.bg = bg
        self.fwhm = fwhm
        self.c0 = c0
        self.psperchannel = psperchannel
        self.area = area
        self.isfake = fake
        self.selected = True
        self.parentsetName = "SET_%s" % name
        self.ready = False
        self.realinit = False
        self.initifready()

    def isready(self):
        self.ready = self.ready or not (
        ((self.exp is None) and not self.isfake) or (
        self.isfake and (self.roi is None))
        or (self.taulist is None) or (self.itylist is None) or (self.bg is None)
        or (self.fwhm is None) or (self.c0 is None) or (
        self.psperchannel is None)
        or (self.isfake and (self.area is None)))
        return self.ready

    def initifready(self, force=False):
        if self.realinit and not force: return self.realinit
        if self.isready(): self._real_init(name=self.name, expdata=self.exp,
                                           roi=self.roi, taulist=self.taulist,
                                           itylist=self.itylist, bg=self.bg,
                                           fwhm=self.fwhm, c0=self.c0,
                                           psperchannel=self.psperchannel,
                                           area=self.area)
        return self.realinit

    def _real_init(self, name=None, expdata=None, roi=None, taulist=None,
                   itylist=None, bg=None, fwhm=None, c0=None, psperchannel=1,
                   area=1.):
        '''
			An object that contains exp and sim spectrum.
			Arguments:
				name: the name for this spectrum (a string)
				expdata: a list/array containing the exp spectrum
				roi: a list/array containing the Region Of Interest (channels that will be fitted)
				taulist: a list of fitpars for lifetimes
				itylist: a list of fitpars for intensities. Must be same len than taulist
				background: a fitpar for background
				fwhm: a fitpar for the resolution
				c0: a fitpar for the offset of the calibration
				psperchannel: The ps/channel (not a fitpar, just a number). Should be known from calibration
		'''
        # Check the inputs and store them in self
        fitable.__init__(self, name=name)
        #		super(discretepals,self).__init__(name=name)
        self.realinit = True  # indicates that the real initialization took place
        if expdata is not None:
            self.exp = S.array(expdata,
                               dtype='d')  # for fitting, self.exp[self.roi] is to be used
        else:
            self.exp = S.zeros(len(roi), dtype='d')
        if roi is not None:
            self.roi = S.array(roi, dtype='i')
        else:
            self.roi = S.arange(self.exp.size, dtype='i')
        if len(taulist) != len(
            itylist): raise TypeError, 'taulist and itylist must be of same size'
        for ob in taulist + itylist:
            if not isinstance(ob, fitpar): raise TypeError("Fitpar wanted")
        self.taulist = taulist
        self.itylist = itylist
        if isinstance(bg, fitpar):
            self.bg = bg
        else:
            raise TypeError("Fitpar wanted")
        if isinstance(fwhm, fitpar):
            self.fwhm = fwhm
        else:
            raise TypeError("Fitpar wanted")
        if isinstance(c0, fitpar):
            self.c0 = c0
        else:
            raise TypeError("Fitpar wanted")
        self.psperchannel = psperchannel

        # Register all the perturbables
        self._register_perturbable_(
            self.taulist + self.itylist + [self.bg, self.fwhm, self.c0])

        # Include this instance of discretepals in the updatelist of each fitpar
        # (this means that every time any of these fitpars is undone, this instance will be undone too)
        for ob in self.perturbablelist: ob.updatelist.append(self)

        # read the init inputs and fill some more vars
        self.ncomp = len(self.taulist)  # number of components
        self.dof = self.roi.size - len(
            self.perturbablelist)  # degrees of freedom
        self.tau = S.zeros(self.ncomp, dtype='d')
        self.ity = S.zeros(self.ncomp, dtype='d')
        self.freeityindexes = []
        for i in xrange(self.ncomp):
            self.tau[i], self.ity[i] = self.taulist[i].val, self.itylist[
                i].val  # filling the tau and ity vectors
            if self.itylist[i].free: self.freeityindexes.append(i)
        self.freeityindexes = S.array(self.freeityindexes,
                                      dtype='i')  # this contains the indexes of those itys which vary (need normalising)
        self.fixeditysum = self.ity.sum() - self.ity[
            self.freeityindexes].sum()  # the sum of the fixed itys (which won't vary unless the 'free' status of an ity varies)
        self.channeltimes = self.calculate_channeltimes(self.roi, self.c0.val,
                                                        self.psperchannel)  # channel times
        self.M = self.calculate_M(self.channeltimes, self.tau, self.fwhm.val,
                                  M=None)  # calculating the M matrix
        self.M_dot_a = S.dot(self.M,
                             self.normalizeity(self.ity, self.freeityindexes,
                                               self.fixeditysum))
        if self.exp.sum() == 0: self.exp[
            self.roi] = self.fake()  # If no expdata was given, create a fake spectrum and use it as exp data
        self.deltaexp = S.where(self.exp < 4, 2., S.sqrt(
            self.exp))  # A quite good approximation to Poisson statistics (error=2 for 0-3 counts and Gaussian approx for the rest)
        self.deltaexp2 = self.deltaexp ** 2
        self.NNRLA_S0 = (1. / self.deltaexp2[self.roi]).sum()
        self.exparea = float(self.exp[
                                 self.roi].sum())  # Area of exp spectrum in roi, including background
        self.sim = self.calculate_sim(self.bg.val, self.exparea,
                                      self.channeltimes, self.M_dot_a)
        # calculate the chi2 and all intermediate things for initialisation
        self.chi2 = self.recalculate_chi2(forcecalc=True)
        self.autocorr = 0
        self.confirm()
        self.clearstats_ity()

    def changed(self):
        '''TODO: make sure that this criterion is enough'''
        return self.chi2 != self.chi2_old

    def confirm(self, savehist=False):
        '''confirm the various elements that may change and then proceed to the standard _confirm_()'''
        # TODO implement history keeping ??: Answer: Not here. hist makes sense only for the fitpar and palsset classes
        self.chi2_old = self.chi2
        self.sim_old, self.M_dot_a_old, self.M_old, self.channeltimes_old, self.tau_old, self.ity_old = self.sim.copy(), self.M_dot_a.copy(), self.M.copy(), self.channeltimes.copy(), self.tau.copy(), self.ity.copy()
        self._confirm_(savehist)

    def undo(self):
        '''undo the various elements that may have changed and then proceed to the standard _undo_()'''
        if self.undo_lock or not self.changed(): return 0
        self.chi2 = self.chi2_old
        self.sim, self.M_dot_a, self.M, self.channeltimes, self.tau, self.ity = self.sim_old.copy(), self.M_dot_a_old.copy(), self.M_old.copy(), self.channeltimes_old.copy(), self.tau_old.copy(), self.ity_old.copy()
        return self._undo_()

    def updatestats_ity(self):
        '''updates the statistics on the itys (which are not fitpar dependent but spectrum dependent due to the normalisation)'''
        itynorm = self.normalizeity()
        #		print 'DEBUG: !!!!!!!!!!!!!!!!', self.ity,'\n:::::::',self.ity_mean
        self.ity_mean, self.ity_var = updatestats(self.ity_mean, self.ity_var,
                                                  self.ity_n, itynorm)
        self.ity_n += 1

    def clearstats_ity(self):
        self.ity_mean = self.normalizeity()
        self.ity_var = S.zeros(self.ity.size, dtype='d')
        self.ity_n = 1

    def fake(self, area=None, noise=True, filename=None):
        '''Generates a fake spectrum by simulation and addition of Poisson noise'''
        if area is None: area = self.bg.val * self.channeltimes.size * 20  # if no area is given, it is calculated so that the total background is ~5% of the counts
        sim = self.calculate_sim(self.bg.val, area, self.channeltimes,
                                 self.M_dot_a)
        if noise: sim = S.random.poisson(sim)
        return sim

    def normalizeity(self, ity=None, freeityindexes=None, fixeditysum=None):
        if ity is None: ity = self.ity
        if freeityindexes is None: freeityindexes = self.freeityindexes
        if fixeditysum is None: fixeditysum = self.fixeditysum
        k = (1 - fixeditysum) / ity[freeityindexes].sum()
        result = ity.copy()
        result[freeityindexes] *= k
        return result

    def normalizeityfactor(self, ity=None, freeityindexes=None,
                           fixeditysum=None):
        if ity is None: ity = self.ity
        if freeityindexes is None: freeityindexes = self.freeityindexes
        if fixeditysum is None: fixeditysum = self.fixeditysum
        k = (1 - fixeditysum) / ity[freeityindexes].sum()
        factor = S.ones(ity.size, dtype='d')
        factor[freeityindexes] = k
        return factor

    def recalculate_chi2(self, full_output=False, forcecalc=False):
        '''Recalculates the chi2 by calculating any needed intermediate step only if required.
		 If full_output is True, it returns the intermediate quantities too
		 Note that it makes changes in self.chi2, self.tau, self.ity, self.sim, self.M , self.M_dot_a, self.channeltimes.
		 These changes can be confirmed or undone afterwards by calling self.confirm() or self.undo().
		 '''
        # first of all check if anything changed in any member of the perturbablelist
        somechange = forcecalc
        for ob in self.perturbablelist: somechange += ob.changed()
        if not somechange:
            if full_output:
                return self.chi2, (self.sim - self.exp[self.roi]) / \
                       self.deltaexp[self.roi]
            else:
                return self.chi2
        # if something changed, recalculate
        recalc_M = []
        recalc_M_dot_a = False
        if self.fwhm.changed():
            recalc_M = range(self.ncomp)
        if self.c0.changed():
            recalc_M = range(self.ncomp)
            self.channeltimes = self.calculate_channeltimes(self.roi,
                                                            self.c0.val,
                                                            self.psperchannel)
        #		print ";;;;;;;;;;;;;;;;;;;;;;;;;",self.ncomp
        for i in xrange(self.ncomp):
            if self.taulist[i].changed():
                self.tau[i] = self.taulist[i].val
                recalc_M.append(i)
            if self.itylist[i].changed():
                self.ity[i] = self.itylist[i].val
                #				print "::::::::::::::::::",i, self.itylist[i].name,self.itylist[i].val,self.ity
                recalc_M_dot_a = True
        # cap the recalc_M to a max of ncomp components (if there are more is because c0 or fwhm were varied)
        if len(recalc_M) > self.ncomp: recalc_M = recalc_M[:self.ncomp]
        # Recalculate M if needed
        if recalc_M:
            self.M = self.calculate_M(t=self.channeltimes, gridtau=self.tau,
                                      fwhm=self.fwhm.val, M=self.M,
                                      indexarray=recalc_M)
            recalc_M_dot_a = True
        # Recalculate M_dot_a if needed
        if recalc_M_dot_a:
            self.M_dot_a = S.dot(self.M, self.normalizeity(self.ity,
                                                           self.freeityindexes,
                                                           self.fixeditysum))
        # calculate the simulated spectrum
        self.sim = self.calculate_sim(self.bg.val, self.exparea,
                                      self.channeltimes, self.M_dot_a)
        # calculate the chi2 and the residuals
        residuals = (self.sim - self.exp[self.roi]) / self.deltaexp[self.roi]
        self.chi2 = (residuals * residuals).sum()
        if full_output:
            return self.chi2, residuals
        else:
            return self.chi2

    def calculate_sim(self, bg, exparea, channeltimes, M_dot_a):
        '''adds the background and scales the M_dot_a vector to obtain the simulated spectrum'''
        area = M_dot_a.sum()
        return bg + ((exparea - bg * S.size(channeltimes)) / area) * M_dot_a

    def calculate_channeltimes(self, roi, c0, psperchannel):
        '''calculates the time corresponding to the center of each channel of a ROI'''
        return (
               roi - c0) * psperchannel  # this returns the times in the boundaries between channels

    #		return (roi+(0.5-c0))*psperchannel	#this would return the times in the middle of the channels

    def calculate_convoluted_decay(self, t, tau=1., intsty=1., sigma=1.):
        '''Calculate one component of a PALS spectrum. Exponential decay (starting at time 0) convolved with a Gaussian.
		result(t)=convolution(G,E) , where G is a Gaussian and E is a exponential decay starting at 0.
		t: times for which the decay is calculated (a scipy one-dimensional array) or other sequence
		tau: decay time
		intsty: intensity of that component (the area below the curve for the given component)
		sigma: gaussian width (standard deviation)
		The formula used is the one from [Kirkegaard & Eldrup, Computer Physics Communications 3 (1972) 240-255], with T0=0, and a redefinition of sigma
		IMPORTANT
		'''
        K = (intsty * 0.5 / tau) * (S.exp(sigma * sigma * 0.5 / (tau * tau)))
        return K * erfc(
            (sigma / (S.sqrt(2.) * tau)) - (t / (S.sqrt(2.) * sigma))) * S.exp(
            -t / tau)

    def calculate_convoluted_decay_integCh(self, t, tau=1., intsty=1.,
                                           sigma=1.):
        """like calculate_convoluted_decay but it integrates time over the channel width instead of using just the given times.
		In other words, eq.4 of Kirkegaard instead of eq.3
		IMPORTANT: this function is optimized assuming that t is a vector of channel times from a compact and homogeneous ROI
		           (i.e. no gaps between channels and  constant --or very slow varying-- channel width))
		           If these premises are not fulfilled, this function wont work"""
        # extend the t vector with one extra time using the channelwidth calculated from the same t (assumes constant channel width!)
        t_extd = S.concatenate((t, (
        2 * t[-1] - t[-2],)))  # the trick is that t_n+Deltat=2*t_n-t_(n-1)
        s = S.sqrt(2.) * sigma
        # Calculate in one go all the values for Y(tau,tk,s)+phi(tk,s)  of eq. 5 of Kirkegaard
        YplusPhi = S.exp(s * s * 0.25 / (tau * tau)) * erfc(
            (s / (2. * tau)) - (t_extd / s)) * S.exp(-t_extd / tau) + erfc(
            t_extd / s)
        return 0.5 * intsty * (YplusPhi[:-1] - YplusPhi[1:])

    def calculate_convoluted_decay_with_tails(self, t, tau=1., tauL=0., tauR=0.,
                                              intsty=1., sigma=1.):
        '''Calculate one component of a PALS spectrum. Exponential decay (starting at time 0) convolved with a Gaussian+exponential tails.
		result(t)=convolution(GT,E) , where GT is a Gaussian+tails and E is a exponential decay starting at 0.
		t: times for which the decay is calculated (a scipy one-dimensional array) or other sequence
		tau: decay time
		intsty: intensity of that component (the area below the curve for the given component)
		sigma: Gaussian width (standard deviation)
		The formula used is eq. 6 from [J.Kansy, Nucl. Instr. and Meth. A 374 (1996), 235-244]
		'''
        alpha = tau * tau / ((tau + tauL)(tau - tauR))
        alphaL = tauL * tauL / ((tau + tauL)(tauR + tauL))
        alphaR = tauR * tauR / ((tauR - tau)(tauR + tauL))

    #		return= intsty*(calculate_convoluted_decay(t,tau=tau,sigma=sigma,intsty=alpha) + calculate_convoluted_decay(-t,tau=tauL,sigma=sigma,intsty=alphaL) + calculate_convoluted_decay(t,tau=tauR,sigma=sigma,intsty=alphaR) )

    def calculate_M(self, t, gridtau, fwhm, M=None, indexarray=None):
        '''Calculates the M matrix. If M is given, it will be reused'''
        sigma = fwhm * FWHM2SIGMA
        if M is None:
            M = S.zeros((t.size, gridtau.size), dtype='d')
            if indexarray is not None: raise ValueError(
                'M must be supplied if indexarray is supplied')
        if indexarray is None:
            indexarray = S.arange(gridtau.size, dtype='i')
        for i in indexarray:
            M[:, i] = self.calculate_convoluted_decay_integCh(t, tau=gridtau[i],
                                                              intsty=1.,
                                                              sigma=sigma)
        return M

    def showreport_1row(self, file=None, min_ncomp=None, silent=False):
        '''Outputs the following to a file:
		name, chi2, autocorr, Set(s), ROImin, ROImax, ROIchann, integral, FWHM, dev, c0, dev, bg,dev, ity1, dev, ity2, dev, ..., tau1, dev, tau2, dev,...
		At least min_ncomp components are written (padded with ## if nonexistent)
		'''
        if file is None: file = sys.stdout
        if min_ncomp is None: min_ncomp = self.ncomp
        #		itynorm=100./S.sum([ob.mean for ob in self.itylist])
        #		itynorm=100.*self.normalizeityfactor(ity=S.array([ob.mean for ob in self.itylist]))
        itymean = 100. * self.ity_mean
        ityerr = 100. * S.sqrt(self.ity_var)
        self.autocorr = self.calculate_residuals_local_correlation()
        retval = "%20s\t%14e\t%14e\t%9s\t" % (
        self.name, self.chi2 / self.dof, self.autocorr,
        string.join([ob.name for ob in self.updatelist], ','))
        retval += "%6i\t%6i\t%6i\t%14e\t" % (
        self.roi[0], self.roi[-1], self.roi.size, self.exparea)
        retval += "%9g\t%9g\t%9g\t%9g\t%9g\t%9g\t" % (
        self.fwhm.mean, S.sqrt(self.fwhm.var), self.c0.mean,
        S.sqrt(self.c0.var), self.bg.mean, S.sqrt(self.bg.var))
        npad = (min_ncomp - self.ncomp)
        #		for ity,i in zip(self.itylist,range(len(self.itylist))): retval+="%9g\t%9g\t"%(ity.mean*itynorm[i], S.sqrt(ity.var)*itynorm[i])
        for i in xrange(self.ncomp): retval += "%9g\t%9g\t" % (
        itymean[i], ityerr[i])
        retval += (2 * npad) * ("%9g\t" % 0)
        for tau in self.taulist: retval += "%9g\t%9g\t" % (
        tau.mean, S.sqrt(tau.var))
        retval += (2 * npad) * ("%9g\t" % 0)
        retval += "\n"
        if not silent: file.write(retval)
        return retval

    def showreport(self, silent=False):
        '''prints a report of the status of this discretepals spectrum (and also returns the string)
		Note that what it prints is human readable (i.e.) some output is processed before printing'''
        #		itynorm=100.*self.normalizeityfactor(ity=S.array([ob.mean for ob in self.itylist]))
        itymean = 100. * self.ity_mean
        ityerr = 100. * S.sqrt(self.ity_var)
        result = ''
        result += '---------------------\n'
        result += "Spectrum name: %s\n" % self.name
        result += "ROI: min=%i max=%i    Calibration=%g ps/ch\n" % (
        self.roi[0], self.roi[-1], self.psperchannel)
        result += "FWHM [ps]: %5g (%g)\t  [%s]\n" % (
        self.fwhm.mean, S.sqrt(self.fwhm.var), self.fwhm.freetag)
        result += "C0   [ch]: %5g (%g)\t  [%s]\n" % (
        self.c0.mean, S.sqrt(self.c0.var), self.c0.freetag)
        result += "bg   [ct]: %5g (%g)\t  [%s]\n" % (
        self.bg.mean, S.sqrt(self.bg.var), self.bg.freetag)
        result += "Intensities [%]       Lifetimes [ps]\n"
        for i in xrange(self.ncomp):
            ity, tau = self.itylist[i], self.taulist[i]
            #			result+= "%4.1f (%4.1f) [%s]         %5i (%i) [%s]\n"%(ity.mean*itynorm[i], S.sqrt(ity.var)*itynorm[i], ity.freetag, tau.mean, S.sqrt(tau.var), tau.freetag)
            result += "%4.1f (%4.1f) [%s]         %5i (%i) [%s]\n" % (
            itymean[i], ityerr[i], ity.freetag, tau.mean, S.sqrt(tau.var),
            tau.freetag)
        #		atocorr=self.calculate_residuals_local_correlation()
        autocorr = 0
        result += "Chi2: %.3f \t (=%.3e/DOF)\t AutoCorrel:%.3e\n" % (
        self.chi2 / self.dof, self.chi2, autocorr)
        result += '---------------------'
        if not silent: print result
        return result

    def calculate_residuals_local_correlation(self, residuals=None,
                                              locallength=None):
        '''It is a crude estimator of local correlations
		Defined as the (normalised) sum of squared correlation coeffs in small boxes of the residuals'''
        if residuals is None: residuals = (self.sim - self.exp[self.roi]) / \
                                          self.deltaexp[self.roi]
        if locallength is None: locallength = max(5, int(
            5 * self.fwhm.val / self.psperchannel))
        nboxes = residuals.size - locallength + 1
        if nboxes < 1: raise ValueError(
            "The locallength must be smaller than the size of the residuals")
        result = 0
        for i in xrange(nboxes):
            localcorr = S.corrcoef(self.channeltimes[i:i + locallength],
                                   residuals[i:i + locallength])[0][1]
            result += localcorr * localcorr
        return result / nboxes

    def save_best(self):
        self.chi2_best = self.chi2
        self._save_best_()

    def calculate_fprime(self, fp, alpha=1e-4):
        '''calculates the numerical derivative of the simulated spectrum with respect to fp'''
        # calculate sim for a sigma*(1+dr)
        fp.confirm()
        fp.val *= (1 + alpha)
        self.recalculate_chi2()
        fprime = (self.sim - self.sim_old) / (alpha * fp.val)
        fp.undo()  # this should also undo all the spectra that depend on it
        return fprime

    def calculate_NNRLA_SZ(self, fp, direct=False):
        '''This function calculates S0,S1,S2,Z, for the given fitpar.
		They are intermediate quantities for the calculation of NNRLA_delta and NNRLA_sigma
		for a given spectrum, NNRLA_delta= Z/S2 and NNRLA_sigma=sqrt(S0/(S0S2-S1S1))
		Note that S0,S1,S2,Z are different for each free fitpar of which this spectrum depends.
		This intermediate quantities allow for an easy generalisation of the NNRLA to multiple spectra because:
		Xgeneral=sum(X) where X is one of {S0, S1, S2, Z} and the sum is done over the various spectra.'''
        fprime = self.calculate_fprime(fp)
        S0 = self.NNRLA_S0  # Warning: if you change self.roi, you must recalculate self.NNRLA_S0!!
        S1 = (fprime / self.deltaexp2[self.roi]).sum()
        S2 = ((fprime ** 2) / self.deltaexp2[self.roi]).sum()
        if direct:
            Z = (((self.exp[self.roi] - self.sim) / self.deltaexp2[
                self.roi]) * fprime).sum()
        else:
            Z = 0
        return S0, S1, S2, Z

    def compatible(self, other, detail=False):
        '''Tests compatibility of this and another spectra.
		Compatible means:
			same number of components (key "ncomp")
			TODO: maybe implement other compatibility checks?
		'''
        res = {}
        res["ncomp"] = temp = (self.ncomp == other.ncomp)
        if detail:
            return res
        else:
            return res["total"]

    def importvalues(self, other, onlyfree=False, flexicomp=False):
        '''Fills values of the fitpars taking them from a compatible spectrum.
		The return value is True only if all the imports were ok. False otherwise
		If onlyfree==True, it only attempts to import the values for fitpars that are free in self
		If flexicomp==True, the method deals automagically with a differing number of components.
		If it is false and the number of components doesnt match, it doesnt change any component at all
		(but it does change  bg,c0 and fwhm) and returns False'''
        success = (flexicomp or self.ncomp == other.ncomp)
        if self.ncomp == other.ncomp:
            t1, i1, t2, i2 = self.taulist, self.itylist, other.taulist, other.itylist
        elif flexicomp and self.ncomp > other.ncomp:  # copy those available and put the rest to ity=0
            t1, i1 = self.taulist[:other.ncomp], self.itylist[:other.ncomp]
            t2, i2 = other.taulist, other.itylist
            for ob in self.ity[other.ncomp:]: success *= ob.importval(0.,
                                                                      onlyfree=onlyfree)  # make the other intensities 0
        elif flexicomp and self.ncomp < other.ncomp:  # the extra components are merged into the LAST one
            tomergetau = S.array([fp.v for fp in other.taulist[
                                                 self.ncomp - 1:]])  # contains lifetimes to merge
            tomergeity = S.array([fp.v for fp in other.itylist[
                                                 self.ncomp - 1:]])  # contains intensities to merge
            mergedtau = fitpar(
                val=((tomergetau * tomergeity).sum() / tomergeity.sum()))
            mergedity = fitpar(val=tomergeity.sum())
            t1, i1 = self.taulist, self.itylist
            t2, i2 = other.taulist[:self.ncomp - 1] + [
                mergedtau], other.itylist[:self.ncomp - 1] + [mergedity]
        else:  # This is the case in which flexicomp is false and the ncomp don't match. No components are changed
            t1 = i1 = t2 = i2 = []
            success = False
        # now the components are matched, construct the lists of fitpars that are going to be imported
        fpl1 = t1 + i1 + [self.bg, self.fwhm, self.c0]
        fpl2 = t2 + i2 + [other.bg, other.fwhm, other.c0]
        for ob1, ob2 in zip(fpl1, fpl2):
            if ((not onlyfree) or ob1.free): success *= ob1.importval(ob2.val)
        return success

    def saveAs_ASCII(self, f, hdr=None, columns=1, datafmt='%i'):
        '''Saves the exp data as ascii with an optional header. It accepts a format string for the data and the number of columns'''
        # TODO: support for multiple columns. Same approach as used in sumpals (Nat)
        if not isinstance(f, file): f = open(f, 'w')
        if hdr is not None: f.write(hdr)
        if columns > 1: raise NotImplementedError()  # TODO
        S.savetxt(f, self.exp, fmt=datafmt)
        f.close()

    def saveAs_LT(self, f):
        hdr = "%s\n%.4g\n%g\n%.4g\n" % (
        'LT_description', self.psperchannel * 1e-3, -1234567,
        self.fwhm.val * 1e-3)
        self.saveAs_ASCII(f, hdr, columns=1, datafmt='%i')


class palsset(fitable):
    ''' This class  defines sets of PALS spectra.
	Design considerations:
	A set defines which spectra are to be fit simultaneously (Those that have common fitting parameters).
	TODO: Ideally, it should hold a common interface so that discretepals and gridpals could be used together

	'''

    def __init__(self, name='set', spectralist=[]):
        fitable.__init__(self, name=name)
        #		super(palsset,self).__init__(name=name)
        self.spectralist = []
        self.fitparlist = []
        self.chi2 = S.inf
        self.n = 1
        self.dof = 1
        self.MCMC_generate(LM=0)
        self.roimin = S.inf
        self.roimax = None
        for sp in spectralist: self.register_spectrum(sp)

    def goodItyErrors(self):
        '''It returns True if the ity errors can be calculated properly'''
        # Trivial cases
        if self.spectralist == 0: return False  # if there are not spectra, the trivial answer is that the errors cannot be calculated (BAD)
        if self.spectralist == 1: return True  # if there is just one spectrum, there is not incompatibility (GOOD)
        if self.spectralist[
            0].ncomp < 1: return False  # the first spectrum has no components (BAD)
        # Check that all spectra in the set are have the same number of free components
        for dp in self.spectralist[1:]:
            if dp.freeityindexes.size != self.spectralist[
                0].freeityindexes.size: return False
        # then check that the itys are either completely independent or completely dependent (i.e. all common or none common)
        common = 0
        itysA = [self.spectralist[0].itylist[i] for i in
                 self.spectralist[0].freeityindexes]
        itysA.sort()
        allitys = unique(itysA)
        for dp in self.spectralist[1:]:
            itysB = [dp.itylist[i] for i in dp.freeityindexes]
            itysB.sort()
            allitys += unique(itysB)
            common += (itysA == itysB)
        if common == len(self.spectralist[1:]):
            return True  # then all components have the same free parameters (GOOD)
        elif len(unique(allitys)) == len(allitys):
            return True  # there are not common itys at all (GOOD)
        else:
            return False  # If none of the previous conditions was met, it means that there are both common and independent itys (BAD)

    def register_spectrum(self, spectrum):
        '''Registers a spectrum in the set'''
        self.spectralist.append(spectrum)
        self._register_perturbable_(spectrum)
        spectrum.updatelist.append(self)
        self.fitparlist = unique(self.fitparlist + spectrum.perturbablelist)
        # calculate dof
        self.dof = -len(self.fitparlist)
        for ob in self.spectralist: self.dof += ob.roi.size
        self.roimin, self.roimax = min(self.roimin, spectrum.roi[0]), max(
            self.roimax, spectrum.roi[-1])

    #	def upgrade_spectrum(self,

    def confirm(self, savehist=False):
        '''confirm the various elements that may change and then proceed to the standard _confirm_()'''
        for ob in self.fitparlist: ob.updatestats(
            savehist=savehist)  # update stats for all fitpars (including the ity pars, which is a waste)
        for ob in self.spectralist: ob.updatestats_ity()  # update stats on itys (this must be done for each spectrum separately)
        self.chi2_old = self.chi2
        self.chi2_mean, self.chi2_var = updatestats(self.chi2_mean,
                                                    self.chi2_var, self.n,
                                                    self.chi2)
        #		if savehist: self.chi2_hist[self.n]=self.chi2
        self.n += 1
        self._confirm_(savehist)

    def undo(self):
        '''undo the various elements that may have changed and then proceed to the standard _undo_()'''
        if self.undo_lock or not self.changed(): return 0
        self.chi2 = self.chi2_old
        return self._undo_()

    def calculate_chi2(self, recalc=True):
        """Important: this returns the chi2 normalised by the degrees of freedom!!!"""
        chi2 = 0
        if recalc:
            for ob in self.spectralist: chi2 += ob.recalculate_chi2()
        else:
            for ob in self.spectralist:    chi2 += ob.chi2
        self.chi2_old = self.chi2
        self.chi2 = chi2 / self.dof  # normalise
        return self.chi2

    def save_best(self):
        self.chi2_best = self.chi2
        self._save_best_()

    def calculate_NNRLA(self, direct=False):
        self.NNRLAcount += 1
        diff = 0
        for fp in self.fitparlist:
            maxstep = max(fp.NNRLA_maxstep, 0.1 * fp.val)
            deltaold = fp.NNRLA_delta
            sigmaold = fp.NNRLA_sigma
            SZ = S.zeros(4, dtype='d')
            for ob in fp.updatelist:  # TODO: This assumes that the fitpar's updatelist only contains discretepals instances!
                SZ += ob.calculate_NNRLA_SZ(fp, direct)
            #				SZ[0]=0
            # now SZ contains the GENERALISED S0,S1,S2,Z for this fp
            if direct:
                # calculate the delta
                fp.NNRLA_delta = SZ[3] / SZ[2]
                # apply limits to delta
                if fp.NNRLA_delta > maxstep:
                    fp.NNRLA_delta = maxstep
                elif fp.NNRLA_delta < -maxstep:
                    fp.NNRLA_delta = -maxstep
            # calculate the diff
            # calculate the sigma
            fp.NNRLA_sigma = S.sqrt(SZ[0] / (SZ[0] * SZ[2] - SZ[1] * SZ[1]))
            # apply limits to sigma
            if fp.NNRLA_sigma > maxstep:
                fp.NNRLA_sigma = maxstep
            elif fp.NNRLA_sigma < -maxstep:
                fp.NNRLA_sigma = -maxstep
            # calculate the diff
            fp.NNRLA_diff = abs(((
                                 deltaold - fp.NNRLA_delta + sigmaold - fp.NNRLA_sigma) / (
                                 abs(deltaold) + sigmaold)))
            diff += fp.NNRLA_diff
        #			print "DEBUG:%s %g %g (%g) %g (%g)"%( fp.name,fp.val, fp.NNRLA_delta, SZ[3]/SZ[2],fp.NNRLA_sigma, S.sqrt(SZ[0]/(SZ[0]*SZ[2]-SZ[1]*SZ[1])))
        try:
            diff /= len(self.fitparlist)
        except:
            pass
        #		print ':::::::::::::::::::::::::',diff
        return diff

    def clearstats(self):
        '''reset the variables involved in statistics'''
        self.chi2_mean = self.chi2_old = self.chi2
        self.chi2_var = 0.
        for ob in self.fitparlist: ob.clearstats()  # reset the mean, var, n, etc. for each fitpar
        for ob in self.spectralist: ob.clearstats_ity()  # reset the mean, var and n  for the itys in each spectrum

    def MCMC_generate(self, LM=None, T=2., ireport=-1, savehist=False,
                      NNRLA='auto', direct=False, factor=1, iemit=-1):
        '''Generates an MonteCarlo Markov Chain (MCMC) from this set. It modifies the set itself.
		LM is the MCMC length (number of accepted transitions)
		Only additive transitions are used (the step can be regulated by hand or by means of NNRLA calculations).
		Note that if direct=True, the chain fails to be of a Markov type (probabilities are not symmetric) (therefore, for BI, direct must be False)
		factor is a number that will be multiplied to the following inputs: LM, ireport, NNRLA (if not auto).
		The intended use of factor is to be able to write something like factor=len(self.unfold_perturbablelist()) to make the fits more uniform
		'''
        if LM is None: LM = len(self.unfold_perturbablelist())
        LM *= factor
        # if required, prepare the history arrays
        if savehist:
            for ob in self.fitparlist: ob.hist = S.zeros(LM, dtype='d')
        ireport *= factor
        iemit *= factor
        nemit = iemit
        self.NNRLAcount = 0
        if NNRLA == 'auto':
            NNRLA = autoNNRLA = True
        else:
            autoNNRLA = False
            NNRLA = min(NNRLA * factor, LM)
            NNRLA_diff = 0
        if NNRLA:
            self.calculate_NNRLA(direct)
        acc = 0
        increase_acc = 0
        self.accratio = 0
        self.inc_dec_ratio = 0
        tries = 1
        ireport = nreport = min(ireport, LM)
        icalcNNRLA = NNRLA
        self.calculate_chi2()
        self.n = 1
        self.clearstats()
        self.save_best()
        acceptflag = False
        self.lastclock = time.clock()
        perttargetlist = 1 * self.fitparlist
        self.lastclock = time.clock()
        while acc < LM:
            # To ensure that each fitpar is perturbated once each time
            try:
                perttarget = perttargetlist.pop()
            except IndexError:
                perttargetlist = 1 * self.fitparlist
                random.shuffle(perttargetlist)
                perttarget = perttargetlist.pop()
            tries += 1
            self.perturbate(npert=1, direct=direct, fitmember=[perttarget])
            # calculate the new chi2
            self.calculate_chi2()
            # Metropolis algorithm:
            negDX2 = self.chi2_old - self.chi2
            #			print "DEBUG: %e,%e,%e,%i,%i"%(self.chi2,self.chi2_old,negDX2,acc,increase_acc)
            #			for ob in myitylist:ob.showreport()
            #			raw_input()
            if (negDX2 > 0):
                acceptflag = True
            elif (random.random() < S.exp(negDX2 * self.dof / T)):
                increase_acc += 1
                acceptflag = True
            else:
                acceptflag = False
            if acceptflag:
                if abort.abortRequested(): return  # check if we should abort
                acc += 1
                self.confirm(savehist=savehist)
                ireport -= 1
                icalcNNRLA -= 1
                iemit -= 1
                if self.chi2 < self.chi2_best: self.save_best()
                # calculate NNRLA when it is time
                if icalcNNRLA == 0:
                    NNRLA_diff = self.calculate_NNRLA(direct)
                    if autoNNRLA:  # If the auto adjustment of NNRLA is required, do it . TODO: the thressholds are quite arbitrary (fix?)
                        if NNRLA_diff > .2:
                            NNRLA = max(1, NNRLA / 2)
                        elif NNRLA_diff < .05:
                            NNRLA = min(LM / 5, nreport, NNRLA * 2)
                    icalcNNRLA = NNRLA  # reset the count
                # Show report when it is time
                if (ireport == 0):
                    self.accratio = float(acc) / float(tries)
                    self.inc_dec_ratio = float(increase_acc) / float(acc)
                    self.showreport(T, acc, NNRLA=NNRLA, verbosity=1)
                    ireport = nreport  # reset count
                #					self.graph_report()
                if (iemit == 0):
                    emitter.commandPBarValue.emit(acc)
                    iemit = nemit
            else:
                self.undo()

    def showreport_1row(self, file=None, min_ncomp=None, header=False):
        if min_ncomp is None: min_ncomp = max(
            [ob.ncomp for ob in self.spectralist])
        if header:
            file.write(time.asctime())
            file.write("\n%20s\t%14s\t%14s\t%9s\t" % (
            "name", "chi2", "autocorr", "Set(s)"))
            file.write("%6s\t%6s\t%6s\t%14s\t" % (
            "ROImin", "ROImax", "ROIch", "Integral"))
            file.write("%9s\t%9s\t%9s\t%9s\t%9s\t%9s\t" % (
            "FWHM", "dev", "c0", "dev", "bg", "dev"))
            for i in xrange(1, min_ncomp + 1): file.write(
                "%9s\t%9s\t" % ("ity%i" % i, "dev"))
            for i in xrange(1, min_ncomp + 1): file.write(
                "%9s\t%9s\t" % ("tau%i" % i, "dev"))
            file.write("\n")
        for ob in self.spectralist: ob.showreport_1row(file=file,
                                                       min_ncomp=min_ncomp)

    def showreport(self, T=None, acc=None, verbosity=0, NNRLA=-1):
        clock = time.clock()
        print "*********************************************"
        print "Set name:", self.name
        if T: print "T= %.2e " % (T)
        print "X2= %.3e(mean)  %.3e(min)  %.3e(deviation)  %.3e(curr)" % (
        self.chi2_mean, self.chi2_best, S.sqrt(self.chi2_var), self.chi2)
        if acc is not None:
            print "accepted: %i  (%.1f%% , %.1f%%increased)" % (
            acc, self.accratio * 100, self.inc_dec_ratio * 100)
            print "NNRLA period: %.1f iter (average) " % (
            self.NNRLAcount / float(acc))
        print  "Time: %.5g s" % (clock - self.lastclock)
        self.lastclock = clock
        if verbosity > 0:
            print "Spectra:"
            for ob in self.spectralist:
                ob.showreport()
        if verbosity > 1:
            for ob in self.fitparlist: ob.showreport()
        if verbosity > 2:
            kk = self.spectralist[0]
            pylab.cla()
            pylab.gca().set_yscale('log')
            pylab.plot(kk.channeltimes, kk.exp[kk.roi])
            pylab.plot(kk.channeltimes, kk.sim)
        print "*********************************************"

    def graph_report(self, filename=None, show=True):
        newclr = newcolor(i0=2)
        # plot of spectra (exp, fit)
        pylab.subplot(211)
        pylab.cla()
        pylab.gca().set_yscale('log')
        pylab.xlabel('channel')
        pylab.ylabel('Cts')
        # plot residuals
        pylab.subplot(212)
        pylab.cla()
        pylab.xlabel('channel')
        pylab.ylabel('(sim-exp)/err')
        pylab.plot([self.roimin, self.roimax], [1, 1],
                   color='black')  # draw a base line for reference
        pylab.plot([self.roimin, self.roimax], [-1, -1],
                   color='black')  # draw a base line for reference
        print 'Plot legend:'
        for sp in self.spectralist:
            col = newclr.next()
            print  col, sp.name
            chi2, residuals = sp.recalculate_chi2(full_output=True,
                                                  forcecalc=True)
            pylab.subplot(211)
            if sp.exp[sp.roi].sum() > 0: pylab.plot(sp.roi, sp.exp[sp.roi],
                                                    linewidth=0,
                                                    markerfacecolor=col,
                                                    marker='o', markersize=3.)
            pylab.plot(sp.roi, sp.sim, color=col, linestyle='-')
            pylab.subplot(212)
            pylab.plot(sp.roi, residuals, markerfacecolor=col, linewidth=0,
                       marker='o', markersize=3.)
        if filename is not None:
            pylab.savefig(filename)
            print "\nGraphic output saved to '%s'\n" % filename
        if show: pylab.show()

    def simann(self, LM=None, startT=2., stopT=1e-3, stepT=.9, maxiter=S.inf,
               minaccratio=0.1, meltratio=0.97, tolerance=None, direct=True,
               LMmult=20, chi2min=1.):
        '''It performs a simulated annealing minimisation'''
        # TODO: Implement restarts?
        if LM is None: LM = len(self.unfold_perturbablelist()) * LMmult
        if maxiter < 1: maxiter = S.inf
        hardminaccratio = minaccratio * .1
        endflag = False
        iter = 0
        T = startT
        # pre-melting
        self.MCMC_generate(LM=LM, T=T, ireport=LM, NNRLA='auto', direct=False)
        if abort.abortRequested(): return  # check if we should abort
        while self.accratio < meltratio:
            T *= 10.
            self.MCMC_generate(LM=LM, T=T, ireport=LM, NNRLA='auto',
                               direct=False)
            print 'SimAnn: initial acc. ratio too low. Increasing T to %.2g' % T
            if abort.abortRequested(): return  # check if we should abort
        # The SA loop
        emitter.initCommandPBar.emit(int(-S.log(T)), int(-S.log(stopT)))
        while not endflag:
            self.MCMC_generate(LM=LM, T=T, ireport=LM, NNRLA='auto',
                               direct=(direct and iter > 4))
            if abort.abortRequested(): return  # check if we should abort
            T *= stepT
            iter += 1
            emitter.commandPBarValue.emit(int(-S.log(T)))
            # Check exit conditions
            if iter > maxiter:
                print '\nMaximum number of iterations reached\n'
                endflag = True
            if T < stopT:
                print '\nMinimum T reached\n'
                endflag = True
            if self.chi2_mean < chi2min and self.chi2_var < tolerance:
                print '\nMinimum chi2 reached\n'
                endflag = True
            if self.chi2_var < tolerance and iter > 15 and self.accratio < minaccratio:
                print '\nMinimum acceptance ratio reached (soft limit)\n'
                endflag = True
            if self.accratio < hardminaccratio:
                print '\nMinimum acceptance ratio reached (hard limit)\n'
                endflag = True

    def BI(self, LM, stabilisation=0., ireport=None, factor=None, iemit=-1,
           savehist=False):
        '''It performs a Bayesian Inference on the set (optionally with stabilisation
		savehist may be False or a file name'''
        if factor is None: factor = len(self.unfold_perturbablelist())
        if ireport is None: ireport = LM
        # do stabilisation
        if stabilisation > 0:
            emitter.initCommandPBar.emit(0, int((stabilisation + LM) * factor))
            self.MCMC_generate(LM=stabilisation, T=2.,
                               ireport=min(ireport, stabilisation),
                               savehist=False, NNRLA='auto', direct=False,
                               factor=factor, iemit=iemit)
        if abort.abortRequested(): return  # check if we should abort
        # and do the proper BI
        emitter.initCommandPBar.emit(int(-stabilisation * factor),
                                     int(LM * factor))
        self.MCMC_generate(LM=LM, T=2., ireport=ireport,
                           savehist=bool(savehist), NNRLA='auto', direct=False,
                           factor=factor, iemit=iemit)
        if abort.abortRequested(): return  # check if we should abort
        # at the end, put the mean values as the val for all parameters (because THAT is the real result of the BI, not the one from the last iteration)
        self.chi2 = self.chi2_mean
        for ob in self.fitparlist: ob.val = ob.mean
        self.calculate_chi2(recalc=True)
        if ireport > 0:
            print 'Results for the MEAN state obtained after %i BI iterations:' % (
            LM * factor)
            self.showreport(acc=LM * factor, verbosity=1)
        # Show the values for the BEST fit
        print 'Results for the "BEST chi2" state found in %i BI iterations:\n(non-normized intensities!)' % (
        LM * factor)
        print 'Best chi2: %5e' % (self.chi2_best)
        for ob in self.fitparlist: print "%9s: %9g" % (ob.name, ob.best)

        # Save the history of the parameters (with a header)
        if savehist:
            if isinstance(savehist, str):
                histfile = open(savehist, 'w')
            else:
                histfile = savehist
            if ireport > 0: print "\n Saving history of parameters in '%s'..." % savehist,
            print >> histfile, "# ", time.asctime()
            print >> histfile, "# History of the following parameters (in rows):"
            print >> histfile, "# ", tuple([ob.name for ob in self.fitparlist])
            S.savetxt(histfile, tuple([ob.hist for ob in self.fitparlist]))
            if ireport > 0: print " Done."
            histfile.close()
        self.confirm()

    def downhill(self, maxiter=S.inf, tolerance=None, ireport=-1):
        '''DO NOT USE. It performs a naive downhill minimisation. Only valid when very close to the min. Use localmin better'''
        self.confirm()
        self.n = 1
        self.chi2_mean = self.chi2
        self.chi2_var = 0
        endflag = False
        iter = 0
        istats = nstats = len(self.fitparlist) * 100
        if ireport > 0: ireport = nreport = max(ireport, nstats)
        while not endflag:
            iter += 1
            ireport -= 1
            istats -= 1
            fp = random.choice(self.fitparlist)
            SZ = S.zeros(4, dtype='d')
            for ob in fp.updatelist:  # TODO: This assumes that the fitpar's updatelist only contains discretepals instances!
                SZ += ob.calculate_NNRLA_SZ(fp, direct=True)
            fp.NNRLA_delta = SZ[3] / SZ[2]
            fp.NNRLA_sigma = 0
            fp.perturbate(direct=True)
            self.calculate_chi2()
            self.confirm()
            # show report if required
            if ireport == 0:
                self.showreport(acc=iter, verbosity=1)
                ireport = nreport
            # Check exit conditions
            if iter > maxiter: endflag = True
            if istats == 0:
                if self.chi2_var < tolerance: endflag = True
                # reset the stats
                self.n = 1
                self.chi2_mean = self.chi2
                self.chi2_var = 0
                istats = nstats

    def localmin(self, maxunbound=0, ireport=False, forcelimits=True):
        '''It uses functions of the scipy.optimize module to perform a local minimisation
		It tries to use a Levenberg-Marquardt Algorithm (LMA) but if the result is not within the limits, it
		packs the LMA between two L-BFGS-B algorithms (which are constrained multivariate minimisation algorithms).
		Estimation of errors:
		  The estimation of errors is based on the diagonal of the covariance matrix returned by the LMA.
		  In the case of the intensity parameters, the variances are normalised by the Frobenius norm of the intensities covariances
		  (this is done because of the way the intensity parameters are handled in the code)
		  Note that these errors aren t trustable at all. Use them only as indicators.
		For info on the L-BFGS-B algorithm, see:
				* C. Zhu, R. H. Byrd and J. Nocedal. L-BFGS-B: Algorithm 778: L-BFGS-B,
				FORTRAN routines for large scale bound constrained optimization (1997),
				ACM Transactions on Mathematical Software, Vol 23, Num. 4, pp. 550 - 560.
		'''
        emitter.initCommandPBar.emit(0, 5)
        # start from a clean point
        self.confirm()
        self.clearstats()
        # get a map of free parameters into vectors
        myargs, myx, minmax = self.get_fitpars(val=True, minmax=True,
                                               onlyfree=True)
        # identify the intensity components in the myargs map.
        itys = []
        for sp in self.spectralist: itys += sp.itylist
        itys = unique(itys)  # clean the list of repeated itys
        temp = []
        nonfreeitys = 0
        for ob in itys:  # clean the list of non-free intensities
            if ob.free:
                temp.append(ob)
            else:
                nonfreeitys += 1
        itys = temp
        nitys = len(itys)
        for i in range(nitys): itys[i] = objectindex(itys[i], myargs)
        # itys now contains the indexes for the parameters that are intensities in myargs
        itys = S.array(itys)
        # Try to do a (relatively fast) *unbounded* minimisation using a Levenberg-Marquardt algorithm
        if ireport: print "\nTrying a Levenberg-Marquardt (LMA) fit\n"
        emitter.commandPBarValue.emit(1)
        #		self.showreport(verbosity=1)
        if abort.abortRequested(): return  # check if we should abort
        myx, cov_x, infodict, mesg, ier = optimize.leastsq(
            self.interfacefunction_leastsq, myx, tuple(myargs), Dfun=None,
            full_output=1, col_deriv=0, maxfev=0, epsfcn=0.0, factor=100,
            diag=None)
        #		for i in xrange(len(myx)): myargs[i].mean=myx[i]  #DEBUG
        #		if ireport: self.showreport(verbosity=1)#DEBUG
        # check if all parameters are within bonds
        minmaxarray = S.array(minmax)
        minmaxarray[:, 1] = S.where(minmaxarray[:, 1] > None, minmaxarray[:, 1],
                                    S.inf)
        # check if all the itys are negative (not only the free ones)!, in which case they can simply be all multiplied by -1
        if nonfreeitys == 0 and (myx[itys] < 0).all():
            # 			print "!!!!!!!!!!"
            myx[
                itys] *= -1.  # the covariance matrix does not need to be converted because it is invariant under this change of sign
            for i in itys: myargs[i].val = myargs[i].mean = myx[i]
        withinlimits = (
        (myx > minmaxarray[:, 0]) * (myx < minmaxarray[:, 1])).all()
        if not withinlimits and forcelimits:
            if ireport:
                print "\nLMA failed to give result within limits:"
                for fp in myargs:
                    if fp.maxval is None:
                        maxval = S.inf
                    else:
                        maxval = fp.maxval
                    if not (fp.minval < fp.val < maxval): fp.showreport()
                print "\nTrying a bounded minimisation (may be slow)\nProgress:",
            # reset the state
            self.undolist += myargs
            self.undo()
            myargs, myx, minmax = self.get_fitpars(val=True, minmax=True,
                                                   onlyfree=True)  # redo the mapping
            # Do a  L-BFGS-B minimisation (slow but bounded)
            if abort.abortRequested(): return  # check if we should abort
            myx, chi2, infodict = optimize.fmin_l_bfgs_b(self.interfacefunction,
                                                         myx, args=tuple(myargs),
                                                         approx_grad=1,
                                                         bounds=minmax, m=10,
                                                         iprint=-1)
            emitter.commandPBarValue.emit(2)
            if ireport: print '#',
            # Do several runs of unbound simplex downhill till it converges
            warnflag, i = True, 0
            while warnflag and i < maxunbound:
                if abort.abortRequested(): return  # check if we should abort
                i += 1
                #				myx,chi2,iter,fcalls,warnflag=optimize.fmin(self.interfacefunction,myx,myargs,disp=False, full_output=True)
                myx, cov_x, infodict, mesg, ier = optimize.leastsq(
                    self.interfacefunction_leastsq, myx, tuple(myargs),
                    Dfun=None, full_output=1, col_deriv=0, maxfev=0, epsfcn=0.0,
                    factor=100, diag=None)
                warnflag = (ier != 1)
                #				print mesg
                if ireport: print '>',
            emitter.commandPBarValue.emit(3)
            # Do a second L-BFGS-B minimisation
            #			myx=S.where(myx<minmaxarray[:,0], minmaxarray[:,0], myx)
            #			myx=S.where(myx>minmaxarray[:,1], minmaxarray[:,1], myx)
            if abort.abortRequested(): return  # check if we should abort
            myx, chi2, infodict = optimize.fmin_l_bfgs_b(self.interfacefunction,
                                                         myx, args=tuple(myargs),
                                                         approx_grad=1,
                                                         bounds=minmax, m=10,
                                                         iprint=-1)
            emitter.commandPBarValue.emit(4)
            if ireport: print '#\n'
        # Confirm and show the results
        emitter.commandPBarValue.emit(5)
        self.calculate_chi2(recalc=True)
        self.confirm()  # by doing this confirm, the .val of each parameter is copied to the .mean
        self.clearstats()
        err = S.diag(cov_x)
        # put errors for the raw parameters
        for i in xrange(len(err)): myargs[i].var = err[i]
        # now caculate the errors for the intensities after normalisation for each espectrum independently
        for dp in self.spectralist:
            if dp.freeityindexes.size > 0:
                # find the indexes for the free intensities for this spectrum
                aindexes = S.zeros(dp.freeityindexes.size, dtype='i')
                for i, j in zip(dp.freeityindexes, xrange(aindexes.size)):
                    # aindexes contains the indexes (in myargs) of the free intensities for this spectrum
                    aindexes[j] = objectindex(dp.itylist[i], myargs)
                a = myx[aindexes]
                asum = a.sum()
                # find the jacobian of the parameters transformation:
                Jac = S.identity(len(myargs))  # for most of the parameters, there is no transformation
                for i in aindexes:
                    Jac[i, aindexes] = myx[
                        i]  # the row corresponding to the intensity a_i is all equal to a_i...
                    Jac[
                        i, i] -= asum  # ...except for the diagonal, where it is (a_i-sum{a})
                    Jac[i, aindexes] *= (1 - dp.fixeditysum) / (
                    asum ** 2)  # Jac_ij= (norm_free/sum_k{a_k})(a_i-dirac_ij*sum_k{a_k})    ... for i,j,k running over the free intensities
                # The new covariance matrix is given by cov_new=J.cov.J^T
                cov_new = S.dot(Jac, S.dot(cov_x, Jac.T))
                dp.ity_var[dp.freeityindexes] = S.diag(cov_new)[
                    aindexes]  # fill the ity_var array for each spectrum
        if ireport: self.showreport(verbosity=1)
        return infodict  # returns the output dictionary from the last call to the L-BFGS-B algorithm

    def compatible(self, other, detail=False):
        '''Tests compatibility of two palssets.
		Compatible means:
			same number of spectra (key "nesp")
			same number of components in each spectra (assumes same ordering of spectra !)
		'''
        res = {}
        res["nesp"] = (len(self.spectralist) == len(other.spectralist))
        temp = True
        for ob1, ob2 in zip(self.spectralist, other.spectralist): temp *= (
        ob1.ncomp == ob2.ncomp)
        res["ncomp"] = temp
        temp = True
        for v in res.values: temp *= v
        res["total"] = temp
        if detail:
            return res
        else:
            return res["total"]

    def importvalues(self, other, onlyfree=False, flexicomp=False):
        '''Fills values of the fitpars taking them from a compatible set'''
        success = (len(self.spectralist) == len(other.spectralist))
        #		success=True
        for ob1, ob2 in zip(self.spectralist, other.spectralist):
            success *= ob1.importvalues(ob2, onlyfree=onlyfree,
                                        flexicomp=flexicomp)
        return success

    def addcomponent(self, tau, commontau=False, commonity=False):
        '''returns another palsset which is similar to itself but whose spectra ALL have an extra component
		The new spectra are initialysed using discretepals.importvalues() with the flexicomp option.
		In the case of palsset having more than one spectra:
			If commontau=True, the new component lifetime is common among all spectra
			If commontau=True, the new component lifetime is common among all spectra
		'''
        pass

    def interfacefunction(self, x, *args):
        '''An interface function be called from scpy.optimize methods.
		The xmap is a list of fitpar objects of which x are its vals'''
        # decode args
        xmap = args
        # decode x
        for i in xrange(len(x)):
            #			if xmap[i].val!=x[i]: xmap[i].val=x[i]
            xmap[i].val = x[i]
        chi2 = self.calculate_chi2(recalc=True)

        return chi2

    def interfacefunction_leastsq(self, x, *args):
        '''An interface function be called from scpy.optimize.leastsq()
		It expects just one argument from the *args tuple:  xmap: a list of fitpar objects of which x are its vals
		Returns a vector containing a concatenation of the residuals of each spectrum in this set'''
        # decode args
        xmap = args
        # decode x
        for i in xrange(len(x)): xmap[i].val = x[i]
        # calculate the residuals of each spectrum
        res = []
        for ob in self.spectralist:  # TODO: Optimize code (eliminate append, maybe calculate residuals without callng recalculate_chi2(), and so...)
            chi2, residuals = ob.recalculate_chi2(full_output=True)
            res.append(residuals)
        return S.concatenate(res)

    def get_fitpars(self, val=True, minmax=True, onlyfree=True):
        '''returns a list of fitpars related with this palsset instance.
		If val=True, (or minmax==True) returns also an array with the fitpars val
		If minmax==True returns also two other arrays containing the lower and upper bounds
		If onlyfree==True, only the perturbable fitpars are included in the output'''
        if onlyfree:
            fpmap = self.unfold_perturbablelist()
        else:
            fpmap = []
            for ob in self.spectralist: fpmap += ob.itylist + ob.taulist + [
                ob.bg, ob.fwhm, ob.c0]
            fpmap = unique(fpmap)
        if minmax:
            return fpmap, S.array([ob.val for ob in fpmap]), [
                (ob.minval, ob.maxval) for ob in fpmap]
        elif val:
            return fpmap, S.array([ob.val for ob in fpmap])
        else:
            return fpmap


# class partial_discretepals(object):
#	''' This class provides a way of storing the quantities that are required for initialising a discretepals object.
#	It has a method that can be used to check wether all the required quantities are already defined'''
#	def __init__(self, name=None, expdata=None, roi=None, taulist=None, itylist=None, bg=None, fwhm=None, c0=None, psperchannel=None, area=None):
# #		self.checklist={'name'=(3>4),
# #		                'expdata'=expdata is not None,
# #		                'roi'=roi is not None,
# #		                'taulist'=taulist is not None,
# #		                'itylist'=itylist is not None,
# #		                'bg'=bg is not None,
# #		                'fwhm'=fwhm is not None,
# #		                'c0'=c0 is not None,
# #		                'psperchannel'=psperchannel is not Nonelse,
# #		                'area'=area is not None}
#		self.name=name
#		self.expdata= expdata
#		self.roi=roi
#		self.taulist=taulist
#		self.itylist=itylist
#		self.bg =bg
#		self.fwhm =fwhm
#		self.c0 =c0
#		self.psperchannel =psperchannel
#		self.area =area
#	def isready(self, fulloutput=False):
#		if ((self.expdata is None) or (self.taulist is None)  or (self.itylist is None)  or (self.bg is None)  or (self.fwhm is None)
#		    (self.c0 is None) or (self.psperchannel is None) ): return False
#
#
#
#		#TODO
# #		(self, name=None, expdata=None, roi=None, taulist=None, itylist=None, bg=None, fwhm=None, c0=None, psperchannel=1, area=1.)


def MELTlikeROI(expdata, headerlines=0, left_of_max=5, stopdat=None):
    '''generates a ROI that goes from left_of_max channels before the peak max to the channel stopdat'''
    if isinstance(expdata, str):
        #		cmax=S.array(pylab.load(expfilename,skiprows=headerlines),dtype='d').argmax(0)
        cmax = S.loadtxt(fname, skiprows=hdrlns, dtype='d').argmax(0)
    else:
        cmax = S.array(expdata, dtype='d').argmax(0)
    roi = S.arange(cmax - left_of_max, stopdat + 1)
    return roi


def to_list(N, parameter):
    if isinstance(parameter, list):
        if len(parameter) != N: raise ValueError(
            "The number of elements of the list (%i) does not match N (%i)" % (
            len(parameter), N))
    else:
        parameter = N * [parameter]
    return parameter


def assignfitpar(v, namedpars=None):
    '''it returns a fitpar.
	If v is a tuple containing (val,min,max), it is instantiated as a new free parameter.
	If v is a single value, it is instantiated as a FIXED fitpar
	If v is the name of a named parameter, it is taken from the namedpars dictionary
	if using a named parameter with an * appended it returns the SAME parameter (so it can be common)
	if the * is not appended, it returns a unique COPY (so it won t be common)'''
    if isinstance(v, str):
        if v[-1] == '*':
            return namedpars[v[:-1]]  # returns the named parameter
        else:
            return copy.deepcopy(
                namedpars[v])  # returns a COPY of named parameter
    elif S.size(v) == 1:
        return fitpar(val=v, name='!', free=False)
    else:
        return fitpar(val=v[0], name='@', minval=v[1], maxval=v[2], free=True)


def findconnectedspectra(spectrum):
    '''returns a list of spectra instances that are connected (directly or indirectly) to the given one by means of common parameters'''
    L1 = [spectrum]  # we start with the given spectrum
    n_old = 0
    n = 1
    while (
        n_old < n):  # This is done while the list is growing (i.e., while new connected spectra ar found)
        for el in L1:  # go through all elements in the connected list
            for fp in el.perturbablelist:  # and go through all their fitpars
                if len(
                        fp.updatelist) > 1:  # note, if len<1 then the only element must be "el" so we don't waste time adding it
                    L1 += fp.updatelist  # include in L1 all spectra that depend on each given fitpar
            L1 = unique(
                L1)  # After including them, clean the list of repetitions
        n_old = n
        n = len(L1)
    # when we exit from previous loop, it means no additional connected spectra are found
    return L1


def distributeinsets(dplist):
    '''gets a list of discretepals instances and analyses the interdependences in their free parameters to group them in palssets
	It returns a list of pals sets
	Note: simple algorithm but very innefficient (although I dont care because it is done only once)'''
    connections = [findconnectedspectra(dp) for dp in
                   dplist]  # find the connection groups for each spectrum in the list
    exclude = []
    # check the uniqueness of each case
    for i in xrange(len(connections)):
        if not exclude.count(i):  # if i is not amongst the already excluded
            for j in xrange(i + 1, len(connections)):
                if len(connections[i]) == len(unique(
                                connections[i] + connections[
                            j])):  # this is true only the elements of connections[j] are the same as those of  connections[i]
                    exclude.append(j)
    # Now we eliminate the connections which aren't unique
    exclude = unique(exclude)
    exclude.sort(reverse=True)
    for i in exclude: connections.pop(i)
    # Finally, we instantiate palssets with the non-connected unique groups
    result = []
    pad = int(S.ceil(S.log10(max(1, len(
        connections)))))  # find the number of digits needed for 0-padded sequential number
    for i in xrange(len(connections)):
        result.append(palsset(name='SET_%0*i' % (pad, i),
                              spectralist=connections[
                                  i]))  # instantiate spectrum set and init it with a group of connected spectra
    return result


def printwarning(message, wait=False):
    '''It prints a warning, returns it for logging and, optionally, waits for user acknowledgement'''
    if isinstance(message, list):
        if len(message) > 0:
            print '\n******************************************************************'
            print '%i warning(s) occurred:' % len(message)
            for ob in message: print ob
            print '******************************************************************\n'
        return len(message)
    else:
        w = "WARNING (%s): %s" % (time.asctime(), message)
        print "\n%s\n" % w
        if wait:
            print "(press ENTER to continue)\n"
            raw_input()
        return [w]


def mainprogram(warningslog=[]):
    '''Initialises, and then runs the command interpreter'''
    # import the input info
    import PAScual_input as userinput
    time.clock()  # Set start of time measuring (we ignore the import time for scipy and pylab)   )
    S.random.seed(userinput.seed)  # Seeding the random generators.

    # initialise a tee for output
    outputfile = None
    if userinput.outputfile:
        outputfile = open(userinput.outputfile, 'w')
        sys.stdout = tee(sys.stdout, outputfile)
        fnamepreffix = userinput.outputfile.rsplit('.', 1)[
            0]  # Outputfilenames preffix
    else:
        fnamepreffix = '~dpout'

    # saving a copy of the input file for future refference
    copy2("PAScual_input.py", fnamepreffix + '_input.py')

    # first instantiate the named parameters. (And replace the tuple by the instance in the namedpars dictionary)
    try:
        temp = userinput.namedparameters
    except AttributeError:
        userinput.namedparameters = {}
    namedpars = {}
    # note that the diff beetween namedpars and userinput.namedparameters is that the former will only contain already instantiated fitpars
    for k in userinput.namedparameters.keys():
        if isinstance(userinput.namedparameters[k],
                      str): warningslog += printwarning(
            "Defining a named parameter using another named parameter may lead to problems. You are warned.",
            wait=True)
        namedpars[k] = userinput.namedparameters[k] = assignfitpar(
            userinput.namedparameters[k], namedpars)

    ###find out the number of spectra to be fitted
    if not isinstance(userinput.expfilenames, list): userinput.expfilenames = [
        userinput.expfilenames]
    try:
        if not isinstance(userinput.skipfilenames,
                          list): userinput.skipfilenames = [
            userinput.skipfilenames]
    except AttributeError:
        userinput.skipfilenames = []
    for fn in userinput.skipfilenames:  # eliminate the ones that the user wants to skip:
        try:
            userinput.expfilenames.remove(fn)
        except ValueError:
            pass
    nspectra = len(userinput.expfilenames)

    ###Start doing some trivial input processing
    userinput.headerlines = to_list(nspectra, userinput.headerlines)
    userinput.psperchannel = to_list(nspectra, userinput.psperchannel)
    userinput.fwhm = to_list(nspectra, userinput.fwhm)
    userinput.tau = to_list(nspectra, userinput.tau)

    # obtain number of components from the tau definition
    userinput.ncomp = [len(el) for el in userinput.tau]

    ###read the spectra from ascii file(s).
    expdata = []
    print "\nReading %i spectra" % nspectra,
    for fname, hdrlns in zip(userinput.expfilenames, userinput.headerlines):
        print '.',
        if fname is None:
            expdata.append(None)  # No exp data is given (we will only simulate)
        else:
            #			expdata.append(S.array(pylab.load(fname,skiprows=hdrlns),dtype='d').flatten()) # load datafile: ascii format
            expdata.append(
                S.loadtxt(fname, skiprows=hdrlns, dtype='d').flatten())
        #
        #	for es in expdata:
        #		pylab.cla()
        #		pylab.gca().set_yscale('log')
        #		pylab.plot(es)
        #		pylab.show()

    ###Now some more complex input processing:
    try:
        userinput.roi = to_list(nspectra,
                                userinput.roi)  # explicit ROI definition
    except AttributeError:  # if roi is not explicitely defined, we expect MELT-like parameters (otherwise it is an error).
        userinput.left_of_max = to_list(nspectra, userinput.left_of_max)
        userinput.stopdat = to_list(nspectra, userinput.stopdat)
        userinput.roi = []
        for i in xrange(nspectra): userinput.roi.append(
            MELTlikeROI(expdata[i], headerlines=userinput.headerlines[i],
                        left_of_max=userinput.left_of_max[i],
                        stopdat=userinput.stopdat[i]))
    try:
        userinput.bg = to_list(nspectra, userinput.bg)  # explicit bg definition
    except AttributeError:  # if not explicit,calculate it from startbg and stopbg
        userinput.startbg = to_list(nspectra, userinput.startbg)
        userinput.stopbg = to_list(nspectra, userinput.stopbg)
        userinput.bg = to_list(nspectra, None)
    try:
        userinput.c0 = to_list(nspectra, userinput.c0)  # explicit c0 definition
    except AttributeError:
        userinput.c0 = to_list(nspectra,
                               None)  # if not explicit, c0 will be calculated later from the spectrum
    try:
        userinput.ity = to_list(nspectra,
                                userinput.ity)  # explicit ity definition
    except AttributeError:
        userinput.ity = [nc * ((1, 0, None),) for nc in
                         userinput.ncomp]  # if not explicit, init them all the same (and free parameters)

    # instantiate all the fitpar and the spectrum objects
    spectra = []
    print "\nInitialising simulations",
    for i in xrange(nspectra):
        print '.',
        # Assign fwhm
        fwhm = assignfitpar(userinput.fwhm[i], namedpars)
        # Assign c0
        if userinput.c0[i] is not None:
            c0 = assignfitpar(userinput.c0[i], namedpars)
        else:
            temp1 = float(
                expdata[i].argmax(0))  # a coarse approx of the time 0 channel
            temp2 = max(1., fwhm.val * 2. / userinput.psperchannel[i])  # a
            c0 = assignfitpar((temp1, temp1 - temp2, temp1 + temp2), namedpars)
        # assign bg
        if userinput.bg[i] is not None:
            bg = assignfitpar(userinput.bg[i], namedpars)
        else:
            temp1 = expdata[i][userinput.startbg[i]:userinput.stopbg[i]].mean()
            temp2 = 10 * max(10, S.sqrt(temp1), expdata[i][userinput.startbg[i]:
            userinput.stopbg[i]].std())
            bg = assignfitpar((temp1, max(0., temp1 - temp2), temp1 + temp2),
                              namedpars)
        # assign tau
        taulist = [assignfitpar(tau, namedpars) for tau in userinput.tau[i]]
        # assign ity
        itylist = [assignfitpar(ity, namedpars) for ity in userinput.ity[i]]

        #		print 'DEBUG:'
        #		for ob in itylist:ob.showreport()
        #		raw_input()

        # instantiate the spectrum (we will have a list of spectra instances)
        if userinput.expfilenames[i] is not None:
            dpname = os.path.basename(userinput.expfilenames[i]).rsplit('.', 1)[
                0]
            fake = False
        else:
            dpname = 'FAKE%i' % i
            fake = True
        spectra.append(
            discretepals(name=dpname, expdata=expdata[i], roi=userinput.roi[i],
                         taulist=taulist, itylist=itylist, bg=bg, fwhm=fwhm,
                         c0=c0, psperchannel=userinput.psperchannel[i],
                         fake=fake, area=1))

    print "\nGenerating sets"
    # Now instantiate the palsset(s) and register spectra
    palssetslist = distributeinsets(spectra)
    npalssets = len(palssetslist)
    # Now generalise (to multiple sets) the fitting inputs from the user:
    userinput.fitmode = to_list(npalssets, userinput.fitmode)
    userinput.SA_maxiter = to_list(npalssets, userinput.SA_maxiter)
    userinput.SA_tol = to_list(npalssets, userinput.SA_tol)
    userinput.SA_stopT = to_list(npalssets, userinput.SA_stopT)
    userinput.SA_maxiter = to_list(npalssets, userinput.SA_maxiter)
    userinput.SA_direct = to_list(npalssets, userinput.SA_direct)
    userinput.SA_meltratio = to_list(npalssets, userinput.SA_meltratio)
    userinput.LOCAL_tol = to_list(npalssets, userinput.LOCAL_tol)
    userinput.LOCAL_maxiter = to_list(npalssets, userinput.LOCAL_maxiter)
    userinput.BI_stab = to_list(npalssets, userinput.BI_stab)
    userinput.BI_length = to_list(npalssets, userinput.BI_length)
    userinput.BI_report = to_list(npalssets, userinput.BI_report)

    #	fake=spectra[0].fake(area=1e6)
    #	pylab.plot(spectra[0].roi,fake)
    #	pylab.show()
    #	raw_input()

    # Main loop of fitting. for all palssets
    saveslot = saveslot_auto = saveslot_user = None  # before starting with the fit of each palsset, reset the save slots
    logfilesdict = {}
    for iset in xrange(npalssets):
        temp = " Processing %s (%s) " % (
        palssetslist[iset].name, time.asctime())
        starwidth = 5 + len(temp) + 5
        print "\n" + (starwidth * "*")
        print "*****%s*****" % temp
        print (starwidth * "*") + "\n"
        print '%s is comprised of the following spectra: ' % palssetslist[
            iset].name,
        for ob in palssetslist[iset].spectralist: print ob.name,
        print
        # parse commands for this set
        for text in userinput.fitmode[iset]:
            try:  # This try-except block is here to catch CTRL+C presses while executing a given program
                text = text.split(None, 1)
                cmd = text[0].upper()  # the commands are case insensitive.
                if len(text) == 2:
                    args = text[
                        1]  # the arguments are not case insensitive *by default*
                else:
                    args = None
                # LOAD command
                if cmd == 'LOAD':
                    print '\n********* Loading previous results **************\n'
                    if args:  # load from file
                        print "\nPrevious status loaded from '%s'\n" % args
                        try:
                            saveslot = pickle.load(open(args, 'rb'))
                        except IOError:
                            saveslot = None
                    else:
                        saveslot = saveslot_user  # load from saveslot_user slot
                    if saveslot:  # check if there is something to load
                        temp = copy.deepcopy(palssetslist[
                                                 iset])  # save a backup before attempting import
                        success = palssetslist[iset].importvalues(saveslot,
                                                                  onlyfree=False,
                                                                  flexicomp=False)  # import the values
                        if not success:  # if the import was not satisfactory, undo changes
                            warningslog += printwarning(
                                "Cannot LOAD. %s is not compatible with %s" % (
                                palssetslist[iset].name, saveslot.name))
                            palssetslist[iset] = copy.deepcopy(temp)
                    else:
                        warningslog += printwarning(
                            "Cannot LOAD. Nothing previously saved")
                    palssetslist[iset].calculate_chi2()
                    palssetslist[iset].confirm()
                    palssetslist[iset].clearstats()
                # SA command
                elif cmd == 'SA':
                    print '\n********* Performing Simulated Annealing **************\n'
                    palssetslist[iset].simann(minaccratio=0.1,
                                              direct=userinput.SA_direct[iset],
                                              stopT=userinput.SA_stopT[iset],
                                              maxiter=userinput.SA_maxiter[
                                                  iset],
                                              tolerance=userinput.SA_tol[iset],
                                              meltratio=userinput.SA_meltratio[
                                                  iset])
                elif cmd == 'LOCAL':
                    if args:
                        args = args.strip().upper()
                        forcelimits = (args != 'NOLIMITS')
                    else:
                        forcelimits = True
                    print '\n********* Performing Local search **************\n'
                    temp = copy.deepcopy(palssetslist[
                                             iset])  # making backup in case LOCAL minimisation fails
                    try:
                        palssetslist[iset].localmin(maxunbound=10, ireport=True,
                                                    forcelimits=forcelimits)
                    except ValueError:
                        warningslog + printwarning(
                            "LOCAL minimisation of %s failed. Skipping!" %
                            palssetslist[iset].name)
                        palssetslist[
                            iset] = temp  # recovering original from backup
                # BI command
                elif cmd == 'BI':
                    print '\n********* Performing Bayesian Inference **************\n'
                    palssetslist[iset].BI(LM=userinput.BI_length[iset],
                                          stabilisation=userinput.BI_stab[iset],
                                          ireport=userinput.BI_report[iset],
                                          savehist=userinput.BI_savehist)
                # SAVE command
                elif cmd == 'SAVE':
                    print '\n********* Saving results **************\n'
                    saveslot_user = copy.deepcopy(palssetslist[iset])
                    saveslot_user.name = "Saved(%s)" % palssetslist[iset].name
                    if args:
                        pickle.dump(saveslot_user, open(args, 'wb'),
                                    -1)  # if a filename is provided, save a copy there
                        print "\nCurrent status saved in '%s'\n" % args
                # REPORT command
                elif cmd == 'REPORT':
                    print '\n********* Reporting **************\n'
                    palssetslist[iset].showreport(verbosity=1)
                    if args:
                        if args.upper().strip() == 'G': palssetslist[
                            iset].graph_report()
                    # FAKE command.
                elif cmd == 'FAKE':
                    print '\n********* Generating fake spectra **************\n'
                    filename = None
                    if args:
                        args = args.split(None, 1)
                        area = float(args[0])
                        if len(args) == 2: filename = args[1]
                    else:
                        area = 1e6
                    #					temp=copy.deepcopy(palssetslist[iset])
                    temp = palssetslist[
                        iset]  # not a deepcopy because we don't need to backup
                    for sp in temp.spectralist:
                        sp.exp[sp.roi] = sp.fake(area=area)
                        sp.exparea = sp.exp[sp.roi].sum()
                        sp.deltaexp = S.where(sp.exp < 4, 2., S.sqrt(sp.exp))
                        sp.recalculate_chi2(forcecalc=True)
                    #						print sp.showreport_1row()
                    temp.showreport(verbosity=1)
                    #					temp.graph_report()
                    if filename:
                        suffix = ''
                        for sp in temp.spectralist:
                            if len(temp.spectralist) > 1: suffix = sp.name
                            print "\nFake spectrum written in '%s'\n" % (
                            filename + suffix)
                            #							S.savetxt(filename+suffix,sp.exp)
                            sp.saveAs_LT(filename + suffix)
                elif cmd == 'LOG':
                    header = False
                    if args:
                        if args in logfilesdict:
                            logfile = logfilesdict[args]
                        else:
                            logfile = open(args,
                                           'a')  # the file is opened in append mode
                            logfilesdict[args] = logfile
                            header = True
                    else:
                        logfile = None
                    palssetslist[iset].showreport_1row(file=logfile,
                                                       min_ncomp=max(
                                                           [ob.ncomp for ob in
                                                            spectra]),
                                                       header=header)
                # ADDCOMPONENT command
                elif cmd == 'ADDCOMPONENT':
                    palssetslist[iset] = palssetslist[
                        iset].addcomponent()  # TODO
                # UNRECOGNISED command
                else:
                    warningslog += printwarning(
                        "Command not recognised (%s). Skipping\n" % cmd)
                # after each command, autosave the last state of the palsset
                saveslot_auto = copy.deepcopy(palssetslist[iset])
                if outputfile: outputfile.flush()
            # Handle Keyboard interrupts
            except KeyboardInterrupt:
                warningslog += printwarning(
                    ' %s command interrupted. \nPress CTRL+C again to exit completely (or ENTER to skip this command only)' % cmd,
                    wait=True)
                pass


def safemain():
    warningslog = []
    try:
        mainprogram(warningslog)
    except:
        printwarning(
            ('\nSome problem Occurred during the execution.\n' +
            'Maybe some previous warning (summarised below) may give a hint.\n' +
            'Check also the error messages below.'),
            wait=True)
        printwarning(warningslog)
        raise
    printwarning(warningslog)
    print '\n\n********* DISCRETEPALS took %5.3f seconds of cpu time ********* \n' % time.clock()
    return 0


def test_component():
    dpp = discretepals()
    pps = 50.
    ch = S.arange(1024, dtype='d')
    cc0 = 200.
    tt0 = cc0 * pps
    tt = ch * pps - tt0  # time in channel boundaries
    ttm = tt + (pps * 0.5)  # times in the middle of the channels
    ttau = 1111
    bbg = 100
    AA = 1e7

    y1 = bbg + dpp.calculate_convoluted_decay_integCh(tt, tau=ttau, intsty=AA,
                                                      sigma=100.)
    y2 = dpp.calculate_convoluted_decay(ttm, tau=ttau, intsty=ttau, sigma=100.)
    y2 = bbg + AA * y2 / y2.sum()
    pylab.plot(ch, y1)
    pylab.plot(ch, y2)
    pylab.gca().set_yscale('log')
    pylab.show()

def start():
    try:
        import pylab
    except:
        print >> sys.stderr, "Pylab could not be imported. Graphical output won't be supported"
    safemain()

if __name__ == '__main__':
    start()
#	test_component()
# Call the main program
#	import profile	
#	profile.run('mainprogram()','gpprofile')
