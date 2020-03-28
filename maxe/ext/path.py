# coding: utf-8
#
# maxe.ext.path: XPath and XSLT extensions to work with paths.
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

# Declarations ===============================================================

# ----------------------------------------------------------------------------
# GetPathAsXml(mp.Path): Xml(Elt)
#   Get path as XML (without stats).
#
#       <maxe:path path>

def GetPathAsXml(path):
    pathElt = mx.MakeElt(mxQNameMxPath)
    mx.SetAttr(pathElt, mxQNamePath, mp.GetPathStr(path))
    return pathElt

# ----------------------------------------------------------------------------
# GetPathStatAsXml(mp.Path): Xml(Elt)
#   Get stat of a path as XML.
#
#       <maxe:non-existing-path path>
#       <maxe:directory path name ctime mtime>
#       <maxe:file path name ctime mtime atime size stem ext>
#       <maxe:unknown-path-type path>
#
#   The function does not scan directories; see 'ScanDirAsXml'.

def GetPathStatAsXml(path):
    if not mp.PathExists(path):
        qName = mxQNameMxPath
    elif mp.PathIsDir(path):
        qName = mxQNameMxDirectory
    elif mp.PathIsFile(path):
        qName = mxQNameMxFile
    else:
        qName = mxQNameMxUnknownPathType
    pathElt = mx.MakeElt(qName)
    mx.SetAttr(pathElt, mxQNamePath, mp.GetPathStr(path))
    if mp.PathIsFile(path) or mp.PathIsDir(path):
        mx.SetAttr(pathElt, mxQNameName, mp.GetPathName(path))
        mx.SetAttr(pathElt, mxQNameCtime, str(mp.GetPathCtime(path)))
        mx.SetAttr(pathElt, mxQNameMtime, str(mp.GetPathMtime(path)))
        if mp.PathIsFile(path):
            mx.SetAttr(pathElt, mxQNameAtime, str(mp.GetPathAtime(path)))
            mx.SetAttr(pathElt, mxQNameSize, str(mp.GetPathSize(path)))
            mx.SetAttr(pathElt, mxQNameStem, mp.GetPathStem(path))
            mx.SetAttr(pathElt, mxQNameExt, mp.GetPathExt(path))
    return pathElt

# ----------------------------------------------------------------------------
# ScanDirAsXml(mp.Path): le.Element
#   Read the directory tree as XML.
#
#   <maxe:directory path name ctime mtime>...</maxe:directory>

def ScanDirAsXml(path):
    dirElt = GetPathStatAsXml(path)
    ScanDirEltAsXml(path, dirElt)
    return dirElt

# ----------------------------------------------------------------------------
# ScanDirEltAsXml(mp.Path, le.Element)
#   Read the directory tree as XML, actual worker.

def ScanDirEltAsXml(path, pathElt):
    for name in mp.ListDir(path):
        subpath = mp.MakeSubpath(path, name)
        subpathElt = GetPathStatAsXml(subpath)
        if mp.PathIsDir(subpath):
            ScanDirEltAsXml(subpath, subpathElt)
        mx.AppendElt(pathElt, subpathElt)
        
# Extensions =================================================================

# ----------------------------------------------------------------------------
# XGetPathStat(_, path): Xml(Elt)
#   XPath function to get stats of a path. 
#
#   path: path, string or element.

def XGetPathStat(_, pathArg):
    try:
        pathStr = mx.GetXArgAsStr(pathArg)
        result = GetPathStatAsXml(mp.MakePath(pathStr))
    except Exception as exc:
        result = mm.GetExcAsXml(exc)
    return result

# ---------------------------------------------------------------------------
# XListDirectory(_, pathArg): [le._Element]
#   XPath function to list a directory.
#
#   path: path, string or element.

def XListDirectory(_, pathArg):
    try:
        pathStr = mx.GetXArgAsStr(pathArg)
        path = mp.MakePath(pathStr)
        result = []
        for name in mp.ListDir(path):
            result.append(GetPathStatAsXml(mp.MakeSubpath(path, name)))
    except Exception as exc:
        result = mm.GetExcAsXml(exc)
    return result

# ---------------------------------------------------------------------------
# XScanDirectory(_, pathArg): le._Element
#   XPath function to get a directory tree.
#
#   path: path, string or element.

def XScanDirectory(leCtx, pathArg):
    try:
        pathStr = mx.GetXArgAsStr(pathArg)
        result = ScanDirAsXml(mp.MakePath(pathStr))
    except Exception as exc:
        result = mm.GetExcAsXml(exc)
    return result

# CODE =======================================================================

import pdb       as pd; pd = pd # debugger

import maxe.msg  as mm
import maxe.path as mp
import maxe.xml  as mx

# mxNs and QNames.

mxNs   = mx.GetNs("")
mxNsMx = mx.GetNs("urn:onegasoft:Maxe")

mxQNameMxDirectory       = mx.GetQName(mxNsMx, "directory"        )
mxQNameMxFile            = mx.GetQName(mxNsMx, "file"             )
mxQNameMxPath            = mx.GetQName(mxNsMx, "path"             )
mxQNameMxUnknownPathType = mx.GetQName(mxNsMx, "unknown-path-type")

mxQNameAtime             = mx.GetQName(mxNs  , "atime"            )
mxQNameCtime             = mx.GetQName(mxNs  , "ctime"            )
mxQNameExt               = mx.GetQName(mxNs  , "ext"              )
mxQNameMessage           = mx.GetQName(mxNs  , "message"          )
mxQNameMtime             = mx.GetQName(mxNs  , "mtime"            )
mxQNameName              = mx.GetQName(mxNs  , "name"             )
mxQNamePath              = mx.GetQName(mxNs  , "path"             )
mxQNameSize              = mx.GetQName(mxNs  , "size"             )
mxQNameStem              = mx.GetQName(mxNs  , "stem"             )
mxQNameType              = mx.GetQName(mxNs  , "type"             )

# Register extensions.

mx.RegExts("urn:onegasoft:Maxe/Ext",
    "get-path-stat" , mx.ExtFunc, XGetPathStat  ,
    "list-directory", mx.ExtFunc, XListDirectory,
    "scan-directory", mx.ExtFunc, XScanDirectory)

