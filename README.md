PAScual: a Positron Annihilation Spectroscopy data analysis program.
====================================================================

(c) 2007-2019 Carlos Pascual-Izarra

email: < cpascual [AT] users.sourceforge.net >

Home page: https://github.com/cpascual/PAScual


Installation instructions for PAScual
=====================================


Prerequisites
-------------

For running PAScual you need, at least:

- Python >=2.7
- Numpy >=1.0.3
- scipy >=0.5.2
- PyQt >=4.6
- PythonQwt >=0.5.5 

For getting graphical output in the text mode interface, you may want

- matplotlib >= 0.90.1

Except for PythonQwt, the rest of the packages should be available in the
official repositories of any linux distribution that supports Python2.7.

For PythonQwt, you may need to use [PyPI](pypi.python.org)

### TIP: using conda to install the pre-requisites

You can create a [conda](https://docs.conda.io/en/latest/miniconda.html) environment with the required prerequisites with:

`conda create -c conda-forge -n PAScual python=2 pythonqwt pyqt numpy scipy`



Installing PAScual
------------------

The simplest way is to use:

```
pip install PAScual
```

Alternatively, you can also download the tar.gz from PyPI, untar it into a
temporary directory, change to it and run:

```
python setup.py install
```

Running PAScual
---------------

Once installed, just run the following command to get the graphical application:

```
pascual
```

And I recommend to try the tutorial from the User Manual (some example spectra
are provided in the examples dir)


Important:
==========

**PLEASE give credit:**

If you use PAScual, acknowledge it by citing, at least:

C. Pascual-Izarra et al.,
Advanced Fitting Algorithms for Analysing Positron Annihilation Lifetime Spectra,
Nuclear Instruments and Methods A, 603, p456-466 (2009)
(DOI: 10.1016/j.nima.2009.01.205)

See CREDITS.txt for acknowledgements to third parties.

Also note its license:  PAScual is Free Software but certain conditions apply
(see LICENSE.TXT).
If you want to request modifications of PAScual, please contact the author.
If you modify PAScual, please communicate the modifications to the author so
that they can be incorporated in future versions.


