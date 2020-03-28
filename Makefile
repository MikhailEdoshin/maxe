# Makefile: recipes to develop and test Maxe.
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

Env27 := venv27/bin
Env37 := venv37/bin

Fl27 := $(Env27)/pyflakes
Fl37 := $(Env37)/pyflakes

Py27 := $(Env27)/python
Py37 := $(Env37)/python

Mx27 := $(Py27) -m maxe
Mx37 := $(Py37) -m maxe

# ----------------------------------------------------------------------------
.PHONY: dist
# dist: create a Python distribution
dist:
	$(Py37) setup.py sdist

# ----------------------------------------------------------------------------
# clean: remove unnecessary files
.PHONY: clean
clean:
	rm -rf maxe/*.pyc maxe/ext/*.pyc maxe/ext/read/*.pyc \
	maxe/__pycache__ maxe/ext/__pycache__ maxe/ext/read/__pycache__

# ----------------------------------------------------------------------------
# test: test maxe command-line interface.
.PHONY: test

# test-xml
test-xml:
	$(Mx27) read test/self.xslt
# test-path
test-path:
	$(Mx27) read test/non-existing.path
# test-file
test-file:
	$(Mx27) read test/index.rst
# test-dir
test-dir:
	$(Mx27) read test


# ----------------------------------------------------------------------------
# test-flakes: test Python source code with pyflakes
# The code makes Make to ignore errors from pyflakes ('-' at the start of the
# line) because a) I want it to test all files nonetheless and b) some errors
# are not errors (e.g. pyflakes thinks I should use '# type' in some special
# way) but there's no way to tell pyflakes to ignore it.

.PHONY: test-flakes 
test-flakes: test-flakes-compat test-flakes-ext test-flakes-ext-path \
    test-flakes-ext-read test-flakes-ext-read-rst test-flakes-ext-read-xml \
    test-flakes-init test-flakes-main test-flakes-msg test-flakes-path \
    test-flakes-strm test-flakes-xml

.PHONY: test-flakes-compat
test-flakes-compat:
	-$(Fl27) maxe/compat.py
	-$(Fl37) maxe/compat.py

.PHONY: test-flakes-ext
test-flakes-ext:
	-$(Fl27) maxe/ext/__init__.py
	-$(Fl37) maxe/ext/__init__.py

.PHONY: test-flakes-ext-path
test-flakes-ext-path:
	-$(Fl27) maxe/ext/path.py
	-$(Fl37) maxe/ext/path.py

.PHONY: test-flakes-ext-read
test-flakes-ext-read:
	-$(Fl27) maxe/ext/read/__init__.py
	-$(Fl37) maxe/ext/read/__init__.py

.PHONY: test-flakes-ext-read-rst
test-flakes-ext-read-rst:
	-$(Fl27) maxe/ext/read/rst.py
	-$(Fl37) maxe/ext/read/rst.py

.PHONY: test-flakes-ext-read-xml
test-flakes-ext-read-xml:
	-$(Fl27) maxe/ext/read/xml.py
	-$(Fl37) maxe/ext/read/xml.py

.PHONY: test-flakes-init
test-flakes-init:
	-$(Fl27) maxe/__init__.py
	-$(Fl37) maxe/__init__.py

.PHONY: test-flakes-main
test-flakes-main:
	-$(Fl27) maxe/__main__.py
	-$(Fl37) maxe/__main__.py

.PHONY: test-flakes-msg
test-flakes-msg:
	-$(Fl27) maxe/msg.py
	-$(Fl37) maxe/msg.py

.PHONY: test-flakes-path
test-flakes-path:
	-$(Fl27) maxe/path.py
	-$(Fl37) maxe/path.py

.PHONY: test-flakes-strm
test-flakes-strm:
	-$(Fl27) maxe/strm.py
	-$(Fl37) maxe/strm.py

.PHONY: test-flakes-xml
test-flakes-xml:
	-$(Fl27) maxe/xml.py
	-$(Fl37) maxe/xml.py

# ----------------------------------------------------------------------------
# test: run a test. For now tests are controlled manually; I need a better rig
# for command-line tests to run them.

.PHONY: test
test: \
    test-rd-cmp-comb \
    test-rd-cmp-dir \
    test-rd-cmp-lmx \
    test-rd-cmp-mult \
    test-rd-cmp-rst \
    test-rd-cmp-unk \
    test-rd-cmp-xml \
    test-rd-imp \
    test-tr-cmp-xml \
    test-tr-dtd \
    test-tr-par \
    test-tr-self \
    test-xp-get-path-stat \
    test-xp-list-directory \
    test-xp-read-file \
    test-xp-read-text \
    test-xp-scan-directory

# ----------------------------------------------------------------------------
# test-rd-cmp-xml: when given an XML, read the XML.
.PHONY: test-rd-cmp-xml
test-rd-cmp-xml:
	$(Mx27) read test/test.xml
	$(Mx37) read test/test.xml

# ----------------------------------------------------------------------------
# test-rd-cmp-rst: when given an .rst, read as reStructuredText.
.PHONY: test-rd-cmp-rst
test-rd-cmp-rst:
	$(Mx27) read test/test.rst
	$(Mx37) read test/test.rst

# ----------------------------------------------------------------------------
# test-rd-cmp-lmx: when given an unknown file, try to read it as XML.
.PHONY: test-rd-cmp-lmx
test-rd-cmp-lmx:
	$(Mx27) read test/test.lmx
	$(Mx37) read test/test.lmx

# ----------------------------------------------------------------------------
# test-rd-cmp-unk: when given an unknown file that cannot be read as XML, get
# path stat.
.PHONY: test-rd-cmp-unk
test-rd-cmp-unk:
	$(Mx27) read test/test.unk
	$(Mx37) read test/test.unk

# ----------------------------------------------------------------------------
# test-rd-cmp-dir: when given a directory, read the whole tree.
.PHONY: test-rd-cmp-dir
test-rd-cmp-dir:
	$(Mx27) read test
	$(Mx37) read test

# ----------------------------------------------------------------------------
# test-rd-cmp-mult: when given multiple paths, switch to improved mode.
.PHONY: test-rd-cmp-mult
test-rd-cmp-mult:
	$(Mx27) read test/test.xml test/test.rst
	$(Mx37) read test/test.xml test/test.rst

# ----------------------------------------------------------------------------
# test-rd-cmp-comb: when given a single path and stdin, switch to improved
# mode.
.PHONY: test-rd-cmp-comb
test-rd-cmp-comb:
	$(Mx27) read test/test.rst < test/test.xml
	$(Mx37) read test/test.rst < test/test.xml

# ----------------------------------------------------------------------------
# test-rd-imp: when given a single path and explicit switch, use the improved
# mode.
.PHONY: test-rd-imp
test-rd-imp:
	$(Mx27) read test/test.rst --improved
	$(Mx37) read test/test.rst --improved

# ----------------------------------------------------------------------------
# test-tr-self: when given a single XSLT, apply it to itself.
.PHONY: test-tr-self
test-tr-self:
	$(Mx27) transform test/test.xslt
	$(Mx37) transform test/test.xslt

# ----------------------------------------------------------------------------
# test-tr-cmp-xml: when given arguments, apply to arguments.
.PHONY: test-tr-cmp-xml
test-tr-cmp-xml:
	$(Mx27) transform test/test.xslt test/test.xml
	$(Mx37) transform test/test.xslt test/test.xml

# ----------------------------------------------------------------------------
# test-tr-imp: in improved mode add self to arguments
.PHONY: test-tr-imp
test-tr-imp:
	$(Mx27) transform test/test.xslt test/test.xml --improved
	$(Mx37) transform test/test.xslt test/test.xml --improved

# TODO: test the same modes as with 'read'?

# ----------------------------------------------------------------------------
# test-tr-par: allow to pass parameters.
.PHONY: test-tr-par
test-tr-par:
	$(Mx27) transform test/test.xslt test/test.xml -p a 1
	$(Mx37) transform test/test.xslt test/test.xml -p a 1
	$(Mx27) transform test/test.xslt test/test.xml -p a "'b'"
	$(Mx37) transform test/test.xslt test/test.xml -p a "'b'"
	$(Mx27) transform test/test.xslt test/test.xml -p a 'name(/*)'
	$(Mx37) transform test/test.xslt test/test.xml -p a 'name(/*)'
	$(Mx27) transform test/test.xslt test/test.xml -P a "b"
	$(Mx37) transform test/test.xslt test/test.xml -P a "b"

# ----------------------------------------------------------------------------
# test-tr-dtd: apply XSLT to an XML with a DTD and test that the 'id()' 
# function works. Do this when DTD is reachable from the XML or when it's in a
# directory passed with '-r'.
.PHONY: test-tr-dtd
test-tr-dtd:
	$(Mx27) transform test/dtd/dtd.xslt test/dtd/dtd.xml
	$(Mx37) transform test/dtd/dtd.xslt test/dtd/dtd.xml
	$(Mx27) transform test/dtd/dtd.xslt test/dtd/ref/dtd.xml -r test/dtd
	$(Mx37) transform test/dtd/dtd.xslt test/dtd/ref/dtd.xml -r test/dtd

# ----------------------------------------------------------------------------
# test-xp-get-path-stat: test 'mext:get-path-stat'
.PHONY: test-xp-get-path-stat
test-xp-get-path-stat:
	$(Mx27) transform test/xp-get-path-stat/test.xslt
	$(Mx37) transform test/xp-get-path-stat/test.xslt

# ----------------------------------------------------------------------------
# test-xp-list-directory: test 'mext:list-directory'
.PHONY: test-xp-list-directory
test-xp-list-directory:
	$(Mx27) transform test/xp-list-directory/test.xslt
	$(Mx37) transform test/xp-list-directory/test.xslt

# ----------------------------------------------------------------------------
# test-xp-scan-directory: test 'mext:scan-directory'
.PHONY: test-xp-scan-directory
test-xp-scan-directory:
	$(Mx27) transform test/xp-scan-directory/test.xslt
	$(Mx37) transform test/xp-scan-directory/test.xslt

# ----------------------------------------------------------------------------
# test-xp-read-file: test 'mext:read-file'
.PHONY: test-xp-read-file
test-xp-read-file:
	$(Mx27) transform test/xp-read-file/test.xslt
	$(Mx37) transform test/xp-read-file/test.xslt

# ----------------------------------------------------------------------------
# test-xp-read-text: test 'mext:read-text'
.PHONY: test-xp-read-text
test-xp-read-text:
	$(Mx27) transform test/xp-read-text/test.xslt
	$(Mx37) transform test/xp-read-text/test.xslt


# rst2fo: sample reST-to-FO
.PHONY: rst2fo
rst2fo: out/rst2fo/sample.pdf

out/rst2fo/sample.xml: src/sample-reST-to-FO.rst
	maxe $(filter %.rst,$^) -i -t $@

out/rst2fo/sample.fo: out/rst2fo/sample.xml src/sample-reST-to-FO.xslt
	maxe $(filter %.xslt,$^) $(filter %.xml,$^) -t $@

out/rst2fo/sample.pdf: out/rst2fo/sample.fo
	fop -fo $(filter %.fo,$^) -pdf $@
	chmod a-x $@

# ----------------------------------------------------------------------------
# dtest: developer tests.

# Test IO encodings. 
out/io-encodings.txt: res/test-io-encodings.py
	if [ -f $@ ] ; then rm $@ ; fi
	touch out/stdin
	venv27/bin/python $< out/ basic
	PYTHONIOENCODING=UTF-16 \
	venv27/bin/python $< out/ basicEncOverride
	venv27/bin/python $< out/ redir \
	< out/stdin > out/stdout 2>out/stderr
	PYTHONIOENCODING=UTF-16 \
	venv27/bin/python $< out/ redirEncOverride \
	< out/stdin > out/stdout 2>out/stderr
	venv37/bin/python $< out/ basic
	PYTHONIOENCODING=UTF-16 \
	venv37/bin/python $< out/ basicEncOverride
	venv37/bin/python $< out/ redir \
	< out/stdin > out/stdout 2>out/stderr
	PYTHONIOENCODING=UTF-16 \
	venv37/bin/python $< out/ redirEncOverride \
	< out/stdin > out/stdout 2>out/stderr
	cat $@

# ----------------------------------------------------------------------------
# venv27: Python virtual environment.
.PHONY: venv27
venv27:
	python2.7 -m virtualenv venv27
	venv27/bin/pip install --requirement maxe.egg-info/requires.txt

# ----------------------------------------------------------------------------
# venv37: Python virtual environment.
.PHONY: venv37
venv37:
	python3.7 -m virtualenv venv37
	venv37/bin/pip install --requirement maxe.egg-info/requires.txt

