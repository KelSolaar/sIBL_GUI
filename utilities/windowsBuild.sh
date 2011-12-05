#/usr/bin/bash
echo ----------------------------------------------------------------
echo sIBL_GUI - Windows - Overall Build
echo ----------------------------------------------------------------

export PYINSTALLER=c:/pyinstaller
export APPLICATION=z:/Documents/Developement/sIBL_GUI
export PYTHONPATH=$APPLICATION/src

export SOURCE=$APPLICATION/src
export RELEASES=$APPLICATION/releases/Windows
export DISTRIBUTION=$RELEASES/dist
export BUILD=$RELEASES/build
export SITE=$RELEASES/sIBL_GUI
export UTILITIES=$APPLICATION/utilities

#! sIBL_GUI cleanup.
echo ----------------------------------------------------------------
echo Cleanup - Begin
echo ----------------------------------------------------------------
rm -rf $BUILD $DISTRIBUTION $SITE
#! python $UTILITIES/recursiveRemove.py $APPLICATION .pyc
#! python $UTILITIES/recursiveRemove.py $APPLICATION .pyo
#! python $UTILITIES/recursiveRemove.py $APPLICATION .DS_Store
#! python $UTILITIES/recursiveRemove.py $APPLICATION Thumbs.db
echo ----------------------------------------------------------------
echo Cleanup - End
echo ----------------------------------------------------------------

#! Windows build.
echo ----------------------------------------------------------------
echo Build - Begin
echo ----------------------------------------------------------------
#! python $PYINSTALLER/Makespec.py --noconsole --icon "$SOURCE/sibl_gui/resources/images/Icon_Light.ico" $SOURCE/sIBL_GUI.py -o $RELEASES
cp $UTILITIES/windowsBuild.py $RELEASES/sIBL_GUI.spec
python $PYINSTALLER/Build.py $RELEASES/sIBL_GUI.spec
echo ----------------------------------------------------------------
echo Build - End
echo ----------------------------------------------------------------

#! Windows release.
echo ----------------------------------------------------------------
echo Release - Begin
echo ----------------------------------------------------------------
cp -r $DISTRIBUTION/sIBL_GUI $RELEASES/
packages="foundations manager umbra sibl_gui"
for package in $packages
do
	cp -r $SOURCE/$package $SITE/
done
packages="umbra sibl_gui"
extensions="bmp icns ico"
for package in $packages
do
	rm -rf $SITE/$package/resources/images/builders

	for extension in $extensions
	do
		rm $SITE/$package/resources/images/*.$extension
	done
done
rm $SITE/sibl_gui/libraries/freeImage/resources/*.dylib
rm $SITE/sibl_gui/libraries/freeImage/resources/*.so
echo ----------------------------------------------------------------
echo Release - End
echo ----------------------------------------------------------------

#! Templates textile files cleanup.
echo ----------------------------------------------------------------
echo Templates Textile Files Cleanup - Begin
echo ----------------------------------------------------------------
#! 3dsMax_MR_Standard textile template documentation removal.
rm "$SITE/sibl_gui/resources/templates/3dsMax_MR_Standard/help/3dsMax_MR_Standard Template Manual"

#! 3dsMax_Scanline_Standard template documentation removal.
rm "$SITE/sibl_gui/resources/templates/3dsMax_Scanline_Standard/help/3dsMax_Scanline_Standard Template Manual"

#! 3dsMax_VRay_Standard template documentation removal.
rm "$SITE/sibl_gui/resources/templates/3dsMax_VRay_Standard/help/3dsMax_VRay_Standard Template Manual"

#! Maya_Arnold_Standard template documentation removal.
rm "$SITE/sibl_gui/resources/templates/Maya_Arnold_Standard/help/Maya_Arnold_Standard Template Manual"

#! Maya_MR_Lightsmith template documentation removal.
rm "$SITE/sibl_gui/resources/templates/Maya_MR_Lightsmith/help/Maya_MR_Lightsmith Template Manual"

#! Maya_MR_Standard template documentation removal.
rm "$SITE/sibl_gui/resources/templates/Maya_MR_Standard/help/Maya_MR_Standard Template Manual"

#! Maya_RfM_Standard template documentation removal.
rm "$SITE/sibl_gui/resources/templates/Maya_RfM_Standard/help/Maya_RfM_Standard Template Manual"

#! Maya_VRay_Dome_Light template documentation removal.
rm "$SITE/sibl_gui/resources/templates/Maya_VRay_Dome_Light/help/Maya_VRay_Dome_Light Template Manual"

#! Maya_VRay_Lightsmith template documentation removal.
rm "$SITE/sibl_gui/resources/templates/Maya_VRay_Lightsmith/help/Maya_VRay_Lightsmith Template Manual"

#! Maya_VRay_Standard template documentation removal.
rm "$SITE/sibl_gui/resources/templates/Maya_VRay_Standard/help/Maya_VRay_Standard Template Manual"

#! Softimage_Arnold_Dome_Light template documentation removal.
rm "$SITE/sibl_gui/resources/templates/Softimage_Arnold_Dome_Light/help/Softimage_Arnold_Dome_Light Template Manual"

#! Softimage_Arnold_Lightsmith template documentation removal.
rm "$SITE/sibl_gui/resources/templates/Softimage_Arnold_Lightsmith/help/Softimage_Arnold_Lightsmith Template Manual"

#! Softimage_Arnold_Standard template documentation removal.
rm "$SITE/sibl_gui/resources/templates/Softimage_Arnold_Standard/help/Softimage_Arnold_Standard Template Manual"

#! Softimage_MR_Lightsmith template documentation removal.
rm "$SITE/sibl_gui/resources/templates/Softimage_MR_Lightsmith/help/Softimage_MR_Lightsmith Template Manual"

#! Softimage_MR_Standard template documentation removal.
rm "$SITE/sibl_gui/resources/templates/Softimage_MR_Standard/help/Softimage_MR_Standard Template Manual"

#! XSI_Arnold_Dome_Light template documentation removal.
rm "$SITE/sibl_gui/resources/templates/XSI_Arnold_Dome_Light/help/XSI_Arnold_Dome_Light Template Manual"

#! XSI_Arnold_Standard template documentation removal.
rm "$SITE/sibl_gui/resources/templates/XSI_Arnold_Standard/help/XSI_Arnold_Standard Template Manual"

#! XSI_MR_Standard template documentation removal.
rm "$SITE/sibl_gui/resources/templates/XSI_MR_Standard/help/XSI_MR_Standard Template Manual"
echo ----------------------------------------------------------------
echo Templates Textile Files Cleanup - End
echo ----------------------------------------------------------------
