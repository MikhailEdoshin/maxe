# coding: utf-8
#
# maxe.__main__: command-line interface.
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

# Maxe command-line tool can read files as XML and apply XSLT transforms:
 
# Read files:
 
#   maxe read [PATH...]
#     -i --improved
#     -o --output PATH
#     -r --resource-paths PATH...
 
# Apply an XSLT tranform:
 
#   maxe [transform] XSLT [PATH...]
#     -i --improved
#     -o --output PATH
#     -p --param NAME VALUE
#     -r --resource-paths PATH...
#     -s --strparam NAME VALUE

# The read action is auxiliary to transform; the following commands are
# equivalent:

#   maxe transform XSLT PATH
#   maxe read PATH | maxe transform XSLT
 
# By default Maxe outputs to stdout and will read stdin, if it's redirected.
 
# Maxe can run in two modes, the compatible mode and the improved mode. The
# improved mode is meant to support multiple input; in this mode Maxe creates
# a shallow XML that lists all inputs and passes it to XSLT. The XSLT can then
# use Maxe extension functions to process these arguments. The improved mode
# is how Maxe operates when it receives more than one input.
 
# When Maxe receives a single input and is not forced to use the improved mode
# with the '--improved' option, it switches to compatible mode. In this mode
# Maxe reads the whole input as XML and processes it. This is similar to how
# other XSLT processors work and allows to use existing XSLTs as a part of the
# process.

# Options:
 
#   -i --improved
#     Force to use the improved mode.

#   -p --param NAME VALUE, -s --strparam NAME VALUE
#      Set the XSLT parameter. '--strparam' ensures the parameter is passed as
#      a string. These options only apply to the 'transform' command.
 
#   -r --resource-paths PATH...
#     Use the specified paths to resolve relative URLs.

#   -o --output PATH
#     Output to this path. If omitted, Maxe will output to standard output. 
#     The path must not exist or be a file.

# ----------------------------------------------------------------------------
# Discarded ideas

# Idea: make the command-line interface more complex, e.g. add code to scan 
#   directories or not, resolve symlinks or not, read files or not and which 
#   ones, set format for a file extension, set format options for a format, 
#   keep the file or symlink wrapper, etc.

#   Discarded because this is all possible, but since Maxe provides a set of
#   XPath functions to read files and directories, it would be simpler and
#   more convenient to do all this with XSLT itself.

# IMPORTS ====================================================================

from __future__ import absolute_import, print_function

import argparse          as pa   # parses command-line arguments
import locale            as pl   # get preferred encoding
import pdb               as pd; pd = pd
import sys               as ps   # provides access to stdin and stdout

import maxe.path         as mp   # work with paths
import maxe.strm         as ms   # work with streams
import maxe.xml          as mx   # read and create XML, apply XSLT.
import maxe.ext.path     as mep  # read path as XML
import maxe.ext.read     as mer  # read files
import maxe.ext.read.rst as merr ; del merr # initialize
import maxe.ext.read.xml as merx # Ctx to mx.ReadParam

# ============================================================================
# DATA TYPES

# ----------------------------------------------------------------------------
# Ctx: command-line context.
#   curPath: current path, mp.Path.
#   paths: additional resource paths, [mp.Path]
#   Usage:
#       MakeCtx(pa.Namespace): Ctx

class Ctx(object):
    __slots__ = "curPath", "paths"

# ============================================================================
# PROCEDURES

# ----------------------------------------------------------------------------
# GetInputXml(mx.Ctx, pa.Namespace): le.Element
#   Get the input XML for 'transform' and 'read' commands. The parameter is
#   the result of parsing the command-line parameters and is an instance of
#   argparse.Namespace. Although it comes from different subparsers, the
#   parameters that are necessary to get inputs have the same names:
#   'improved' and 'inputPathStrs'.

