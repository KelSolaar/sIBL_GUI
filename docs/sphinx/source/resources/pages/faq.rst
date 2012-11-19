Faq
===

The following questions are answered by **sIBL_GUI** developer Thomas Mansencal and don't necessarily reflect other HDRLabs developer opinions and thoughts.

.. raw:: html

   <br/>

_`General Questions`
-------------------------------------

.. raw:: html

   <br/>


_`Overall`
^^^^^^^^^^

::

      Is sIBL_GUI Open Source?

| Yes **sIBL_GUI** is Open Source and licensed under: `GNU GPL V3 license <http://www.gnu.org/copyleft/gpl.html>`_
| You can grab the source code from: `sIBL_GUI Git Repository on GitHub <http://kelsolaar.github.com/sIBL_GUI/>`_

.. raw:: html

   <br/>

::

      I'm using sIBL_GUI 1 / 2 / 3, is there still support for it?

No, **sIBL_GUI** is developed by one person on his free time, cross version support can't be achieved. Any new version deprecate the previous one.

.. raw:: html

   <br/>

::

      Can I pay to help me making sIBL_GUI run on my computer?

| No, since I cannot provide a real quality support (Although I'm doing my best), I don't want money, only happy people doing nice renders with HDRLabs team stuff.
| If you are having issues, it's my duty to make my best solving them.
| However if you feel **sIBL_GUI** is worth something I'm receiving donations: http://kelsolaar.hdrlabs.com/sIBL_GUI/Support/Donations/Make_A_Donation.html

.. raw:: html

   <br/>

::

      Can I pay you to make a custom template?

No, same as above, however if you need a custom template, we can discuss of what can be done. Just remember that **sIBL_GUI** is done on my free time.

.. raw:: html

   <br/>

::

      Where are sIBL_GUI preferences stored?

-  C:\\Users\\$USER\\AppData\\Roaming\\HDRLabs\\sIBL_GUI\\$MAJOR_VERSION.$MINOR_VERSION on Windows 7
-  C:\\Documents and Settings\\$USER\\Application Data\\HDRLabs\\sIBL_GUI\\$MAJOR_VERSION.$MINOR_VERSION on Windows XP
-  /Users/$USER/Library/Preferences/HDRLabs/sIBL_GUI/$MAJOR_VERSION.$MINOR_VERSION on Mac Os X
-  /home/$USER/.HDRLabs/sIBL_GUI/$MAJOR_VERSION.$MINOR_VERSION on Linux

.. raw:: html

   <br/>

::

      I installed sIBL_GUI and its not starting, what can I do?

You need to launch **sIBL_GUI** into Debug verbose mode using the *-v 4* command line parameter and send me back the logging *sIBL_GUI_Logging.log* and *sIBL_GUI_Database.sqlite* database files.

.. raw:: html

   <br/>

::

      I'm having too many problems with sIBL_GUI x.x.x, are older versions still available?

-  `sIBL_GUI 1 <http://kelsolaar.hdrlabs.com/?dir=./sIBL_Framework/sIBL_GUI/Archives>`_
-  `sIBL_GUI 2 <http://kelsolaar.hdrlabs.com/?dir=./sIBL_Framework/sIBL_GUI/Archives>`_
-  `sIBL_GUI 3 <http://kelsolaar.hdrlabs.com/?dir=./sIBL_GUI/Repository/Builds>`_
-  `sIBL_GUI 4 <http://kelsolaar.hdrlabs.com/?dir=./sIBL_GUI/Repository/Builds>`_

.. raw:: html

   <br/>

::

      I thought Loader Scripts are obsolete now?

Please refer to the first post of this thread: http://www.hdrlabs.com/cgi-bin/forum/YaBB.pl?num=1271612492 to see the development status of the various loader script.

.. raw:: html

   <br/>

::

      Is there a difference between an Helper Script and a Loader Script?

Yes! *Helper Scripts* are additional scripts that help integrating **sIBL_GUI** into the target 3d package whereas *Loader Scripts* are native 3d package scripts enabling direct *Smart Ibl* support.
One confusion source is that I also call *Loader Scripts* the scripts **sIBL_GUI** generates.
Here is a link to the **sIBL_GUI** Helper Scripts: http://www.hdrlabs.com/cgi-bin/forum/YaBB.pl?num=1271609371/1#1

.. raw:: html

   <br/>

::

      Is it possible to move the user preferences directory into sIBL_GUI installation directory, like in sIBL_GUI 2?

Using the *-u / --userApplicationDatasDirectory* command line parameter, you can define where *sIBL_GUI 4* preferences are stored. You can easily pass **sIBL_GUI** installation folder to retrieve the portability of *sIBL_GUI 2*.

.. raw:: html

   <br/>

_`Rendering`
^^^^^^^^^^^^

::

      What is the shift between the viewport visual feedback sphere and the render image?

| When you render using an environment map, the image is "kind" of warped on an infinite radius sphere centered on the camera: http://www.pauldebevec.com/ReflectionMapping/. If you are way off the center of the viewport with a fairly small visual feedback, you'll encounter a shift.
| There are 2 solutions to counter this effect :

-  Constrain in position the visual feedBack to your render camera.
-  Increase the visual feedBack scale.

.. raw:: html

   <br/>

::

      Is it possible to use the three Smart Ibl maps without a Ray Switch Shader?

Yes you need to map each one on a different sphere and play with the different rays visibility of those spheres. Just remember than probing geometry will be slower than using a pure shading solution.

.. raw:: html

   <br/>

::

      Is it possible to share a common Database file between multiple computers?

**Shared Database Configuration**: http://kelsolaar.hdrlabs.com/sIBL_GUI/Support/Documentation/Api/../pages/usage.html#id4

.. raw:: html

   <br/>

_`Operating System Questions`
--------------------------------

.. raw:: html

   <br/>

_`Windows`
^^^^^^^^^^^^^^^^

::

      How do I launch sIBL_GUI with command line parameters?

Create or modify a *shortcut* to the executable, then append the parameters you want to use into the *target* field.

.. raw:: html

   <br/>

_`Mac Os X`
^^^^^^^^^^^^^^^^

::

      How do I launch sIBL_GUI with command line parameters?

Open a terminal then issue the following commands with the parameters you want to use:

      ``cd /Applications/sIBL_GUI\ 4.app/``

      ``./Contents/MacOS/sIBL_GUI``

.. raw:: html

   <br/>

_`3D Packages Questions`
--------------------------------

.. raw:: html

   <br/>

_`Autodesk Maya`
^^^^^^^^^^^^^^^^

::

      I'm getting that error: "LoaderScript | Socket connection error: '[Errno 10061] No connection could be made because the target machine actively refused it'!"

| **sIBL_GUI** is relying on Socket Connection to communicate with Autodesk Maya.
| You need to make Autodesk Maya listen to the port **sIBL_GUI** is using. You can do that using the **Autodesk Maya - Helper Script**: http://www.hdrlabs.com/cgi-bin/forum/YaBB.pl?num=1271609371/1#1 or executing the following lines into the script editor:

-  Autodesk Maya 2008 - 2012:
   
      ``commandPort -n "127.0.0.1:2048";``

-  Autodesk Maya 2010 - Windows Vista / 7 :
   
      ``commandPort -n "127.0.0.1:2048"; commandPort -n ":2048";``

.. raw:: html

   <br/>

::

      How do I open automatically the command port in Autodesk Maya?

Open your *userSetup.mel* in Autodesk Maya script folder (Or create the file if it doesn't exists) and append the following lines:

-  Autodesk Maya 2008 - 2012:
   
      ``commandPort -n ("127.0.0.1:"  + `optionVar -q "sIBL_GUI_commandPort"`);``

-  Autodesk Maya 2010 - Windows Vista / 7 :
   
      ``commandPort -n ("127.0.0.1:"  + `optionVar -q "sIBL_GUI_commandPort"`); commandPort -n (":" + `optionVar -q "sIBL_GUI_commandPort"`);``

.. raw:: html

   <br/>

::

      I have installed Autodesk Maya - Helper Script, what do I put in sIBL_GUI Executable Path field?

It's a convenient method to directly launch **sIBL_GUI** from within Autodesk Maya, just point to **sIBL_GUI** executable, then you can use the second shelf button to launch **sIBL_GUI**.
   
      ``/Applications/sIBL_GUI.app/Contents/MacOs/sIBL_GUI 4.app``

.. raw:: html

   <br/>

_`Autodesk Softimage`
^^^^^^^^^^^^^^^^^^^^^

::

      I'm getting that error: "LoaderScript | Socket connection error: '[Errno 10061] No connection could be made because the target machine actively refused it'!"

| **sIBL_GUI** is relying on Socket Connection to communicate with Autodesk Softimage.
| You need to make Autodesk Softimage listen to the port **sIBL_GUI** is using. You can do that using the *sIBL_GUI_XSI_Server Addon*:

sIBL_GUI_XSI_Server Addon ( Windows Only ):

-  `Nightly <http://kelsolaar.hdrlabs.com/?dir=./sIBL_GUI/Support/Softwares/XSI/sIBL_GUI_XSI_Server/Nightly>`_
-  `Stable <http://kelsolaar.hdrlabs.com/?dir=./sIBL_GUI/Support/Softwares/XSI/sIBL_GUI_XSI_Server/Stable>`_
-  `Archives <http://kelsolaar.hdrlabs.com/?dir=./sIBL_GUI/Support/Softwares/XSI/sIBL_GUI_XSI_Server/Archives>`_

.. raw:: html

   <br/>

::

      I'm getting that error: "' ERROR : 2424 - XSI failed to load a .NET plug-in. This error happens because the plug-in may have been compiled with a different version of XSI. Recompile the plug-in with the current version of XSI to fix the problem. ' <Plug-in: \\..\sIBL_GUI_XSI_Server\Application\Plugins\sIBL_GUI_XSI_Server.dll> ' <Current XSI version: X.X.XXX.X>"

You either:

-  Don't have the correct *sIBL_GUI_XSI_Server Addon* compiled for your version of Autodesk Softimage.
-  Didn't registered the *sIBL_GUI_XSI_Server.dll* file into the Windows GAC ( Global Assembly Cache ).

.. raw:: html

   <br/>

::

      How do I register the sIBL_GUI_XSI_Server.dll file into Windows Global Assembly Cache?

| You need to use a Microsoft .Net tool called *gacutil* available with the .Net Framework: `.Net Framework on Wikipedia <http://en.wikipedia.org/wiki/.NET_Framework>`_
| If you don't have the .Net Framework, you can get the gacutil executable alone here: `gacutil.rar <http://kelsolaar.hdrlabs.com/sIBL_Framework/XSI/sIBL_GUI_For_XSI/Others/gacutil.rar>`_

You will then need to issue a command like this in an Administrator elevated prompt:

      ``gacutil.exe /i C:\Addons\sIBL_GUI_XSI\Application\Plugins\sIBL_GUI_XSI_Server.dll``

There is also an alternative way without gacutil.exe, it has been tested on a few computers and seems to work: You just need to drag'n'drop the *sIBL_GUI_Server.dll* into Windows GAC folder (C:\\Windows\\assembly).

.. raw:: html

   <br/>

_`Autodesk 3ds Max`
^^^^^^^^^^^^^^^^^^^

::

      I'm getting that error: "LoaderScript | Win32 OLE server connection error: '(-2147221164, 'Class not registered', None, None)'!"

| **sIBL_GUI** is relying on a Win32 OLE Connection to communicate with Autodesk 3ds Max.
| You need to register Autodesk 3ds Max as an OLE Server and expose the communication class. The easiest way to do that is to use *Autodesk 3ds Max - Helper Script* and trigger the *Register OLE Server* button: http://www.hdrlabs.com/cgi-bin/forum/YaBB.pl?num=1271609371/1#1

Notice that you need to launch Autodesk 3ds Max as Administrator for that purpose.

.. raw:: html

   <br/>

::

      What is this error with Autodesk 3dsMax_MR_Standard Template: "sIBL_GUI | Mental Ray Productions Shaders are not available!"?

| Zap Anderson Production Shaders are hidden by default in Autodesk 3ds Max 2009 and 2010 since they were introduced a few versions ago.
| You need to edit the associated *production_max.mi* include file in Autodesk 3ds Max Mental Ray folder by commenting out those type of statements:

      ``"hidden"``

to

      ``# "hidden"``

Or after backuping the original one, you can directly use one of those already edited files: `Production Shaders Files <http://kelsolaar.hdrlabs.com/?dir=./sIBL_GUI/Support/Softwares/3dsMax/Others/Production%20Shader%20Files>`_

.. raw:: html

   <br/>

