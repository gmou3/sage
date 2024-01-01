r"""
Circuits matroids

Matroids are characterized by a set of flats, which are sets invariant under
closure. The FlatsMatroid class implements matroids using this information as
data.

A ``FlatsMatroid`` can be created from another matroid or from a set of flats.
For a full description of allowed inputs, see
:class:`below <sage.matroids.flats_matroid.FlatsMatroid>`. It is
recommended to use the :func:`Matroid() <sage.matroids.constructor.Matroid>`
function for a more flexible construction of a ``FlatsMatroid``. For direct
access to the ``FlatsMatroid`` constructor, run::

    sage: from sage.matroids.flats_matroid import FlatsMatroid

AUTHORS:

- Giorgos Mousa (2024-01-01): initial version

TESTS::

    sage: from sage.matroids.flats_matroid import FlatsMatroid
    sage: M = FlatsMatroid(matroids.catalog.Fano())
    sage: # TestSuite(M).run()

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
    - ``circuits`` -- a list (default: ``None``); the collection of circuits of
      the matroid

    OUTPUT:

    - If the input is a matroid ``M``, return a ``FlatsMatroid`` instance
      representing ``M``.
    - Otherwise, return a ``FlatsMatroid`` instance based on the
      ``groundset`` and ``circuits``.

    .. NOTE::

        For a more flexible means of input, use the ``Matroid()`` function.

    """

    # NECESSARY (__init__, groundset, _rank)


    def __init__(self, M=None, groundset=None, flats=None):
        """
        Initialization of the matroid. See class docstring for full
        documentation.
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

        OUTPUT:

        a set

        EXAMPLES::

            sage: M = matroids.Theta(2)
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

        OUTPUT:

        an integer; the rank of ``X`` in the matroid

        EXAMPLES::

            sage: M = matroids.Theta(3)
            sage: M._rank(['x1', 'y0', 'y2'])
            2
        """
        min = len(self._groundset)
        for i in self._F:
            if i < min:
                for f in self._F[i]:
                    if f >= X:
                        min = i
                        break
        return min


    # OPTIONAL


    cpdef full_rank(self) noexcept:
        r"""
        Return the rank of the matroid.

        The *rank* of the matroid is the size of the largest independent
        subset of the groundset.

        OUTPUT:

        an integer; the rank of the matroid

        EXAMPLES::

            sage: M = matroids.Theta(20)
            sage: M.full_rank()
            20
        """
        return self._matroid_rank

    cpdef _is_isomorphic(self, other, certificate=False) noexcept:
        """
        Test if ``self`` is isomorphic to ``other``.

        INPUT:

        - ``other`` -- a matroid
        - ``certificate`` -- a Boolean (optional)

        OUTPUT:

        a Boolean,
        and, if certificate = True, a dictionary giving the isomorphism or None

        .. NOTE::

            Internal version that does no input checking.
        """
        if certificate:
            return self._is_isomorphic(other), self._isomorphism(other)
        N = FlatsMatroid(other)
        flats_self = [F for i in self._F for F in self._F[i]]
        flats_other = [F for i in N._F for F in N._F[i]]
        SS = SetSystem(list(self._groundset), flats_self)
        OS = SetSystem(list(N._groundset), flats_other)
        return SS._isomorphism(OS) is not None


    # REPRESENTATION


    def _repr_(self):
        """
        Return a string representation of the matroid.
        """
        return Matroid._repr_(self) + " with " + str(len(self._F)) + " flats"


    # COMPARISON


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

            sage: M = matroids.catalog.Vamos()
            sage: N = matroids.catalog.Vamos()
            sage: hash(M) == hash(N)
            True
            sage: O = matroids.catalog.NonVamos()
            sage: hash(M) == hash(O)
            False
        """
        return hash(tuple([self.groundset(), frozenset(self._C)]))

    def __richcmp__(left, right, int op):
        r"""
        Compare two matroids.

        We take a very restricted view on equality: the objects need to be of
        the exact same type (so no subclassing) and the internal data need to
        be the same. For BasisMatroids, this means that the groundsets and the
        sets of bases of the two matroids are equal.

        EXAMPLES::

            sage: M = matroids.catalog.Pappus()
            sage: N = matroids.catalog.NonPappus()
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


    # COPYING, LOADING, SAVING


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
        (currently 0) and ``data`` is a tuple ``(E, CC, name)`` where ``E`` is
        the groundset, ``CC`` is the dictionary of circuit closures, and
        ``name`` is a custom name.

        EXAMPLES::

            sage: M = matroids.catalog.Vamos()
            sage: M == loads(dumps(M))  # indirect doctest
            True
            sage: M.reset_name()
            sage: loads(dumps(M))
            Matroid of rank 4 on 8 elements with circuit-closures
            {3: {{'a', 'b', 'c', 'd'}, {'a', 'b', 'e', 'f'},
                 {'a', 'b', 'g', 'h'}, {'c', 'd', 'e', 'f'},
                 {'e', 'f', 'g', 'h'}},
             4: {{'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'}}}
        """
        import sage.matroids.unpickling
        data = (self._groundset, self._F, self.get_custom_name())
        version = 0
        return sage.matroids.unpickling.unpickle_flats_matroid, (version, data)

    cpdef relabel(self, l) noexcept:
        r"""
        Return an isomorphic matroid with relabeled groundset.

        The output is obtained by relabeling each element ``e`` by ``l[e]``,
        where ``l`` is a given injective map. If ``e not in l`` then the
        identity map is assumed.

        INPUT:

        - ``l`` -- a python object such that `l[e]` is the new label of `e`

        OUTPUT:

        a matroid

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
        """
        d = self._relabel_map(l)
        E = [d[x] for x in self._groundset]
        F = {}
        for i in self._F:
            F[i] = []
            F[i] += [[d[y] for y in list(x)] for x in self._F[i]]
        M = FlatsMatroid(groundset=E, flats=F)
        return M


    # ENUMERATION


    cpdef flats(self, k) noexcept:
        r"""
        Return the flats of the matroid.

        OUTPUT:

        a dictionary

        EXAMPLES::

            sage: from sage.matroids.flats_matroid import FlatsMatroid
            sage: M = FlatsMatroid(matroids.Uniform(2, 4))
            sage: M.print_bases()
            [[0, 1], [0, 2], [0, 3], [1, 2], [1, 3], [2, 3]]
        """
        if k in self._F:
            return self._F[k]
        else:
            return frozenset()

    def flats_iterator(self):
        r"""
        Return the bases of the matroid.

        OUTPUT:

        an iterable
        """
        for F in self._F:
            yield F


    # VERIFICATION


    cpdef is_valid(self) noexcept:
        r"""
        Test if self obeys the matroid axioms.

        For a matroid defined by its flats, we check the flat axioms.

        OUTPUT:

        a Boolean
        """
        E_flat = False
        for i in self._F:
            for F1 in self._F[i]:
                if F1 == self._groundset:
                    E_flats = True
                    break
        if not E_flat:
            return False

        for i in self._F:
            for j in self._F:
                if i <= j:
                    for F1 in self._F[i]:
                        if j == i+1:
                            for e in F1 ^ self._groundset:
                                cnt = 0
                                for F2 in self._F[j]:
                                    if F2 >= F1 | e:
                                        cnt += 1
                                if cnt != 1:
                                    return False
                        for F2 in self._F[j]:
                            flag = False
                            for k in self._F:
                                if k <= j and not flag:
                                    for F3 in self._F[k]:
                                        if F3 == F1 & F2:
                                            flag = True
                                            break
                            if not flag:
                                return False
        return True
