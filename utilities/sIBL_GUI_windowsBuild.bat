echo ----------------------------------------------------------------
echo sIBL_GUI - Windows - Build
echo ----------------------------------------------------------------

rem // Windows Build.
rmdir /S /Q "Z:\sIBL_GUI\releases\Windows\build\
rmdir /S /Q "Z:\sIBL_GUI\releases\Windows\dist\
python c:\pyinstaller\Makespec.py --noconsole --icon "Z:\sIBL_GUI\src\resources\Icon_Light_48.ico" Z:\sIBL_GUI\src\sIBL_GUI.py -o Z:\sIBL_GUI\releases\Windows
python c:\pyinstaller\Build.py Z:\sIBL_GUI\releases\Windows\sIBL_GUI.spec

rem // Windows Release.
rmdir /S /Q "Z:\sIBL_GUI\releases\Windows\sIBL_GUI"
xcopy /e /c /i /h /k /y "Z:\sIBL_GUI\releases\Windows\dist\sIBL_GUI" "Z:\sIBL_GUI\releases\Windows\sIBL_GUI"
rem // xcopy /c /y "Z:\sIBL_GUI\releases\Windows\dist\sIBL_GUI.exe" "Z:\sIBL_GUI\releases\Windows\sIBL_GUI\"
xcopy /c /y "Z:\sIBL_GUI\src\ui\sIBL_GUI.ui" "Z:\sIBL_GUI\releases\Windows\sIBL_GUI\ui\"
xcopy /c /y "Z:\sIBL_GUI\src\ui\sIBL_GUI_Layouts.rc" "Z:\sIBL_GUI\releases\Windows\sIBL_GUI\ui\"
xcopy /c /y "Z:\sIBL_GUI\src\ui\Windows_styleSheet.qss" "Z:\sIBL_GUI\releases\Windows\sIBL_GUI\ui\"
xcopy /c /y "Z:\sIBL_GUI\src\ui\Darwin_styleSheet.qss" "Z:\sIBL_GUI\releases\Windows\sIBL_GUI\ui\"
xcopy /c /y "Z:\sIBL_GUI\src\ui\Linux_styleSheet.qss" "Z:\sIBL_GUI\releases\Windows\sIBL_GUI\ui\"
xcopy /c /y "Z:\sIBL_GUI\src\resources\Icon_Light_48.ico" "Z:\sIBL_GUI\releases\Windows\sIBL_GUI\resources\"
xcopy /c /y "Z:\sIBL_GUI\src\resources\sIBL_GUI_SpashScreen.png" "Z:\sIBL_GUI\releases\Windows\sIBL_GUI\resources\"
xcopy /c /y "Z:\sIBL_GUI\src\resources\sIBL_GUI_Logo.png" "Z:\sIBL_GUI\releases\Windows\sIBL_GUI\resources\"
xcopy /c /y "Z:\sIBL_GUI\src\resources\Central_Widget.png" "Z:\sIBL_GUI\releases\Windows\sIBL_GUI\resources\"
xcopy /c /y "Z:\sIBL_GUI\src\resources\Central_Widget_Hover.png" "Z:\sIBL_GUI\releases\Windows\sIBL_GUI\resources\"
xcopy /c /y "Z:\sIBL_GUI\src\resources\Central_Widget_Active.png" "Z:\sIBL_GUI\releases\Windows\sIBL_GUI\resources\"
xcopy /c /y "Z:\sIBL_GUI\src\resources\Layout.png" "Z:\sIBL_GUI\releases\Windows\sIBL_GUI\resources\"
xcopy /c /y "Z:\sIBL_GUI\src\resources\Layout_Hover.png" "Z:\sIBL_GUI\releases\Windows\sIBL_GUI\resources\"
xcopy /c /y "Z:\sIBL_GUI\src\resources\Layout_Active.png" "Z:\sIBL_GUI\releases\Windows\sIBL_GUI\resources\"
xcopy /c /y "Z:\sIBL_GUI\src\resources\Miscellaneous.png" "Z:\sIBL_GUI\releases\Windows\sIBL_GUI\resources\"
xcopy /c /y "Z:\sIBL_GUI\src\resources\Miscellaneous_Hover.png" "Z:\sIBL_GUI\releases\Windows\sIBL_GUI\resources\"
xcopy /c /y "Z:\sIBL_GUI\src\resources\Miscellaneous_Active.png" "Z:\sIBL_GUI\releases\Windows\sIBL_GUI\resources\"
xcopy /c /y "Z:\sIBL_GUI\src\resources\Library.png" "Z:\sIBL_GUI\releases\Windows\sIBL_GUI\resources\"
xcopy /c /y "Z:\sIBL_GUI\src\resources\Library_Hover.png" "Z:\sIBL_GUI\releases\Windows\sIBL_GUI\resources\"
xcopy /c /y "Z:\sIBL_GUI\src\resources\Library_Active.png" "Z:\sIBL_GUI\releases\Windows\sIBL_GUI\resources\"
xcopy /c /y "Z:\sIBL_GUI\src\resources\Export.png" "Z:\sIBL_GUI\releases\Windows\sIBL_GUI\resources\"
xcopy /c /y "Z:\sIBL_GUI\src\resources\Export_Hover.png" "Z:\sIBL_GUI\releases\Windows\sIBL_GUI\resources\"
xcopy /c /y "Z:\sIBL_GUI\src\resources\Export_Active.png" "Z:\sIBL_GUI\releases\Windows\sIBL_GUI\resources\"
xcopy /c /y "Z:\sIBL_GUI\src\resources\Preferences.png" "Z:\sIBL_GUI\releases\Windows\sIBL_GUI\resources\"
xcopy /c /y "Z:\sIBL_GUI\src\resources\Preferences_Hover.png" "Z:\sIBL_GUI\releases\Windows\sIBL_GUI\resources\"
xcopy /c /y "Z:\sIBL_GUI\src\resources\Preferences_Active.png" "Z:\sIBL_GUI\releases\Windows\sIBL_GUI\resources\"
xcopy /c /y "Z:\sIBL_GUI\src\resources\Toolbar.png" "Z:\sIBL_GUI\releases\Windows\sIBL_GUI\resources\"
xcopy /e /c /i /h /k /y "Z:\sIBL_GUI\src\templates" "Z:\sIBL_GUI\releases\Windows\sIBL_GUI\templates"
xcopy /e /c /i /h /k /y "Z:\sIBL_GUI\src\components" "Z:\sIBL_GUI\releases\Windows\sIBL_GUI\components"

