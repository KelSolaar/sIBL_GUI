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
***		Portions Of The Code Are Taken From FreeImagePy By Michele Petrazzo : http://freeimagepy.sourceforge.net/.
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
import sys
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

BYTE_P = ctypes.POINTER( BYTE )

'''
System Endian.
'''
if sys.byteorder == "big" :
	FREEIMAGE_BIGENDIAN = 1
else :
	FREEIMAGE_BIGENDIAN = 0

FREEIMAGE_COLORORDER_BGR = 0
FREEIMAGE_COLORORDER_RGB = 1

if FREEIMAGE_BIGENDIAN :
	FREEIMAGE_COLORORDER = FREEIMAGE_COLORORDER_RGB
else :
	FREEIMAGE_COLORORDER = FREEIMAGE_COLORORDER_BGR

class RGBQUAD( ctypes.Structure ):
	'''
	This Class Is The RGBQUAD Class.
	'''

	_fields_ = []
	if FREEIMAGE_COLORORDER == FREEIMAGE_COLORORDER_BGR :
		_fields_ += [( "rgbBlue", BYTE ),
					 ( "rgbGreen", BYTE ),
					 ( "rgbRed", BYTE )]
	else:
		_fields_ += [( "rgbRed", BYTE ),
					 ( "rgbGreen", BYTE ),
					 ( "rgbBlue", BYTE )]

	_fields_ += [ ( "rgbReserved", BYTE ) ]

class RGBTRIPLE( ctypes.Structure ):
	'''
	This Class Is The RGBTRIPLE Class.
	'''

	_fields_ = []
	if FREEIMAGE_COLORORDER == FREEIMAGE_COLORORDER_BGR :
		_fields_ += [( "rgbBlue", BYTE ),
					( "rgbGreen", BYTE ),
					( "rgbRed", BYTE )]
	else:
		_fields_ += [( "rgbRed", BYTE ),
					( "rgbGreen", BYTE ),
					( "rgbBlue", BYTE )]

class FIBITMAP( ctypes.Structure ):
	'''
	This Class Is The FIBITMAP Class.
	'''

	_fields_ = [ ( "data", ctypes.POINTER( VOID ) ) ]

class BITMAPINFOHEADER( ctypes.Structure ):
	'''
	This Class Is The BITMAPINFOHEADER Class.
	'''

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
				 ( "biClrImportant", DWORD ) ]

class BITMAPINFO( ctypes.Structure ):
	'''
	This Class Is The BITMAPINFO Class.
	'''

	_fields_ = [ ( "bmiHeader", BITMAPINFOHEADER ),
				( "bmiColors[1]", RGBQUAD ) ]

class FIRGB16( ctypes.Structure ):
	'''
	This Class Is The FIRGB16 Class.
	'''

	_fields_ = [ ( "red", WORD ),
				( "green", WORD ),
				( "blue", WORD ) ]

class FIRGBA16( ctypes.Structure ):
	'''
	This Class Is The FIRGBA16 Class.
	'''

	_fields_ = [ ( "red", WORD ),
				( "green", WORD ),
				( "blue", WORD ),
				( "alpha", WORD ) ]

class FIRGBF( ctypes.Structure ):
	'''
	This Class Is The FIRGBF Class.
	'''

	_fields_ = [ ( "red", ctypes.c_float ),
				( "green", ctypes.c_float ),
				( "blue", ctypes.c_float ) ]

class FIRGBAF( ctypes.Structure ):
	'''
	This Class Is The FIRGBAF Class.
	'''

	_fields_ = [ ( "red", ctypes.c_float ),
				( "green", ctypes.c_float ),
				( "blue", ctypes.c_float ),
				( "alpha", ctypes.c_float ) ]

class FICOMPLEX( ctypes.Structure ):
	'''
	This Class Is The FICOMPLEX Class.
	'''

	_fields_ = [ ( "r", ctypes.c_double ),
				( "i", ctypes.c_double ) ]

