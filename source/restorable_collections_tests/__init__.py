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
Unit tests for :mod:`restorable_collections`.
"""

__status__ = "Stable"
__version__ = "1.0.0"
__maintainer__ = (u"Alexis Petrounias <www.petrounias.org>", )
__author__ = (u"Alexis Petrounias <www.petrounias.org>", )

# Python
import pickle, cPickle
from unittest import TestCase

# Python Restorable Collections
from helpers import Group, C, D


class RestorableCollectionsTestCase(TestCase):
    """
    Tests :mod:`restorable_collections` by creating pickled structures featuring
    no cycles, self cycles, and mutual cycles, for all supported dictionary and
    set wrappers. Python bult-in dictionaries and sets are also tested with
    expectation of failure via raising exceptions.
    """

    def setUp(self):
        self.pickle = pickle


    def test_dict_no_cycle(self):

        g = Group("group")
        c1 = C(42)
        g.elements.append(c1)
        c2 = C(67)
        g.elements.append(c2)

        c1.add(c2, 'a') # points to c2, which does not point to anything

        self.assertTrue(c2 in c1.plain)
        self.assertTrue(c2 in c1.plain_ordered)
        self.assertTrue(c2 in c1.plain_default)
        self.assertTrue(c2 in c1.restorable_plain)
        self.assertTrue(c2 in c1.restorable_ordered)
        self.assertTrue(c2 in c1.restorable_default)

        gp = pickle.dumps(g)
        gu = pickle.loads(gp)

        c1u = gu.elements[0]
        c2u = gu.elements[1]

        # check existence of keys directly

        self.assertTrue(c2u in c1u.plain.keys())
        self.assertTrue(c2u in c1u.plain_ordered.keys())
        self.assertTrue(c2u in c1u.plain_default.keys())
        self.assertTrue(c2u in c1u.restorable_plain.keys())
        self.assertTrue(c2u in c1u.restorable_ordered.keys())
        self.assertTrue(c2u in c1u.restorable_default.keys())

        # check direct key-based lookup

        self.assertEqual(c2u, c1u.plain[c2u][0])
        self.assertEqual(c2u, c1u.plain_ordered[c2u][0])
        self.assertEqual(c2u, c1u.plain_default[c2u][0])
        self.assertEqual(c2u, c1u.restorable_plain[c2u][0])
        self.assertEqual(c2u, c1u.restorable_ordered[c2u][0])
        self.assertEqual(c2u, c1u.restorable_default[c2u][0])

        # check key lookup with key directly from keys()

        self.assertEqual(c2u, c1u.plain[c1u.plain.keys()[0]][0])
        self.assertEqual(c2u, c1u.plain_ordered[c1u.plain_ordered.keys()[0]][0])
        self.assertEqual(c2u, c1u.plain_default[c1u.plain_default.keys()[0]][0])
        self.assertEqual(c2u,
            c1u.restorable_plain[c1u.restorable_plain.keys()[0]][0])
        self.assertEqual(c2u,
            c1u.restorable_ordered[c1u.restorable_ordered.keys()[0]][0])
        self.assertEqual(c2u,
            c1u.restorable_default[c1u.restorable_default.keys()[0]][0])


    def test_dict_self_cycle(self):

        g = Group("group")
        c1 = C(42)
        g.elements.append(c1)
        c2 = C(67)
        g.elements.append(c2)

        c1.add(c1, 'a') # cycle to itself
        c1.add(c2, 'b') # c2 does not point to itself nor c1

        self.assertTrue(c1 in c1.plain)
        self.assertTrue(c1 in c1.plain_ordered)
        self.assertTrue(c1 in c1.plain_default)
        self.assertTrue(c1 in c1.restorable_plain)
        self.assertTrue(c1 in c1.restorable_ordered)
        self.assertTrue(c1 in c1.restorable_default)

        gp = pickle.dumps(g)
        gu = pickle.loads(gp)

        c1u = gu.elements[0]
        c2u = gu.elements[1]

        # check existence of keys directly

        # key c1u

        self.assertTrue(c1u in c1u.plain.keys())
        self.assertTrue(c1u in c1u.plain_ordered.keys())
        self.assertTrue(c1u in c1u.plain_default.keys())
        self.assertTrue(c1u in c1u.restorable_plain.keys())
        self.assertTrue(c1u in c1u.restorable_ordered.keys())
        self.assertTrue(c1u in c1u.restorable_default.keys())

        # key c2u

        self.assertTrue(c2u in c1u.plain.keys())
        self.assertTrue(c2u in c1u.plain_ordered.keys())
        self.assertTrue(c2u in c1u.plain_default.keys())
        self.assertTrue(c2u in c1u.restorable_plain.keys())
        self.assertTrue(c2u in c1u.restorable_ordered.keys())
        self.assertTrue(c2u in c1u.restorable_default.keys())

        # check direct key-based lookup

        # key c1u

        # fails because c1u hash changed during unpickling
        self.assertRaises(KeyError, lambda: c1u.plain[c1u][0])

        # fails because c1u hash changed during unpickling
        self.assertRaises(KeyError, lambda: c1u.plain_ordered[c1u][0])

        # succeeds, but only because it creates a new entry, equal to zero!
        self.assertEqual(len(c1u.plain_default), 2)
        self.assertEqual(0, c1u.plain_default[c1u][0].v)
        self.assertEqual(len(c1u.plain_default), 3)

        self.assertEqual(c1u, c1u.restorable_plain[c1u][0])
        self.assertEqual(c1u, c1u.restorable_ordered[c1u][0])
        self.assertEqual(c1u, c1u.restorable_default[c1u][0])

        # key c2u

        # succeeds because c2u does not have a cycle to itself
        self.assertEqual(c2u, c1u.plain[c2u][0])

        # succeeds because c2u does not have a cycle to itself
        self.assertEqual(c2u, c1u.plain_ordered[c2u][0])

        # succeeds because c2u does not have a cycle to itself
        self.assertEqual(c2u, c1u.plain_default[c2u][0])

        self.assertEqual(c2u, c1u.restorable_plain[c2u][0])
        self.assertEqual(c2u, c1u.restorable_ordered[c2u][0])
        self.assertEqual(c2u, c1u.restorable_default[c2u][0])

        # check key lookup with key directly from keys()

        # key c1u

        # fails because c1u hash changed during unpickling
        self.assertRaises(KeyError, lambda: c1u.plain[c1u.plain.keys()[0]][0])

        # fails because c1u hash changed during unpickling
        self.assertRaises(KeyError,
            lambda: c1u.plain_ordered[c1u.plain_ordered.keys()[0]][0])

        # succeeds because it is the previously-created duplicate key!
        self.assertEqual(0,
            c1u.plain_default[c1u.plain_default.keys()[0]][0].v)

        self.assertEqual(c1u,
            c1u.restorable_plain[c1u.restorable_plain.keys()[0]][0])
        self.assertEqual(c1u,
            c1u.restorable_ordered[c1u.restorable_ordered.keys()[0]][0])
        self.assertEqual(c1u,
            c1u.restorable_default[c1u.restorable_default.keys()[0]][0])

        # key c2u

        # succeeds because c2u does not have a cycle to itself
        self.assertEqual(c2u, c1u.plain[c1u.plain.keys()[1]][0])

        # succeeds because c2u does not have a cycle to itself
        self.assertEqual(c2u, c1u.plain_ordered[c1u.plain_ordered.keys()[1]][0])

        # succeeds but is the previously-created duplicate key, not c2u!
        self.assertEqual(0, c1u.plain_default[c1u.plain_default.keys()[1]][0].v)

        self.assertEqual(c2u,
            c1u.restorable_plain[c1u.restorable_plain.keys()[1]][0])
        self.assertEqual(c2u,
            c1u.restorable_ordered[c1u.restorable_ordered.keys()[1]][0])
        self.assertEqual(c2u,
            c1u.restorable_default[c1u.restorable_default.keys()[1]][0])

    def test_dict_mutual_cycle(self):

        g = Group("group")
        c1 = C(42)
        g.elements.append(c1)
        c2 = C(67)
        g.elements.append(c2)

        c1.add(c2, 'a') # points to c2, which points to c1, forming cycle
        c2.add(c1, 'a') # points to c1 in order to form cycle

        self.assertTrue(c2 in c1.plain)
        self.assertTrue(c2 in c1.plain_ordered)
        self.assertTrue(c2 in c1.plain_default)
        self.assertTrue(c2 in c1.restorable_plain)
        self.assertTrue(c2 in c1.restorable_ordered)
        self.assertTrue(c2 in c1.restorable_default)

        self.assertTrue(c1 in c2.plain)
        self.assertTrue(c1 in c2.plain_ordered)
        self.assertTrue(c1 in c2.plain_default)
        self.assertTrue(c1 in c2.restorable_plain)
        self.assertTrue(c1 in c2.restorable_ordered)
        self.assertTrue(c1 in c2.restorable_default)

        gp = pickle.dumps(g)
        gu = pickle.loads(gp)

        c1u = gu.elements[0]
        c2u = gu.elements[1]

        # check existence of keys directly

        # key c2u

        self.assertTrue(c2u in c1u.plain.keys())
        self.assertTrue(c2u in c1u.plain_ordered.keys())
        self.assertTrue(c2u in c1u.plain_default.keys())
        self.assertTrue(c2u in c1u.restorable_plain.keys())
        self.assertTrue(c2u in c1u.restorable_ordered.keys())
        self.assertTrue(c2u in c1u.restorable_default.keys())

        # key c1u

        self.assertTrue(c1u in c2u.plain.keys())
        self.assertTrue(c1u in c2u.plain_ordered.keys())
        self.assertTrue(c1u in c2u.plain_default.keys())
        self.assertTrue(c1u in c2u.restorable_plain.keys())
        self.assertTrue(c1u in c2u.restorable_ordered.keys())
        self.assertTrue(c1u in c2u.restorable_default.keys())

        # check direct key-based lookup

        # key c2u, succeed because c2u added to c1u after __setstate__

        self.assertEqual(c2u, c1u.plain[c2u][0])
        self.assertEqual(c2u, c1u.plain_ordered[c2u][0])
        self.assertEqual(c2u, c1u.plain_default[c2u][0])
        self.assertEqual(c2u, c1u.restorable_plain[c2u][0])
        self.assertEqual(c2u, c1u.restorable_ordered[c2u][0])
        self.assertEqual(c2u, c1u.restorable_default[c2u][0])

        # key c1u

        # fails because c1u hash changed during unpickling
        self.assertRaises(KeyError, lambda: c2u.plain[c1u][0])

        # fails because c1u hash changed during unpickling
        self.assertRaises(KeyError, lambda: c2u.plain_ordered[c1u][0])


        # succeeds, but only because it creates a new entry, equal to zero!
        self.assertEqual(len(c2u.plain_default), 1)
        self.assertEqual(0, c2u.plain_default[c1u][0].v)
        self.assertEqual(len(c2u.plain_default), 2)

        self.assertEqual(c1u, c2u.restorable_plain[c1u][0])
        self.assertEqual(c1u, c2u.restorable_ordered[c1u][0])
        self.assertEqual(c1u, c2u.restorable_default[c1u][0])

        # check key lookup with key directly from keys()

        # key c2u, succeed because c2u added to c1u after __setstate__

        self.assertEqual(c2u, c1u.plain[c1u.plain.keys()[0]][0])
        self.assertEqual(c2u, c1u.plain_ordered[c1u.plain_ordered.keys()[0]][0])
        self.assertEqual(c2u, c1u.plain_default[c1u.plain_default.keys()[0]][0])
        self.assertEqual(c2u,
            c1u.restorable_plain[c1u.restorable_plain.keys()[0]][0])
        self.assertEqual(c2u,
            c1u.restorable_ordered[c1u.restorable_ordered.keys()[0]][0])
        self.assertEqual(c2u,
            c1u.restorable_default[c1u.restorable_default.keys()[0]][0])

        # key c1u

        # fails because c1u hash changed during unpickling
        self.assertRaises(KeyError, lambda: c2u.plain[c2u.plain.keys()[0]][0])

        # fails because c1u hash changed during unpickling
        self.assertRaises(KeyError,
            lambda: c2u.plain_ordered[c2u.plain_ordered.keys()[0]][0])

        # succeeds but is the previously-created duplicate key, not c2u!
        self.assertEqual(0, c2u.plain_default[c2u.plain_default.keys()[0]][0].v)

        self.assertEqual(c1u,
            c2u.restorable_plain[c2u.restorable_plain.keys()[0]][0])
        self.assertEqual(c1u,
            c2u.restorable_ordered[c2u.restorable_ordered.keys()[0]][0])

        self.assertEqual(c1u,
            c2u.restorable_default[c2u.restorable_default.keys()[0]][0])


    def test_set_no_cycle(self):

        g = Group("group")
        d1 = D(42)
        g.elements.append(d1)
        d2 = D(67)
        g.elements.append(d2)

        d1.add(d2) # d1 points to d1, d2 does not point to anything, no cycles

        self.assertTrue(d2 in d1.plain)
        self.assertTrue(d2 in d1.restorable_plain)

        gp = pickle.dumps(g)
        gu = pickle.loads(gp)

        d1u = gu.elements[0]
        d2u = gu.elements[1]

        # check element directly

        self.assertTrue(d2u in d1u.plain)
        self.assertTrue(d2u in d1u.restorable_plain)

        # check element taken from elements

        self.assertTrue(list(d1u.plain)[0] in d1u.plain)
        self.assertTrue(list(d1u.restorable_plain)[0] in d1u.restorable_plain)


    def test_set_self_cycle(self):
        
        g = Group("group")
        d1 = D(42)
        g.elements.append(d1)
        d2 = D(67)
        g.elements.append(d2)

        d1.add(d1) # cycle to itself
        d1.add(d2) # d1 also points to d2, but d2 does not point to d1

        self.assertTrue(d1 in d1.plain)
        self.assertTrue(d1 in d1.restorable_plain)

        gp = pickle.dumps(g)
        gu = pickle.loads(gp)

        d1u = gu.elements[0]
        d2u = gu.elements[1]

        # check element directly

        # fails because d1u hash changed during unpickling
        self.assertFalse(d1u in d1u.plain)

        self.assertTrue(d1u in d1u.restorable_plain)

        # check element taken from elements

        # fails because d1u hash changed during unpickling
        self.assertFalse(list(d1u.plain)[0] in d1u.plain)

        # succeeds because d2u added to d1u after __setstate__

        self.assertTrue(list(d1u.plain)[1] in d1u.plain)
        self.assertTrue(list(d1u.restorable_plain)[0] in d1u.restorable_plain)
        self.assertTrue(list(d1u.restorable_plain)[1] in d1u.restorable_plain)


    def test_set_mutual_cycle(self):

        g = Group("group")
        d1 = D(42)
        g.elements.append(d1)
        d2 = D(67)
        g.elements.append(d2)

        d1.add(d2) # points to d2, which points to d1, forming cycle
        d2.add(d1) # points to d1 in order to form cycle

        self.assertTrue(d2 in d1.plain)
        self.assertTrue(d2 in d1.restorable_plain)
        self.assertTrue(d1 in d2.plain)
        self.assertTrue(d1 in d2.restorable_plain)

        gp = pickle.dumps(g)
        gu = pickle.loads(gp)

        d1u = gu.elements[0]
        d2u = gu.elements[1]

        # check element directly

        # succeeds because d2u added to d1u after __setstate__
        self.assertTrue(d2u in d1u.plain)

        self.assertTrue(d2u in d1u.restorable_plain)

        # fails because d1u hash changed during unpickling
        self.assertFalse(d1u in d2u.plain)

        self.assertTrue(d1u in d2u.restorable_plain)

        # check element taken from elements

        # succeeds because d2u added to d1u after __setstate__
        self.assertTrue(list(d1u.plain)[0] in d1u.plain)

        self.assertTrue(list(d1u.restorable_plain)[0] in d1u.restorable_plain)

        # fails because d1u hash changed during unpickling
        self.assertFalse(list(d2u.plain)[0] in d2u.plain)

        self.assertTrue(list(d2u.restorable_plain)[0] in d2u.restorable_plain)


class CPickleRestorableCollectionsTestCase(RestorableCollectionsTestCase):
    """
    The same as :class:`RestorableCollectionsTestCase` but with :mod:`cPickle`
    instead of :mod:`pickle`.
    """

    def setUp(self):
        self.pickle = cPickle

