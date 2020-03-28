# coding: utf-8
#
# maxe.xml: XML.
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

# TODO: consider to use Ctx to make Elts so that I can supply 'nsmap'.

# ============================================================================
# Data types

# ----------------------------------------------------------------------------
# Ctx: XML processing context. Processing XML involves quite a bit of
# functionality. We may need to find external documents (DTDs, XSDs, XSLTs),
# to resolve a namespace prefix (XPath), to set security options. (We also
# need to supply XPath and XSLT extensions, although these are normally
# supplied in a global way.) XML processing context is an object that collects
# all these options. 
#
#   paths: paths to search in addition to default ones, [mp.Path].
#   nsPfxs: namespace prefixes, [nsPfx].
#   exts: XPath and XSLT extensions, [Ext].
#   parser: XML parser, le.XMLParser
#
# All context options are stored plainly as lists of custom structures. The 
# system creates the required lxml structures when necessary.
#
# Usage:
# + MakeCtx(): Ctx
#   AddNsPfx(Ctx, Ns, str)
#   AddPath(Ctx, mp.Path)
#   AddExts(Ctx, [Ext])
#   MakeXslt(Xml, Ctx): Xslt
#   ReadXml(Strm, Ctx): Xml
#   DefaultCtx

class Ctx(object):
    __slots__ = "paths", "nsPfxs", "exts", "parser"

# ----------------------------------------------------------------------------
# Ext: XPath or XSLT extension.
#   qName: function or element name, QName.
#  _type: extension type, Ext*.
#   func: function to call, Python function or callable, depends on type.
#
# Usage:
#   Ctx.exts: [Ext]
#   Exts: [Ext]
#
#   AddExts(Ctx, [Ext])
#   GetAllExts(): [Ext]
# + MakeExt(QName, ExtType, func): Ext

class Ext(object):
    __slots__ = "qName", "type", "func"

# ----------------------------------------------------------------------------
# ExtType: possible extension types, function (XPath) or element (XSLT).
# Usage:
#   Ext.type
#   MakeExt(QName, ExtType, func)
#   RegExts(str, str, ExtType, func, ...)

ExtFunc = 0 # Extension function (XPath)
ExtElt  = 1 # Extension element (XSLT)

# ----------------------------------------------------------------------------
# Ns: an XML namespace.
#   uri: namespace URI, str.
#   qNames: map from local name string to QNames, {str:QName}
# Usage:
#   QName.ns: Ns
#   NsPfx.ns: Ns
#   AddNsPfx(Ctx, Ns, str)
# + GetNs(str): Ns
#   GetQName(Ns, str): QName

class Ns(object):
    __slots__ = "uri", "qNames"

# ----------------------------------------------------------------------------
# NsPfx: XML namespace prefix.
#
#   ns: namespace, Ns.
#   pfx: prefix string, str.
#
# Usage:
#   Ctx.nsPfxs: [NsPfx]
#   (Internally) AddNsPfx(Ctx, Ns, str)

class NsPfx(object):
    __slots__ = "ns", "pfx"

# ----------------------------------------------------------------------------
# QName
#   ns: namespace, Ns.
#   localName: local name, str.
#   jcStr: cached JcStr, str.
# Usage:
#   Ext.qName
#   Ns.qNames: {str:QName}
#   GetAttr(Xml, QName): str
#   GetEltQName(Xml): QName
#   GetQName(Ns, str): QName
#   MakeElt(QName): Xml
#   MakeExt(QName, Ext*, func): Ext
#   SetAttr(Xml, QName, str)

class QName(object):
    __slots__ = "ns", "localName", "jcStr"

# ----------------------------------------------------------------------------
# ReadParam: parameters for reading XML.
#   paths: resource paths, [mp.Path]
#   Usage:
#       MakeReadParam(): ReadParam
#       ReadXml(Strm, ReadParam): Xml
#       ReadParamCli(maxe.__main__.Ctx): ReadParam
#       ReadParamXArg(XArg): ReadParam
#       ReadStrm(Strm, ReadParam): Xml
#       ReadText(Text, ReadParam): Xml

class ReadParam(object):
    __slots__ = "paths"

# ----------------------------------------------------------------------------
# SCfg: XML serialization configuration. Stores serialization parameters.
# Sources: read when parsing XML; compute when compiling XSLT; obtain when
# transforming XML; copy; create programmatically. Usage: pass to WriteXml to
# specify the options.

#   can: canonicalization format, SCfgCan*.
#   canCmt: whether to output comments, bool.
#   canExc: whether to use exclusive namespaces, bool.
#   canInc: namespaces to include (hoist to the root), [Ns].
#   canTxt: whether to output text, bool.
#   dcl: whether to emit XML declaration, bool.
#   dtdPub: public ID of the document type, string.
#   dtdStd: whether the document is standalone, bool.
#   dtdSys: system ID of the document type, string.
#   dtdTyp: document type in DTD schema, QName.
#   enc: encoding, string.
#   ind: indent XML, bool.
#   mdt: media type, string.
#   mtd: serialization method, string.
#   url: document URL.
#   ver: version, string.
#   TODO: cdata-section-elements
#
# Usage:
#   CopySCfg(SCfg): SCfg
#   GetSCfgOfXml(Xml): SCfg
#   MakeSCfg(): SCfg