'''
Indexes For Byte Arrays, Masks And Shifts For Treating Pixels As Words.
'''
if FREEIMAGE_BIGENDIAN :
	# Little Endian ( x86 / MS Windows, Linux ) : BGR(A) Order.
	if FREEIMAGE_COLORORDER == FREEIMAGE_COLORORDER_BGR:
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
		# Little Endian ( x86 / MaxOSX ) : RGB(A) Order.
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
else :
	if FREEIMAGE_COLORORDER == FREEIMAGE_COLORORDER_BGR :
		# Big Endian ( PPC / none ) : BGR(A) Order.
		FI_RGBA_RED			 = 2
		FI_RGBA_GREEN		 = 1
		FI_RGBA_BLUE		 = 0
		FI_RGBA_ALPHA		 = 3
		FI_RGBA_RED_MASK	 = 0x0000FF00
		FI_RGBA_GREEN_MASK	 = 0x00FF0000
		FI_RGBA_BLUE_MASK	 = 0xFF000000
		FI_RGBA_ALPHA_MASK	 = 0x000000FF
		FI_RGBA_RED_SHIFT	 = 8
		FI_RGBA_GREEN_SHIFT	 = 16
		FI_RGBA_BLUE_SHIFT	 = 24
		FI_RGBA_ALPHA_SHIFT	 = 0
	else :
		#Big Endian ( PPC / Linux, MaxOSX ) : RGB(A) Order.
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
		FI_RGBA_BLUE_SHIFT 	 = 8
		FI_RGBA_ALPHA_SHIFT	 = 0

FI_RGBA_RGB_MASK = ( FI_RGBA_RED_MASK | FI_RGBA_GREEN_MASK | FI_RGBA_BLUE_MASK )

FI16_555_RED_MASK		 = 0x7C00
FI16_555_GREEN_MASK		 = 0x03E0
FI16_555_BLUE_MASK		 = 0x001F
FI16_555_RED_SHIFT		 = 10
FI16_555_GREEN_SHIFT	 = 5
FI16_555_BLUE_SHIFT		 = 0
FI16_565_RED_MASK		 = 0xF800
FI16_565_GREEN_MASK		 = 0x07E0
FI16_565_BLUE_MASK		 = 0x001F
FI16_565_RED_SHIFT		 = 11
FI16_565_GREEN_SHIFT	 = 5
FI16_565_BLUE_SHIFT		 = 0

'''
ICC Profile Support
'''
FIICC_DEFAULT			 = 0x00
FIICC_COLOR_IS_CMYK		 = 0x01

class FIICCPROFILE( ctypes.Structure ):
	_fields_ = [ ( "flags", WORD ),
				( "size", DWORD ),
				( "data", VOID ) ]

class FREE_IMAGE_FORMAT( object ):
	'''
	This Class Is Used For I/O Image Format Identifiers.
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
	FIF_MUTLIPAGE = ( FIF_TIFF, FIF_ICO, FIF_GIF )

class FREE_IMAGE_TYPE( object ):
	'''
	This Class Is Used For Images Types.
	'''

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

class FREE_IMAGE_COLOR_TYPE( object ):
	'''
	This Class Is Used For Image Color Types.
	'''

	FIC_MINISWHITE = 0
	FIC_MINISBLACK = 1
	FIC_RGB = 2
	FIC_PALETTE = 3
	FIC_RGBALPHA = 4
	FIC_CMYK = 5

class FREE_IMAGE_QUANTIZE( object ):
	'''
	This Class Is Used For Color Quantization Algorithms.
	'''

	FIQ_WUQUANT = 0
	FIQ_NNQUANT = 1

class FREE_IMAGE_DITHER( object ):
	'''
	This Class Is Used For Dithering Algorithms.
	'''

	FID_FS		 	 = 0
	FID_BAYER4x4	 = 1
	FID_BAYER8x8	 = 2
	FID_CLUSTER6x6	 = 3
	FID_CLUSTER8x8	 = 4
	FID_CLUSTER16x16 = 5
	FID_BAYER16x16 	 = 6

class FREE_IMAGE_JPEG_OPERATION( object ):
	'''
	This Class Is Used For Lossless JPEG Transformations.
	'''

	FIJPEG_OP_NONE			 = 0
	FIJPEG_OP_FLIP_H		 = 1
	FIJPEG_OP_FLIP_V		 = 2
	FIJPEG_OP_TRANSPOSE		 = 3
	FIJPEG_OP_TRANSVERSE	 = 4
	FIJPEG_OP_ROTATE_90		 = 5
	FIJPEG_OP_ROTATE_180	 = 6
	FIJPEG_OP_ROTATE_270	 = 7

class FREE_IMAGE_TMO( object ):
	'''
	This Class Is Used For Tone Mapping Operators.
	'''

	FITMO_DRAGO03	 = 0
	FITMO_REINHARD05 = 1
	FITMO_FATTAL02	 = 2

class FREE_IMAGE_FILTER( object ):
	'''
	This Class Is Used For Upsampling / Downsampling Filters.
	'''

	FILTER_BOX			 = 0
	FILTER_BICUBIC		 = 1
	FILTER_BILINEAR		 = 2
	FILTER_BSPLINE		 = 3
	FILTER_CATMULLROM	 = 4
	FILTER_LANCZOS3		 = 5

class FREE_IMAGE_COLOR_CHANNEL( object ):
	'''
	This Class Is Used For Color Channels.
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

