# sage_setup: distribution = sagemath-modules
# sage.doctest: needs sage.modules
r"""
Orlik-Solomon Algebras
"""

# ****************************************************************************
#       Copyright (C) 2015 William Slofstra
#                          Travis Scrimshaw <tscrimsh at umn.edu>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#                  https://www.gnu.org/licenses/
# ****************************************************************************

from sage.misc.cachefunc import cached_method
from sage.combinat.free_module import CombinatorialFreeModule
from sage.categories.algebras import Algebras
from sage.sets.family import Family
from sage.modules.with_basis.invariant import FiniteDimensionalInvariantModule


class OrlikSolomonAlgebra(CombinatorialFreeModule):
    r"""
    An Orlik-Solomon algebra.

    Let `R` be a commutative ring. Let `M` be a matroid with ground set
    `X`. Let `C(M)` denote the set of circuits of `M`. Let `E` denote
    the exterior algebra over `R` generated by `\{ e_x \mid x \in X \}`.
    The *Orlik-Solomon ideal* `J(M)` is the ideal of `E` generated by

    .. MATH::

        \partial e_S := \sum_{i=1}^t (-1)^{i-1} e_{j_1} \wedge e_{j_2}
        \wedge \cdots \wedge \widehat{e}_{j_i} \wedge \cdots \wedge e_{j_t}

    for all `S = \left\{ j_1 < j_2 < \cdots < j_t \right\} \in C(M)`,
    where `\widehat{e}_{j_i}` means that the term `e_{j_i}` is being
    omitted. The notation `\partial e_S` is not a coincidence, as
    `\partial e_S` is actually the image of
    `e_S := e_{j_1} \wedge e_{j_2} \wedge \cdots \wedge e_{j_t}` under the
    unique derivation `\partial` of `E` which sends all `e_x` to `1`.

    It is easy to see that `\partial e_S \in J(M)` not only for circuits
    `S`, but also for any dependent set `S` of `M`. Moreover, every
    dependent set `S` of `M` satisfies `e_S \in J(M)`.

    The *Orlik-Solomon algebra* `A(M)` is the quotient `E / J(M)`. This is
    a graded finite-dimensional skew-commutative `R`-algebra. Fix
    some ordering on `X`; then, the NBC sets of `M` (that is, the subsets
    of `X` containing no broken circuit of `M`) form a basis of `A(M)`.
    (Here, a *broken circuit* of `M` is defined to be the result of
    removing the smallest element from a circuit of `M`.)

    In the current implementation, the basis of `A(M)` is indexed by the
    NBC sets, which are implemented as frozensets.

    INPUT:

    - ``R`` -- the base ring
    - ``M`` -- the defining matroid
    - ``ordering`` -- (optional) an ordering of the ground set

    EXAMPLES:

    We create the Orlik-Solomon algebra of the uniform matroid `U(3, 4)`
    and do some basic computations::

        sage: M = matroids.Uniform(3, 4)
        sage: OS = M.orlik_solomon_algebra(QQ)
        sage: OS.dimension()
        14
        sage: G = OS.algebra_generators()
        sage: M.broken_circuits()
        frozenset({frozenset({1, 2, 3})})
        sage: G[1] * G[2] * G[3]
        OS{0, 1, 2} - OS{0, 1, 3} + OS{0, 2, 3}

    REFERENCES:

    - :wikipedia:`Arrangement_of_hyperplanes#The_Orlik-Solomon_algebra`

    - [CE2001]_
    """
    @staticmethod
    def __classcall_private__(cls, R, M, ordering=None):
        """
        Normalize input to ensure a unique representation.

        EXAMPLES::

            sage: M = matroids.Wheel(3)
            sage: from sage.algebras.orlik_solomon import OrlikSolomonAlgebra
            sage: OS1 = OrlikSolomonAlgebra(QQ, M)
            sage: OS2 = OrlikSolomonAlgebra(QQ, M, ordering=(0,1,2,3,4,5))
            sage: OS3 = OrlikSolomonAlgebra(QQ, M, ordering=[0,1,2,3,4,5])
            sage: OS1 is OS2 and OS2 is OS3
            True
        """
        if ordering is None:
            ordering = sorted(M.groundset())
        return super().__classcall__(cls, R, M, tuple(ordering))

    def __init__(self, R, M, ordering=None):
        """
        Initialize ``self``.

        EXAMPLES::

            sage: M = matroids.Wheel(3)
            sage: OS = M.orlik_solomon_algebra(QQ)
            sage: TestSuite(OS).run()

        We check on the matroid associated to the graph with 3 vertices and
        2 edges between each vertex::

            sage: # needs sage.graphs
            sage: G = Graph([[1,2],[1,2],[2,3],[2,3],[1,3],[1,3]], multiedges=True)
            sage: MG = Matroid(G)
            sage: OS = MG.orlik_solomon_algebra(QQ)
            sage: elts = OS.some_elements() + list(OS.algebra_generators())
            sage: TestSuite(OS).run(elements=elts)
        """
        self._M = M
        self._sorting = {x:i for i,x in enumerate(ordering)}

        # set up the dictionary of broken circuits
        self._broken_circuits = {}
        for c in self._M.circuits():
            L = sorted(c, key=lambda x: self._sorting[x])
            self._broken_circuits[frozenset(L[1:])] = L[0]

        cat = Algebras(R).FiniteDimensional().WithBasis().Graded()
        CombinatorialFreeModule.__init__(self, R, M.no_broken_circuits_sets(ordering),
                                         prefix='OS', bracket='{',
                                         sorting_key=self._sort_key,
                                         category=cat)

    def _sort_key(self, x):
        """
        Return the key used to sort the terms.

        EXAMPLES::

            sage: M = matroids.Wheel(3)
            sage: OS = M.orlik_solomon_algebra(QQ)
            sage: OS._sort_key(frozenset({1, 2}))
            (-2, [1, 2])
            sage: OS._sort_key(frozenset({0, 1, 2}))
            (-3, [0, 1, 2])
            sage: OS._sort_key(frozenset({}))
            (0, [])
        """
        return (-len(x), sorted(x))

    def _repr_term(self, m):
        """
        Return a string representation of the basis element indexed by `m`.

        EXAMPLES::

            sage: M = matroids.Uniform(3, 4)
            sage: OS = M.orlik_solomon_algebra(QQ)
            sage: OS._repr_term(frozenset([0]))
            'OS{0}'
        """
        return "OS{{{}}}".format(', '.join(str(t) for t in sorted(m)))

    def _repr_(self):
        """
        Return a string representation of ``self``.

        EXAMPLES::

            sage: M = matroids.Wheel(3)
            sage: M.orlik_solomon_algebra(QQ)
            Orlik-Solomon algebra of Wheel(3): Regular matroid of rank 3
             on 6 elements with 16 bases
        """
        return "Orlik-Solomon algebra of {}".format(self._M)

    @cached_method
    def one_basis(self):
        """
        Return the index of the basis element corresponding to `1`
        in ``self``.

        EXAMPLES::

            sage: M = matroids.Wheel(3)
            sage: OS = M.orlik_solomon_algebra(QQ)
            sage: OS.one_basis() == frozenset([])
            True
        """
        return frozenset({})

    @cached_method
    def algebra_generators(self):
        r"""
        Return the algebra generators of ``self``.

        These form a family indexed by the ground set `X` of `M`. For
        each `x \in X`, the `x`-th element is `e_x`.

        EXAMPLES::

            sage: M = matroids.Uniform(2, 2)
            sage: OS = M.orlik_solomon_algebra(QQ)
            sage: OS.algebra_generators()
            Finite family {0: OS{0}, 1: OS{1}}

            sage: M = matroids.Uniform(1, 2)
            sage: OS = M.orlik_solomon_algebra(QQ)
            sage: OS.algebra_generators()
            Finite family {0: OS{0}, 1: OS{0}}

            sage: M = matroids.Uniform(1, 3)
            sage: OS = M.orlik_solomon_algebra(QQ)
            sage: OS.algebra_generators()
            Finite family {0: OS{0}, 1: OS{0}, 2: OS{0}}
        """
        return Family(sorted(self._M.groundset()),
                      lambda i: self.subset_image(frozenset([i])))

    @cached_method
    def product_on_basis(self, a, b):
        r"""
        Return the product in ``self`` of the basis elements
        indexed by ``a`` and ``b``.

        EXAMPLES::

            sage: M = matroids.Wheel(3)
            sage: OS = M.orlik_solomon_algebra(QQ)
            sage: OS.product_on_basis(frozenset([2]), frozenset([3,4]))
            OS{0, 1, 2} - OS{0, 1, 4} + OS{0, 2, 3} + OS{0, 3, 4}

        ::

            sage: G = OS.algebra_generators()
            sage: prod(G)
            0
            sage: G[2] * G[4]
            -OS{1, 2} + OS{1, 4}
            sage: G[3] * G[4] * G[2]
            OS{0, 1, 2} - OS{0, 1, 4} + OS{0, 2, 3} + OS{0, 3, 4}
            sage: G[2] * G[3] * G[4]
            OS{0, 1, 2} - OS{0, 1, 4} + OS{0, 2, 3} + OS{0, 3, 4}
            sage: G[3] * G[2] * G[4]
            -OS{0, 1, 2} + OS{0, 1, 4} - OS{0, 2, 3} - OS{0, 3, 4}

        TESTS:

        Let us check that `e_{s_1} e_{s_2} \cdots e_{s_k} = e_S` for any
        subset `S = \{ s_1 < s_2 < \cdots < s_k \}` of the ground set::

            sage: # needs sage.graphs
            sage: G = Graph([[1,2],[1,2],[2,3],[3,4],[4,2]], multiedges=True)
            sage: MG = Matroid(G).regular_matroid()
            sage: E = MG.groundset_list()
            sage: OS = MG.orlik_solomon_algebra(ZZ)
            sage: G = OS.algebra_generators()
            sage: import itertools
            sage: def test_prod(F):
            ....:     LHS = OS.subset_image(frozenset(F))
            ....:     RHS = OS.prod([G[i] for i in sorted(F)])
            ....:     return LHS == RHS
            sage: all( test_prod(F) for k in range(len(E)+1)
            ....:                   for F in itertools.combinations(E, k) )
            True
        """
        if not a:
            return self.basis()[b]
        if not b:
            return self.basis()[a]

        if not a.isdisjoint(b):
            return self.zero()

        R = self.base_ring()
        # since a is disjoint from b, we can just multiply the generator
        if len(a) == 1:
            i = list(a)[0]
            # insert i into nbc, keeping track of sign in coeff
            ns = b.union({i})
            ns_sorted = sorted(ns, key=lambda x: self._sorting[x])
            coeff = (-1)**ns_sorted.index(i)

            return R(coeff) * self.subset_image(ns)

        # r is the accumulator
        # we reverse a in the product, so add a sign
        # note that l>=2 here
        if len(a) % 4 < 2:
            sign = R.one()
        else:
            sign = - R.one()
        r = self._from_dict({b: sign}, remove_zeros=False)

        # now do the multiplication generator by generator
        G = self.algebra_generators()
        for i in sorted(a, key=lambda x: self._sorting[x]):
            r = G[i] * r

        return r

    @cached_method
    def subset_image(self, S):
        """
        Return the element `e_S` of `A(M)` (``== self``) corresponding to
        a subset `S` of the ground set of `M`.

        INPUT:

        - ``S`` -- a frozenset which is a subset of the ground set of `M`

        EXAMPLES::

            sage: M = matroids.Wheel(3)
            sage: OS = M.orlik_solomon_algebra(QQ)
            sage: BC = sorted(M.broken_circuits(), key=sorted)
            sage: for bc in BC: (sorted(bc), OS.subset_image(bc))
            ([1, 3], -OS{0, 1} + OS{0, 3})
            ([1, 4, 5], OS{0, 1, 4} - OS{0, 1, 5} - OS{0, 3, 4} + OS{0, 3, 5})
            ([2, 3, 4], OS{0, 1, 2} - OS{0, 1, 4} + OS{0, 2, 3} + OS{0, 3, 4})
            ([2, 3, 5], OS{0, 2, 3} + OS{0, 3, 5})
            ([2, 4], -OS{1, 2} + OS{1, 4})
            ([2, 5], -OS{0, 2} + OS{0, 5})
            ([4, 5], -OS{3, 4} + OS{3, 5})

            sage: # needs sage.graphs
            sage: M4 = matroids.CompleteGraphic(4)
            sage: OSM4 = M4.orlik_solomon_algebra(QQ)
            sage: OSM4.subset_image(frozenset({2,3,4}))
            OS{0, 2, 3} + OS{0, 3, 4}

        An example of a custom ordering::

            sage: # needs sage.graphs
            sage: G = Graph([[3, 4], [4, 1], [1, 2], [2, 3], [3, 5], [5, 6], [6, 3]])
            sage: MG = Matroid(G)
            sage: s = [(5, 6), (1, 2), (3, 5), (2, 3), (1, 4), (3, 6), (3, 4)]
            sage: sorted([sorted(c) for c in MG.circuits()])
            [[(1, 2), (1, 4), (2, 3), (3, 4)],
             [(3, 5), (3, 6), (5, 6)]]
            sage: OSMG = MG.orlik_solomon_algebra(QQ, ordering=s)
            sage: OSMG.subset_image(frozenset([]))
            OS{}
            sage: OSMG.subset_image(frozenset([(1,2),(3,4),(1,4),(2,3)]))
            0
            sage: OSMG.subset_image(frozenset([(2,3),(1,2),(3,4)]))
            OS{(1, 2), (2, 3), (3, 4)}
            sage: OSMG.subset_image(frozenset([(1,4),(3,4),(2,3),(3,6),(5,6)]))
            -OS{(1, 2), (1, 4), (2, 3), (3, 6), (5, 6)}
             + OS{(1, 2), (1, 4), (3, 4), (3, 6), (5, 6)}
             - OS{(1, 2), (2, 3), (3, 4), (3, 6), (5, 6)}
            sage: OSMG.subset_image(frozenset([(1,4),(3,4),(2,3),(3,6),(3,5)]))
            OS{(1, 2), (1, 4), (2, 3), (3, 5), (5, 6)}
             - OS{(1, 2), (1, 4), (2, 3), (3, 6), (5, 6)}
             + OS{(1, 2), (1, 4), (3, 4), (3, 5), (5, 6)}
             + OS{(1, 2), (1, 4), (3, 4), (3, 6), (5, 6)}
             - OS{(1, 2), (2, 3), (3, 4), (3, 5), (5, 6)}
             - OS{(1, 2), (2, 3), (3, 4), (3, 6), (5, 6)}

        TESTS::

            sage: # needs sage.graphs
            sage: G = Graph([[1,2],[1,2],[2,3],[2,3],[1,3],[1,3]], multiedges=True)
            sage: MG = Matroid(G)
            sage: sorted([sorted(c) for c in MG.circuits()])
            [[0, 1], [0, 2, 4], [0, 2, 5], [0, 3, 4],
             [0, 3, 5], [1, 2, 4], [1, 2, 5], [1, 3, 4],
             [1, 3, 5], [2, 3], [4, 5]]
            sage: OSMG = MG.orlik_solomon_algebra(QQ)
            sage: OSMG.subset_image(frozenset([]))
            OS{}
            sage: OSMG.subset_image(frozenset([1, 2, 3]))
            0
            sage: OSMG.subset_image(frozenset([1, 3, 5]))
            0
            sage: OSMG.subset_image(frozenset([1, 2]))
            OS{0, 2}
            sage: OSMG.subset_image(frozenset([3, 4]))
            -OS{0, 2} + OS{0, 4}
            sage: OSMG.subset_image(frozenset([1, 5]))
            OS{0, 4}

            sage: # needs sage.graphs
            sage: G = Graph([[1,2],[1,2],[2,3],[3,4],[4,2]], multiedges=True)
            sage: MG = Matroid(G)
            sage: sorted([sorted(c) for c in MG.circuits()])
            [[0, 1], [2, 3, 4]]
            sage: OSMG = MG.orlik_solomon_algebra(QQ)
            sage: OSMG.subset_image(frozenset([]))
            OS{}
            sage: OSMG.subset_image(frozenset([1, 3, 4]))
            -OS{0, 2, 3} + OS{0, 2, 4}

        We check on a non-standard ordering::

            sage: M = matroids.Wheel(3)
            sage: o = [5,4,3,2,1,0]
            sage: OS = M.orlik_solomon_algebra(QQ, ordering=o)
            sage: BC = sorted(M.broken_circuits(ordering=o), key=sorted)
            sage: for bc in BC: (sorted(bc), OS.subset_image(bc))
            ([0, 1], OS{0, 3} - OS{1, 3})
            ([0, 1, 4], OS{0, 3, 5} - OS{0, 4, 5} - OS{1, 3, 5} + OS{1, 4, 5})
            ([0, 2], OS{0, 5} - OS{2, 5})
            ([0, 2, 3], -OS{0, 3, 5} + OS{2, 3, 5})
            ([1, 2], OS{1, 4} - OS{2, 4})
            ([1, 2, 3], -OS{1, 3, 5} + OS{1, 4, 5} + OS{2, 3, 5} - OS{2, 4, 5})
            ([3, 4], OS{3, 5} - OS{4, 5})
        """
        if not isinstance(S, frozenset):
            raise ValueError("S needs to be a frozenset")
        for bc in self._broken_circuits:
            if bc.issubset(S):
                i = self._broken_circuits[bc]
                if i in S:
                    # ``S`` contains not just a broken circuit, but an
                    # actual circuit; then `e_S = 0`.
                    return self.zero()
                coeff = self.base_ring().one()
                # Now, reduce ``S``, and build the result ``r``:
                r = self.zero()
                switch = False
                Si = S.union({i})
                Ss = sorted(Si, key=lambda x: self._sorting[x])
                for j in Ss:
                    if j in bc:
                        r += coeff * self.subset_image(Si.difference({j}))
                    if switch:
                        coeff *= -1
                    if j == i:
                        switch = True
                return r
        # So ``S`` is an NBC set.
        return self.monomial(S)

    def degree_on_basis(self, m):
        """
        Return the degree of the basis element indexed by ``m``.

        EXAMPLES::

            sage: M = matroids.Wheel(3)
            sage: OS = M.orlik_solomon_algebra(QQ)
            sage: OS.degree_on_basis(frozenset([1]))
            1
            sage: OS.degree_on_basis(frozenset([0, 2, 3]))
            3
        """
        return len(m)

    def as_gca(self):
        r"""
        Return the graded commutative algebra corresponding to ``self``.

        EXAMPLES::

            sage: # needs sage.geometry.polyhedron sage.graphs
            sage: H = hyperplane_arrangements.braid(3)
            sage: O = H.orlik_solomon_algebra(QQ)
            sage: O.as_gca()
            Graded Commutative Algebra with generators ('e0', 'e1', 'e2') in degrees (1, 1, 1)
             with relations [e0*e1 - e0*e2 + e1*e2] over Rational Field

        ::

            sage: N = matroids.catalog.Fano()
            sage: O = N.orlik_solomon_algebra(QQ)
            sage: O.as_gca()                                                            # needs sage.libs.singular
            Graded Commutative Algebra with generators ('e0', 'e1', 'e2', 'e3', 'e4', 'e5', 'e6')
             in degrees (1, 1, 1, 1, 1, 1, 1) with relations
             [e1*e2 - e1*e3 + e2*e3, e0*e1*e3 - e0*e1*e4 + e0*e3*e4 - e1*e3*e4,
              e0*e2 - e0*e4 + e2*e4, e3*e4 - e3*e5 + e4*e5,
              e1*e2*e4 - e1*e2*e5 + e1*e4*e5 - e2*e4*e5,
              e0*e2*e3 - e0*e2*e5 + e0*e3*e5 - e2*e3*e5, e0*e1 - e0*e5 + e1*e5,
              e2*e5 - e2*e6 + e5*e6, e1*e3*e5 - e1*e3*e6 + e1*e5*e6 - e3*e5*e6,
              e0*e4*e5 - e0*e4*e6 + e0*e5*e6 - e4*e5*e6, e1*e4 - e1*e6 + e4*e6,
              e2*e3*e4 - e2*e3*e6 + e2*e4*e6 - e3*e4*e6, e0*e3 - e0*e6 + e3*e6,
              e0*e1*e2 - e0*e1*e6 + e0*e2*e6 - e1*e2*e6] over Rational Field

        TESTS::

            sage: # needs sage.geometry.polyhedron
            sage: H = hyperplane_arrangements.Catalan(3,QQ).cone()
            sage: O = H.orlik_solomon_algebra(QQ)
            sage: A = O.as_gca()
            sage: H.poincare_polynomial()
            20*x^3 + 29*x^2 + 10*x + 1
            sage: [len(A.basis(i)) for i in range(5)]
            [1, 10, 29, 20, 0]
        """
        from sage.algebras.commutative_dga import GradedCommutativeAlgebra
        gens = self.algebra_generators()
        gkeys = gens.keys()
        names = ['e{}'.format(i) for i in range(len(gens))]
        A = GradedCommutativeAlgebra(self.base_ring(), names)
        rels = []
        for bc in self._broken_circuits.items():
            bclist = [bc[1]] + list(bc[0])
            indices = [gkeys.index(el) for el in bclist]
            indices.sort()
            rel = A.zero()
            sign = -(-1)**len(indices)
            for i in indices:
                mon = A.one()
                for j in indices:
                    if j != i:
                        mon *= A.gen(j)
                rel += sign * mon
                sign = -sign
            rels.append(rel)
        I = A.ideal(rels)
        return A.quotient(I)

    def as_cdga(self):
        r"""
        Return the commutative differential graded algebra corresponding
        to ``self`` with the trivial differential.

        EXAMPLES::

            sage: # needs sage.geometry.polyhedron sage.graphs
            sage: H = hyperplane_arrangements.braid(3)
            sage: O = H.orlik_solomon_algebra(QQ)
            sage: O.as_cdga()
            Commutative Differential Graded Algebra with generators ('e0', 'e1', 'e2')
             in degrees (1, 1, 1) with relations [e0*e1 - e0*e2 + e1*e2] over Rational Field
             with differential:
               e0 --> 0
               e1 --> 0
               e2 --> 0
        """
        return self.as_gca().cdg_algebra({})

    def aomoto_complex(self, omega):
        r"""
        Return the Aomoto complex of ``self`` defined by ``omega``.

        Let `A(M)` be an Orlik-Solomon algebra of a matroid `M`. Let
        `\omega \in A(M)_1` be an element of (homogeneous) degree 1.
        The Aomoto complete is the chain complex defined on `A(M)`
        with the differential defined by `\omega \wedge`.

        EXAMPLES::

            sage: OS = hyperplane_arrangements.braid(3).orlik_solomon_algebra(QQ)
            sage: gens = OS.algebra_generators()
            sage: AC = OS.aomoto_complex(gens[0])
            sage: ascii_art(AC)
                                      [0]
                        [1 0 0]       [0]
                        [0 1 0]       [1]
             0 <-- C_2 <-------- C_1 <---- C_0 <-- 0
            sage: AC.homology()
            {0: Vector space of dimension 0 over Rational Field,
             1: Vector space of dimension 0 over Rational Field,
             2: Vector space of dimension 0 over Rational Field}

            sage: AC = OS.aomoto_complex(-2*gens[0] + gens[1] + gens[2]); ascii_art(AC)
                                         [ 1]
                        [-1 -1 -1]       [ 1]
                        [-1 -1 -1]       [-2]
             0 <-- C_2 <----------- C_1 <----- C_0 <-- 0
            sage: AC.homology()
            {0: Vector space of dimension 0 over Rational Field,
             1: Vector space of dimension 1 over Rational Field,
             2: Vector space of dimension 1 over Rational Field}

        TESTS::

            sage: OS = hyperplane_arrangements.braid(4).orlik_solomon_algebra(QQ)
            sage: gens = OS.algebra_generators()
            sage: OS.aomoto_complex(gens[0] * gens[1] * gens[3])
            Traceback (most recent call last):
            ...
            ValueError: omega must be a homogeneous element of degree 1

        REFERENCES:

        - [BY2016]_
        """
        if not omega.is_homogeneous() or omega.degree() != 1:
            raise ValueError("omega must be a homogeneous element of degree 1")
        from sage.homology.chain_complex import ChainComplex
        R = self.base_ring()
        from collections import defaultdict
        from sage.matrix.constructor import matrix
        graded_basis = defaultdict(list)
        B = self.basis()
        for k in B.keys():
            graded_basis[len(k)].append(k)
        degrees = list(graded_basis)
        data = {i: matrix.zero(R, len(graded_basis[i+1]), len(graded_basis[i]))
                for i in degrees}
        for i in degrees:
            mat = data[i]
            for j, key in enumerate(graded_basis[i]):
                ret = (omega * B[key]).monomial_coefficients(copy=False)
                for k, imkey in enumerate(graded_basis[i+1]):
                    if imkey in ret:
                        mat[k,j] = ret[imkey]
            mat.set_immutable()
        return ChainComplex(data, R)


