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
***	freeImage.py
***
***	Platform :
***		Windows, Linux, Mac Os X
***
***	Description :
***		FreeImage libraryPath Manipulation Module.
***
***	Others :
***		Large Portions Of The Code Are Taken From FreeImagePy By Michele Petrazzo : http://freeimagepy.sourceforge.net/.
************************************************************************************************
'''

#***********************************************************************************************
#***	Python Begin
#***********************************************************************************************

#***********************************************************************************************
#***	External Imports
#***********************************************************************************************
import ctypes
import logging
import os
import platform
import types

#***********************************************************************************************
#***	Internal Imports
#***********************************************************************************************
import core
import io
import foundations.exceptions
from globals.constants import Constants

#***********************************************************************************************
#***	Overall Variables
#***********************************************************************************************
LOGGER = logging.getLogger( Constants.logger )

#***********************************************************************************************
#***	FreeImage Variables
#***********************************************************************************************

if platform.system() == "Windows" or platform.system() == "Microsoft" :
	DLL_CALLCONV = ctypes.WINFUNCTYPE
else:
	DLL_CALLCONV = ctypes.CFUNCTYPE

LITTLEENDIAN = 1

'''
Internal Types.
'''
VOID	 = ctypes.c_void_p
INT		 = ctypes.c_int
BOOL	 = ctypes.c_long
BYTE	 = ctypes.c_ubyte
WORD	 = ctypes.c_ushort
DWORD	 = ctypes.c_ulong
LONG	 = ctypes.c_long

FI_HANLDE = ctypes.c_void_p
BYTE_P = ctypes.POINTER( BYTE )

'''
'I/O Image Format Identifiers.
'''
FIF_UNKNOWN	 = -1
FIF_BMP		 = 0
FIF_ICO		 = 1
FIF_JPEG	 = 2
FIF_JNG		 = 3
FIF_KOALA	 = 4
FIF_LBM		 = 5
FIF_IFF		 = FIF_LBM
FIF_MNG		 = 6
FIF_PBM		 = 7
FIF_PBMRAW	 = 8
FIF_PCD		 = 9
FIF_PCX		 = 10
FIF_PGM		 = 11
FIF_PGMRAW	 = 12
FIF_PNG		 = 13
FIF_PPM		 = 14
FIF_PPMRAW	 = 15
FIF_RAS		 = 16
FIF_TARGA	 = 17
FIF_TIFF	 = 18
FIF_WBMP	 = 19
FIF_PSD		 = 20
FIF_CUT		 = 21
FIF_XBM		 = 22
FIF_XPM		 = 23
FIF_DDS		 = 24
FIF_GIF		 = 25
FIF_HDR		 = 26
FIF_FAXG3	 = 27
FIF_SGI		 = 28
FIF_EXR		 = 29
FIF_J2K		 = 30
FIF_JP2		 = 31
FIF_PFM		 = 32
FIF_PICT	 = 33
FIF_RAW		 = 34

FIFToType = { -1 : "UNKNOWN",
			0 : "BMP",
			1 : "ICO",
			2 : "JPEG",
			3 : "JNG",
			4 : "KOALA",
			5 : "IFF",
			6 : "MNG",
			7 : "BPM",
			8 : "PBMRAW",
			9 : "PCD",
			10 : "PCX",
			11 : "PGM",
			12 : "PGMRAW",
			13 : "PNG",
			14 : "PPM",
			15 : "PPMRAW",
			16 : "RAS",
			17 : "TARGA",
			18 : "TIFF",
			19 : "WBMP",
			20 : "PSD",
			21 : "CUT",
			22 : "XBM",
			23 : "XPM",
			24 : "DDS",
			25 : "GIF",
			26 : "HDR",
			27 : "FAXG3",
			28 : "SGI",
			29 : "EXR",
			30 : "J2K",
			31 : "JP2",
			32 : "PFM",
			33 : "PICT",
			34 : "RAW"
			}

FIF_MUTLIPAGE = ( FIF_TIFF, FIF_ICO, FIF_GIF )

'''
Load / Save Flag Constants.
'''
BMP_DEFAULT		 = 0
BMP_SAVE_RLE	 = 1

PNG_DEFAULT		 = 0
PNG_IGNOREGAMMA	 = 1

GIF_DEFAULT		 = 0
GIF_LOAD256		 = 1
GIF_PLAYBACK	 = 2

ICO_DEFAULT		 = 0
ICO_MAKEALPHA	 = 1

TIFF_DEFAULT		 = 0
TIFF_CMYK			 = 0x0001
TIFF_NONE			 = 0x0800
TIFF_PACKBITS		 = 0x0100
TIFF_DEFLATE		 = 0x0200
TIFF_ADOBE_DEFLATE	 = 0x0400
TIFF_CCITTFAX3		 = 0x1000
TIFF_CCITTFAX4		 = 0x2000
TIFF_LZW			 = 0x4000
TIFF_JPEG			 = 0x8000

JPEG_DEFAULT		 = 0
JPEG_FAST			 = 1
JPEG_ACCURATE		 = 2
JPEG_QUALITYSUPERB	 = 0x80
JPEG_QUALITYGOOD	 = 0x100
JPEG_QUALITYNORMAL	 = 0x200
JPEG_QUALITYAVERAGE	 = 0x400
JPEG_QUALITYBAD		 = 0x800
JPEG_CMYK			 = 0x1000
JPEG_PROGRESSIVE	 = 0x2000

CUT_DEFAULT			 = 0
DDS_DEFAULT			 = 0
HDR_DEFAULT			 = 0
IFF_DEFAULT			 = 0
KOALA_DEFAULT		 = 0
LBM_DEFAULT			 = 0
MNG_DEFAULT			 = 0
PCD_DEFAULT			 = 0
PCD_BASE			 = 1
PCD_BASEDIV4		 = 2
PCD_BASEDIV16		 = 3
PCX_DEFAULT			 = 0
PNM_DEFAULT			 = 0
PNM_SAVE_RAW		 = 0
PNM_SAVE_ASCII		 = 1
PSD_DEFAULT			 = 0
RAS_DEFAULT			 = 0
TARGA_DEFAULT 		 = 0
TARGA_LOAD_RGB888	 = 1
WBMP_DEFAULT		 = 0
XBM_DEFAULT			 = 0
EXR_DEFAULT			 = 0
PFM_DEFAULT			 = 0

'''
Extension To Type.
'''
EXTToType = dict( 
			 tiff = ( FIF_TIFF, TIFF_DEFAULT, '.tif' ),
			 tiffg3 = ( FIF_TIFF, TIFF_CCITTFAX3, '.tif' ),
			 tiffg4 = ( FIF_TIFF, TIFF_CCITTFAX4, '.tif' ),
			 tiffno = ( FIF_TIFF, TIFF_NONE, '.tif' ),

			 jpeg = ( FIF_JPEG, JPEG_DEFAULT, '.jpg' ),
			 jpegfa = ( FIF_JPEG, JPEG_FAST, '.jpg' ),
			 jpegac = ( FIF_JPEG, JPEG_ACCURATE, '.jpg' ),
			 jpegsu = ( FIF_JPEG, JPEG_QUALITYSUPERB, '.jpg' ),
			 jpeggo = ( FIF_JPEG, JPEG_QUALITYGOOD, '.jpg' ),
			 jpegav = ( FIF_JPEG, JPEG_QUALITYAVERAGE, '.jpg' ),
			 jpegba = ( FIF_JPEG, JPEG_QUALITYBAD, '.jpg' ),

			 png = ( FIF_PNG, PNG_DEFAULT, '.png' ),

			 bmp = ( FIF_BMP, BMP_DEFAULT, '.bmp' ),

			 ico = ( FIF_ICO, ICO_DEFAULT, '.ico' ),

			 gif = ( FIF_GIF, GIF_DEFAULT, '.gif' ),

			 pbm = ( FIF_PBM, PNM_DEFAULT, '.pbm' ),
			 pgm = ( FIF_PGM, PNM_DEFAULT, '.pgm' ),
			 pnm = ( FIF_PPM, PNM_DEFAULT, '.pnm' ),
			 ppm = ( FIF_PPM, PNM_DEFAULT, '.ppm' ),
		)

#Internal C structures
class FITAG( ctypes.Structure ):
	_fields_ = [ ( "data", VOID )]

class RGBQUAD( ctypes.Structure ):
	_fields_ = []
	if LITTLEENDIAN:
		_fields_ += [( "rgbBlue", BYTE ),
					 ( "rgbGreen", BYTE ),
					 ( "rgbRed", BYTE )]
	else:
		_fields_ += [( "rgbRed", BYTE ),
					 ( "rgbGreen", BYTE ),
					 ( "rgbBlue", BYTE )]

	_fields_ += [ ( "rgbReserved", BYTE ) ]

class FIBITMAP( ctypes.Structure ):
	_fields_ = [ ( "data", ctypes.POINTER( VOID ) ) ]

class FIMETADATA( ctypes.Structure ):
	_fields_ = [ ( "data", VOID ), ]

class PBITMAPINFOHEADER( ctypes.Structure ):
	_fields_ = [ ( "biSize", DWORD ),
				 ( "biWidth", LONG ),
				 ( "biHeight", LONG ),
				 ( "biPlanes", WORD ),
				 ( "biBitCount", WORD ),
				 ( "biCompression", DWORD ),
				 ( "biSizeImage", DWORD ),
				 ( "biXPelsPerMeter", LONG ),
				 ( "biYPelsPerMeter", LONG ),
				 ( "biClrUsed", DWORD ),
				 ( "biClrImportant", DWORD ), ]

'''
Dither transformation
'''
FID_FS		 = 0
FID_BAYER4x4	 = 1
FID_BAYER8x8	 = 2
FID_CLUSTER6x6	 = 3
FID_CLUSTER8x8	 = 4
FID_CLUSTER16x16 = 5
FID_BAYER16x16 = 6

# Get_type
FIC_MINISWHITE = 0
FIC_MINISBLACK = 1
FIC_RGB = 2
FIC_PALETTE = 3
FIC_RGBALPHA = 4
FIC_CMYK = 5

FICToType = {0 : "MINISWHITE",
			1 : "MINISBLACK",
			2 : "RGB",
			3 : "PALETTE",
			4 : "RGBALPHA",
			5 : "CMYK"
			}

'''
Rescale Filters.
'''

FILTER_BOX			 = 0
FILTER_BICUBIC		 = 1
FILTER_BILINEAR		 = 2
FILTER_BSPLINE		 = 3
FILTER_CATMULLROM	 = 4
FILTER_LANCZOS3		 = 5

# Format Types.
FIT_UNKNOWN	 = 0
FIT_BITMAP	 = 1
FIT_UINT16	 = 2
FIT_INT16	 = 3
FIT_UINT32	 = 4
FIT_INT32	 = 5
FIT_FLOAT	 = 6
FIT_DOUBLE	 = 7
FIT_COMPLEX	 = 8
FIT_RGB16	 = 9
FIT_RGBA16	 = 10
FIT_RGBF	 = 11
FIT_RGBAF	 = 12

# Metadatas.
FIMD_NODATA			 = -1
FIMD_COMMENTS		 = 0
FIMD_EXIF_MAIN		 = 1
FIMD_EXIF_EXIF		 = 2
FIMD_EXIF_GPS		 = 3
FIMD_EXIF_MAKERNOTE	 = 4
FIMD_EXIF_INTEROP	 = 5
FIMD_IPTC			 = 6
FIMD_XMP			 = 7
FIMD_GEOTIFF		 = 8
FIMD_ANIMATION		 = 9
FIMD_CUSTOM			 = 10

FIMD__METALIST = {"FIMD_NODATA": FIMD_NODATA, "FIMD_COMMENTS":FIMD_COMMENTS,
				  "FIMD_EXIF_MAIN":FIMD_EXIF_MAIN, "FIMD_EXIF_EXIF": FIMD_EXIF_EXIF,
				  "FIMD_EXIF_GPS": FIMD_EXIF_GPS, "FIMD_EXIF_MAKERNOTE": FIMD_EXIF_MAKERNOTE,
				  "FIMD_EXIF_INTEROP": FIMD_EXIF_INTEROP, "FIMD_IPTC": FIMD_IPTC,
				  "FIMD_XMP": FIMD_XMP, "FIMD_GEOTIFF": FIMD_GEOTIFF,
				  "FIMD_ANIMATION": FIMD_ANIMATION, "FIMD_CUSTOM": FIMD_CUSTOM}

FIDT_NOTYPE		 = 0
FIDT_BYTE		 = 1
FIDT_ASCII		 = 2
FIDT_SHORT		 = 3
FIDT_LONG		 = 4
FIDT_RATIONAL	 = 5
FIDT_SBYTE		 = 6
FIDT_UNDEFINED	 = 7
FIDT_SSHORT		 = 8
FIDT_SLONG		 = 9
FIDT_SRATIONAL	 = 10
FIDT_FLOAT		 = 11
FIDT_DOUBLE		 = 12
FIDT_IFD		 = 13
FIDT_PALETTE	 = 14

FIDT__LIST = {FIDT_NOTYPE: VOID,
			FIDT_BYTE: ctypes.c_ubyte,
			FIDT_ASCII: ctypes.c_char_p,
			FIDT_SHORT: ctypes.c_ushort,
			FIDT_LONG: ctypes.c_uint,
			FIDT_RATIONAL: ctypes.c_ulong,
			FIDT_SBYTE: ctypes.c_short,
			FIDT_UNDEFINED: VOID,
			FIDT_SSHORT: ctypes.c_short,
			FIDT_SLONG: ctypes.c_long,
			FIDT_SRATIONAL: ctypes.c_long,
			FIDT_FLOAT: ctypes.c_float,
			FIDT_DOUBLE: ctypes.c_double,
			FIDT_IFD: ctypes.c_uint,
			FIDT_PALETTE: RGBQUAD
			}


'''
Color Channels
'''
FICC_RGB	 = 0
FICC_RED	 = 1
FICC_GREEN	 = 2
FICC_BLUE	 = 3
FICC_ALPHA	 = 4
FICC_BLACK	 = 5
FICC_REAL	 = 6
FICC_IMAG	 = 7
FICC_MAG	 = 8
FICC_PHASE	 = 9

'''
Image Quantize
'''
FIQ_WUQUANT = 0
FIQ_NNQUANT = 1

if LITTLEENDIAN:
	FI_RGBA_RED			 = 2
	FI_RGBA_GREEN		 = 1
	FI_RGBA_BLUE		 = 0
	FI_RGBA_ALPHA		 = 3
	FI_RGBA_RED_MASK	 = 0x00FF0000
	FI_RGBA_GREEN_MASK	 = 0x0000FF00
	FI_RGBA_BLUE_MASK	 = 0x000000FF
	FI_RGBA_ALPHA_MASK	 = 0xFF000000L
	FI_RGBA_RED_SHIFT	 = 16
	FI_RGBA_GREEN_SHIFT	 = 8
	FI_RGBA_BLUE_SHIFT	 = 0
	FI_RGBA_ALPHA_SHIFT	 = 24
else:
	FI_RGBA_RED			 = 0
	FI_RGBA_GREEN		 = 1
	FI_RGBA_BLUE		 = 2
	FI_RGBA_ALPHA		 = 3
	FI_RGBA_RED_MASK	 = 0xFF000000
	FI_RGBA_GREEN_MASK	 = 0x00FF0000
	FI_RGBA_BLUE_MASK	 = 0x0000FF00
	FI_RGBA_ALPHA_MASK	 = 0x000000FF
	FI_RGBA_RED_SHIFT	 = 24
	FI_RGBA_GREEN_SHIFT	 = 16
	FI_RGBA_BLUE_SHIFT	 = 8
	FI_RGBA_ALPHA_SHIFT	 = 0

'''
Custom Constants
'''
COL_1 = 1
COL_4 = 4
COL_8 = 8
COL_16 = 16
COL_24 = 24
COL_32 = 32
COL_48 = 48
COL_64 = 64
COL_96 = 96
COL_1TO8 = ( COL_1, COL_4, COL_8 )
COL_16TO32 = ( COL_16, COL_24, COL_32 )
COL_1TO32 = ( COL_1, COL_4, COL_8, COL_16, COL_24, COL_32 )
COL_1TO48 = COL_1TO32 + ( COL_48, )

ROTATE_ANGLE_1BIT = ( -90, 90, 180, 270 )

##Internal class structure
#
#class FISize( object ):
#	''' A class used for store width and height bitmap informations
#	'''
#	def __init__( self, valW = 0, valH = 0 ):
#		''' Pass me the width and height
#		'''
#		if type( valW ) == types.IntType:
#			self.__W, self.__H = valW, valH
#		elif len( valW ) == 2:
#			self.__W, self.__H = valW
#		else:
#			raise ValueError
#
#	def getWidth( self ):
#		return self.__W
#
#	def getHeight( self ):
#		return self.__H
#
#	def getSize( self ):
#		return ( self.__W, self.__H )
#
#	def __repr__( self ):
#		'''
#		'''
#		return "FISize (%i, %i)" % ( self.getWidth(), self.getHeight() )
#
#	def __len__( self ):
#		'''
#		'''
#		return 2
#
#	def __iter__( self ):
#		'''
#		'''
#		yield self.__W
#		yield self.__H
#
#	def __eq__( self, object ):
#		'''
#		'''
#		if not isinstance( object, FISize ):
#			return False
#		else:
#			#print object.w == self.getWidth(), object.h == self.getHeight()
#			return object.w == self.getWidth() and object.h == self.getHeight()
#
#	w = property( getWidth )
#	h = property( getHeight )
#	size = property( getSize )
#
#FI_ReadProc = DLL_CALLCONV( ctypes.c_uint, BYTE_P, ctypes.c_uint, ctypes.c_uint, FI_HANLDE )
#FI_WriteProc = DLL_CALLCONV( ctypes.c_uint, BYTE_P, ctypes.c_uint, ctypes.c_uint, FI_HANLDE )
#FI_SeekProc = DLL_CALLCONV( ctypes.c_int, FI_HANLDE, ctypes.c_long, ctypes.c_int )
#FI_TellProc = DLL_CALLCONV( ctypes.c_long, FI_HANLDE )
#
#class FreeImageIO( ctypes.Structure ):
#	_fields_ = [( "read_proc", FI_ReadProc ),
#				( "write_proc", FI_WriteProc ),
#				( "seek_proc", FI_SeekProc ),
#				( "tell_proc", FI_TellProc )]

