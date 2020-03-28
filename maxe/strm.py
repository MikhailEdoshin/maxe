# coding: utf-8
#
# maxe.strm: streams.
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

import sys         as ps # stdin/out attributes

import maxe.compat as mc # streams in memory, stdin/out binary stream.
import maxe.path   as mp # streams from paths

# ============================================================================
# Data types.

# ----------------------------------------------------------------------------
# Strm: binary input or output stream. 

#   type: stream type, StrmType*.
#   fhdl: file handle open for writing in binary mode.
#
# Usage:
# - DropStrm(Strm)
# + MakeIStrmInMem(bytes): Strm
# + MakeIStrmFromPath(mp.Path): Strm
# + MakeIStrmFromStdin(): Strm
# + MakeOStrmFromPath(mp.Path): Strm
# + MakeOStrmFromStdoit(): Strm
#   ReadStrm(Strm): bytes

class Strm(object):
    __slots__ = "type", "fhdl"

# ----------------------------------------------------------------------------
# StrmType: stream type.
#   Usage: Strm.type.

StrmTypeFile = 0
StrmTypePipe = 1
StrmTypeTty  = 2
StrmTypeMem  = 3

# ============================================================================
# Functions.

# ----------------------------------------------------------------------------
# DropStrm(Strm):
#   Dispose a Strm.

def DropStrm(strm):
    if strm.type == StrmTypeFile:
        strm.fhdl.close()

# ----------------------------------------------------------------------------
# MakeIStrmInMem(bytes): Strm
#   Make an input stream from bytes in memory.

def MakeIStrmInMem(data):
    strm = Strm()
    strm.type = StrmTypeMem
    strm.fhdl = mc.MakeFhdlInMem(data)
    return strm

# ----------------------------------------------------------------------------
# MakeIStrmFromFile(mp.Path): Strm
#   Make an input stream from a file.

def MakeIStrmFromPath(path):
    if not mp.PathExists(path) or not mp.PathIsFile(path):
        raise Exception("The input path '%s' does not exist or is not a file" 
                % mp.GetPathStr(path))
    strm = Strm()
    strm.type = StrmTypeFile
    strm.fhdl = open(mp.GetPathStr(path), "rb")
    return strm

# ----------------------------------------------------------------------------
# MakeIStrmFromStdin(): Strm
#   Make an input stream from standard input.

def MakeIStrmFromStdin():
    strm = Strm()
    if ps.stdin.isatty():
        strm.type = StrmTypeTty
    else:
        strm.type = StrmTypePipe
    strm.fhdl = mc.GetStdinFhdl()
    return strm

# ----------------------------------------------------------------------------
# MakeOStrmFromPath(mp.Path): Strm
#   Make an out-Strm from an mp.Path.

def MakeOStrmFromPath(path):
    if mp.PathExists(path) and not mp.PathIsFile(path):
        raise Exception("The output path '%s' exists and is not a file" %
                mp.GetPathStr(path))
    strm = Strm()
    strm.type = StrmTypeFile
    strm.fhdl = open(mp.GetPathStr(path), "wb")
    return strm

# ----------------------------------------------------------------------------
# MakeOStrmFromStdout(): Strm
#   Make an out-Strm from standard output.

def MakeOStrmFromStdout():
    strm = Strm()
    if ps.stdout.isatty():
        strm.type = StrmTypeTty
    else:
        strm.type = StrmTypePipe
    strm.fhdl = mc.GetStdoutFhdl()
    return strm
# ---------------------------------------------------------------------------
# ReadStrm(Strm): bytes
#   Read data from an IStrm.

def ReadStrm(strm):
    return strm.fhdl.read()

# ----------------------------------------------------------------------------
# ReadText(Strm, str): Text
#   Read and decode a stream.

def ReadText(strm, enc):
    return ReadStrm(strm).decode(enc)

