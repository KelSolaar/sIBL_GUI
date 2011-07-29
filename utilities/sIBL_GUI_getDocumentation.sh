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

#! Inline documentation build.
echo ----------------------------------------------------------------
echo Inline Documentation Build - Begin
echo ----------------------------------------------------------------
python $UTILITIES/sIBL_GUI_reStructuredTextToHtml.py "$HELP/sIBL_GUI Manual" "$HELP/sIBL_GUI Manual.html"
echo ----------------------------------------------------------------
echo Inline Documentation Build - End
echo ----------------------------------------------------------------

#! HDRLabs documentation build.
echo ----------------------------------------------------------------
echo HDRLabs Documentation Build - Begin
echo ----------------------------------------------------------------
python $UTILITIES/sIBL_GUI_getHDRLabsDocumentation.py "$HELP/sIBL_GUI Manual.html" "$HELP/sIBL_GUI_Manual_Body.html"
echo ----------------------------------------------------------------
echo HDRLabs Documentation Build - End
echo ----------------------------------------------------------------

#! Sphinx documentation build.
echo ----------------------------------------------------------------
echo Sphinx Documentation Build - Begin
echo ----------------------------------------------------------------
python $UTILITIES/sIBL_GUI_sliceDocumentation.py "$HELP/sIBL_GUI Manual" "$SPHINX/source/resources/pages"
python $UTILITIES/sIBL_GUI_getSphinxDocumentationTocTree.py "$SPHINX/source/resources/pages/tocTree.rst" "$SPHINX/source/index.rst" "$SPHINX/source/resources/pages"
rm -rf $SPHINX/build
rm -rf /source/resources/src
rm $SPHINX/source/resources/pages/api/*
rm "$SPHINX/source/resources/pages/tocTree.rst"
python $UTILITIES/sIBL_GUI_getSphinxDocumentationApi.py  "$APPLICATION/src"  "$SPHINX/source/resources/src" "$SPHINX/source/resources/pages/api" "$SPHINX/source/resources/pages/api.rst"
export PYTHONPATH=$SPHINX/source/resources/src
sphinx-build -b html -d $SPHINX/build/doctrees   $SPHINX/source $SPHINX/build/html
echo ----------------------------------------------------------------
echo Sphinx Documentation Build - End
echo ----------------------------------------------------------------
