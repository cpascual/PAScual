''' Tests of installation'''
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


print "Testing the required Python packages"

##print '**Required for PAScual.py'
print '\nnumpy...',
try: import numpy as t1
except:	print "Failed"
else: 
	print 'ok, version:',t1.version.version

print '\nscipy...',
try: import scipy as t2
except:	print "Failed"
else: 
	print 'ok, version:',t2.version.version

##print '**Required for graphs in text mode'

print '\nmatplotlib...',
try: import matplotlib as t3
except:	print "Failed"
else: 
	print 'ok, version:',t3.__version__

##print '**Required for PAScualGUI.py'

print '\nPyQt...',
try: import PyQt4 as t4
except:	print "Failed"
else: 
	print 'ok, version:','??'

print '\nPyQwt...',
try: import PyQt4.Qwt5 as t5
except:	print "Failed"
else: 
	print 'ok, version:','??'

print '\n\nTesting PAScual.py'
try: import PAScual as t6
except:	print "Failed"
else: 
	print 'ok, version:',t6.__version__

raw_input('\n\nPress <Enter> key to finish')