rem \\ Templates Textile Files Cleanup.
rem \\ XSI_MR_Standard Textile Template Documentation Removal.
del "Z:\sIBL_GUI\releases\Windows\sIBL_GUI\templates\XSI\XSI_MR_Standard\help\XSI_MR_Standard Template Manual"

rem \\ Softimage_MR_Standard Textile Template Documentation Removal.
del "Z:\sIBL_GUI\releases\Windows\sIBL_GUI\templates\Softimage\Softimage_MR_Standard\help\Softimage_MR_Standard Template Manual"

rem \\ Maya_MR_Standard Textile Template Documentation Removal.
del "Z:\sIBL_GUI\releases\Windows\sIBL_GUI\templates\Maya\Maya_MR_Standard\help\Maya_MR_Standard Template Manual"

rem \\ Maya_RfM_Standard Textile Template Documentation Removal.
del "Z:\sIBL_GUI\releases\Windows\sIBL_GUI\templates\Maya\Maya_RfM_Standard\help\Maya_RfM_Standard Template Manual"

rem \\ Maya_Turtle_Standard Textile Template Documentation Removal.
del "Z:\sIBL_GUI\releases\Windows\sIBL_GUI\templates\Maya\Maya_Turtle_Standard\help\Maya_Turtle_Standard Template Manual"

rem \\ Maya_VRay_Dome_Light Textile Template Documentation Removal.
del "Z:\sIBL_GUI\releases\Windows\sIBL_GUI\templates\Maya\Maya_VRay_Dome_Light\help\Maya_VRay_Dome_Light Template Manual"

rem \\ Maya_VRay_Standard Textile Template Documentation Removal.
del "Z:\sIBL_GUI\releases\Windows\sIBL_GUI\templates\Maya\Maya_VRay_Standard\help\Maya_VRay_Standard Template Manual"

rem \\ 3dsMax_MR_Standard Textile Template Documentation Removal.
del "Z:\sIBL_GUI\releases\Windows\sIBL_GUI\templates\3dsMax\3dsMax_MR_Standard\help\3dsMax_MR_Standard Template Manual"

rem \\ 3dsMax_Scanline_Standard Textile Template Documentation Removal.
del "Z:\sIBL_GUI\releases\Windows\sIBL_GUI\templates\3dsMax\3dsMax_Scanline_Standard\help\3dsMax_Scanline_Standard Template Manual"

rem \\ 3dsMax_VRay_Standard Textile Template Documentation Removal.
del "Z:\sIBL_GUI\releases\Windows\sIBL_GUI\templates\3dsMax\3dsMax_VRay_Standard\help\3dsMax_VRay_Standard Template Manual"

rem // Windows Release .DS_Store / .pyc Cleanup.
python "Z:\sIBL_GUI\utilities\sIBL_GUI_recursiveRemove.py" Z:\sIBL_GUI\releases\Windows\sIBL_GUI .pyc
python "Z:\sIBL_GUI\utilities\sIBL_GUI_recursiveRemove.py" Z:\sIBL_GUI\releases\Windows\sIBL_GUI .pyo
python "Z:\sIBL_GUI\utilities\sIBL_GUI_recursiveRemove.py" Z:\sIBL_GUI\releases\Windows\sIBL_GUI .DS_Store
python "Z:\sIBL_GUI\utilities\sIBL_GUI_recursiveRemove.py" Z:\sIBL_GUI\releases\Windows\sIBL_GUI Thumbs.db