class FREE_IMAGE_MDTYPE( object ):
	'''
	This Class Is Used For Tags Data Types Informations.
	'''

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

	FIDTToType = { FIDT_NOTYPE : VOID,
				FIDT_BYTE : ctypes.c_ubyte,
				FIDT_ASCII : ctypes.c_char_p,
				FIDT_SHORT : ctypes.c_ushort,
				FIDT_LONG : ctypes.c_uint,
				FIDT_RATIONAL: ctypes.c_ulong,
				FIDT_SBYTE : ctypes.c_short,
				FIDT_UNDEFINED : VOID,
				FIDT_SSHORT : ctypes.c_short,
				FIDT_SLONG : ctypes.c_long,
				FIDT_SRATIONAL : ctypes.c_long,
				FIDT_FLOAT : ctypes.c_float,
				FIDT_DOUBLE : ctypes.c_double,
				FIDT_IFD : ctypes.c_uint,
				FIDT_PALETTE : RGBQUAD }

class FREE_IMAGE_MDMODEL( object ):
	'''
	This Class Is Used For Metadatas Models.
	'''
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

class FIMETADATA( ctypes.Structure ) :
	'''
	This Class Is A Handle To A Metadata Model.
	'''

	_fields_ = [ ( "data", VOID ), ]

class FITAG( ctypes.Structure ):
	'''
	This Class Is A Handle To A FreeImage Tag.
	'''

	_fields_ = [ ( "data", VOID ) ]

'''
File IO Routines.
'''

fi_handle = ctypes.c_void_p

FI_ReadProc = DLL_CALLCONV( ctypes.c_uint, BYTE_P, ctypes.c_uint, ctypes.c_uint, fi_handle )
FI_WriteProc = DLL_CALLCONV( ctypes.c_uint, BYTE_P, ctypes.c_uint, ctypes.c_uint, fi_handle )
FI_SeekProc = DLL_CALLCONV( ctypes.c_int, fi_handle, ctypes.c_long, ctypes.c_int )
FI_TellProc = DLL_CALLCONV( ctypes.c_long, fi_handle )

class FreeImageIO( ctypes.Structure ):
	'''
	This Class Is The FreeImageIO Class.
	'''

	_fields_ = [ ( 'read_proc', FI_ReadProc ),
                ( 'write_proc', FI_WriteProc ),
                ( 'seek_proc', FI_SeekProc ),
                ( 'tell_proc', FI_TellProc ) ]

class FIMEMORY( ctypes.Structure ):
	'''
	This Class Is A Handle To A Memory I/O stream
	'''

	_fields_ = [ ( "data", VOID ) ]

