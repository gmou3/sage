r"""
Flats matroids

Matroids are characterized by a set of flats, which are sets invariant under
closure. The ``FlatsMatroid`` class implements matroids using this information
as data.

A ``FlatsMatroid`` can be created from another matroid or from a dictionary of
flats. For a full description of allowed inputs, see
:class:`below <sage.matroids.flats_matroid.FlatsMatroid>`. It is
recommended to use the :func:`Matroid() <sage.matroids.constructor.Matroid>`
function for a more flexible way of constructing a ``FlatsMatroid`` and other
classes of matroids. For direct access to the ``FlatsMatroid`` constructor,
run::

    sage: from sage.matroids.flats_matroid import FlatsMatroid

AUTHORS:

- Giorgos Mousa (2024-01-01): initial version
"""

# ****************************************************************************
#       Copyright (C) 2024 Giorgos Mousa <gmousa@proton.me>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#                  https://www.gnu.org/licenses/
# ****************************************************************************

from sage.structure.richcmp cimport rich_to_bool, richcmp
from sage.matroids.matroid cimport Matroid
from sage.matroids.set_system cimport SetSystem
from sage.matroids.utilities import setprint_s
from cpython.object cimport Py_EQ, Py_NE


cdef class FlatsMatroid(Matroid):
    r"""
    INPUT:

    - ``M`` -- a matroid (default: ``None``)
    - ``groundset`` -- a list (default: ``None``); the groundset of the matroid
    - ``flats`` -- a list (default: ``None``); the collection of flats of the
      matroid

    .. NOTE::

        For a more flexible means of input, use the ``Matroid()`` function.
    """

    # necessary (__init__, groundset, _rank)

    def __init__(self, M=None, groundset=None, flats=None):
        """
        Initialization of the matroid. See class docstring for full
        documentation.

        TESTS::

            sage: from sage.matroids.flats_matroid import FlatsMatroid
            sage: M = FlatsMatroid(matroids.catalog.Fano())
            sage: TestSuite(M).run()
        """
        self._F = {}
        if M is not None:
            self._groundset = frozenset(M.groundset())
            for i in range(len(M.groundset()) + 1):
                for F in M.flats(i):
                    try:
                        self._F[i].add(frozenset(F))
                    except KeyError:
                        self._F[i] = set()
                        self._F[i].add(frozenset(F))
        else:
            self._groundset = frozenset(groundset)
            for i in flats:
                for F in flats[i]:
                    try:
                        self._F[i].add(frozenset(F))
                    except KeyError:
                        self._F[i] = set()
                        self._F[i].add(frozenset(F))
        self._matroid_rank = self.rank(self._groundset)

    cpdef groundset(self) noexcept:
        """
        Return the groundset of the matroid.

        The groundset is the set of elements that comprise the matroid.

        OUTPUT: a set

        EXAMPLES::

            sage: from sage.matroids.flats_matroid import FlatsMatroid
            sage: M = FlatsMatroid(matroids.Theta(2))
            sage: sorted(M.groundset())
            ['x0', 'x1', 'y0', 'y1']
        """
        return self._groundset

    cpdef _rank(self, X) noexcept:
        """
        Return the rank of a set ``X``.

        This method does no checking on ``X``, and ``X`` may be assumed to have
        the same interface as ``frozenset``.

        INPUT:

        - ``X`` -- an object with Python's ``frozenset`` interface

        OUTPUT: an integer; the rank of ``X`` in the matroid

        EXAMPLES::

            sage: from sage.matroids.flats_matroid import FlatsMatroid
            sage: M = FlatsMatroid(matroids.Theta(3))
            sage: M._rank(['x1', 'y0', 'y2'])
            2
        """
        cdef frozenset XX = frozenset(X)
        cdef int min = len(self._groundset)
        for i in self._F:
            if i < min:
                for f in self._F[i]:
                    if f >= XX:
                        min = i
                        break
        return min

    # optional

    cpdef full_rank(self) noexcept:
        r"""
        Return the rank of the matroid.

        The *rank* of the matroid is the size of the largest independent
        subset of the groundset.

        OUTPUT: an integer; the rank of the matroid

        EXAMPLES::

            sage: from sage.matroids.flats_matroid import FlatsMatroid
            sage: M = FlatsMatroid(matroids.Theta(7))
            sage: M.full_rank()
            7
        """
        return self._matroid_rank

    cpdef _is_isomorphic(self, other, certificate=False) noexcept:
        """
        Test if ``self`` is isomorphic to ``other``.

        INPUT:

        - ``other`` -- a matroid
        - ``certificate`` -- boolean (default: ``False``)


        OUTPUT: boolean, and, if ``certificate=True``, a dictionary giving the
        isomorphism or ``None``

        EXAMPLES::

            sage: from sage.matroids.flats_matroid import FlatsMatroid
            sage: M = matroids.catalog.NonDesargues()
            sage: N = FlatsMatroid(M)
            sage: N._is_isomorphic(M)
            True
            sage: N._is_isomorphic(matroids.catalog.R9())
            False

        .. NOTE::

            Internal version that does no input checking.
        """
        if certificate:
            return self._is_isomorphic(other), self._isomorphism(other)
        N = FlatsMatroid(other)
        flats_self = frozenset([F for i in self._F for F in self._F[i]])
        flats_other = frozenset([F for i in N._F for F in N._F[i]])
        SS = SetSystem(list(self._groundset), flats_self)
        OS = SetSystem(list(N._groundset), flats_other)
        return SS._isomorphism(OS) is not None

    # representation

    def _repr_(self):
        """
        Return a string representation of the matroid.

        EXAMPLES::

            sage: from sage.matroids.flats_matroid import FlatsMatroid
            sage: M = FlatsMatroid(matroids.Uniform(6, 6)); M
            Matroid of rank 6 on 6 elements with 64 flats
        """
        flats_num = sum(1 for i in self._F for F in self._F[i])
        return Matroid._repr_(self) + " with " + str(flats_num) + " flats"

    # comparison

    def __hash__(self):
        r"""
        Return an invariant of the matroid.

        This function is called when matroids are added to a set. It is very
        desirable to override it so it can distinguish matroids on the same
        groundset, which is a very typical use case!

        .. WARNING::

            This method is linked to __richcmp__ (in Cython) and __cmp__ or
            __eq__/__ne__ (in Python). If you override one, you should
            (and in Cython: MUST) override the other!

        EXAMPLES::

            sage: from sage.matroids.flats_matroid import FlatsMatroid
            sage: M = FlatsMatroid(matroids.catalog.Vamos())
            sage: N = FlatsMatroid(matroids.catalog.Vamos())
            sage: hash(M) == hash(N)
            True
            sage: O = FlatsMatroid(matroids.catalog.NonVamos())
            sage: hash(M) == hash(O)
            False
        """
        flats = frozenset([F for i in self._F for F in self._F[i]])
        return hash(tuple([self._groundset, flats]))

    def __richcmp__(left, right, int op):
        r"""
        Compare two matroids.

        We take a very restricted view on equality: the objects need to be of
        the exact same type (so no subclassing) and the internal data need to
        be the same. For FlatsMatroids, this means that the groundsets and the
        dictionaries of flats of the two matroids are equal.

        EXAMPLES::

            sage: from sage.matroids.flats_matroid import FlatsMatroid
            sage: M = FlatsMatroid(matroids.catalog.Pappus())
            sage: N = FlatsMatroid(matroids.catalog.NonPappus())
            sage: M == N
            False
            sage: N = Matroid(M.bases())
            sage: M == N
            False
        """
        cdef FlatsMatroid lt, rt
        if op not in [Py_EQ, Py_NE]:
            return NotImplemented
        if type(left) is not type(right):
            return NotImplemented
        lt = <FlatsMatroid> left
        rt = <FlatsMatroid> right
        if lt.groundset() != rt.groundset():
            return rich_to_bool(op, 1)
        if lt.full_rank() != rt.full_rank():
            return rich_to_bool(op, 1)
        return richcmp(lt._F, rt._F, op)

    # copying, loading, saving

    def __copy__(self):
        """
        Create a shallow copy.

        EXAMPLES::

            sage: from sage.matroids.flats_matroid import FlatsMatroid
            sage: M = FlatsMatroid(matroids.catalog.Vamos())
            sage: N = copy(M)  # indirect doctest
            sage: M == N
            True
            sage: M.groundset() is N.groundset()
            True
        """
        N = FlatsMatroid(groundset=[], flats={})
        N._groundset = self._groundset
        N._F = self._F
        N._matroid_rank = self._matroid_rank
        N.rename(self.get_custom_name())
        return N

    def __deepcopy__(self, memo=None):
        """
        Create a deep copy.

        .. NOTE::

            Since matroids are immutable, a shallow copy normally suffices.

        EXAMPLES::

            sage: from sage.matroids.flats_matroid import FlatsMatroid
            sage: M = FlatsMatroid(matroids.catalog.Vamos())
            sage: N = deepcopy(M)  # indirect doctest
            sage: M == N
            True
            sage: M.groundset() is N.groundset()
            False
        """
        if memo is None:
            memo = {}
        from copy import deepcopy
        # Since matroids are immutable, N cannot reference itself in correct code, so no need to worry about the recursion.
        N = FlatsMatroid(groundset=deepcopy(self._groundset, memo), flats=deepcopy(self._F, memo))
        N.rename(deepcopy(self.get_custom_name(), memo))
        return N

    def __reduce__(self):
        """
        Save the matroid for later reloading.

        OUTPUT:

        A tuple ``(unpickle, (version, data))``, where ``unpickle`` is the
        name of a function that, when called with ``(version, data)``,
        produces a matroid isomorphic to ``self``. ``version`` is an integer
        (currently 0) and ``data`` is a tuple ``(E, F, name)`` where ``E`` is
        the groundset, ``F`` is the dictionary of flats, and ``name`` is a
        custom name.

        EXAMPLES::

            sage: from sage.matroids.flats_matroid import FlatsMatroid
            sage: M = FlatsMatroid(matroids.catalog.Vamos())
            sage: M == loads(dumps(M))  # indirect doctest
            True
            sage: M.reset_name()
            sage: loads(dumps(M))
            Matroid of rank 4 on 8 elements with 79 flats
        """
        import sage.matroids.unpickling
        data = (self._groundset, self._F, self.get_custom_name())
        version = 0
        return sage.matroids.unpickling.unpickle_flats_matroid, (version, data)

    cpdef relabel(self, f) noexcept:
        r"""
        Return an isomorphic matroid with relabeled groundset.

        The output is obtained by relabeling each element ``e`` by ``f[e]``,
        where ``f`` is a given injective map. If ``e not in f`` then the
        identity map is assumed.

        INPUT:

        - ``f`` -- a python object such that `f[e]` is the new label of `e`

        OUTPUT: a matroid

        EXAMPLES::

            sage: from sage.matroids.flats_matroid import FlatsMatroid
            sage: M = FlatsMatroid(matroids.catalog.RelaxedNonFano())
            sage: sorted(M.groundset())
            [0, 1, 2, 3, 4, 5, 6]
            sage: N = M.relabel({'g':'x', 0:'z'}) # 'g':'x' is ignored
            sage: sorted(N.groundset(), key=str)
            [1, 2, 3, 4, 5, 6, 'z']
            sage: M.is_isomorphic(N)
            True

        TESTS::

            sage: from sage.matroids.flats_matroid import FlatsMatroid
            sage: M = FlatsMatroid(matroids.catalog.RelaxedNonFano())
            sage: f = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g'}
            sage: N = M.relabel(f)
            sage: for S in powerset(M.groundset()):
            ....:     assert M.rank(S) == N.rank([f[x] for x in S])
        """
        d = self._relabel_map(f)
        E = [d[x] for x in self._groundset]
        F = {}
        for i in self._F:
            F[i] = []
            F[i] += [[d[y] for y in list(x)] for x in self._F[i]]
        M = FlatsMatroid(groundset=E, flats=F)
        return M

    # enumeration

    cpdef flats(self, k) noexcept:
        r"""
        Return the flats of the matroid.

        OUTPUT: a SetSystem

        EXAMPLES::

            sage: from sage.matroids.flats_matroid import FlatsMatroid
            sage: M = FlatsMatroid(matroids.Uniform(3, 4))
            sage: sorted(M.flats(2), key=str)
            [frozenset({0, 1}),
             frozenset({0, 2}),
             frozenset({0, 3}),
             frozenset({1, 2}),
             frozenset({1, 3}),
             frozenset({2, 3})]
        """
        if k in self._F:
            return SetSystem(list(self._groundset), self._F[k])
        return SetSystem(list(self._groundset))

    def flats_iterator(self, k):
        r"""
        Return an iterator over the flats of the matroid.

        EXAMPLES::

            sage: from sage.matroids.flats_matroid import FlatsMatroid
            sage: M = FlatsMatroid(matroids.Uniform(3, 4))
            sage: sorted([list(F) for F in M.flats_iterator(2)])
            [[0, 1], [0, 2], [0, 3], [1, 2], [1, 3], [2, 3]]
        """
        if k in self._F:
            for F in self._F[k]:
                yield F

    # verification

    cpdef is_valid(self) noexcept:
        r"""
        Test if ``self`` obeys the matroid axioms.

        For a matroid defined by its flats, we check the flat axioms.

        OUTPUT: boolean

        EXAMPLES::

            sage: M = Matroid(flats={0: [''], 1: ['0','1']})  # missing groundset
            sage: M.is_valid()
            False
            sage: M = Matroid(flats={0: [''], 1: ['0','1'], 2: ['01']})
            sage: M.is_valid()
            True
            sage: M = Matroid(flats={0: [''],
            ....:                    1: ['0','1','2','3','4','5','6','7','8','9','a','b','c'],
            ....:                    2: ['45','46','47','4c','56','57','5c','67','6c','7c',
            ....:                        '048','149','24a','34b','059','15a','25b','358',
            ....:                        '06a','16b','268','369','07b','178','279','37a',
            ....:                        '0123c','89abc'],
            ....:                    3: ['0123456789abc']})
            sage: M.is_valid()
            True
            sage: from sage.matroids.flats_matroid import FlatsMatroid
            sage: M = FlatsMatroid(matroids.catalog.NonVamos())
            sage: M.is_valid()
            True

        TESTS::

            sage: M = Matroid(flats={1: ['0','1'], 2: ['01']})  # missing an intersection
            sage: M.is_valid()
            False
            sage: M = Matroid(flats={0: [''],  # missing an extention of flat ['5'] by '6'
            ....:                    1: ['0','1','2','3','4','5','6','7','8','9','a','b','c'],
            ....:                    2: ['45','46','47','4c','57','5c','67','6c','7c',
            ....:                        '048','149','24a','34b','059','15a','25b','358',
            ....:                        '06a','16b','268','369','07b','178','279','37a',
            ....:                        '0123c','89abc'],
            ....:                    3: ['0123456789abc']})
            sage: M.is_valid()
            False
        """
        from itertools import combinations_with_replacement
        cdef int i, j, k, cnt
        cdef frozenset F1, F2, F3, I12, U1e
        cdef bint flag, E_flat

        E_flat = False
        for i in self._F:
            for F1 in self._F[i]:
                if F1 == self._groundset:
                    E_flat = True
                    break
        if not E_flat:  # the groundset must be a flat
            return False

        for (i, j) in combinations_with_replacement(sorted(self._F), 2):
            for F1 in self._F[i]:
                if j == i+1:
                    for e in F1 ^ self._groundset:
                        cnt = 0
                        U1e = F1 | set([e])
                        for F2 in self._F[j]:
                            if F2 >= U1e:
                                cnt += 1
                        if cnt != 1:
                            return False
                for F2 in self._F[j]:
                    flag = False
                    I12 = F1 & F2
                    for k in self._F:
                        if k <= j:
                            for F3 in self._F[k]:
                                if F3 == I12:
                                    flag = True
                                    break
                            if flag:
                                break
                    if not flag:
                        return False

        return True
