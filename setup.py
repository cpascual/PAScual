import os
from setuptools import setup, find_packages

# Load the variables (__version__, __citation_html__, etc.)
# from PAScual/release.py without importing the module
releasefname = os.path.join(os.path.dirname(__file__), 'PAScual', 'release.py')
with open(releasefname) as f:
    exec(f.read())

# entry points to create scripts
entry_points={
    'console_scripts': [
        'pascual_batch = PAScual.PAScual:start',
        'pascual = PAScual.PAScualGUI:main',
        'pascual_TEcalc = PAScual.TEcalcGUI:main',
    ]
}

# classifiers
classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Environment :: X11 Applications :: Qt",
    "Environment :: Win32 (MS Windows)",
    "Intended Audience :: Science/Research",
    "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
    "Natural Language :: English",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 2 :: Only",
    "Topic :: Scientific/Engineering",
]

# call setup()
setup(
    name='PAScual',
    version=__version__,
    url='https://sourceforge.net/p/pascual/w/Main_Page/',
    license='GPLv3',
    author='Carlos Pascual-Izarra',
    author_email='cpascual@users.sourceforge.net',
    description='Positron Annihilation Spectroscopy data analysis',
    long_description=open(os.path.join(os.path.dirname(__file__),
                                       'README.md')).read(),
    keywords = "science PALS PAS positron annihilation fit",

    packages=find_packages(),
    entry_points=entry_points,
    install_requires=['numpy', 'scipy', 'PythonQwt'],
    classifiers=classifiers,

)

