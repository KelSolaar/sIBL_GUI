#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**ibl_sets_scanner.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines the :class:`IblSetsScanner` Component Interface class.

**Others:**

"""

from __future__ import unicode_literals

from PyQt4.QtGui import QMessageBox

import foundations.exceptions
import foundations.namespace
import foundations.verbose
import sibl_gui.components.core.database.operations
import umbra.engine
import umbra.ui.widgets.message_box as message_box
from manager.QObject_component import QObjectComponent
from sibl_gui.components.addons.ibl_sets_scanner.workers import IblSetsScanner_worker

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "IblSetsScanner"]

LOGGER = foundations.verbose.install_logger()

class IblSetsScanner(QObjectComponent):
	"""
	| Defines the :mod:`sibl_gui.components.addons.ibl_sets_scanner.ibl_sets_scanner` Component Interface class.
	| It instantiates the :class:`IblSetsScanner` class on Application startup which will gather new Ibl Sets
		from Database registered directories parents.
	"""

	def __init__(self, parent=None, name=None, *args, **kwargs):
		"""
		Initializes the class.

		:param parent: Object parent.
		:type parent: QObject
		:param name: Component name.
		:type name: unicode
		:param \*args: Arguments.
		:type \*args: \*
		:param \*\*kwargs: Keywords arguments.
		:type \*\*kwargs: \*\*
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		QObjectComponent.__init__(self, parent, name, *args, **kwargs)

		# --- Setting class attributes. ---
		self.deactivatable = True

		self.__engine = None

		self.__collections_outliner = None
		self.__ibl_sets_outliner = None

		self.__ibl_sets_scanner_worker_thread = None

	@property
	def engine(self):
		"""
		Property for **self.__engine** attribute.

		:return: self.__engine.
		:rtype: QObject
		"""

		return self.__engine

	@engine.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def engine(self, value):
		"""
		Setter for **self.__engine** attribute.

		:param value: Attribute value.
		:type value: QObject
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "engine"))

	@engine.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def engine(self):
		"""
		Deleter for **self.__engine** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "engine"))

	@property
	def collections_outliner(self):
		"""
		Property for **self.__collections_outliner** attribute.

		:return: self.__collections_outliner.
		:rtype: QWidget
		"""

		return self.__collections_outliner

	@collections_outliner.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def collections_outliner(self, value):
		"""
		Setter for **self.__collections_outliner** attribute.

		:param value: Attribute value.
		:type value: QWidget
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "collections_outliner"))

	@collections_outliner.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def collections_outliner(self):
		"""
		Deleter for **self.__collections_outliner** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "collections_outliner"))

	@property
	def ibl_sets_outliner(self):
		"""
		Property for **self.__ibl_sets_outliner** attribute.

		:return: self.__ibl_sets_outliner.
		:rtype: QWidget
		"""

		return self.__ibl_sets_outliner

	@ibl_sets_outliner.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def ibl_sets_outliner(self, value):
		"""
		Setter for **self.__ibl_sets_outliner** attribute.

		:param value: Attribute value.
		:type value: QWidget
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "ibl_sets_outliner"))

	@ibl_sets_outliner.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def ibl_sets_outliner(self):
		"""
		Deleter for **self.__ibl_sets_outliner** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "ibl_sets_outliner"))

	@property
	def ibl_sets_scanner_worker_thread(self):
		"""
		Property for **self.__ibl_sets_scanner_worker_thread** attribute.

		:return: self.__ibl_sets_scanner_worker_thread.
		:rtype: QThread
		"""

		return self.__ibl_sets_scanner_worker_thread

	@ibl_sets_scanner_worker_thread.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def ibl_sets_scanner_worker_thread(self, value):
		"""
		Setter for **self.__ibl_sets_scanner_worker_thread** attribute.

		:param value: Attribute value.
		:type value: QThread
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "ibl_sets_scanner_worker_thread"))

	@ibl_sets_scanner_worker_thread.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def ibl_sets_scanner_worker_thread(self):
		"""
		Deleter for **self.__ibl_sets_scanner_worker_thread** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "ibl_sets_scanner_worker_thread"))

	def activate(self, engine):
		"""
		Activates the Component.

		:param engine: Engine to attach the Component to.
		:type engine: QObject
		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Activating '{0}' Component.".format(self.__class__.__name__))

		self.__engine = engine

		self.__collections_outliner = self.__engine.components_manager["core.collections_outliner"]
		self.__ibl_sets_outliner = self.__engine.components_manager["core.ibl_sets_outliner"]

		self.activated = True
		return True

	def deactivate(self):
		"""
		Deactivates the Component.

		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Deactivating '{0}' Component.".format(self.__class__.__name__))

		self.__engine = None

		self.__collections_outliner = None
		self.__ibl_sets_outliner = None

		self.activated = False
		return True

	def initialize(self):
		"""
		Initializes the Component.

		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Initializing '{0}' Component.".format(self.__class__.__name__))

		self.__ibl_sets_scanner_worker_thread = IblSetsScanner_worker(self)
		self.__engine.worker_threads.append(self.__ibl_sets_scanner_worker_thread)

		if not self.__engine.parameters.database_read_only:
			if not self.__engine.parameters.deactivate_worker_threads:
				# Signals / Slots.
				self.__ibl_sets_scanner_worker_thread.ibl_sets_retrieved.connect(self.__ibl_sets_scanner_worker_thread__ibl_sets_retrieved)
			else:
				LOGGER.info("{0} | Ibl Sets scanning capabilities deactivated by '{1}' command line parameter value!".format(
				self.__class__.__name__, "deactivate_worker_threads"))
		else:
			LOGGER.info("{0} | Ibl Sets scanning capabilities deactivated by '{1}' command line parameter value!".format(
			self.__class__.__name__, "database_read_only"))

		self.initialized = True
		return True

	def uninitialize(self):
		"""
		Uninitializes the Component.

		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Uninitializing '{0}' Component.".format(self.__class__.__name__))

		if not self.__engine.parameters.database_read_only:
			if not self.__engine.parameters.deactivate_worker_threads:
				# Signals / Slots.
				not self.__engine.parameters.database_read_only and \
				self.__ibl_sets_scanner_worker_thread.ibl_sets_retrieved.disconnect(
				self.__ibl_sets_scanner_worker_thread__ibl_sets_retrieved)

		self.__engine.worker_threads.remove(self.__ibl_sets_scanner_worker_thread)
		self.__ibl_sets_scanner_worker_thread = None

		self.initialized = False
		return True

	def on_startup(self):
		"""
		Defines the slot triggered on Framework startup.

		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Calling '{0}' Component Framework 'on_startup' method.".format(self.__class__.__name__))

		not self.__engine.parameters.database_read_only and \
		not self.__engine.parameters.deactivate_worker_threads and self.__ibl_sets_scanner_worker_thread.start()
		return True

	@umbra.engine.encapsulate_processing
	def __ibl_sets_scanner_worker_thread__ibl_sets_retrieved(self, ibl_sets):
		"""
		Defines the slot triggered by **IblSetsScanner_worker** when the Database has changed.

		:param ibl_sets: Retrieve Ibl Sets.
		:type ibl_sets: dict
		"""

		if message_box.message_box("Question", "Question",
		"One or more neighbor Ibl Sets have been found! Would you like to add that content: '{0}' to the Database?".format(
		", ".join(map(foundations.strings.get_splitext_basename, ibl_sets))),
		 buttons=QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
			self.__engine.start_processing("Adding Retrieved Ibl Sets ...", len(ibl_sets))
			for path in ibl_sets:
				ibl_set = foundations.strings.get_splitext_basename(path)
				LOGGER.info("{0} | Adding '{1}' Ibl Set to the Database!".format(self.__class__.__name__, ibl_set))
				if not sibl_gui.components.core.database.operations.add_ibl_set(
				ibl_set, path, self.__collections_outliner.get_collection_id(self.__collections_outliner.default_collection)):
					LOGGER.error("!> {0} | Exception raised while adding '{1}' Ibl Set to the Database!".format(
					self.__class__.__name__, ibl_set))
				self.__engine.step_processing()
			self.__engine.stop_processing()

			self.__ibl_sets_outliner.refresh_nodes.emit()
