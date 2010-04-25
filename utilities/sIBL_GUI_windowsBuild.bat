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
rem // xcopy /e /c /i /h /k /y "Y:\sIBL_GUI\src\Help" "Y:\sIBL_GUI\src\releases\Windows\sIBL_GUI\Help\"
rem // xcopy /e /c /i /h /k /y "Y:\sIBL_GUI\src\Templates" "Y:\sIBL_GUI\src\releases\Windows\sIBL_GUI\Templates"
rem // xcopy /e /c /i /h /k /y "Y:\sIBL_GUI\src\releases\Windows\Utilities\PyQt4" "Y:\sIBL_GUI\src\releases\Windows\sIBL_GUI\PyQt4"
rem // xcopy /c /y "Y:\sIBL_GUI\src\releases\Windows\Utilities\qt.conf" "Y:\sIBL_GUI\src\releases\Windows\sIBL_GUI\"
rem // xcopy /c /y "Y:\sIBL_GUI\src\Resources\Earth_Map.jpg" "Y:\sIBL_GUI\src\releases\Windows\sIBL_GUI\Resources\"

rem // Upx.
rem // upx "Y:\sIBL_GUI\src\releases\Windows\sIBL_GUI\sIBL_GUI.exe"
rem // upx "Y:\sIBL_GUI\src\releases\Windows\sIBL_GUI\sIBL_Framework.exe"
rem // upx "Y:\sIBL_GUI\src\releases\Windows\sIBL_GUI\w9xpopen.exe"
rem // upx "Y:\sIBL_GUI\src\releases\Windows\sIBL_GUI\python26.dll"
rem // upx "Y:\sIBL_GUI\src\releases\Windows\sIBL_GUI\pythoncom26.dll"
rem // upx "Y:\sIBL_GUI\src\releases\Windows\sIBL_GUI\pywintypes26.dll"
rem // upx "Y:\sIBL_GUI\src\releases\Windows\sIBL_GUI\QtCore4.dll"
rem // upx "Y:\sIBL_GUI\src\releases\Windows\sIBL_GUI\QtGui4.dll"

rem // Windows Release .DS_Store / .pyc Cleanup.
python "Y:\sIBL_GUI\utilities\sIBL_GUI_recursiveRemove.py" Y:\sIBL_GUI\releases\Windows\sIBL_GUI .pyc
python "Y:\sIBL_GUI\utilities\sIBL_GUI_recursiveRemove.py" Y:\sIBL_GUI\releases\Windows\sIBL_GUI .pyo
python "Y:\sIBL_GUI\utilities\sIBL_GUI_recursiveRemove.py" Y:\sIBL_GUI\releases\Windows\sIBL_GUI .DS_Store
python "Y:\sIBL_GUI\utilities\sIBL_GUI_recursiveRemove.py" Y:\sIBL_GUI\releases\Windows\sIBL_GUI Thumbs.db

rem // Windows XSI Release.
rem // rmdir /S /Q "Y:\sIBL_GUI_For_XSI\Addons\sIBL_GUI_For_XSI\Application\Plugins\sIBL_GUI_Windows\"
rem // xcopy /e /c /i /h /k /y "Y:\sIBL_GUI\src\releases\Windows\sIBL_GUI" "Y:\sIBL_GUI_For_XSI\Addons\sIBL_GUI_For_XSI\Application\Plugins\sIBL_GUI_Windows\"
rem // rmdir /S /Q "Y:\sIBL_GUI_For_XSI\Addons\sIBL_GUI_For_XSI\Application\Plugins\sIBL_GUI_Windows\Templates\3ds Max"
rem // rmdir /S /Q "Y:\sIBL_GUI_For_XSI\Addons\sIBL_GUI_For_XSI\Application\Plugins\sIBL_GUI_Windows\Templates\Maya"

rem // Windows XSI Release .DS_Store Cleanup.
rem // python "Y:\sIBL_GUI\src\utilities\KSL_RecursiveRemove.py" Y:\sIBL_GUI_For_XSI .DS_Store
rem // python "Y:\sIBL_GUI\src\utilities\KSL_RecursiveRemove.py" Y:\sIBL_GUI_For_XSI Thumbs.db
