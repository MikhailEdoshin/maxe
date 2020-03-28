# coding: utf-8
#
# ============================================================================
# maxe.compat: Python 2/3 compatibility utilities

# This file is part of Maxe.

# Maxe is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.

# Maxe is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.

# You should have received a copy of the GNU General Public License
# along with Maxe.  If not, see <https://www.gnu.org/licenses/>.

import sys as ps
pyVer = ps.version_info.major

# ============================================================================
# Functions

# ----------------------------------------------------------------------------
# GetAsText(obj):
#   Get object as Unicode text.

if pyVer == 2:
    def GetAsText(obj):
        return unicode(obj)

elif pyVer == 3:
    def GetAsText(obj):
        return str(obj)

# ----------------------------------------------------------------------------
# GetStdinFhdl(): Fhdl
#   Get the stdin filelike object in binary mode.

if pyVer == 2:
    def GetStdinFhdl():
        return ps.stdin

elif pyVer == 3:
    def GetStdinFhdl():
        return ps.stdin.buffer

# ----------------------------------------------------------------------------
# GetDictVals(dict): [?]
#   Get dictionary values.

if pyVer == 2:
    def GetDictVals(d):
        return d.values()

elif pyVer == 3:
    def GetDictVals(d):
        return list(d.values())

# ----------------------------------------------------------------------------
# GetStdoutFhdl(): Fhdl
#   Get the stdout filelike object in binary mode.

if pyVer == 2:
    def GetStdoutFhdl():
        return ps.stdout

elif pyVer == 3:
    def GetStdoutFhdl():
        return ps.stdout.buffer

# ----------------------------------------------------------------------------
# MakeFhdlInMem(bytes):
#   Wrap data into a filelike object.

if pyVer == 2:
    import cStringIO as pc

    def MakeFhdlInMem(data):
        return pc.StringIO(data)

elif pyVer == 3:
    import io as pi

    def MakeFhdlInMem(data):
        return pi.BytesIO(data)
        