FREEIMAGE_FUNCTIONS = ( 

	# General Funtions.
	( "FreeImage_Initialise", "@4" ),
	( "FreeImage_DeInitialise", "@0" ),
	( "FreeImage_GetVersion", "@0", None, ctypes.c_char_p ),
	( "FreeImage_GetCopyrightMessage", "@0", None, ctypes.c_char_p ),
	( "FreeImage_SetOutputMessage", "@4" ),

	 # Bitmap Management Functions.
	( "FreeImage_Allocate", "@24", COL_1TO32 ),
	( "FreeImage_AllocateT", "@28" ),
	( "FreeImage_Load", "@12" ),
	( "FreeImage_LoadU", "@12" ),
	( "FreeImage_LoadFromHandle", "@16" ),
	( "FreeImage_Save", "@16" ),
	( "FreeImage_SaveU", "@16" ),
	( "FreeImage_SaveToHandle", "@20" ),
	( "FreeImage_Clone", "@4" ),
	( "FreeImage_Unload", "@4" ),

	# Bitmap Information.
	( "FreeImage_GetImageType", "@4" ),
	( "FreeImage_GetColorsUsed", "@4", COL_1TO32 ),
	( "FreeImage_GetBPP", "@4" ),
	( "FreeImage_GetWidth", "@4" ),
	( "FreeImage_GetHeight", "@4" ),
	( "FreeImage_GetLine", "@4" ),
	( "FreeImage_GetPitch", "@4" ),
	( "FreeImage_GetDIBSize", "@4" ),
	( "FreeImage_GetPalette", "@4", COL_1TO32, ctypes.POINTER( RGBQUAD ) ),
	( "FreeImage_GetDotsPerMeterX", "@4" ),
	( "FreeImage_GetDotsPerMeterY", "@4" ),
	( "FreeImage_SetDotsPerMeterX", "@8" ),
	( "FreeImage_SetDotsPerMeterY", "@8" ),
	( "FreeImage_GetInfoHeader", "@4", COL_1TO32, ctypes.POINTER( PBITMAPINFOHEADER ) ),
	( "FreeImage_GetColorType", "@4", COL_1TO32 ),
	( "FreeImage_GetRedMask", "@4", COL_1TO32 ),
	( "FreeImage_GetGreenMask", "@4", COL_1TO32 ),
	( "FreeImage_GetBlueMask", "@4", COL_1TO32 ),
	( "FreeImage_GetTransparencyCount", "@4", COL_1TO32 ),
	( "FreeImage_GetTransparencyTable", "@4", ( COL_8, ), ctypes.POINTER( BYTE ) ),
	( "FreeImage_SetTransparencyTable", "@12", ( COL_8, ) ),
	( "FreeImage_SetTransparent", "@8", ( COL_8, COL_32 ) ),
	( "FreeImage_IsTransparent", "@4", COL_1TO32 ),
	( "FreeImage_HasBackgroundColor", "@4", ( COL_8, COL_24, COL_32 ) ),
	( "FreeImage_GetBackgroundColor", "@8", ( COL_8, COL_24, COL_32 ), ctypes.POINTER( RGBQUAD ) ),
	( "FreeImage_SetBackgroundColor", "@8", ( COL_8, COL_24, COL_32 ) ),

	# Filetype Functions.
	( "FreeImage_GetFileType", "@8" ),
	( "FreeImage_GetFileTypeU", "@8" ),
	( "FreeImage_GetFileTypeFromHandle", "@12" ),


	# Pixel Access.
	( "FreeImage_GetBits", "@4", None, ctypes.POINTER( BYTE ) ),
	( "FreeImage_GetScanLine", "@8", None, ctypes.POINTER( BYTE ) ),
	( "FreeImage_GetPixelIndex", "@16", COL_1TO8 ),
	( "FreeImage_SetPixelIndex", "@16", COL_1TO8 ),
	( "FreeImage_GetPixelColor", "@16", COL_16TO32 ),
	( "FreeImage_SetPixelColor", "@16", COL_16TO32 ),

	# Conversion / Trasformation.
	( "FreeImage_ConvertTo4Bits", "@4", COL_1TO32 ),
	( "FreeImage_ConvertTo8Bits", "@4", COL_1TO32 ),
	( "FreeImage_ConvertToGreyscale", "@4", COL_1TO32 ),
	( "FreeImage_ConvertTo16Bits555", "@4", COL_1TO32 ),
	( "FreeImage_ConvertTo16Bits565", "@4", COL_1TO32 ),
	( "FreeImage_ConvertTo24Bits", "@4", COL_1TO48 ),
	( "FreeImage_ConvertTo32Bits", "@4", COL_1TO32 ),
	( "FreeImage_ColorQuantize", "@8", ( COL_24, ) ),
	( "FreeImage_ColorQuantizeEx", "@20", ( COL_24, ) ),
	( "FreeImage_Threshold", "@8", COL_1TO32 ),
	( "FreeImage_Dither", "@8", COL_1TO32 ),
	( "FreeImage_ConvertFromRawBits", "@36", COL_1TO32 ),
	( "FreeImage_ConvertToRawBits", "@32", COL_1TO32 ),
	( "FreeImage_ConvertToStandardType", "@8" ),
	( "FreeImage_ConvertToType", "@12" ),
	( "FreeImage_ConvertToRGBF", "@4", ( COL_24, COL_32, ) ),

	#Copy / Paste / Composite Routines.
	( "FreeImage_Copy", "@20" ),
	( "FreeImage_Paste", "@20", COL_1TO32 ),

	# Plugin.
	( "FreeImage_GetFIFCount", "@0" ),
	( "FreeImage_SetPluginEnabled", "@8" ),
	( "FreeImage_FIFSupportsReading", "@4" ),
	( "FreeImage_GetFIFFromFilename", "@4" ),
	( "FreeImage_GetFIFFromFilenameU", "@4" ),
	( "FreeImage_FIFSupportsExportBPP", "@8" ),
	( "FreeImage_FIFSupportsExportType", "@8" ),
	( "FreeImage_FIFSupportsICCProfiles", "@4" ),
	( "FreeImage_FIFSupportsWriting", "@4" ),
	( "FreeImage_IsPluginEnabled", "@4" ),
	( "FreeImage_RegisterLocalPlugin", "@20" ),
	( "FreeImage_GetFIFDescription", "@4", None, ctypes.c_char_p ),
	( "FreeImage_GetFIFExtensionList", "@4", None, ctypes.c_char_p ),
	( "FreeImage_GetFIFFromFormat", "@4", None, ctypes.c_char_p ),
	( "FreeImage_GetFIFFromMime", "@4", None, ctypes.c_char_p ),
	( "FreeImage_GetFIFMimeType", "@4", None, ctypes.c_char_p ),
	( "FreeImage_GetFIFRegExpr", "@4", None, ctypes.c_char_p ),
	( "FreeImage_GetFormatFromFIF", "@4", None, ctypes.c_char_p ),

	# Upsampling / Downsampling.
	( "FreeImage_Rescale", "@16", COL_1TO32 ),
	( "FreeImage_MakeThumbnail", "@12", COL_1TO32 ),

	# Rotation and Flipping.
	( "FreeImage_RotateClassic", "@12", COL_1TO32 ),
	( "FreeImage_RotateEx", "@48", ( COL_8, COL_24, COL_32 ), ),


	# Color Manipulation.
	( "FreeImage_AdjustBrightness", "@12", ( COL_8, COL_24, COL_32 ), BOOL ),
	( "FreeImage_AdjustCurve", "@12", ( COL_8, COL_24, COL_32 ), BOOL ),
	( "FreeImage_AdjustGamma", "@12", ( COL_8, COL_24, COL_32 ), BOOL ),
	( "FreeImage_AdjustContrast", "@12", ( COL_8, COL_24, COL_32 ), BOOL ),
	( "FreeImage_GetHistogram", "@12", ( COL_8, COL_24, COL_32 ), BOOL ),
	( "FreeImage_Invert", "@4", COL_1TO32, BOOL ),
	( "FreeImage_GetChannel", "@8", ( COL_24, COL_32 ) ),
	( "FreeImage_SetChannel", "@12", ( COL_24, COL_32 ) ),
	( "FreeImage_GetComplexChannel", "@8" ),
	( "FreeImage_SetComplexChannel", "@12" ),

	# Multipage.
	( "FreeImage_OpenMultiBitmap", "@24" ),
	( "FreeImage_AppendPage", "@8" ),
	( "FreeImage_CloseMultiBitmap", "@8" ),
	( "FreeImage_GetPageCount", "@4" ),
	( "FreeImage_LockPage", "@8" ),
	( "FreeImage_UnlockPage", "@12" ),
	( "FreeImage_InsertPage", "@12" ),
	( "FreeImage_DeletePage", "@8" ),
	( "FreeImage_MovePage", "@12" ),
	( "FreeImage_GetLockedPageNumbers", "@12" ),

	# Tags.
	( "FreeImage_GetTagValue", "@4" ),
	( "FreeImage_GetTagDescription", "@4", None, ctypes.c_char_p ),
	( "FreeImage_TagToString", "@12", None, ctypes.c_char_p ),
	( "FreeImage_GetTagCount", "@4", None, DWORD ),
	( "FreeImage_GetTagKey", "@4", None, ctypes.c_char_p ),
	( "FreeImage_GetTagID", "@4", None, ctypes.c_char_p ),
	( "FreeImage_GetTagType", "@4" ),


	# Metadatas.
	( "FreeImage_GetMetadata", "@16" ),
	( "FreeImage_GetMetadataCount", "@8", None, DWORD ),
	( "FreeImage_FindFirstMetadata", "@12", None, VOID ),
	( "FreeImage_FindNextMetadata", "@8", None, VOID ),
	( "FreeImage_FindCloseMetadata", "@4" ),

	( "FreeImage_IsLittleEndian", "@0" )

 )

