#/bin/bash
echo ----------------------------------------------------------------
echo sIBL_GUI - Files Gathering
echo ----------------------------------------------------------------

#! Gathering folder cleanup.
rm -rf ./releases/repository/*
mkdir ./releases/repository/sIBL_GUI
#! Windows Gathering.
cp ./utilities/nsis/sIBL_GUI_Setup.exe ./releases/repository/sIBL_GUI/sIBL_GUI.exe

#! Mac Os X gathering.
cp ./releases/Darwin/sIBL_GUI.dmg ./releases/repository/sIBL_GUI/sIBL_GUI.dmg

#! sIBL_GUI change log gathering.
cp -rf ./releases/Change\ Log.html ./releases/repository/sIBL_GUI/

#! sIBL_GUI releases file.
cp -rf ./releases/sIBL_GUI_Releases.rc ./releases/repository/sIBL_GUI/

#! sIBL_GUI manual / help file.
cp -rf ./support/documentation/help ./releases/repository/sIBL_GUI/
rm ./releases/repository/sIBL_GUI/help/sIBL_GUI\ Manual.rst