class SCfg(object):
    __slots__ = "can", "canCmt", "canExc", "canInc", "canTxt", "dcl", "dtd", \
            "dtdPub", "dtdStd", "dtdStd", "dtdSys", "dtdTyp", "enc", "ind", \
            "mdt", "mtd", "url", "ver"

# ----------------------------------------------------------------------------
# XArg: argument that may be received by an XPath extension function.
#   = list, bool, float, lxml.etree._ElementStringResult
#
# Usage:
#   GetXArgType(XArg): XArgType
#   GetXArtAsStr(XArg): str

# ----------------------------------------------------------------------------
# XArgType: Type of arguments that may be received by an XPath extension 
# function. Note that in lxml it's not possible to receive the document root
# (XPath "/") even though it seems logical and is a totall valid XPath that
# should be returning the document for the XML.
#
# Usage:
#   GetXArgType(XArg): XArgType

XArgNSet = 0 # list; any nodeset, result of XPath.
XArgBool = 1 # bool
XArgNum  = 2 # float
XArgStr  = 3 # lxml.etree._ElementStringResult,
             # lxml.etree._ElementUnicodeResult

# XArgNSet can contain any XmlType (in lxml it's not possible for it to pass
# Xml(Doc) in any way).

# ----------------------------------------------------------------------------
# Xml: XML objects that may appear when reading, transforming, or accessing
# XML. _ElementTree is what gets read from files; _XSLTresultTree is the
# result of an XSLT transform; the rest are XML parts that can be e.g.
# selected by an XPath expression (see also XmlType and XArg).
#   = lxml.etree._Element, ._ElementTree, ._XSLTResultTree,
#   _ElementStringResult, _ProcessingInstruction, _Comment.
# Usage:
#   Append(Xml, Xml)
#   AppendElt(Xml, Xml)
#   AppendText(Xml, str)
# + ApplyXslt(Xslt, XsltParams, Xml): Xml
#   GetAttr(Xml, QName): str
#   GetEltQName(Xml, QName)
#   GetXmlEnc(Xml): str | None
#   GetXmlType(Xml): XmlType
#   Insert(Xml, Xml, Int)
# + MakeElt(QName): Xml
#   MakeXslt(Xml, Ctx): Xslt
# + ReadXml(Strm, Ctx): Xml
#   SetAttr(Xml, QName, str)
#   WriteXml(Strm, Xml)

# ----------------------------------------------------------------------------
# XmlType XML object type
# Usage:
#   GetXmlType(Xml): XmlType

XmlDoc  = 0 # lxml.etree._ElementTree, ._XSLTResultTree
XmlElt  = 1 # lxml.etree._Element
XmlAttr = 2 # lxml.etree._ElementStringResult[is_attribute]
XmlText = 3 # lxml.etree._ElementStringREsult[not(is_attribute)]
XmlPi   = 4 # lxml.etree._ProcessingInstruction
XmlCmnt = 5 # lxml.etree._Comment

# ----------------------------------------------------------------------------
# Xslt: XSLT transformation.
#   xml: the source XML, lxml.etree._ElementTree
#   xslt: the compiled XSLT, lxml.etree.XSLT
#
# Usage:
#   ApplyXslt(Xslt, XsltParams, Xml): Xml
#   GetBuiltinXslt(str): Xslt
#   GetSCfgOfXstl(Xslt): SCfg
#   MakeXslt(Xml, Ctx): Xslt
#   TODO: ApplyXsltTemplates(Xslt, QName, XsltParams, Xml): XRes
#   TODO: CallXsltTemplate(Xslt, QName, XsltParams, XSet): XRes

class Xslt(object):
    __slots__ = "xml", "xslt"

# ----------------------------------------------------------------------------
# XsltParamType XSLT parameter type. Normally XSLT parameters are interpreted
# as XPaths, so to supply a string one has to enclose it in additional quotes:
# "foo" is an XPath looking for the child elements called 'foo' and "'foo'" is
# a string 'foo'. In shell it may be hard to construct such strings
# programmatically, so many XSLT engines provide a way to explicitly label a
# parameter as a string; the engine will then do its own escaping. Maxe does
# this with the '--strparam' option and internally uses XsltParamType* to
# speicfy the parameter type.
#
# Usage:
#   AddXsltParam(XsltParams, str, XsltParamType str)

XsltParamXPath = 0
XsltParamStr   = 1

