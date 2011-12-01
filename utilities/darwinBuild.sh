#/usr/bin/bash
echo ----------------------------------------------------------------
echo sIBL_GUI - Mac Os X - Overall Build
echo ----------------------------------------------------------------

alias python=/Library/Frameworks/Python.framework/Versions/2.7/bin/python
export APPLICATION=/Users/KelSolaar/Documents/Developement/sIBL_GUI

export SOURCE=$APPLICATION/src/
export RELEASES=$APPLICATION/releases/Darwin
export DISTRIBUTION=$RELEASES/dist
export BUILD=$RELEASES/build
export UTILITIES=$APPLICATION/utilities
export SITE=$DISTRIBUTION/sIBL_GUI.app/Contents/Resources

#! sIBL_GUI cleanup.
echo ----------------------------------------------------------------
echo Cleanup - Begin
echo ----------------------------------------------------------------
rm -rf $BUILD $DISTRIBUTION
python $UTILITIES/recursiveRemove.py $APPLICATION .pyc
python $UTILITIES/recursiveRemove.py $APPLICATION .pyo
python $UTILITIES/recursiveRemove.py $APPLICATION .DS_Store
python $UTILITIES/recursiveRemove.py $APPLICATION Thumbs.db
echo ----------------------------------------------------------------
echo Cleanup - End
echo ----------------------------------------------------------------

#! Darwin build.
echo ----------------------------------------------------------------
echo Build - Begin
echo ----------------------------------------------------------------
python $UTILITIES/darwinSetup.py py2app --includes "PyQt4.QtCore,PyQt4.QtGui,PyQt4.QtNetwork,PyQt4.QtWebKit,PyQt4.uic,base64,cStringIO,code,collections,ctypes,datetime,functools,hashlib,inspect,itertools,linecache,logging,migrate,migrate.exceptions,migrate.versioning.api,optparse,os,pickle,platform,posixpath,re,shutil,sip,socket,sqlalchemy,sqlalchemy.ext.declarative,sqlalchemy.orm,sys,threading,time,traceback,weakref,xml.etree,zipfile" --excludes "foundations,manager,umbra,sibl_gui" --no-strip
rm -rf `find $DISTRIBUTION/sIBL_GUI.app/ -name *debug*`
echo ----------------------------------------------------------------
echo Build - End
echo ----------------------------------------------------------------

#! Darwin release.
echo ----------------------------------------------------------------
echo Release - Begin
echo ----------------------------------------------------------------

cp $SOURCE/sibl_gui/resources/images/Icon_Light_512.icns $SITE/
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
rm $SITE/sibl_gui/libraries/freeImage/resources/*.dll
rm $SITE/sibl_gui/libraries/freeImage/resources/*.so
cp -f ./support/qt.conf $SITE/
cp -r ./support/imageformats $DISTRIBUTION/sIBL_GUI.app/Contents/MacOs
echo ----------------------------------------------------------------
echo Release - End
echo ----------------------------------------------------------------

echo ----------------------------------------------------------------
echo Templates Textile Files Cleanup - Begin
echo ----------------------------------------------------------------
#! Maya_Arnold_Standard template documentation removal.
#! rm "$SITE/templates/Maya_Arnold_Standard/help/Maya_Arnold_Standard Template Manual"

#! Maya_MR_Lightsmith template documentation removal.
#! rm "$SITE/templates/Maya_MR_Lightsmith/help/Maya_MR_Lightsmith Template Manual"

#! Maya_MR_Standard template documentation removal.
#! rm "$SITE/templates/Maya_MR_Standard/help/Maya_MR_Standard Template Manual"

#! Maya_RfM_Standard template documentation removal.
#! rm "$SITE/templates/Maya_RfM_Standard/help/Maya_RfM_Standard Template Manual"

#! Maya_VRay_Dome_Light template documentation removal.
#! rm "$SITE/templates/Maya_VRay_Dome_Light/help/Maya_VRay_Dome_Light Template Manual"

#! Maya_VRay_Lightsmith template documentation removal.
#! rm "$SITE/templates/Maya_VRay_Lightsmith/help/Maya_VRay_Lightsmith Template Manual"

#! Maya_VRay_Standard template documentation removal.
#! rm "$SITE/templates/Maya_VRay_Standard/help/Maya_VRay_Standard Template Manual"
echo ----------------------------------------------------------------
echo Templates Textile Files Cleanup - End
echo ----------------------------------------------------------------

#! sIBL_GUI DMG.
echo ----------------------------------------------------------------
echo Dmg Compilation - Begin
echo ----------------------------------------------------------------
#! rm -f ./sIBL_GUI.dmg
#! hdiutil create ./sIBL_GUI.dmg -volname "sIBL_GUI" -fs HFS+ -srcfolder "$DISTRIBUTION/sIBL_GUI.app"
#! dropdmg -g sIBL_GUI -y sIBL_GUI $DISTRIBUTION/sIBL_GUI.app
echo ----------------------------------------------------------------
echo Dmg Compilation - End
echo ----------------------------------------------------------------