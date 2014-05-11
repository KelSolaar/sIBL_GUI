#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**setup.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	`https://pypi.python.org/pypi/sIBL_GUI <https://pypi.python.org/pypi/sIBL_GUI>`_ package setup file.

**Others:**

"""

from __future__ import unicode_literals

import re
from setuptools import setup
from setuptools import find_packages

import sibl_gui.globals.constants

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["get_long_description"]


def get_long_description():
    """
    Returns the Package long description.

    :return: Package long description.
    :rtype: unicode
    """

    description = []
    with open("README.rst") as file:
        for line in file:
            if ".. code:: python" in line and len(description) >= 2:
                blockLine = description[-2]
                if re.search(r":$", blockLine) and not re.search(r"::$", blockLine):
                    description[-2] = "::".join(blockLine.rsplit(":", 1))
                continue

            description.append(line)
    return "".join(description)


setup(name=sibl_gui.globals.constants.Constants.application_name,
      version=sibl_gui.globals.constants.Constants.version,
      author=sibl_gui.globals.constants.__author__,
      author_email=sibl_gui.globals.constants.__email__,
      include_package_data=True,
      packages=find_packages(),
      scripts=["bin/sIBL_GUI"],
      url="https://github.com/KelSolaar/sIBL_GUI",
      license="GPLv3",
      description="sIBL_GUI is an open source lighting assistant making the Image Based Lighting process easier and straight forward through the use of \"Smart Ibl\" files.",
      long_description=get_long_description(),
      install_requires=["Alembic>=0.6.4", "Counter>=1.0.0", "SQLAlchemy==0.9.4", "Umbra>=1.0.9"],
      classifiers=["Development Status :: 5 - Production/Stable",
                   "Environment :: Console",
                   "Environment :: MacOS X",
                   "Environment :: Win32 (MS Windows)",
                   "Environment :: X11 Applications :: Qt",
                   "Intended Audience :: Developers",
                   "Intended Audience :: Other Audience",
                   "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
                   "Natural Language :: English",
                   "Operating System :: OS Independent",
                   "Programming Language :: Python :: 2.7",
                   "Topic :: Utilities"])
