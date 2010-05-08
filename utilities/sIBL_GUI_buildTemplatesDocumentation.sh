#/bin/bash
echo ----------------------------------------------------------------
echo sIBL_GUI - Build Templates Documentation
echo ----------------------------------------------------------------

alias python=/Library/Frameworks/Python.framework/Versions/2.6/bin/python

#! XSI_MR_Standard Template Documentation Building.
python sIBL_GUI_textileToHtml.py "/Users/KelSolaar/Documents/Developement/sIBL_GUI/src/templates/XSI/XSI_MR_Standard/help/XSI_MR_Standard Template Manual" "/Users/KelSolaar/Documents/Developement/sIBL_GUI/src/templates/XSI/XSI_MR_Standard/help/XSI_MR_Standard Template Manual.html"  "XSI MR Standard - Template - Manual - Help File"