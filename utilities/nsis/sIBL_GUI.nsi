Name "sIBL_GUI"

# Handle shortcuts deletion on Windows Vista / 7.
RequestExecutionLevel user

# General Symbols Definitions.
!define MAJOR_VERSION 4
!define MINOR_VERSION 0
!define CHANGE_VERSION 0
!define RELEASE "${MAJOR_VERSION}.${MINOR_VERSION}.${CHANGE_VERSION}"
!define APPLICATION "$(^Name) ${MAJOR_VERSION}"
!define COMPANY "HDRLabs"
!define URL "http://www.thomasmansencal.com/"

!define REGKEY "SOFTWARE\${COMPANY}\$(^Name)"

# MUI Symbols Definitions.
!define MUI_ICON "..\..\src\sibl_gui\resources\images\Icon_Light.ico"
!define MUI_FINISHPAGE_NOAUTOCLOSE
!define MUI_STARTMENUPAGE_REGISTRY_ROOT HKLM
!define MUI_STARTMENUPAGE_REGISTRY_KEY ${REGKEY}
!define MUI_STARTMENUPAGE_REGISTRY_VALUENAME StartMenuGroup
!define MUI_STARTMENUPAGE_DEFAULTFOLDER "${COMPANY}\${APPLICATION}"
!define MUI_UNICON "..\..\src\sibl_gui\resources\images\Icon_Light.ico"
!define MUI_UNFINISHPAGE_NOAUTOCLOSE

# Included files.
!include Sections.nsh
!include MUI2.nsh

# Reserved Files.
ReserveFile "${NSISDIR}\Plugins\AdvSplash.dll"

# Variables.
Var StartMenuGroup

# Installer pages.
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE ..\..\src\COPYING
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_STARTMENU Application $StartMenuGroup
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES

# Installer languages.
!insertmacro MUI_LANGUAGE English

# Installer attributes.
OutFile sIBL_GUI_Setup.exe
InstallDir "$PROGRAMFILES\${COMPANY}\${APPLICATION}"
CRCCheck on
XPStyle on
ShowInstDetails show
VIProductVersion "${MAJOR_VERSION}.${MINOR_VERSION}.${CHANGE_VERSION}.0"
VIAddVersionKey ProductName "${APPLICATION}"
VIAddVersionKey ProductVersion "${RELEASE}"
VIAddVersionKey CompanyName "${COMPANY}"
VIAddVersionKey CompanyWebsite "${URL}"
VIAddVersionKey FileVersion "${RELEASE}"
VIAddVersionKey FileDescription ""
VIAddVersionKey LegalCopyright ""
InstallDirRegKey HKLM "${REGKEY}" Path
ShowUninstDetails show

# Installer sections.
Section -Main SEC0000
	SetOutPath $INSTDIR
    ExecWait '"$INSTDIR\Uninstall.exe" /S'
    SetOverwrite on
    !include  "installedFiles.nsh"
    WriteRegStr HKLM "${REGKEY}\Components" Main 1
SectionEnd

Section -post SEC0001
	WriteRegStr HKLM "${REGKEY}" Path $INSTDIR
	SetOutPath $INSTDIR
	WriteUninstaller $INSTDIR\Uninstall.exe
	!insertmacro MUI_STARTMENU_WRITE_BEGIN Application
	SetOutPath $INSTDIR
	CreateShortcut "$DESKTOP\${APPLICATION}.lnk" $INSTDIR\$(^Name).exe
	SetOutPath $SMPROGRAMS\$StartMenuGroup
	SetOutPath $INSTDIR
	CreateShortcut "$SMPROGRAMS\$StartMenuGroup\${APPLICATION}.lnk" $INSTDIR\$(^Name).exe
	CreateShortcut "$SMPROGRAMS\$StartMenuGroup\Uninstall ${APPLICATION}.lnk" $INSTDIR\Uninstall.exe
	!insertmacro MUI_STARTMENU_WRITE_END
	WriteRegStr HKLM "SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\${APPLICATION}" DisplayName "${APPLICATION}"
	WriteRegStr HKLM "SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\${APPLICATION}" DisplayVersion "${RELEASE}"
	WriteRegStr HKLM "SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\${APPLICATION}" Publisher "${COMPANY}"
	WriteRegStr HKLM "SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\${APPLICATION})" URLInfoAbout "${URL}"
	WriteRegStr HKLM "SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\${APPLICATION}" DisplayIcon $INSTDIR\Uninstall.exe
	WriteRegStr HKLM "SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\${APPLICATION}" UninstallString $INSTDIR\Uninstall.exe
	WriteRegDWORD HKLM "SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\${APPLICATION}" NoModify 1
	WriteRegDWORD HKLM "SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\${APPLICATION}" NoRepair 1
SectionEnd

# Macro for selecting uninstaller sections.
!macro SELECT_UNSECTION SECTION_NAME UNSECTION_ID
	Push $R0
	ReadRegStr $R0 HKLM "${REGKEY}\Components" "${SECTION_NAME}"
	StrCmp $R0 1 0 next${UNSECTION_ID}
	!insertmacro SelectSection "${UNSECTION_ID}"
	GoTo done${UNSECTION_ID}
next${UNSECTION_ID}:
	!insertmacro UnselectSection "${UNSECTION_ID}"
done${UNSECTION_ID}:
	Pop $R0
!macroend

# Uninstaller sections.
Section /o -un.Main UNSEC0000
	!include  "uninstalledFiles.nsh"
	DeleteRegValue HKLM "${REGKEY}\Components" Main
SectionEnd

Section -un.post UNSEC0001
	DeleteRegKey HKLM "SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\${APPLICATION}"
	Delete /REBOOTOK "$DESKTOP\${APPLICATION}.lnk"
	Delete /REBOOTOK "$SMPROGRAMS\$StartMenuGroup\${APPLICATION}.lnk"
	Delete /REBOOTOK "$SMPROGRAMS\$StartMenuGroup\Uninstall ${APPLICATION}.lnk"
	Delete /REBOOTOK $INSTDIR\Uninstall.exe
	DeleteRegValue HKLM "${REGKEY}" StartMenuGroup
	DeleteRegValue HKLM "${REGKEY}" Path
	DeleteRegKey /IfEmpty HKLM "${REGKEY}\Components"
	DeleteRegKey /IfEmpty HKLM "${REGKEY}"
	RmDir /REBOOTOK $SMPROGRAMS\$StartMenuGroup
    RmDir /REBOOTOK $SMPROGRAMS\${COMPANY}
	RmDir /REBOOTOK $INSTDIR
	Push $R0
	StrCpy $R0 $StartMenuGroup 1
	StrCmp $R0 ">" no_smgroup
no_smgroup:
	Pop $R0
SectionEnd

# Installer functions.
Function .onInit
	InitPluginsDir
	Push $R1
	File /oname=$PLUGINSDIR\spltmp.bmp ..\..\src\sibl_gui\resources\images\sIBL_GUI_Installer_Logo.bmp
	advsplash::show 1000 600 400 -1 $PLUGINSDIR\spltmp
	Pop $R1
	Pop $R1
FunctionEnd

# Uninstaller functions.
Function un.onInit
	ReadRegStr $INSTDIR HKLM "${REGKEY}" Path
	!insertmacro MUI_STARTMENU_GETFOLDER Application $StartMenuGroup
	!insertmacro SELECT_UNSECTION Main ${UNSEC0000}
FunctionEnd
