#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**freeimage.py**

**Platform:**
    Windows, Linux, Mac Os X.

**Description:**
    Provides FreeImage library (http://freeimage.sourceforge.net/) bindings.

**Others:**
    Portions of the code from FreeImagePy by
    Michele Petrazzo: http://freeimagepy.sourceforge.net/ and ctypesgen: http://code.google.com/p/ctypesgen/.
"""

from __future__ import unicode_literals

import ctypes
import os
import platform
import re
import sys

import foundations.common
import foundations.data_structures
import foundations.exceptions
import foundations.library
import foundations.verbose
import sibl_gui
from foundations.library import LibraryHook
from umbra.globals.constants import Constants

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER",
           "pointer",
           "FREEIMAGE_LIBRARY_PATH",
           "DLL_CALLCONV",
           "FREEIMAGE_MAJOR_VERSION",
           "FREEIMAGE_MINOR_VERSION",
           "FREEIMAGE_RELEASE_SERIAL",
           "FREEIMAGE_LOOKUP",
           "INT",
           "BOOL",
           "BYTE",
           "WORD",
           "DWORD",
           "LONG",
           "DOUBLE",
           "BYTE_P",
           "FREEIMAGE_BIGENDIAN",
           "FREEIMAGE_COLORORDER_BGR",
           "FREEIMAGE_COLORORDER_RGB",
           "FREEIMAGE_COLORORDER",
           "FIBITMAP",
           "FIMULTIBITMAP",
           "tagRGBQUAD",
           "RGBQUAD",
           "tagRGBTRIPLE",
           "RGBTRIPLE",
           "tagBITMAPINFOHEADER",
           "BITMAPINFOHEADER",
           "tagBITMAPINFO",
           "BITMAPINFO",
           "PBITMAPINFO",
           "tagFIRGB16",
           "FIRGB16",
           "tagFIRGBA16",
           "FIRGBA16",
           "tagFIRGBF",
           "FIRGBF",
           "tagFIRGBAF",
           "FIRGBAF",
           "tagFICOMPLEX",
           "FICOMPLEX",
           "FI_RGBA_RED",
           "FI_RGBA_GREEN",
           "FI_RGBA_BLUE",
           "FI_RGBA_ALPHA",
           "FI_RGBA_RED_MASK",
           "FI_RGBA_GREEN_MASK",
           "FI_RGBA_BLUE_MASK",
           "FI_RGBA_ALPHA_MASK",
           "FI_RGBA_RED_SHIFT",
           "FI_RGBA_GREEN_SHIFT",
           "FI_RGBA_BLUE_SHIFT",
           "FI_RGBA_ALPHA_SHIFT",
           "FI_RGBA_RGB_MASK",
           "FI_RGBA_LOOKUP",
           "FI16_555_RED_MASK",
           "FI16_555_GREEN_MASK",
           "FI16_555_BLUE_MASK",
           "FI16_555_RED_SHIFT",
           "FI16_555_GREEN_SHIFT",
           "FI16_555_BLUE_SHIFT",
           "FI16_565_RED_MASK",
           "FI16_565_GREEN_MASK",
           "FI16_565_BLUE_MASK",
           "FI16_565_RED_SHIFT",
           "FI16_565_GREEN_SHIFT",
           "FI16_565_BLUE_SHIFT",
           "FI16_LOOKUP",
           "FIICC_DEFAULT",
           "FIICC_COLOR_IS_CMYK",
           "FIICC_LOOKUP",
           "FIICCPROFILE",
           "FREE_IMAGE_FORMAT",
           "FIF_UNKNOWN",
           "FIF_BMP",
           "FIF_ICO",
           "FIF_JPEG",
           "FIF_JNG",
           "FIF_KOALA",
           "FIF_LBM",
           "FIF_IFF",
           "FIF_MNG",
           "FIF_PBM",
           "FIF_PBMRAW",
           "FIF_PCD",
           "FIF_PCX",
           "FIF_PGM",
           "FIF_PGMRAW",
           "FIF_PNG",
           "FIF_PPM",
           "FIF_PPMRAW",
           "FIF_RAS",
           "FIF_TARGA",
           "FIF_TIFF",
           "FIF_WBMP",
           "FIF_PSD",
           "FIF_CUT",
           "FIF_XBM",
           "FIF_XPM",
           "FIF_DDS",
           "FIF_GIF",
           "FIF_HDR",
           "FIF_FAXG3",
           "FIF_SGI",
           "FIF_EXR",
           "FIF_J2K",
           "FIF_JP2",
           "FIF_PFM",
           "FIF_PICT",
           "FIF_RAW",
           "FIF_LOOKUP",
           "FREE_IMAGE_TYPE",
           "FIT_UNKNOWN",
           "FIT_BITMAP",
           "FIT_UINT16",
           "FIT_INT16",
           "FIT_UINT32",
           "FIT_INT32",
           "FIT_FLOAT",
           "FIT_DOUBLE",
           "FIT_COMPLEX",
           "FIT_RGB16",
           "FIT_RGBA16",
           "FIT_RGBF",
           "FIT_RGBAF",
           "FIT_LOOKUP",
           "FREE_IMAGE_COLOR_TYPE",
           "FIC_MINISWHITE",
           "FIC_MINISBLACK",
           "FIC_RGB",
           "FIC_PALETTE",
           "FIC_RGBALPHA",
           "FIC_CMYK",
           "FIC_LOOKUP",
           "FREE_IMAGE_QUANTIZE",
           "FIQ_WUQUANT",
           "FIQ_NNQUANT",
           "FIQ_LOOKUP",
           "FREE_IMAGE_DITHER",
           "FID_FS",
           "FID_BAYER4x4",
           "FID_BAYER8x8",
           "FID_CLUSTER6x6",
           "FID_CLUSTER8x8",
           "FID_CLUSTER16x16",
           "FID_BAYER16x16",
           "FID_LOOKUP",
           "FREE_IMAGE_JPEG_OPERATION",
           "FIJPEG_OP_NONE",
           "FIJPEG_OP_FLIP_H",
           "FIJPEG_OP_FLIP_V",
           "FIJPEG_OP_TRANSPOSE",
           "FIJPEG_OP_TRANSVERSE",
           "FIJPEG_OP_ROTATE_90",
           "FIJPEG_OP_ROTATE_180",
           "FIJPEG_OP_ROTATE_270",
           "FIJPEG_LOOKUP",
           "FREE_IMAGE_TMO",
           "FITMO_DRAGO03",
           "FITMO_REINHARD05",
           "FITMO_FATTAL02",
           "FITMO_LOOKUP",
           "FREE_IMAGE_FILTER",
           "FILTER_BOX",
           "FILTER_BICUBIC",
           "FILTER_BILINEAR",
           "FILTER_BSPLINE",
           "FILTER_CATMULLROM",
           "FILTER_LANCZOS3",
           "FILTER_LOOKUP",
           "FREE_IMAGE_COLOR_CHANNEL",
           "FICC_RGB",
           "FICC_RED",
           "FICC_GREEN",
           "FICC_BLUE",
           "FICC_ALPHA",
           "FICC_BLACK",
           "FICC_REAL",
           "FICC_IMAG",
           "FICC_MAG",
           "FICC_PHASE",
           "FICC_LOOKUP",
           "FREE_IMAGE_MDTYPE",
           "FIDT_NOTYPE",
           "FIDT_BYTE",
           "FIDT_ASCII",
           "FIDT_SHORT",
           "FIDT_LONG",
           "FIDT_RATIONAL",
           "FIDT_SBYTE",
           "FIDT_UNDEFINED",
           "FIDT_SSHORT",
           "FIDT_SLONG",
           "FIDT_SRATIONAL",
           "FIDT_FLOAT",
           "FIDT_DOUBLE",
           "FIDT_IFD",
           "FIDT_PALETTE",
           "FIDT_LOOKUP",
           "FREE_IMAGE_MDMODEL",
           "FIMD_NODATA",
           "FIMD_COMMENTS",
           "FIMD_EXIF_MAIN",
           "FIMD_EXIF_EXIF",
           "FIMD_EXIF_GPS",
           "FIMD_EXIF_MAKERNOTE",
           "FIMD_EXIF_INTEROP",
           "FIMD_IPTC",
           "FIMD_XMP",
           "FIMD_GEOTIFF",
           "FIMD_ANIMATION",
           "FIMD_CUSTOM",
           "FIMD_EXIF_RAW",
           "FIMD_LOOKUP",
           "FIMETADATA",
           "FITAG",
           "fi_handle",
           "FI_ReadProc",
           "FI_WriteProc",
           "FI_SeekProc",
           "FI_TellProc",
           "FreeImageIO	",
           "FIMEMORY",
           "FI_FormatProc",
           "FI_DescriptionProc",
           "FI_ExtensionListProc",
           "FI_RegExprProc",
           "FI_OpenProc",
           "FI_CloseProc",
           "FI_PageCountProc",
           "FI_PageCapabilityProc",
           "FI_LoadProc",
           "FI_SaveProc",
           "FI_ValidateProc",
           "FI_MimeProc",
           "FI_SupportsExportBPPProc",
           "FI_SupportsExportTypeProc",
           "FI_SupportsICCProfilesProc",
           "FI_SupportsNoPixelsProc",
           "Plugin",
           "FI_InitProc",
           "FIF_LOAD_NOPIXELS",
           "BMP_DEFAULT",
           "BMP_SAVE_RLE",
           "CUT_DEFAULT",
           "DDS_DEFAULT",
           "EXR_DEFAULT",
           "EXR_FLOAT",
           "EXR_NONE",
           "EXR_ZIP",
           "EXR_PIZ",
           "EXR_PXR24",
           "EXR_B44",
           "EXR_LC",
           "FAXG3_DEFAULT",
           "GIF_DEFAULT",
           "GIF_LOAD256",
           "GIF_PLAYBACK",
           "HDR_DEFAULT",
           "ICO_DEFAULT",
           "ICO_MAKEALPHA",
           "IFF_DEFAULT",
           "J2K_DEFAULT",
           "JP2_DEFAULT",
           "JPEG_DEFAULT",
           "JPEG_FAST",
           "JPEG_ACCURATE",
           "JPEG_CMYK",
           "JPEG_EXIFROTATE",
           "JPEG_QUALITYSUPERB",
           "JPEG_QUALITYGOOD",
           "JPEG_QUALITYNORMAL",
           "JPEG_QUALITYAVERAGE",
           "JPEG_QUALITYBAD",
           "JPEG_PROGRESSIVE",
           "JPEG_SUBSAMPLING_411",
           "JPEG_SUBSAMPLING_420",
           "JPEG_SUBSAMPLING_422",
           "JPEG_SUBSAMPLING_444",
           "JPEG_OPTIMIZE",
           "JPEG_BASELINE",
           "KOALA_DEFAULT",
           "LBM_DEFAULT",
           "MNG_DEFAULT",
           "PCD_DEFAULT",
           "PCD_BASE",
           "PCD_BASEDIV4",
           "PCD_BASEDIV16",
           "PCX_DEFAULT",
           "PFM_DEFAULT",
           "PICT_DEFAULT",
           "PNG_DEFAULT",
           "PNG_IGNOREGAMMA",
           "PNG_Z_BEST_SPEED",
           "PNG_Z_DEFAULT_COMPRESSION",
           "PNG_Z_BEST_COMPRESSION",
           "PNG_Z_NO_COMPRESSION",
           "PNG_INTERLACED",
           "PNM_DEFAULT",
           "PNM_SAVE_RAW",
           "PNM_SAVE_ASCII",
           "PSD_DEFAULT",
           "PSD_CMYK",
           "PSD_LAB",
           "RAS_DEFAULT",
           "RAW_DEFAULT",
           "RAW_PREVIEW",
           "RAW_DISPLAY",
           "RAW_HALFSIZE",
           "SGI_DEFAULT",
           "TARGA_DEFAULT",
           "TARGA_LOAD_RGB888",
           "TIFF_DEFAULT",
           "TIFF_CMYK",
           "TIFF_PACKBITS",
           "TIFF_DEFLATE",
           "TIFF_ADOBE_DEFLATE",
           "TIFF_NONE",
           "TIFF_CCITTFAX3",
           "TIFF_CCITTFAX4",
           "TIFF_LZW",
           "TIFF_JPEG",
           "TIFF_LOGLUV",
           "WBMP_DEFAULT",
           "XBM_DEFAULT",
           "XPM_DEFAULT",
           "FI_COLOR_IS_RGB_COLOR",
           "FI_COLOR_IS_RGBA_COLOR",
           "FI_COLOR_FIND_EQUAL_COLOR",
           "FI_COLOR_ALPHA_IS_INDEX",
           "FI_COLOR_PALETTE_SEARCH_MASK",
           "FI_COLOR_LOOKUP",
           "BPP_1",
           "BPP_4",
           "BPP_8",
           "BPP_16",
           "BPP_24",
           "BPP_32",
           "BPP_48",
           "BPP_64",
           "BPP_96",
           "BPP_1TO8",
           "BPP_16TO32",
           "BPP_1TO32",
           "BPP_1TO48",
           "BPP_LOOKUP",
           "CPC_8",
           "CPC_16",
           "CPC_LOOKUP",
           "FI_DEFAULT_NULL",
           "FI_DEFAULT_GAMMA",
           "FI_DEFAULT_LOOKUP",
           "FreeImage_OutputMessageFunctionStdCall",
           "FreeImage_OutputMessageFunction",
           "FREEIMAGE_FUNCTIONS",
           "get_free_image_library_path",
           "ImageInformationsHeader",
           "Image"]

LOGGER = foundations.verbose.install_logger()


def pointer(data):
    """
    Converts None to a real NULL pointer to work around bugs
    in how ctypes handles None on 64-bit platforms.

    :param data: Data .
    :type data: object
    :return: Pointer.
    :rtype: POINTER
    """

    pointer = ctypes.POINTER(data)

    if not isinstance(pointer.from_param, classmethod):
        def from_param(class_, value):
            if value is None:
                return class_()
            else:
                return value

        pointer.from_param = classmethod(from_param)
    return pointer


def unchecked(type):
    """
    Ensures that all callbacks return primitive datatypes.

    As of ctypes 1.0, ctypes does not support custom error-checking functions on callbacks,
    nor does it support custom datatypes on callbacks, so we must ensure that all callbacks return primitive datatypes.
    Non-primitive return values wrapped with unchecked won't be typechecked, and will be converted to c_void_p.

    :param type: Type .
    :type type: object
    :return: Type.
    :rtype: object
    """

    if (hasattr(type, "_type_") and isinstance(type._type_, str) and type._type_ != "P"):
        return type
    else:
        return ctypes.c_void_p


FREEIMAGE_LIBRARY_PATH = None

if platform.system() == "Windows" or platform.system() == "Microsoft":
    DLL_CALLCONV = ctypes.WINFUNCTYPE
else:
    DLL_CALLCONV = ctypes.CFUNCTYPE

FREEIMAGE_MAJOR_VERSION = 3
FREEIMAGE_MINOR_VERSION = 15
FREEIMAGE_RELEASE_SERIAL = 1
FREEIMAGE_LOOKUP = foundations.data_structures.Lookup(**dict((key, value) for key, value in locals().iteritems()
                                                             if re.search(r"^FREEIMAGE_\w+", key)))

"""
Internal types.
"""
INT = ctypes.c_int
BOOL = ctypes.c_int32
BYTE = ctypes.c_uint8
WORD = ctypes.c_uint16
DWORD = ctypes.c_uint32
LONG = ctypes.c_int32
DOUBLE = ctypes.c_double

BYTE_P = pointer(BYTE)

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


class FIBITMAP(ctypes.Structure):
    """
    Defines a :class:`ctypes.Structure` subclass representing FreeImage **FIBITMAP** C / C++ object.
    """

    __slots__ = ["data"]
    _fields_ = [("data", pointer(None))]


class FIMULTIBITMAP(ctypes.Structure):
    """
    Defines a :class:`ctypes.Structure` subclass representing FreeImage **FIMULTIBITMAP** C / C++ object.
    """

    __slots__ = ["data"]
    _fields_ = [("data", pointer(None))]


class tagRGBQUAD(ctypes.Structure):
    """
    Defines a :class:`ctypes.Structure` subclass representing FreeImage **tagRGBQUAD** C / C++ object.
    """

    __slots__ = ["rgbBlue", "rgbGreen", "rgbRed", "rgbReserved"]
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


RGBQUAD = tagRGBQUAD


class tagRGBTRIPLE(ctypes.Structure):
    """
    Defines a :class:`ctypes.Structure` subclass representing FreeImage **tagRGBTRIPLE** C / C++ object.
    """

    __slots__ = ["rgbBlue", "rgbGreen", "rgbRed"]
    _fields_ = []

    if FREEIMAGE_COLORORDER == FREEIMAGE_COLORORDER_BGR:
        _fields_ += [("rgbBlue", BYTE),
                     ("rgbGreen", BYTE),
                     ("rgbRed", BYTE)]
    else:
        _fields_ += [("rgbRed", BYTE),
                     ("rgbGreen", BYTE),
                     ("rgbBlue", BYTE)]


RGBTRIPLE = tagRGBTRIPLE


class tagBITMAPINFOHEADER(ctypes.Structure):
    """
    Defines a :class:`ctypes.Structure` subclass representing FreeImage **tagBITMAPINFOHEADER** C / C++ object.
    """
    __slots__ = ["biSize",
                 "biWidth",
                 "biHeight",
                 "biPlanes",
                 "biHeight",
                 "biBitCount",
                 "biCompression",
                 "biSizeImage",
                 "biXPelsPerMeter",
                 "biYPelsPerMeter",
                 "biClrUsed",
                 "biClrImportant"]
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


BITMAPINFOHEADER = tagBITMAPINFOHEADER


class tagBITMAPINFO(ctypes.Structure):
    """
    Defines a :class:`ctypes.Structure` subclass representing FreeImage **tagBITMAPINFO** C / C++ object.
    """
    __slots__ = ["bmiHeader", "bmiColors"]
    _fields_ = [("bmiHeader", BITMAPINFOHEADER),
                ("bmiColors", RGBQUAD * 1)]


BITMAPINFO = tagBITMAPINFO

PBITMAPINFO = pointer(tagBITMAPINFO)


class tagFIRGB16(ctypes.Structure):
    """
    Defines a :class:`ctypes.Structure` subclass representing FreeImage **tagFIRGB16** C / C++ object.
    """

    __slots__ = ["red", "green", "blue"]
    _fields_ = [("red", WORD),
                ("green", WORD),
                ("blue", WORD)]


FIRGB16 = tagFIRGB16


class tagFIRGBA16(ctypes.Structure):
    """
    Defines a :class:`ctypes.Structure` subclass representing FreeImage **tagFIRGBA16** C / C++ object.
    """

    __slots__ = ["red", "green", "blue", "alpha"]
    _fields_ = [("red", WORD),
                ("green", WORD),
                ("blue", WORD),
                ("alpha", WORD)]


FIRGBA16 = tagFIRGBA16


class tagFIRGBF(ctypes.Structure):
    """
    Defines a :class:`ctypes.Structure` subclass representing FreeImage **tagFIRGBF** C / C++ object.
    """

    __slots__ = ["red", "green", "blue"]
    _fields_ = [("red", ctypes.c_float),
                ("green", ctypes.c_float),
                ("blue", ctypes.c_float)]


FIRGBF = tagFIRGBF


class tagFIRGBAF(ctypes.Structure):
    """
    Defines a :class:`ctypes.Structure` subclass representing FreeImage **tagFIRGBAF** C / C++ object.
    """

    __slots__ = ["red", "green", "blue", "alpha"]
    _fields_ = [("red", ctypes.c_float),
                ("green", ctypes.c_float),
                ("blue", ctypes.c_float),
                ("alpha", ctypes.c_float)]


FIRGBAF = tagFIRGBAF


class tagFICOMPLEX(ctypes.Structure):
    """
    Defines a :class:`ctypes.Structure` subclass representing FreeImage **tagFICOMPLEX** C / C++ object.
    """

    __slots__ = ["r", "i"]
    _fields_ = [("r", ctypes.c_double),
                ("i", ctypes.c_double)]


FICOMPLEX = tagFICOMPLEX

"""
Indexes for byte arrays, masks and shifts for treating pixels as words.
"""
if FREEIMAGE_BIGENDIAN:
    # Little Endian ( x86 / MS Windows, Linux ): BGR(A) order.
    if FREEIMAGE_COLORORDER == FREEIMAGE_COLORORDER_BGR:
        FI_RGBA_RED = 2
        FI_RGBA_GREEN = 1
        FI_RGBA_BLUE = 0
        FI_RGBA_ALPHA = 3
        FI_RGBA_RED_MASK = 0x00FF0000
        FI_RGBA_GREEN_MASK = 0x0000FF00
        FI_RGBA_BLUE_MASK = 0x000000FF
        FI_RGBA_ALPHA_MASK = 0xFF000000L
        FI_RGBA_RED_SHIFT = 16
        FI_RGBA_GREEN_SHIFT = 8
        FI_RGBA_BLUE_SHIFT = 0
        FI_RGBA_ALPHA_SHIFT = 24
    else:
        # Little Endian ( x86 / MacOSX ): RGB(A) order.
        FI_RGBA_RED = 0
        FI_RGBA_GREEN = 1
        FI_RGBA_BLUE = 2
        FI_RGBA_ALPHA = 3
        FI_RGBA_RED_MASK = 0xFF000000
        FI_RGBA_GREEN_MASK = 0x00FF0000
        FI_RGBA_BLUE_MASK = 0x0000FF00
        FI_RGBA_ALPHA_MASK = 0x000000FF
        FI_RGBA_RED_SHIFT = 24
        FI_RGBA_GREEN_SHIFT = 16
        FI_RGBA_BLUE_SHIFT = 8
        FI_RGBA_ALPHA_SHIFT = 0
else:
    if FREEIMAGE_COLORORDER == FREEIMAGE_COLORORDER_BGR:
        # Big Endian ( PPC / None ): BGR(A) order.
        FI_RGBA_RED = 2
        FI_RGBA_GREEN = 1
        FI_RGBA_BLUE = 0
        FI_RGBA_ALPHA = 3
        FI_RGBA_RED_MASK = 0x0000FF00
        FI_RGBA_GREEN_MASK = 0x00FF0000
        FI_RGBA_BLUE_MASK = 0xFF000000
        FI_RGBA_ALPHA_MASK = 0x000000FF
        FI_RGBA_RED_SHIFT = 8
        FI_RGBA_GREEN_SHIFT = 16
        FI_RGBA_BLUE_SHIFT = 24
        FI_RGBA_ALPHA_SHIFT = 0
    else:
        # Big Endian ( PPC / Linux, MacOSX ): RGB(A) order.
        FI_RGBA_RED = 0
        FI_RGBA_GREEN = 1
        FI_RGBA_BLUE = 2
        FI_RGBA_ALPHA = 3
        FI_RGBA_RED_MASK = 0xFF000000
        FI_RGBA_GREEN_MASK = 0x00FF0000
        FI_RGBA_BLUE_MASK = 0x0000FF00
        FI_RGBA_ALPHA_MASK = 0x000000FF
        FI_RGBA_RED_SHIFT = 24
        FI_RGBA_GREEN_SHIFT = 16
        FI_RGBA_BLUE_SHIFT = 8
        FI_RGBA_ALPHA_SHIFT = 0

FI_RGBA_RGB_MASK = ((FI_RGBA_RED_MASK | FI_RGBA_GREEN_MASK) | FI_RGBA_BLUE_MASK)
FI_RGBA_LOOKUP = foundations.data_structures.Lookup(**dict((key, value) for key, value in locals().iteritems()
                                                           if re.search(r"^FI_RGBA_\w+", key)))

FI16_555_RED_MASK = 0x7C00
FI16_555_GREEN_MASK = 0x03E0
FI16_555_BLUE_MASK = 0x001F
FI16_555_RED_SHIFT = 10
FI16_555_GREEN_SHIFT = 5
FI16_555_BLUE_SHIFT = 0
FI16_565_RED_MASK = 0xF800
FI16_565_GREEN_MASK = 0x07E0
FI16_565_BLUE_MASK = 0x001F
FI16_565_RED_SHIFT = 11
FI16_565_GREEN_SHIFT = 5
FI16_565_BLUE_SHIFT = 0
FI16_LOOKUP = foundations.data_structures.Lookup(**dict((key, value) for key, value in locals().iteritems()
                                                        if re.search(r"^FI16_\w+", key)))

"""
ICC Profile support
"""
FIICC_DEFAULT = 0x00
FIICC_COLOR_IS_CMYK = 0x01
FIICC_LOOKUP = foundations.data_structures.Lookup(**dict((key, value) for key, value in locals().iteritems()
                                                         if re.search(r"^FIICC_\w+", key)))


class FIICCPROFILE(ctypes.Structure):
    """
    Defines a :class:`ctypes.Structure` subclass representing FreeImage **FIICCPROFILE** C / C++ object.
    """

    __slots__ = ["flags", "size", "data"]
    _fields_ = [("flags", WORD),
                ("size", DWORD),
                ("data", pointer(None))]


FREE_IMAGE_FORMAT = ctypes.c_int
FIF_UNKNOWN = -1
FIF_BMP = 0
FIF_ICO = 1
FIF_JPEG = 2
FIF_JNG = 3
FIF_KOALA = 4
FIF_LBM = 5
FIF_IFF = FIF_LBM
FIF_MNG = 6
FIF_PBM = 7
FIF_PBMRAW = 8
FIF_PCD = 9
FIF_PCX = 10
FIF_PGM = 11
FIF_PGMRAW = 12
FIF_PNG = 13
FIF_PPM = 14
FIF_PPMRAW = 15
FIF_RAS = 16
FIF_TARGA = 17
FIF_TIFF = 18
FIF_WBMP = 19
FIF_PSD = 20
FIF_CUT = 21
FIF_XBM = 22
FIF_XPM = 23
FIF_DDS = 24
FIF_GIF = 25
FIF_HDR = 26
FIF_FAXG3 = 27
FIF_SGI = 28
FIF_EXR = 29
FIF_J2K = 30
FIF_JP2 = 31
FIF_PFM = 32
FIF_PICT = 33
FIF_RAW = 34
FIF_LOOKUP = foundations.data_structures.Lookup(**dict((key, value) for key, value in locals().iteritems()
                                                       if re.search(r"^FIF_\w+", key)))

FREE_IMAGE_TYPE = ctypes.c_int
FIT_UNKNOWN = 0
FIT_BITMAP = 1
FIT_UINT16 = 2
FIT_INT16 = 3
FIT_UINT32 = 4
FIT_INT32 = 5
FIT_FLOAT = 6
FIT_DOUBLE = 7
FIT_COMPLEX = 8
FIT_RGB16 = 9
FIT_RGBA16 = 10
FIT_RGBF = 11
FIT_RGBAF = 12
FIT_LOOKUP = foundations.data_structures.Lookup(**dict((key, value) for key, value in locals().iteritems()
                                                       if re.search(r"^FIT_\w+", key)))

FREE_IMAGE_COLOR_TYPE = ctypes.c_int
FIC_MINISWHITE = 0
FIC_MINISBLACK = 1
FIC_RGB = 2
FIC_PALETTE = 3
FIC_RGBALPHA = 4
FIC_CMYK = 5
FIC_LOOKUP = foundations.data_structures.Lookup(**dict((key, value) for key, value in locals().iteritems()
                                                       if re.search(r"^FIC_\w+", key)))

FREE_IMAGE_QUANTIZE = ctypes.c_int
FIQ_WUQUANT = 0
FIQ_NNQUANT = 1
FIQ_LOOKUP = foundations.data_structures.Lookup(**dict((key, value) for key, value in locals().iteritems()
                                                       if re.search(r"^FIQ_\w+", key)))

FREE_IMAGE_DITHER = ctypes.c_int
FID_FS = 0
FID_BAYER4x4 = 1
FID_BAYER8x8 = 2
FID_CLUSTER6x6 = 3
FID_CLUSTER8x8 = 4
FID_CLUSTER16x16 = 5
FID_BAYER16x16 = 6
FID_LOOKUP = foundations.data_structures.Lookup(**dict((key, value) for key, value in locals().iteritems()
                                                       if re.search(r"^FID_\w+", key)))

FREE_IMAGE_JPEG_OPERATION = ctypes.c_int
FIJPEG_OP_NONE = 0
FIJPEG_OP_FLIP_H = 1
FIJPEG_OP_FLIP_V = 2
FIJPEG_OP_TRANSPOSE = 3
FIJPEG_OP_TRANSVERSE = 4
FIJPEG_OP_ROTATE_90 = 5
FIJPEG_OP_ROTATE_180 = 6
FIJPEG_OP_ROTATE_270 = 7
FIJPEG_LOOKUP = foundations.data_structures.Lookup(**dict((key, value) for key, value in locals().iteritems()
                                                          if re.search(r"^FIJPEG_\w+", key)))

FREE_IMAGE_TMO = ctypes.c_int
FITMO_DRAGO03 = 0
FITMO_REINHARD05 = 1
FITMO_FATTAL02 = 2
FITMO_LOOKUP = foundations.data_structures.Lookup(**dict((key, value) for key, value in locals().iteritems()
                                                         if re.search(r"^FITMO_\w+", key)))

FREE_IMAGE_FILTER = ctypes.c_int
FILTER_BOX = 0
FILTER_BICUBIC = 1
FILTER_BILINEAR = 2
FILTER_BSPLINE = 3
FILTER_CATMULLROM = 4
FILTER_LANCZOS3 = 5
FILTER_LOOKUP = foundations.data_structures.Lookup(**dict((key, value) for key, value in locals().iteritems()
                                                          if re.search(r"^FILTER_\w+", key)))

FREE_IMAGE_COLOR_CHANNEL = ctypes.c_int
FICC_RGB = 0
FICC_RED = 1
FICC_GREEN = 2
FICC_BLUE = 3
FICC_ALPHA = 4
FICC_BLACK = 5
FICC_REAL = 6
FICC_IMAG = 7
FICC_MAG = 8
FICC_PHASE = 9
FICC_LOOKUP = foundations.data_structures.Lookup(**dict((key, value) for key, value in locals().iteritems()
                                                        if re.search(r"^FICC_\w+", key)))

FREE_IMAGE_MDTYPE = ctypes.c_int
FIDT_NOTYPE = 0
FIDT_BYTE = 1
FIDT_ASCII = 2
FIDT_SHORT = 3
FIDT_LONG = 4
FIDT_RATIONAL = 5
FIDT_SBYTE = 6
FIDT_UNDEFINED = 7
FIDT_SSHORT = 8
FIDT_SLONG = 9
FIDT_SRATIONAL = 10
FIDT_FLOAT = 11
FIDT_DOUBLE = 12
FIDT_IFD = 13
FIDT_PALETTE = 14
FIDT_LOOKUP = foundations.data_structures.Lookup(**dict((key, value) for key, value in locals().iteritems()
                                                        if re.search(r"^FIDT_\w+", key)))

FREE_IMAGE_MDMODEL = ctypes.c_int
FIMD_NODATA = -1
FIMD_COMMENTS = 0
FIMD_EXIF_MAIN = 1
FIMD_EXIF_EXIF = 2
FIMD_EXIF_GPS = 3
FIMD_EXIF_MAKERNOTE = 4
FIMD_EXIF_INTEROP = 5
FIMD_IPTC = 6
FIMD_XMP = 7
FIMD_GEOTIFF = 8
FIMD_ANIMATION = 9
FIMD_CUSTOM = 10
FIMD_EXIF_RAW = 11
FIMD_LOOKUP = foundations.data_structures.Lookup(**dict((key, value) for key, value in locals().iteritems()
                                                        if re.search(r"^FIMD_\w+", key)))


class FIMETADATA(ctypes.Structure):
    """
    Defines a :class:`ctypes.Structure` subclass representing FreeImage **FIMETADATA** C / C++ object.
    """

    __slots__ = ["data"]
    _fields_ = [("data", pointer(None)), ]


class FITAG(ctypes.Structure):
    """
    Defines a :class:`ctypes.Structure` subclass representing FreeImage **FITAG** C / C++ object.
    """

    __slots__ = ["data"]
    _fields_ = [("data", pointer(None))]


"""
File io routines.
"""

fi_handle = pointer(None)

FI_ReadProc = DLL_CALLCONV(unchecked(ctypes.c_uint), pointer(None), ctypes.c_uint, ctypes.c_uint, fi_handle)
FI_WriteProc = DLL_CALLCONV(unchecked(ctypes.c_uint), pointer(None), ctypes.c_uint, ctypes.c_uint, fi_handle)
FI_SeekProc = DLL_CALLCONV(unchecked(ctypes.c_int), fi_handle, ctypes.c_long, ctypes.c_int)
FI_TellProc = DLL_CALLCONV(unchecked(ctypes.c_long), fi_handle)


class FreeImageIO(ctypes.Structure):
    """
    Defines a :class:`ctypes.Structure` subclass representing FreeImage **FreeImageIO** C / C++ object.
    """

    __slots__ = ["read_proc", "write_proc", "seek_proc", "tell_proc"]
    _fields_ = [("read_proc", FI_ReadProc),
                ("write_proc", FI_WriteProc),
                ("seek_proc", FI_SeekProc),
                ("tell_proc", FI_TellProc)]


class FIMEMORY(ctypes.Structure):
    """
    Defines a :class:`ctypes.Structure` subclass representing FreeImage **FIMEMORY** C / C++ object.
    """

    __slots__ = ["data"]
    _fields_ = [("data", pointer(None))]


"""
Plugin routines.
"""
FI_FormatProc = ctypes.CFUNCTYPE(unchecked(ctypes.c_char_p), )
FI_DescriptionProc = ctypes.CFUNCTYPE(unchecked(ctypes.c_char_p), )
FI_ExtensionListProc = ctypes.CFUNCTYPE(unchecked(ctypes.c_char_p), )
FI_RegExprProc = ctypes.CFUNCTYPE(unchecked(ctypes.c_char_p), )
FI_OpenProc = ctypes.CFUNCTYPE(unchecked(pointer(None)), pointer(FreeImageIO), fi_handle, BOOL)
FI_CloseProc = ctypes.CFUNCTYPE(unchecked(None), pointer(FreeImageIO), fi_handle, pointer(None))
FI_PageCountProc = ctypes.CFUNCTYPE(unchecked(ctypes.c_int), pointer(FreeImageIO), fi_handle, pointer(None))
FI_PageCapabilityProc = ctypes.CFUNCTYPE(unchecked(ctypes.c_int), pointer(FreeImageIO), fi_handle, pointer(None))
FI_LoadProc = ctypes.CFUNCTYPE(unchecked(pointer(FIBITMAP)),
                               pointer(FreeImageIO),
                               fi_handle,
                               ctypes.c_int,
                               ctypes.c_int,
                               pointer(None))
FI_SaveProc = ctypes.CFUNCTYPE(unchecked(BOOL),
                               pointer(FreeImageIO),
                               pointer(FIBITMAP),
                               fi_handle,
                               ctypes.c_int,
                               ctypes.c_int,
                               pointer(None))
FI_ValidateProc = ctypes.CFUNCTYPE(unchecked(BOOL), pointer(FreeImageIO), fi_handle)
FI_MimeProc = ctypes.CFUNCTYPE(unchecked(ctypes.c_char_p), )
FI_SupportsExportBPPProc = ctypes.CFUNCTYPE(unchecked(BOOL), ctypes.c_int)
FI_SupportsExportTypeProc = ctypes.CFUNCTYPE(unchecked(BOOL), FREE_IMAGE_TYPE)
FI_SupportsICCProfilesProc = ctypes.CFUNCTYPE(unchecked(BOOL), )
FI_SupportsNoPixelsProc = ctypes.CFUNCTYPE(unchecked(BOOL), )


class Plugin(ctypes.Structure):
    """
    Defines a :class:`ctypes.Structure` subclass representing FreeImage **Plugin** C / C++ object.
    """

    __slots__ = ["format_proc",
                 "description_proc",
                 "extension_proc",
                 "regexpr_proc",
                 "open_proc",
                 "close_proc",
                 "pagecount_proc",
                 "pagecapability_proc",
                 "load_proc",
                 "save_proc",
                 "validate_proc",
                 "mime_proc",
                 "supports_export_bpp_proc",
                 "supports_export_type_proc",
                 "supports_icc_profiles_proc",
                 "supports_no_pixels_proc"]
    _fields_ = [("format_proc", FI_FormatProc),
                ("description_proc", FI_DescriptionProc),
                ("extension_proc", FI_ExtensionListProc),
                ("regexpr_proc", FI_RegExprProc),
                ("open_proc", FI_OpenProc),
                ("close_proc", FI_CloseProc),
                ("pagecount_proc", FI_PageCountProc),
                ("pagecapability_proc", FI_PageCapabilityProc),
                ("load_proc", FI_LoadProc),
                ("save_proc", FI_SaveProc),
                ("validate_proc", FI_ValidateProc),
                ("mime_proc", FI_MimeProc),
                ("supports_export_bpp_proc", FI_SupportsExportBPPProc),
                ("supports_export_type_proc", FI_SupportsExportTypeProc),
                ("supports_icc_profiles_proc", FI_SupportsICCProfilesProc),
                ("supports_no_pixels_proc", FI_SupportsNoPixelsProc)]


FI_InitProc = ctypes.CFUNCTYPE(unchecked(None), pointer(Plugin), ctypes.c_int)

"""
Load / save flag constants.
"""
FIF_LOAD_NOPIXELS = 0x8000

BMP_DEFAULT = 0
BMP_SAVE_RLE = 1
CUT_DEFAULT = 0
DDS_DEFAULT = 0
EXR_DEFAULT = 0
EXR_FLOAT = 0x0001
EXR_NONE = 0x0002
EXR_ZIP = 0x0004
EXR_PIZ = 0x0008
EXR_PXR24 = 0x0010
EXR_B44 = 0x0020
EXR_LC = 0x0040
FAXG3_DEFAULT = 0
GIF_DEFAULT = 0
GIF_LOAD256 = 1
GIF_PLAYBACK = 2
HDR_DEFAULT = 0
ICO_DEFAULT = 0
ICO_MAKEALPHA = 1
IFF_DEFAULT = 0
J2K_DEFAULT = 0
JP2_DEFAULT = 0
JPEG_DEFAULT = 0
JPEG_FAST = 0x0001
JPEG_ACCURATE = 0x0002
JPEG_CMYK = 0x0004
JPEG_EXIFROTATE = 0x0008
JPEG_QUALITYSUPERB = 0x80
JPEG_QUALITYGOOD = 0x0100
JPEG_QUALITYNORMAL = 0x0200
JPEG_QUALITYAVERAGE = 0x0400
JPEG_QUALITYBAD = 0x0800
JPEG_PROGRESSIVE = 0x2000
JPEG_SUBSAMPLING_411 = 0x1000
JPEG_SUBSAMPLING_420 = 0x4000
JPEG_SUBSAMPLING_422 = 0x8000
JPEG_SUBSAMPLING_444 = 0x10000
JPEG_OPTIMIZE = 0x20000
JPEG_BASELINE = 0x40000
KOALA_DEFAULT = 0
LBM_DEFAULT = 0
MNG_DEFAULT = 0
PCD_DEFAULT = 0
PCD_BASE = 1
PCD_BASEDIV4 = 2
PCD_BASEDIV16 = 3
PCX_DEFAULT = 0
PFM_DEFAULT = 0
PICT_DEFAULT = 0
PNG_DEFAULT = 0
PNG_IGNOREGAMMA = 1
PNG_Z_BEST_SPEED = 0x0001
PNG_Z_DEFAULT_COMPRESSION = 0x0006
PNG_Z_BEST_COMPRESSION = 0x0009
PNG_Z_NO_COMPRESSION = 0x0100
PNG_INTERLACED = 0x0200
PNM_DEFAULT = 0
PNM_SAVE_RAW = 0
PNM_SAVE_ASCII = 1
PSD_DEFAULT = 0
PSD_CMYK = 1
PSD_LAB = 2
RAS_DEFAULT = 0
RAW_DEFAULT = 0
RAW_PREVIEW = 1
RAW_DISPLAY = 2
RAW_HALFSIZE = 4
SGI_DEFAULT = 0
TARGA_DEFAULT = 0
TARGA_LOAD_RGB888 = 1
TIFF_DEFAULT = 0
TIFF_CMYK = 0x0001
TIFF_PACKBITS = 0x0100
TIFF_DEFLATE = 0x0200
TIFF_ADOBE_DEFLATE = 0x0400
TIFF_NONE = 0x0800
TIFF_CCITTFAX3 = 0x1000
TIFF_CCITTFAX4 = 0x2000
TIFF_LZW = 0x4000
TIFF_JPEG = 0x8000
TIFF_LOGLUV = 0x10000
WBMP_DEFAULT = 0
XBM_DEFAULT = 0
XPM_DEFAULT = 0

"""
Background filling options.
"""
FI_COLOR_IS_RGB_COLOR = 0x00
FI_COLOR_IS_RGBA_COLOR = 0x01
FI_COLOR_FIND_EQUAL_COLOR = 0x02
FI_COLOR_ALPHA_IS_INDEX = 0x04
FI_COLOR_PALETTE_SEARCH_MASK = (FI_COLOR_FIND_EQUAL_COLOR | FI_COLOR_ALPHA_IS_INDEX)
FI_COLOR_LOOKUP = foundations.data_structures.Lookup(**dict((key, value) for key, value in locals().iteritems()
                                                            if re.search(r"^FI_COLOR_\w+", key)))

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
BPP_LOOKUP = foundations.data_structures.Lookup(**dict((key, value) for key, value in locals().iteritems()
                                                       if re.search(r"^BPP_\w+", key)))

CPC_8 = 255
CPC_16 = 65535
CPC_LOOKUP = foundations.data_structures.Lookup(**dict((key, value) for key, value in locals().iteritems()
                                                       if re.search(r"^CPC_\w+", key)))

FI_DEFAULT_NULL = 0
FI_DEFAULT_GAMMA = 2.2
FI_DEFAULT_LOOKUP = foundations.data_structures.Lookup(**dict((key, value) for key, value in locals().iteritems()
                                                              if re.search(r"^FI_DEFAULT_\w+", key)))

FreeImage_OutputMessageFunctionStdCall = ctypes.CFUNCTYPE(unchecked(None), FREE_IMAGE_FORMAT, ctypes.c_char_p)
FreeImage_OutputMessageFunction = ctypes.CFUNCTYPE(unchecked(None), FREE_IMAGE_FORMAT, ctypes.c_char_p)

FREEIMAGE_FUNCTIONS = (

    # Initialization functions.
    LibraryHook(name="FreeImage_Initialise",
                arguments_types=[BOOL],
                return_value=None),
    LibraryHook(name="FreeImage_DeInitialise",
                arguments_types=[],
                return_value=None),

    # Version functions.
    LibraryHook(name="FreeImage_GetVersion",
                arguments_types=[],
                return_value=ctypes.c_char_p),
    LibraryHook(name="FreeImage_GetCopyrightMessage",
                arguments_types=[],
                return_value=ctypes.c_char_p),

    # Message output functions.
    LibraryHook(name="FreeImage_SetOutputMessageStdCall",
                arguments_types=[FreeImage_OutputMessageFunctionStdCall],
                return_value=None),
    LibraryHook(name="FreeImage_SetOutputMessage",
                arguments_types=[FreeImage_OutputMessageFunction],
                return_value=None),
    # LibraryHook(name="FreeImage_OutputMessageProc",
    # 			argumentstype=none,
    # 			return_value=none),
    # FreeImage_OutputMessageProc is a variadic function and is not supported by ctypes.

    # Allocate / clone / unload functions.
    LibraryHook(name="FreeImage_Allocate",
                arguments_types=[ctypes.c_int, ctypes.c_int, ctypes.c_int,
                                 ctypes.c_uint, ctypes.c_uint, ctypes.c_uint],
                return_value=pointer(FIBITMAP)),
    LibraryHook(name="FreeImage_AllocateT",
                arguments_types=[FREE_IMAGE_TYPE,
                                 ctypes.c_int,
                                 ctypes.c_int,
                                 ctypes.c_int,
                                 ctypes.c_uint,
                                 ctypes.c_uint,
                                 ctypes.c_uint],
                return_value=pointer(FIBITMAP)),
    LibraryHook(name="FreeImage_Clone",
                arguments_types=[pointer(FIBITMAP)],
                return_value=pointer(FIBITMAP)),
    LibraryHook(name="FreeImage_Unload",
                arguments_types=[pointer(FIBITMAP)],
                return_value=None),

    # Header loading routines.
    LibraryHook(name="FreeImage_HasPixels",
                arguments_types=[pointer(FIBITMAP)],
                return_value=BOOL),

    # Load / save unload functions.
    LibraryHook(name="FreeImage_Load",
                arguments_types=[FREE_IMAGE_FORMAT, ctypes.c_char_p, ctypes.c_int],
                return_value=pointer(FIBITMAP)),
    LibraryHook(name="FreeImage_LoadU",
                arguments_types=[FREE_IMAGE_FORMAT, pointer(ctypes.c_wchar), ctypes.c_int],
                return_value=pointer(FIBITMAP)),
    LibraryHook(name="FreeImage_LoadFromHandle",
                arguments_types=[FREE_IMAGE_FORMAT, pointer(FreeImageIO), fi_handle, ctypes.c_int],
                return_value=pointer(FIBITMAP)),
    LibraryHook(name="FreeImage_Save",
                arguments_types=[FREE_IMAGE_FORMAT, pointer(FIBITMAP), ctypes.c_char_p, ctypes.c_int],
                return_value=BOOL),
    LibraryHook(name="FreeImage_SaveU",
                arguments_types=[FREE_IMAGE_FORMAT, pointer(FIBITMAP), pointer(ctypes.c_wchar), ctypes.c_int],
                return_value=BOOL),
    LibraryHook(name="FreeImage_SaveToHandle",
                arguments_types=[FREE_IMAGE_FORMAT, pointer(FIBITMAP), pointer(FreeImageIO), fi_handle, ctypes.c_int],
                return_value=BOOL),

    # Memory I/O stream functions.
    LibraryHook(name="FreeImage_OpenMemory",
                arguments_types=[pointer(BYTE), DWORD],
                return_value=pointer(FIMEMORY)),
    LibraryHook(name="FreeImage_CloseMemory",
                arguments_types=[pointer(FIMEMORY)],
                return_value=None),
    LibraryHook(name="FreeImage_LoadFromMemory",
                arguments_types=[FREE_IMAGE_FORMAT, pointer(FIMEMORY), ctypes.c_int],
                return_value=pointer(FIBITMAP)),
    LibraryHook(name="FreeImage_SaveToMemory",
                arguments_types=[FREE_IMAGE_FORMAT, pointer(FIBITMAP), pointer(FIMEMORY), ctypes.c_int],
                return_value=BOOL),
    LibraryHook(name="FreeImage_TellMemory",
                arguments_types=[pointer(FIMEMORY)],
                return_value=ctypes.c_long),
    LibraryHook(name="FreeImage_SeekMemory",
                arguments_types=[pointer(FIMEMORY), ctypes.c_long, ctypes.c_int],
                return_value=BOOL),
    LibraryHook(name="FreeImage_AcquireMemory",
                arguments_types=[pointer(FIMEMORY), pointer(pointer(BYTE)), pointer(DWORD)],
                return_value=BOOL),
    LibraryHook(name="FreeImage_ReadMemory",
                arguments_types=[pointer(None), ctypes.c_uint, ctypes.c_uint, pointer(FIMEMORY)],
                return_value=ctypes.c_uint),
    LibraryHook(name="FreeImage_WriteMemory",
                arguments_types=[pointer(None), ctypes.c_uint, ctypes.c_uint, pointer(FIMEMORY)],
                return_value=ctypes.c_uint),
    LibraryHook(name="FreeImage_LoadMultiBitmapFromMemory",
                arguments_types=[FREE_IMAGE_FORMAT, pointer(FIMEMORY), ctypes.c_int],
                return_value=pointer(FIMULTIBITMAP)),
    LibraryHook(name="FreeImage_SaveMultiBitmapToMemory",
                arguments_types=[FREE_IMAGE_FORMAT, pointer(FIMULTIBITMAP), pointer(FIMEMORY), ctypes.c_int],
                return_value=BOOL),

    # Plugin interface functions.
    LibraryHook(name="FreeImage_RegisterLocalPlugin",
                arguments_types=[FI_InitProc, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p],
                return_value=FREE_IMAGE_FORMAT),
    # LibraryHook(name="FreeImage_RegisterExternalPlugin",
    # 			argumentstype=[ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p],
    # 			return_value=FREE_IMAGE_FORMAT),
    LibraryHook(name="FreeImage_GetFIFCount",
                arguments_types=[],
                return_value=ctypes.c_int),
    LibraryHook(name="FreeImage_SetPluginEnabled",
                arguments_types=[FREE_IMAGE_FORMAT, BOOL],
                return_value=ctypes.c_int),
    LibraryHook(name="FreeImage_IsPluginEnabled",
                arguments_types=[FREE_IMAGE_FORMAT],
                return_value=ctypes.c_int),
    LibraryHook(name="FreeImage_GetFIFFromFormat",
                arguments_types=[ctypes.c_char_p],
                return_value=FREE_IMAGE_FORMAT),
    LibraryHook(name="FreeImage_GetFIFFromMime",
                arguments_types=[ctypes.c_char_p],
                return_value=FREE_IMAGE_FORMAT),
    LibraryHook(name="FreeImage_GetFormatFromFIF",
                arguments_types=[FREE_IMAGE_FORMAT],
                return_value=ctypes.c_char_p),
    LibraryHook(name="FreeImage_GetFIFExtensionList",
                arguments_types=[FREE_IMAGE_FORMAT],
                return_value=ctypes.c_char_p),
    LibraryHook(name="FreeImage_GetFIFDescription",
                arguments_types=[FREE_IMAGE_FORMAT],
                return_value=ctypes.c_char_p),
    LibraryHook(name="FreeImage_GetFIFRegExpr",
                arguments_types=[FREE_IMAGE_FORMAT],
                return_value=ctypes.c_char_p),
    LibraryHook(name="FreeImage_GetFIFMimeType",
                arguments_types=[FREE_IMAGE_FORMAT],
                return_value=ctypes.c_char_p),
    LibraryHook(name="FreeImage_GetFIFFromFilename",
                arguments_types=[ctypes.c_char_p],
                return_value=FREE_IMAGE_FORMAT),
    LibraryHook(name="FreeImage_GetFIFFromFilenameU",
                arguments_types=[pointer(ctypes.c_wchar)],
                return_value=FREE_IMAGE_FORMAT),
    LibraryHook(name="FreeImage_FIFSupportsReading",
                arguments_types=[FREE_IMAGE_FORMAT],
                return_value=BOOL),
    LibraryHook(name="FreeImage_FIFSupportsWriting",
                arguments_types=[FREE_IMAGE_FORMAT],
                return_value=BOOL),
    LibraryHook(name="FreeImage_FIFSupportsExportBPP",
                arguments_types=[FREE_IMAGE_FORMAT, ctypes.c_int],
                return_value=BOOL),
    LibraryHook(name="FreeImage_FIFSupportsExportType",
                arguments_types=[FREE_IMAGE_FORMAT, FREE_IMAGE_TYPE],
                return_value=BOOL),
    LibraryHook(name="FreeImage_FIFSupportsICCProfiles",
                arguments_types=[FREE_IMAGE_FORMAT],
                return_value=BOOL),
    LibraryHook(name="FreeImage_FIFSupportsNoPixels",
                arguments_types=[FREE_IMAGE_FORMAT],
                return_value=BOOL),

    # Multipaging functions.
    LibraryHook(name="FreeImage_OpenMultiBitmap",
                arguments_types=[FREE_IMAGE_FORMAT, ctypes.c_char_p, BOOL, BOOL, BOOL, ctypes.c_char_p],
                return_value=pointer(FIMULTIBITMAP)),
    LibraryHook(name="FreeImage_OpenMultiBitmapFromHandle",
                arguments_types=[FREE_IMAGE_FORMAT, pointer(FreeImageIO), fi_handle, ctypes.c_int],
                return_value=pointer(FIMULTIBITMAP)),
    LibraryHook(name="FreeImage_SaveMultiBitmapToHandle",
                arguments_types=[FREE_IMAGE_FORMAT, pointer(
                    FIMULTIBITMAP), pointer(FreeImageIO), fi_handle, ctypes.c_int],
                return_value=BOOL),
    LibraryHook(name="FreeImage_CloseMultiBitmap",
                arguments_types=[pointer(FIMULTIBITMAP), ctypes.c_int],
                return_value=BOOL),
    LibraryHook(name="FreeImage_GetPageCount",
                arguments_types=[pointer(FIMULTIBITMAP)],
                return_value=ctypes.c_int),
    LibraryHook(name="FreeImage_AppendPage",
                arguments_types=[pointer(FIMULTIBITMAP), pointer(FIBITMAP)],
                return_value=None),
    LibraryHook(name="FreeImage_InsertPage",
                arguments_types=[pointer(FIMULTIBITMAP), ctypes.c_int, pointer(FIBITMAP)],
                return_value=None),
    LibraryHook(name="FreeImage_DeletePage",
                arguments_types=[pointer(FIMULTIBITMAP), ctypes.c_int],
                return_value=None),
    LibraryHook(name="FreeImage_LockPage",
                arguments_types=[pointer(FIMULTIBITMAP), ctypes.c_int],
                return_value=pointer(FIBITMAP)),
    LibraryHook(name="FreeImage_UnlockPage",
                arguments_types=[pointer(FIMULTIBITMAP), pointer(FIBITMAP), BOOL],
                return_value=None),
    LibraryHook(name="FreeImage_MovePage",
                arguments_types=[pointer(FIMULTIBITMAP), ctypes.c_int, ctypes.c_int],
                return_value=BOOL),
    LibraryHook(name="FreeImage_GetLockedPageNumbers",
                arguments_types=[pointer(FIMULTIBITMAP), pointer(ctypes.c_int), pointer(ctypes.c_int)],
                return_value=BOOL),

    # File type request functions.
    LibraryHook(name="FreeImage_GetFileType",
                arguments_types=[ctypes.c_char_p, ctypes.c_int],
                return_value=FREE_IMAGE_FORMAT),
    LibraryHook(name="FreeImage_GetFileTypeU",
                arguments_types=[pointer(ctypes.c_wchar), ctypes.c_int],
                return_value=FREE_IMAGE_FORMAT),
    LibraryHook(name="FreeImage_GetFileTypeFromHandle",
                arguments_types=[pointer(FreeImageIO), fi_handle, ctypes.c_int],
                return_value=FREE_IMAGE_FORMAT),
    LibraryHook(name="FreeImage_GetFileTypeFromMemory",
                arguments_types=[pointer(FIMEMORY), ctypes.c_int],
                return_value=FREE_IMAGE_FORMAT),

    # Image type request functions.
    LibraryHook(name="FreeImage_GetImageType",
                arguments_types=[pointer(FIBITMAP)],
                return_value=FREE_IMAGE_TYPE),

    # FreeImage helper functions.
    LibraryHook(name="FreeImage_IsLittleEndian",
                arguments_types=[],
                return_value=BOOL),
    LibraryHook(name="FreeImage_LookupX11Color",
                arguments_types=[ctypes.c_char_p, pointer(BYTE), pointer(BYTE), pointer(BYTE)],
                return_value=BOOL),
    LibraryHook(name="FreeImage_LookupSVGColor",
                arguments_types=[ctypes.c_char_p, pointer(BYTE), pointer(BYTE), pointer(BYTE)],
                return_value=BOOL),

    # Pixel access functions.
    LibraryHook(name="FreeImage_GetBits",
                arguments_types=[pointer(FIBITMAP)],
                return_value=pointer(BYTE)),
    LibraryHook(name="FreeImage_GetScanLine",
                arguments_types=[pointer(FIBITMAP), ctypes.c_int],
                return_value=pointer(BYTE)),
    LibraryHook(name="FreeImage_GetPixelIndex",
                arguments_types=[pointer(FIBITMAP), ctypes.c_uint, ctypes.c_uint, pointer(BYTE)],
                return_value=BOOL),
    LibraryHook(name="FreeImage_GetPixelColor",
                arguments_types=[pointer(FIBITMAP), ctypes.c_uint, ctypes.c_uint, pointer(RGBQUAD)],
                return_value=BOOL),
    LibraryHook(name="FreeImage_SetPixelIndex",
                arguments_types=[pointer(FIBITMAP), ctypes.c_uint, ctypes.c_uint, pointer(BYTE)],
                return_value=BOOL),
    LibraryHook(name="FreeImage_SetPixelColor",
                arguments_types=[pointer(FIBITMAP), ctypes.c_uint, ctypes.c_uint, pointer(RGBQUAD)],
                return_value=BOOL),

    # DIB informations functions.
    LibraryHook(name="FreeImage_GetColorsUsed",
                arguments_types=[pointer(FIBITMAP)],
                return_value=ctypes.c_uint),
    LibraryHook(name="FreeImage_GetBPP",
                arguments_types=[pointer(FIBITMAP)],
                return_value=ctypes.c_uint),
    LibraryHook(name="FreeImage_GetWidth",
                arguments_types=[pointer(FIBITMAP)],
                return_value=ctypes.c_uint),
    LibraryHook(name="FreeImage_GetHeight",
                arguments_types=[pointer(FIBITMAP)],
                return_value=ctypes.c_uint),
    LibraryHook(name="FreeImage_GetLine",
                arguments_types=[pointer(FIBITMAP)],
                return_value=ctypes.c_uint),
    LibraryHook(name="FreeImage_GetPitch",
                arguments_types=[pointer(FIBITMAP)],
                return_value=ctypes.c_uint),
    LibraryHook(name="FreeImage_GetDIBSize",
                arguments_types=[pointer(FIBITMAP)],
                return_value=ctypes.c_uint),
    LibraryHook(name="FreeImage_GetPalette",
                arguments_types=[pointer(FIBITMAP)],
                return_value=pointer(RGBQUAD)),
    LibraryHook(name="FreeImage_GetDotsPerMeterX",
                arguments_types=[pointer(FIBITMAP)],
                return_value=ctypes.c_uint),
    LibraryHook(name="FreeImage_GetDotsPerMeterY",
                arguments_types=[pointer(FIBITMAP)],
                return_value=ctypes.c_uint),
    LibraryHook(name="FreeImage_SetDotsPerMeterX",
                arguments_types=[pointer(FIBITMAP), ctypes.c_uint],
                return_value=None),
    LibraryHook(name="FreeImage_SetDotsPerMeterY",
                arguments_types=[pointer(FIBITMAP), ctypes.c_uint],
                return_value=None),
    LibraryHook(name="FreeImage_GetInfoHeader",
                arguments_types=[pointer(FIBITMAP)],
                return_value=pointer(BITMAPINFOHEADER)),
    LibraryHook(name="FreeImage_GetInfo",
                arguments_types=[pointer(FIBITMAP)],
                return_value=pointer(BITMAPINFO)),
    LibraryHook(name="FreeImage_GetColorType",
                arguments_types=[pointer(FIBITMAP)],
                return_value=FREE_IMAGE_COLOR_TYPE),
    LibraryHook(name="FreeImage_GetRedMask",
                arguments_types=[pointer(FIBITMAP)],
                return_value=ctypes.c_uint),
    LibraryHook(name="FreeImage_GetGreenMask",
                arguments_types=[pointer(FIBITMAP)],
                return_value=ctypes.c_uint),
    LibraryHook(name="FreeImage_GetBlueMask",
                arguments_types=[pointer(FIBITMAP)],
                return_value=ctypes.c_uint),
    LibraryHook(name="FreeImage_GetTransparencyCount",
                arguments_types=[pointer(FIBITMAP)],
                return_value=ctypes.c_uint),
    LibraryHook(name="FreeImage_GetTransparencyTable",
                arguments_types=[pointer(FIBITMAP)],
                return_value=BYTE),
    LibraryHook(name="FreeImage_SetTransparent",
                arguments_types=[pointer(FIBITMAP), BOOL],
                return_value=None),
    LibraryHook(name="FreeImage_SetTransparencyTable",
                arguments_types=[pointer(FIBITMAP), pointer(BYTE), ctypes.c_int],
                return_value=None),
    LibraryHook(name="FreeImage_IsTransparent",
                arguments_types=[pointer(FIBITMAP)],
                return_value=BOOL),
    LibraryHook(name="FreeImage_SetTransparentIndex",
                arguments_types=[pointer(FIBITMAP), ctypes.c_int],
                return_value=None),
    LibraryHook(name="FreeImage_GetTransparentIndex",
                arguments_types=[pointer(FIBITMAP)],
                return_value=ctypes.c_int),
    LibraryHook(name="FreeImage_HasBackgroundColor",
                arguments_types=[pointer(FIBITMAP)],
                return_value=BOOL),
    LibraryHook(name="FreeImage_GetBackgroundColor",
                arguments_types=[pointer(FIBITMAP), pointer(RGBQUAD)],
                return_value=BOOL),
    LibraryHook(name="FreeImage_SetBackgroundColor",
                arguments_types=[pointer(FIBITMAP), pointer(RGBQUAD)],
                return_value=BOOL),
    LibraryHook(name="FreeImage_GetThumbnail",
                arguments_types=[pointer(FIBITMAP)],
                return_value=pointer(FIBITMAP)),
    LibraryHook(name="FreeImage_SetThumbnail",
                arguments_types=[pointer(FIBITMAP), pointer(FIBITMAP)],
                return_value=BOOL),

    # ICC profile functions.
    LibraryHook(name="FreeImage_GetICCProfile",
                arguments_types=[pointer(FIBITMAP)],
                return_value=pointer(FIICCPROFILE)),
    LibraryHook(name="FreeImage_CreateICCProfile",
                arguments_types=[pointer(FIBITMAP), pointer(None), ctypes.c_long],
                return_value=pointer(FIICCPROFILE)),
    LibraryHook(name="FreeImage_DestroyICCProfile",
                arguments_types=[pointer(FIBITMAP)],
                return_value=None),

    # Line conversion functions.
    LibraryHook(name="FreeImage_ConvertLine1To4",
                arguments_types=[pointer(BYTE), pointer(BYTE), ctypes.c_int],
                return_value=None),
    LibraryHook(name="FreeImage_ConvertLine8To4",
                arguments_types=[pointer(BYTE), pointer(BYTE), ctypes.c_int, pointer(RGBQUAD)],
                return_value=None),
    LibraryHook(name="FreeImage_ConvertLine16To4_555",
                arguments_types=[pointer(BYTE), pointer(BYTE), ctypes.c_int],
                return_value=None),
    LibraryHook(name="FreeImage_ConvertLine16To4_565",
                arguments_types=[pointer(BYTE), pointer(BYTE), ctypes.c_int],
                return_value=None),
    LibraryHook(name="FreeImage_ConvertLine24To4",
                arguments_types=[pointer(BYTE), pointer(BYTE), ctypes.c_int],
                return_value=None),
    LibraryHook(name="FreeImage_ConvertLine32To4",
                arguments_types=[pointer(BYTE), pointer(BYTE), ctypes.c_int],
                return_value=None),
    LibraryHook(name="FreeImage_ConvertLine1To8",
                arguments_types=[pointer(BYTE), pointer(BYTE), ctypes.c_int],
                return_value=None),
    LibraryHook(name="FreeImage_ConvertLine4To8",
                arguments_types=[pointer(BYTE), pointer(BYTE), ctypes.c_int],
                return_value=None),
    LibraryHook(name="FreeImage_ConvertLine16To8_555",
                arguments_types=[pointer(BYTE), pointer(BYTE), ctypes.c_int],
                return_value=None),
    LibraryHook(name="FreeImage_ConvertLine16To8_565",
                arguments_types=[pointer(BYTE), pointer(BYTE), ctypes.c_int],
                return_value=None),
    LibraryHook(name="FreeImage_ConvertLine24To8",
                arguments_types=[pointer(BYTE), pointer(BYTE), ctypes.c_int],
                return_value=None),
    LibraryHook(name="FreeImage_ConvertLine32To8",
                arguments_types=[pointer(BYTE), pointer(BYTE), ctypes.c_int],
                return_value=None),
    LibraryHook(name="FreeImage_ConvertLine1To16_555",
                arguments_types=[pointer(BYTE), pointer(BYTE), ctypes.c_int, pointer(RGBQUAD)],
                return_value=None),
    LibraryHook(name="FreeImage_ConvertLine4To16_555",
                arguments_types=[pointer(BYTE), pointer(BYTE), ctypes.c_int, pointer(RGBQUAD)],
                return_value=None),
    LibraryHook(name="FreeImage_ConvertLine8To16_555",
                arguments_types=[pointer(BYTE), pointer(BYTE), ctypes.c_int, pointer(RGBQUAD)],
                return_value=None),
    LibraryHook(name="FreeImage_ConvertLine16_565_To16_555",
                arguments_types=[pointer(BYTE), pointer(BYTE), ctypes.c_int],
                return_value=None),
    LibraryHook(name="FreeImage_ConvertLine24To16_555",
                arguments_types=[pointer(BYTE), pointer(BYTE), ctypes.c_int],
                return_value=None),
    LibraryHook(name="FreeImage_ConvertLine32To16_555",
                arguments_types=[pointer(BYTE), pointer(BYTE), ctypes.c_int],
                return_value=None),
    LibraryHook(name="FreeImage_ConvertLine1To16_565",
                arguments_types=[pointer(BYTE), pointer(BYTE), ctypes.c_int, pointer(RGBQUAD)],
                return_value=None),
    LibraryHook(name="FreeImage_ConvertLine4To16_565",
                arguments_types=[pointer(BYTE), pointer(BYTE), ctypes.c_int, pointer(RGBQUAD)],
                return_value=None),
    LibraryHook(name="FreeImage_ConvertLine8To16_565",
                arguments_types=[pointer(BYTE), pointer(BYTE), ctypes.c_int, pointer(RGBQUAD)],
                return_value=None),
    LibraryHook(name="FreeImage_ConvertLine16_555_To16_565",
                arguments_types=[pointer(BYTE), pointer(BYTE), ctypes.c_int],
                return_value=None),
    LibraryHook(name="FreeImage_ConvertLine24To16_565",
                arguments_types=[pointer(BYTE), pointer(BYTE), ctypes.c_int],
                return_value=None),
    LibraryHook(name="FreeImage_ConvertLine32To16_565",
                arguments_types=[pointer(BYTE), pointer(BYTE), ctypes.c_int],
                return_value=None),
    LibraryHook(name="FreeImage_ConvertLine1To24",
                arguments_types=[pointer(BYTE), pointer(BYTE), ctypes.c_int, pointer(RGBQUAD)],
                return_value=None),
    LibraryHook(name="FreeImage_ConvertLine4To24",
                arguments_types=[pointer(BYTE), pointer(BYTE), ctypes.c_int, pointer(RGBQUAD)],
                return_value=None),
    LibraryHook(name="FreeImage_ConvertLine8To24",
                arguments_types=[pointer(BYTE), pointer(BYTE), ctypes.c_int, pointer(RGBQUAD)],
                return_value=None),
    LibraryHook(name="FreeImage_ConvertLine16To24_555",
                arguments_types=[pointer(BYTE), pointer(BYTE), ctypes.c_int],
                return_value=None),
    LibraryHook(name="FreeImage_ConvertLine16To24_565",
                arguments_types=[pointer(BYTE), pointer(BYTE), ctypes.c_int],
                return_value=None),
    LibraryHook(name="FreeImage_ConvertLine32To24",
                arguments_types=[pointer(BYTE), pointer(BYTE), ctypes.c_int],
                return_value=None),
    LibraryHook(name="FreeImage_ConvertLine1To32",
                arguments_types=[pointer(BYTE), pointer(BYTE), ctypes.c_int, pointer(RGBQUAD)],
                return_value=None),
    LibraryHook(name="FreeImage_ConvertLine4To32",
                arguments_types=[pointer(BYTE), pointer(BYTE), ctypes.c_int, pointer(RGBQUAD)],
                return_value=None),
    LibraryHook(name="FreeImage_ConvertLine8To32",
                arguments_types=[pointer(BYTE), pointer(BYTE), ctypes.c_int, pointer(RGBQUAD)],
                return_value=None),
    LibraryHook(name="FreeImage_ConvertLine16To32_555",
                arguments_types=[pointer(BYTE), pointer(BYTE), ctypes.c_int],
                return_value=None),
    LibraryHook(name="FreeImage_ConvertLine16To32_565",
                arguments_types=[pointer(BYTE), pointer(BYTE), ctypes.c_int],
                return_value=None),
    LibraryHook(name="FreeImage_ConvertLine24To32",
                arguments_types=[pointer(BYTE), pointer(BYTE), ctypes.c_int],
                return_value=None),

    # Smart conversion functions.
    LibraryHook(name="FreeImage_ConvertTo4Bits",
                arguments_types=[pointer(FIBITMAP)],
                return_value=pointer(FIBITMAP)),
    LibraryHook(name="FreeImage_ConvertTo8Bits",
                arguments_types=[pointer(FIBITMAP)],
                return_value=pointer(FIBITMAP)),
    LibraryHook(name="FreeImage_ConvertToGreyscale",
                arguments_types=[pointer(FIBITMAP)],
                return_value=pointer(FIBITMAP)),
    LibraryHook(name="FreeImage_ConvertTo16Bits555",
                arguments_types=[pointer(FIBITMAP)],
                return_value=pointer(FIBITMAP)),
    LibraryHook(name="FreeImage_ConvertTo16Bits565",
                arguments_types=[pointer(FIBITMAP)],
                return_value=pointer(FIBITMAP)),
    LibraryHook(name="FreeImage_ConvertTo24Bits",
                arguments_types=[pointer(FIBITMAP)],
                return_value=pointer(FIBITMAP)),
    LibraryHook(name="FreeImage_ConvertTo32Bits",
                arguments_types=[pointer(FIBITMAP)],
                return_value=pointer(FIBITMAP)),
    LibraryHook(name="FreeImage_ColorQuantize",
                arguments_types=[pointer(FIBITMAP), FREE_IMAGE_QUANTIZE],
                return_value=pointer(FIBITMAP)),
    LibraryHook(name="FreeImage_ColorQuantizeEx",
                arguments_types=[pointer(FIBITMAP), FREE_IMAGE_QUANTIZE, ctypes.c_int, ctypes.c_int, pointer(RGBQUAD)],
                return_value=pointer(FIBITMAP)),
    LibraryHook(name="FreeImage_Threshold",
                arguments_types=[pointer(FIBITMAP), BYTE],
                return_value=pointer(FIBITMAP)),
    LibraryHook(name="FreeImage_Dither",
                arguments_types=[pointer(FIBITMAP), FREE_IMAGE_DITHER],
                return_value=pointer(FIBITMAP)),
    LibraryHook(name="FreeImage_ConvertFromRawBits",
                arguments_types=[pointer(BYTE),
                                 ctypes.c_int,
                                 ctypes.c_int,
                                 ctypes.c_int,
                                 ctypes.c_uint,
                                 ctypes.c_uint,
                                 ctypes.c_uint,
                                 ctypes.c_uint,
                                 BOOL],
                return_value=pointer(FIBITMAP)),
    LibraryHook(name="FreeImage_ConvertToRawBits",
                arguments_types=[pointer(BYTE),
                                 pointer(FIBITMAP),
                                 ctypes.c_int,
                                 ctypes.c_uint,
                                 ctypes.c_uint,
                                 ctypes.c_uint,
                                 ctypes.c_uint,
                                 BOOL],
                return_value=None),
    LibraryHook(name="FreeImage_ConvertToFloat",
                arguments_types=[pointer(FIBITMAP)],
                return_value=pointer(FIBITMAP)),
    LibraryHook(name="FreeImage_ConvertToRGBF",
                arguments_types=[pointer(FIBITMAP)],
                return_value=pointer(FIBITMAP)),
    LibraryHook(name="FreeImage_ConvertToUINT16",
                arguments_types=[pointer(FIBITMAP)],
                return_value=pointer(FIBITMAP)),
    LibraryHook(name="FreeImage_ConvertToRGB16",
                arguments_types=[pointer(FIBITMAP)],
                return_value=pointer(FIBITMAP)),
    LibraryHook(name="FreeImage_ConvertToStandardType",
                arguments_types=[pointer(FIBITMAP), BOOL],
                return_value=pointer(FIBITMAP)),
    LibraryHook(name="FreeImage_ConvertToType",
                arguments_types=[pointer(FIBITMAP), FREE_IMAGE_TYPE, BOOL],
                return_value=pointer(FIBITMAP)),

    # Tone mapping operators functions.
    LibraryHook(name="FreeImage_ToneMapping",
                arguments_types=[pointer(FIBITMAP), FREE_IMAGE_TMO, ctypes.c_double, ctypes.c_double],
                return_value=pointer(FIBITMAP)),
    LibraryHook(name="FreeImage_TmoDrago03",
                arguments_types=[pointer(FIBITMAP), ctypes.c_double, ctypes.c_double],
                return_value=pointer(FIBITMAP)),
    LibraryHook(name="FreeImage_TmoReinhard05",
                arguments_types=[pointer(FIBITMAP), ctypes.c_double, ctypes.c_double],
                return_value=pointer(FIBITMAP)),
    LibraryHook(name="FreeImage_TmoReinhard05Ex",
                arguments_types=[
                    pointer(FIBITMAP), ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double],
                return_value=pointer(FIBITMAP)),
    LibraryHook(name="FreeImage_TmoFattal02",
                arguments_types=[pointer(FIBITMAP), ctypes.c_double, ctypes.c_double],
                return_value=pointer(FIBITMAP)),

    # ZLib functions.
    LibraryHook(name="FreeImage_ZLibCompress",
                arguments_types=[pointer(BYTE), DWORD, pointer(BYTE), DWORD],
                return_value=DWORD),
    LibraryHook(name="FreeImage_ZLibUncompress",
                arguments_types=[pointer(BYTE), DWORD, pointer(BYTE), DWORD],
                return_value=DWORD),
    LibraryHook(name="FreeImage_ZLibGZip",
                arguments_types=[pointer(BYTE), DWORD, pointer(BYTE), DWORD],
                return_value=DWORD),
    LibraryHook(name="FreeImage_ZLibGUnzip",
                arguments_types=[pointer(BYTE), DWORD, pointer(BYTE), DWORD],
                return_value=DWORD),
    LibraryHook(name="FreeImage_ZLibCRC32",
                arguments_types=[DWORD, pointer(BYTE), DWORD],
                return_value=DWORD),

    # Tags creation / destruction functions.
    LibraryHook(name="FreeImage_CreateTag",
                arguments_types=[],
                return_value=pointer(FITAG)),
    LibraryHook(name="FreeImage_DeleteTag",
                arguments_types=[pointer(FITAG)],
                return_value=None),
    LibraryHook(name="FreeImage_CloneTag",
                arguments_types=[pointer(FITAG)],
                return_value=pointer(FITAG)),

    # Tags getters / setters functions.
    LibraryHook(name="FreeImage_GetTagKey",
                arguments_types=[pointer(FITAG)],
                return_value=ctypes.c_char_p),
    LibraryHook(name="FreeImage_GetTagDescription",
                arguments_types=[pointer(FITAG)],
                return_value=ctypes.c_char_p),
    LibraryHook(name="FreeImage_GetTagID",
                arguments_types=[pointer(FITAG)],
                return_value=WORD),
    LibraryHook(name="FreeImage_GetTagType",
                arguments_types=[pointer(FITAG)],
                return_value=FREE_IMAGE_MDTYPE),
    LibraryHook(name="FreeImage_GetTagCount",
                arguments_types=[pointer(FITAG)],
                return_value=DWORD),
    LibraryHook(name="FreeImage_GetTagLength",
                arguments_types=[pointer(FITAG)],
                return_value=DWORD),
    LibraryHook(name="FreeImage_GetTagValue",
                arguments_types=[pointer(FITAG)],
                return_value=pointer(None)),
    LibraryHook(name="FreeImage_SetTagKey",
                arguments_types=[pointer(FITAG), ctypes.c_char_p],
                return_value=BOOL),
    LibraryHook(name="FreeImage_SetTagDescription",
                arguments_types=[pointer(FITAG), ctypes.c_char_p],
                return_value=BOOL),
    LibraryHook(name="FreeImage_SetTagID",
                arguments_types=[pointer(FITAG), WORD],
                return_value=BOOL),
    LibraryHook(name="FreeImage_SetTagType",
                arguments_types=[pointer(FITAG), FREE_IMAGE_MDTYPE],
                return_value=BOOL),
    LibraryHook(name="FreeImage_SetTagCount",
                arguments_types=[pointer(FITAG), DWORD],
                return_value=BOOL),
    LibraryHook(name="FreeImage_SetTagLength",
                arguments_types=[pointer(FITAG), DWORD],
                return_value=BOOL),
    LibraryHook(name="FreeImage_SetTagValue",
                arguments_types=[pointer(FITAG), pointer(None)],
                return_value=BOOL),

    # Iterator functions.
    LibraryHook(name="FreeImage_FindFirstMetadata",
                arguments_types=[FREE_IMAGE_MDMODEL, pointer(FIBITMAP), pointer(pointer(FITAG))],
                return_value=pointer(FIMETADATA)),
    LibraryHook(name="FreeImage_FindNextMetadata",
                arguments_types=[pointer(FIMETADATA), pointer(pointer(FITAG))],
                return_value=BOOL),
    LibraryHook(name="FreeImage_FindCloseMetadata",
                arguments_types=[pointer(FIMETADATA)],
                return_value=None),

    # Metadata getters / setters functions.
    LibraryHook(name="FreeImage_SetMetadata",
                arguments_types=[FREE_IMAGE_MDMODEL, pointer(FIBITMAP), ctypes.c_char_p, pointer(FITAG)],
                return_value=BOOL),
    LibraryHook(name="FreeImage_GetMetadata",
                arguments_types=[FREE_IMAGE_MDMODEL, pointer(FIBITMAP), ctypes.c_char_p, pointer(pointer(FITAG))],
                return_value=BOOL),
    LibraryHook(name="FreeImage_GetMetadataCount",
                arguments_types=[FREE_IMAGE_MDMODEL, pointer(FIBITMAP)],
                return_value=ctypes.c_uint),
    LibraryHook(name="FreeImage_CloneMetadata",
                arguments_types=[pointer(FIBITMAP), pointer(FIBITMAP)],
                return_value=BOOL),

    # Tag to C string conversion function.
    LibraryHook(name="FreeImage_TagToString",
                arguments_types=[FREE_IMAGE_MDMODEL, pointer(FITAG), ctypes.c_char_p],
                return_value=ctypes.c_char_p),

    # Rotation and flipping functions.
    LibraryHook(name="FreeImage_RotateClassic",
                arguments_types=[pointer(FIBITMAP), ctypes.c_double],
                return_value=pointer(FIBITMAP)),
    LibraryHook(name="FreeImage_Rotate",
                arguments_types=[pointer(FIBITMAP), ctypes.c_double, pointer(None)],
                return_value=pointer(FIBITMAP)),
    LibraryHook(name="FreeImage_RotateEx",
                arguments_types=[pointer(FIBITMAP),
                                 ctypes.c_double,
                                 ctypes.c_double,
                                 ctypes.c_double,
                                 ctypes.c_double,
                                 ctypes.c_double,
                                 BOOL],
                return_value=pointer(FIBITMAP)),
    LibraryHook(name="FreeImage_FlipHorizontal",
                arguments_types=[pointer(FIBITMAP)],
                return_value=BOOL),
    LibraryHook(name="FreeImage_FlipVertical",
                arguments_types=[pointer(FIBITMAP)],
                return_value=BOOL),
    LibraryHook(name="FreeImage_JPEGTransform",
                arguments_types=[ctypes.c_char_p, ctypes.c_char_p, FREE_IMAGE_JPEG_OPERATION, BOOL],
                return_value=BOOL),
    LibraryHook(name="FreeImage_JPEGTransformU",
                arguments_types=[pointer(ctypes.c_wchar), pointer(ctypes.c_wchar), FREE_IMAGE_JPEG_OPERATION, BOOL],
                return_value=BOOL),

    # Upsampling / downsampling functions.
    LibraryHook(name="FreeImage_Rescale",
                arguments_types=[pointer(FIBITMAP), ctypes.c_int, ctypes.c_int, FREE_IMAGE_FILTER],
                return_value=pointer(FIBITMAP)),
    LibraryHook(name="FreeImage_MakeThumbnail",
                arguments_types=[pointer(FIBITMAP), ctypes.c_int, BOOL],
                return_value=pointer(FIBITMAP)),

    # Color manipulation functions.
    LibraryHook(name="FreeImage_AdjustCurve",
                arguments_types=[pointer(FIBITMAP), pointer(BYTE), FREE_IMAGE_COLOR_CHANNEL],
                return_value=BOOL),
    LibraryHook(name="FreeImage_AdjustGamma",
                arguments_types=[pointer(FIBITMAP), ctypes.c_double],
                return_value=BOOL),
    LibraryHook(name="FreeImage_AdjustBrightness",
                arguments_types=[pointer(FIBITMAP), ctypes.c_double],
                return_value=BOOL),
    LibraryHook(name="FreeImage_AdjustContrast",
                arguments_types=[pointer(FIBITMAP), ctypes.c_double],
                return_value=BOOL),
    LibraryHook(name="FreeImage_Invert",
                arguments_types=[pointer(FIBITMAP)],
                return_value=BOOL),
    LibraryHook(name="FreeImage_GetHistogram",
                arguments_types=[pointer(FIBITMAP), pointer(DWORD), FREE_IMAGE_COLOR_CHANNEL],
                return_value=BOOL),
    LibraryHook(name="FreeImage_GetAdjustColorsLookupTable",
                arguments_types=[pointer(BYTE), ctypes.c_double, ctypes.c_double, ctypes.c_double, BOOL],
                return_value=ctypes.c_int),
    LibraryHook(name="FreeImage_AdjustColors",
                arguments_types=[pointer(FIBITMAP), ctypes.c_double, ctypes.c_double, ctypes.c_double, BOOL],
                return_value=BOOL),
    LibraryHook(name="FreeImage_ApplyColorMapping",
                arguments_types=[pointer(FIBITMAP), pointer(RGBQUAD), pointer(RGBQUAD), ctypes.c_uint, BOOL, BOOL],
                return_value=ctypes.c_uint),
    LibraryHook(name="FreeImage_SwapColors",
                arguments_types=[pointer(FIBITMAP), pointer(RGBQUAD), pointer(RGBQUAD), BOOL],
                return_value=ctypes.c_uint),
    LibraryHook(name="FreeImage_ApplyPaletteIndexMapping",
                arguments_types=[pointer(FIBITMAP), pointer(BYTE), pointer(BYTE), ctypes.c_uint, BOOL],
                return_value=ctypes.c_uint),
    LibraryHook(name="FreeImage_SwapPaletteIndices",
                arguments_types=[pointer(FIBITMAP), pointer(BYTE), pointer(BYTE)],
                return_value=ctypes.c_uint),

    # Channel processing functions.
    LibraryHook(name="FreeImage_GetChannel",
                arguments_types=[pointer(FIBITMAP), FREE_IMAGE_COLOR_CHANNEL],
                return_value=pointer(FIBITMAP)),
    LibraryHook(name="FreeImage_SetChannel",
                arguments_types=[pointer(FIBITMAP), pointer(FIBITMAP), FREE_IMAGE_COLOR_CHANNEL],
                return_value=BOOL),
    LibraryHook(name="FreeImage_GetComplexChannel",
                arguments_types=[pointer(FIBITMAP), FREE_IMAGE_COLOR_CHANNEL],
                return_value=pointer(FIBITMAP)),
    LibraryHook(name="FreeImage_SetComplexChannel",
                arguments_types=[pointer(FIBITMAP), pointer(FIBITMAP), FREE_IMAGE_COLOR_CHANNEL],
                return_value=BOOL),

    # Copy / paste / composite functions.
    LibraryHook(name="FreeImage_Copy",
                arguments_types=[pointer(FIBITMAP), ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int],
                return_value=pointer(FIBITMAP)),
    LibraryHook(name="FreeImage_Paste",
                arguments_types=[pointer(FIBITMAP), pointer(FIBITMAP), ctypes.c_int, ctypes.c_int, ctypes.c_int],
                return_value=BOOL),
    LibraryHook(name="FreeImage_Composite",
                arguments_types=[pointer(FIBITMAP), BOOL, pointer(RGBQUAD), pointer(FIBITMAP)],
                return_value=pointer(FIBITMAP)),
    LibraryHook(name="FreeImage_JPEGCrop",
                arguments_types=[ctypes.c_char_p, ctypes.c_char_p,
                                 ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int],
                return_value=BOOL),
    LibraryHook(name="FreeImage_JPEGCropU",
                arguments_types=[pointer(ctypes.c_wchar),
                                 pointer(ctypes.c_wchar),
                                 ctypes.c_int,
                                 ctypes.c_int,
                                 ctypes.c_int,
                                 ctypes.c_int],
                return_value=BOOL),
    LibraryHook(name="FreeImage_PreMultiplyWithAlpha",
                arguments_types=[pointer(FIBITMAP)],
                return_value=BOOL),

    # Background filling functions.
    LibraryHook(name="FreeImage_FillBackground",
                arguments_types=[pointer(FIBITMAP), pointer(None), ctypes.c_int],
                return_value=BOOL),
    LibraryHook(name="FreeImage_EnlargeCanvas",
                arguments_types=[pointer(FIBITMAP),
                                 ctypes.c_int,
                                 ctypes.c_int,
                                 ctypes.c_int,
                                 ctypes.c_int,
                                 pointer(None),
                                 ctypes.c_int],
                return_value=pointer(FIBITMAP)),
    LibraryHook(name="FreeImage_AllocateEx",
                arguments_types=[ctypes.c_int,
                                 ctypes.c_int,
                                 ctypes.c_int,
                                 pointer(RGBQUAD),
                                 ctypes.c_int,
                                 pointer(RGBQUAD),
                                 ctypes.c_uint,
                                 ctypes.c_uint,
                                 ctypes.c_uint],
                return_value=pointer(FIBITMAP)),
    LibraryHook(name="FreeImage_AllocateExT",
                arguments_types=[FREE_IMAGE_TYPE,
                                 ctypes.c_int,
                                 ctypes.c_int,
                                 ctypes.c_int,
                                 pointer(None),
                                 ctypes.c_int,
                                 pointer(RGBQUAD),
                                 ctypes.c_uint,
                                 ctypes.c_uint,
                                 ctypes.c_uint],
                return_value=pointer(FIBITMAP)),

    # Miscellaneous algorithms functions.
    LibraryHook(name="FreeImage_MultigridPoissonSolver",
                arguments_types=[pointer(FIBITMAP), ctypes.c_int],
                return_value=pointer(FIBITMAP)),

    # Custom functions.
    LibraryHook(name="FreeImage_HDRLabs_ConvertToLdr",
                arguments_types=[pointer(FIBITMAP), ctypes.c_double],
                return_value=pointer(FIBITMAP)),)


def get_free_image_library_path():
    """
    Returns the FreeImage library path.

    :return: FreeImage library path.
    :rtype: unicode
    """

    global FREEIMAGE_LIBRARY_PATH
    if FREEIMAGE_LIBRARY_PATH is None:
        for path in (os.path.join(foundations.common.get_first_item(sibl_gui.__path__), Constants.freeimage_library),
                     os.path.join(os.getcwd(), sibl_gui.__name__, Constants.freeimage_library)):
            if foundations.common.path_exists(path):
                FREEIMAGE_LIBRARY_PATH = path
                continue
    return FREEIMAGE_LIBRARY_PATH


class ImageInformationsHeader(foundations.data_structures.Structure):
    """
    Defines a storage object for image informations header.
    """

    def __init__(self, **kwargs):
        """
        Initializes the class.

        :param kwargs: path, width, height, bpp, os_stats.
        :type kwargs: dict
        """

        LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

        foundations.data_structures.Structure.__init__(self, **kwargs)


class Image(object):
    """
    Defines various methods to manipulate images files.
    """

    def __init__(self, image_path=None):
        """
        Initializes the class.

        :param image_path: Image path.
        :type image_path: unicode
        """

        LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

        # --- Setting class attributes. ---
        self.__library = foundations.library.Library(get_free_image_library_path(), FREEIMAGE_FUNCTIONS)

        self.__errors_callback = self.__library.callback(self.__log_library_errors)
        self.__library.library.FreeImage_SetOutputMessage(self.__errors_callback)

        self.__image_path = None
        self.image_path = image_path

        self.__bitmap = None

        if image_path:
            self.load()

    @property
    def library(self):
        """
        Property for **self.__library** attribute.

        :return: self.__library.
        :rtype: Library
        """

        return self.__library

    @library.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def library(self, value):
        """
        Setter for **self.__library** attribute.

        :param value: Attribute value.
        :type value: Library
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "library"))

    @library.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def library(self):
        """
        Deleter for **self.__library** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "library"))

    @property
    def errors_callback(self):
        """
        Property for **self.__errors_callback** attribute.

        :return: self.__errors_callback.
        :rtype: object
        """

        return self.__errors_callback

    @errors_callback.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def errors_callback(self, value):
        """
        Setter for **self.__errors_callback** attribute.

        :param value: Attribute value.
        :type value: object
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "errors_callback"))

    @errors_callback.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def errors_callback(self):
        """
        Deleter for **self.__errors_callback** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "errors_callback"))

    @property
    def image_path(self):
        """
        Property for **self.__image_path** attribute.

        :return: self.__image_path.
        :rtype: unicode
        """

        return self.__image_path

    @image_path.setter
    @foundations.exceptions.handle_exceptions(AssertionError)
    def image_path(self, value):
        """
        Setter for **self.__image_path** attribute.

        :param value: Attribute value.
        :type value: unicode
        """

        if value is not None:
            assert type(value) is unicode, "'{0}' attribute: '{1}' type is not 'unicode'!".format("image_path", value)
        self.__image_path = value

    @image_path.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def image_path(self):
        """
        Deleter for **self.__image_path** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "image_path"))

    @property
    def bitmap(self):
        """
        Property for **self.__bitmap** attribute.

        :return: self.__bitmap.
        :rtype: object
        """

        return self.__bitmap

    @bitmap.setter
    @foundations.exceptions.handle_exceptions(AssertionError)
    def bitmap(self, value):
        """
        Setter for **self.__bitmap** attribute.

        :param value: Attribute value.
        :type value: object
        """

        self.__bitmap = value

    @bitmap.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def bitmap(self):
        """
        Deleter for **self.__bitmap** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "bitmap"))

    @foundations.exceptions.handle_exceptions(foundations.exceptions.LibraryExecutionError)
    def __log_library_errors(self, error_code, message):
        """
        Logs the Library errors.
        """

        raise foundations.exceptions.LibraryExecutionError("{0} | Exit code '{1}', message: '{2}'".format(
            self.__class__.__name__, error_code, message))

    def get_image_format(self, image_path=None):
        """
        Gets the file format.

        :param image_path: Image path.
        :type image_path: unicode
        :return: File format.
        :rtype: FREE_IMAGE_FORMAT
        """

        image_path = image_path or self.__image_path
        if not image_path:
            return

        file_format = self.__library.FreeImage_GetFileType(image_path, False)
        if file_format == -1:
            file_format = self.__library.FreeImage_GetFIFFromFilename(image_path)
        return file_format

    @foundations.exceptions.handle_exceptions(foundations.exceptions.LibraryExecutionError)
    def load(self):
        """
        Loads the file.

        :return: Method success.
        :rtype: bool
        """

        if not self.__image_path:
            return False

        image_format = self.get_image_format(self.__image_path)
        if image_format != FIF_UNKNOWN:
            if self.__library.FreeImage_FIFSupportsReading(image_format):
                self.__bitmap = self.__library.FreeImage_Load(image_format, self.__image_path, FI_DEFAULT_NULL)
                self.__bitmap and LOGGER.debug("> '{0}' image has been loaded!".format(self.__image_path))
                return True
            else:
                raise foundations.exceptions.LibraryExecutionError("{0} | '{1}' format read isn't supported!".format(
                    self.__class__.__name__, FIF_LOOKUP.get_first_key_from_value(image_format)))

    def save(self):
        """
        Saves the file.

        :return: Method success.
        :rtype: bool
        """

        return self.save_as(self.get_image_format(self.__image_path), self.__image_path, FI_DEFAULT_NULL)

    @foundations.exceptions.handle_exceptions(foundations.exceptions.LibraryExecutionError)
    def save_as(self, image_format, image_path, flags=FI_DEFAULT_NULL):
        """
        Saves the image to the given file.

        :param image_format: Image format.
        :type image_format: int
        :param image_path: Image path.
        :type image_path: unicode
        :param flags: Save flags.
        :type flags: int
        :return: Method success.
        :rtype: bool
        """

        if self.__library.FreeImage_FIFSupportsWriting(image_format):
            if not image_path:
                return False
            if self.__library.FreeImage_Save(image_format, self.__bitmap, image_path, flags):
                LOGGER.debug("> '{0}' image has been saved!".format(image_path))
                return True
        else:
            raise foundations.exceptions.LibraryExecutionError(
                "{0} | '{1}' format write isn't supported!".format(image_format))

    def convert_to_type(self, target_type, linear_scale=True):
        """
        Converts the bitmap to given type.

        :param target_type: Target type.
        :type target_type: int
        :param linear_scale: Linear scale.
        :type linear_scale: bool
        :return: Method success.
        :rtype: bool
        """

        LOGGER.debug("> Converting '{0}' image bitmap to type '{1}'!".format(self.__image_path, target_type))
        self.__bitmap = self.__library.FreeImage_ConvertToType(self.__bitmap, target_type, linear_scale)
        if self.__bitmap:
            LOGGER.debug("> '{0}' image bitmap conversion to type '{1}' done!".format(self.__image_path, target_type))
            return True

    def convert_to_ldr(self, gamma=2.2):
        """
        Converts the HDR bitmap to LDR.

        :param gamma: Image conversion gamma.
        :type gamma: float
        :return: Method success.
        :rtype: bool
        """

        LOGGER.debug("> Converting '{0}' HDR image bitmap to LDR!".format(self.__image_path))
        self.__bitmap = self.__library.FreeImage_HDRLabs_ConvertToLdr(self.__bitmap, gamma)
        if self.__bitmap:
            LOGGER.debug("> '{0}' HDR image bitmap conversion to LDR done!".format(self.__image_path))
            return True

    @foundations.exceptions.handle_exceptions(foundations.exceptions.LibraryExecutionError)
    def convert_to_QImage(self):
        """
        Converts the bitmap to `QImage <http://doc.qt.nokia.com/qimage.html>`_.

        :return: Converted image.
        :rtype: QImage
        """

        bpp = self.__library.FreeImage_GetBPP(self.__bitmap)
        (self.__library.FreeImage_GetImageType(self.__bitmap) == FIT_RGBF or self.__library.FreeImage_GetImageType(
            self.__bitmap) == FIT_RGBAF) and self.convert_to_ldr(2.2)

        if self.__library.FreeImage_GetImageType(self.__bitmap) == FIT_BITMAP:
            LOGGER.debug("> Converting '{0}' image bitmap to QImage!".format(self.__image_path))

            from PyQt4.QtGui import QImage
            from sip import voidptr

            width = self.__library.FreeImage_GetWidth(self.__bitmap)
            height = self.__library.FreeImage_GetHeight(self.__bitmap)
            pitch = width * (BPP_32 / 8)
            bits = ctypes.create_string_buffer(chr(0) * height * pitch)
            self.__library.FreeImage_ConvertToRawBits(bits,
                                                      self.__bitmap,
                                                      pitch,
                                                      BPP_32,
                                                      FI_RGBA_RED_MASK,
                                                      FI_RGBA_GREEN_MASK,
                                                      FI_RGBA_BLUE_MASK,
                                                      True)

            self.__library.FreeImage_Unload(self.__bitmap)

            bits_pointer = ctypes.addressof(bits)

            LOGGER.debug("> Initializing image from memory pointer '{0}' address.".format(bits_pointer))
            LOGGER.debug("> Image width: '{0}'.".format(width))
            LOGGER.debug("> Image height: '{0}'.".format(height))
            LOGGER.debug("> Image pitch: '{0}'.".format(pitch))
            LOGGER.debug("> Initializing QImage with memory pointer '{0}' address.".format(bits_pointer))

            image = QImage(voidptr(bits_pointer, size=height * pitch), width, height, pitch, QImage.Format_RGB32)

            image.data = ImageInformationsHeader(path=self.__image_path,
                                                 width=width,
                                                 height=height,
                                                 bpp=bpp,
                                                 os_stats=os.stat(self.__image_path))

            # Removing the following line would result in a blank image display the first time.
            LOGGER.debug("> Final memory pointer with '{0}' address.".format(image.bits().__int__()))

            LOGGER.debug("> '{0}' image bitmap conversion to QImage done!".format(self.__image_path))

            return image
        else:
            raise foundations.exceptions.LibraryExecutionError("{0} | Image bitmap is not of type '{1}'!".format(
                FREE_IMAGE_TYPE.FIT_BITMAP))
