Python Restorable Collections
=============================

Pickleable wrappers for Python collections with non-built-in type keys and
cycles or self-references.

Interfaces to collections which solve the problem of unpickleable objects when
non-built-in type keys are used and form cycles, either mutually or through
self-reference.

A detailed article explaining the problem and this solution will soon be
available at: http://www.petrounias.org/articles/

Version 1.0.0

Documentation: https://python-restorable-collections.readthedocs.org/en/latest/


Prerequisites
=============

Core:

- Python >= 2.7


Obtaining
=========

- Author's website for the project:
  http://www.petrounias.org/software/python-restorable-collections/

- Git repository on GitHub:
  https://github.com/petrounias/python-restorable-collections/

- Mercurial repository on BitBucket:
  http://www.bitbucket.org/petrounias/python-restorable-collections/


Installation
============

Via setup tools:

    python setup.py install

Via pip and pypi:

    pip install python-restorable-collections


Usage
=====

Import the collections wrappers from the `restorable_collections` module.

    from restorable_collections import RestorableDict

and use it instead of the corresponding Python object:

    self.foo = RestorableDict()
    self.foo[self] = 42


Release Notes
=============

- v1.0.0 @ 7 Sep 2014 Initial public release.


Development Status
==================

Actively developed and maintained since 2014. Currently used in production in
proprietary projects by the author and his team, as well as other third parties.


Future Work
===========

- Support for non-standard collections, specifically OrderedSet and
  OrderedDefaultDict.


Contributors
============

Written and maintained by Alexis Petrounias < http://www.petrounias.org/ >.


License
=======

Released under the OSI-approved BSD license.

Copyright (c) 2014 Alexis Petrounias < www.petrounias.org >,
all rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

Redistributions of source code must retain the above copyright notice, this list
of conditions and the following disclaimer.

Redistributions in binary form must reproduce the above copyright notice, this
list of conditions and the following disclaimer in the documentation and/or
other materials provided with the distribution.

Neither the name of the author nor the names of its contributors may be used to
endorse or promote products derived from this software without specific prior
written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

