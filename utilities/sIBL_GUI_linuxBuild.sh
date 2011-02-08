#/usr/bin/bash
echo ----------------------------------------------------------------
echo sIBL_GUI - Linux - Overall Build
echo ----------------------------------------------------------------

#! Linux Build.
echo ----------------------------------------------------------------
echo Build - Begin
echo ----------------------------------------------------------------
rm -rf ../releases/Linux/build/
rm -rf ../releases/Linux/dist/
python /home/kelsolaar/Softwares/pyinstaller/Makespec.py --noconsole  ../src/sIBL_GUI.py -o ../releases/Linux
python /home/kelsolaar/Softwares/pyinstaller/Build.py ../releases/Linux/sIBL_GUI.spec
echo ----------------------------------------------------------------
echo Build - End
echo ----------------------------------------------------------------

#! Linux Release.
echo ----------------------------------------------------------------
echo Release - Begin
echo ----------------------------------------------------------------
rm -rf ../releases/Linux/sIBL_GUI/
cp -r ../releases/Linux/dist/sIBL_GUI ../releases/Linux/
mkdir ../releases/Linux/sIBL_GUI/ui/
cp ../src/ui/sIBL_GUI.ui ../releases/Linux/sIBL_GUI/ui/
cp ../src/ui/sIBL_GUI_Layouts.rc ../releases/Linux/sIBL_GUI/ui/
cp ../src/ui/Windows_styleSheet.qss ../releases/Linux/sIBL_GUI/ui/
cp ../src/ui/Darwin_styleSheet.qss ../releases/Linux/sIBL_GUI/ui/
cp ../src/ui/Linux_styleSheet.qss ../releases/Linux/sIBL_GUI/ui/
mkdir ../releases/Linux/sIBL_GUI/resources/
cp ../src/resources/Icon_Light.ico ../releases/Linux/sIBL_GUI/resources/
cp ../src/resources/sIBL_GUI_SpashScreen.png ../releases/Linux/sIBL_GUI/resources/
cp ../src/resources/sIBL_GUI_Logo.png ../releases/Linux/sIBL_GUI/resources/
cp ../src/resources/Central_Widget.png ../releases/Linux/sIBL_GUI/resources/
cp ../src/resources/Central_Widget_Hover.png ../releases/Linux/sIBL_GUI/resources/
cp ../src/resources/Central_Widget_Active.png ../releases/Linux/sIBL_GUI/resources/
cp ../src/resources/Layout.png ../releases/Linux/sIBL_GUI/resources/
cp ../src/resources/Layout_Hover.png ../releases/Linux/sIBL_GUI/resources/
cp ../src/resources/Layout_Active.png ../releases/Linux/sIBL_GUI/resources/
cp ../src/resources/Miscellaneous.png ../releases/Linux/sIBL_GUI/resources/
cp ../src/resources/Miscellaneous_Hover.png ../releases/Linux/sIBL_GUI/resources/
cp ../src/resources/Miscellaneous_Active.png ../releases/Linux/sIBL_GUI/resources/
cp ../src/resources/Library.png ../releases/Linux/sIBL_GUI/resources/
cp ../src/resources/Library_Hover.png ../releases/Linux/sIBL_GUI/resources/
cp ../src/resources/Library_Active.png ../releases/Linux/sIBL_GUI/resources/
cp ../src/resources/Export.png ../releases/Linux/sIBL_GUI/resources/
cp ../src/resources/Export_Hover.png ../releases/Linux/sIBL_GUI/resources/
cp ../src/resources/Export_Active.png ../releases/Linux/sIBL_GUI/resources/
cp ../src/resources/Preferences.png ../releases/Linux/sIBL_GUI/resources/
cp ../src/resources/Preferences_Hover.png ../releases/Linux/sIBL_GUI/resources/
cp ../src/resources/Preferences_Active.png ../releases/Linux/sIBL_GUI/resources/
cp ../src/resources/Toolbar.png ../releases/Linux/sIBL_GUI/resources/
mkdir ../releases/Linux/sIBL_GUI/templates
cp -r ../src/templates/Maya/* ../releases/Linux/sIBL_GUI/templates/
cp -r ../src/templates/Softimage/* ../releases/Linux/sIBL_GUI/templates/
cp -r ../src/templates/XSI/* ../releases/Linux/sIBL_GUI/templates/
cp -r ../src/components/ ../releases/Linux/sIBL_GUI/
echo ----------------------------------------------------------------
echo Release - End
echo ----------------------------------------------------------------

#! Templates Textile Files Cleanup.
echo ----------------------------------------------------------------
echo Templates Textile Files Cleanup - Begin
echo ----------------------------------------------------------------
#! XSI_MR_Standard Textile Template Documentation Removal.
rm "../releases/Linux/sIBL_GUI/templates/XSI_MR_Standard/help/XSI_MR_Standard Template Manual"

#! Softimage_MR_Standard Textile Template Documentation Removal.
rm "../releases/Linux/sIBL_GUI/templates/Softimage_MR_Standard/help/Softimage_MR_Standard Template Manual"

#! Maya_MR_Standard Textile Template Documentation Removal.
rm "../releases/Linux/sIBL_GUI/templates/Maya_MR_Standard/help/Maya_MR_Standard Template Manual"

#! Maya_RfM_Standard Textile Template Documentation Removal.
rm "../releases/Linux/sIBL_GUI/templates/Maya_RfM_Standard/help/Maya_RfM_Standard Template Manual"

#! Maya_Turtle_Standard Textile Template Documentation Removal.
rm "../releases/Linux/sIBL_GUI/templates/Maya_Turtle_Standard/help/Maya_Turtle_Standard Template Manual"

#! Maya_VRay_Dome_Light Textile Template Documentation Removal.
rm "../releases/Linux/sIBL_GUI/templates/Maya_VRay_Dome_Light/help/Maya_VRay_Dome_Light Template Manual"

#! Maya_VRay_Standard Textile Template Documentation Removal.
rm "../releases/Linux/sIBL_GUI/templates/Maya_VRay_Standard/help/Maya_VRay_Standard Template Manual"

echo ----------------------------------------------------------------
echo Templates Textile Files Cleanup - End
echo ----------------------------------------------------------------

#! sIBL_GUI Cleanup.
echo ----------------------------------------------------------------
echo Cleanup - Begin
echo ----------------------------------------------------------------
python ./sIBL_GUI_recursiveRemove.py ../releases/Linux/sIBL_GUI/ .pyc
python ./sIBL_GUI_recursiveRemove.py ../releases/Linux/sIBL_GUI/ .pyo
python ./sIBL_GUI_recursiveRemove.py ../releases/Linux/sIBL_GUI/ .DS_Store
python ./sIBL_GUI_recursiveRemove.py ../releases/Linux/sIBL_GUI/ Thumbs.db
echo ----------------------------------------------------------------
echo Cleanup - End
echo ----------------------------------------------------------------