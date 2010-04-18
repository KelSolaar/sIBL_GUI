#/usr/bin/bash

echo ----------------------------------------------------------------
echo sIBL_GUI - Mac Os X - Build
echo ----------------------------------------------------------------

alias python=/Library/Frameworks/Python.framework/Versions/2.6/bin/python
#! sIBL_GUI Build.
rm -rf build dist
python ../../utilities/sIBL_GUI_darwinSetup.py py2app --includes "foundations.strings,foundations.pkzip,ui.widgets.variable_QPushButton,sip,PyQt4.QtNetwork,PyQt4.QtWebKit,sqlalchemy,sqlalchemy.orm,sqlalchemy.ext,sqlalchemy.ext.declarative,sqlalchemy.databases" --no-strip
rm -rf `find ./dist/sIBL_GUI.app/ -name *debug*`
mkdir ./dist/sIBL_GUI.app/Contents/Resources/ui
cp  ../../src/ui/sIBL_GUI.ui ./dist/sIBL_GUI.app/Contents/Resources/ui
cp  ../../src/ui/sIBL_GUI_Layouts.rc ./dist/sIBL_GUI.app/Contents/Resources/ui
mkdir ./dist/sIBL_GUI.app/Contents/Resources/resources
cp  ../../src/resources/sIBL_GUI_SpashScreen.png ./dist/sIBL_GUI.app/Contents/Resources/resources
cp  ../../src/resources/sIBL_GUI_Logo.png ./dist/sIBL_GUI.app/Contents/Resources/resources
cp  ../../src/resources/sIBL_GUI_Layout.png ./dist/sIBL_GUI.app/Contents/Resources/resources
cp  ../../src/resources/sIBL_GUI_Misc.png ./dist/sIBL_GUI.app/Contents/Resources/resources
cp  ../../src/resources/sIBL_GUI_CentralWidget.png ./dist/sIBL_GUI.app/Contents/Resources/resources
cp -rf ../../src/templates ./dist/sIBL_GUI.app/Contents/Resources/
cp -rf ../../src/components ./dist/sIBL_GUI.app/Contents/Resources/
cp -f ./support/__boot__.py ./dist/sIBL_GUI.app/Contents/Resources/
cp -f ./support/qt.conf ./dist/sIBL_GUI.app/Contents/Resources/
cp -rf ./support/imageformats ./dist/sIBL_GUI.app/Contents/MacOs