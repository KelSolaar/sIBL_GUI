echo ----------------------------------------------------------------
echo sIBL_GUI - Windows Build
echo ----------------------------------------------------------------

rem // Windows Build.
rmdir /S /Q "Y:\sIBL_GUI\releases\Windows\build\
rmdir /S /Q "Y:\sIBL_GUI\releases\Windows\dist\
python c:\pyinstaller\Makespec.py --noconsole --icon "Y:\sIBL_GUI\src\resources\Icon_Light_48.ico" Y:\sIBL_GUI\src\sIBL_GUI.py -o Y:\sIBL_GUI\releases\Windows
python c:\pyinstaller\Build.py Y:\sIBL_GUI\releases\Windows\sIBL_GUI.spec

rem // Windows Release.
rmdir /S /Q "Y:\sIBL_GUI\releases\Windows\sIBL_GUI"
xcopy /e /c /i /h /k /y "Y:\sIBL_GUI\releases\Windows\dist\sIBL_GUI" "Y:\sIBL_GUI\releases\Windows\sIBL_GUI"
rem // xcopy /c /y "Y:\sIBL_GUI\releases\Windows\dist\sIBL_GUI.exe" "Y:\sIBL_GUI\releases\Windows\sIBL_GUI\"
xcopy /c /y "Y:\sIBL_GUI\src\ui\sIBL_GUI.ui" "Y:\sIBL_GUI\releases\Windows\sIBL_GUI\ui\"
xcopy /c /y "Y:\sIBL_GUI\src\ui\sIBL_GUI_Layouts.rc" "Y:\sIBL_GUI\releases\Windows\sIBL_GUI\ui\"
xcopy /c /y "Y:\sIBL_GUI\src\ui\Windows_styleSheet.qss" "Y:\sIBL_GUI\releases\Windows\sIBL_GUI\ui\"
xcopy /c /y "Y:\sIBL_GUI\src\ui\Darwin_styleSheet.qss" "Y:\sIBL_GUI\releases\Windows\sIBL_GUI\ui\"
xcopy /c /y "Y:\sIBL_GUI\src\ui\Linux_styleSheet.qss" "Y:\sIBL_GUI\releases\Windows\sIBL_GUI\ui\"
xcopy /c /y "Y:\sIBL_GUI\src\resources\Icon_Light_48.ico" "Y:\sIBL_GUI\releases\Windows\sIBL_GUI\resources\"
xcopy /c /y "Y:\sIBL_GUI\src\resources\sIBL_GUI_SpashScreen.png" "Y:\sIBL_GUI\releases\Windows\sIBL_GUI\resources\"
xcopy /c /y "Y:\sIBL_GUI\src\resources\sIBL_GUI_Logo.png" "Y:\sIBL_GUI\releases\Windows\sIBL_GUI\resources\"
xcopy /c /y "Y:\sIBL_GUI\src\resources\Central_Widget.png" "Y:\sIBL_GUI\releases\Windows\sIBL_GUI\resources\"
xcopy /c /y "Y:\sIBL_GUI\src\resources\Central_Widget_Hover.png" "Y:\sIBL_GUI\releases\Windows\sIBL_GUI\resources\"
xcopy /c /y "Y:\sIBL_GUI\src\resources\Central_Widget_Active.png" "Y:\sIBL_GUI\releases\Windows\sIBL_GUI\resources\"
xcopy /c /y "Y:\sIBL_GUI\src\resources\Layout.png" "Y:\sIBL_GUI\releases\Windows\sIBL_GUI\resources\"
xcopy /c /y "Y:\sIBL_GUI\src\resources\Layout_Hover.png" "Y:\sIBL_GUI\releases\Windows\sIBL_GUI\resources\"
xcopy /c /y "Y:\sIBL_GUI\src\resources\Layout_Active.png" "Y:\sIBL_GUI\releases\Windows\sIBL_GUI\resources\"
xcopy /c /y "Y:\sIBL_GUI\src\resources\Miscellaneous.png" "Y:\sIBL_GUI\releases\Windows\sIBL_GUI\resources\"
xcopy /c /y "Y:\sIBL_GUI\src\resources\Miscellaneous_Hover.png" "Y:\sIBL_GUI\releases\Windows\sIBL_GUI\resources\"
xcopy /c /y "Y:\sIBL_GUI\src\resources\Miscellaneous_Active.png" "Y:\sIBL_GUI\releases\Windows\sIBL_GUI\resources\"
xcopy /c /y "Y:\sIBL_GUI\src\resources\Library.png" "Y:\sIBL_GUI\releases\Windows\sIBL_GUI\resources\"
xcopy /c /y "Y:\sIBL_GUI\src\resources\Library_Hover.png" "Y:\sIBL_GUI\releases\Windows\sIBL_GUI\resources\"
xcopy /c /y "Y:\sIBL_GUI\src\resources\Library_Active.png" "Y:\sIBL_GUI\releases\Windows\sIBL_GUI\resources\"
xcopy /c /y "Y:\sIBL_GUI\src\resources\Export.png" "Y:\sIBL_GUI\releases\Windows\sIBL_GUI\resources\"
xcopy /c /y "Y:\sIBL_GUI\src\resources\Export_Hover.png" "Y:\sIBL_GUI\releases\Windows\sIBL_GUI\resources\"
xcopy /c /y "Y:\sIBL_GUI\src\resources\Export_Active.png" "Y:\sIBL_GUI\releases\Windows\sIBL_GUI\resources\"
xcopy /c /y "Y:\sIBL_GUI\src\resources\Preferences.png" "Y:\sIBL_GUI\releases\Windows\sIBL_GUI\resources\"
xcopy /c /y "Y:\sIBL_GUI\src\resources\Preferences_Hover.png" "Y:\sIBL_GUI\releases\Windows\sIBL_GUI\resources\"
xcopy /c /y "Y:\sIBL_GUI\src\resources\Preferences_Active.png" "Y:\sIBL_GUI\releases\Windows\sIBL_GUI\resources\"
xcopy /c /y "Y:\sIBL_GUI\src\resources\Toolbar.png" "Y:\sIBL_GUI\releases\Windows\sIBL_GUI\resources\"
xcopy /e /c /i /h /k /y "Y:\sIBL_GUI\src\templates" "Y:\sIBL_GUI\releases\Windows\sIBL_GUI\templates"
xcopy /e /c /i /h /k /y "Y:\sIBL_GUI\src\components" "Y:\sIBL_GUI\releases\Windows\sIBL_GUI\components"