# ----------------------------------------------------------------------------
# XsltParams: a structure to collect XSLT parameters.
#
#   params: parameters, {str:str}.
#
# Usage:
# + MakeXsltParams(): XsltParams
#   AddXsltParam(XsltParams, str, XsltParamType str)
#   ApplyXslt(Xslt, XsltParams, Xml): Xml

class XsltParams(object):
    __slots__ = "params"

# ============================================================================
# Procedures

# ----------------------------------------------------------------------------
# AddNsPfx(Ctx, Ns, str)
#   Add a XML namespace prefix to a Ctx.

def AddNsPfx(ctx, ns, pfxStr):
    i = 0; n = len(ctx.nsPfxs)
    while i < n:
        nsPfx = ctx.nsPfsx[i]; i += 1
        if nsPfx.pfx == pfxStr:
            if nsPfx.ns == ns:
                break
            else:
                raise Exception("The Ctx already has prefix '%s' registered "
                    "to another namespace" % pfxStr)
    else:
        nsPfx = NsPfx(); nsPfx.ns = ns; nsPfx.pfx = pfxStr
        ctx.nsPfxs.append(nsPfx)

# ----------------------------------------------------------------------------
# AddPath(Ctx, mp.Path)
#   Add a resource path to a Ctx.

def AddPath(ctx, path):
    i = 0; n = len(ctx.paths)
    while i < n:
        existingPath = ctx.paths[i]; i += 1
        if mp.PathEq(existingPath, path):
            break
    else:
        ctx.paths.append(path)

# ----------------------------------------------------------------------------
# AddPathToReadParam(ReadParam, mp.Path)
#   Add a path to a ReadParam.

def AddPathToReadParam(readParam, path):
    i = 0; n = len(readParam.paths)
    while i < n:
        existingPath = readParam.paths[i]; i += 1
        if mp.PathEq(existingPath, path):
            break
    else:
        readParam.paths.append(path)

# ----------------------------------------------------------------------------
# AddExts(Ctx, [Ext])
#   Add extensions to a context.

def AddExts(ctx, exts):
    ctx.exts.extend(exts)

# ----------------------------------------------------------------------------
# AddXsltParam(XsltParams, str, XsltParamType, str)
#   Add an XSLT parameter.

def AddXsltParam(xsltParams, nameStr, xsltParamType, valStr):
    if nameStr in xsltParams.params:
        raise Exception("The XsltParams record already has parameter with "
                "name '%s'" % nameStr)
    if xsltParamType == XsltParamStr:
        val = le.XSLT.strparam(valStr)
    else: # XsltParamXPath
        val = valStr
    # Store parameters in the form they will be passed to lxml.
    xsltParams.params[nameStr] = val

# ----------------------------------------------------------------------------
# Append(Xml(Elt), Xml(Elt, Attr, Text, Pi, Cmnt))
#   Append an Xml as the last child.

def Append(xml, childXml):
    xmlType = GetXmlType(xml)
    if xmlType == XmlDoc:
        xml = xml.getroot(); xmlType = XmlElt
    if xmlType == XmlElt:
        childXmlType = GetXmlType(childXml)
        if childXmlType == XmlDoc:
            childXml = childXml.getroot(); childXmlType = XmlElt
        if childXmlType == XmlAttr:
            raise Exception("Cannot append Xml(Attr); use SetAttr")
        elif childXmlType == XmlText:
            AppendText(xml, childXml)
        else: # Elt, Pi, or Cmnt
            AppendElt(xml, childXml)
    else:
        # Technically it must be possible to append to Xml(Doc) too; an XML
        # document must have one root element, but may have additional
        # comments or processing instructions. But in lxml this is not
        # possible. There's a hack: I can insert any text between the
        # declaration and the first element and technically I can use this for
        # document type declaration, processing instructions, and comments. 
        # Right now I don't do that.
        raise Exception("Cannot append to Xml of type %d." % xmlType)

# ----------------------------------------------------------------------------
# AppendElt(Xml(Elt), Xml(Elt, Pi, Cmnt))
#   Append an Xml as the last child.
#   Convenience method for the most common case without checking.

def AppendElt(xml, childXml):
    xml.append(childXml)

# ----------------------------------------------------------------------------
# AppendText(Xml(Elt), Xml(Text) | str)
#   Append text as the last child.
#   Convenience method for a common case without checking.

def AppendText(xml, childXml):
    # lxml does not store text nodes as first-class children; instead it puts
    # the first text node in element 'text' attribute and intermediate text 
    # nodes in child element 'tail' attributes:
    #
    # xml     : <elt>A<c1 />B<c2 />C</elt>
    # logical : elt [ "A" c1 "B" c2 "C" ]
    # lxml    : elt .text "A" .children [ c1 .tail "B", c2 .tail "C" ]
    # TODO: research if this applies to comments or PIs.
    # Convert the childXml into a string. Works for str, Xml(Text); would also
    # work for Xml(Attr).
    childText = str(childXml)
    if not len(xml): 
        # The element has no child nodes; set element's 'text'
        xml.text = childText
    else:
        # The element has child nodes; set last child's 'tail'
        xml[-1].tail = childText

