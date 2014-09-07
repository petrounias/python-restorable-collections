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
Python Restorable Collections provides an abstract interface to the restoration
facilities and life-cycle management of unpickled objects who feature
non-built-in types as keys and cycles or self-references, as well as concrete
implementations of restorable wrappers for :class:`dict`, :class:`defaultdict`,
:class:`OrderedDict`, and :class:`set`.

The project's website is available at:
`Python Restorable Collections
<http://www.petrounias.org/software/python-restorable-collections/>`_

Documentation is available at:
`Python Restorable Collections Documentation
<https://python-restorable-collections.readthedocs.org/en/latest/>`_

An article explaining the motivation, problem, and solution implemented here
will soon be available at:
`Pickling Python collections with non-built-in type keys and cycles
<http://www.petrounias.org/articles/>`_

The module :module:`restorable_collections_tests` contains all unit tests
associated with this module.
"""

__status__ = "Stable"
__version__ = "1.0.0"
__maintainer__ = (u"Alexis Petrounias <www.petrounias.org>", )
__author__ = (u"Alexis Petrounias <www.petrounias.org>", )

# Python
from collections import MutableMapping, MutableSet, OrderedDict, defaultdict

__all__ = ('VERSION', 'Restorable', 'RestorableDict', 'RestorableOrderedDict', )

VERSION = (1, 0, 0)


class Restorable(object):
    """
    Abstract mix-in class responsible for maintaining the
    :attr:`_requires_restoration` marker on an object, intercepting access to a
    wrapped :attr:`_contents` attribute, and invoking a user-supplied
    :meth:`_restore` method precisely once prior to the first access of the
    wrapped :attr:`_contents`.

    Intended to be used with any Collection Abstract Base Class which must
    handle creation and wrapping of :attr:`_contents`, as well as implementation
    of :meth:`_restore`.

    In order to use :meth:`__init__` must be invoked in the subclass's own
    initialization.
    """

    def __init__(self):
        """
        Marks this :class:`Restorable` with :attr:`_requires_restoration` as
        `False` because collections do not need to be restored unless they have
        just been unpickled.
        """
        self._requires_restoration = False

    def __setstate__(self, state):
        """
        After performing default object state restoration by assigning *state*
        to this object's internal :attr:`__dict__`, sets the
        :attr:`_requires_restoration` marker to `True` so that during the next
        wrapped :attr`_`contents` attribute access :meth`_restore` is called.

        If you inherit from :class:`Restorable` and override
        :meth:`__setstate__` then you must ensure the
        :attr:`_requires_restoration` market is set to `True`.

        :param object state: the unpickled state of this object.
        """
        self.__dict__ = state
        self._requires_restoration = True

    def __getattribute__(self, item):
        """
        Intercepts attribute access to this object so that the first time the
        wrapped :attr:`_contents` attribute is accessed the object is restored
        if necessary. This is achieved by checking whether
        :attr:`_requires_restoration` is `True` and if so, sets the marker to
        `False` and invokes :meth:`_restore`. Since the marker is set to `False`
        prior to invocation of the restoration logic, implementations of
        :meth:`_restore` are free to access thi object and its wrapped
        :attr:`_contents` without entering an indefinite recursion through this
        interceptor.

        :param str item: the attribute of interest.
        :return: the value of the attribute.
        """
        if item == '_contents':
            if self._requires_restoration:
                self._requires_restoration = False
                self._restore()
        return object.__getattribute__(self, item)

    def _restore(self):
        """
        Abstract method responsible for restoring the state of the wrapped
        :attr:`_contents` prior to first access. This method must be overridden
        by the subclass of :class:`Restorable`, otherwise it will raise a
        :class:`NotImplementedError`.

        This method is free to access this object and the wrapped
        :attr:`_contents` as attribute access interception will only invoke it
        once.

        :raises NotImplementedError: if not overridden by the subclass
        """
        raise NotImplementedError(
            "you must specify the _restore method with the Restorable type")


class RestorableDict(MutableMapping, Restorable, object):
    """
    A :class:`MutableMapping` restorable wrapper of a :class:`dict`.
    """

    def __init__(self, *args, **kwargs):
        self._contents = dict(*args, **kwargs)
        Restorable.__init__(self)

    def _restore(self):
        self._contents = { key : value for key, value in \
            self._contents.iteritems() }

    def __getitem__(self, item):
        return self._contents[item]

    def __setitem__(self, key, value):
        self._contents[key] = value

    def __delitem__(self, key):
        del self._contents[key]

    def __iter__(self):
        return iter(self._contents)

    def __len__(self):
        return len(self._contents)

    def __repr__(self):
        return """RestorableDict{}""".format(repr(self._contents))


class RestorableDefaultDict(RestorableDict, object):
    """
    A :class:`MutableMapping` restorable wrapper of a :class:`defaultdict`.
    """

    def __init__(self, *args, **kwargs):
        self._contents = defaultdict(*args, **kwargs)
        Restorable.__init__(self)
        self._restoration_pairs = None

    def __setstate__(self, state):
        Restorable.__setstate__(self, state)
        self._restoration_pairs = [ (key, value) for key, value in \
            state['_contents'].iteritems()]

    def _restore(self):
        self._contents = { key : value for key, value in \
            self._restoration_pairs }
        self._restoration_pairs = None

    def __repr__(self):
        return """RestorableDefaultDict{}""".format(repr(self._contents))


class RestorableOrderedDict(RestorableDict, object):
    """
    A :class:`MutableMapping` restorable wrapper of a :class:`OrderedDict`.
    """

    def __init__(self, *args, **kwargs):
        self._contents = OrderedDict(*args, **kwargs)
        Restorable.__init__(self)
        self._restoration_pairs = None

    def __setstate__(self, state):
        Restorable.__setstate__(self, state)
        self._restoration_pairs = [ (key, value) for key, value in \
            state['_contents'].iteritems()]

    def _restore(self):
        self._contents = { key : value for key, value in \
            self._restoration_pairs }
        self._restoration_pairs = None

    def __repr__(self):
        return """RestorableOrderedDict{}""".format(repr(self._contents))


class RestorableSet(MutableSet, Restorable, object):
    """
    A :class:`MutableSet` restorable wrapper of a :class:`set`.
    """

    def __init__(self, *args):
        self._contents = set(*args)
        Restorable.__init__(self)

    def _restore(self):
        self._contents = set(list(self._contents))

    def __contains__(self, x):
        return x in self._contents

    def __iter__(self):
        return iter(self._contents)

    def __len__(self):
        return len(self._contents)

    def add(self, value):
        return self._contents.add(value)

    def discard(self, value):
        return self._contents.discard(value)

    def __repr__(self):
        return """RestorableSet{}""".format(repr(self._contents))

