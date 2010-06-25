#!/usr/bin/env python
# -*- coding: utf-8 -*-

#***********************************************************************************************
#
# Copyright (C) 2008 - 2010 - Thomas Mansencal - kelsolaar_fool@hotmail.com
#
#***********************************************************************************************
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
#***********************************************************************************************
#
# The Following Code Is Protected By GNU GPL V3 Licence.
#
#***********************************************************************************************
#
# If You Are A HDRI Ressources Vendor And Are Interested In Making Your Sets SmartIBL Compliant:
# Please Contact Us At HDRLabs :
# Christian Bloch - blochi@edenfx.com
# Thomas Mansencal - kelsolaar_fool@hotmail.com
#
#***********************************************************************************************

'''
************************************************************************************************
***	preview.py
***
***	Platform :
***		Windows, Linux, Mac Os X
***
***	Description :
***		Preview Component Module.
***
***	Others :
***
************************************************************************************************
'''

#***********************************************************************************************
#***	Python Begin
#***********************************************************************************************

#***********************************************************************************************
#***	External Imports
#***********************************************************************************************
import logging
import os
import sys
from PyQt4 import uic
from PyQt4.QtCore import *
from PyQt4.QtGui import *

#***********************************************************************************************
#***	Internal Imports
#***********************************************************************************************
import foundations.core as core
import foundations.exceptions
import ui.common
from globals.constants import Constants
from libraries.freeImage.freeImage import Image
from manager.uiComponent import UiComponent

#***********************************************************************************************
#***	Global Variables
#***********************************************************************************************
LOGGER = logging.getLogger( Constants.logger )

