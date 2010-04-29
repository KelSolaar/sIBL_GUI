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

#! Templates Gathering.
mkdir ./releases/repository/templates/
cd ./src/templates/3dsMax/
zip -r ../../../releases/repository/templates/3dsMax_MR_Standard.zip 3dsMax_MR_Standard
zip -r ../../../releases/repository/templates/3dsMax_Scanline_Standard.zip 3dsMax_Scanline_Standard
zip -r ../../../releases/repository/templates/3dsMax_VRay_Standard.zip 3dsMax_VRay_Standard
cd ../Softimage
zip -r ../../../releases/repository/templates/Softimage_Standard.zip Softimage_MR_Standard
cd ../Maya
zip -r ../../../releases/repository/templates/Maya_MR_Standard.zip Maya_MR_Standard
zip -r ../../../releases/repository/templates/Maya_RfM_Standard.zip Maya_RfM_Standard
zip -r ../../../releases/repository/templates/Maya_Turtle_Standard.zip Maya_Turtle_Standard
zip -r ../../../releases/repository/templates/Maya_VRay_Dome_Light.zip Maya_VRay_Dome_Light
zip -r ../../../releases/repository/templates/Maya_VRay_Standard.zip Maya_VRay_Standard
cd ../XSI
zip -r ../../../releases/repository/templates/XSI_MR_Standard.zip XSI_MR_Standard

#! Reaching Original Directory.
cd ../../../

#! sIBL_GUI Change Log Gathering.
mkdir ./releases/repository/sIBL_GUI\ Change\ Log
cp -rf ./releases/Change\ Log.html ./releases/repository/sIBL_GUI\ Change\ Log

#! sIBL_GUI Releases File.
cp -rf ./releases/sIBL_GUI_Releases.rc ./releases/repository/