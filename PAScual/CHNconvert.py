###################################################################################
#     CHNconvert: Batch conversion of MAESTRO CHN Files to ASCII
#     Copyright (C) 2007  Carlos Pascual-Izarra < cpascual [AT] users.sourceforge.net >
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.
####################################################################################

import glob
import sys

import CHNfiles

#############################################
## Change the following options to your needs


# Input file names (with path) (accepts regular wildcards such as *, ?,...):
FILES = "./data/chntest/*.chn"

COLUMNS = 1  # number of columns (will be 0-padded if needed)
EXTENSION = ".dat"  # extension of the output files

WRITECHANNEL = True  # write the channel number?

LTOUTPUT = False  # write an LT header?
LT_description = "LT_description"
LT_nsperchannel = "LT_nsperchannel"
LT_key = "LT_key"
LT_fwhm = "LT_fwhm"

## End of user options
##############################################


#############################################
##Do not modify the lines below unless you know what you are doing

if __name__ == '__main__':
    if len(sys.argv) > 1:
        filenames = sys.argv[1:]
    else:
        filenames = glob.glob(FILES)
    print "Converting %i files..." % len(filenames)
    for f in filenames:
        print "'%s' " % f,
        spectrum = CHNfiles.CHN(f)
        ASCIIfile = f.rsplit('.', 1)[0] + EXTENSION
        if LTOUTPUT:
            spectrum.toLT(ASCIIfile, description=LT_description,
                          nsperchannel=LT_nsperchannel, key=LT_key,
                          fwhm=LT_fwhm, ncol=COLUMNS, onError='w')
        else:
            spectrum.toASCII(ASCIIfile, ncol=COLUMNS, hdr="", onError='w',
                             writechannel=WRITECHANNEL)
        print "--> '%s' (%i columns) " % (ASCIIfile, COLUMNS)
