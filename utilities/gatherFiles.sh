#/bin/bash
echo ----------------------------------------------------------------
echo sIBL_GUI - Files Gathering
echo ----------------------------------------------------------------

#! Gathering folder cleanup.
rm -rf ./releases/repository/*
mkdir ./releases/repository/sIBL_GUI

#! Windows gathering.
cp ./utilities/nsis/sIBL_GUI_Setup.exe ./releases/repository/sIBL_GUI/sIBL_GUI.exe

#! Mac Os X gathering.
cp ./releases/Darwin/sIBL_GUI.dmg ./releases/repository/sIBL_GUI/sIBL_GUI.dmg

#! sIBL_GUI Change Log gathering.
cp -rf ./releases/Change_Log.html ./releases/repository/sIBL_GUI/

#! sIBL_GUI Releases file.
cp -rf ./releases/sIBL_GUI_Releases.rc ./releases/repository/sIBL_GUI/

#! sIBL_GUI Manual / Help file.
cp -rf ./support/documentation/help ./releases/repository/sIBL_GUI/Help
rm ./releases/repository/sIBL_GUI/help/sIBL_GUI_Manual.rst

#! sIBL_GUI Api file.
cp -rf ./support/documentation/sphinx/build/html ./releases/repository/sIBL_GUI/Api