def GetInputXml(ctx, args):
    # See if stdin is redirected and count input paths.
    if ps.stdin.isatty():
        stdinIsRedirected = False
    else:
        stdinIsRedirected = True
    inputPathCount = len(args.files)

    # See if we must use the improved mode.
    improved = args.improved
    if stdinIsRedirected and inputPathCount or inputPathCount > 1:
        # We have multiple inputs; force the improved mode.
        improved = True

    # If stdin is redirected, read it as XML. Errors are fatal.
    if stdinIsRedirected:
        # Try to parse stdin as XML. Errors are fatal: there seems to be no 
        # sensible way to handle non-XML input nor it appears to be of much 
        # use. Besides such robustness would also prolifearte runtime errors 
        # as invalid XML would simply be accepted as text.
        stdinXml = mx.ReadXml(ms.MakeIStrmFromStdin(), ctx)

    # Construct XML.
    if improved:
        # Improved mode: create 'maxe:arguments'.
        xml = mx.MakeElt(mxQNameMaxeArguments)
        if stdinIsRedirected:
            stdinArgXml = mx.MakeElt(mxQNameMaxeStdin)
            mx.Append(stdinArgXml, stdinXml)
            mx.Append(xml, stdinArgXml)
        if inputPathCount:
            i = 0
            while i < inputPathCount:
                inputPath = mp.MakePath(args.files[i]); i += 1
                mx.Append(xml, mep.GetPathAsXml(inputPath))
    elif stdinIsRedirected:
        # Compatible mode, single input, stdin.
        xml = stdinXml
    elif inputPathCount:
        # Compatible mode, single input, path.
        inputPath = mp.MakePath(args.files[0])
        if mp.PathIsFile(inputPath):
            # File; try to read as XML or fall back to giving file stats.
            try:
                xml = mer.ReadFileFromCli(inputPath, "", ctx)
            except Exception:
                # Fallback: try to parse as XML.
                # TODO: warn
                try:
                    xml = mer.ReadFileFromCli(inputPath, "xml", ctx)
                except:
                    # Fallback: get path stats.
                    # TODO: warn
                    xml = mep.GetPathStatAsXml(inputPath)
        elif mp.PathIsDir(inputPath):
            # For directories scan the whole directory tree.
            xml = mep.ScanDirAsXml(inputPath)
        else:
            # For non-existing paths or other path types read path stats.
            xml = mep.GetPathStatAsXml(inputPath)
    else:
        # Compatible mode, no input. Only happens with 'transform' ('read'
        # requires at least one input path), in which case 'transform' will
        # apply the XSLT to itself.
        xml = None
    return xml

# ----------------------------------------------------------------------------
# MakeCtx(pa.Namespace): Ctx
#   Make a command-line context.

def MakeCtx(args):
    ctx = Ctx()
    ctx.curPath = mp.GetCurPath()
    ctx.paths = []
    i = 0; n = len(args.resPathStrs)
    while i < n:
        ctx.paths.append(mp.MakePath(args.resPathStrs[i])); i += 1
    return ctx

# ----------------------------------------------------------------------------
# RunFromCli()
#   Run from command-line.

def RunFromCli():
    paParser = pa.ArgumentParser()
    # The default action if no subcommand is present is same as 'transform'.
    #   maxe XSLT PATH...
    #   -i --improved
    #   -o --output-path PATH
    #   -p --param NAME VALUE
    #   -r --resource-paths PATH...
    #   -P --strparam NAME VALUE
    # Note: cannot be done with 'argparse'.

    # There are two subcommands: transform and read.
    paCmds = paParser.add_subparsers()

    # Transform is same as the default action:
    #   maxe transform XSLT PATH...
    #   -i --improved
    #   -o --output-path PATH
    #   -p --param NAME VALUE
    #   -r --resource-paths PATH...
    #   -P --strparam NAME VALUE
    paCmdTr = paCmds.add_parser("transform")
    paCmdTr.set_defaults(func=RunFromCliTr)
    paCmdTr.add_argument("xslt", nargs=1)
    paCmdTr.add_argument("files", nargs="*", default=[])
    paCmdTr.add_argument("-i", "--improved", dest="improved",
           action="store_true", default=False)
    paCmdTr.add_argument("-o", "--output", dest="outputPathStr", nargs=1)
    paCmdTr.add_argument("-p", "--param", dest="params", nargs=2, default=[],
            action="append")
    paCmdTr.add_argument("-r", "--resources", dest="resPathStrs", nargs="*",
            default=[])
    paCmdTr.add_argument("-P", "--strparam", dest="strParams", nargs=2,
            default=[], action="append")

    # Read is similar to transform, but without XSLT
    #   maxe read PATH...
    #   -i --improved
    #   -o --output-path PATH
    #   -r --resource-paths PATH...
    paCmdRd = paCmds.add_parser("read")
    paCmdRd.set_defaults(func=RunFromCliRd)
    paCmdRd.add_argument("files", nargs="+")
    paCmdRd.add_argument("-i", "--improved", dest="improved",
           action="store_true", default=False)
    paCmdRd.add_argument("-o", "--output", dest="outputPathStr", nargs=1)
    paCmdRd.add_argument("-r", "--resources", dest="resPathStrs", nargs="*",
            default=[])

    args = paParser.parse_args()
    args.func(args)

