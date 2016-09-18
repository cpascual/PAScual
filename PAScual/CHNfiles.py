###################################################################################
#     CHNfiles: support for reading/converting MAESTRO CHN Files
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

import struct
import sys
from scipy import array, savetxt, zeros, concatenate, arange


class CHN(object):
    def __init__(self, CHNfile):
        self.hdr, self.data = self.readCHN(CHNfile)
        (self.ftype, self.mca_num, self.segment, self.secs, self.realtime,
         self.livetime, self.acqtime, self.channoffset, self.nchann) = self.hdr

    @staticmethod
    def readCHN(CHNfile):
        if isinstance(CHNfile, (str, str)): CHNfile = open(CHNfile, 'rb')
        raw = CHNfile.read()
        CHNfile.close()
        # the header contains the following: (ftype,mca_num,segment,secs,realtime,livetime,acqtime,channoffset,nchann)
        hdrfmt = 'h h h 2s i i 12s h h'
        hdrsize = struct.calcsize(hdrfmt)
        hdr = struct.unpack(hdrfmt, raw[:hdrsize])
        if hdr[0] != -1: raise ValueError(
            'The file is not recognised as Ortec CHN format')
        datfmt = "%ii" % (hdr[8] - hdr[
            7])  # hdr[8] is the number of channels and hdr[7] is the channel offset
        datsize = struct.calcsize(datfmt)
        dat = array(struct.unpack(datfmt, raw[hdrsize:hdrsize + datsize]),
                    dtype='i')
        return hdr, dat

    def toASCII(self, ASCIIfile, ncol=1, hdr="", onError='w',
                writechannel=False):
        if isinstance(ASCIIfile, str): ASCIIfile = open(ASCIIfile, 'w')
        ASCIIfile.write(hdr)
        if ncol > 1:
            nrow = self.data.size // ncol
            rm = self.data.size % ncol
            if rm > 0:
                nrow += 1
                if onError == 'w':
                    print>> sys.stderr, 'Warning: padded with %i zeros' % (
                    ncol - rm)
                elif onError == 'n':
                    pass
                else:
                    raise ValueError(
                        'Data size does not fit into %i columns' % ncol)
            dat = self.data.copy()
            dat.resize(nrow, ncol)
        else:
            dat = self.data
        if writechannel:
            if ncol == 1:
                channels = arange(1, dat.size + 1)
                channels.resize(dat.size, 1)
                dat.resize(dat.size, 1)
                print>> ASCIIfile, "Channel Counts"
                savetxt(ASCIIfile, concatenate((channels, dat), axis=1),
                        fmt='%i')
            else:
                raise NonImplementedError(
                    "channel numbers not yet supported for multicolumns")
        else:
            savetxt(ASCIIfile, dat, fmt='%9i')
        ASCIIfile.close()

    def toLT(self, ASCIIfile, description="LT_description",
             nsperchannel="LT_nsperchannel", key="LT_key", fwhm="LT_fwhm",
             ncol=1, onError='w'):
        hdr = "%s\n%s\n%s\n%s\n" % (description, nsperchannel, key, fwhm)
        self.toASCII(ASCIIfile, ncol=ncol, hdr=hdr, onError=onError)

        #
        # if __name__ == '__main__':
        # 	filename ='C:\\Documents and Settings\\pas064\\My Documents\\PaLS\\phytantriol\\phyt-t20/28_080.CHN'
        # 	spectrum=CHN(filename)
        # 	print spectrum.hdr
        # 	print spectrum.data
        # # 	import pylab
        # # 	pylab.plot(spectrum.data)
        # # 	pylab.show()
        # 	spectrum.toLT('kk.txt',ncol=7, onError='w')
        # 	raw_input()
        # 	f=open('kk.txt')
        # 	a=f.read()
        # 	print a
        # 	f.close()
