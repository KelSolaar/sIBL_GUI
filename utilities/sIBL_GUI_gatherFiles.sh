#/bin/bash
echo ----------------------------------------------------------------
echo sIBL_GUI - Files Gathering
echo ----------------------------------------------------------------

#! Gathering Folder Cleanup.
rm -rf ./releases/repository/*

#! Windows Gathering.
cp ./utilities/nsis/sIBL_GUI_Setup.exe ./releases/repository/sIBL_GUI.exe

#! MacOsX Gathering.
cp ./releases/Darwin/sIBL_GUI.dmg ./releases/repository/sIBL_GUI.dmg

#! sIBL_GUI Change Log Gathering.
mkdir ./releases/repository/sIBL_GUI\ Change\ Log
cp -rf ./releases/Change\ Log.html ./releases/repository/sIBL_GUI\ Change\ Log

#! sIBL_GUI Releases File.
cp -rf ./releases/sIBL_GUI_Releases.rc ./releases/repository/