# ----------------------------------------------------------------------------
# ApplyXslt(Xslt, XsltParams, Xml): Xml
#   Apply an XSLT.

def ApplyXslt(xslt, xsltParams, xml):
    return xslt.xslt(xml, **xsltParams.params)

# ---------------------------------------------------------------------------
# CopySCfg(SCfg): SCfg
#   Copy an SCfg.

def CopySCfg(sSCfg):
    tSCfg = SCfg()
    tSCfg.can    = sSCfg.can
    tSCfg.canCmt = sSCfg.canCmt
    tSCfg.canExc = sSCfg.canExc
    tSCfg.canInc = sSCfg.canInc
    tSCfg.canTxt = sSCfg.canTxt
    tSCfg.dcl    = sSCfg.dcl
    tSCfg.dtd    = sSCfg.dtd
    tSCfg.dtdPub = sSCfg.dtdPub
    tSCfg.dtdStd = sSCfg.dtdStd
    tSCfg.dtdSys = sSCfg.dtdSys
    tSCfg.dtdTyp = sSCfg.dtdTyp
    tSCfg.enc    = sSCfg.enc
    tSCfg.ind    = sSCfg.ind
    tSCfg.mdt    = sSCfg.mdt
    tSCfg.mtd    = sSCfg.mtd
    tSCfg.url    = sSCfg.url
    tSCfg.ver    = sSCfg.ver
    return tSCfg

# ----------------------------------------------------------------------------
# GetAllExts(): [Ext]
#   Get all extensions (to add to Ctx).

def GetAllExts():
    return Exts.values()

# ----------------------------------------------------------------------------
# GetAttr(Xml(Elt), QName): str
#   Get an XML attribute.

def GetAttr(elt, qName):
    # lxml uses strings in James Clark notation to support namespaces.
    return elt.get(qName.jcStr)

# ----------------------------------------------------------------------------
# GetBuiltinXslt(str): Xslt
#   Get a built-in XSLT. E.g. GetBuiltinXslt('foo') -> maxe/xslt/foo.xslt

def GetBuiltinXslt(filename):
    strm = ms.MakeIStrmInMem(GetPkgRes("xslt/" + filename + ".xslt"))
    readParam = MakeReadParam()
    xml = ReadXml(strm, readParam); 
    ms.DropStrm(strm)
    return MakeXslt(xml)

# ----------------------------------------------------------------------------
# GetEltQName(Xml(Elt, Attr)): QName
#   Get the QName of an element or an attribute.

def GetEltQName(xml):
    xmlType = GetXmlType(xml)
    if xmlType == XmlDoc:
        xml = xml.getroot(); xmlType = XmlElt
    if xmlType == XmlElt:
        jcStr = xml.tag
    elif xmlType == XmlAttr:
        jcStr = xml.attrname
    else:
        raise Exception("Cannot get QName of Xml type %d." % xmlType)
    if jcStr.startswith("{"):
        nsUriStr, localNameStr = JcRegEx.match(jcStr).groups()
    else:
        nsUriStr = ""; localNameStr = jcStr
    return GetQName(GetNs(nsUriStr), localNameStr)

# ----------------------------------------------------------------------------
# GetNs(Str(Uri)): Ns
#   Get an Ns by the namespace URI.

def GetNs(uriStr):
    try:
        ns = UriStrToNs[uriStr]
    except KeyError:
        ns = Ns(); ns.uri = uriStr; ns.qNames = {}; UriStrToNs[uriStr] = ns
    return ns

# ----------------------------------------------------------------------------
# GetPkgRes(str): bytes
#   Get a package resource.

def GetPkgRes(pathStr):
    return pp.get_data("maxe", pathStr)

# ----------------------------------------------------------------------------
# GetQName(Ns, Str(XmlName)): QName
#   Get an QName by Ns and local name.

def GetQName(ns, localNameStr):
    try:
        qName = ns.qNames[localNameStr]
    except KeyError:
        qName = QName(); qName.ns = ns; qName.localName = localNameStr
        # lxml can only use QNames in James Clark notation. Since QNames
        # are global and permanent we cache the string here. In James Clark 
        # notation non-empty namespace URIs are prepended to local name in 
        # braces: '{namespaceUri}localName'. The empty URI is omitted.
        if ns.uri == "": 
            # URI is empty
            jcStr = localNameStr
        else: 
            # URI is not empty
            jcStr = "{" + ns.uri + "}" + localNameStr
        qName.jcStr = jcStr
        ns.qNames[localNameStr] = qName
    return qName

# ----------------------------------------------------------------------------
# GetSCfgOfXml(Xml(Doc)): SCfg
#   Get the SCfg of an Xml(Doc).

