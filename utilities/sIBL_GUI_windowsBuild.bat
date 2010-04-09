echo ----------------------------------------------------------------
echo sIBL_GUI - Windows Build
echo ----------------------------------------------------------------

rem // Windows Build.
rmdir /S /Q "Z:\sIBL_GUI\Releases\Windows\build\
rmdir /S /Q "Z:\sIBL_GUI\Releases\Windows\dist\
python c:\pyinstaller\Makespec.py -F --icon "Z:\sIBL_GUI\src\resources\Icon_Light_48.ico" Z:\sIBL_GUI\src\sIBL_GUI.py -o Z:\sIBL_GUI\Releases\Windows
python c:\pyinstaller\Build.py Z:\sIBL_GUI\Releases\Windows\sIBL_GUI.spec

rem // Windows Release.
rmdir /S /Q "Z:\sIBL_GUI\Releases\Windows\sIBL_GUI"
xcopy /c /y "Z:\sIBL_GUI\Releases\Windows\dist\sIBL_GUI.exe" "Z:\sIBL_GUI\Releases\Windows\sIBL_GUI\"
xcopy /c /y "Z:\sIBL_GUI\src\ui\sIBL_GUI.ui" "Z:\sIBL_GUI\Releases\Windows\sIBL_GUI\ui\"
xcopy /c /y "Z:\sIBL_GUI\src\resources\sIBL_GUI_SpashScreen.png" "Z:\sIBL_GUI\Releases\Windows\sIBL_GUI\resources\"
xcopy /c /y "Z:\sIBL_GUI\src\resources\sIBL_GUI_Logo.png" "Z:\sIBL_GUI\Releases\Windows\sIBL_GUI\resources\"
xcopy /c /y "Z:\sIBL_GUI\src\resources\sIBL_GUI_Layout.png" "Z:\sIBL_GUI\Releases\Windows\sIBL_GUI\resources\"
xcopy /c /y "Z:\sIBL_GUI\src\resources\sIBL_GUI_CentralWidget.png" "Z:\sIBL_GUI\Releases\Windows\sIBL_GUI\resources\"
xcopy /e /c /i /h /k /y "Z:\sIBL_GUI\src\components" "Z:\sIBL_GUI\Releases\Windows\sIBL_GUI\components"
rem // xcopy /e /c /i /h /k /y "Y:\sIBL_GUI\src\Help" "Y:\sIBL_GUI\src\Releases\Windows\sIBL_GUI\Help\"
rem // xcopy /e /c /i /h /k /y "Y:\sIBL_GUI\src\Templates" "Y:\sIBL_GUI\src\Releases\Windows\sIBL_GUI\Templates"
rem // xcopy /e /c /i /h /k /y "Y:\sIBL_GUI\src\Releases\Windows\Utilities\PyQt4" "Y:\sIBL_GUI\src\Releases\Windows\sIBL_GUI\PyQt4"
rem // xcopy /c /y "Y:\sIBL_GUI\src\Releases\Windows\Utilities\qt.conf" "Y:\sIBL_GUI\src\Releases\Windows\sIBL_GUI\"
rem // xcopy /c /y "Y:\sIBL_GUI\src\Resources\Earth_Map.jpg" "Y:\sIBL_GUI\src\Releases\Windows\sIBL_GUI\Resources\"

rem // Upx.
rem // upx "Y:\sIBL_GUI\src\Releases\Windows\sIBL_GUI\sIBL_GUI.exe"
rem // upx "Y:\sIBL_GUI\src\Releases\Windows\sIBL_GUI\sIBL_Framework.exe"
rem // upx "Y:\sIBL_GUI\src\Releases\Windows\sIBL_GUI\w9xpopen.exe"
rem // upx "Y:\sIBL_GUI\src\Releases\Windows\sIBL_GUI\python26.dll"
rem // upx "Y:\sIBL_GUI\src\Releases\Windows\sIBL_GUI\pythoncom26.dll"
rem // upx "Y:\sIBL_GUI\src\Releases\Windows\sIBL_GUI\pywintypes26.dll"
rem // upx "Y:\sIBL_GUI\src\Releases\Windows\sIBL_GUI\QtCore4.dll"
rem // upx "Y:\sIBL_GUI\src\Releases\Windows\sIBL_GUI\QtGui4.dll"

rem // Windows Release .DS_Store / .pyc Cleanup.
python "Z:\sIBL_GUI\External Tools\sIBL_GUI_recursiveRemove.py" Z:\sIBL_GUI\Releases\Windows\sIBL_GUI .pyc
python "Z:\sIBL_GUI\External Tools\sIBL_GUI_recursiveRemove.py" Z:\sIBL_GUI\Releases\Windows\sIBL_GUI .DS_Store
python "Z:\sIBL_GUI\External Tools\sIBL_GUI_recursiveRemove.py" Z:\sIBL_GUI\Releases\Windows\sIBL_GUI Thumbs.db

rem // Windows XSI Release.
rem // rmdir /S /Q "Y:\sIBL_GUI_For_XSI\Addons\sIBL_GUI_For_XSI\Application\Plugins\sIBL_GUI_Windows\"
rem // xcopy /e /c /i /h /k /y "Y:\sIBL_GUI\src\Releases\Windows\sIBL_GUI" "Y:\sIBL_GUI_For_XSI\Addons\sIBL_GUI_For_XSI\Application\Plugins\sIBL_GUI_Windows\"
rem // rmdir /S /Q "Y:\sIBL_GUI_For_XSI\Addons\sIBL_GUI_For_XSI\Application\Plugins\sIBL_GUI_Windows\Templates\3ds Max"
rem // rmdir /S /Q "Y:\sIBL_GUI_For_XSI\Addons\sIBL_GUI_For_XSI\Application\Plugins\sIBL_GUI_Windows\Templates\Maya"

rem // Windows XSI Release .DS_Store Cleanup.
rem // python "Y:\sIBL_GUI\src\External Tools\KSL_RecursiveRemove.py" Y:\sIBL_GUI_For_XSI .DS_Store
rem // python "Y:\sIBL_GUI\src\External Tools\KSL_RecursiveRemove.py" Y:\sIBL_GUI_For_XSI Thumbs.db