class OrlikSolomonInvariantAlgebra(FiniteDimensionalInvariantModule):
    r"""
    The invariant algebra of the Orlik-Solomon algebra from the
    action on `A(M)` induced from the ``action_on_groundset``.

    INPUT:

    - ``R`` -- the ring of coefficients
    - ``M`` -- a matroid
    - ``G`` -- a semigroup
    - ``action_on_groundset`` -- (optional) a function defining the action
      of ``G`` on the elements of the groundset of ``M``; default is ``g(x)``

    EXAMPLES:

    Lets start with the action of `S_3` on the rank `2` braid matroid::

        sage: # needs sage.graphs
        sage: M = matroids.CompleteGraphic(3)
        sage: M.groundset()
        frozenset({0, 1, 2})
        sage: G = SymmetricGroup(3)                                                     # needs sage.groups

    Calling elements ``g`` of ``G`` on an element `i` of `\{1, 2, 3\}`
    defines the action we want, but since the groundset is `\{0, 1, 2\}`
    we first add `1` and then subtract `1`::

        sage: def on_groundset(g, x):
        ....:     return g(x+1) - 1

    Now that we have defined an action we can create the invariant, and
    get its basis::

        sage: # needs sage.graphs sage.groups
        sage: OSG = M.orlik_solomon_algebra(QQ, invariant=(G, on_groundset))
        sage: OSG.basis()
        Finite family {0: B[0], 1: B[1]}
        sage: [OSG.lift(b) for b in OSG.basis()]
        [OS{}, OS{0} + OS{1} + OS{2}]

    Since it is invariant, the action of any ``g`` in ``G`` is trivial::

        sage: # needs sage.graphs sage.groups
        sage: x = OSG.an_element(); x
        2*B[0] + 2*B[1]
        sage: g = G.an_element(); g
        (2,3)
        sage: g * x
        2*B[0] + 2*B[1]

        sage: # needs sage.graphs sage.groups
        sage: x = OSG.random_element()
        sage: g = G.random_element()
        sage: g * x == x
        True

    The underlying ambient module is the Orlik-Solomon algebra,
    which is accessible via :meth:`ambient()`::

        sage: M.orlik_solomon_algebra(QQ) is OSG.ambient()                              # needs sage.graphs sage.groups
        True

    There is not much structure here, so lets look at a bigger example.
    Here we will look at the rank `3` braid matroid, and to make things
    easier, we'll start the indexing at `1` so that the `S_6` action
    on the groundset is simply calling `g`::

        sage: # needs sage.graphs sage.groups
        sage: M = matroids.CompleteGraphic(4); M.groundset()
        frozenset({0, 1, 2, 3, 4, 5})
        sage: new_bases = [frozenset(i+1 for i in j) for j in M.bases()]
        sage: M = Matroid(bases=new_bases); M.groundset()
        frozenset({1, 2, 3, 4, 5, 6})
        sage: G = SymmetricGroup(6)
        sage: OSG = M.orlik_solomon_algebra(QQ, invariant=G)
        sage: OSG.basis()
        Finite family {0: B[0], 1: B[1]}
        sage: [OSG.lift(b) for b in OSG.basis()]
        [OS{}, OS{1} + OS{2} + OS{3} + OS{4} + OS{5} + OS{6}]
        sage: (OSG.basis()[1])^2
        0
        sage: 5 * OSG.basis()[1]
        5*B[1]

    Next, we look at the same matroid but with an `S_3 \times S_3` action
    (here realized as a Young subgroup of `S_6`)::

        sage: # needs sage.graphs sage.groups
        sage: H = G.young_subgroup([3, 3])
        sage: OSH = M.orlik_solomon_algebra(QQ, invariant=H)
        sage: OSH.basis()
        Finite family {0: B[0], 1: B[1], 2: B[2]}
        sage: [OSH.lift(b) for b in OSH.basis()]
        [OS{}, OS{4} + OS{5} + OS{6}, OS{1} + OS{2} + OS{3}]

    We implement an `S_4` action on the vertices::

        sage: # needs sage.graphs sage.groups
        sage: M = matroids.CompleteGraphic(4)
        sage: G = SymmetricGroup(4)
        sage: edge_map = {i: M.groundset_to_edges([i])[0][:2]
        ....:             for i in M.groundset()}
        sage: inv_map = {v: k for k, v in edge_map.items()}
        sage: def vert_action(g, x):
        ....:     a, b = edge_map[x]
        ....:     return inv_map[tuple(sorted([g(a+1)-1, g(b+1)-1]))]
        sage: OSG = M.orlik_solomon_algebra(QQ, invariant=(G, vert_action))
        sage: B = OSG.basis()
        sage: [OSG.lift(b) for b in B]
        [OS{}, OS{0} + OS{1} + OS{2} + OS{3} + OS{4} + OS{5}]

    We use this to describe the Young subgroup `S_2 \times S_2` action::

        sage: # needs sage.graphs sage.groups
        sage: H = G.young_subgroup([2,2])
        sage: OSH = M.orlik_solomon_algebra(QQ, invariant=(H, vert_action))
        sage: B = OSH.basis()
        sage: [OSH.lift(b) for b in B]
        [OS{}, OS{5}, OS{1} + OS{2} + OS{3} + OS{4}, OS{0},
         -1/2*OS{1, 2} + OS{1, 5} - 1/2*OS{3, 4} + OS{3, 5},
         OS{0, 5}, OS{0, 1} + OS{0, 2} + OS{0, 3} + OS{0, 4},
         -1/2*OS{0, 1, 2} + OS{0, 1, 5} - 1/2*OS{0, 3, 4} + OS{0, 3, 5}]

    We demonstrate the algebra structure::

        sage: matrix([[b*bp for b in B] for bp in B])                                   # needs sage.graphs sage.groups
        [   B[0]    B[1]    B[2]    B[3]    B[4]    B[5]    B[6]    B[7]]
        [   B[1]       0  2*B[4]    B[5]       0       0  2*B[7]       0]
        [   B[2] -2*B[4]       0    B[6]       0 -2*B[7]       0       0]
        [   B[3]   -B[5]   -B[6]       0    B[7]       0       0       0]
        [   B[4]       0       0    B[7]       0       0       0       0]
        [   B[5]       0 -2*B[7]       0       0       0       0       0]
        [   B[6]  2*B[7]       0       0       0       0       0       0]
        [   B[7]       0       0       0       0       0       0       0]

    .. NOTE::

        The algebra structure only exists when the action on the
        groundset yields an equivariant matroid, in the sense that
        `g \cdot I \in \mathcal{I}` for every `g \in G` and for
        every `I \in \mathcal{I}`.
    """
    def __init__(self, R, M, G, action_on_groundset=None, *args, **kwargs):
        r"""
        Initialize ``self``.

        EXAMPLES::

            sage: # needs sage.graphs sage.groups
            sage: M = matroids.CompleteGraphic(4)
            sage: new_bases = [frozenset(i+1 for i in j) for j in M.bases()]
            sage: M = Matroid(bases=new_bases)
            sage: G = SymmetricGroup(6)
            sage: OSG = M.orlik_solomon_algebra(QQ, invariant=G)
            sage: TestSuite(OSG).run()
        """
        ordering = kwargs.pop('ordering', None)
        OS = OrlikSolomonAlgebra(R, M, ordering)
        self._ambient = OS

        if action_on_groundset is None:
            # if sage knows the action, we don't need to provide it

            def action_on_groundset(g, x):
                return g(x)

        self._groundset_action = action_on_groundset

        self._side = kwargs.pop('side', 'left')
        category = kwargs.pop('category', OS.category().Subobjects())

        def action(g, m):
            return OS.sum(c * self._basis_action(g, x)
                          for x, c in m._monomial_coefficients.items())

        self._action = action

        # Since an equivariant matroid yields a degree-preserving action
        # on the basis of OS, the matrix which computes the action when
        # computing the invariant will be a block matrix. To avoid dealing
        # with huge matrices, we can split it up into graded pieces.

        max_deg = max([b.degree() for b in OS.basis()])
        B = []  #initialize the basis
        for d in range(max_deg+1):
            OS_d = OS.homogeneous_component(d)
            OSG_d = OS_d.invariant_module(G, action=action, category=category)
            B += [OS_d.lift(OSG_d.lift(b)) for b in OSG_d.basis()]

        # `FiniteDimensionalInvariantModule.__init__` is already called
        # by `OS_d.invariant_module`, and so we pass to the superclass
        # of `FiniteDimensionalInvariantModule`, which is `SubmoduleWithBasis`.
        from sage.modules.with_basis.subquotient import SubmoduleWithBasis
        SubmoduleWithBasis.__init__(self, Family(B),
                                    support_order=OS._compute_support_order(B),
                                    ambient=OS,
                                    unitriangular=False,
                                    category=category,
                                    *args, **kwargs)

        # To subclass FiniteDimensionalInvariant module, we also need a
        # self._semigroup attribute.
        self._semigroup = G

    def construction(self):
        r"""
        Return the functorial construction of ``self``.

        This implementation of the method only returns ``None``.

        TESTS::

            sage: M = matroids.Wheel(3)
            sage: from sage.algebras.orlik_solomon import OrlikSolomonAlgebra
            sage: OS1 = OrlikSolomonAlgebra(QQ, M)
            sage: OS1.construction() is None
            True
        """
        return None

    def _basis_action(self, g, f):
        r"""
        Return the action of the group element ``g`` on the n.b.c. set ``f``
        in the ambient Orlik-Solomon algebra.

        INPUT:

        - ``g`` -- a group element
        - ``f`` -- ``frozenset`` for an n.b.c. set

        OUTPUT:

        - the result of the action of ``g`` on ``f`` inside
          of the Orlik-Solomon algebra

        EXAMPLES::

            sage: # needs sage.graphs sage.groups
            sage: M = matroids.CompleteGraphic(3)
            sage: M.groundset()
            frozenset({0, 1, 2})
            sage: G = SymmetricGroup(3)
            sage: def on_groundset(g, x):
            ....:     return g(x+1)-1
            sage: OSG = M.orlik_solomon_algebra(QQ, invariant=(G,on_groundset))
            sage: act = lambda g: (OSG._basis_action(g,frozenset({0,1})),
            ....:                  OSG._basis_action(g,frozenset({0,2})))
            sage: [act(g) for g in G]
            [(OS{0, 1}, OS{0, 2}),
             (-OS{0, 2}, OS{0, 1} - OS{0, 2}),
             (-OS{0, 1} + OS{0, 2}, -OS{0, 1}),
             (OS{0, 2}, OS{0, 1}),
             (OS{0, 1} - OS{0, 2}, -OS{0, 2}),
             (-OS{0, 1}, -OS{0, 1} + OS{0, 2})]

        We also check that the ordering is respected::

            sage: # needs sage.graphs sage.groups
            sage: fset = frozenset({1,2})
            sage: OS1 = M.orlik_solomon_algebra(QQ)
            sage: OS1.subset_image(fset)
            -OS{0, 1} + OS{0, 2}
            sage: OS2 = M.orlik_solomon_algebra(QQ, range(2,-1,-1))
            sage: OS2.subset_image(fset)
            OS{1, 2}
            sage: OSG2 = M.orlik_solomon_algebra(QQ,
            ....:                                invariant=(G,on_groundset),
            ....:                                ordering=range(2,-1,-1))
            sage: g = G.an_element(); g
            (2,3)

        This choice of ``g`` acting on this choice of ``fset`` reverses
        the sign::

            sage: OSG._basis_action(g, fset)                                            # needs sage.graphs sage.groups
            OS{0, 1} - OS{0, 2}
            sage: OSG2._basis_action(g, fset)                                           # needs sage.graphs sage.groups
            -OS{1, 2}
        """
        OS = self._ambient
        if not f:
            return OS.one()

        # basis_elt is an n.b.c. set, but it should be
        # in a standardized order to deal with sign issues
        basis_elt = sorted(f, key=OS._sorting.__getitem__)

        gx = OS.one()

        for e in basis_elt:
            fset = frozenset([self._groundset_action(g, e)])
            gx = gx * OS.subset_image(fset)

        return gx
