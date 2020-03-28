# config: utf-8
#
# maxe.path: Path tools.
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

# ============================================================================
# Data types

# ----------------------------------------------------------------------------
# Path
#   A filesystem path.
#
#   pathStr: path string, str.
#   pathStat: most recent path stat result, PathStat or None.
#
# Usage:
#   mx.AddPath(mx.Ctx, Path)

class Path(object):
    __slots__ = "pathStr", "pathStat"

# ----------------------------------------------------------------------------
# PathStat
#   Path stat results
#
#   path: the path the pathstat is for, Path.
#   poStat: stat result, os.stat_result.

class PathStat(object):
    __slots__ = "path", "poStat"

# ============================================================================
# Functions

# ----------------------------------------------------------------------------
# GetCurPath(): Path
#   Get the current path.

def GetCurPath():
    return MakePath(po.getcwd())

# ----------------------------------------------------------------------------
# GetPathAtime(Path): int(UnixTime)
#   Get path access time.

def GetPathAtime(path):
    return GetPathStat(path).poStat.st_atime

# ----------------------------------------------------------------------------
# GetParentPath(Path): Path
#   Get the parent path.

def GetParentPath(path):
    return MakePath(pop.dirname(path.pathStr))

# ----------------------------------------------------------------------------
# GetPathCtime(Path): int(UnixTime)
#   Get path creation time.

def GetPathCtime(path):
    return GetPathStat(path).poStat.st_ctime

# ----------------------------------------------------------------------------
# GetPathExt(Path): str
#   Get Path name extension.

def GetPathExt(path):
    return pop.splitext(path.pathStr)[1]

# ----------------------------------------------------------------------------
# GetPathMtime(path): int(UnixTime)
#   Get path modification time.

def GetPathMtime(path):
    return GetPathStat(path).poStat.st_mtime

# ----------------------------------------------------------------------------
# GetPathName(Path): str
#   Get Path base name string.

def GetPathName(path):
    return pop.basename(path.pathStr)

# ----------------------------------------------------------------------------
# GetPathSize(Path): int
#   Get Path size.

def GetPathSize(path):
    return GetPathStat(path).poStat.st_size

# ----------------------------------------------------------------------------
# GetPathStat(Path): PathStat
#   Get PathStat of a Path. Use cached PathStat, if present, else read.

def GetPathStat(path):
    if path.pathStat is None:
        path.pathStat = ReadPathStat(path)
    return path.pathStat

# ----------------------------------------------------------------------------
# GetPathStem(Path): str
#   Get the stem (the base name without extension) of the Path.

def GetPathStem(path):
    return pop.splitext(path.pathStr)[0]

# ----------------------------------------------------------------------------
# GetPathStr(Path): str
#   Get Path string.

def GetPathStr(path):
    return path.pathStr

# ----------------------------------------------------------------------------
# GetPathXfrm(Path): str
#   Get an xfrm of a Path.

def GetPathXfrm(path):
    return pop.normcase(pop.realpath(path.pathStr))

# ----------------------------------------------------------------------------
# ListDir(Path): [str]
#   List the Path directory.

def ListDir(path):
    return po.listdir(path.pathStr)

# ----------------------------------------------------------------------------
# MakePath(str): Path
#   Make a Path from a str.

def MakePath(pathStr):
    path = Path()
    path.pathStr = pathStr
    path.pathStat = None
    return path

# ----------------------------------------------------------------------------
# MakeSubpath(Path, *str): Path
#   Make a subpath.

def MakeSubpath(path, *nameStrs):
    return MakePath(pop.join(path.pathStr, *nameStrs))

# ----------------------------------------------------------------------------
# PathEq(Path, Path): bool
#   Test if two paths are equal.

def PathEq(aPath, bPath):
    return GetPathXfrm(aPath) == GetPathXfrm(bPath)

# ----------------------------------------------------------------------------
# PathExists(Path): bool
#   Test whether the path exists.

def PathExists(path):
    return (GetPathStat(path).poStat is not None)

# ----------------------------------------------------------------------------
# PathIsDir(Path): bool
#   Test whether the Path is a directory.

def PathIsDir(path):
    poStat = GetPathStat(path).poStat
    if poStat:
        result = pst.S_ISDIR(poStat.st_mode)
    else:
        result = False
    return result

# ----------------------------------------------------------------------------
# PathIsFile(Path): bool
#   Test whether the Path is a regular file

def PathIsFile(path):
    poStat = GetPathStat(path).poStat
    if poStat:
        result = pst.S_ISREG(poStat.st_mode)
    else:
        result = False
    return result

# ----------------------------------------------------------------------------
# ReadPathStat(Path): PathStat
#   Read PathStat from a Path.

def ReadPathStat(path):
    pathStat = PathStat()
    pathStat.path = path; path.pathStat = pathStat
    try:
        pathStat.poStat = po.stat(path.pathStr)
    except OSError as error:
        if error.errno == pe.ENOENT:
            pathStat.poStat = None
        else:
            raise
    return pathStat

# CODE =======================================================================

import errno       as pe  # pe.ENOENT
import os          as po  # getcwd, listdir, stat
import os.path     as pop # join, splitext
import stat        as pst # interpret po.stat
