#!/usr/bin/env python

"""Setup script for packaging signboard.

To build a package for distribution:
    python setup.py sdist
and upload it to the PyPI with:
    python setup.py upload

Install a link for development work:
    pip install -e .

The manifest.in file (if present) is used for data files.

"""

import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
try:
    with open(os.path.join(here, 'readme.md')) as f:
        README = f.read()
except IOError:
    README = ''


__author__ = "David Wheeler"
__author_email__ = "dwheeler1512@yahoo.com.au"
__license__ = "MIT"
__maintainer_email__ = "as above"
__url__ = "https://github.com/wheeled/signboard"
__version__ = "1.0.0"


setup(name="signboard",
    packages=find_packages(),
    # metadata
    version=__version__,
    description="signboard is a Python utility to rescale images to suit the Electroboard sign",
    long_description=README,
    author=__author__,
    author_email=__author_email__,
    url=__url__,
    license=__license__,
    python_requires=">=3.6, ",
    classifiers=[
                 'Development Status :: 3 - Alpha',
                 'Operating System :: MacOS :: MacOS X',
                 'License :: OSI Approved :: MIT License',
                 'Programming Language :: Python :: 3.6',
                 'Programming Language :: Python :: 3.7',
                 'Programming Language :: Python :: 3.8',
                 'Programming Language :: Python :: 3.9',
                 ],
    )
