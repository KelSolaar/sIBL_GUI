#/bin/bash
echo ----------------------------------------------------------------
echo sIBL_GUI - Files Gathering
echo ----------------------------------------------------------------

#! Gathering Folder Cleanup.
rm -rf ./releases/repository/*
mkdir ./releases/repository/sIBL_GUI
#! Windows Gathering.
cp ./utilities/nsis/sIBL_GUI_Setup.exe ./releases/repository/sIBL_GUI/sIBL_GUI.exe

#! MacOsX Gathering.
cp ./releases/Darwin/sIBL_GUI.dmg ./releases/repository/sIBL_GUI/sIBL_GUI.dmg

#! Templates Gathering.
mkdir ./releases/repository/sIBL_GUI/templates/
cd ./src/templates/3dsMax/
zip -r ../../../releases/repository/sIBL_GUI/templates/3dsMax_MR_Standard.zip 3dsMax_MR_Standard
zip -r ../../../releases/repository/sIBL_GUI/templates/3dsMax_Scanline_Standard.zip 3dsMax_Scanline_Standard
zip -r ../../../releases/repository/sIBL_GUI/templates/3dsMax_VRay_Standard.zip 3dsMax_VRay_Standard
cd ../Softimage
zip -r ../../../releases/repository/sIBL_GUI/templates/Softimage_Standard.zip Softimage_MR_Standard
cd ../Maya
zip -r ../../../releases/repository/sIBL_GUI/templates/Maya_MR_Standard.zip Maya_MR_Standard
zip -r ../../../releases/repository/sIBL_GUI/templates/Maya_RfM_Standard.zip Maya_RfM_Standard
zip -r ../../../releases/repository/sIBL_GUI/templates/Maya_Turtle_Standard.zip Maya_Turtle_Standard
zip -r ../../../releases/repository/sIBL_GUI/templates/Maya_VRay_Dome_Light.zip Maya_VRay_Dome_Light
zip -r ../../../releases/repository/sIBL_GUI/templates/Maya_VRay_Standard.zip Maya_VRay_Standard
cd ../XSI
zip -r ../../../releases/repository/sIBL_GUI/templates/XSI_MR_Standard.zip XSI_MR_Standard

#! Reaching Original Directory.
cd ../../../

#! sIBL_GUI Change Log Gathering.
cp -rf ./releases/Change\ Log.html ./releases/repository/sIBL_GUI/

#! sIBL_GUI Releases File.
cp -rf ./releases/sIBL_GUI_Releases.rc ./releases/repository/sIBL_GUI/

#! sIBL_GUI Manual / Help File.
cp -rf ./src/support/documentation/help ./releases/repository/sIBL_GUI/
rm ./releases/repository/sIBL_GUI/help/sIBL_GUI\ Manual