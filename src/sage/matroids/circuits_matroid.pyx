r"""
Circuits matroids

Matroids are characterized by a list of circuits, which are minimal dependent
sets. The CircuitsMatroid class implements matroids using this information as
data.

A ``CircuitsMatroid`` can be created from another matroid or from a list of
circuits. For a full description of allowed inputs, see
:class:`below <sage.matroids.circuits_matroid.CircuitsMatroid>`. It is
recommended to use the :func:`Matroid() <sage.matroids.constructor.Matroid>`
function for a more flexible construction of a ``CircuitsMatroid``. For direct
access to the ``CircuitsMatroid`` constructor, run::

    sage: from sage.matroids.circuits_matroid import CircuitsMatroid

AUTHORS:

- Giorgos Mousa (2023-12-23): initial version

TESTS::

    sage: from sage.matroids.circuits_matroid import CircuitsMatroid
    sage: M = CircuitsMatroid(matroids.catalog.Fano())
    sage: TestSuite(M).run()

"""

# ****************************************************************************
#       Copyright (C) 2023 Giorgos Mousa <gmousa@proton.me>
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


cdef class CircuitsMatroid(Matroid):
    r"""
    INPUT:

    - ``M`` -- a matroid (default: ``None``)
    - ``groundset`` -- a list (default: ``None``); the groundset of the matroid
    - ``circuits`` -- a list (default: ``None``); the collection of circuits of
      the matroid

    OUTPUT:

    - If the input is a matroid ``M``, return a ``CircuitsMatroid`` instance
      representing ``M``.
    - Otherwise, return a ``CircuitsMatroid`` instance based on the
      ``groundset`` and ``circuits``.

    .. NOTE::

        For a more flexible means of input, use the ``Matroid()`` function.

    """

    # NECESSARY (__init__, groundset, _rank)


    def __init__(self, M=None, groundset=None, circuits=None):
        """
        Initialization of the matroid. See class docstring for full
        documentation.

        """
        if M is not None:
            self._groundset = frozenset(M.groundset())
            self._C = SetSystem(list(M.groundset()), frozenset([frozenset(C) for C in M.circuits()]))
        else:
            self._groundset = frozenset(groundset)
            self._C = SetSystem(list(groundset), frozenset([frozenset(C) for C in circuits]))
        # k-circuits
        self._k_C = {}
        for C in self._C:
            try:
                self._k_C[len(C)] += [C]
            except KeyError:
                self._k_C[len(C)] = []
                self._k_C[len(C)] += [C]
        self._matroid_rank = self.rank(self._groundset)
        # nonspanning circuits
        NSC = []
        for C in self._C:
            if len(C) <= self._matroid_rank:
                NSC += [C]
        self._NSC = SetSystem(list(self._groundset), frozenset([C for C in NSC]))

    cpdef groundset(self) noexcept:
        """
        Return the groundset of the matroid.

        The groundset is the set of elements that comprise the matroid.

        OUTPUT:

        a set (ordered)

        EXAMPLES::

            sage: M = matroids.Theta(2)
            sage: M.groundset()
            {'x0', 'x1', 'y0', 'y1'}

        """
        return set(sorted(self._groundset, key=str))

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
        return len(self._max_independent(X))


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

    cpdef _is_independent(self, F) noexcept:
        """
        Test if input is independent.

        INPUT:

        - ``X`` -- An object with Python's ``frozenset`` interface containing
          a subset of ``self.groundset()``

        OUTPUT:

        a Boolean

        """
        I = set(F)
        s = len(F)
        for i in self._k_C:
            if i <= s:
                for C in self._k_C[i]:
                    if C <= I:
                        return False
        return True

    cpdef _max_independent(self, F) noexcept:
        """
        Compute a maximal independent subset.

        INPUT:

        - ``X`` -- An object with Python's ``frozenset`` interface containing
          a subset of ``self.groundset()``

        OUTPUT:

        a frozenset; a maximal independent subset of ``X``

        """
        I = set(F)
        for i in self._k_C:
            for C in self._k_C[i]:
                if i <= len(I) and i > 0:
                    if C <= I:
                        for e in C:
                            break
                        I.remove(e)

        return frozenset(I)

    cpdef _circuit(self, F) noexcept:
        """
        Return a minimal dependent subset.

        INPUT:

        - ``X`` -- An object with Python's ``frozenset`` interface containing
          a subset of ``self.groundset()``.

        OUTPUT:

        a frozenset; a circuit contained in ``X``, if it exists. Otherwise an
        error is raised.

        """
        I = set(F)
        for C in self._C:
            if C <= I:
                return C
        raise ValueError("no circuit in independent set")

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
        N = CircuitsMatroid(other)
        return self._C._isomorphism(N._C) is not None


    # REPRESENTATION


    def _repr_(self):
        """
        Return a string representation of the matroid.

        """
        return Matroid._repr_(self) + " with " + str(len(self._C)) + " circuits"


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
        cdef CircuitsMatroid lt, rt
        if op not in [Py_EQ, Py_NE]:
            return NotImplemented
        if type(left) is not type(right):
            return NotImplemented
        lt = <CircuitsMatroid> left
        rt = <CircuitsMatroid> right
        if lt.groundset() != rt.groundset():
            return rich_to_bool(op, 1)
        if lt.full_rank() != rt.full_rank():
            return rich_to_bool(op, 1)
        return richcmp(frozenset(lt._C), frozenset(rt._C), op)


    # COPYING, LOADING, SAVING


    def __copy__(self):
        """
        Create a shallow copy.

        EXAMPLES::

            sage: M = matroids.catalog.Vamos()
            sage: N = copy(M)  # indirect doctest
            sage: M == N
            True
            sage: M.groundset() is N.groundset()
            True

        """
        N = CircuitsMatroid(groundset=[], circuits=[])
        N._groundset = self._groundset
        N._C = self._C
        N._matroid_rank = self._matroid_rank
        N.rename(self.get_custom_name())
        return N

    def __deepcopy__(self, memo=None):
        """
        Create a deep copy.

        .. NOTE::

            Since matroids are immutable, a shallow copy normally suffices.

        EXAMPLES::

            sage: M = matroids.catalog.Vamos()
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
        N = CircuitsMatroid(groundset=deepcopy(self._groundset, memo), circuits=deepcopy(frozenset(self._C), memo))
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
        data = (self._groundset, frozenset(self._C), self.get_custom_name())
        version = 0
        return sage.matroids.unpickling.unpickle_circuits_matroid, (version, data)

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

            sage: from sage.matroids.circuits_matroid import CircuitsMatroid
            sage: M = CircuitsMatroid(matroids.catalog.RelaxedNonFano())
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
        C = [[d[y] for y in list(x)] for x in self._C]
        M = CircuitsMatroid(groundset=E, circuits=C)
        return M


    # ENUMERATION


    cpdef bases(self) noexcept:
        r"""
        Return the bases of the matroid.

        OUTPUT:

        a list of sets (ordered)

        EXAMPLES::

            sage: from sage.matroids.circuits_matroid import CircuitsMatroid
            sage: M = CircuitsMatroid(matroids.Uniform(2, 4))
            sage: M.bases()
            [{0, 1}, {0, 2}, {0, 3}, {1, 2}, {1, 3}, {2, 3}]

        """
        return sorted([set(sorted(B, key=str)) for B in self._bases()], key=self._sort_key)

    cpdef _bases(self) noexcept:
        r"""
        Return the bases of the matroid.

        OUTPUT:

        an iterable

        EXAMPLES::

            sage: from sage.matroids.circuits_matroid import CircuitsMatroid
            sage: M = CircuitsMatroid(matroids.Uniform(2, 4))
            sage: sorted([sorted(X) for X in M._bases()])
            [[0, 1], [0, 2], [0, 3], [1, 2], [1, 3], [2, 3]]

        """
        cdef SetSystem bases
        if not self._B:
            from itertools import combinations
            bases = SetSystem(list(self._groundset))
            for B in combinations(self._groundset, self._matroid_rank):
                flag = True
                for C in self._NSC:
                    if C <= set(B):
                        flag = False
                        break
                if flag:
                    bases.append(frozenset(B))
            self._B = bases
        return self._B

    cpdef circuits(self, k=None) noexcept:
        """
        Return the list of circuits of the matroid.

        OUTPUT:

        a list of sets (ordered)

        EXAMPLES::

            sage: M = matroids.Theta(4)
            sage: M.circuits()
            [{'x0', 'x1', 'x2'},
            {'x0', 'x1', 'x3'},
            {'x0', 'x2', 'x3'},
            {'x1', 'x2', 'x3'},
            {'x0', 'y1', 'y2', 'y3'},
            {'x1', 'y0', 'y2', 'y3'},
            {'x2', 'y0', 'y1', 'y3'},
            {'x3', 'y0', 'y1', 'y2'},
            {'x0', 'x1', 'y0', 'y1', 'y2'},
            {'x0', 'x1', 'y0', 'y1', 'y3'},
            {'x0', 'x2', 'y0', 'y1', 'y2'},
            {'x0', 'x2', 'y0', 'y2', 'y3'},
            {'x0', 'x3', 'y0', 'y1', 'y3'},
            {'x0', 'x3', 'y0', 'y2', 'y3'},
            {'x1', 'x2', 'y0', 'y1', 'y2'},
            {'x1', 'x2', 'y1', 'y2', 'y3'},
            {'x1', 'x3', 'y0', 'y1', 'y3'},
            {'x1', 'x3', 'y1', 'y2', 'y3'},
            {'x2', 'x3', 'y0', 'y2', 'y3'},
            {'x2', 'x3', 'y1', 'y2', 'y3'}]

        .. SEEALSO::

            :meth:`Matroid.circuit() <sage.matroids.matroid.Matroid.circuit>`,
            :meth:`Matroid.closure() <sage.matroids.matroid.Matroid.closure>`

        """
        if k:
            return sorted([set(sorted(C, key=str)) for C in self._k_C[k]], key=self._sort_key)
        else:
            return sorted([set(sorted(C, key=str)) for C in self._C], key=self._sort_key)

    cpdef _circuits(self, k=None) noexcept:
        """
        Return the list of circuits of the matroid.

        OUTPUT:

        a list of sets (ordered)

        """
        if k:
            return self._k_C[k]
        else:
            return self._C

    cpdef nonspanning_circuits(self) noexcept:
        """
        Return the list of nonspanning circuits of the matroid.

        OUTPUT:

        a list of sets (ordered)

        """
        return sorted([set(sorted(C, key=str)) for C in self._NSC], key=self._sort_key)

    cpdef _nonspanning_circuits(self) noexcept:
        """
        Return the list of nonspanning circuits of the matroid.

        OUTPUT:

        a SetSystem

        """
        return self._NSC

    cpdef _sort_key(self, x) noexcept:
        return (len(x), str(sorted(x, key=str)))


    # VERIFICATION


    cpdef is_valid(self) noexcept:
        r"""
        Test if self obeys the matroid axioms.

        For a matroid defined by its circuits, we check the circuit axioms.

        OUTPUT:

        a Boolean

        EXAMPLES::

            sage: C = [[1, 2, 3], [3, 4, 5], [1, 2, 4, 5]]
            sage: M = Matroid(circuits=C)
            sage: M.is_valid()
            True
            sage: C = [[1,2], [1, 2, 3], [3, 4, 5], [1, 2, 4, 5]]
            sage: M = Matroid(circuits=C)
            sage: M.is_valid()
            False
            sage: C = [[3,6], [1, 2, 3], [3, 4, 5], [1, 2, 4, 5]]
            sage: M = Matroid(circuits=C)
            sage: M.is_valid()
            False
            sage: C = [[3,6], [1, 2, 3], [3, 4, 5], [1, 2, 6], [6, 4, 5], [1, 2, 4, 5]]
            sage: M = Matroid(circuits=C)
            sage: M.is_valid()
            True
            sage: C = [[], [1, 2, 3], [3, 4, 5], [1, 2, 4, 5]]
            sage: M = Matroid(circuits=C)
            sage: M.is_valid()
            False
            sage: C = [[1, 2, 3], [3, 4, 5]]
            sage: M = Matroid(circuits=C)
            sage: M.is_valid()
            False

        """
        for i in self._k_C:
            for j in self._k_C:
                if i <= j:
                    for C1 in self._k_C[i]:
                        if len(C1) == 0:
                            return False
                        for C2 in self._k_C[j]:
                            if C1 < C2:
                                return False
                            if C1 == C2:
                                break
                            for e in C1 & C2:
                                flag = False
                                S = (set(C1) | set(C2)) - {e}
                                for k in self._k_C:
                                    if k <= len(S) and not flag:
                                        for C3 in self._k_C[k]:
                                            if C3 <= S:
                                                flag = True
                                                break
                                if not flag:
                                    return False
        return True
