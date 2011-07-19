#/usr/bin/bash
echo ----------------------------------------------------------------
echo sIBL_GUI - Documentation Build
echo ----------------------------------------------------------------

alias python=/Library/Frameworks/Python.framework/Versions/2.7/bin/python
alias sphinx-build=/Library/Frameworks/Python.framework/Versions/2.7/bin/sphinx-build
export APPLICATION=/Users/KelSolaar/Documents/Developement/sIBL_GUI

export UTILITIES=$APPLICATION/utilities
export DOCUMENTATION=$APPLICATION/support/documentation
export HELP=$APPLICATION/support/documentation/help
export SPHINX=$APPLICATION/support/documentation/sphinx

#! Inline Documentation Build.
echo ----------------------------------------------------------------
echo Inline Documentation Build - Begin
echo ----------------------------------------------------------------
python $UTILITIES/sIBL_GUI_reStructuredTextToHtml.py "$HELP/sIBL_GUI Manual" "$HELP/sIBL_GUI Manual.html"
echo ----------------------------------------------------------------
echo Inline Documentation Build - End
echo ----------------------------------------------------------------

#! HDRLabs Documentation Build.
echo ----------------------------------------------------------------
echo HDRLabs Documentation Build - Begin
echo ----------------------------------------------------------------
python $UTILITIES/sIBL_GUI_getHDRLabsDocumentation.py "$HELP/sIBL_GUI Manual.html" "$HELP/sIBL_GUI_Manual_Body.html"
echo ----------------------------------------------------------------
echo HDRLabs Documentation Build - End
echo ----------------------------------------------------------------

#! Sphinx Documentation Build.
echo ----------------------------------------------------------------
echo Sphinx Documentation Build - Begin
echo ----------------------------------------------------------------
python $UTILITIES/sIBL_GUI_sliceDocumentation.py "$HELP/sIBL_GUI Manual" "$SPHINX/source/resources/pages"
python $UTILITIES/sIBL_GUI_getSphinxDocumentationIndexFile.py "$SPHINX/source/resources/pages/tocTree.rst" "$SPHINX/source/index.rst" "$SPHINX/source/resources/pages"
sphinx-build -b html -d $SPHINX/build/doctrees   $SPHINX/source $SPHINX/build/html
echo ----------------------------------------------------------------
echo Sphinx Documentation Build - End
echo ----------------------------------------------------------------
