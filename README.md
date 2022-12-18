# PAScual: a Positron Annihilation Spectroscopy data analysis program.

(c) 2007-2022 Carlos Pascual-Izarra

email: < cpascual [AT] users.sourceforge.net >

Home page: https://github.com/cpascual/PAScual


## Installation instructions for PAScual


The **recommended way** of installing PAScual is by using a virtual environment where all needed dependencies are installed using [mamba](https://mamba.readthedocs.io). For this, first [install mamba](https://mamba.readthedocs.io/en/latest/installation.html) and then, on a terminal, run: 

```
mamba create -c conda-forge -n PAScual python=2 pythonqwt pyqt numpy scipy

mamba activate PAScual
```

> **Note**: Using other conda implementations such as [Anaconda](https://www.anaconda.com) should also work, but I found mamba **a lot** faster. Replace `mamba` by `conda` if you are using Anaconda or miniconda instead of mamba.


Once the requirements are installed, **and in the same terminal (or a terminal where you alsready activated thePAScual environment), you can install PAScual with:

```
pip install PAScual
```

### Alternative: manual installation of PAScual


> **Note**: I strongly recommended installing using a mamba (or conda) environment (as described above), specially for Windows users.

If for some reason you cannot install with the recommended way, here are generic instructions to install it (but note that you may run into more trouble to get the proper versions of all the requirements).

For running PAScual, at least the following packages **and all their dependencies** should
be installed:

- Python >=2.7
- Numpy >=1.0.3
- scipy >=0.5.2
- PyQt >=5
- PythonQwt >=0.5.5 

For getting graphical output in the text mode interface, you may want

- matplotlib >= 0.90.1

Except for PythonQwt, the rest of the packages should be available in the
official repositories of any linux distribution that supports Python2.7.

For PythonQwt, you may need to use [PyPI](pypi.python.org)

Once the requirements are properly installed, you can install PAScual with:

```
pip install PAScual
```


## Running PAScual


> *Note**: if you installed PAScual in a virtual environment (as recommended), make sure to activate the environment before continuing (i.e., in your current terminal, run `mamba activate PAScual` or equivalent)


Once installed, just run the following command to get the graphical application:

```
pascual
```

And I recommend to try the tutorial from the User Manual (some example spectra
are provided in the examples dir)


# Important:

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