def GetSCfgOfXml(xml):
    xmlType = GetXmlType(xml)
    sCfg = SCfg()
    # canonicalization: no way to tell
    sCfg.can    = None # n/a
    sCfg.canCmt = None # n/a
    sCfg.canExc = None # n/a
    sCfg.canInc = None # n/a
    sCfg.canTxt = None # n/a
    # declaration: cannot tell with lxml
    sCfg.dcl    = True # general default
    # DTD: TODO: research the XML model.
    sCfg.dtd    = None
    sCfg.dtdPub = None
    sCfg.dtdStd = None
    sCfg.dtdSys = None
    sCfg.dtdTyp = None
    # encoding
    if xmlType == XmlDoc:
        sCfg.enc = xml.docinfo.encoding
    else:
        sCfg.enc = None
    # indentation or pretty-print: no way to tell
    sCfg.ind    = False # general default
    # media type: no way to tell from the XML itself
    sCfg.mdt    = None
    # method: always 'xml', cannot read anything else.
    sCfg.mtd    = "xml"
    # url
    if xmlType == XmlDoc:
        sCfg.url = xml.docinfo.URL
    else:
        sCfg.url = None
    # version
    if xmlType == XmlDoc:
        sCfg.ver = xml.docinfo.xml_version
    else:
        sCfg.ver = "1.0"
    return sCfg

# ----------------------------------------------------------------------------
# GetSCfgOfXslt(Xslt): SCfg
#   Get the output SCfg of an XSLT stylesheet.

def GetSCfgOfXslt(xslt):
    gatherXslOutput = GetBuiltinXslt("gather-xsl-output")
    xsltParams = MakeXsltParams()
    gatherResult = ApplyXslt(gatherXslOutput, xsltParams, xslt.xml)
    sCfg = MakeSCfg()
    for outputElt in gatherResult.getroot():
        # cdata-section-elements = qnames
        cdataSectionElements = GetAttr(outputElt, QNameCdataSectionElements)
        if cdataSectionElements:
            # TODO: get namespace prefixes, expand QNames, set sCfg
            pass
        # doctype-public = STRING
        doctypePublic = GetAttr(outputElt, QNameDoctypePublic)
        if doctypePublic and not sCfg.dtdPub:
            sCfg.dtdPub = doctypePublic
        # doctype-system = STRING
        doctypeSystem = GetAttr(outputElt, QNameDoctypeSystem)
        if doctypeSystem and not sCfg.dtdSys:
            sCfg.dtdSys = doctypeSystem
        # encoding = STRING
        encoding = GetAttr(outputElt, QNameEncoding)
        if encoding and not sCfg.enc:
            sCfg.enc = encoding
        # indent = "yes" | "no"
        indent = GetAttr(outputElt, QNameIndent)
        if indent and not sCfg.ind:
            if indent == "yes":
                ind = False
            elif indent == "no":
                ind = True
            else:
                raise Exception("Unknown value for 'indent")
            sCfg.ind = ind
        # media-type = STRING
        mediaType = GetAttr(outputElt, QNameMediaType)
        if mediaType and not sCfg.mdt:
            sCfg.mdt = mediaType
        # method = "xml" | "html" | "text" | QNAME-BUT-NOT-NCNAME
        method = GetAttr(outputElt, QNameMethod)
        if method and not sCfg.mtd:
            if method == "xml":
                mtd = "xml"
            elif method == "html":
                mtd = "html"
            elif method == "text":
                mtd = "text"
            else:
                raise Exception("Unknown method")
            sCfg.mtd = mtd
        # omit-xml-declaration = "yes" | "no"
        omitXmlDeclaration = GetAttr(outputElt, QNameOmitXmlDeclaration)
        if omitXmlDeclaration and not sCfg.dcl:
            if omitXmlDeclaration == "yes":
                dcl = False
            elif omitXmlDeclaration == "no":
                dcl = True
            else:
                raise Exception("Unknown value for 'omit-xml-declaration'")
            sCfg.dcl = dcl
        # standalone = "yes" | "no"
        standalone = GetAttr(outputElt, QNameStandalone)
        if standalone and not sCfg.dtdStd:
            if standalone == "yes":
                std = True
            elif standalone == "no":
                std = False
            else:
                raise Exception("Unknown value for 'standalone'")
            sCfg.dtdStd = std
        # version = NMTOKEN
        version = GetAttr(outputElt, QNameVersion)
        if version and not sCfg.ver:
            sCfg.ver = version
    return sCfg

# ----------------------------------------------------------------------------
# GetXArgAsPath(XArg): mp.Path
#   Get XArg as path.

def GetXArgAsPath(xArg):
    return mp.MakePath(GetXArgAsStr(xArg))

# ----------------------------------------------------------------------------
# GetXArgAsStr(arg): str
#   Get the XArg as a string.

