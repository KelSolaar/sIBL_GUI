#/usr/bin/bash
echo -------------------------------------------------------------------------------
echo sIBL_GUI - Documentation Build
echo -------------------------------------------------------------------------------

export PROJECT=$( dirname "${BASH_SOURCE[0]}" )/..

export UTILITIES=$PROJECT/utilities
export DOCUMENTATION=$PROJECT/docs/documentation
export HELP=$PROJECT/docs/help
export SPHINX=$PROJECT/docs/sphinx

#! Inline documentation build.
echo -------------------------------------------------------------------------------
echo Inline Documentation Build - Begin
echo -------------------------------------------------------------------------------
python $UTILITIES/reStructuredTextToHtml.py "$HELP/sIBL_GUI_Manual.rst" "$HELP/sIBL_GUI_Manual.html"
echo -------------------------------------------------------------------------------
echo Inline Documentation Build - End
echo -------------------------------------------------------------------------------

#! HDRLabs documentation build.
echo -------------------------------------------------------------------------------
echo HDRLabs Documentation Build - Begin
echo -------------------------------------------------------------------------------
python $UTILITIES/getHDRLabsDocumentation.py "$HELP/sIBL_GUI_Manual.html" "$HELP/sIBL_GUI_Manual_Body.html"
echo -------------------------------------------------------------------------------
echo HDRLabs Documentation Build - End
echo -------------------------------------------------------------------------------

#! Sphinx documentation build.
echo -------------------------------------------------------------------------------
echo Sphinx Documentation Build - Begin
echo -------------------------------------------------------------------------------
python $UTILITIES/sliceDocumentation.py "$HELP/sIBL_GUI_Manual.rst" "$SPHINX/source/resources/pages"
python $UTILITIES/sliceDocumentation.py "$PROJECT/CHANGES.rst" "$SPHINX/source/resources/pages"
python $UTILITIES/getSphinxDocumentationTocTree.py "sIBL_GUI" "$SPHINX/source/resources/pages/tocTree.rst" "$SPHINX/source/index.rst" "$SPHINX/source/resources/pages"
rm -rf $SPHINX/build
rm -rf $SPHINX/source/resources/packages
rm $SPHINX/source/resources/pages/api/*
rm "$SPHINX/source/resources/pages/tocTree.rst"
python $UTILITIES/getSphinxDocumentationApi.py "foundations,manager,umbra,sibl_gui" "$SPHINX/source/resources/packages" "$SPHINX/source/resources/pages/api" "$SPHINX/source/resources/pages/api.rst"
export PYTHONPATH=$SPHINX/source/resources/packages
sphinx-build -b html -d $SPHINX/build/doctrees $SPHINX/source $SPHINX/build/html
echo -------------------------------------------------------------------------------
echo Sphinx Documentation Build - End
echo -------------------------------------------------------------------------------
