#/usr/bin/bash
echo ----------------------------------------------------------------
echo sIBL_GUI - Windows - Overall Build
echo ----------------------------------------------------------------

export PYINSTALLER=c:/pyinstaller
export PROJECT=z:/Documents/Developement/sIBL_GUI
export PYTHONPATH=$PROJECT/src

export UTILITIES=$PROJECT/utilities

export SOURCE=$PROJECT/src
export RELEASES=$PROJECT/releases/Windows
export DISTRIBUTION=$RELEASES/dist
export BUILD=$RELEASES/build
export DEPENDENCIES=$RELEASES/sIBL_GUI

IFS=","

#! sIBL_GUI cleanup.
echo ----------------------------------------------------------------
echo Cleanup - Begin
echo ----------------------------------------------------------------
rm -rf $BUILD $DISTRIBUTION $DEPENDENCIES
rm -rf $BUILD $DISTRIBUTION $DEPENDENCIES
for type in ".pyc,.pyo,.DS_Store,Thumbs.db"
do
	python $UTILITIES/recursiveRemove.py $PROJECT $type
done
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
rm -f $DEPENDENCIES/sibl_gui/libraries/freeImage/resources/*.dylib
rm -f $DEPENDENCIES/sibl_gui/libraries/freeImage/resources/*.so
echo ----------------------------------------------------------------
echo Release - End
echo ----------------------------------------------------------------

echo ----------------------------------------------------------------
echo Templates Textile Files Cleanup - Begin
echo ----------------------------------------------------------------
python $UTILITIES/recursiveRemove.py $DEPENDENCIES/sibl_gui/resources/templates/ .rst
echo ----------------------------------------------------------------
echo Templates Textile Files Cleanup - End
echo ----------------------------------------------------------------