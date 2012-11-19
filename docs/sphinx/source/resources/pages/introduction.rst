_`Introduction`
===============

| **sIBL_GUI** is an open source lighting assistant making the Image Based Lighting process easier and straight forward through the use of sIbl files (*.Ibl*).
| What is sIBL? It’s a short for *Smart IBL*, a standard describing all informations and files needed to provide a fast and easy Image Based Lighting Setup in the 3d package of your choice.

More detailed informations are available here: http://www.smartibl.com

.. raw:: html

   <br/>

_`Donations`
------------

With *sIBL_GUI 4* release I decided to accept donations, so if you think the application is worth something you can use the following `Paypal <https://www.paypal.com/>`_ button:

.. raw:: html

	<form action="https://www.paypal.com/cgi-bin/webscr" method="post">
	<input type="hidden" name="cmd" value="_s-xclick">
	<input type="hidden" name="encrypted" value="-----BEGIN PKCS7-----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-----END PKCS7-----">
	<input type="image" src="http://kelsolaar.hdrlabs.com/sIBL_GUI/Support/Pictures/Make_A_Donation.png" border="0" name="submit" alt="PayPal — The safer, easier way to pay online.">
	<img alt="" border="0" src="https://www.paypalobjects.com/fr_FR/i/scr/pixel.gif" width="1" height="1">
	</form>

.. raw:: html

   <br/>