'''
Load / Save Flag Constants.
'''
BMP_DEFAULT					 = 0
BMP_SAVE_RLE				 = 1
CUT_DEFAULT					 = 0
DDS_DEFAULT			 		 = 0
EXR_DEFAULT					 = 0
EXR_FLOAT					 = 0x0001
EXR_NONE	 				 = 0x0002
EXR_ZIP		 				 = 0x0004
EXR_PIZ						 = 0x0008
EXR_PXR24	 				 = 0x0010
EXR_B44						 = 0x0020
EXR_LC						 = 0x0040
FAXG3_DEFAULT				 = 0
GIF_DEFAULT					 = 0
GIF_LOAD256					 = 1
GIF_PLAYBACK	 			 = 2
HDR_DEFAULT					 = 0
ICO_DEFAULT					 = 0
ICO_MAKEALPHA				 = 1
IFF_DEFAULT					 = 0
J2K_DEFAULT					 = 0
JP2_DEFAULT			 		 = 0
JPEG_DEFAULT 				 = 0
JPEG_FAST 					 = 0x0001
JPEG_ACCURATE 				 = 0x0002
JPEG_CMYK			 		 = 0x0004
JPEG_EXIFROTATE		 		 = 0x0008
JPEG_QUALITYSUPERB 			 = 0x80
JPEG_QUALITYGOOD 			 = 0x0100
JPEG_QUALITYNORMAL 			 = 0x0200
JPEG_QUALITYAVERAGE 		 = 0x0400
JPEG_QUALITYBAD 			 = 0x0800
JPEG_PROGRESSIVE	 		 = 0x2000
JPEG_SUBSAMPLING_411 		 = 0x1000
JPEG_SUBSAMPLING_420		 = 0x4000
JPEG_SUBSAMPLING_422 		 = 0x8000
JPEG_SUBSAMPLING_444 		 = 0x10000
KOALA_DEFAULT				 = 0
LBM_DEFAULT					 = 0
MNG_DEFAULT					 = 0
PCD_DEFAULT					 = 0
PCD_BASE					 = 1
PCD_BASEDIV4				 = 2
PCD_BASEDIV16				 = 3
PCX_DEFAULT			 		 = 0
PFM_DEFAULT			 		 = 0
PICT_DEFAULT		 		 = 0
PNG_DEFAULT		 			 = 0
PNG_IGNOREGAMMA	 			 = 1
PNG_Z_BEST_SPEED			 = 0x0001
PNG_Z_DEFAULT_COMPRESSION	 = 0x0006
PNG_Z_BEST_COMPRESSION		 = 0x0009
PNG_Z_NO_COMPRESSION		 = 0x0100
PNG_INTERLACED				 = 0x0200
PNM_DEFAULT			 		 = 0
PNM_SAVE_RAW		 		 = 0
PNM_SAVE_ASCII		 		 = 1
PSD_DEFAULT			 		 = 0
RAS_DEFAULT			 		 = 0
RAW_DEFAULT			 		 = 0
RAW_PREVIEW			 		 = 1
RAW_DISPLAY			 		 = 2
SGI_DEFAULT			 		 = 0
TARGA_DEFAULT 		 		 = 0
TARGA_LOAD_RGB888	 		 = 1
TIFF_DEFAULT		 		 = 0
TIFF_CMYK			 		 = 0x0001
TIFF_NONE			 		 = 0x0800
TIFF_PACKBITS		 		 = 0x0100
TIFF_DEFLATE		 		 = 0x0200
TIFF_ADOBE_DEFLATE	 		 = 0x0400
TIFF_CCITTFAX3		 		 = 0x1000
TIFF_CCITTFAX4		 		 = 0x2000
TIFF_LZW					 = 0x4000
TIFF_JPEG			 		 = 0x8000
WBMP_DEFAULT		 		 = 0
XBM_DEFAULT					 = 0
XPM_DEFAULT					 = 0

'''
Background Filling Options.
'''
FI_COLOR_IS_RGB_COLOR			 = 0x00
FI_COLOR_IS_RGBA_COLOR			 = 0x01
FI_COLOR_FIND_EQUAL_COLOR		 = 0x02
FI_COLOR_ALPHA_IS_INDEX			 = 0x04
FI_COLOR_PALETTE_SEARCH_MASK	 = ( FI_COLOR_FIND_EQUAL_COLOR | FI_COLOR_ALPHA_IS_INDEX )

'''
Extension To Type.
'''
EXTToType = dict( bmp = ( FREE_IMAGE_FORMAT.FIF_BMP, BMP_DEFAULT, '.bmp' ),
				ico = ( FREE_IMAGE_FORMAT.FIF_ICO, ICO_DEFAULT, '.ico' ),
				gif = ( FREE_IMAGE_FORMAT.FIF_GIF, GIF_DEFAULT, '.gif' ),
				jpeg = ( FREE_IMAGE_FORMAT.FIF_JPEG, JPEG_DEFAULT, '.jpg' ),
				jpegfa = ( FREE_IMAGE_FORMAT.FIF_JPEG, JPEG_FAST, '.jpg' ),
				jpegac = ( FREE_IMAGE_FORMAT.FIF_JPEG, JPEG_ACCURATE, '.jpg' ),
				jpegsu = ( FREE_IMAGE_FORMAT.FIF_JPEG, JPEG_QUALITYSUPERB, '.jpg' ),
				jpeggo = ( FREE_IMAGE_FORMAT.FIF_JPEG, JPEG_QUALITYGOOD, '.jpg' ),
				jpegav = ( FREE_IMAGE_FORMAT.FIF_JPEG, JPEG_QUALITYAVERAGE, '.jpg' ),
				jpegba = ( FREE_IMAGE_FORMAT.FIF_JPEG, JPEG_QUALITYBAD, '.jpg' ),
				pbm = ( FREE_IMAGE_FORMAT.FIF_PBM, PNM_DEFAULT, '.pbm' ),
				pgm = ( FREE_IMAGE_FORMAT.FIF_PGM, PNM_DEFAULT, '.pgm' ),
				png = ( FREE_IMAGE_FORMAT.FIF_PNG, PNG_DEFAULT, '.png' ),
				pnm = ( FREE_IMAGE_FORMAT.FIF_PPM, PNM_DEFAULT, '.pnm' ),
				ppm = ( FREE_IMAGE_FORMAT.FIF_PPM, PNM_DEFAULT, '.ppm' ),
				tiff = ( FREE_IMAGE_FORMAT.FIF_TIFF, TIFF_DEFAULT, '.tif' ),
				tiffg3 = ( FREE_IMAGE_FORMAT.FIF_TIFF, TIFF_CCITTFAX3, '.tif' ),
				tiffg4 = ( FREE_IMAGE_FORMAT.FIF_TIFF, TIFF_CCITTFAX4, '.tif' ),
				tiffno = ( FREE_IMAGE_FORMAT.FIF_TIFF, TIFF_NONE, '.tif' ) )

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