def GetXArgAsStr(xArg):
    result = None; xArgType = GetXArgType(xArg)
    if xArgType == XArgNSet:
        if len(xArg) == 0:
            result = ""
        elif len(xArg) == 1:
            xArg = xArg[0]; xArgType = GetXmlType(xArg)
        else:
            raise Exception("Expected a string, an attribute, or a single "
                    "element")
    if result is None:
        if xArgType == XmlText or xArgType == XmlAttr:
            result = str(xArg)
        elif xArgType == XmlElt:
            result = le.tostring(xArg, method="text")
        else:
            raise Exception("Cannot convert XmlType %d to string." % xArgType)
    return result

# ----------------------------------------------------------------------------
# GetXArgType(XArg): XArgType
#   Get the type of an argument passed to an XPath function.

def GetXArgType(arg):
    if isinstance(arg, list):
        result = XArgNSet
    elif isinstance(arg, bool):
        result = XArgBool
    elif isinstance(arg, float):
        result = XArgNum
    elif isinstance(arg, (le._ElementStringResult, le._ElementUnicodeResult)):
        result = XArgStr
    return result

# ----------------------------------------------------------------------------
# GetXmlEnc(Xml): str or None
#   Get encoding that is inherent to this XML.

def GetXmlEnc(xml):
    xmlType = GetXmlType(xml)
    if xmlType == XmlDoc:
        # Documents have encoding.
        enc = xml.docinfo.encoding
    else:
        # Other Xml objects do not have encodung.
        enc = None
    return enc

# ----------------------------------------------------------------------------
# GetXmlType(Xml): XmlType
#   Get the type of an XML object.

def GetXmlType(xml):
    if isinstance(xml, le._ElementTree):
        result = XmlDoc
    elif isinstance(xml, le._Element):
        result = XmlElt
    elif isinstance(xml, (le._ElementStringResult, le._ElementUnicodeResult)):
        if xml.is_attribute:
            result = XmlAttr
        else:
            result = XmlText
    elif isinstance(xml, le._ProcessingInstruction):
        result = XmlPi
    elif isinstance(xml, le._Comment):
        result = XmlCmnt
    else:
        raise Exception("Unexpected XML object type %s" % type(xml).__name__)
    return result

# ----------------------------------------------------------------------------
# Insert(Xml(Elt), Xml(Elt, Pi, Cmnt), int)
#    Insert child XML node.

def Insert(xml, childXml, index):
    xmlType = GetXmlType(xml)
    if xmlType == XmlDoc:
        xml = xml.getroot(); xmlType = XmlElt
    if xmlType != XmlElt:
        raise Exception("Cannot insert into Xml of type %d" % xmlType)
    childXmlType = GetXmlType(childXml)
    if childXmlType == XmlDoc:
        childXml = childXml.getroot(); childXmlType = XmlElt
    if childXmlType != XmlElt and childXmlType != XmlPi \
            and childXmlType != XmlCmnt:
        raise Exception("Cannot insert Xml of type %d" % childXmlType)
    xml.insert(index, childXml)

# ----------------------------------------------------------------------------
# MakeCtx(): Ctx
#   Create a Ctx.

def MakeCtx():
    ctx = Ctx()
    ctx.paths = []
    ctx.nsPfxs = []
    ctx.exts = []
    ctx.parser = le.XMLParser(dtd_validation=True)
    ctx.parser.resolvers.add(Resolver(ctx))
    return ctx

# ----------------------------------------------------------------------------
# MakeElt(QName): le.Element
#   Create an le.Element

def MakeElt(qName):
    # lxml can only use name in James Clark notation.
    return le.Element(qName.jcStr)

# ----------------------------------------------------------------------------
# MakeExt(QName, Ext*, func): Ext
#   Make an Ext.

def MakeExt(qName, extType, func):
    ext = Ext()
    ext.qName = qName
    ext.type = extType
    if extType == ExtElt:
        # In lxml an XSLT extension must be an instance of a subclass of
        # lxml.etree.XSLTExtension class that implements the 'execute()'
        # method. Since it doesn't seem that the subclass can use anything
        # else, like '__init__()' or that this may be of any use, in Maxe we
        # just register a function and create a temporary class and instance
        # on the fly.
        xsltExtSubclass = type("Ext", (le.XSLTExtension,), execute=func)
        func = xsltExtSubclass()
    ext.func = func
    return ext

# ----------------------------------------------------------------------------
# MakeReadParam(): ReadParam
#   Make a ReadParam.

def MakeReadParam():
    readParam = ReadParam()
    readParam.paths = []
    return readParam

# ----------------------------------------------------------------------------
# MakeSCfg(): SCfg
#   Make an empty SCfg.

def MakeSCfg():
    sCfg = SCfg()
    sCfg.can    = None
    sCfg.canCmt = None
    sCfg.canExc = None
    sCfg.canInc = None
    sCfg.canTxt = None
    sCfg.dcl    = True
    sCfg.dtd    = None
    sCfg.dtdPub = None
    sCfg.dtdStd = None
    sCfg.dtdSys = None
    sCfg.dtdTyp = None
    sCfg.enc    = "utf-8"
    sCfg.ind    = False
    sCfg.mdt    = "application/xml"
    sCfg.mtd    = "xml"
    sCfg.url    = None
    sCfg.ver    = "1.0"
    return sCfg

