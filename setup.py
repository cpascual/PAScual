import os
from setuptools import setup, find_packages


def get_release_info():
    from importlib.util import spec_from_file_location, module_from_spec
    from pathlib import Path

    path = Path(__file__).parent / "PAScual" / "release.py"
    spec = spec_from_file_location("release", path.as_posix())
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


release = get_release_info()


# entry points to create scripts
entry_points = {
    "console_scripts": [
        "pascual_batch = PAScual.PAScual:start",
        "pascual = PAScual.PAScualGUI:main",
        "pascual_TEcalc = PAScual.TEcalcGUI:main",
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
    "Programming Language :: Python :: 3 :: Only",
    "Topic :: Scientific/Engineering",
]

# call setup()
setup(
    name="PAScual",
    version=release.__version__,
    url=release.__homepage__,
    license="GPLv3",
    author="Carlos Pascual-Izarra",
    author_email="cpascual@users.sourceforge.net",
    description="Positron Annihilation Spectroscopy data analysis",
    long_description=open(os.path.join(os.path.dirname(__file__), "README.md")).read(),
    long_description_content_type="text/markdown",
    keywords="science PALS PAS positron annihilation fit",
    packages=find_packages(),
    include_package_data=True,
    entry_points=entry_points,
    install_requires=["numpy", "scipy", "PythonQwt", "pyqt5"],
    classifiers=classifiers,
)
