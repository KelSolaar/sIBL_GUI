#/bin/bash
echo ----------------------------------------------------------------
echo sIBL_GUI - Build Templates Documentation
echo ----------------------------------------------------------------

alias python=/Library/Frameworks/Python.framework/Versions/2.6/bin/python

#! XSI_MR_Standard Template Documentation Building.
python sIBL_GUI_textileToHtml.py "/Users/KelSolaar/Documents/Developement/sIBL_GUI/src/templates/XSI/XSI_MR_Standard/help/XSI_MR_Standard Template Manual" "/Users/KelSolaar/Documents/Developement/sIBL_GUI/src/templates/XSI/XSI_MR_Standard/help/XSI_MR_Standard Template Manual.html"  "XSI MR Standard - Template - Manual - Help File"

#! Softimage_MR_Standard Template Documentation Building.
python sIBL_GUI_textileToHtml.py "/Users/KelSolaar/Documents/Developement/sIBL_GUI/src/templates/Softimage/Softimage_MR_Standard/help/Softimage_MR_Standard Template Manual" "/Users/KelSolaar/Documents/Developement/sIBL_GUI/src/templates/Softimage/Softimage_MR_Standard/help/Softimage_MR_Standard Template Manual.html"  "Softimage MR Standard - Template - Manual - Help File"

#! Maya_MR_Standard Template Documentation Building.
python sIBL_GUI_textileToHtml.py "/Users/KelSolaar/Documents/Developement/sIBL_GUI/src/templates/Maya/Maya_MR_Standard/help/Maya_MR_Standard Template Manual" "/Users/KelSolaar/Documents/Developement/sIBL_GUI/src/templates/Maya/Maya_MR_Standard/help/Maya_MR_Standard Template Manual.html"  "Maya MR Standard - Template - Manual - Help File"

#! Maya_RfM_Standard Template Documentation Building.
python sIBL_GUI_textileToHtml.py "/Users/KelSolaar/Documents/Developement/sIBL_GUI/src/templates/Maya/Maya_RfM_Standard/help/Maya_RfM_Standard Template Manual" "/Users/KelSolaar/Documents/Developement/sIBL_GUI/src/templates/Maya/Maya_RfM_Standard/help/Maya_RfM_Standard Template Manual.html"  "Maya RfM Standard - Template - Manual - Help File"

#! Maya_Turtle_Standard Template Documentation Building.
python sIBL_GUI_textileToHtml.py "/Users/KelSolaar/Documents/Developement/sIBL_GUI/src/templates/Maya/Maya_Turtle_Standard/help/Maya_Turtle_Standard Template Manual" "/Users/KelSolaar/Documents/Developement/sIBL_GUI/src/templates/Maya/Maya_Turtle_Standard/help/Maya_Turtle_Standard Template Manual.html"  "Maya Turtle Standard - Template - Manual - Help File"