# coding: utf-8
#
# maxe.msg: messages.
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

import maxe.xml as mx

# ----------------------------------------------------------------------------
# GetExcAsXml(exc):
#   Get Python exception as XML.

def GetExcAsXml(exc):
    excElt = mx.MakeElt(mxQNameMxError)
    mx.SetAttr(excElt, mxQNameType, type(exc).__name__)
    mx.SetAttr(excElt, mxQNameMessage, str(exc))
    return excElt

# TODO (Later) Add code to intelligently store data for all Python exceptions.
# TODO (Later) Add code to attach exception traceback.
# TODO (Later) Add code to support Maxe exceptions.
# TODO (Later) See if I can somehow store a pointer to exception data instead
# of performing an expensive conversion.

# ----------------------------------------------------------------------------
# mxNs and QNames.

mxNs = mx.GetNs("")
mxQNameType = mx.GetQName(mxNs, "type")
mxQNameMessage= mx.GetQName(mxNs, "message")

mxNsMx = mx.GetNs("urn:onegasoft:Maxe")
mxQNameMxError = mx.GetQName(mxNsMx, "error")

