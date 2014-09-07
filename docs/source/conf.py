# -*- coding: utf-8 -*-
#
# This document is free and open-source software, subject to the OSI-approved
# BSD license below.
#
# Copyright (c) 2014 Alexis Petrounias <www.petrounias.org>,
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
# list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# * Neither the name of the author nor the names of its contributors may be used
# to endorse or promote products derived from this software without specific
# prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""
Sphinx documentation configuration for Python Restorable Collections.
"""

__status__ = "Release"
__version__ = "1.0.0"
__maintainer__ = (u"Alexis Petrounias <www.petrounias.org>", )
__author__ = (u"Alexis Petrounias <www.petrounias.org>", )

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.coverage',
    'sphinx.ext.viewcode',
]

templates_path = ['_templates']

source_suffix = '.rst'

master_doc = 'index'

project = u'Python Restorable Collections'

copyright = u'2014, Alexis Petrounias'

version = '1.0'

release = '1.0.0'

exclude_patterns = []

pygments_style = 'sphinx'

html_theme = 'default'

html_static_path = ['_static']

htmlhelp_basename = 'PythonRestorableCollectionsdoc'

latex_elements = {}

latex_documents = [
  ('index', 'PythonRestorableCollections.tex',
   u'Python Restorable Collections Documentation', u'Alexis Petrounias',
   'manual', ), ]

man_pages = [
    ('index', 'pythonrestorablecollections',
     u'Python Restorable Collections Documentation',
     [u'Alexis Petrounias', ], 1, )
]

texinfo_documents = [
  ('index', 'PythonRestorableCollections',
   u'Python Restorable Collections Documentation', u'Alexis Petrounias',
   'PythonRestorableCollections',
   'Solution to unpickling collections with non-built-in type keys and cycles.',
   'Miscellaneous'),
]

