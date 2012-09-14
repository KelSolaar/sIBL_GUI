#/bin/bash
echo -------------------------------------------------------------------------------
echo sIBL_GUI - Files Gathering
echo -------------------------------------------------------------------------------

export PROJECT=$( dirname "${BASH_SOURCE[0]}" )/..

export DOCUMENTATION=$PROJECT/docs/
export RELEASES=$PROJECT/releases/
export REPOSITORY=$RELEASES/repository/
export UTILITIES=$PROJECT/utilities

#! Gathering folder cleanup.
rm -rf $REPOSITORY
mkdir -p $REPOSITORY/sIBL_GUI

#! Windows gathering.
cp $RELEASES/windows/sIBL_GUI_Setup.exe $REPOSITORY/sIBL_GUI/sIBL_GUI.exe

#! Mac Os X gathering.
cp $RELEASES/Darwin/sIBL_GUI.dmg $REPOSITORY/sIBL_GUI/sIBL_GUI.dmg

#! sIBL_GUI Changes gathering.
cp -rf $RELEASES/Changes.html $REPOSITORY/sIBL_GUI/

#! sIBL_GUI Releases file.
cp -rf $RELEASES/sIBL_GUI_Releases.rc $REPOSITORY/sIBL_GUI/

#! sIBL_GUI Manual / Help files.
cp -rf $DOCUMENTATION/help $REPOSITORY/sIBL_GUI/Help
rm $REPOSITORY/sIBL_GUI/help/sIBL_GUI_Manual.rst

#! sIBL_GUI Api files.
cp -rf $DOCUMENTATION/sphinx/build/html $REPOSITORY/sIBL_GUI/Api

#! sIBL_GUI Donations files.
cp -rf $DOCUMENTATION/donations $REPOSITORY/sIBL_GUI/Donations
rm $REPOSITORY/sIBL_GUI/Donations/Make_A_Donation.rst
