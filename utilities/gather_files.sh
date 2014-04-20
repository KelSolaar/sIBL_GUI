#/bin/bash
echo -------------------------------------------------------------------------------
echo sIBL_GUI - Files Gathering
echo -------------------------------------------------------------------------------

export PROJECT_DIRECTORY=$(cd $( dirname "${BASH_SOURCE[0]}" )/..; pwd)

export DOCUMENTATION_DIRECTORY=$PROJECT_DIRECTORY/docs/
export RELEASES_DIRECTORY=$PROJECT_DIRECTORY/releases/
export REPOSITORY_DIRECTORY=$RELEASES_DIRECTORY/repository/
export UTILITIES_DIRECTORY=$PROJECT_DIRECTORY/utilities

#! Gathering folder cleanup.
rm -rf $REPOSITORY_DIRECTORY
mkdir -p $REPOSITORY_DIRECTORY/sIBL_GUI

#! Windows gathering.
cp $RELEASES_DIRECTORY/windows/sIBL_GUI_Setup.exe $REPOSITORY_DIRECTORY/sIBL_GUI/sIBL_GUI.exe

#! Mac Os X gathering.
cp $RELEASES_DIRECTORY/Darwin/sIBL_GUI.dmg $REPOSITORY_DIRECTORY/sIBL_GUI/sIBL_GUI.dmg

#! sIBL_GUI Changes gathering.
cp -rf $RELEASES_DIRECTORY/Changes.html $REPOSITORY_DIRECTORY/sIBL_GUI/

#! sIBL_GUI Releases file.
cp -rf $RELEASES_DIRECTORY/sIBL_GUI_Releases.rc $REPOSITORY_DIRECTORY/sIBL_GUI/

#! sIBL_GUI Manual / Help files.
cp -rf $DOCUMENTATION_DIRECTORY/help $REPOSITORY_DIRECTORY/sIBL_GUI/Help
rm $REPOSITORY_DIRECTORY/sIBL_GUI/help/sIBL_GUI_Manual.rst

#! sIBL_GUI Api files.
cp -rf $DOCUMENTATION_DIRECTORY/sphinx/build/html $REPOSITORY_DIRECTORY/sIBL_GUI/Api

#! sIBL_GUI Donations files.
cp -rf $DOCUMENTATION_DIRECTORY/donations $REPOSITORY_DIRECTORY/sIBL_GUI/Donations
rm $REPOSITORY_DIRECTORY/sIBL_GUI/Donations/Make_A_Donation.rst