FREEIMAGE_FUNCTIONS = ( 

	# Initialization Functions.
	( "FreeImage_Initialise", "@4" ),
	( "FreeImage_DeInitialise", "@0" ),

	# Version Functions.
	( "FreeImage_GetVersion", "@0", None, ctypes.c_char_p ),
	( "FreeImage_GetCopyrightMessage", "@0", None, ctypes.c_char_p ),

	# Message Output Functions.
	# ( "FreeImage_SetOutputMessageStdCall", "@0" ),
	( "FreeImage_SetOutputMessage", "@4" ),
	# ( "FreeImage_OutputMessageProc", "@0" ),

	# Allocate / Clone / Unload Functions.
	( "FreeImage_Allocate", "@24", COL_1TO32 ),
	( "FreeImage_AllocateT", "@28" ),
	( "FreeImage_Clone", "@4" ),
	( "FreeImage_Unload", "@4" ),

	# Load / Save Unload Functions.
	( "FreeImage_Load", "@12" ),
	( "FreeImage_LoadU", "@12" ),
	( "FreeImage_LoadFromHandle", "@16" ),
	( "FreeImage_Save", "@16" ),
	( "FreeImage_SaveU", "@16" ),
	( "FreeImage_SaveToHandle", "@20" ),

	# Memory I/O Stream Functions.
	# ( "FreeImage_OpenMemory", "@0" ),
	# ( "FreeImage_CloseMemory", "@0" ),
	# ( "FreeImage_LoadFromMemory", "@0" ),
	# ( "FreeImage_SaveToMemory", "@0" ),
	# ( "FreeImage_TellMemory", "@0" ),
	# ( "FreeImage_SeekMemory", "@0" ),
	# ( "FreeImage_AcquireMemory", "@0" ),
	# ( "FreeImage_ReadMemory", "@0" ),
	# ( "FreeImage_WriteMemory", "@0" ),
	# ( "FreeImage_LoadMultiBitmapFromMemory", "@0" ),

	# Plugin Interface Functions.
	( "FreeImage_RegisterLocalPlugin", "@20" ),
	# ( "FreeImage_RegisterExternalPlugin", "@0" ),
	( "FreeImage_GetFIFCount", "@0" ),
	( "FreeImage_SetPluginEnabled", "@8" ),
	( "FreeImage_IsPluginEnabled", "@4" ),
	( "FreeImage_GetFIFFromFormat", "@4", None, ctypes.c_char_p ),
	( "FreeImage_GetFIFFromMime", "@4", None, ctypes.c_char_p ),
	( "FreeImage_GetFormatFromFIF", "@4", None, ctypes.c_char_p ),
	( "FreeImage_GetFIFExtensionList", "@4", None, ctypes.c_char_p ),
	( "FreeImage_GetFIFDescription", "@4", None, ctypes.c_char_p ),
	( "FreeImage_GetFIFRegExpr", "@4", None, ctypes.c_char_p ),
	( "FreeImage_GetFIFMimeType", "@4", None, ctypes.c_char_p ),
	( "FreeImage_GetFIFFromFilename", "@4" ),
	( "FreeImage_GetFIFFromFilenameU", "@4" ),
	( "FreeImage_FIFSupportsReading", "@4" ),
	( "FreeImage_FIFSupportsWriting", "@4" ),
	( "FreeImage_FIFSupportsExportBPP", "@8" ),
	( "FreeImage_FIFSupportsExportType", "@8" ),
	( "FreeImage_FIFSupportsICCProfiles", "@4" ),

	# Multipaging Functions.
	( "FreeImage_OpenMultiBitmap", "@24" ),
	# ( "FreeImage_OpenMultiBitmapFromHandle", "@0" ),
	( "FreeImage_CloseMultiBitmap", "@8" ),
	( "FreeImage_GetPageCount", "@4" ),
	( "FreeImage_AppendPage", "@8" ),
	( "FreeImage_InsertPage", "@12" ),
	( "FreeImage_DeletePage", "@8" ),
	( "FreeImage_LockPage", "@8" ),
	( "FreeImage_UnlockPage", "@12" ),
	( "FreeImage_MovePage", "@12" ),
	( "FreeImage_GetLockedPageNumbers", "@12" ),

	# File Type Request Functions.
	( "FreeImage_GetFileType", "@8" ),
	( "FreeImage_GetFileTypeU", "@8" ),
	( "FreeImage_GetFileTypeFromHandle", "@12" ),
	# ( "FreeImage_GetFileTypeFromMemory", "@0" ),

	# Image Type Request Functions.
	( "FreeImage_GetImageType", "@4" ),

	# FreeImage Helper Functions.
	( "FreeImage_IsLittleEndian", "@0" )
	# ( "FreeImage_LookupX11Color", "@0" ),
	# ( "FreeImage_LookupSVGColor", "@0" ),

	# Pixel Access Functions.
	( "FreeImage_GetBits", "@4", None, ctypes.POINTER( BYTE ) ),
	( "FreeImage_GetScanLine", "@8", None, ctypes.POINTER( BYTE ) ),
	( "FreeImage_GetPixelIndex", "@16", COL_1TO8 ),
	( "FreeImage_GetPixelColor", "@16", COL_16TO32 ),
	( "FreeImage_SetPixelIndex", "@16", COL_1TO8 ),
	( "FreeImage_SetPixelColor", "@16", COL_16TO32 ),

	# DIB Informations Functions.
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
	( "FreeImage_GetInfoHeader", "@4", COL_1TO32, ctypes.POINTER( BITMAPINFOHEADER ) ),
	# ( "FreeImage_GetInfo", "@0" ),
	( "FreeImage_GetColorType", "@4", COL_1TO32 ),
	( "FreeImage_GetRedMask", "@4", COL_1TO32 ),
	( "FreeImage_GetGreenMask", "@4", COL_1TO32 ),
	( "FreeImage_GetBlueMask", "@4", COL_1TO32 ),
	( "FreeImage_GetTransparencyCount", "@4", COL_1TO32 ),
	( "FreeImage_GetTransparencyTable", "@4", ( COL_8, ), ctypes.POINTER( BYTE ) ),
	( "FreeImage_SetTransparencyTable", "@12", ( COL_8, ) ),
	( "FreeImage_IsTransparent", "@4", COL_1TO32 ),
	( "FreeImage_SetTransparent", "@8", ( COL_8, COL_32 ) ),
	# ( "FreeImage_SetTransparentIndex", "@0" ),
	# ( "FreeImage_GetTransparentIndex", "@0" ),
	( "FreeImage_HasBackgroundColor", "@4", ( COL_8, COL_24, COL_32 ) ),
	( "FreeImage_GetBackgroundColor", "@8", ( COL_8, COL_24, COL_32 ), ctypes.POINTER( RGBQUAD ) ),
	( "FreeImage_SetBackgroundColor", "@8", ( COL_8, COL_24, COL_32 ) ),

	# ICC Profile Functions.
	# ( "FreeImage_GetICCProfile", "@0" ),
	# ( "FreeImage_CreateICCProfile", "@0" ),
	# ( "FreeImage_DestroyICCProfile", "@0" ),

	# Line Conversion Functions.
	# ( "FreeImage_ConvertLine1To4", "@0" ),
	# ( "FreeImage_ConvertLine8To4", "@0" ),
	# ( "FreeImage_ConvertLine16To4_555", "@0" ),
	# ( "FreeImage_ConvertLine16To4_565", "@0" ),
	# ( "FreeImage_ConvertLine24To4", "@0" ),
	# ( "FreeImage_ConvertLine32To4", "@0" ),
	# ( "FreeImage_ConvertLine1To8", "@0" ),
	# ( "FreeImage_ConvertLine4To8", "@0" ),
	# ( "FreeImage_ConvertLine16To8_555", "@0" ),
	# ( "FreeImage_ConvertLine16To8_565", "@0" ),
	# ( "FreeImage_ConvertLine24To8", "@0" ),
	# ( "FreeImage_ConvertLine32To8", "@0" ),
	# ( "FreeImage_ConvertLine1To16_555", "@0" ),
	# ( "FreeImage_ConvertLine4To16_555", "@0" ),
	# ( "FreeImage_ConvertLine8To16_555", "@0" ),
	# ( "FreeImage_ConvertLine16_565_To16_555", "@0" ),
	# ( "FreeImage_ConvertLine24To16_555", "@0" ),
	# ( "FreeImage_ConvertLine32To16_555", "@0" ),
	# ( "FreeImage_ConvertLine1To16_565", "@0" ),
	# ( "FreeImage_ConvertLine4To16_565", "@0" ),
	# ( "FreeImage_ConvertLine8To16_565", "@0" ),
	# ( "FreeImage_ConvertLine16_555_To16_565", "@0" ),
	# ( "FreeImage_ConvertLine24To16_565", "@0" ),
	# ( "FreeImage_ConvertLine32To16_565", "@0" ),
	# ( "FreeImage_ConvertLine1To24", "@0" ),
	# ( "FreeImage_ConvertLine4To24", "@0" ),
	# ( "FreeImage_ConvertLine8To24", "@0" ),
	# ( "FreeImage_ConvertLine16To24_555", "@0" ),
	# ( "FreeImage_ConvertLine16To24_565", "@0" ),
	# ( "FreeImage_ConvertLine32To24", "@0" ),
	# ( "FreeImage_ConvertLine1To32", "@0" ),
	# ( "FreeImage_ConvertLine4To32", "@0" ),
	# ( "FreeImage_ConvertLine8To32", "@0" ),
	# ( "FreeImage_ConvertLine16To32_555", "@0" ),
	# ( "FreeImage_ConvertLine16To32_565", "@0" ),
	# ( "FreeImage_ConvertLine24To32", "@0" ),

	# Smart Conversion Functions.
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
	( "FreeImage_ConvertToRGBF", "@4", ( COL_24, COL_32, ) ),
	( "FreeImage_ConvertToRawBits", "@32", COL_1TO32 ),
	( "FreeImage_ConvertToStandardType", "@8" ),
	( "FreeImage_ConvertToType", "@12" ),

	# Tone Mapping Operators Functions.
	# ( "FreeImage_ToneMapping", "@0" ),
	# ( "FreeImage_TmoDrago03", "@0" ),
	# ( "FreeImage_TmoReinhard05", "@0" ),
	# ( "FreeImage_TmoReinhard05Ex", "@0" ),
	# ( "FreeImage_TmoFattal02", "@0" ),

	# ZLib Functions.
	# ( "FreeImage_ZLibCompress", "@0" ),
	# ( "FreeImage_ZLibUncompress", "@0" ),
	# ( "FreeImage_ZLibGZip", "@0" ),
	# ( "FreeImage_ZLibGUnzip", "@0" ),
	# ( "FreeImage_ZLibCRC32", "@0" ),

	# Tags Creation / Destruction Functions.
	# ( "FreeImage_CreateTag", "@0" ),
	# ( "FreeImage_DeleteTag", "@0" ),
	# ( "FreeImage_CloneTag", "@0" ),

	# Tags Getters / Setters Functions.
	( "FreeImage_GetTagKey", "@4", None, ctypes.c_char_p ),
	( "FreeImage_GetTagDescription", "@4", None, ctypes.c_char_p ),
	( "FreeImage_GetTagID", "@4", None, ctypes.c_char_p ),
	( "FreeImage_GetTagType", "@4" ),
	( "FreeImage_GetTagCount", "@4", None, DWORD ),
	# ( "FreeImage_GetTagLength", "@0" ),
	( "FreeImage_GetTagValue", "@4" ),
	# ( "FreeImage_SetTagKey", "@0" ),
	# ( "FreeImage_SetTagDescription", "@0" ),
	# ( "FreeImage_SetTagID", "@0" ),
	# ( "FreeImage_SetTagType", "@0" ),
	# ( "FreeImage_SetTagCount", "@0" ),
	# ( "FreeImage_SetTagLength", "@0" ),
	# ( "FreeImage_SetTagValue", "@0" ),

	# Iterator Functions.
	( "FreeImage_FindFirstMetadata", "@12", None, VOID ),
	( "FreeImage_FindNextMetadata", "@8", None, VOID ),
	( "FreeImage_FindCloseMetadata", "@4" ),

	# Metadatas Getters / Setters Functions.
	# ( "FreeImage_SetMetadata", "@0" ),
	( "FreeImage_GetMetadata", "@16" ),
	( "FreeImage_GetMetadataCount", "@8", None, DWORD ),
	# ( "FreeImage_CloneMetadata", "@0" ),

	# Tag To C String Conversion Function.
	( "FreeImage_TagToString", "@12", None, ctypes.c_char_p ),

	# Rotation and Flipping Functions.
	( "FreeImage_RotateClassic", "@12", COL_1TO32 ),
	# ( "FreeImage_Rotate", "@0" ),
	( "FreeImage_RotateEx", "@48", ( COL_8, COL_24, COL_32 ), ),
	# ( "FreeImage_FlipHorizontal", "@0" ),
	# ( "FreeImage_FlipVertical", "@0" ),
	# ( "FreeImage_JPEGTransform", "@0" ),
	# ( "FreeImage_JPEGTransformU", "@0" ),

	# Upsampling / Downsampling Functions.
	( "FreeImage_Rescale", "@16", COL_1TO32 ),
	( "FreeImage_MakeThumbnail", "@12", COL_1TO32 ),

	# Color Manipulation Functions.
	( "FreeImage_AdjustCurve", "@12", ( COL_8, COL_24, COL_32 ), BOOL ),
	( "FreeImage_AdjustGamma", "@12", ( COL_8, COL_24, COL_32 ), BOOL ),
	( "FreeImage_AdjustBrightness", "@12", ( COL_8, COL_24, COL_32 ), BOOL ),
	( "FreeImage_AdjustContrast", "@12", ( COL_8, COL_24, COL_32 ), BOOL ),
	( "FreeImage_Invert", "@4", COL_1TO32, BOOL ),
	( "FreeImage_GetHistogram", "@12", ( COL_8, COL_24, COL_32 ), BOOL ),
	# ( "FreeImage_GetAdjustColorsLookupTable", "@0" ),
	# ( "FreeImage_AdjustColors", "@0" ),
	# ( "FreeImage_ApplyColorMapping", "@0" ),
	# ( "FreeImage_SwapColors", "@0" ),
	# ( "FreeImage_ApplyPaletteIndexMapping", "@0" ),
	# ( "FreeImage_SwapPaletteIndices", "@0" ),

	# Channel Processing Functions.
	( "FreeImage_GetChannel", "@8", ( COL_24, COL_32 ) ),
	( "FreeImage_SetChannel", "@12", ( COL_24, COL_32 ) ),
	( "FreeImage_GetComplexChannel", "@8" ),
	( "FreeImage_SetComplexChannel", "@12" ),

	# Copy / Paste / Composite Functions.
	( "FreeImage_Copy", "@20" ),
	( "FreeImage_Paste", "@20", COL_1TO32 ),
	# ( "FreeImage_Composite", "@0" ),
	# ( "FreeImage_JPEGCrop", "@0" ),
	# ( "FreeImage_JPEGCropU", "@0" ),
	# ( "FreeImage_PreMultiplyWithAlpha", "@0" ),

	# Background Filling Functions.
	# ( "FreeImage_FillBackground", "@0" ),
	# ( "FreeImage_EnlargeCanvas", "@0" ),
	# ( "FreeImage_AllocateEx", "@0" ),
	# ( "FreeImage_AllocateExT", "@0" ),

	# Miscellaneous Algorithms Functions.
	# ( "FreeImage_MultigridPoissonSolver", "@0" ),
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
	@foundations.exceptions.exceptionsHandler( None, False, AttributeError )
	def bindLibrary( self ):
		'''
		This Method Bind The Library.
		'''

		for function in FREEIMAGE_FUNCTIONS:
			self.bindFunction( function )

	@core.executionTrace
	def bindFunction( self, function ):
		'''
		This Method Bind A Function.
		
		@param function: Function To Bind. ( Tuple )
		'''

		LOGGER.debug( "> Binding '{0}' Library '{1}' Function.".format( self.__class__.__name__, function ) )

		name, affixe = function[0:2]
		returnType = len( function ) == 4 and function[3] or None

		bindingName = name.split( "_", 1 )[1]

		if platform.system() == "Windows" or platform.system() == "Microsoft" :
			functionName = getattr( self._library, '_{0}{1}'.format( name, affixe ) )
		else:
			functionName = getattr( self._library, name )

		setattr( self, bindingName, functionName )

		if returnType :
			functionName.restype = returnType

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

print freeImage.GetVersion()
