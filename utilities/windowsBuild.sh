#/usr/bin/bash
echo -------------------------------------------------------------------------------
echo sIBL_GUI - Windows - Overall Build
echo -------------------------------------------------------------------------------

export PYINSTALLER=c:/pyinstaller
export PYTHONPATH=$PROJECT

export PROJECT=z:/Documents/Development/sIBL_GUI
export MAJOR_VERSION=4

export UTILITIES=$PROJECT/utilities

export SOURCE=$PROJECT
export RELEASES=$PROJECT/releases/Windows
export DISTRIBUTION=$RELEASES/dist
export BUILD=$RELEASES/build
export BUNDLE=$RELEASES/sIBL_GUI\ $MAJOR_VERSION
export DEPENDENCIES=$BUNDLE

IFS=","

#! sIBL_GUI cleanup.
echo -------------------------------------------------------------------------------
echo Cleanup - Begin
echo -------------------------------------------------------------------------------
rm -rf $BUILD $DISTRIBUTION $DEPENDENCIES $BUNDLE
packages="foundations,manager,umbra,sibl_gui"
for package in $packages
do
	for type in ".pyc,.pyo,.DS_Store,Thumbs.db"
	do
		python $UTILITIES/recursiveRemove.py $( $UTILITIES/getPackagePath.py $package ) $type
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
cp $UTILITIES/windowsSetup.py $RELEASES/sIBL_GUI.spec
python $PYINSTALLER/Build.py $RELEASES/sIBL_GUI.spec
echo -------------------------------------------------------------------------------
echo Build - End
echo -------------------------------------------------------------------------------

#! Windows release.
echo -------------------------------------------------------------------------------
echo Release - Begin
echo -------------------------------------------------------------------------------
cp -r $DISTRIBUTION/sIBL_GUI $BUNDLE
for package in $packages
do
	cp -rL $( cygpath --unix $( $UTILITIES/getPackagePath.py $package ) ) $DEPENDENCIES/$package
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
rm -f $DEPENDENCIES/sibl_gui/libraries/freeImage/resources/*.dylib
rm -f $DEPENDENCIES/sibl_gui/libraries/freeImage/resources/*.so
rm -rf $DEPENDENCIES/*/tests
echo -------------------------------------------------------------------------------
echo Release - End
echo -------------------------------------------------------------------------------

echo -------------------------------------------------------------------------------
echo Templates Textile Files Cleanup - Begin
echo -------------------------------------------------------------------------------
python $UTILITIES/recursiveRemove.py $DEPENDENCIES/sibl_gui/resources/templates/ .rst
echo -------------------------------------------------------------------------------
echo Templates Textile Files Cleanup - End
echo -------------------------------------------------------------------------------