# ----------------------------------------------------------------------------
# RunFromCliRd(pa.Namespace)
#   Run the 'read' command.

def RunFromCliRd(args):
    ctx = MakeCtx(args)
    inputXml = GetInputXml(ctx, args)
    SaveResXml(args, inputXml, mx.GetSCfgOfXml(inputXml))

# ----------------------------------------------------------------------------
# RunFromCliTr(pa.Namespace)
#   Run the 'transform' command.

def RunFromCliTr(args):
    # Read the XSLT XML and compile XSLT. Keep the XML in case we need it.
    ctx = MakeCtx(args)
    xsltPath = mp.MakePath(args.xslt[0])
    xsltStrm = ms.MakeIStrmFromPath(xsltPath)
    readParam = merx.ReadParamCli(ctx)
    xsltXml = mx.ReadXml(xsltStrm, readParam)
    xslt = mx.MakeXslt(xsltXml)
    # Add XSLT parameters.
    xsltParams = mx.MakeXsltParams()
    i = 0; n = len(args.params)
    while i < n:
        param = args.params[i]; i += 1; nStr = param[0]; vStr = param[1]
        mx.AddXsltParam(xsltParams, nStr, mx.XsltParamXPath, vStr)
    i = 0; n = len(args.strParams)
    while i < n:
        param = args.strParams[i]; i += 1; nStr = param[0]; 
        vStr = param[1]
        mx.AddXsltParam(xsltParams, nStr, mx.XsltParamStr, vStr)
    inputXml = GetInputXml(ctx, args)
    if inputXml is None:
        # No inputs; apply the XSLT to itself.
        inputXml = xsltXml
    elif mx.GetEltQName(inputXml) == mxQNameMaxeArguments:
        # Running in improved mode; add XSLT path as the first arg.
        mx.Insert(inputXml, mep.GetPathAsXml(xsltPath), 0)
    resXml = mx.ApplyXslt(xslt, xsltParams, inputXml)
    SaveResXml(args, resXml, mx.GetSCfgOfXslt(xslt))

# ----------------------------------------------------------------------------
# SaveResXml(pa.Namespace, mx.Xml, sCfg)
#   Send the XML result to output. The XML result can be an XML element
#   (lxml.etree._Element)  XML Document (lxml.etree._ElementTree) or 

def SaveResXml(args, resXml, sCfg):
    if args.outputPathStr:
        # Use the XML encoding. 
        enc = sCfg.enc
        strm = ms.MakeOStrmFromPath(mp.MakePath(args.outputPathStr[0]))
    else:
        # The output goes to stdout; use the stdout encoding.
        enc = ps.stdout.encoding
        strm = ms.MakeOStrmFromStdout()
    try:
        # Both stdout and XML encodings may be not set.
        if not enc:
            # Try to get the preferred locale encoding
            enc = pl.getpreferredencdoing()
        if not enc:
            # Fall back to UTF-8.
            enc = "utf-8"
        sCfg.enc = enc
        mx.WriteXml(strm, resXml, sCfg)
    finally:
        ms.DropStrm(strm)

# VARIABLES ==================================================================

# mxNs*, mxQName*: namespaces and QNames.

mxNsMaxe = mx.GetNs("urn:onegasoft:Maxe")
mxQNameMaxeArguments = mx.GetQName(mxNsMaxe, "arguments")
mxQNameMaxeStdin     = mx.GetQName(mxNsMaxe, "stdin"    )

# CODE =======================================================================

if __name__ == "__main__":
    RunFromCli()
