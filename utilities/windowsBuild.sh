#!/usr/bin/env bash
echo -------------------------------------------------------------------------------
echo sIBL_GUI - Windows - Overall Build
echo -------------------------------------------------------------------------------

export PYINSTALLER_DIRECTORY=c:/pyinstaller
export PYTHONPATH=$PROJECT

export PROJECT_DIRECTORY=z:/Documents/Development/sIBL_GUI
export PROJECT_MAJOR_VERSION=4

export UTILITIES_DIRECTORY=$PROJECT_DIRECTORY/utilities

export SOURCE_DIRECTORY=$PROJECT_DIRECTORY
export RELEASES_DIRECTORY=$PROJECT_DIRECTORY/releases/Windows
export DISTRIBUTION_DIRECTORY=$RELEASES_DIRECTORY/dist
export BUILD_DIRECTORY=$RELEASES_DIRECTORY/build
export BUNDLE_DIRECTORY=$RELEASES_DIRECTORY/sIBL_GUI\ $PROJECT_MAJOR_VERSION
export DEPENDENCIES_DIRECTORY=$BUNDLE_DIRECTORY

IFS=","

#! sIBL_GUI cleanup.
echo -------------------------------------------------------------------------------
echo Cleanup - Begin
echo -------------------------------------------------------------------------------
rm -rf $BUILD_DIRECTORY $DISTRIBUTION_DIRECTORY $DEPENDENCIES_DIRECTORY $BUNDLE_DIRECTORY
packages="foundations,manager,umbra,sibl_gui"
types=".pyc,.pyo,.DS_Store,Thumbs.db"
for package in $packages
do
	for type in $types
	do
		python $UTILITIES_DIRECTORY/recursiveRemove.py --input $( $UTILITIES_DIRECTORY/getPackagePath.py --package $package ) --pattern $type
	done
done
echo -------------------------------------------------------------------------------
echo Cleanup - End
echo -------------------------------------------------------------------------------

#! Windows build.
echo -------------------------------------------------------------------------------
echo Build - Begin
echo -------------------------------------------------------------------------------
#! python $PYINSTALLER/Makespec.py --noconsole --icon "$SOURCE/sibl_gui/resources/images/Icon_Light.ico" $SOURCE/sIBL_GUI.py -o $RELEASES
cp $UTILITIES_DIRECTORY/windowsSetup.py $RELEASES_DIRECTORY/sIBL_GUI.spec
python $PYINSTALLER_DIRECTORY/Build.py $RELEASES_DIRECTORY/sIBL_GUI.spec
echo -------------------------------------------------------------------------------
echo Build - End
echo -------------------------------------------------------------------------------

#! Windows release.
echo -------------------------------------------------------------------------------
echo Release - Begin
echo -------------------------------------------------------------------------------
cp -r $DISTRIBUTION_DIRECTORY/sIBL_GUI $BUNDLE_DIRECTORY
for package in $packages
do
	cp -rL $( cygpath --unix $( $UTILITIES_DIRECTORY/getPackagePath.py --package $package ) ) $DEPENDENCIES_DIRECTORY/$package
done
packages="umbra,sibl_gui"
extensions="bmp,icns,ico"
for package in $packages
do
	rm -rf $DEPENDENCIES_DIRECTORY/$package/resources/images/builders

	for extension in $extensions
	do
		rm -f $DEPENDENCIES_DIRECTORY/$package/resources/images/*.$extension
	done
done
rm -f $DEPENDENCIES_DIRECTORY/sibl_gui/libraries/freeImage/resources/*.dylib
rm -f $DEPENDENCIES_DIRECTORY/sibl_gui/libraries/freeImage/resources/*.so
rm -rf $DEPENDENCIES_DIRECTORY/*/tests
echo -------------------------------------------------------------------------------
echo Release - End
echo -------------------------------------------------------------------------------

echo -------------------------------------------------------------------------------
echo Templates Textile Files Cleanup - Begin
echo -------------------------------------------------------------------------------
python $UTILITIES_DIRECTORY/recursiveRemove.py --input $DEPENDENCIES_DIRECTORY/sibl_gui/resources/templates/ --pattern .rst
echo -------------------------------------------------------------------------------
echo Templates Textile Files Cleanup - End
echo -------------------------------------------------------------------------------

echo -------------------------------------------------------------------------------
echo Console Build - Begin
echo -------------------------------------------------------------------------------
rm -rf $BUILD_DIRECTORY $DISTRIBUTION_DIRECTORY
export CONSOLE_BUILD=True
python $PYINSTALLER_DIRECTORY/Build.py $RELEASES_DIRECTORY/sIBL_GUI.spec
cp -r $DISTRIBUTION_DIRECTORY/sIBL_GUI/sIBL_GUI.exe $BUNDLE_DIRECTORY/sIBL_GUI\ $PROJECT_MAJOR_VERSION\ -\ Console.exe
cp -r $DISTRIBUTION_DIRECTORY/sIBL_GUI/sIBL_GUI.exe.manifest $BUNDLE_DIRECTORY/sIBL_GUI\ $PROJECT_MAJOR_VERSION\ -\ Console.exe.manifest
echo -------------------------------------------------------------------------------
echo Console Build - End
echo -------------------------------------------------------------------------------
