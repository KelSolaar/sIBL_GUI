"""
Welcome to sIBL_GUI International Script file!

The purpose of this file is to test sIBL_GUI in an international context.
"""

from __future__ import unicode_literals

import os
import sibl_gui

collections_outliner = components_manager["core.collections_outliner"]
collections_outliner.add_collection(collections_outliner.default_collection, "Default Collection")
collections_outliner.add_collection("0级")
ibl_sets_outliner = components_manager["core.ibl_sets_outliner"]
ibl_sets_outliner.add_ibl_set("标准", os.path.join(sibl_gui.__path__[0], "tests/resources/标准/标准.ibl"),
						collections_outliner.get_collection_by_name("0级").id)

