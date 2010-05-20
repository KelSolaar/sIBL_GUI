#/usr/bin/bash

echo ----------------------------------------------------------------
echo sIBL_GUI - Mac Os X - Overall Build
echo ----------------------------------------------------------------

alias python=/Library/Frameworks/Python.framework/Versions/2.6/bin/python

#! Darwin Build.
echo ----------------------------------------------------------------
echo Build - Begin
echo ----------------------------------------------------------------
rm -rf build dist
python ../../utilities/sIBL_GUI_darwinSetup.py py2app --includes "foundations.strings,foundations.pkzip,ui.widgets.variable_QPushButton,sip,PyQt4.QtNetwork,PyQt4.QtWebKit,sqlalchemy,sqlalchemy.orm,sqlalchemy.ext,sqlalchemy.ext.declarative,sqlalchemy.databases" --no-strip
rm -rf `find ./dist/sIBL_GUI.app/ -name *debug*`
echo ----------------------------------------------------------------
echo Build - End
echo ----------------------------------------------------------------

#! Darwin Release.
echo ----------------------------------------------------------------
echo Release - Begin
echo ----------------------------------------------------------------
mkdir ./dist/sIBL_GUI.app/Contents/Resources/ui
cp  ../../src/ui/sIBL_GUI.ui ./dist/sIBL_GUI.app/Contents/Resources/ui
cp  ../../src/ui/sIBL_GUI_Layouts.rc ./dist/sIBL_GUI.app/Contents/Resources/ui
cp  ../../src/ui/Windows_styleSheet.qss ./dist/sIBL_GUI.app/Contents/Resources/ui
cp  ../../src/ui/Darwin_styleSheet.qss ./dist/sIBL_GUI.app/Contents/Resources/ui
cp  ../../src/ui/Linux_styleSheet.qss ./dist/sIBL_GUI.app/Contents/Resources/ui
mkdir ./dist/sIBL_GUI.app/Contents/Resources/resources
cp  ../../src/resources/Icon_Light_512.icns ./dist/sIBL_GUI.app/Contents/Resources/resources
cp  ../../src/resources/sIBL_GUI_SpashScreen.png ./dist/sIBL_GUI.app/Contents/Resources/resources
cp  ../../src/resources/sIBL_GUI_Logo.png ./dist/sIBL_GUI.app/Contents/Resources/resources
cp  ../../src/resources/Central_Widget.png ./dist/sIBL_GUI.app/Contents/Resources/resources
cp  ../../src/resources/Central_Widget_Hover.png ./dist/sIBL_GUI.app/Contents/Resources/resources
cp  ../../src/resources/Central_Widget_Active.png ./dist/sIBL_GUI.app/Contents/Resources/resources
cp  ../../src/resources/Layout.png ./dist/sIBL_GUI.app/Contents/Resources/resources
cp  ../../src/resources/Layout_Hover.png ./dist/sIBL_GUI.app/Contents/Resources/resources
cp  ../../src/resources/Layout_Active.png ./dist/sIBL_GUI.app/Contents/Resources/resources
cp  ../../src/resources/Miscellaneous.png ./dist/sIBL_GUI.app/Contents/Resources/resources
cp  ../../src/resources/Miscellaneous_Hover.png ./dist/sIBL_GUI.app/Contents/Resources/resources
cp  ../../src/resources/Miscellaneous_Active.png ./dist/sIBL_GUI.app/Contents/Resources/resources
cp  ../../src/resources/Library.png ./dist/sIBL_GUI.app/Contents/Resources/resources
cp  ../../src/resources/Library_Hover.png ./dist/sIBL_GUI.app/Contents/Resources/resources
cp  ../../src/resources/Library_Active.png ./dist/sIBL_GUI.app/Contents/Resources/resources
cp  ../../src/resources/Export.png ./dist/sIBL_GUI.app/Contents/Resources/resources
cp  ../../src/resources/Export_Hover.png ./dist/sIBL_GUI.app/Contents/Resources/resources
cp  ../../src/resources/Export_Active.png ./dist/sIBL_GUI.app/Contents/Resources/resources
cp  ../../src/resources/Preferences.png ./dist/sIBL_GUI.app/Contents/Resources/resources
cp  ../../src/resources/Preferences_Hover.png ./dist/sIBL_GUI.app/Contents/Resources/resources
cp  ../../src/resources/Preferences_Active.png ./dist/sIBL_GUI.app/Contents/Resources/resources
cp  ../../src/resources/Toolbar.png ./dist/sIBL_GUI.app/Contents/Resources/resources
mkdir ./dist/sIBL_GUI.app/Contents/Resources/templates
cp -r ../../src/templates/Maya/* ./dist/sIBL_GUI.app/Contents/Resources/templates/
cp -r ../../src/components ./dist/sIBL_GUI.app/Contents/Resources/
cp -f ./support/__boot__.py ./dist/sIBL_GUI.app/Contents/Resources/
cp -f ./support/qt.conf ./dist/sIBL_GUI.app/Contents/Resources/
cp -r ./support/imageformats ./dist/sIBL_GUI.app/Contents/MacOs
echo ----------------------------------------------------------------
echo Release - End
echo ----------------------------------------------------------------

#! Maya_MR_Standard Textile Template Documentation Removal.
echo ----------------------------------------------------------------
echo Templates Textile Files Cleanup - Begin
echo ----------------------------------------------------------------
rm "./dist/sIBL_GUI.app/Contents/Resources/templates/Maya_MR_Standard/help/Maya_MR_Standard Template Manual"

#! Maya_RfM_Standard Textile Template Documentation Removal.
rm "./dist/sIBL_GUI.app/Contents/Resources/templates/Maya_RfM_Standard/help/Maya_RfM_Standard Template Manual"

#! Maya_Turtle_Standard Textile Template Documentation Removal.
rm "./dist/sIBL_GUI.app/Contents/Resources/templates/Maya_Turtle_Standard/help/Maya_Turtle_Standard Template Manual"

#! Maya_VRay_Dome_Light Textile Template Documentation Removal.
rm "./dist/sIBL_GUI.app/Contents/Resources/templates/Maya_VRay_Dome_Light/help/Maya_VRay_Dome_Light Template Manual"

#! Maya_VRay_Standard Textile Template Documentation Removal.
rm "./dist/sIBL_GUI.app/Contents/Resources/templates/Maya_VRay_Standard/help/Maya_VRay_Standard Template Manual"
echo ----------------------------------------------------------------
echo Templates Textile Files Cleanup - End
echo ----------------------------------------------------------------

#! sIBL_GUI Cleanup.
echo ----------------------------------------------------------------
echo Cleanup - Begin
echo ----------------------------------------------------------------
python ../../utilities/sIBL_GUI_recursiveRemove.py ./dist/sIBL_GUI.app/ .pyc
python ../../utilities/sIBL_GUI_recursiveRemove.py ./dist/sIBL_GUI.app/ .pyo
python ../../utilities/sIBL_GUI_recursiveRemove.py ./dist/sIBL_GUI.app/ .DS_Store
python ../../utilities/sIBL_GUI_recursiveRemove.py ./dist/sIBL_GUI.app/ Thumbs.db
echo ----------------------------------------------------------------
echo Cleanup - End
echo ----------------------------------------------------------------

#! sIBL_GUI DMG.
echo ----------------------------------------------------------------
echo Dmg Compilation - Begin
echo ----------------------------------------------------------------
rm -f ./sIBL_GUI.dmg
hdiutil create ./sIBL_GUI.dmg -volname "sIBL_GUI" -fs HFS+ -srcfolder "./dist/sIBL_GUI.app"
#! /usr/local/bin/./dmgcanvas ../../utilities/dmgCanvas/sIBL_GUI.dmgCanvas ./sIBL_GUI.dmg
echo ----------------------------------------------------------------
echo Dmg Compilation - End
echo ----------------------------------------------------------------