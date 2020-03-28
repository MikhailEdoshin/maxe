Maxe
====

Maxe is an extensible XSLT processor. Maxe plans to let XSLT process more
input formats and perform more actions during the transform, e.g. create
directories, delete files, send HTTP requests, and so on.

Maxe is written in Python and is based on ``libxml2`` and ``libxslt`` as
they're wrapped for Python with ``lxml``.

For now Maxe and apply XSLT transforms, get path information (stats and
listing a directory), and parse reStructuredText files and text snippets.

Planned development
===================

Write code to manipulate files from XSLT: create directories, create or update
files, delete files and directories.

Add code for the generic ``object`` extension in reST. See if there's a code
for the generic code snippet with language hightlights or port my own version.
Consider to add the literate programming extensions I have.

Write code to send HTTP requests from XSLT and work with response. Register
file readers by MIME type plus add a structure to access HTTP message in XSLT.
