# coding: utf-8
#
# maxe.read: extensions to read files and text-based data formats.
#
# Copyright (C) 2020 Mikhail Edoshin.
#
# This file is part of Maxe.
#
# Maxe is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# Maxe is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License
# along with Maxe.  If not, see <https://www.gnu.org/licenses/>.

# ============================================================================

from __future__ import absolute_import

import pdb       as pd; pd = pd

import maxe.msg  as mm
import maxe.path as mp
import maxe.strm as ms
import maxe.xml  as mx

# ============================================================================
# DATA TYPES

# ----------------------------------------------------------------------------
# Reader
#   type: reader type, str.
#   readText: function to read text, (Text, Param): Xml
#   readStrm: function to read streams, (Strm, Param): Xml
#   readParamXArg: function to read parameter from XArg, (XArg): Param
#   readParamCli: function to read parameters from CLI, (CliCtx): Param
#   exts: filename extensions, [str].
#   mimeTypes: MIME types, [str]
#   Usage:
#       AddFileExt(Reader, str)
#       AddMimeType(Reader, str)
#       MakeReader(str, func, func, func, func): Reader
#       RegReader(str, Reader)

class Reader(object):
    __slots__ = "type", "readText", "readStrm", "readParamXArg", \
            "readParamCli", "exts", "mimeTypes"

# ============================================================================
# PROCEDURES

# ----------------------------------------------------------------------------
# AddFileExt(Reader, str)
#   Add a file extension.

def AddFileExt(reader, extStr):
    RegReader(extStr, reader)
    reader.exts.append(extStr)

# ----------------------------------------------------------------------------
# AddMimeType(Reader, str)
#   Add a MIME type.

def AddMimeType(reader, mimeTypeStr):
    RegReader(mimeTypeStr, reader)
    reader.mimeTypes.append(mimeTypeStr)

# ----------------------------------------------------------------------------
# GetFmtXfrm(str): str
#   Get an xfrm of a format name (reader name, file extension, MIME type).

def GetFmtXfrm(extStr):
    return extStr.lower()

# ----------------------------------------------------------------------------
# GetReader(str): Reader
#   Get the reader.

def GetReader(fmt):
    fmtXfrm = GetFmtXfrm(fmt)
    try:
        reader = Readers[fmtXfrm]
    except KeyError:
        raise Exception("Failed to find a reader for '%s'" % fmt)
    return reader

# ----------------------------------------------------------------------------
# MakeReader(str, func, func, func, func): Reader
#   Make a Reader.

def MakeReader(name, readStrm, readText, readParamXArg, readParamCli):
    reader = Reader()
    reader.type = name
    RegReader(name, reader)
    reader.readStrm = readStrm
    reader.readText = readText
    reader.readParamXArg = readParamXArg
    reader.readParamCli = readParamCli
    reader.exts = []
    reader.mimeTypes = []
    return reader

# ----------------------------------------------------------------------------
# ReadFile(Reader, mp.Path, func, param): Xml
#   Read a file given a reader, a path, and optional parameter.

def ReadFile(reader, path, param):
    if not reader.readStrm:
        raise Exception("The reader does not support stream reading")
    strm = ms.MakeIStrmFromPath(path)
    try:
        xml = reader.readStrm(strm, param)
    finally:
        ms.DropStrm(strm)
    return xml

# ----------------------------------------------------------------------------
# ReadFileFromCli(mp.Path, str, CliCtx): mx.Xml
#   Read file as XML given a command-line context.

def ReadFileFromCli(path, fmt, cliCtx):
    if not fmt:
        fmt = mp.GetPathExt(path)
    reader = GetReader(fmt)
    # When calling from command line we always have command line context, but
    # not every reader needs it.
    if reader.readParamCli:
        param = reader.readParamCli(cliCtx)
    else:
        param = None 
    return ReadFile(reader, path, param)

# ----------------------------------------------------------------------------
# ReadParamXArg(Reader, XArg Param
#   Read the parameter from XArg.

def ReadParamXArg(reader, param):
    if param is not None:
        if reader.readParamXArg:
            param = reader.readParamXArg(param)
        else:
            raise Exception("The reader does not support parameters")
    return param

# ----------------------------------------------------------------------------
# RegReader(str, Reader)
#   Register a reader for a format string.

def RegReader(fmtStr, reader):
    fmtXfrm = GetFmtXfrm(fmtStr)
    if fmtXfrm in Readers:
        raise Exception("There already exists a reader for '%s'" % fmtStr)
    Readers[fmtXfrm] = reader

# ----------------------------------------------------------------------------
# XReadFile(_, XArg, XArg?, XArg?): XArg(NSet)
#   XPath function to read a file. 

def XReadFile(_, pathArg, fmtArg=None, paramArg=None):
    try:
        path = mx.GetXArgAsPath(pathArg)
        fmt = None
        if fmtArg is not None:
            fmt = mx.GetXArgAsStr(fmtArg)
            if fmt == "":
                fmt = None
        if fmt is None:
            fmt = mp.GetPathExt(path)
        reader = GetReader(fmt)
        result = ReadFile(reader, path, ReadParamXArg(reader, paramArg))
    except Exception as exc:
        result = mm.GetExcAsXml(exc)
    return [result]

# ----------------------------------------------------------------------------
# XReadText(_, XArg, XArg, XArg?): XArg(NSet)
#   XPath function to read a text. Return <maxe:text type> with contents.

def XReadText(_, textArg, fmtArg, paramArg=None):
    try:
        text = mx.GetXArgAsStr(textArg)
        fmt = mx.GetXArgAsStr(fmtArg)
        reader = GetReader(fmt)
        if not reader.readText:
            raise Exception("The reader does not support text reading")
        result = reader.readText(text, ReadParamXArg(reader, paramArg))
    except Exception as exc:
        result = mm.GetExcAsXml(exc)
    return [result]

# CODE ======================================================================

# ----------------------------------------------------------------------------
# Readers: readers by name, file extension or MIME type, {str:Reader}

Readers = {}

# ----------------------------------------------------------------------------
# Register extensions.

mx.RegExts("urn:onegasoft:Maxe/Ext",
    "read-file", mx.ExtFunc, XReadFile,
    "read-text", mx.ExtFunc, XReadText)
