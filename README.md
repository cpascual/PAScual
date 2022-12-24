# PAScual: a Positron Annihilation Spectroscopy data analysis program.

(c) 2007-2022 Carlos Pascual-Izarra

email: < cpascual [AT] users.sourceforge.net >

Home page: https://github.com/cpascual/PAScual


## Installation instructions for PAScual

PAScual and all its dependencies can be installed simply by running the following in a  terminal of a system where [Python](https://www.python.org/) >=3.7 is installed:

```
pip install PAScual
```

However, **I strongly recommend installing it in some sort of virtual python environment**.

For example, you can use [venv](https://docs.python.org/3/library/venv.html), but my 
preferred choice is using [mamba](https://mamba.readthedocs.io). For this, first 
[install mamba](https://mamba.readthedocs.io/en/latest/installation.html) and then, 
on a terminal, run: 

```
mamba create -c conda-forge -n PAScual pythonqwt pyqt numpy scipy

mamba activate PAScual

pip install PAScual
```

> **Note**: Using other conda implementations such as [Anaconda](https://www.anaconda.com) is also possible, but I found mamba **a lot** faster. Replace `mamba` by `conda` if you are using Anaconda or miniconda instead of mamba.

> **Note** If you intend to use PAScual **in text mode**, you may want to also install `matplotlib` to produce plots.


## Running PAScual


> **Note**: if you installed PAScual in a virtual environment (as recommended), make sure to activate the environment before continuing (i.e., in your current terminal, run `mamba activate PAScual` or equivalent)


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


