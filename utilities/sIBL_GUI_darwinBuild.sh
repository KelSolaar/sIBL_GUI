#/usr/bin/bash
echo ----------------------------------------------------------------
echo sIBL_GUI - Mac Os X - Overall Build
echo ----------------------------------------------------------------

export SOURCE=../../src
export DISTRIBUTION=./dist
export BUILD=./build
export UTILITIES=../../utilities

alias python=/Library/Frameworks/Python.framework/Versions/2.7/bin/python

#! Darwin Build.
echo ----------------------------------------------------------------
echo Build - Begin
echo ----------------------------------------------------------------
rm -rf $BUILD $DISTRIBUTION
python $UTILITIES/sIBL_GUI_darwinSetup.py py2app --includes "foundations.pkzip,foundations.strings,libraries.freeImage.freeImage,ui.widgets.search_QLineEdit,ui.widgets.variable_QPushButton,PyQt4.QtNetwork,PyQt4.QtWebKit,sip,sqlalchemy,sqlalchemy.databases,sqlalchemy.ext.declarative,sqlalchemy.ext,sqlalchemy.orm" --no-strip
rm -rf `find $DISTRIBUTION/sIBL_GUI.app/ -name *debug*`
echo ----------------------------------------------------------------
echo Build - End
echo ----------------------------------------------------------------

