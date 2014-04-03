_`foundations.exceptions`
=========================

.. automodule:: foundations.exceptions

Module Attributes
-----------------

.. attribute:: foundations.exceptions.LOGGER

.. attribute:: foundations.exceptions.EXCEPTIONS_FRAME_SYMBOL

Functions
---------

.. autofunction:: getInnerMostFrame

.. autofunction:: extractStack

.. autofunction:: extractArguments

.. autofunction:: extractLocals

.. autofunction:: extractException

.. autofunction:: formatException

.. autofunction:: formatReport

.. autofunction:: baseExceptionHandler

.. autofunction:: installExceptionHandler

.. autofunction:: uninstallExceptionHandler

.. autofunction:: handleExceptions

Classes
-------

.. autoclass:: AbstractError
	:show-inheritance:
	:members:

.. autoclass:: ExecutionError
	:show-inheritance:
	:members:

.. autoclass:: BreakIteration
	:show-inheritance:
	:members:

.. autoclass:: AbstractParsingError
	:show-inheritance:
	:members:

.. autoclass:: FileStructureParsingError
	:show-inheritance:
	:members:

.. autoclass:: AttributeStructureParsingError
	:show-inheritance:
	:members:

.. autoclass:: AbstractIOError
	:show-inheritance:
	:members:

.. autoclass:: FileReadError
	:show-inheritance:
	:members:

.. autoclass:: FileWriteError
	:show-inheritance:
	:members:

.. autoclass:: UrlReadError
	:show-inheritance:
	:members:

.. autoclass:: UrlWriteError
	:show-inheritance:
	:members:

.. autoclass:: DirectoryCreationError
	:show-inheritance:
	:members:

.. autoclass:: PathCopyError
	:show-inheritance:
	:members:

.. autoclass:: PathRemoveError
	:show-inheritance:
	:members:

.. autoclass:: AbstractOsError
	:show-inheritance:
	:members:

.. autoclass:: PathExistsError
	:show-inheritance:
	:members:

.. autoclass:: DirectoryExistsError
	:show-inheritance:
	:members:

.. autoclass:: FileExistsError
	:show-inheritance:
	:members:

.. autoclass:: AbstractObjectError
	:show-inheritance:
	:members:

.. autoclass:: ObjectTypeError
	:show-inheritance:
	:members:

.. autoclass:: ObjectExistsError
	:show-inheritance:
	:members:

.. autoclass:: AbstractUserError
	:show-inheritance:
	:members:

.. autoclass:: ProgrammingError
	:show-inheritance:
	:members:

.. autoclass:: UserError
	:show-inheritance:
	:members:

.. autoclass:: AbstractNodeError
	:show-inheritance:
	:members:

.. autoclass:: NodeAttributeTypeError
	:show-inheritance:
	:members:

.. autoclass:: NodeAttributeExistsError
	:show-inheritance:
	:members:

.. autoclass:: AbstractLibraryError
	:show-inheritance:
	:members:

.. autoclass:: LibraryInstantiationError
	:show-inheritance:
	:members:

.. autoclass:: LibraryInitializationError
	:show-inheritance:
	:members:

.. autoclass:: LibraryExecutionError
	:show-inheritance:
	:members:

.. autoclass:: AbstractServerError
	:show-inheritance:
	:members:

.. autoclass:: ServerOperationError
	:show-inheritance:
	:members:

.. autoclass:: AnsiEscapeCodeExistsError
	:show-inheritance:
	:members:

