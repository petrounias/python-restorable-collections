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
Classes featuring various collections used by
:mod:`restorable_collections_tests` unit tests; these classes must be
module-level (including the default dictionary factory method) so that they can
be pickled.
"""

__status__ = "Stable"
__version__ = "1.0.0"
__maintainer__ = (u"Alexis Petrounias <www.petrounias.org>", )
__author__ = (u"Alexis Petrounias <www.petrounias.org>", )

# Python
from collections import OrderedDict, defaultdict

# Restorable Collections
from restorable_collections import RestorableDict, RestorableOrderedDict, \
    RestorableDefaultDict, RestorableSet


class Group(object):

    def __init__(self, name):
        super(Group, self).__init__()
        self.name = name
        self.elements = []

    def __repr__(self):
        return "Group({})".format(self.name)


class C(object):

    def __init__(self, v):
        super(C, self).__init__()
        self.v = v
        self.plain = dict()
        self.plain_ordered = OrderedDict()
        self.plain_default = defaultdict(c_factory)
        self.restorable_plain = RestorableDict()
        self.restorable_ordered = RestorableOrderedDict()
        self.restorable_default = RestorableDefaultDict(c_factory)

    def add(self, key, value):
        self.plain[key] = (key, value)
        self.plain_ordered[key] = (key, value)
        self.plain_default[key] = (key, value)
        self.restorable_plain[key] = (key, value)
        self.restorable_ordered[key] = (key, value)
        self.restorable_default[key] = (key, value)

    def __hash__(self):
        return hash(self.v) if hasattr(self, 'v') else id(self)

    def __repr__(self):
        return "C({})".format(self.v)

    def restoration_key(self, d, key, value, identifier = None):
        return key.v

    def restoration_map(self, d, identifier = None):
        return { v : c[0] for v, c in d.iteritems() }


def c_factory():
    return (C(0), '_')


class D(object):

    def __init__(self, v):
        super(D, self).__init__()
        self.v = v
        self.plain = set()
        self.restorable_plain = RestorableSet()

    def add(self, item):
        self.plain.add(item)
        self.restorable_plain.add(item)

    def __hash__(self):
        return hash(self.v) if hasattr(self, 'v') else id(self)

    def __repr__(self):
        return "D({})".format(self.v)

