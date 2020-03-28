# coding: utf-8
#
# maxe.ext.read.xml: extensions to read XML.
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

import maxe.xml      as mx
import maxe.ext.read as mer

# ============================================================================
# DATA TYPES

# ============================================================================
# PROCEDURES

# ----------------------------------------------------------------------------
# ReadParamCli(maxe.__main__.Ctx): ReadParam
#   Read a ReadParam from command-line context:

def ReadParamCli(cliCtx):
    param = mx.MakeReadParam()
    mx.AddPathToReadParam(param, cliCtx.curPath)
    i = 0; n = len(cliCtx.paths)
    while i < n:
        mx.AddPathToReadParam(param, cliCtx.paths[i]); i += 1
    return param

# ----------------------------------------------------------------------------
# ReadParamXArg(XArg): ReadParam
#   Read a ReadParam from XArg.
#   NOTE: no-op for now.

def ReadParamXArg(xArg):
    param = mx.MakeReadParam()
    return param

# ----------------------------------------------------------------------------
# ReadStrm(Strm, ReadParam): Xml
#   Read XML from stream.

def ReadStrm(strm, param):
    return mx.ReadXml(strm, param)

# ----------------------------------------------------------------------------
# ReadText(Text, ReadParam): Xml
#   Read text as XML.

#   Serialized XML normally specifies the encoding in the XML declaration at 
#   the beginning of the file: '<?xml ...?>'. It may only omit the encoding or
#   the whole declaration if the encoding is UTF-8 or UTF-16. If the stream
#   was decoded externally, the specified encoding becomes moot (although may 
#   still be used for information about the original stream).

# TODO: find if I can read XML from Unicode in lxml.


# ----------------------------------------------------------------------------
# Reader: XML file reader.

Reader = mer.MakeReader("XML", ReadStrm, None, ReadParamXArg, ReadParamCli)
mer.AddFileExt(Reader, ".xml")
mer.AddMimeType(Reader, "text/xml")



