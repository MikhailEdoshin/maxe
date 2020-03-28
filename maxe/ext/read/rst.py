# coding: utf-8
#
# maxe.ext.read.rst: code to read reStructuredText.
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

import pdb                  as pd; pd = pd

import docutils.frontend    as df
import docutils.parsers.rst as dpr
import docutils.utils       as du

import maxe.compat          as mc
import maxe.ext.read        as mer
import maxe.strm            as ms
import maxe.xml             as mx

# ---------------------------------------------------------------------------
# GetDprParser(): dpr.Parser
#   Get a docutils.parsers.rst.Parser instance. This is relatively slow call,
#   so I don't create it by default on importing the module, but create and 
#   cache on the first call.

def GetDprParser():
    global DprParser
    if DprParser is None:
        DprParser = dpr.Parser()
    return DprParser

# ----------------------------------------------------------------------------
# GetRstXml(rst): mx.Xml
#   Transform a docutils object  representing reStructuredText elements
#   ('rst') directly into XML in Onegasoft reST namespace or extension 
#   namespace.
#
#   An 'rst' is like that:
#
#      { tagname: str, attlist(): [(str, str)], children: [rst] }
#
#   If tagname is '#text' it's a text node, else it's an element.
#
#   TODO: consider to also add the '.line' attribute.

def GetRstXml(rst):
    # Use '.tagname' to create the element.
    elt = mx.MakeElt(mx.GetQName(NsRst, rst.tagname))

    # Use '.attlist()' to add attributes.
    attrs = rst.attlist(); i = 0; n = len(attrs)
    while i < n:
        attr = attrs[i]; i += 1; nameStr = attr[0]; val = attr[1]
        # An extension may add attributes in XML namespace (e.g. xml:lang).
        if nameStr.startswith("xml:"):
            # XML attribute.
            attrNs = NsXml; localName = nameStr[4:];
        else:
            # This is an ordinary attribute.
            attrNs = Ns; localName = nameStr
        # In reStructuredText attributes may be strings or lists of strings.
        if isinstance(val, list):
            val = "\n".join(val)
        elif isinstance(val, int):
            val = str(val)
        mx.SetAttr(elt, mx.GetQName(attrNs, localName), val)

    # Process '.children'.
    children = rst.children; i = 0; n = len(children); lastChildElt = None
    while i < n:
        child = children[i]; i += 1
        if child.tagname == '#text':
            mx.AppendText(elt, mc.GetAsText(child))
        else:
            lastChildElt = GetRstXml(child)
            mx.AppendElt(elt, lastChildElt)
    return elt

# ----------------------------------------------------------------------------
# ReadText(Text, _)
#   Read reST text.

def ReadText(text, _):
    # Get a parser.
    dprParser = GetDprParser()
    # Get default document settings using magic from help(du.new_document).
    dfCfg = df.OptionParser(components=(dpr.Parser,)).get_default_values()
    # Create a new document.
    duDoc = du.new_document(None, dfCfg)
    # Parse.
    dprParser.parse(text, duDoc)
    # Convert to XML (duDoc is an rst object too).
    return GetRstXml(duDoc)

# Default dfCfg settings for docutils 0.16

# title                         :  None
# generator                     :  None
# datestamp                     :  None
# source_link                   :  None
# source_url                    :  None
# toc_backlinks                 : 'entry'
# footnote_backlinks            :  1
# sectnum_xform                 :  1
# strip_comments                :  None
# strip_classes                 :  None
# strip_elements_with_classes   :  None
# report_level                  :  2
# halt_level                    :  4
# exit_status_level             :  5
# debug                         :  None
# warning_stream                :  None
# traceback                     :  None
# input_encoding                :  None
# input_encoding_error_handler  : 'strict'
# output_encoding               : 'utf-8'
# output_encoding_error_handler : 'strict'
# error_encoding                : 'utf-8'
# error_encoding_error_handler  : 'backslashreplace'
# language_code                 : 'en'
# record_dependencies           :  DependencyList(None, [])
# config                        :  None
# id_prefix                     : ''
# auto_id_prefix                : 'id'
# dump_settings                 :  None
# dump_internals                :  None
# dump_transforms               :  None
# dump_pseudo_xml               :  None
# expose_internals              :  None
# strict_visitor                :  None
# _disable_config               :  None
# _source                       :  None
# _destination                  :  None
# _config_files                 :  []
# pep_references                :  None
# pep_base_url                  : 'http://www.python.org/dev/peps/'
# pep_file_url_template         : 'pep-%04d'
# rfc_references                :  None
# rfc_base_url                  : 'http://tools.ietf.org/html/'
# tab_width                     :  8
# trim_footnote_reference_space :  None
# file_insertion_enabled        :  1
# raw_enabled                   :  1
# syntax_highlight              : 'long'
# smart_quotes                  :  False
# smartquotes_locales           :  None
# character_level_inline_markup :  False
    
# ----------------------------------------------------------------------------
# ReadStrm(Strm, _)
#   Read reST data.

def ReadStrm(strm, _):
    return ReadText(ms.ReadText(strm, "utf-8"), _)

# ============================================================================
# CODE

# ----------------------------------------------------------------------------
# DprParser: docutils.parsers.rst.Parser instance. Initialization takes some
# time, so it's initialized on the first call; see 'GetDprRarser'.

DprParser = None

# ----------------------------------------------------------------------------
# mx.Ns, mx.QName instances

Ns    = mx.GetNs("")
NsRst = mx.GetNs("urn:onegasoft:reST")
NsXml = mx.GetNs("http://www.w3.org/XML/1998/namespace")

# ----------------------------------------------------------------------------
# Reader

Reader = mer.MakeReader("reStructuredText", ReadStrm, ReadText, None, None)
mer.AddFileExt(Reader, ".rst")
mer.AddMimeType(Reader, "text/x-rst")
