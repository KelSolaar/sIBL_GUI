#/usr/bin/bash
echo ----------------------------------------------------------------
echo sIBL_GUI - Mac Os X - Overall Build
echo ----------------------------------------------------------------

alias python=/Library/Frameworks/Python.framework/Versions/2.7/bin/python
export APPLICATION=/Users/KelSolaar/Documents/Developement/sIBL_GUI

export SOURCE=$APPLICATION/src/
export RELEASES=$APPLICATION/releases/Darwin
export DISTRIBUTION=$RELEASES/dist
export BUILD=$RELEASES/build
export UTILITIES=$APPLICATION/utilities

#! Darwin build.
echo ----------------------------------------------------------------
echo Build - Begin
echo ----------------------------------------------------------------
rm -rf $BUILD $DISTRIBUTION
python $UTILITIES/sIBL_GUI_darwinSetup.py py2app --includes "code,foundations.pkzip,foundations.strings,foundations.rotatingBackup,migrate.exceptions,migrate.versioning.api,PyQt4.QtNetwork,PyQt4.QtWebKit,sibl_gui.components.core.db.utilities.common,sibl_gui.components.core.db.exceptions,sibl_gui.components.core.db.utilities.types,sibl_gui.exceptions,sibl_gui.libraries.freeImage.freeImage,sibl_gui.ui.common,umbra.exceptions,umbra.ui.completers,umbra.ui.highlighters,umbra.ui.widgets.codeEditor_QPlainTextEdit,umbra.ui.widgets.search_QLineEdit,umbra.ui.widgets.variable_QPushButton,sip,sqlalchemy,sqlalchemy.databases,sqlalchemy.ext.declarative,sqlalchemy.ext,sqlalchemy.orm" --no-strip
rm -rf `find $DISTRIBUTION/sIBL_GUI.app/ -name *debug*`
echo ----------------------------------------------------------------
echo Build - End
echo ----------------------------------------------------------------

#! Darwin release.
echo ----------------------------------------------------------------
echo Release - Begin
echo ----------------------------------------------------------------
cp $SOURCE/sibl_gui/resources/images/Icon_Light_512.icns $DISTRIBUTION/sIBL_GUI.app/Contents/Resources/
mkdir -p $DISTRIBUTION/sIBL_GUI.app/Contents/Resources/sibl_gui
cp -r $SOURCE/sibl_gui/resources $DISTRIBUTION/sIBL_GUI.app/Contents/Resources/sibl_gui/
cp -r $SOURCE/sibl_gui/components $DISTRIBUTION/sIBL_GUI.app/Contents/Resources/sibl_gui/
mkdir -p $DISTRIBUTION/sIBL_GUI.app/Contents/Resources/umbra
cp -r $SOURCE/umbra/resources $DISTRIBUTION/sIBL_GUI.app/Contents/Resources/umbra/
cp -r $SOURCE/umbra/components $DISTRIBUTION/sIBL_GUI.app/Contents/Resources/umbra/
mkdir -p $DISTRIBUTION/sIBL_GUI.app/Contents/Resources/sibl_gui/libraries/freeImage/resources
cp -f $SOURCE/sibl_gui/libraries/freeImage/resources/libfreeimage.dylib $DISTRIBUTION/sIBL_GUI.app/Contents/Resources/sibl_gui/libraries/freeImage/resources/
cp -f ./support/qt.conf $DISTRIBUTION/sIBL_GUI.app/Contents/Resources/
cp -r ./support/imageformats $DISTRIBUTION/sIBL_GUI.app/Contents/MacOs
echo ----------------------------------------------------------------
echo Release - End
echo ----------------------------------------------------------------

echo ----------------------------------------------------------------
echo Templates Textile Files Cleanup - Begin
echo ----------------------------------------------------------------
#! Maya_Arnold_Standard template documentation removal.
#! rm "$DISTRIBUTION/sIBL_GUI.app/Contents/Resources/templates/Maya_Arnold_Standard/help/Maya_Arnold_Standard Template Manual"

#! Maya_MR_Lightsmith template documentation removal.
#! rm "$DISTRIBUTION/sIBL_GUI.app/Contents/Resources/templates/Maya_MR_Lightsmith/help/Maya_MR_Lightsmith Template Manual"

#! Maya_MR_Standard template documentation removal.
#! rm "$DISTRIBUTION/sIBL_GUI.app/Contents/Resources/templates/Maya_MR_Standard/help/Maya_MR_Standard Template Manual"

#! Maya_RfM_Standard template documentation removal.
#! rm "$DISTRIBUTION/sIBL_GUI.app/Contents/Resources/templates/Maya_RfM_Standard/help/Maya_RfM_Standard Template Manual"

#! Maya_VRay_Dome_Light template documentation removal.
#! rm "$DISTRIBUTION/sIBL_GUI.app/Contents/Resources/templates/Maya_VRay_Dome_Light/help/Maya_VRay_Dome_Light Template Manual"

#! Maya_VRay_Lightsmith template documentation removal.
#! rm "$DISTRIBUTION/sIBL_GUI.app/Contents/Resources/templates/Maya_VRay_Lightsmith/help/Maya_VRay_Lightsmith Template Manual"

#! Maya_VRay_Standard template documentation removal.
#! rm "$DISTRIBUTION/sIBL_GUI.app/Contents/Resources/templates/Maya_VRay_Standard/help/Maya_VRay_Standard Template Manual"
echo ----------------------------------------------------------------
echo Templates Textile Files Cleanup - End
echo ----------------------------------------------------------------

#! sIBL_GUI cleanup.
echo ----------------------------------------------------------------
echo Cleanup - Begin
echo ----------------------------------------------------------------
python $UTILITIES/sIBL_GUI_recursiveRemove.py $DISTRIBUTION/sIBL_GUI.app/ .pyc
python $UTILITIES/sIBL_GUI_recursiveRemove.py $DISTRIBUTION/sIBL_GUI.app/ .pyo
python $UTILITIES/sIBL_GUI_recursiveRemove.py $DISTRIBUTION/sIBL_GUI.app/ .DS_Store
python $UTILITIES/sIBL_GUI_recursiveRemove.py $DISTRIBUTION/sIBL_GUI.app/ Thumbs.db
echo ----------------------------------------------------------------
echo Cleanup - End
echo ----------------------------------------------------------------

#! sIBL_GUI DMG.
echo ----------------------------------------------------------------
echo Dmg Compilation - Begin
echo ----------------------------------------------------------------
#! rm -f ./sIBL_GUI.dmg
#! hdiutil create ./sIBL_GUI.dmg -volname "sIBL_GUI" -fs HFS+ -srcfolder "$DISTRIBUTION/sIBL_GUI.app"
#! dropdmg -g sIBL_GUI -y sIBL_GUI $DISTRIBUTION/sIBL_GUI.app
echo ----------------------------------------------------------------
echo Dmg Compilation - End
echo ----------------------------------------------------------------