#***********************************************************************************************
#***	Module Classes And Definitions
#***********************************************************************************************
class ImagePreviewer( object ):
	'''
	This Is The ImagePreviewer Class.
	'''

	@core.executionTrace
	def __init__( self, container, imagePath ):
		'''
		This Method Initializes The Class.
		
		@param container: Container. ( Object )
		@param imagePath: Image Path. ( String )
		'''

		LOGGER.debug( "> Initializing '{0}()' Class.".format( self.__class__.__name__ ) )

		# --- Setting Class Attributes. ---
		self._container = container
		self._imagePath = None
		self.imagePath = imagePath

		self._signalsSlotsCenter = QObject()

		self._uiPath = "ui/Image_Previewer.ui"
		self._uiPath = os.path.join( os.path.dirname( core.getModule( self ).__file__ ), self._uiPath )

		self._ui = uic.loadUi( self._uiPath )
		if "." in sys.path :
			sys.path.remove( "." )

		self._pixmap = None
		self._graphicsPixmapItem = None

		self._graphicsView = QGraphicsView()
		self._graphicsScene = QGraphicsScene( self._graphicsView )
		self._graphicsSceneBackgroundColor = QColor( 128, 128, 128 )
		self._graphicsSceneMargin = 64
		self._graphicsSceneWidth = 8192
		self._graphicsSceneHeight = 6144
		self._minimumZoomFactor = 0.5
		self._maximumZoomFactor = 25
		self._wheelZoomFactor = 250.0
		self._keyZoomFactor = 1.20

		self.initializeUi()

		self._ui.show()

	#***************************************************************************************
	#***	Attributes Properties
	#***************************************************************************************
	@property
	def container( self ):
		'''
		This Method Is The Property For The _container Attribute.

		@return: self._container. ( QObject )
		'''

		return self._container

	@container.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def container( self, value ):
		'''
		This Method Is The Setter Method For The _container Attribute.

		@param value: Attribute Value. ( QObject )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "container" ) )

	@container.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def container( self ):
		'''
		This Method Is The Deleter Method For The _container Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "container" ) )

	@property
	def imagePath( self ):
		'''
		This Method Is The Property For The _imagePath Attribute.

		@return: self._imagePath. ( String )
		'''

		return self._imagePath

	@imagePath.setter
	@foundations.exceptions.exceptionsHandler( None, False, AssertionError )
	def imagePath( self, value ):
		'''
		This Method Is The Setter Method For The _imagePath Attribute.

		@param value: Attribute Value. ( String )
		'''

		if value :
			assert type( value ) in ( str, unicode, QString ), "'{0}' Attribute : '{1}' Type Is Not 'str', 'unicode' or 'QString' !".format( "imagePath", value )
			assert os.path.exists( value ), "'{0}' Attribute : '{1}' Image File Doesn't Exists !".format( "imagePath", value )
		self._imagePath = value

	@imagePath.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def imagePath( self ):
		'''
		This Method Is The Deleter Method For The _imagePath Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "imagePath" ) )

	@property
	def signalsSlotsCenter( self ):
		'''
		This Method Is The Property For The _signalsSlotsCenter Attribute.

		@return: self._signalsSlotsCenter. ( QObject )
		'''

		return self._signalsSlotsCenter

	@signalsSlotsCenter.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def signalsSlotsCenter( self, value ):
		'''
		This Method Is The Setter Method For The _signalsSlotsCenter Attribute.

		@param value: Attribute Value. ( QObject )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "signalsSlotsCenter" ) )

	@signalsSlotsCenter.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def signalsSlotsCenter( self ):
		'''
		This Method Is The Deleter Method For The _signalsSlotsCenter Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "signalsSlotsCenter" ) )

	@property
	def uiPath( self ):
		'''
		This Method Is The Property For The _uiPath Attribute.

		@return: self._uiPath. ( String )
		'''

		return self._uiPath

	@uiPath.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def uiPath( self, value ):
		'''
		This Method Is The Setter Method For The _uiPath Attribute.

		@param value: Attribute Value. ( String )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "uiPath" ) )

	@uiPath.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def uiPath( self ):
		'''
		This Method Is The Deleter Method For The _uiPath Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "uiPath" ) )

	@property
	def pixmap( self ):
		'''
		This Method Is The Property For The _pixmap Attribute.

		@return: self._pixmap. ( QPixmap )
		'''

		return self._pixmap

	@pixmap.setter
	@foundations.exceptions.exceptionsHandler( None, False, AssertionError )
	def pixmap( self, value ):
		'''
		This Method Is The Setter Method For The _pixmap Attribute.
		
		@param value: Attribute Value. ( QPixmap )
		'''

		if value :
			assert type( value ) is QPixmap, "'{0}' Attribute : '{1}' Type Is Not 'QPixmap' !".format( "pixmap", value )
		self._imagePath = value

	@pixmap.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def pixmap( self ):
		'''
		This Method Is The Deleter Method For The _pixmap Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "pixmap" ) )

	@property
	def graphicsPixmapItem( self ):
		'''
		This Method Is The Property For The _graphicsPixmapItem Attribute.

		@return: self._graphicsPixmapItem. ( QGraphicsPixmapItem )
		'''

		return self._graphicsPixmapItem

	@graphicsPixmapItem.setter
	@foundations.exceptions.exceptionsHandler( None, False, AssertionError )
	def graphicsPixmapItem( self, value ):
		'''
		This Method Is The Setter Method For The _graphicsPixmapItem Attribute.
		
		@param value: Attribute Value. ( QGraphicsPixmapItem )
		'''

		if value :
			assert type( value ) is QGraphicsPixmapItem, "'{0}' Attribute : '{1}' Type Is Not 'QGraphicsPixmapItem' !".format( "graphicsPixmapItem", value )
		self._graphicsPixmapItem = value

	@graphicsPixmapItem.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def graphicsPixmapItem( self ):
		'''
		This Method Is The Deleter Method For The _graphicsPixmapItem Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "graphicsPixmapItem" ) )

	@property
	def graphicsView( self ):
		'''
		This Method Is The Property For The _graphicsView Attribute.

		@return: self._graphicsView. ( QGraphicsView )
		'''

		return self._graphicsView

	@graphicsView.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def graphicsView( self, value ):
		'''
		This Method Is The Setter Method For The _graphicsView Attribute.
		
		@param value: Attribute Value. ( QGraphicsView )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "graphicsView" ) )

	@graphicsView.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def graphicsView( self ):
		'''
		This Method Is The Deleter Method For The _graphicsView Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "graphicsView" ) )

	@property
	def graphicsScene( self ):
		'''
		This Method Is The Property For The _graphicsScene Attribute.

		@return: self._graphicsScene. ( QGraphicsScene )
		'''

		return self._graphicsScene

	@graphicsScene.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def graphicsScene( self, value ):
		'''
		This Method Is The Setter Method For The _graphicsScene Attribute.
		
		@param value: Attribute Value. ( QGraphicsScene )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "graphicsScene" ) )

	@graphicsScene.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def graphicsScene( self ):
		'''
		This Method Is The Deleter Method For The _graphicsScene Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "graphicsScene" ) )

	@property
	def graphicsSceneBackgroundColor( self ):
		'''
		This Method Is The Property For The _graphicsSceneBackgroundColor Attribute.

		@return: self._graphicsSceneBackgroundColor. ( QColor )
		'''

		return self._graphicsSceneBackgroundColor

	@graphicsSceneBackgroundColor.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def graphicsSceneBackgroundColor( self, value ):
		'''
		This Method Is The Setter Method For The _graphicsSceneBackgroundColor Attribute.
		
		@param value: Attribute Value. ( QColor )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "graphicsSceneBackgroundColor" ) )

	@graphicsSceneBackgroundColor.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def graphicsSceneBackgroundColor( self ):
		'''
		This Method Is The Deleter Method For The _graphicsSceneBackgroundColor Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "graphicsSceneBackgroundColor" ) )

	@property
	def graphicsSceneMargin( self ):
		'''
		This Method Is The Property For The _graphicsSceneMargin Attribute.

		@return: self._graphicsSceneMargin. ( Integer )
		'''

		return self._graphicsSceneMargin

	@graphicsSceneMargin.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def graphicsSceneMargin( self, value ):
		'''
		This Method Is The Setter Method For The _graphicsSceneMargin Attribute.
		
		@param value: Attribute Value. ( Integer )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "graphicsSceneMargin" ) )

	@graphicsSceneMargin.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def graphicsSceneMargin( self ):
		'''
		This Method Is The Deleter Method For The _graphicsSceneMargin Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "graphicsSceneMargin" ) )

	@property
	def graphicsSceneWidth( self ):
		'''
		This Method Is The Property For The _graphicsSceneWidth Attribute.

		@return: self._graphicsSceneWidth. ( Integer )
		'''

		return self._graphicsSceneWidth

	@graphicsSceneWidth.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def graphicsSceneWidth( self, value ):
		'''
		This Method Is The Setter Method For The _graphicsSceneWidth Attribute.
		
		@param value: Attribute Value. ( Integer )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "graphicsSceneWidth" ) )

	@graphicsSceneWidth.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def graphicsSceneWidth( self ):
		'''
		This Method Is The Deleter Method For The _graphicsSceneWidth Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "graphicsSceneWidth" ) )

	@property
	def graphicsSceneHeight( self ):
		'''
		This Method Is The Property For The _graphicsSceneHeight Attribute.

		@return: self._graphicsSceneHeight. ( Object )
		'''

		return self._graphicsSceneHeight

	@graphicsSceneHeight.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def graphicsSceneHeight( self, value ):
		'''
		This Method Is The Setter Method For The _graphicsSceneHeight Attribute.
		
		@param value: Attribute Value. ( Object )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "graphicsSceneHeight" ) )

	@graphicsSceneHeight.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def graphicsSceneHeight( self ):
		'''
		This Method Is The Deleter Method For The _graphicsSceneHeight Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "graphicsSceneHeight" ) )

	@property
	def minimumZoomFactor( self ):
		'''
		This Method Is The Property For The _minimumZoomFactor Attribute.

		@return: self._minimumZoomFactor. ( Float )
		'''

		return self._minimumZoomFactor

	@minimumZoomFactor.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def minimumZoomFactor( self, value ):
		'''
		This Method Is The Setter Method For The _minimumZoomFactor Attribute.
		
		@param value: Attribute Value. ( Float )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "minimumZoomFactor" ) )

	@minimumZoomFactor.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def minimumZoomFactor( self ):
		'''
		This Method Is The Deleter Method For The _minimumZoomFactor Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "minimumZoomFactor" ) )

	@property
	def maximumZoomFactor( self ):
		'''
		This Method Is The Property For The _maximumZoomFactor Attribute.

		@return: self._maximumZoomFactor. ( Float )
		'''

		return self._maximumZoomFactor

	@maximumZoomFactor.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def maximumZoomFactor( self, value ):
		'''
		This Method Is The Setter Method For The _maximumZoomFactor Attribute.
		
		@param value: Attribute Value. ( Float )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "maximumZoomFactor" ) )

	@maximumZoomFactor.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def maximumZoomFactor( self ):
		'''
		This Method Is The Deleter Method For The _maximumZoomFactor Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "maximumZoomFactor" ) )

	@property
	def wheelZoomFactor( self ):
		'''
		This Method Is The Property For The _wheelZoomFactor Attribute.

		@return: self._wheelZoomFactor. ( Float )
		'''

		return self._wheelZoomFactor

	@wheelZoomFactor.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def wheelZoomFactor( self, value ):
		'''
		This Method Is The Setter Method For The _wheelZoomFactor Attribute.
		
		@param value: Attribute Value. ( Float )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "wheelZoomFactor" ) )

	@wheelZoomFactor.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def wheelZoomFactor( self ):
		'''
		This Method Is The Deleter Method For The _wheelZoomFactor Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "wheelZoomFactor" ) )

	@property
	def keyZoomFactor( self ):
		'''
		This Method Is The Property For The _keyZoomFactor Attribute.

		@return: self._keyZoomFactor. ( Float )
		'''

		return self._keyZoomFactor

	@keyZoomFactor.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def keyZoomFactor( self, value ):
		'''
		This Method Is The Setter Method For The _keyZoomFactor Attribute.
		
		@param value: Attribute Value. ( Float )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "keyZoomFactor" ) )

	@keyZoomFactor.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def keyZoomFactor( self ):
		'''
		This Method Is The Deleter Method For The _keyZoomFactor Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "keyZoomFactor" ) )

	@property
	def ui( self ):
		'''
		This Method Is The Property For The _ui Attribute.

		@return: self._ui. ( Object )
		'''

		return self._ui

	@ui.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def ui( self, value ):
		'''
		This Method Is The Setter Method For The _ui Attribute.
		
		@param value: Attribute Value. ( Object )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "ui" ) )

	@ui.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def ui( self ):
		'''
		This Method Is The Deleter Method For The _ui Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "ui" ) )

	#***************************************************************************************
	#***	Class Methods
	#***************************************************************************************
	@core.executionTrace
	def initializeUi( self ):
		'''
		This Method Initializes The Widget Ui.
		'''

		image = Image( str( self._imagePath ) )
		self._pixmap = QPixmap().fromImage( image.convertToQImage() )

		#self._scaleFactor = 1 / ( float( self.cWorldMap_QPixmap.width() ) / float( cWidgetSizeX ) )
		#self._graphicsView.scale( self._scaleFactor, self._scaleFactor )

		self._graphicsView.setHorizontalScrollBarPolicy( Qt.ScrollBarAlwaysOff )
		self._graphicsView.setVerticalScrollBarPolicy( Qt.ScrollBarAlwaysOff )
		self._graphicsView.setTransformationAnchor( QGraphicsView.AnchorUnderMouse )
		self._graphicsView.setDragMode( QGraphicsView.ScrollHandDrag )
		self._graphicsView.wheelEvent = self.wheelEvent

		self._graphicsScene.setItemIndexMethod( QGraphicsScene.NoIndex )
		self._graphicsScene.setSceneRect( -( float( self._graphicsSceneWidth ) + self._pixmap.width() / 2 ) / 2, -( float( self._graphicsSceneHeight ) + self._pixmap.height() / 2 ) / 2, float( self._graphicsSceneWidth ) + self._pixmap.width() / 2, float( self._graphicsSceneHeight ) + self._pixmap.height() / 2 )

		self._graphicsView.setScene( self._graphicsScene )

		self._graphicsView.setBackgroundBrush( QBrush( self._graphicsSceneBackgroundColor ) )

		self._graphicsPixmapItem = QGraphicsPixmapItem( self._pixmap )
		self._graphicsPixmapItem.setOffset( -self._pixmap.width() / 2, -self._pixmap.height() / 2 )
		self._graphicsScene.addItem( self._graphicsPixmapItem )

		self._ui.sIBL_GUI_Image_Previewer_Form_gridLayout.addWidget( self._graphicsView )


		width = self._pixmap.width() > QApplication.desktop().width() and QApplication.desktop().width() + self._graphicsSceneMargin or self._pixmap.width() + self._graphicsSceneMargin
		height = self._pixmap.height() > QApplication.desktop().height() and QApplication.desktop().height() + self._graphicsSceneMargin or self._pixmap.height() + self._graphicsSceneMargin

		self._ui.resize( width, height )

	@core.executionTrace
	def scaleView( self, scaleFactor ) :
		'''
		This Method Scales The QGraphicsView.

		@param scaleFactor: Float ( Float )
		'''

		factor = self._graphicsView.matrix().scale( scaleFactor, scaleFactor ).mapRect( QRectF( 0, 0, 1, 1 ) ).width()
		if factor < self._minimumZoomFactor or factor > self._maximumZoomFactor :
			return

		self._graphicsView.scale( scaleFactor, scaleFactor )

	@core.executionTrace
	def wheelEvent( self, event ) :
		'''
		This Method Redefines wheelEvent.

		@param event: QEvent ( QEvent )
		'''

		self.scaleView( pow( 1.5, event.delta() / self._wheelZoomFactor ) )

	@core.executionTrace
	def keyPressEvent( self, event ) :
		'''
		This Method Redefines keyPressEvent.

		@param event: QEvent ( QEvent )
		'''

		key = event.key()
		if key == Qt.Key_Plus:
			self.scaleView( self._keyZoomFactor )
		elif key == Qt.Key_Minus:
			self.scaleView( 1 / self._keyZoomFactor )
		else:
			QGraphicsView.keyPressEvent( self, event )

class Preview( UiComponent ):
	'''
	This Class Is The Preview Class.
	'''

	@core.executionTrace
	def __init__( self, name = None, uiFile = None ):
		'''
		This Method Initializes The Class.
		
		@param name: Component Name. ( String )
		@param uiFile: Ui File. ( String )
		'''

		LOGGER.debug( "> Initializing '{0}()' Class.".format( self.__class__.__name__ ) )

		UiComponent.__init__( self, name = name, uiFile = uiFile )

		# --- Setting Class Attributes. ---
		self.deactivatable = True

		self._uiPath = "ui/Preview.ui"
		self._uiResources = "resources"

		self._container = None
		self._signalsSlotsCenter = None
		self._settings = None
		self._settingsSection = None

		self._corePreferencesManager = None
		self._coreDatabaseBrowser = None

		self._imagePreviewers = None

		self._previewLightingImageAction = None

	#***************************************************************************************
	#***	Attributes Properties
	#***************************************************************************************
	@property
	def uiPath( self ):
		'''
		This Method Is The Property For The _uiPath Attribute.

		@return: self._uiPath. ( String )
		'''

		return self._uiPath

	@uiPath.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def uiPath( self, value ):
		'''
		This Method Is The Setter Method For The _uiPath Attribute.

		@param value: Attribute Value. ( String )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "uiPath" ) )

	@uiPath.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def uiPath( self ):
		'''
		This Method Is The Deleter Method For The _uiPath Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "uiPath" ) )

	@property
	def uiResources( self ):
		'''
		This Method Is The Property For The _uiResources Attribute.

		@return: self._uiResources. ( String )
		'''

		return self._uiResources

	@uiResources.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def uiResources( self, value ):
		'''
		This Method Is The Setter Method For The _uiResources Attribute.

		@param value: Attribute Value. ( String )
		'''
		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "uiResources" ) )

	@uiResources.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def uiResources( self ):
		'''
		This Method Is The Deleter Method For The _uiResources Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "uiResources" ) )

	@property
	def container( self ):
		'''
		This Method Is The Property For The _container Attribute.

		@return: self._container. ( QObject )
		'''

		return self._container

	@container.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def container( self, value ):
		'''
		This Method Is The Setter Method For The _container Attribute.

		@param value: Attribute Value. ( QObject )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "container" ) )

	@container.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def container( self ):
		'''
		This Method Is The Deleter Method For The _container Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "container" ) )

	@property
	def signalsSlotsCenter( self ):
		'''
		This Method Is The Property For The _signalsSlotsCenter Attribute.

		@return: self._signalsSlotsCenter. ( QObject )
		'''

		return self._signalsSlotsCenter

	@signalsSlotsCenter.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def signalsSlotsCenter( self, value ):
		'''
		This Method Is The Setter Method For The _signalsSlotsCenter Attribute.

		@param value: Attribute Value. ( QObject )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "signalsSlotsCenter" ) )

	@signalsSlotsCenter.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def signalsSlotsCenter( self ):
		'''
		This Method Is The Deleter Method For The _signalsSlotsCenter Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "signalsSlotsCenter" ) )

	@property
	def settings( self ):
		'''
		This Method Is The Property For The _settings Attribute.

		@return: self._settings. ( QSettings )
		'''

		return self._settings

	@settings.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def settings( self, value ):
		'''
		This Method Is The Setter Method For The _settings Attribute.

		@param value: Attribute Value. ( QSettings )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "settings" ) )

	@settings.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def settings( self ):
		'''
		This Method Is The Deleter Method For The _settings Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "settings" ) )

	@property
	def settingsSection( self ):
		'''
		This Method Is The Property For The _settingsSection Attribute.

		@return: self._settingsSection. ( String )
		'''

		return self._settingsSection

	@settingsSection.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def settingsSection( self, value ):
		'''
		This Method Is The Setter Method For The _settingsSection Attribute.

		@param value: Attribute Value. ( String )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "settingsSection" ) )

	@settingsSection.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def settingsSection( self ):
		'''
		This Method Is The Deleter Method For The _settingsSection Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "settingsSection" ) )

	@property
	def corePreferencesManager( self ):
		'''
		This Method Is The Property For The _corePreferencesManager Attribute.

		@return: self._corePreferencesManager. ( Object )
		'''

		return self._corePreferencesManager

	@corePreferencesManager.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def corePreferencesManager( self, value ):
		'''
		This Method Is The Setter Method For The _corePreferencesManager Attribute.

		@param value: Attribute Value. ( Object )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "corePreferencesManager" ) )

	@corePreferencesManager.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def corePreferencesManager( self ):
		'''
		This Method Is The Deleter Method For The _corePreferencesManager Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "corePreferencesManager" ) )

	@property
	def coreDatabaseBrowser( self ):
		'''
		This Method Is The Property For The _coreDatabaseBrowser Attribute.

		@return: self._coreDatabaseBrowser. ( Object )
		'''

		return self._coreDatabaseBrowser

	@coreDatabaseBrowser.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def coreDatabaseBrowser( self, value ):
		'''
		This Method Is The Setter Method For The _coreDatabaseBrowser Attribute.

		@param value: Attribute Value. ( Object )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "coreDatabaseBrowser" ) )

	@coreDatabaseBrowser.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def coreDatabaseBrowser( self ):
		'''
		This Method Is The Deleter Method For The _coreDatabaseBrowser Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "coreDatabaseBrowser" ) )
	@property
	def imagePreviewers( self ):
		'''
		This Method Is The Property For The _imagePreviewers Attribute.

		@return: self._imagePreviewers. ( List )
		'''

		return self._imagePreviewers

	@imagePreviewers.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def imagePreviewers( self, value ):
		'''
		This Method Is The Setter Method For The _imagePreviewers Attribute.

		@param value: Attribute Value. ( List )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "imagePreviewers" ) )

	@imagePreviewers.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def imagePreviewers( self ):
		'''
		This Method Is The Deleter Method For The _imagePreviewers Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "imagePreviewers" ) )

	@property
	def previewLightingImageAction( self ):
		'''
		This Method Is The Property For The _previewLightingImageAction Attribute.

		@return: self._previewLightingImageAction. ( QAction )
		'''

		return self._previewLightingImageAction

	@previewLightingImageAction.setter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def previewLightingImageAction( self, value ):
		'''
		This Method Is The Setter Method For The _previewLightingImageAction Attribute.

		@param value: Attribute Value. ( QAction )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "previewLightingImageAction" ) )

	@previewLightingImageAction.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def previewLightingImageAction( self ):
		'''
		This Method Is The Deleter Method For The _previewLightingImageAction Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "previewLightingImageAction" ) )

	#***************************************************************************************
	#***	Class Methods
	#***************************************************************************************
	@core.executionTrace
	def activate( self, container ):
		'''
		This Method Activates The Component.
		
		@param container: Container To Attach The Component To. ( QObject )
		'''

		LOGGER.debug( "> Activating '{0}' Component.".format( self.__class__.__name__ ) )

		self.uiFile = os.path.join( os.path.dirname( core.getModule( self ).__file__ ), self._uiPath )
		self._uiResources = os.path.join( os.path.dirname( core.getModule( self ).__file__ ), self._uiResources )
		self._container = container
		self._signalsSlotsCenter = QObject()
		self._settings = self._container.settings
		self._settingsSection = self.name

		self._corePreferencesManager = self._container.componentsManager.components["core.preferencesManager"].interface
		self._coreDatabaseBrowser = self._container.componentsManager.components["core.databaseBrowser"].interface

		self._imagePreviewers = []

		self._activate()

	@core.executionTrace
	def deactivate( self ):
		'''
		This Method Deactivates The Component.
		'''

		LOGGER.debug( "> Deactivating '{0}' Component.".format( self.__class__.__name__ ) )

		self.uiFile = None
		self._uiResources = os.path.basename( self._uiResources )
		self._container = None
		self._signalsSlotsCenter = None
		self._settings = None
		self._settingsSection = None

		self._corePreferencesManager = None
		self._coreDatabaseBrowser = None

		self._imagePreviewers = None

		self._deactivate()

	@core.executionTrace
	def initializeUi( self ):
		'''
		This Method Initializes The Component Ui.
		'''

		LOGGER.debug( "> Initializing '{0}' Component Ui.".format( self.__class__.__name__ ) )

		self.Custom_Previewer_Path_lineEdit_setUi()

		self.addActions_()

		# Signals / Slots.
		self._signalsSlotsCenter.connect( self.ui.Custom_Previewer_Path_toolButton, SIGNAL( "clicked()" ), self.Custom_Previewer_Path_toolButton_OnClicked )
		self._signalsSlotsCenter.connect( self.ui.Custom_Previewer_Path_lineEdit, SIGNAL( "editingFinished()" ), self.Custom_Previewer_Path_lineEdit_OnEditFinished )

	@core.executionTrace
	def uninitializeUi( self ):
		'''
		This Method Uninitializes The Component Ui.
		'''

		LOGGER.debug( "> Uninitializing '{0}' Component Ui.".format( self.__class__.__name__ ) )

		self.removeActions_()

		# Signals / Slots.
		self._signalsSlotsCenter.disconnect( self.ui.Custom_Previewer_Path_toolButton, SIGNAL( "clicked()" ), self.Custom_Previewer_Path_toolButton_OnClicked )
		self._signalsSlotsCenter.disconnect( self.ui.Custom_Previewer_Path_lineEdit, SIGNAL( "editingFinished()" ), self.Custom_Previewer_Path_lineEdit_OnEditFinished )

	@core.executionTrace
	def addWidget( self ):
		'''
		This Method Adds The Component Widget To The Container.
		'''

		LOGGER.debug( "> Adding '{0}' Component Widget.".format( self.__class__.__name__ ) )

		self._corePreferencesManager.ui.Others_Preferences_gridLayout.addWidget( self.ui.Custom_Previewer_Path_groupBox )

	@core.executionTrace
	def removeWidget( self ):
		'''
		This Method Removes The Component Widget From The Container.
		'''

		LOGGER.debug( "> Removing '{0}' Component Widget.".format( self.__class__.__name__ ) )

		self._corePreferencesManager.ui.findChild( QGridLayout, "Others_Preferences_gridLayout" ).removeWidget( self.ui )
		self.ui.Custom_Previewer_Path_groupBox.setParent( None )

	@core.executionTrace
	def addActions_( self ):
		'''
		This Method Adds Actions.
		'''

		LOGGER.debug( "> Adding '{0}' Component Actions.".format( self.__class__.__name__ ) )

		separatorAction = QAction( self._coreDatabaseBrowser.ui.Database_Browser_listView )
		separatorAction.setSeparator( True )
		self._coreDatabaseBrowser.ui.Database_Browser_listView.addAction( separatorAction )

		self._previewLightingImageAction = QAction( "Preview Lighting Image ...", self._coreDatabaseBrowser.ui.Database_Browser_listView )
		self._previewLightingImageAction.triggered.connect( self.Database_Browser_listView_previewLightingImageAction )
		self._coreDatabaseBrowser.ui.Database_Browser_listView.addAction( self._previewLightingImageAction )

	@core.executionTrace
	def removeActions_( self ):
		'''
		This Method Removes Actions.
		'''

		LOGGER.debug( "> Removing '{0}' Component Actions.".format( self.__class__.__name__ ) )

		self._coreDatabaseBrowser.ui.Database_Browser_listView.removeAction( self._previewLightingImageAction )

		self._previewLightingImageAction = None

	@core.executionTrace
	def Database_Browser_listView_previewLightingImageAction( self, checked ):
		'''
		This Method Is Triggered By previewLightingImageAction.

		@param checked: Action Checked State. ( Boolean )
		'''

		selectedIblSets = self._coreDatabaseBrowser.getSelectedItems()
		for iblSet in selectedIblSets:
			iblSet._datas.lightingImage and os.path.exists( iblSet._datas.lightingImage ) and self.launchImagePreviewer( iblSet._datas.lightingImage )

	@core.executionTrace
	def Custom_Previewer_Path_lineEdit_setUi( self ) :
		'''
		This Method Fills The Custom_Previewer_Path_lineEdit.
		'''

		customPreviewer = self._settings.getKey( self._settingsSection, "customPreviewer" )
		LOGGER.debug( "> Setting '{0}' With Value '{1}'.".format( "Custom_Previewer_Path_lineEdit", customPreviewer.toString() ) )
		self.ui.Custom_Previewer_Path_lineEdit.setText( customPreviewer.toString() )

	@core.executionTrace
	def Custom_Previewer_Path_toolButton_OnClicked( self ) :
		'''
		This Method Is Called When Custom_Previewer_Path_toolButton Is Clicked.
		'''

		customPreviewerExecutable = self._container.storeLastBrowsedPath( QFileDialog.getOpenFileName( self, "Custom Previewer Executable :", self._container.lastBrowsedPath ) )
		if customPreviewerExecutable != "":
			LOGGER.debug( "> Chosen Custom Previewer Executable : '{0}'.".format( customPreviewerExecutable ) )
			self.ui.Custom_Previewer_Path_lineEdit.setText( QString( customPreviewerExecutable ) )
			self._settings.setKey( self._settingsSection, "customPreviewer", self.ui.Custom_Previewer_Path_lineEdit.text() )

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( ui.common.uiBasicExceptionHandler, False, foundations.exceptions.UserError )
	def Custom_Previewer_Path_lineEdit_OnEditFinished( self ) :
		'''
		This Method Is Called When Custom_Previewer_Path_lineEdit Is Edited And Check That Entered Path Is Valid.
		'''

		if not os.path.exists( os.path.abspath( str( self.ui.Custom_Previewer_Path_lineEdit.text() ) ) ) and str( self.ui.Custom_Previewer_Path_lineEdit.text() ) != "":
			LOGGER.debug( "> Restoring Preferences !" )
			self.Custom_Previewer_Path_lineEdit_setUi()

			raise foundations.exceptions.UserError, "{0} | Invalid Custom Previewer Executable File !".format( self.__class__.__name__ )
		else :
			self._settings.setKey( self._settingsSection, "customPreviewer", self.ui.Custom_Previewer_Path_lineEdit.text() )

	@core.executionTrace
	def launchImagePreviewer( self, imagePath ):
		'''
		This Method Launches An Image Previewer.
		'''

		customPreviewer = str( self.ui.Custom_Previewer_Path_lineEdit.text() )
		if customPreviewer :
			previewCommand = None
		else :
			self._imagePreviewers.append( ImagePreviewer( self, imagePath ) )

#***********************************************************************************************
#***	Python End
#***********************************************************************************************
