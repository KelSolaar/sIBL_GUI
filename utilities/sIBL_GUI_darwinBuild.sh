#/usr/bin/bash
echo ----------------------------------------------------------------
echo sIBL_GUI - Mac Os X - Overall Build
echo ----------------------------------------------------------------

alias python=/Library/Frameworks/Python.framework/Versions/2.7/bin/python
export APPLICATION=/Users/KelSolaar/Documents/Developement/sIBL_GUI

export SOURCE=$APPLICATION/src/umbra
export RELEASES=$APPLICATION/releases/Darwin
export DISTRIBUTION=$RELEASES/dist
export BUILD=$RELEASES/build
export UTILITIES=$APPLICATION/utilities

#! Darwin build.
echo ----------------------------------------------------------------
echo Build - Begin
echo ----------------------------------------------------------------
rm -rf $BUILD $DISTRIBUTION
python $UTILITIES/sIBL_GUI_darwinSetup.py py2app --includes "code,foundations.pkzip,foundations.strings,foundations.rotatingBackup,migrate.exceptions,migrate.versioning.api,PyQt4.QtNetwork,PyQt4.QtWebKit,umbra.components.core.db.dbUtilities.common,umbra.components.core.db.dbUtilities.types,umbra.libraries.freeImage.freeImage,umbra.ui.completers,umbra.ui.highlighters,umbra.ui.widgets.codeEditor_QPlainTextEdit,umbra.ui.widgets.search_QLineEdit,umbra.ui.widgets.variable_QPushButton,sip,sqlalchemy,sqlalchemy.databases,sqlalchemy.ext.declarative,sqlalchemy.ext,sqlalchemy.orm" --no-strip
rm -rf `find $DISTRIBUTION/sIBL_GUI.app/ -name *debug*`
echo ----------------------------------------------------------------
echo Build - End
echo ----------------------------------------------------------------

#! Darwin release.
echo ----------------------------------------------------------------
echo Release - Begin
echo ----------------------------------------------------------------
cp $SOURCE/resources/images/Icon_Light_512.icns $DISTRIBUTION/sIBL_GUI.app/Contents/Resources/
mkdir -p $DISTRIBUTION/sIBL_GUI.app/Contents/Resources/resources/images
images=( "Central_Widget.png" "Central_Widget_Active.png" "Central_Widget_Hover.png" "Close_Cross.png" "Close_Cross_Hover.png" "Export.png" "Export_Active.png" "Export_Hover.png" "Horizontal_Scrollbar_Grip.png" "Icon_Light.png" "Inspect.png" "Inspect_Active.png" "Inspect_Hover.png" "Layout.png" "Layout_Active.png" "Layout_Hover.png" "Library.png" "Library_Active.png" "Library_Hover.png" "Miscellaneous.png" "Miscellaneous_Active.png" "Miscellaneous_Hover.png" "Preferences.png" "Preferences_Active.png" "Preferences_Hover.png" "Resize_Grip.png" "sIBL_GUI_Logo.png" "sIBL_GUI_SpashScreen.png" "Small_Down_Arrow.png" "Small_Left_Arrow.png" "Small_Right_Arrow.png" "Small_Up_Arrow.png" "Thumbnail_Format_Not_Supported_Yet.png" "Thumbnail_Not_Found.png" "Tiny_Down_Arrow.png" "Tiny_Up_Arrow.png" "TreeView_Branch_Closed.png" "TreeView_Branch_End.png" "TreeView_Branch_More.png" "TreeView_Branch_Open.png" "TreeView_VLine.png" "Undock_Window.png" "Undock_Window_Hover.png" "Vertical_Scrollbar_Grip.png" )
for image in "${images[@]}"
do
	cp $SOURCE/resources/images/$image $DISTRIBUTION/sIBL_GUI.app/Contents/Resources/resources/images
done
resourcesDirectories=( "layouts" "others" "styles" )
for directory in "${resourcesDirectories[@]}"
do
	cp -r $SOURCE/resources/$directory $DISTRIBUTION/sIBL_GUI.app/Contents/Resources/resources/
done
cp $SOURCE/resources/sIBL_GUI.ui $DISTRIBUTION/sIBL_GUI.app/Contents/Resources/resources/sIBL_GUI.ui
mkdir -p $DISTRIBUTION/sIBL_GUI.app/Contents/Resources/templates
cp -r $SOURCE/templates/Maya/* $DISTRIBUTION/sIBL_GUI.app/Contents/Resources/templates/
cp -r $SOURCE/components $DISTRIBUTION/sIBL_GUI.app/Contents/Resources/
mkdir -p $DISTRIBUTION/sIBL_GUI.app/Contents/Resources/libraries/freeImage/resources
cp -r $SOURCE/libraries/freeImage/resources/libfreeimage.dylib $DISTRIBUTION/sIBL_GUI.app/Contents/Resources/libraries/freeImage/resources/
#! cp -f ./support/__boot__.py $DISTRIBUTION/sIBL_GUI.app/Contents/Resources/
cp -f ./support/qt.conf $DISTRIBUTION/sIBL_GUI.app/Contents/Resources/
cp -r ./support/imageformats $DISTRIBUTION/sIBL_GUI.app/Contents/MacOs
echo ----------------------------------------------------------------
echo Release - End
echo ----------------------------------------------------------------

echo ----------------------------------------------------------------
echo Templates Textile Files Cleanup - Begin
echo ----------------------------------------------------------------
#! Maya_Arnold_Standard template documentation removal.
rm "$DISTRIBUTION/sIBL_GUI.app/Contents/Resources/templates/Maya_Arnold_Standard/help/Maya_Arnold_Standard Template Manual"

#! Maya_MR_Lightsmith template documentation removal.
rm "$DISTRIBUTION/sIBL_GUI.app/Contents/Resources/templates/Maya_MR_Lightsmith/help/Maya_MR_Lightsmith Template Manual"

#! Maya_MR_Standard template documentation removal.
rm "$DISTRIBUTION/sIBL_GUI.app/Contents/Resources/templates/Maya_MR_Standard/help/Maya_MR_Standard Template Manual"

#! Maya_RfM_Standard template documentation removal.
rm "$DISTRIBUTION/sIBL_GUI.app/Contents/Resources/templates/Maya_RfM_Standard/help/Maya_RfM_Standard Template Manual"

#! Maya_VRay_Dome_Light template documentation removal.
rm "$DISTRIBUTION/sIBL_GUI.app/Contents/Resources/templates/Maya_VRay_Dome_Light/help/Maya_VRay_Dome_Light Template Manual"

#! Maya_VRay_Lightsmith template documentation removal.
rm "$DISTRIBUTION/sIBL_GUI.app/Contents/Resources/templates/Maya_VRay_Lightsmith/help/Maya_VRay_Lightsmith Template Manual"

#! Maya_VRay_Standard template documentation removal.
rm "$DISTRIBUTION/sIBL_GUI.app/Contents/Resources/templates/Maya_VRay_Standard/help/Maya_VRay_Standard Template Manual"
echo ----------------------------------------------------------------
echo Templates Textile Files Cleanup - End
echo ----------------------------------------------------------------

#! sIBL_GUI cleanup.
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