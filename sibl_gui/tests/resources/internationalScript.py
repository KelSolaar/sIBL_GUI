"""
Welcome to sIBL_GUI International Script file!

The purpose of this file is to test sIBL_GUI in an international context.
"""

from __future__ import unicode_literals

import os
import sibl_gui

collectionsOutliner = componentsManager["core.collectionsOutliner"]
collectionsOutliner.addCollection(collectionsOutliner.defaultCollection, "Default Collection")
collectionsOutliner.addCollection("0级")
iblSetsOutliner = componentsManager["core.iblSetsOutliner"]
iblSetsOutliner.addIblSet("标准", os.path.join(sibl_gui.__path__[0], "tests/resources/标准/标准.ibl"),
						collectionsOutliner.getCollectionByName("0级").id)

