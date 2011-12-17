#/usr/bin/bash
echo ----------------------------------------------------------------
echo sIBL_GUI - Mac Os X - Overall Build
echo ----------------------------------------------------------------

alias python=/Library/Frameworks/Python.framework/Versions/2.7/bin/python

export PROJECT=/Users/KelSolaar/Documents/Developement/sIBL_GUI
export MAJOR_VERSION=4

export UTILITIES=$PROJECT/utilities

export SOURCE=$PROJECT/src/
export RELEASES=$PROJECT/releases/Darwin
export DISTRIBUTION=$RELEASES/dist
export BUILD=$RELEASES/build
export BUNDLE=$DISTRIBUTION/sIBL_GUI\ $MAJOR_VERSION.app
export DEPENDENCIES=$BUNDLE/Contents/Resources

IFS=","

#! sIBL_GUI cleanup.
echo ----------------------------------------------------------------
echo Cleanup - Begin
echo ----------------------------------------------------------------
rm -rf $BUILD $DISTRIBUTION $DEPENDENCIES
for type in ".pyc,.pyo,.DS_Store,Thumbs.db"
do
	python $UTILITIES/recursiveRemove.py $PROJECT $type
done
echo ----------------------------------------------------------------
echo Cleanup - End
echo ----------------------------------------------------------------

#! Darwin build.
echo ----------------------------------------------------------------
echo Build - Begin
echo ----------------------------------------------------------------
python $UTILITIES/darwinSetup.py py2app --includes "PyQt4.QtCore,PyQt4.QtGui,PyQt4.QtNetwork,PyQt4.QtSvg,PyQt4.QtWebKit,PyQt4.QtXml,PyQt4.uic,base64,cStringIO,code,collections,ctypes,datetime,functools,hashlib,inspect,itertools,linecache,logging,migrate,migrate.exceptions,migrate.versioning.api,optparse,os,pickle,platform,posixpath,re,shutil,sip,socket,sqlalchemy,sqlalchemy.ext.declarative,sqlalchemy.orm,sys,threading,time,traceback,weakref,xml.etree,zipfile" --excludes "foundations,manager,umbra,sibl_gui" --no-strip
python $UTILITIES/recursiveRemove.py $BUNDLE/ debug
echo ----------------------------------------------------------------
echo Build - End
echo ----------------------------------------------------------------

#! Darwin release.
echo ----------------------------------------------------------------
echo Release - Begin
echo ----------------------------------------------------------------
cp $SOURCE/sibl_gui/resources/images/Icon_Light_256.icns $DEPENDENCIES/
cp -f $RELEASES/support/qt.conf $DEPENDENCIES/
cp -r $RELEASES/support/plugins $BUNDLE/Contents/
packages="foundations,manager,umbra,sibl_gui"
for package in $packages
do
	cp -r $SOURCE/$package $DEPENDENCIES/
done
packages="umbra,sibl_gui"
extensions="bmp,icns,ico"
for package in $packages
do
	rm -rf $DEPENDENCIES/$package/resources/images/builders

	for extension in $extensions
	do
		rm -f $DEPENDENCIES/$package/resources/images/*.$extension
	done
done
rm -f $DEPENDENCIES/sibl_gui/libraries/freeImage/resources/*.dll
rm -f $DEPENDENCIES/sibl_gui/libraries/freeImage/resources/*.so
rm -rf $DEPENDENCIES/sibl_gui/resources/templates/3dsMax*
rm -rf $DEPENDENCIES/sibl_gui/resources/templates/Softimage*
rm -rf $DEPENDENCIES/sibl_gui/resources/templates/XSI*
echo ----------------------------------------------------------------
echo Release - End
echo ----------------------------------------------------------------

echo ----------------------------------------------------------------
echo Templates Textile Files Cleanup - Begin
echo ----------------------------------------------------------------
python $UTILITIES/recursiveRemove.py $BUNDLE/ .rst
echo ----------------------------------------------------------------
echo Templates Textile Files Cleanup - End
echo ----------------------------------------------------------------

#! sIBL_GUI DMG.
echo ----------------------------------------------------------------
echo Dmg Compilation - Begin
echo ----------------------------------------------------------------
rm -f ./*.dmg
dropdmg -g sIBL_GUI -y sIBL_GUI $BUNDLE
mv sIBL_GUI\ $MAJOR_VERSION.dmg sIBL_GUI.dmg
echo ----------------------------------------------------------------
echo Dmg Compilation - End
echo ----------------------------------------------------------------