# ----------------------------------------------------------------------------
# MakeXslt(Xml): Xslt
#   Make an XSLT.

def MakeXslt(xml):
    xslt = Xslt(); xslt.xml = xml; 
    exts = mc.GetDictVals(Exts); xsltExts = {}; i = 0; n = len(exts)
    while i < n:
        ext = exts[i]; i += 1
        xsltExts[(ext.qName.ns.uri, ext.qName.localName)] = ext.func
    xslt.xslt = le.XSLT(xml, extensions=xsltExts)
    return xslt

# ----------------------------------------------------------------------------
# MakeXsltParams(): XsltParams
#   Make an XsltParams object.

def MakeXsltParams():
    xsltParams = XsltParams()
    xsltParams.params = {}
    return xsltParams
# ----------------------------------------------------------------------------
# ReadXml(Strm, ReadParam): Xml
#   Read XML.

def ReadXml(strm, readParam):
    xml = le.parse(strm.fhdl)
    # Test if XML references a DTD and if yes, validate it to make the 'id()'
    # function in XSLT work. The 'dtd_validation' parameter for 'parse()' is
    # not a good fit, because it errs if the document has no DTD to begin
    # with, but how do we know this in a general case? We have to parse it
    # first. (Maybe another workaround would be to parse the document twice,
    # first to see if it has a DTD and if yes, second time with validation.)

    # For now handle only one case: an XML references a DTD using a single
    # <!DOCTYPE> that references a SYSTEM entity. When this happens, lxml will
    # fill in '.doctype.internalDTD' with a shallow DTD wrapper that has
    # 'system_url'. It won't load that DTD though and if we try to validate
    # with 'internalDTD' itself, it will fail. We have to resolve the URL,
    # load the DTD, and call its '.validate' method.

    # TODO: test how a partial DTD works, try to find out when 'externalDTD'
    # gets set, test what happens if a DTD includes other DTDs. 
    # TODO: think how to use catalogs.
    if xml.docinfo.internalDTD:
        dtdPathStrs = xml.docinfo.internalDTD.system_url.split("/")
        # Search for the DTD.
        i = 0; n = len(readParam.paths); dtd = None
        while i < n:
            path = readParam.paths[i]; i += 1
            dtdSubpath = mp.MakeSubpath(path, *dtdPathStrs)
            if mp.PathExists(dtdSubpath) and mp.PathIsFile(dtdSubpath):
                dtd = le.DTD(mp.GetPathStr(dtdSubpath))
                break
        else:
            # Try to find the DTD relatively to the XML.
            # TODO: check if this works; using a stream may not have the URL.
            xmlPath = mp.MakePath(xml.docinfo.URL)
            xmlDir = mp.GetParentPath(xmlPath)
            dtdSubpath = mp.MakeSubpath(xmlDir, *dtdPathStrs)
            if mp.PathExists(dtdSubpath) and mp.PathIsFile(dtdSubpath):
                dtd = le.DTD(mp.GetPathStr(dtdSubpath))
        if dtd is not None:
            dtd.validate(xml)
        # TODO: warn or err if the DTD is not found.
    return xml

# ----------------------------------------------------------------------------
# RegExts(str, str, ExtType, func, str, ExtType, func...)
#   Register XPath and XSLT extensions. The function takes the namespace URI
#   string and then triplets that describe extensions: local name, type
#   (XPath function or XSLT element), and function itself.

def RegExts(uriStr, *args):
    ns = GetNs(uriStr); i = 0; n = len(args)
    if n % 3 != 0:
        raise Exception("Wrong number of arguments for RegExt: %d" % n)
    while i < n:
        localNameStr = args[i]; extType = args[i+1]; func = args[i+2]; i += 3
        qName = GetQName(ns, localNameStr)
        if qName in Exts:
            raise Exception("Cannot register extension %s namespace %s "
                    "because this QName has been already registered." %
                    (localNameStr, uriStr))
        Exts[qName] = MakeExt(qName, extType, func)

# ----------------------------------------------------------------------------
# SetAttr(xml, QName, str)
#   Set XML element attribute.

def SetAttr(xml, qName, strVal):
    xml.set(qName.jcStr, strVal)

# ---------------------------------------------------------------------------
# WriteXml(Strm, Xml, SCfg)
#   Write XML to stream according to serialization settings.

#   The function serializes a single element. All serialization must be
#   defined by SCfg. The SCfg must be created programmatically, read from XML,
#   or gathered from XSLT.

# Relevant knowledge: lxml serialization summary:

