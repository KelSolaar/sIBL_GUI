#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**freeImage.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module provides FreeImage library ( http://freeimage.sourceforge.net/ ) bindings.

**Others:**
	Portions of the code from FreeImagePy by Michele Petrazzo: http://freeimagepy.sourceforge.net/.
"""

#***********************************************************************************************
#***	External imports.
#***********************************************************************************************
import ctypes
import logging
import os
import platform
import sys

#***********************************************************************************************
#***	Internal imports.
#***********************************************************************************************
import foundations.core as core
import foundations.exceptions
import foundations.library
from foundations.library import LibraryHook
from umbra.globals.constants import Constants

#***********************************************************************************************
#***	Module attributes.
#***********************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2011 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

LOGGER = logging.getLogger(Constants.logger)

#***********************************************************************************************
#***	FreeImage variables.
#***********************************************************************************************
FREEIMAGE_LIBRARY_PATH = os.path.join(os.getcwd(), Constants.freeImageLibrary)

if platform.system() == "Windows" or platform.system() == "Microsoft":
	DLL_CALLCONV = ctypes.WINFUNCTYPE
else:
	DLL_CALLCONV = ctypes.CFUNCTYPE

"""
Internal types.
"""
VOID	 = ctypes.c_void_p
INT		 = ctypes.c_int
BOOL	 = ctypes.c_long
BYTE	 = ctypes.c_ubyte
WORD	 = ctypes.c_ushort
DWORD	 = ctypes.c_ulong
LONG	 = ctypes.c_long
DOUBLE	 = ctypes.c_double

BYTE_P = ctypes.POINTER(BYTE)

"""
System endian.
"""
if sys.byteorder == "big":
	FREEIMAGE_BIGENDIAN = 1
else:
	FREEIMAGE_BIGENDIAN = 0

FREEIMAGE_COLORORDER_BGR = 0
FREEIMAGE_COLORORDER_RGB = 1

if FREEIMAGE_BIGENDIAN:
	FREEIMAGE_COLORORDER = FREEIMAGE_COLORORDER_RGB
else:
	FREEIMAGE_COLORORDER = FREEIMAGE_COLORORDER_BGR

class RGBQUAD(ctypes.Structure):
	"""
	This class is a :class:`ctypes.Structure` subclass representing FreeImage **RGBQUAD** C / C++ object.
	"""

	_fields_ = []
	if FREEIMAGE_COLORORDER == FREEIMAGE_COLORORDER_BGR:
		_fields_ += [("rgbBlue", BYTE),
					 ("rgbGreen", BYTE),
					 ("rgbRed", BYTE)]
	else:
		_fields_ += [("rgbRed", BYTE),
					 ("rgbGreen", BYTE),
					 ("rgbBlue", BYTE)]

	_fields_ += [("rgbReserved", BYTE)]

class RGBTRIPLE(ctypes.Structure):
	"""
	This class is a :class:`ctypes.Structure` subclass representing FreeImage **RGBTRIPLE** C / C++ object.
	"""

	_fields_ = []
	if FREEIMAGE_COLORORDER == FREEIMAGE_COLORORDER_BGR:
		_fields_ += [("rgbBlue", BYTE),
					("rgbGreen", BYTE),
					("rgbRed", BYTE)]
	else:
		_fields_ += [("rgbRed", BYTE),
					("rgbGreen", BYTE),
					("rgbBlue", BYTE)]

class FIBITMAP(ctypes.Structure):
	"""
	This class is a :class:`ctypes.Structure` subclass representing FreeImage **FIBITMAP** C / C++ object.
	"""

	_fields_ = [("data", ctypes.POINTER(VOID))]

class BITMAPINFOHEADER(ctypes.Structure):
	"""
	This class is a :class:`ctypes.Structure` subclass representing FreeImage **BITMAPINFOHEADER** C / C++ object.
	"""

	_fields_ = [("biSize", DWORD),
				 ("biWidth", LONG),
				 ("biHeight", LONG),
				 ("biPlanes", WORD),
				 ("biBitCount", WORD),
				 ("biCompression", DWORD),
				 ("biSizeImage", DWORD),
				 ("biXPelsPerMeter", LONG),
				 ("biYPelsPerMeter", LONG),
				 ("biClrUsed", DWORD),
				 ("biClrImportant", DWORD)]

class BITMAPINFO(ctypes.Structure):
	"""
	This class is a :class:`ctypes.Structure` subclass representing FreeImage **BITMAPINFO** C / C++ object.
	"""

	_fields_ = [("bmiHeader", BITMAPINFOHEADER),
				("bmiColors", RGBQUAD)]

class FIRGB16(ctypes.Structure):
	"""
	This class is a :class:`ctypes.Structure` subclass representing FreeImage **FIRGB16** C / C++ object.
	"""

	_fields_ = [("red", WORD),
				("green", WORD),
				("blue", WORD)]

class FIRGBA16(ctypes.Structure):
	"""
	This class is a :class:`ctypes.Structure` subclass representing FreeImage **FIRGBA16** C / C++ object.
	"""

	_fields_ = [("red", WORD),
				("green", WORD),
				("blue", WORD),
				("alpha", WORD)]

class FIRGBF(ctypes.Structure):
	"""
	This class is a :class:`ctypes.Structure` subclass representing FreeImage **FIRGBF** C / C++ object.
	"""

	_fields_ = [("red", ctypes.c_float),
				("green", ctypes.c_float),
				("blue", ctypes.c_float)]

class FIRGBAF(ctypes.Structure):
	"""
	This class is a :class:`ctypes.Structure` subclass representing FreeImage **FIRGBAF** C / C++ object.
	"""

	_fields_ = [("red", ctypes.c_float),
				("green", ctypes.c_float),
				("blue", ctypes.c_float),
				("alpha", ctypes.c_float)]

class FICOMPLEX(ctypes.Structure):
	"""
	This class is a :class:`ctypes.Structure` subclass representing FreeImage **FICOMPLEX** C / C++ object.
	"""

	_fields_ = [("r", ctypes.c_double),
				("i", ctypes.c_double)]

"""
Indexes for byte arrays, masks and shifts for treating pixels as words.
"""
if FREEIMAGE_BIGENDIAN:
	# Little Endian ( x86 / MS Windows, Linux ): BGR(A) order.
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
		# Little Endian ( x86 / MacOSX ): RGB(A) order.
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
else:
	if FREEIMAGE_COLORORDER == FREEIMAGE_COLORORDER_BGR:
		# Big Endian ( PPC / None ): BGR(A) order.
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
	else:
		# Big Endian ( PPC / Linux, MacOSX ): RGB(A) order.
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

FI_RGBA_RGB_MASK = (FI_RGBA_RED_MASK | FI_RGBA_GREEN_MASK | FI_RGBA_BLUE_MASK)

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

"""
ICC Profile support
"""
FIICC_DEFAULT			 = 0x00
FIICC_COLOR_IS_CMYK		 = 0x01

class FIICCPROFILE(ctypes.Structure):
	"""
	This class is a :class:`ctypes.Structure` subclass representing FreeImage **FIICCPROFILE** C / C++ object.
	"""

	_fields_ = [("flags", WORD),
				("size", DWORD),
				("data", VOID)]

class FREE_IMAGE_FORMAT(object):
	"""
	This class is used for I/O image format identifiers.
	"""

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
	FIF_MUTLIPAGE = (FIF_TIFF, FIF_ICO, FIF_GIF)

class FREE_IMAGE_TYPE(object):
	"""
	This class is used for images types.
	"""

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

class FREE_IMAGE_COLOR_TYPE(object):
	"""
	This class is used for image color types.
	"""

	FIC_MINISWHITE = 0
	FIC_MINISBLACK = 1
	FIC_RGB = 2
	FIC_PALETTE = 3
	FIC_RGBALPHA = 4
	FIC_CMYK = 5

class FREE_IMAGE_QUANTIZE(object):
	"""
	This class is used for color Quantization algorithms.
	"""

	FIQ_WUQUANT = 0
	FIQ_NNQUANT = 1

class FREE_IMAGE_DITHER(object):
	"""
	This class is used for dithering algorithms.
	"""

	FID_FS			 = 0
	FID_BAYER4x4	 = 1
	FID_BAYER8x8	 = 2
	FID_CLUSTER6x6	 = 3
	FID_CLUSTER8x8	 = 4
	FID_CLUSTER16x16 = 5
	FID_BAYER16x16	 = 6

class FREE_IMAGE_JPEG_OPERATION(object):
	"""
	This class is used for lossless jpeg transformations.
	"""

	FIJPEG_OP_NONE			 = 0
	FIJPEG_OP_FLIP_H		 = 1
	FIJPEG_OP_FLIP_V		 = 2
	FIJPEG_OP_TRANSPOSE		 = 3
	FIJPEG_OP_TRANSVERSE	 = 4
	FIJPEG_OP_ROTATE_90		 = 5
	FIJPEG_OP_ROTATE_180	 = 6
	FIJPEG_OP_ROTATE_270	 = 7

class FREE_IMAGE_TMO(object):
	"""
	This class is used for tone mapping operators.
	"""

	FITMO_DRAGO03	 = 0
	FITMO_REINHARD05 = 1
	FITMO_FATTAL02	 = 2

class FREE_IMAGE_FILTER(object):
	"""
	This class is used for upsampling / downsampling filters.
	"""

	FILTER_BOX			 = 0
	FILTER_BICUBIC		 = 1
	FILTER_BILINEAR		 = 2
	FILTER_BSPLINE		 = 3
	FILTER_CATMULLROM	 = 4
	FILTER_LANCZOS3		 = 5

class FREE_IMAGE_COLOR_CHANNEL(object):
	"""
	This class is used for color channels.
	"""
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

class FREE_IMAGE_MDTYPE(object):
	"""
	This class is used for tags data types informations.
	"""

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

	FIDTToType = {FIDT_NOTYPE : VOID,
				FIDT_BYTE : ctypes.c_ubyte,
				FIDT_ASCII : ctypes.c_char_p,
				FIDT_SHORT : ctypes.c_ushort,
				FIDT_LONG : ctypes.c_uint,
				FIDT_RATIONAL : ctypes.c_ulong,
				FIDT_SBYTE : ctypes.c_short,
				FIDT_UNDEFINED : VOID,
				FIDT_SSHORT : ctypes.c_short,
				FIDT_SLONG : ctypes.c_long,
				FIDT_SRATIONAL : ctypes.c_long,
				FIDT_FLOAT : ctypes.c_float,
				FIDT_DOUBLE : ctypes.c_double,
				FIDT_IFD : ctypes.c_uint,
				FIDT_PALETTE : RGBQUAD}

class FREE_IMAGE_MDMODEL(object):
	"""
	This class is used for metadatas Models.
	"""
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

class FIMETADATA(ctypes.Structure):
	"""
	This class is a :class:`ctypes.Structure` subclass representing FreeImage **FIMETADATA** C / C++ object.
	"""

	_fields_ = [("data", VOID), ]

class FITAG(ctypes.Structure):
	"""
	This class is a :class:`ctypes.Structure` subclass representing FreeImage **FITAG** C / C++ object.
	"""

	_fields_ = [("data", VOID)]

"""
File io routines.
"""

fi_handle = ctypes.c_void_p

FI_ReadProc = DLL_CALLCONV(ctypes.c_uint, BYTE_P, ctypes.c_uint, ctypes.c_uint, fi_handle)
FI_WriteProc = DLL_CALLCONV(ctypes.c_uint, BYTE_P, ctypes.c_uint, ctypes.c_uint, fi_handle)
FI_SeekProc = DLL_CALLCONV(ctypes.c_int, fi_handle, ctypes.c_long, ctypes.c_int)
FI_TellProc = DLL_CALLCONV(ctypes.c_long, fi_handle)

class FreeImageIO(ctypes.Structure):
	"""
	This class is a :class:`ctypes.Structure` subclass representing FreeImage **FreeImageIO** C / C++ object.
	"""

	_fields_ = [('read_proc', FI_ReadProc),
				('write_proc', FI_WriteProc),
				('seek_proc', FI_SeekProc),
				('tell_proc', FI_TellProc)]

class FIMEMORY(ctypes.Structure):
	"""
	This class is a :class:`ctypes.Structure` subclass representing FreeImage **FIMEMORY** C / C++ object.
	"""

	_fields_ = [("data", VOID)]

"""
Load / save flag constants.
"""
BMP_DEFAULT					 = 0
BMP_SAVE_RLE				 = 1
CUT_DEFAULT					 = 0
DDS_DEFAULT					 = 0
EXR_DEFAULT					 = 0
EXR_FLOAT					 = 0x0001
EXR_NONE					 = 0x0002
EXR_ZIP						 = 0x0004
EXR_PIZ						 = 0x0008
EXR_PXR24					 = 0x0010
EXR_B44						 = 0x0020
EXR_LC						 = 0x0040
FAXG3_DEFAULT				 = 0
GIF_DEFAULT					 = 0
GIF_LOAD256					 = 1
GIF_PLAYBACK				 = 2
HDR_DEFAULT					 = 0
ICO_DEFAULT					 = 0
ICO_MAKEALPHA				 = 1
IFF_DEFAULT					 = 0
J2K_DEFAULT					 = 0
JP2_DEFAULT					 = 0
JPEG_DEFAULT				 = 0
JPEG_FAST					 = 0x0001
JPEG_ACCURATE				 = 0x0002
JPEG_CMYK					 = 0x0004
JPEG_EXIFROTATE				 = 0x0008
JPEG_QUALITYSUPERB			 = 0x80
JPEG_QUALITYGOOD			 = 0x0100
JPEG_QUALITYNORMAL			 = 0x0200
JPEG_QUALITYAVERAGE			 = 0x0400
JPEG_QUALITYBAD				 = 0x0800
JPEG_PROGRESSIVE			 = 0x2000
JPEG_SUBSAMPLING_411		 = 0x1000
JPEG_SUBSAMPLING_420		 = 0x4000
JPEG_SUBSAMPLING_422		 = 0x8000
JPEG_SUBSAMPLING_444		 = 0x10000
KOALA_DEFAULT				 = 0
LBM_DEFAULT					 = 0
MNG_DEFAULT					 = 0
PCD_DEFAULT					 = 0
PCD_BASE					 = 1
PCD_BASEDIV4				 = 2
PCD_BASEDIV16				 = 3
PCX_DEFAULT					 = 0
PFM_DEFAULT					 = 0
PICT_DEFAULT				 = 0
PNG_DEFAULT					 = 0
PNG_IGNOREGAMMA				 = 1
PNG_Z_BEST_SPEED			 = 0x0001
PNG_Z_DEFAULT_COMPRESSION	 = 0x0006
PNG_Z_BEST_COMPRESSION		 = 0x0009
PNG_Z_NO_COMPRESSION		 = 0x0100
PNG_INTERLACED				 = 0x0200
PNM_DEFAULT					 = 0
PNM_SAVE_RAW				 = 0
PNM_SAVE_ASCII				 = 1
PSD_DEFAULT					 = 0
RAS_DEFAULT					 = 0
RAW_DEFAULT					 = 0
RAW_PREVIEW					 = 1
RAW_DISPLAY					 = 2
SGI_DEFAULT					 = 0
TARGA_DEFAULT				 = 0
TARGA_LOAD_RGB888			 = 1
TIFF_DEFAULT				 = 0
TIFF_CMYK					 = 0x0001
TIFF_NONE					 = 0x0800
TIFF_PACKBITS				 = 0x0100
TIFF_DEFLATE				 = 0x0200
TIFF_ADOBE_DEFLATE			 = 0x0400
TIFF_CCITTFAX3				 = 0x1000
TIFF_CCITTFAX4				 = 0x2000
TIFF_LZW					 = 0x4000
TIFF_JPEG					 = 0x8000
WBMP_DEFAULT				 = 0
XBM_DEFAULT					 = 0
XPM_DEFAULT					 = 0

"""
Background filling options.
"""
FI_COLOR_IS_RGB_COLOR			 = 0x00
FI_COLOR_IS_RGBA_COLOR			 = 0x01
FI_COLOR_FIND_EQUAL_COLOR		 = 0x02
FI_COLOR_ALPHA_IS_INDEX			 = 0x04
FI_COLOR_PALETTE_SEARCH_MASK	 = (FI_COLOR_FIND_EQUAL_COLOR | FI_COLOR_ALPHA_IS_INDEX)

"""
Custom constants
"""
BPP_1 = 1
BPP_4 = 4
BPP_8 = 8
BPP_16 = 16
BPP_24 = 24
BPP_32 = 32
BPP_48 = 48
BPP_64 = 64
BPP_96 = 96
BPP_1TO8 = (BPP_1, BPP_4, BPP_8)
BPP_16TO32 = (BPP_16, BPP_24, BPP_32)
BPP_1TO32 = (BPP_1, BPP_4, BPP_8, BPP_16, BPP_24, BPP_32)
BPP_1TO48 = BPP_1TO32 + (BPP_48,)

CPC_8 = 255
CPC_16 = 65535

FI_DEFAULT_NULL = 0
FI_DEFAULT_GAMMA = 2.2

FREEIMAGE_FUNCTIONS = (

	# Initialization functions.
	LibraryHook(name="FreeImage_Initialise", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_DeInitialise", argumentsTypes=None, returnValue=None),

	# Version functions.
	LibraryHook(name="FreeImage_GetVersion", argumentsTypes=None, returnValue=ctypes.c_char_p),
	LibraryHook(name="FreeImage_GetCopyrightMessage", argumentsTypes=None, returnValue=ctypes.c_char_p),

	# Message output functions.
	LibraryHook(name="FreeImage_SetOutputMessageStdCall", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_SetOutputMessage", argumentsTypes=None, returnValue=None),
	# LibraryHook(name="FreeImage_OutputMessageProc", argumentstype=none, returnvalue=none),

	# Allocate / clone / unload functions.
	LibraryHook(name="FreeImage_Allocate", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_AllocateT", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_Clone", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_Unload", argumentsTypes=None, returnValue=None),

	# Load / save unload functions.
	LibraryHook(name="FreeImage_Load", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_LoadU", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_LoadFromHandle", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_Save", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_SaveU", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_SaveToHandle", argumentsTypes=None, returnValue=None),

	# Memory I/O stream functions.
	LibraryHook(name="FreeImage_OpenMemory", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_CloseMemory", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_LoadFromMemory", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_SaveToMemory", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_TellMemory", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_SeekMemory", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_AcquireMemory", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_ReadMemory", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_WriteMemory", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_LoadMultiBitmapFromMemory", argumentsTypes=None, returnValue=None),

	# Plugin interface functions.
	LibraryHook(name="FreeImage_RegisterLocalPlugin", argumentsTypes=None, returnValue=None),
	# LibraryHook(name="FreeImage_RegisterExternalPlugin", argumentstype=none, returnvalue=none),
	LibraryHook(name="FreeImage_GetFIFCount", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_SetPluginEnabled", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_IsPluginEnabled", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_GetFIFFromFormat", argumentsTypes=None, returnValue=ctypes.c_char_p),
	LibraryHook(name="FreeImage_GetFIFFromMime", argumentsTypes=None, returnValue=ctypes.c_char_p),
	LibraryHook(name="FreeImage_GetFormatFromFIF", argumentsTypes=None, returnValue=ctypes.c_char_p),
	LibraryHook(name="FreeImage_GetFIFExtensionList", argumentsTypes=None, returnValue=ctypes.c_char_p),
	LibraryHook(name="FreeImage_GetFIFDescription", argumentsTypes=None, returnValue=ctypes.c_char_p),
	LibraryHook(name="FreeImage_GetFIFRegExpr", argumentsTypes=None, returnValue=ctypes.c_char_p),
	LibraryHook(name="FreeImage_GetFIFMimeType", argumentsTypes=None, returnValue=ctypes.c_char_p),
	LibraryHook(name="FreeImage_GetFIFFromFilename", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_GetFIFFromFilenameU", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_FIFSupportsReading", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_FIFSupportsWriting", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_FIFSupportsExportBPP", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_FIFSupportsExportType", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_FIFSupportsICCProfiles", argumentsTypes=None, returnValue=None),

	# Multipaging functions.
	LibraryHook(name="FreeImage_OpenMultiBitmap", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_OpenMultiBitmapFromHandle", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_CloseMultiBitmap", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_GetPageCount", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_AppendPage", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_InsertPage", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_DeletePage", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_LockPage", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_UnlockPage", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_MovePage", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_GetLockedPageNumbers", argumentsTypes=None, returnValue=None),

	# File type request functions.
	LibraryHook(name="FreeImage_GetFileType", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_GetFileTypeU", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_GetFileTypeFromHandle", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_GetFileTypeFromMemory", argumentsTypes=None, returnValue=None),

	# Image type request functions.
	LibraryHook(name="FreeImage_GetImageType", argumentsTypes=None, returnValue=None),

	# FreeImage helper functions.
	LibraryHook(name="FreeImage_IsLittleEndian", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_LookupX11Color", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_LookupSVGColor", argumentsTypes=None, returnValue=None),

	# Pixel access functions.
	LibraryHook(name="FreeImage_GetBits", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_GetScanLine", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_GetPixelIndex", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_GetPixelColor", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_SetPixelIndex", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_SetPixelColor", argumentsTypes=None, returnValue=None),

	# DIB informations functions.
	LibraryHook(name="FreeImage_GetColorsUsed", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_GetBPP", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_GetWidth", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_GetHeight", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_GetLine", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_GetPitch", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_GetDIBSize", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_GetPalette", argumentsTypes=None, returnValue=ctypes.POINTER(RGBQUAD)),
	LibraryHook(name="FreeImage_GetDotsPerMeterX", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_GetDotsPerMeterY", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_SetDotsPerMeterX", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_SetDotsPerMeterY", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_GetInfoHeader", argumentsTypes=None, returnValue=ctypes.POINTER(BITMAPINFOHEADER)),
	LibraryHook(name="FreeImage_GetInfo", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_GetColorType", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_GetRedMask", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_GetGreenMask", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_GetBlueMask", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_GetTransparencyCount", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_GetTransparencyTable", argumentsTypes=None, returnValue=ctypes.POINTER(BYTE)),
	LibraryHook(name="FreeImage_SetTransparencyTable", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_IsTransparent", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_SetTransparent", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_SetTransparentIndex", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_GetTransparentIndex", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_HasBackgroundColor", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_GetBackgroundColor", argumentsTypes=None, returnValue=ctypes.POINTER(RGBQUAD)),
	LibraryHook(name="FreeImage_SetBackgroundColor", argumentsTypes=None, returnValue=None),

	# ICC profile functions.
	LibraryHook(name="FreeImage_GetICCProfile", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_CreateICCProfile", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_DestroyICCProfile", argumentsTypes=None, returnValue=None),

	# Line conversion functions.
	LibraryHook(name="FreeImage_ConvertLine1To4", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_ConvertLine8To4", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_ConvertLine16To4_555", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_ConvertLine16To4_565", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_ConvertLine24To4", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_ConvertLine32To4", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_ConvertLine1To8", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_ConvertLine4To8", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_ConvertLine16To8_555", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_ConvertLine16To8_565", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_ConvertLine24To8", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_ConvertLine32To8", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_ConvertLine1To16_555", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_ConvertLine4To16_555", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_ConvertLine8To16_555", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_ConvertLine16_565_To16_555", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_ConvertLine24To16_555", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_ConvertLine32To16_555", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_ConvertLine1To16_565", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_ConvertLine4To16_565", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_ConvertLine8To16_565", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_ConvertLine16_555_To16_565", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_ConvertLine24To16_565", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_ConvertLine32To16_565", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_ConvertLine1To24", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_ConvertLine4To24", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_ConvertLine8To24", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_ConvertLine16To24_555", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_ConvertLine16To24_565", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_ConvertLine32To24", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_ConvertLine1To32", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_ConvertLine4To32", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_ConvertLine8To32", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_ConvertLine16To32_555", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_ConvertLine16To32_565", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_ConvertLine24To32", argumentsTypes=None, returnValue=None),

	# Smart conversion functions.
	LibraryHook(name="FreeImage_ConvertTo4Bits", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_ConvertTo8Bits", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_ConvertToGreyscale", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_ConvertTo16Bits555", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_ConvertTo16Bits565", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_ConvertTo24Bits", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_ConvertTo32Bits", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_ColorQuantize", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_ColorQuantizeEx", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_Threshold", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_Dither", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_ConvertFromRawBits", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_ConvertToRGBF", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_ConvertToRawBits", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_ConvertToStandardType", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_ConvertToType", argumentsTypes=None, returnValue=None),

	# Tone mapping operators functions.
	LibraryHook(name="FreeImage_ToneMapping", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_TmoDrago03", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_TmoReinhard05", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_TmoReinhard05Ex", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_TmoFattal02", argumentsTypes=None, returnValue=None),

	# ZLib functions.
	LibraryHook(name="FreeImage_ZLibCompress", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_ZLibUncompress", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_ZLibGZip", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_ZLibGUnzip", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_ZLibCRC32", argumentsTypes=None, returnValue=None),

	# Tags creation / destruction functions.
	LibraryHook(name="FreeImage_CreateTag", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_DeleteTag", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_CloneTag", argumentsTypes=None, returnValue=None),

	# Tags getters / setters functions.
	LibraryHook(name="FreeImage_GetTagKey", argumentsTypes=None, returnValue=ctypes.c_char_p),
	LibraryHook(name="FreeImage_GetTagDescription", argumentsTypes=None, returnValue=ctypes.c_char_p),
	LibraryHook(name="FreeImage_GetTagID", argumentsTypes=None, returnValue=ctypes.c_char_p),
	LibraryHook(name="FreeImage_GetTagType", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_GetTagCount", argumentsTypes=None, returnValue=ctypes.c_ulong),
	LibraryHook(name="FreeImage_GetTagLength", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_GetTagValue", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_SetTagKey", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_SetTagDescription", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_SetTagID", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_SetTagType", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_SetTagCount", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_SetTagLength", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_SetTagValue", argumentsTypes=None, returnValue=None),

	# Iterator functions.
	LibraryHook(name="FreeImage_FindFirstMetadata", argumentsTypes=None, returnValue=ctypes.c_void_p),
	LibraryHook(name="FreeImage_FindNextMetadata", argumentsTypes=None, returnValue=ctypes.c_void_p),
	LibraryHook(name="FreeImage_FindCloseMetadata", argumentsTypes=None, returnValue=None),

	# Metadatas getters / setters functions.
	LibraryHook(name="FreeImage_SetMetadata", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_GetMetadata", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_GetMetadataCount", argumentsTypes=None, returnValue=ctypes.c_ulong),
	LibraryHook(name="FreeImage_CloneMetadata", argumentsTypes=None, returnValue=None),

	# Tag to C string conversion function.
	LibraryHook(name="FreeImage_TagToString", argumentsTypes=None, returnValue=ctypes.c_char_p),

	# Rotation and flipping functions.
	LibraryHook(name="FreeImage_RotateClassic", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_Rotate", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_RotateEx", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_FlipHorizontal", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_FlipVertical", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_JPEGTransform", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_JPEGTransformU", argumentsTypes=None, returnValue=None),

	# Upsampling / downsampling functions.
	LibraryHook(name="FreeImage_Rescale", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_MakeThumbnail", argumentsTypes=None, returnValue=None),

	# Color manipulation functions.
	LibraryHook(name="FreeImage_AdjustCurve", argumentsTypes=None, returnValue=ctypes.c_long),
	LibraryHook(name="FreeImage_AdjustGamma", argumentsTypes=None, returnValue=ctypes.c_long),
	LibraryHook(name="FreeImage_AdjustBrightness", argumentsTypes=None, returnValue=ctypes.c_long),
	LibraryHook(name="FreeImage_AdjustContrast", argumentsTypes=None, returnValue=ctypes.c_long),
	LibraryHook(name="FreeImage_Invert", argumentsTypes=None, returnValue=ctypes.c_long),
	LibraryHook(name="FreeImage_GetHistogram", argumentsTypes=None, returnValue=ctypes.c_long),
	LibraryHook(name="FreeImage_GetAdjustColorsLookupTable", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_AdjustColors", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_ApplyColorMapping", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_SwapColors", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_ApplyPaletteIndexMapping", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_SwapPaletteIndices", argumentsTypes=None, returnValue=None),

	# Channel processing functions.
	LibraryHook(name="FreeImage_GetChannel", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_SetChannel", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_GetComplexChannel", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_SetComplexChannel", argumentsTypes=None, returnValue=None),

	# Copy / paste / composite functions.
	LibraryHook(name="FreeImage_Copy", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_Paste", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_Composite", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_JPEGCrop", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_JPEGCropU", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_PreMultiplyWithAlpha", argumentsTypes=None, returnValue=None),

	# Background filling functions.
	LibraryHook(name="FreeImage_FillBackground", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_EnlargeCanvas", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_AllocateEx", argumentsTypes=None, returnValue=None),
	LibraryHook(name="FreeImage_AllocateExT", argumentsTypes=None, returnValue=None),

	# Miscellaneous algorithms functions.
	LibraryHook(name="FreeImage_MultigridPoissonSolver", argumentsTypes=None, returnValue=None),

	# Custom functions.
	LibraryHook(name="FreeImage_HDRLabs_ConvertToLdr", argumentsTypes=None, returnValue=None),)

#***********************************************************************************************
#***	Module classes and definitions.
#***********************************************************************************************
class ImageInformationsHeader(core.Structure):
	"""
	This class represents a storage object for image informations header.
	"""

	@core.executionTrace
	def __init__(self, **kwargs):
		"""
		This method initializes the class.

		:param kwargs: path, width, height, bpp. ( Key / Value pairs )
		"""

		core.Structure.__init__(self, **kwargs)

class Image(object):
	"""
	This class provides various methods to manipulate images files.
	"""

	@core.executionTrace
	def __init__(self, imagePath=None):
		"""
		This method initializes the class.

		:param imagePath: Image path. ( String )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		# --- Setting class attributes. ---
		self.__library = foundations.library.Library(FREEIMAGE_LIBRARY_PATH, FREEIMAGE_FUNCTIONS)

		self.__errorsCallback = self.__library.callback(self.__logLibraryErrors)
		self.__library.library.FreeImage_SetOutputMessage(self.__errorsCallback)

		self.__imagePath = None
		self.imagePath = imagePath

		self.__bitmap = None

		if imagePath:
			self.load()

	#***********************************************************************************************
	#***	Attributes properties.
	#***********************************************************************************************
	@property
	def library(self):
		"""
		This method is the property for **self.__library** attribute.

		:return: self.__library. ( Library )
		"""

		return self.__library

	@library.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def library(self, value):
		"""
		This method is the setter method for **self.__library** attribute.

		:param value: Attribute value. ( Library )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("library"))

	@library.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def library(self):
		"""
		This method is the deleter method for **self.__library** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("library"))

	@property
	def errorsCallback(self):
		"""
		This method is the property for **self.__errorsCallback** attribute.

		:return: self.__errorsCallback. ( Object )
		"""

		return self.__errorsCallback

	@errorsCallback.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def errorsCallback(self, value):
		"""
		This method is the setter method for **self.__errorsCallback** attribute.

		:param value: Attribute value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("errorsCallback"))

	@errorsCallback.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def errorsCallback(self):
		"""
		This method is the deleter method for **self.__errorsCallback** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("errorsCallback"))

	@property
	def imagePath(self):
		"""
		This method is the property for **self.__imagePath** attribute.

		:return: self.__imagePath. ( String )
		"""

		return self.__imagePath

	@imagePath.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def imagePath(self, value):
		"""
		This method is the setter method for **self.__imagePath** attribute.

		:param value: Attribute value. ( String )
		"""

		if value:
			assert type(value) is str, "'{0}' attribute: '{1}' type is not 'str'!".format("imagePath", value)
		self.__imagePath = value

	@imagePath.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def imagePath(self):
		"""
		This method is the deleter method for **self.__imagePath** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("imagePath"))

	@property
	def bitmap(self):
		"""
		This method is the property for **self.__bitmap** attribute.

		:return: self.__bitmap. ( Object )
		"""

		return self.__bitmap

	@bitmap.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def bitmap(self, value):
		"""
		This method is the setter method for **self.__bitmap** attribute.

		:param value: Attribute value. ( Object )
		"""

		self.__bitmap = value

	@bitmap.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def bitmap(self):
		"""
		This method is the deleter method for **self.__bitmap** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("bitmap"))

	#***********************************************************************************************
	#***	Class methods.
	#***********************************************************************************************
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.LibraryExecutionError)
	def __logLibraryErrors(self, errorCode, message):
		"""
		This method logs the Library errors.
		"""

		raise foundations.exceptions.LibraryExecutionError, "Exit code '{1}', message: '{2}'".format(self.__class__.__name__, errorCode, message)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def getImageFormat(self, imagePath=None):
		"""
		This method gets the file format.

		:param imagePath: Image path. ( String )
		:return: File format. ( Object )
		"""

		imagePath = imagePath or self.__imagePath
		if not imagePath:
			return

		imagePath = ctypes.c_char_p(imagePath)
		fileFormat = self.__library.FreeImage_GetFileType(imagePath, False)
		if fileFormat == -1:
			fileFormat = self.__library.FreeImage_GetFIFFromFilename(imagePath)
		return fileFormat

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.LibraryExecutionError)
	def load(self, imagePath=None):
		"""
		This method loads the file.

		:param imagePath: Image path. ( String )
		:return: Method success. ( Boolean )
		"""

		if not self.__imagePath:
			return

		imageFormat = self.getImageFormat(self.__imagePath)
		if imageFormat != FREE_IMAGE_FORMAT.FIF_UNKNOWN:
			if self.__library.FreeImage_FIFSupportsReading(imageFormat):
				self.__bitmap = self.__library.FreeImage_Load(imageFormat, self.__imagePath, FI_DEFAULT_NULL)
				self.__bitmap and LOGGER.debug("> '{0}' image has been loaded!".format(self.__imagePath))
				return True
			else:
				raise foundations.exceptions.LibraryExecutionError, "'{0}' format read isn't supported!".format(imageFormat)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def save(self):
		"""
		This method saves the file.

		:return: Method success. ( Boolean )
		"""

		return self.saveAs(self.getImageFormat(self.__imagePath), self.__imagePath, FI_DEFAULT_NULL)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.LibraryExecutionError)
	def saveAs(self, imageFormat, imagePath, flags=FI_DEFAULT_NULL):
		"""
		This method saves the image to the provided file.

		:param imageFormat: Image format. ( Integer )
		:param imagePath: Image path. ( String )
		:param flags: Save flags. ( Integer )
		:return: Method success. ( Boolean )
		"""

		if self.__library.FreeImage_FIFSupportsWriting(imageFormat):
			if not imagePath:
				return
			if self.__library.FreeImage_Save(imageFormat, self.__bitmap, ctypes.c_char_p(imagePath), flags):
				LOGGER.debug("> '{0}' image has been saved!".format(imagePath))
				return True
		else:
			raise foundations.exceptions.LibraryExecutionError, "'{0}' format write isn't supported!".format(imageFormat)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def convertToType(self, targetType, linearScale=True):
		"""
		This method converts the bitmap to provided type.

		:param targetType: Target type. ( Integer )
		:param linearScale: Linear scale. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Converting '{0}' image bitmap to type '{1}'!".format(self.__imagePath, targetType))
		self.__bitmap = self.__library.FreeImage_ConvertToType(self.__bitmap, targetType, linearScale)
		if self.__bitmap:
			LOGGER.debug("> '{0}' image bitmap conversion to type '{1}' done!".format(self.__imagePath, targetType))
			return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def convertToLdr(self, gamma=2.2):
		"""
		This method converts the HDR bitmap to LDR.

		:param gamma: Image conversion gamma. ( Float )
		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Converting '{0}' HDR image bitmap to LDR!".format(self.__imagePath))
		self.__bitmap = self.__library.FreeImage_HDRLabs_ConvertToLdr(self.__bitmap, ctypes.c_double(gamma))
		if self.__bitmap:
			LOGGER.debug("> '{0}' HDR image bitmap conversion to LDR done!".format(self.__imagePath))
			return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.LibraryExecutionError)
	def convertToQImage(self):
		"""
		This method converts the bitmap to `QImage <http://doc.qt.nokia.com/4.7/qimage.html>`_.

		:return: Converted image. ( QImage )
		"""

		bpp = self.__library.FreeImage_GetBPP(self.__bitmap)
		(self.__library.FreeImage_GetImageType(self.__bitmap) == FREE_IMAGE_TYPE.FIT_RGBF or self.__library.FreeImage_GetImageType(self.__bitmap) == FREE_IMAGE_TYPE.FIT_RGBAF) and self.convertToLdr(2.2)

		if self.__library.FreeImage_GetImageType(self.__bitmap) == FREE_IMAGE_TYPE.FIT_BITMAP:
			LOGGER.debug("> Converting '{0}' image bitmap to QImage!".format(self.__imagePath))

			from PyQt4.QtGui import QImage
			from sip import voidptr

			width = self.__library.FreeImage_GetWidth(self.__bitmap)
			height = self.__library.FreeImage_GetHeight(self.__bitmap)
			pitch = width * (BPP_32 / 8)
			bits = ctypes.create_string_buffer(chr(0) * height * pitch)
			self.__library.FreeImage_ConvertToRawBits(ctypes.byref(bits), self.__bitmap, pitch, BPP_32, FI_RGBA_RED_MASK, FI_RGBA_GREEN_MASK, FI_RGBA_BLUE_MASK, True)

			self.__library.FreeImage_Unload(self.__bitmap)

			bitsPointer = ctypes.addressof(bits)

			LOGGER.debug("> Initializing image from memory pointer '{0}' address.".format(bitsPointer))
			LOGGER.debug("> Image width: '{0}'.".format(width))
			LOGGER.debug("> Image height: '{0}'.".format(height))
			LOGGER.debug("> Image pitch: '{0}'.".format(pitch))
			LOGGER.debug("> Initializing QImage with memory pointer '{0}' address.".format(bitsPointer))

			image = QImage(voidptr(bitsPointer, size=height * pitch), width, height, pitch, QImage.Format_RGB32)

			image._datas = ImageInformationsHeader(path=self.__imagePath, width=width, height=height, bpp=bpp)

			# Removing the following line would result in a Python process crash, I need to call 'bits()' method at some point.
			LOGGER.debug("> Final memory pointer with '{0}' address.".format(image.bits().__int__()))

			LOGGER.debug("> '{0}' image bitmap conversion to QImage done!".format(self.__imagePath))

			return image
		else:
			raise foundations.exceptions.LibraryExecutionError, "Image bitmap is not of type '{0}'!".format(FREE_IMAGE_TYPE.FIT_BITMAP)