#! Darwin Release.
echo ----------------------------------------------------------------
echo Release - Begin
echo ----------------------------------------------------------------
mkdir -p $DISTRIBUTION/sIBL_GUI.app/Contents/Resources/ui
cp  $SOURCE/ui/sIBL_GUI.ui $DISTRIBUTION/sIBL_GUI.app/Contents/Resources/ui
cp  $SOURCE/ui/sIBL_GUI_Layouts.rc $DISTRIBUTION/sIBL_GUI.app/Contents/Resources/ui
cp  $SOURCE/ui/Windows_styleSheet.qss $DISTRIBUTION/sIBL_GUI.app/Contents/Resources/ui
cp  $SOURCE/ui/Darwin_styleSheet.qss $DISTRIBUTION/sIBL_GUI.app/Contents/Resources/ui
cp  $SOURCE/ui/Linux_styleSheet.qss $DISTRIBUTION/sIBL_GUI.app/Contents/Resources/ui
cp  $SOURCE/resources/Icon_Light_512.icns $DISTRIBUTION/sIBL_GUI.app/Contents/Resources/
mkdir -p $DISTRIBUTION/sIBL_GUI.app/Contents/Resources/resources
cp  $SOURCE/resources/Icon_Light.icns $DISTRIBUTION/sIBL_GUI.app/Contents/Resources/resources
cp  $SOURCE/resources/sIBL_GUI_SpashScreen.png $DISTRIBUTION/sIBL_GUI.app/Contents/Resources/resources
cp  $SOURCE/resources/sIBL_GUI_Logo.png $DISTRIBUTION/sIBL_GUI.app/Contents/Resources/resources
cp  $SOURCE/resources/Central_Widget.png $DISTRIBUTION/sIBL_GUI.app/Contents/Resources/resources
cp  $SOURCE/resources/Central_Widget_Hover.png $DISTRIBUTION/sIBL_GUI.app/Contents/Resources/resources
cp  $SOURCE/resources/Central_Widget_Active.png $DISTRIBUTION/sIBL_GUI.app/Contents/Resources/resources
cp  $SOURCE/resources/Layout.png $DISTRIBUTION/sIBL_GUI.app/Contents/Resources/resources
cp  $SOURCE/resources/Layout_Hover.png $DISTRIBUTION/sIBL_GUI.app/Contents/Resources/resources
cp  $SOURCE/resources/Layout_Active.png $DISTRIBUTION/sIBL_GUI.app/Contents/Resources/resources
cp  $SOURCE/resources/Miscellaneous.png $DISTRIBUTION/sIBL_GUI.app/Contents/Resources/resources
cp  $SOURCE/resources/Miscellaneous_Hover.png $DISTRIBUTION/sIBL_GUI.app/Contents/Resources/resources
cp  $SOURCE/resources/Miscellaneous_Active.png $DISTRIBUTION/sIBL_GUI.app/Contents/Resources/resources
cp  $SOURCE/resources/Library.png $DISTRIBUTION/sIBL_GUI.app/Contents/Resources/resources
cp  $SOURCE/resources/Library_Hover.png $DISTRIBUTION/sIBL_GUI.app/Contents/Resources/resources
cp  $SOURCE/resources/Library_Active.png $DISTRIBUTION/sIBL_GUI.app/Contents/Resources/resources
cp  $SOURCE/resources/Export.png $DISTRIBUTION/sIBL_GUI.app/Contents/Resources/resources
cp  $SOURCE/resources/Export_Hover.png $DISTRIBUTION/sIBL_GUI.app/Contents/Resources/resources
cp  $SOURCE/resources/Export_Active.png $DISTRIBUTION/sIBL_GUI.app/Contents/Resources/resources
cp  $SOURCE/resources/Preferences.png $DISTRIBUTION/sIBL_GUI.app/Contents/Resources/resources
cp  $SOURCE/resources/Preferences_Hover.png $DISTRIBUTION/sIBL_GUI.app/Contents/Resources/resources
cp  $SOURCE/resources/Preferences_Active.png $DISTRIBUTION/sIBL_GUI.app/Contents/Resources/resources
cp  $SOURCE/resources/Toolbar.png $DISTRIBUTION/sIBL_GUI.app/Contents/Resources/resources
mkdir -p $DISTRIBUTION/sIBL_GUI.app/Contents/Resources/templates
cp -r $SOURCE/templates/Maya/* $DISTRIBUTION/sIBL_GUI.app/Contents/Resources/templates/
cp -r $SOURCE/components $DISTRIBUTION/sIBL_GUI.app/Contents/Resources/
mkdir -p $DISTRIBUTION/sIBL_GUI.app/Contents/Resources/libraries/freeImage/resources
cp -r $SOURCE/libraries/freeImage/resources/libfreeimage.dylib $DISTRIBUTION/sIBL_GUI.app/Contents/Resources/libraries/freeImage/resources/
cp -f ./support/__boot__.py $DISTRIBUTION/sIBL_GUI.app/Contents/Resources/
cp -f ./support/qt.conf $DISTRIBUTION/sIBL_GUI.app/Contents/Resources/
cp -r ./support/imageformats $DISTRIBUTION/sIBL_GUI.app/Contents/MacOs
echo ----------------------------------------------------------------
echo Release - End
echo ----------------------------------------------------------------

echo ----------------------------------------------------------------
echo Templates Textile Files Cleanup - Begin
echo ----------------------------------------------------------------
#! Maya_Arnold_Standard Textile Template Documentation Removal.
rm "$DISTRIBUTION/sIBL_GUI.app/Contents/Resources/templates/Maya_Arnold_Standard/help/Maya_Arnold_Standard Template Manual"

#! Maya_MR_Lightsmith Textile Template Documentation Removal.
rm "$DISTRIBUTION/sIBL_GUI.app/Contents/Resources/templates/Maya_MR_Lightsmith/help/Maya_MR_Lightsmith Template Manual"

#! Maya_MR_Standard Textile Template Documentation Removal.
rm "$DISTRIBUTION/sIBL_GUI.app/Contents/Resources/templates/Maya_MR_Standard/help/Maya_MR_Standard Template Manual"

#! Maya_RfM_Standard Textile Template Documentation Removal.
rm "$DISTRIBUTION/sIBL_GUI.app/Contents/Resources/templates/Maya_RfM_Standard/help/Maya_RfM_Standard Template Manual"

#! Maya_VRay_Dome_Light Textile Template Documentation Removal.
rm "$DISTRIBUTION/sIBL_GUI.app/Contents/Resources/templates/Maya_VRay_Dome_Light/help/Maya_VRay_Dome_Light Template Manual"

#! Maya_VRay_Lightsmith Textile Template Documentation Removal.
rm "$DISTRIBUTION/sIBL_GUI.app/Contents/Resources/templates/Maya_VRay_Lightsmith/help/Maya_VRay_Lightsmith Template Manual"

#! Maya_VRay_Standard Textile Template Documentation Removal.
rm "$DISTRIBUTION/sIBL_GUI.app/Contents/Resources/templates/Maya_VRay_Standard/help/Maya_VRay_Standard Template Manual"
echo ----------------------------------------------------------------
echo Templates Textile Files Cleanup - End
echo ----------------------------------------------------------------

#! sIBL_GUI Cleanup.
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
rm -f ./sIBL_GUI.dmg
#! hdiutil create ./sIBL_GUI.dmg -volname "sIBL_GUI" -fs HFS+ -srcfolder "$DISTRIBUTION/sIBL_GUI.app"
dropdmg -g sIBL_GUI -y sIBL_GUI $DISTRIBUTION/sIBL_GUI.app
echo ----------------------------------------------------------------
echo Dmg Compilation - End
echo ----------------------------------------------------------------