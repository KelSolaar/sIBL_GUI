#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**testsruntime_globals.py**

**Platform:**
    Windows, Linux, Mac Os X.

**Description:**
    Defines units tests for :mod:`sibl_gui.globals.runtime_globals` module.

**Others:**

"""

from __future__ import unicode_literals

import sys

if sys.version_info[:2] <= (2, 6):
    import unittest2 as unittest
else:
    import unittest

from sibl_gui.globals.runtime_globals import RuntimeGlobals

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["TestRuntimeGlobals"]


class TestRuntimeGlobals(unittest.TestCase):
    """
    Defines :class:`sibl_gui.globals.runtime_globals.RuntimeGlobals` class units tests methods.
    """

    def test_required_attributes(self):
        """
        Tests presence of required attributes.
        """

        required_attributes = ("templates_factory_directory",
                               "templates_user_directory",
                               "thumbnails_cache_directory",
                               "images_caches")

        for attribute in required_attributes:
            self.assertIn(attribute, RuntimeGlobals.__dict__)


if __name__ == "__main__":
    unittest.main()