rem \\ Templates Textile Files Cleanup.
rem \\ XSI_MR_Standard Textile Template Documentation Removal.
del "Y:\sIBL_GUI\releases\Windows\sIBL_GUI\templates\XSI\XSI_MR_Standard\help\XSI_MR_Standard Template Manual"

rem \\ Softimage_MR_Standard Textile Template Documentation Removal.
del "Y:\sIBL_GUI\releases\Windows\sIBL_GUI\templates\Softimage\Softimage_MR_Standard\help\Softimage_MR_Standard Template Manual"

rem \\ Maya_MR_Standard Textile Template Documentation Removal.
del "Y:\sIBL_GUI\releases\Windows\sIBL_GUI\templates\Maya\Maya_MR_Standard\help\Maya_MR_Standard Template Manual"

rem \\ Maya_RfM_Standard Textile Template Documentation Removal.
del "Y:\sIBL_GUI\releases\Windows\sIBL_GUI\templates\Maya\Maya_RfM_Standard\help\Maya_RfM_Standard Template Manual"

rem \\ Maya_Turtle_Standard Textile Template Documentation Removal.
del "Y:\sIBL_GUI\releases\Windows\sIBL_GUI\templates\Maya\Maya_Turtle_Standard\help\Maya_Turtle_Standard Template Manual"

rem \\ Maya_VRay_Dome_Light Textile Template Documentation Removal.
del "Y:\sIBL_GUI\releases\Windows\sIBL_GUI\templates\Maya\Maya_VRay_Dome_Light\help\Maya_VRay_Dome_Light Template Manual"

rem \\ Maya_VRay_Standard Textile Template Documentation Removal.
del "Y:\sIBL_GUI\releases\Windows\sIBL_GUI\templates\Maya\Maya_VRay_Standard\help\Maya_VRay_Standard Template Manual"

rem \\ 3dsMax_MR_Standard Textile Template Documentation Removal.
del "Y:\sIBL_GUI\releases\Windows\sIBL_GUI\templates\3dsMax\3dsMax_MR_Standard\help\3dsMax_MR_Standard Template Manual"

rem \\ 3dsMax_Scanline_Standard Textile Template Documentation Removal.
del "Y:\sIBL_GUI\releases\Windows\sIBL_GUI\templates\3dsMax\3dsMax_Scanline_Standard\help\3dsMax_Scanline_Standard Template Manual"

rem \\ 3dsMax_VRay_Standard Textile Template Documentation Removal.
del "Y:\sIBL_GUI\releases\Windows\sIBL_GUI\templates\3dsMax\3dsMax_VRay_Standard\help\3dsMax_VRay_Standard Template Manual"

rem // Windows Release .DS_Store / .pyc Cleanup.
python "Y:\sIBL_GUI\utilities\sIBL_GUI_recursiveRemove.py" Y:\sIBL_GUI\releases\Windows\sIBL_GUI .pyc
python "Y:\sIBL_GUI\utilities\sIBL_GUI_recursiveRemove.py" Y:\sIBL_GUI\releases\Windows\sIBL_GUI .pyo
python "Y:\sIBL_GUI\utilities\sIBL_GUI_recursiveRemove.py" Y:\sIBL_GUI\releases\Windows\sIBL_GUI .DS_Store
python "Y:\sIBL_GUI\utilities\sIBL_GUI_recursiveRemove.py" Y:\sIBL_GUI\releases\Windows\sIBL_GUI Thumbs.db