#***********************************************************************************************
#***	Module Classes And Definitions
#***********************************************************************************************
class FreeImage( object ):
	'''
	This Class Provides Methods To Manipulate FreeImage libraryPath.
	'''

	_libraryInstance = None
	_libraryInstantiated = False

	@core.executionTrace
	def __new__( self, *args, **kwargs ):
		if self._libraryInstance is None:
			self._libraryInstance = object.__new__( self )
		return self._libraryInstance

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.LibraryInitializationError )
	def __init__( self, libraryPath ):
		'''
		This Method Initializes The Class.
		'''

		if self._libraryInstantiated :
			return

		LOGGER.debug( "> Initializing '{0}()' Class.".format( self.__class__.__name__ ) )

		self._libraryInstantiated = True

		# --- Setting Class Attributes. ---
		self._libraryPath = None
		self.libraryPath = libraryPath

		self._library = None

		if platform.system() == "Windows" or platform.system() == "Microsoft" :
			loadingFunction = ctypes.windll
		else:
			loadingFunction = ctypes.cdll

		if self.libraryPath :
			self._library = loadingFunction.LoadLibrary( libraryPath )
		else :
			raise foundations.exceptions.LibraryInitializationError, "'{0}' Library Not Found !".format( self.__class__.__name__ )

		self.bindLibrary()

	#***************************************************************************************
	#***	Attributes Properties
	#***************************************************************************************
	@property
	def libraryPath( self ):
		'''
		This Method Is The Property For The _libraryPath Attribute.
		
		@return: self._libraryPath. ( String )
		'''

		return self._libraryPath

	@libraryPath.setter
	@foundations.exceptions.exceptionsHandler( None, False, AssertionError )
	def libraryPath( self, value ):
		'''
		This Method Is The Setter Method For The _libraryPath Attribute.
		
		@param value: Attribute Value. ( String )
		'''

		if value :
			assert type( value ) in ( str, unicode ), "'{0}' Attribute : '{1}' Type Is Not 'str' or 'unicode' !".format( "libraryPath", value )
			assert os.path.exists( value ), "'{0}' Attribute : '{1}' File Doesn't Exists !".format( "libraryPath", value )
		self._libraryPath = value

	@libraryPath.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def libraryPath( self ):
		'''
		This Method Is The Deleter Method For The _libraryPath Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "libraryPath" ) )

	@property
	def library( self ):
		'''
		This Method Is The Property For The _library Attribute.
		
		@return: self._library. ( Object )
		'''

		return self._library

	@library.setter
	@foundations.exceptions.exceptionsHandler( None, False, AssertionError )
	def library( self, value ):
		'''
		This Method Is The Setter Method For The _library Attribute.
		
		@param value: Attribute Value. ( Object )
		'''

		self._library = value

	@library.deleter
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def library( self ):
		'''
		This Method Is The Deleter Method For The _library Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "library" ) )

	#***************************************************************************************
	#***	Class Methods
	#***************************************************************************************
	@core.executionTrace
	def bindFunction( self, function ):
		'''
		This Method Bind A Function.
		
		@param function: Function To Bind. ( Tuple )
		'''

		name, affixe = function[0:2]
		returnType = len( function ) == 4 and function[3] or None

		bindingName = name.split( "_", 1 )[1]

		if platform.system() == "Windows" or platform.system() == "Microsoft" :
			functionName = getattr( self._library, '_{0}{1}'.format( name, affixe ) )
		else:
			functionName = getattr( self._library, name )

		setattr( self, bindingName, functionName )

		if returnType :
			functionName.returnType = returnType

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, AttributeError )
	def bindLibrary( self ):
		'''
		This Method Bind The Library.
		'''

		for function in FREEIMAGE_FUNCTIONS:
			self.bindFunction( function )
#***********************************************************************************************
#***	Python End
#***********************************************************************************************
import sys
from globals.runtimeConstants import RuntimeConstants

# Starting The Console Handler.
RuntimeConstants.loggingConsoleHandler = logging.StreamHandler( sys.stdout )
RuntimeConstants.loggingConsoleHandler.setFormatter( core.LOGGING_FORMATTER )
LOGGER.addHandler( RuntimeConstants.loggingConsoleHandler )

freeImage = FreeImage( os.path.join( os.getcwd(), "..", Constants.freeImageLibrary ) )

print freeImage

freeImage2 = FreeImage( os.path.join( os.getcwd(), "..", Constants.freeImageLibrary ) )

print freeImage