# lxml.etree.tostring()
#   Can serialize _Element and _ElementTree. Inefficient, because produces the
#   whole serialization in memory. Can override some of serialization options
#   (e.g. encoding), but for others, like document type, the documentation
#   says that it will be used together with the existing document type in
#   .docinfo (haven't tested this to understand what it means). The only way
#   to serialize an _Element; for _ElementTree '.write' would be better if
#   we're writing to a file.

# lxml.etree._ElementTree.write()
#   Can serialize _ElementTree and, since _XSLTResultTree is a subclass of
#   _ElementTree, _XSLTResultTree as well, but incorrectly, because it's not
#   aware of all <xsl:output> serialization settings, specifically of
#   'method' and thus always serializes as if the method was 'xml'. Otherwise
#   is similar to the 'tostring' function.

# lxml.etree._XSLTResultTree.write()
#   Works incorrectly, should not be used. Could be used if there were a way
#   to extract <xsl:output> 'method' attribute, but lxml provides no direct
#   way to do this even though it's undoubtely there somewhere.

# lxml.etree._XSLTResultTree.write_output()
#   Works unreliably, should not be used. Works only if the XSLT specifies the
#   encoding with <xsl:output>; if not, then the result of the transform won't
#   have any encoding and the method will fail complaining about an unknown 
#   encoding. Does not accept an encoding parameter either.

# str/bytes(lxml.etree._XSLTResultTree)
#   Works regardless of whether XSLT specifies the encoding and is aware of
#   all <xsl:output> settings.

def WriteXml(strm, xml, sCfg):
    leEnc = sCfg.enc
    leMtd = sCfg.mtd
    if leMtd == "xml":
        leDcl = sCfg.dcl
        # TODO: DTD options: doctype, public ID, system URL, standalone.
        # In lxml we have to pass 'doctype' that must be a string that will be
        # written as is before the root element. I.e. we have to build the
        # DOCTYPE on our own. 
    # Get the serialized element.
    xmlType = GetXmlType(xml)
    if xmlType == XmlDoc:
        elt = xml.getroot()
    elif xmlType == XmlElt:
        elt = xml
    else:
        raise Exception("Cannot write Xml of type %d to stream." % xmlType)
    # Transplant the root element into a new 'element tree' to strip the Xml
    # from the linked serialization information, and write with new options.
    tElt = le.Element("tmp"); tDoc = tElt.getroottree(); tDoc._setroot(elt)
    tDoc.write(strm.fhdl, encoding=leEnc, method=leMtd, xml_declaration=leDcl)

# CODE =======================================================================

import re          as pr # to parse QNames in James Clark notation.
import pkgutil     as pp # load package resources

import lxml.etree  as le # core backend

import maxe.compat as mc # GetDictVals
import maxe.path   as mp # paths
import maxe.strm   as ms # streams

# ----------------------------------------------------------------------------
# Resolver
#   Adapter to resolve URIs for lxml.etree.XMLParser.

class Resolver(le.Resolver):
    def __init__(self, ctx):
        self.ctx = ctx
    def resolve(self, uriStr, idStr, leCtx):
        i = 0; n = len(self.ctx.paths); foundPath = None
        while i < n:
            subpath = mp.MakeSubpath(self.ctx.paths[i], uriStr.split("/"))
            if mp.PathExists(subpath):
                foundPath = subpath
                break
            i += 1
        if foundPath:
            leResult = self.resolve_filename(mp.GetPathStr(foundPath))
        else:
            leResult = None # causes lxml to try the next resolver
        return leResult

# ----------------------------------------------------------------------------
# DefaultCtx: the default Ctx.
# TODO: consider to remove.

DefaultCtx = MakeCtx()

# ----------------------------------------------------------------------------
# Exts: Registered XPath and XSLT extensions, {QName:Ext}.
Exts = {}

# ----------------------------------------------------------------------------
# JcRegEx: a regular expression to read strings in James Clark notation.

JcRegEx = pr.compile("^\{([^\}]*)\}(.+)")

# ----------------------------------------------------------------------------
# UriStrToNs: Mapping of URI string to Ns, {str:Ns}. See 'GetNs'.

UriStrToNs = {}

# ----------------------------------------------------------------------------
# Nses and QNames

EmptyNs = GetNs("")
QNameCdataSectionElements = GetQName(EmptyNs, "cdata-section-elements")
QNameDoctypePublic        = GetQName(EmptyNs, "doctype-public"        )
QNameDoctypeSystem        = GetQName(EmptyNs, "doctype-system"        )
QNameEncoding             = GetQName(EmptyNs, "encoding"              )
QNameIndent               = GetQName(EmptyNs, "indent"                )
QNameMediaType            = GetQName(EmptyNs, "media-type"            )
QNameMethod               = GetQName(EmptyNs, "method"                )
QNameOmitXmlDeclaration   = GetQName(EmptyNs, "omit-xml-declaration"  )
QNameStandalone           = GetQName(EmptyNs, "standalone"            )
QNameVersion              = GetQName(EmptyNs, "version"               )

