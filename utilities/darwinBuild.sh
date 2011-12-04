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
python $UTILITIES/recursiveRemove.py $DISTRIBUTION/sIBL_GUI.app/ debug
echo ----------------------------------------------------------------
echo Build - End
echo ----------------------------------------------------------------

#! Darwin release.
echo ----------------------------------------------------------------
echo Release - Begin
echo ----------------------------------------------------------------
cp $SOURCE/sibl_gui/resources/images/Icon_Light_256.icns $SITE/
cp -f ./support/qt.conf $SITE/
cp -r ./support/imageformats $DISTRIBUTION/sIBL_GUI.app/Contents/MacOs
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
rm -rf $SITE/sibl_gui/resources/templates/3dsMax*
rm -rf $SITE/sibl_gui/resources/templates/Softimage*
rm -rf $SITE/sibl_gui/resources/templates/XSI*
echo ----------------------------------------------------------------
echo Release - End
echo ----------------------------------------------------------------

echo ----------------------------------------------------------------
echo Templates Textile Files Cleanup - Begin
echo ----------------------------------------------------------------
python $UTILITIES/recursiveRemove.py $DISTRIBUTION/sIBL_GUI.app/ .rst
echo ----------------------------------------------------------------
echo Templates Textile Files Cleanup - End
echo ----------------------------------------------------------------

#! sIBL_GUI DMG.
echo ----------------------------------------------------------------
echo Dmg Compilation - Begin
echo ----------------------------------------------------------------
rm -f ./*.dmg
dropdmg -g sIBL_GUI -y sIBL_GUI $DISTRIBUTION/sIBL_GUI.app
echo ----------------------------------------------------------------
echo Dmg Compilation - End
echo ----------------------------------------------------------------
