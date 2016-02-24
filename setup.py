from setuptools import setup, find_packages


entry_points={
    'console_scripts': [
        'pascual_batch = PAScual.PAScual:start',
    ],
    'gui_scripts': [
        'pascual = PAScual.PAScualGUI:main',
        'pascual_TEcalc = PAScual.TEcalcGUI:main',
    ]
}

setup(
    name='PAScual',
    version='1.6',
    url='https://sourceforge.net/p/pascual/w/Main_Page/',
    license='GPLv3',
    author='Carlos Pascual-Izarra',
    author_email='cpascual@users.sourceforge.net',
    description='Positron Annihilation Spectroscopy data analysis',
    keywords = "science PALS PAS positron annihilation fit",

    packages=find_packages(),
    entry_points=entry_points,
    install_requires=['numpy'],)

