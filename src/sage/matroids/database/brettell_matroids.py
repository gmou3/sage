r"""
Collection of Brettell's matroids

This module contains implementations of Brettell's interesting matroids,
accessible through :mod:`matroids.catalog. <sage.matroids.catalog>` (type
and hit :kbd:`Tab` for a list).

AUTHORS:

- Nick Brettell (2023-02-25): initial version
- Giorgos Mousa (2023-12-08): import to sage and add examples

REFERENCES:

For more information, see `Nick Brettell's research page
<https://homepages.ecs.vuw.ac.nz/~bretteni/research.html>`_,
or one of the following references:

- [Bre2023]_ \N. Brettell, *The excluded minors for GF (5)-representable
  matroids on ten elements*, arXiv preprint :arxiv:`2307.14614` (2023).

- [BP2023]_ \N. Brettell and R. Pendavingh, *Computing excluded minors for
  classes of matroids representable over partial fields*, arXiv preprint
  :arxiv:`2302.13175` (2023).

"""
from sage.matrix.constructor import Matrix
from sage.matroids.circuit_closures_matroid import CircuitClosuresMatroid
from sage.matroids.linear_matroid import TernaryMatroid, QuaternaryMatroid
from sage.rings.finite_rings.finite_field_constructor import GF


# 7 elements:


def RelaxedNonFano():
    """
    Return the relaxed NonFano matroid.

    An excluded minor for `2`-regular matroids. UPF is `K_2`.

    EXAMPLES::

        sage: M = matroids.catalog.RelaxedNonFano()
        sage: M.is_valid()
        True

    """
    GF4 = GF(4, 'w')
    w = GF4('w')
    A = Matrix(GF4, [[1, 1, 0, 1], [1, 0, 1, 1], [0, 1, w, 1]])
    M = QuaternaryMatroid(reduced_matrix=A)
    M.rename("F7=: " + repr(M))
    return M


def TippedFree3spike():
    """
    Return the tipped free `3`-spike.

    Unique 3-connected extension of
    :func:`U36 <sage.matroids.database.oxley_matroids.U36>`. Stabilizer for
    `K_2`.

    EXAMPLES::

        sage: M = matroids.catalog.TippedFree3spike()
        sage: M.has_minor(matroids.Uniform(3,6))
        True

    """
    GF4 = GF(4, 'w')
    w = GF4('w')
    A = Matrix(GF4, [[1, 1, 1, 1], [1, w + 1, 0, w], [1, 0, w + 1, w]])
    M = QuaternaryMatroid(
        reduced_matrix=A, groundset=[0, 3, 5, 1, 4, 6, 2]
    )
    M.rename("Tipped rank-3 free spike: " + repr(M))
    return M


# 8 elements:


def AG23minusDY():
    r"""
    Return the matroid `AG23minusDY`.

    The matroid obtained from a `AG(2, 3)\setminus e` by a single `\delta-Y`
    exchange on a triangle. An excluded minor for near-regular matroids. UPF
    is `S`.

    EXAMPLES::

        sage: M = matroids.catalog.AG23minusDY()
        sage: M.is_valid()
        True

    """
    A = Matrix(GF(3), [[1, 1, 1, 1], [1, 0, 1, 2], [2, 0, 1, 2], [2, 1, 1, 0]])
    M = TernaryMatroid(reduced_matrix=A)
    M.rename("Delta-Y of AG(2,3)\\e: " + repr(M))
    return M


def TQ8():
    """
    Return the matroid `TQ8`.

    An excluded minor for `2`-regular matroids.
    UPF is `K_2`. Self-dual.

    EXAMPLES::

        sage: M = matroids.catalog.TQ8()
        sage: M.is_isomorphic(M.dual())
        True

    """
    GF4 = GF(4, 'w')
    w = GF4('w')
    A = Matrix(
        GF4, [[0, w, 1, 1], [1, 0, w, w + 1], [1, w, 0, w], [1, w + 1, 1, 0]]
    )
    M = QuaternaryMatroid(
        reduced_matrix=A, groundset=[1, 7, 5, 3, 8, 6, 4, 2]
    )
    M.rename("TQ8: " + repr(M))
    return M


def P8p():
    """
    Return the matroid `P8^-`.

    `P8^-` is obtained by relaxing one of the disjoint circuit-hyperplanes of
    :func:`P8 <sage.matroids.database.oxley_matroids.P8>`. An excluded minor
    for `2`-regular matroids. UPF is `K_2`. Self-dual.

    EXAMPLES::

        sage: M = matroids.catalog.P8p()
        sage: M.is_isomorphic(M.dual())
        True

    """
    GF4 = GF(4, 'w')
    w = GF4('w')
    A = Matrix(
        GF4, [[1, 1, 1, w], [1, w + 1, 1, 0], [1, 0, w, w], [0, 1, 1, 1]]
    )
    M = QuaternaryMatroid(
        reduced_matrix=A, groundset=['a', 'c', 'b', 'f', 'd', 'e', 'g', 'h']
    )
    M.rename("P8-: " + repr(M))
    return M


def KP8():
    """
    Return the matroid `KP8`.

    An excluded minor for `K_2`-representable matroids.
    UPF is `G`. Self-dual. Uniquely `GF(5)`-representable.
    (An excluded minor for `H_2`-representable matroids.)

    EXAMPLES::

        sage: M = matroids.catalog.KP8()
        sage: M.is_isomorphic(M.dual())
        True

    """
    GF4 = GF(4, 'w')
    w = GF4('w')
    A = Matrix(
        GF4, [[0, 1, 1, 1], [1, 0, w, w], [1, 1, 1, 1 + w], [1, 1, 1 + w, 0]]
    )
    M = QuaternaryMatroid(
        reduced_matrix=A, groundset=[1, 4, 3, 5, 6, 7, 0, 2]
    )
    M.rename("KP8: " + repr(M))
    return M


def Sp8():
    """
    Return the matroid `Sp8`.

    An excluded minor for `G`- and `K_2`-representable matroids.
    UPF is `U_1^{(2)}`. Self-dual.
    (An excluded minor for `H_2`- and `GF(5)`-representable matroids.)

    EXAMPLES::

        sage: M = matroids.catalog.Sp8()
        sage: M.is_isomorphic(M.dual())
        True

    """
    GF4 = GF(4, 'w')
    w = GF4('w')
    A = Matrix(
        GF4, [[1, 1, w + 1, 0], [1, 1, 0, w + 1], [1, 0, w, w], [0, 1, 1, 1]]
    )
    M = QuaternaryMatroid(
        reduced_matrix=A, groundset=[1, 2, 3, 5, 4, 6, 7, 8]
    )
    M.rename("Sp8: " + repr(M))
    return M


def Sp8pp():
    """
    Return the matroid `Sp8=`.

    An excluded minor for `G`- and `K_2`-representable matroids.
    UPF is `(GF(2)(a,b),<a,b,a+1,b+1,ab+a+b>)`. Self-dual.
    (An excluded minor for `H_2`- and `GF(5)`-representable matroids.)

    EXAMPLES::

        sage: M = matroids.catalog.Sp8pp()
        sage: M.is_isomorphic(M.dual())
        True

    """
    GF4 = GF(4, 'w')
    w = GF4('w')
    A = Matrix(GF4, [[1, w, 1, 0], [1, 1, 1, 1], [w, 0, 1, w], [0, w, 1, 1]])
    M = QuaternaryMatroid(
        reduced_matrix=A, groundset=[1, 5, 6, 7, 2, 3, 4, 8]
    )
    M.rename("Sp8=: " + repr(M))
    return M


def LP8():
    """
    Return the matroid `LP8`.

    An excluded minor for `G`- and `K_2`-representable matroids.
    Self-dual. UPF is `W`.
    (Also an excluded minor for `H_2`- and `GF(5)`-representable matroids.)

    EXAMPLES::

        sage: M = matroids.catalog.LP8()
        sage: M.is_isomorphic(M.dual())
        True

    """
    GF4 = GF(4, 'w')
    w = GF4('w')
    A = Matrix(
        GF4, [[1, 1, 1, 1], [w + 1, w, 0, 1], [1, 0, w + 1, 1], [0, w, w, 1]]
    )
    M = QuaternaryMatroid(
        reduced_matrix=A, groundset=['a', 'b', 'd', 'e', 'c', 'f', 'g', 'h']
    )
    M.rename("LP8: " + repr(M))
    return M


def WQ8():
    r"""
    Return the matroid `WQ8`.

    An excluded minor for `G`, `K_2`, `H_4`, and `GF(5)`-representable
    matroids. Self-dual. UPF is `(Z[\zeta,a], <\zeta,a-\zeta>)` where `\zeta`
    is solution to `x^2-x+1 = 0` and `a` is an indeterminate.

    EXAMPLES::

        sage: M = matroids.catalog.WQ8()
        sage: M.is_isomorphic(M.dual())
        True

    """
    GF4 = GF(4, 'w')
    w = GF4('w')
    A = Matrix(
        GF4, [[1, 0, 1, w + 1], [1, 1, 1, 1], [w, 1, 1, 0], [0, w, 1, 1]]
    )
    M = QuaternaryMatroid(
        reduced_matrix=A, groundset=[0, 1, 3, 4, 2, 5, 6, 7]
    )
    M.rename("WQ8: " + repr(M))
    return M


# 9 elements:


def BB9():
    """
    Return the matroid `BB9`.

    An excluded minor for `K_2`-representable matroids, and a restriction of
    the Betsy Ross matroid. The UPF is `G`. Uniquely `GF(5)`-representable.
    (An excluded minor for `H_2`-representable matroids.)

    EXAMPLES::

        sage: BB = matroids.catalog.BB9()
        sage: BR = matroids.catalog.BetsyRoss()
        sage: for M in BB.extensions(): # long time
        ....:     for N in M.extensions():
        ....:         if N.is_isomorphic(BR):
        ....:             print(True)
        True
        True

    """
    GF4 = GF(4, 'w')
    w = GF4('w')
    A = Matrix(
        GF4, [[1, 0, 1, 1, 1, 1],
              [0, 1, w, 1, 0, w],
              [w + 1, 1, w + 1, 1, w, 0]]
    )
    M = QuaternaryMatroid(
        reduced_matrix=A,
        groundset=['i', 'b', 'd', 'j', 'h', 'f', 'c', 'a', 'k']
    )
    M.rename("BB9: " + repr(M))
    return M


def TQ9():
    """
    Return the matroid `TQ9`.

    An excluded minor for `K_2`-representable matroids, and
    a single-element extension of
    :func:`TQ8 <sage.matroids.database.brettell_matroids.TQ8>`.
    The UPF is `G`. Uniquely `GF(5)`-representable.
    (An excluded minor for `H_2`-representable matroids.)

    EXAMPLES::

        sage: TQ8 = matroids.catalog.TQ8()
        sage: TQ9 = matroids.catalog.TQ9()
        sage: for M in TQ8.extensions():
        ....:     if M.is_isomorphic(TQ9):
        ....:         print(True)
        ....:         break
        True

    """
    GF4 = GF(4, 'w')
    w = GF4('w')
    A = Matrix(
        GF4, [[1, 0, w, 1, 1],
              [w + 1, 0, 0, w, 1],
              [1, w, 0, 0, w + 1],
              [1, 1, 1, 1, 0]],
    )
    M = QuaternaryMatroid(
        reduced_matrix=A, groundset=[1, 4, 6, 0, 2, 5, 3, 7, 8]
    )
    M.rename("TQ9: " + repr(M))
    return M


def TQ9p():
    """
    Return the matroid `TQ9^-`.

    An excluded minor for `G`- and `K_2`-representable matroids, and
    a single-element extension of
    :func:`TQ8 <sage.matroids.database.brettell_matroids.TQ8>`. UPF is
    `U_1^{(2)}`. (An excluded minor for `H_2`- and
    `GF(5)`-representable matroids.)

    EXAMPLES::

        sage: TQ8 = matroids.catalog.TQ8()
        sage: TQ9p = matroids.catalog.TQ9p()
        sage: for M in TQ8.extensions():
        ....:     if M.is_isomorphic(TQ9p):
        ....:         print(True)
        ....:         break
        True

    """
    GF4 = GF(4, 'w')
    w = GF4('w')
    A = Matrix(
        GF4,
        [
            [1, 1, 1, w + 1, 1],
            [w + 1, w, w + 1, w + 1, w + 1],
            [w, 0, w, 1, w + 1],
            [0, 1, w + 1, w + 1, 0],
        ],
    )
    M = QuaternaryMatroid(
        reduced_matrix=A, groundset=[1, 4, 7, 8, 0, 6, 5, 2, 3]
    )
    M.rename("TQ9': " + repr(M))
    return M


def M8591():
    r"""
    Return the matroid `M8591`.

    An excluded minor for `K_2`-representable matroids.
    A `Y-\delta` exchange on the unique triad gives
    :func:`A9 <sage.matroids.database.brettell_matroids.A9>`. The UPF is `P_4`.

    EXAMPLES::

        sage: M = matroids.catalog.M8591()
        sage: M.is_valid()
        True

    """
    GF4 = GF(4, 'w')
    w = GF4('w')
    A = Matrix(
        GF4, [[1, 1, 0, w, 1],
              [0, 1, 1, w, w + 1],
              [1, 0, w, w, 1],
              [0, 0, 1, 1, 0]]
    )
    M = QuaternaryMatroid(reduced_matrix=A)
    M.rename("M8591: " + repr(M))
    return M


def PP9():
    """
    Return the matroid `PP9`.

    An excluded minor for `K_2`-representable matroids. A single-element
    extension of `P8^-`. The UPF is `P_4`. Has a
    :func:`P8p <sage.matroids.database.brettell_matroids.P8p>`-minor (delete
    `z`). Uniquely `GF(5)`-representable. (An excluded minor for
    `H_2`-representable matroids.)

    EXAMPLES::

        sage: P8p = matroids.catalog.P8p()
        sage: PP9 = matroids.catalog.PP9()
        sage: for M in P8p.extensions():
        ....:     if M.is_isomorphic(PP9):
        ....:         print(True)
        ....:         break
        True
        sage: M = PP9.delete('z')
        sage: M.is_isomorphic(P8p)
        True

    """
    GF4 = GF(4, 'w')
    w = GF4('w')
    A = Matrix(
        GF4, [[1, 1, 1, w, w],
              [1, 1 + w, 1, 0, w],
              [1, 0, w, w, w],
              [0, 1, 1, 1, 1]]
    )
    M = QuaternaryMatroid(
        reduced_matrix=A,
        groundset=['a', 'c', 'b', 'f', 'd', 'e', 'g', 'h', 'z']
    )
    M.rename("PP9: " + repr(M))
    return M


def BB9gDY():
    r"""
    Return the matroid `BB9gDY`.

    An excluded minor for `K_2`-representable matroids. The UPF is `G`. In a
    `DY^*`-equivalence class of 4 matroids, one of which can be obtained from
    :func:`BB9 <sage.matroids.database.brettell_matroids.BB9>` by a
    segment-cosegment exchange on `\{a,d,i,j\}`. Uniquely
    `GF(5)`-representable. (An excluded minor for `H_2`-representable
    matroids.)

    EXAMPLES::

        sage: M = matroids.catalog.BB9gDY()
        sage: M.is_valid()
        True

    """
    GF4 = GF(4, 'w')
    w = GF4('w')
    A = Matrix(
        GF4,
        [
            [w, w, w + 1, 1],
            [w, 1, 0, 0],
            [w + 1, 1, 0, 0],
            [1, w, w + 1, w],
            [w, 0, 1, 1],
        ],
    )
    # M9573
    M = QuaternaryMatroid(
        reduced_matrix=A,
        groundset=['c', 'd', 'i', 'f', 'h', 'a', 'j', 'k', 'b']
    )
    M.rename("Segment cosegment exchange on BB9: " + repr(M))
    return M


def A9():
    """
    Return the matroid `A9`.

    An excluded minor for `K_2`-representable matroids.
    The UPF is `P_4`. Uniquely `GF(5)`-representable.
    (An excluded minor for `H_2`-representable matroids.)

    EXAMPLES::

        sage: M = matroids.catalog.A9()
        sage: M.is_valid()
        True

    """
    GF4 = GF(4, 'w')
    w = GF4('w')
    A = Matrix(
        GF4, [[w + 1, 1, w, w, w, w],
              [0, 1, 1, w + 1, 0, w],
              [w, 0, 1, w + 1, w, 1]]
    )
    M = QuaternaryMatroid(
        reduced_matrix=A, groundset=[6, 5, 4, 1, 2, 3, 7, 8, 0]
    )
    M.rename("A9: " + repr(M))
    return M


def FN9():
    """
    Return the matroid `FN9`.

    An excluded minor for `G`- and `K_2`-representable matroids.
    In a `DY^*`-equivalence class of `10` matroids. UPF is `U_1^{(2)}`.
    (An excluded minor for `H_2`- and `GF(5)`-representable matroids.)

    EXAMPLES::

        sage: M = matroids.catalog.FN9()
        sage: M.is_valid()
        True

    """
    GF4 = GF(4, 'w')
    w = GF4('w')
    A = Matrix(
        GF4,
        [
            [w + 1, w, w + 1, w, 1, 0],
            [1, w + 1, 0, 1, w + 1, 1],
            [w + 1, w + 1, w, w + 1, 1, 1],
        ],
    )
    # M3209
    M = QuaternaryMatroid(
        reduced_matrix=A,
        groundset=['b0', 'a', 'y', 'z', 'x', "c0", 'b', 'c', 'a0']
    )
    M.rename("FN9: " + repr(M))
    return M


def FX9():
    """
    Return the matroid `FX9`.

    An excluded minor for `G`- and `K_2`-representable matroids.
    UPF is `(Q(a,b), <-1,a,b,a-1,b-1,a-b,a+b,a+b-2,a+b-2ab>)`.
    (An excluded minor for `H_2`- and `GF(5)`-representable matroids.)

    EXAMPLES::

        sage: M = matroids.catalog.FX9()
        sage: M.is_valid()
        True

    """
    GF4 = GF(4, 'w')
    w = GF4('w')
    A = Matrix(
        GF4,
        [
            [0, w + 1, 0, w, 1],
            [1, w, 1, w + 1, 1],
            [w + 1, w + 1, w, w + 1, w + 1],
            [w, w, w + 1, w + 1, 1],
        ],
    )
    # M48806
    M = QuaternaryMatroid(reduced_matrix=A)
    M.rename("FX9: " + repr(M))
    return M


def KR9():
    """
    Return the matroid `KR9`.

    An excluded minor for `G`-representable matroids (and
    `GF(5)`-representable matroids.) In a `DY`-equivalence class of `4`
    matroids. Has a
    :func:`KP8 <sage.matroids.database.brettell_matroids.KP8>`-minor (delete
    `8`). UPF is `GF(4)`.

    EXAMPLES::

        sage: KR9 = matroids.catalog.KR9()
        sage: KP8 = matroids.catalog.KP8()
        sage: KP8.is_isomorphic(KR9.delete(8))
        True

    """
    GF4 = GF(4, 'w')
    w = GF4('w')
    A = Matrix(
        GF4,
        [
            [w + 1, w, w + 1, w, 1],
            [0, 1, w + 1, w, 1],
            [w, w + 1, 1, 1, 1],
            [w + 1, w + 1, w, w + 1, 0],
        ],
    )
    M = QuaternaryMatroid(
        reduced_matrix=A, groundset=[2, 4, 0, 6, 1, 5, 3, 7, 8]
    )
    M.rename("KR9: " + repr(M))
    return M


def KQ9():
    """
    Return the matroid `KQ9`.

    An excluded minor for `G`-representable matroids (and
    `GF(5)`-representable matroids.) Has a
    :func:`TQ8 <sage.matroids.database.brettell_matroids.TQ8>`-minor`
    (delete `6`) and a
    :func:`KP8 <sage.matroids.database.brettell_matroids.KP8>`-minor
    (delete `8`). UPF is `GF(4)`.

    EXAMPLES::

        sage: KQ9 = matroids.catalog.KQ9()
        sage: TQ8 = matroids.catalog.TQ8()
        sage: TQ8.is_isomorphic(KQ9.delete(6))
        True
        sage: KP8 = matroids.catalog.KP8()
        sage: KP8.is_isomorphic(KQ9.delete(8))
        True

    """
    GF4 = GF(4, 'w')
    w = GF4('w')
    A = Matrix(
        GF4,
        [
            [w + 1, w, w + 1, 1, w + 1],
            [1, 0, w + 1, w + 1, 1],
            [0, 1, w, w + 1, 1],
            [1, 1, w + 1, 0, w + 1],
        ],
    )
    M = QuaternaryMatroid(
        reduced_matrix=A, groundset=[5, 0, 4, 3, 2, 6, 8, 7, 1]
    )
    M.rename("KQ9: " + repr(M))
    return M


# 10 elements:


def UG10():
    """
    Return the matroid `UG10`.

    An excluded minor for `K_2`- and `P_4`-representable matroids. Self-dual.
    An excluded minor for `H_3`- and `H_2`-representable matroids.
    Uniquely `GF(5)`-representable.
    Although not `P_4`-representable, it is `O`-representable,
    and hence is representable over all fields of size at least four.

    EXAMPLES::

        sage: M = matroids.catalog.UG10()
        sage: M.is_isomorphic(M.dual())
        True

    """
    GF4 = GF(4, 'w')
    w = GF4('w')
    A = Matrix(
        GF4,
        [
            [1, 0, 1, w, w + 1],
            [1, 1, 1, 1, 1],
            [1, 0, w, 1, w + 1],
            [1, w + 1, w, 1, 0],
            [1, 1, 1, 0, 0],
        ],
    )
    M = QuaternaryMatroid(reduced_matrix=A)
    M.rename("UG10: " + repr(M))
    return M


def FF10():
    """
    Return the matroid `FF10`.

    An excluded minor for `K_2`-representable matroids.
    UPF is `P_4`. Self-dual.

    EXAMPLES::

        sage: M = matroids.catalog.FF10()
        sage: M.is_isomorphic(M.dual())
        True

    """
    GF4 = GF(4, 'w')
    w = GF4('w')
    A = Matrix(
        GF4,
        [
            [0, 0, 1, 1, 1],
            [1, 0, 0, 1, 1],
            [1 + w, 1, 0, 0, 1],
            [1, 1, w, 0, 1],
            [1 + w, 1 + w, w, w, 1 + w],
        ],
    )
    M = QuaternaryMatroid(
        reduced_matrix=A, groundset=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    )
    M.rename("FF10: " + repr(M))
    return M


def GP10():
    """
    Return the matroid `GP10`.

    An excluded minor for `K_2`-representable matroids.
    UPF is `G`. Self-dual.

    EXAMPLES::

        sage: M = matroids.catalog.GP10()
        sage: M.is_isomorphic(M.dual())
        True

    """
    GF4 = GF(4, 'w')
    w = GF4('w')
    A = Matrix(
        GF4,
        [
            [w + 1, w, 0, 1, 1],
            [w, w, 0, 0, 1],
            [0, 0, w + 1, w, 1],
            [1, 0, w, 0, 1],
            [1, 1, 1, 1, 0],
        ],
    )
    M = QuaternaryMatroid(reduced_matrix=A)
    M.rename("GP10: " + repr(M))
    return M


def FZ10():
    """
    Return the matroid `FZ10`.

    An excluded minor for `K_2`- and `G`-representable matroids
    (and `H_2`- and `GF(5)`-representable matroids).
    UPF is `W`. Not self-dual.

    EXAMPLES::

        sage: M = matroids.catalog.FZ10()
        sage: M.is_isomorphic(M.dual())
        False

    """
    GF4 = GF(4, 'w')
    w = GF4('w')
    A = Matrix(
        GF4,
        [
            [0, 0, 1, w, 1],
            [1, 0, w, w + 1, w + 1],
            [1, 1, w, w, w],
            [0, 1, 0, w, w],
            [1, 1, w + 1, 1, w],
        ],
    )
    M = QuaternaryMatroid(reduced_matrix=A)
    M.rename("FZ10: " + repr(M))
    return M


def UQ10():
    """
    Return the matroid `UQ10`.

    An excluded minor for `K_2`- and `G`-representable matroids
    (and `H_2`- and `GF(5)`-representable matroids).
    Self-dual. UPF is `(Q(a,b), <-1,a,b,a-1,b-1,a-b,a+b,a+1,ab+b-1,ab-b+1>)`.

    EXAMPLES::

        sage: M = matroids.catalog.UQ10()
        sage: M.is_isomorphic(M.dual())
        True

    """
    GF4 = GF(4, 'w')
    w = GF4('w')
    A = Matrix(
        GF4,
        [
            [0, 0, 1, w, 1],
            [1, 1, 1, 1, 0],
            [1, w + 1, 0, 1, 0],
            [w + 1, w, 0, 0, 1],
            [1, 1, 1, w + 1, 1],
        ],
    )
    M = QuaternaryMatroid(reduced_matrix=A)
    M.rename("UQ10: " + repr(M))
    return M


def FP10():
    """
    Return the matroid `FP10`.

    An excluded minor for `K_2`- and `G`-representable matroids
    (and `H_2`- and `GF(5)`-representable matroids).
    UPF is `U_1^{(2)}`. Self-dual.

    EXAMPLES::

        sage: M = matroids.catalog.FP10()
        sage: M.is_isomorphic(M.dual())
        True

    """
    GF4 = GF(4, 'w')
    w = GF4('w')
    A = Matrix(
        GF4,
        [
            [1, 1, 1, 1, 1],
            [0, 1, 1, 1, 0],
            [w, w, w + 1, 0, 0],
            [0, 1, 1, 0, w],
            [1, w, 1, w, 1],
        ],
    )
    M = QuaternaryMatroid(reduced_matrix=A)
    M.rename("FP10: " + repr(M))
    return M


def TQ10():
    """
    Return the matroid `TQ10`.

    An excluded minor for `K_2`-representable matroids. UPF is `G`. Self-dual.
    Has :func:`TQ8 <sage.matroids.database.brettell_matroids.TQ8>` as a minor
    (delete 'd' and contract 'c').

    EXAMPLES::

        sage: M = matroids.catalog.TQ10()
        sage: M.is_isomorphic(M.dual())
        True
        sage: N = M.delete('d').contract('c')
        sage: N.is_isomorphic(matroids.catalog.TQ8())
        True

    """
    GF4 = GF(4, 'w')
    w = GF4('w')
    A = Matrix(
        GF4,
        [
            [1, w, 0, w + 1, 1],
            [w + 1, w + 1, w + 1, w, 1],
            [w + 1, w, 1, 0, 1],
            [1, 1, 0, w + 1, 0],
            [w + 1, 0, w, w + 1, 0],
        ],
    )
    M = QuaternaryMatroid(
        reduced_matrix=A, groundset=[1, 6, 8, 'c', 3, 7, 'd', 2, 5, 4]
    )
    M.rename("TQ10: " + repr(M))
    return M


def FY10():
    """
    Return the matroid `FY10`.

    An excluded minor for `P_4`-representable matroids. UPF is `G`. Not
    self-dual.

    EXAMPLES::

        sage: M = matroids.catalog.FY10()
        sage: M.is_isomorphic(M.dual())
        False

    """
    GF4 = GF(4, 'w')
    w = GF4('w')
    A = Matrix(
        GF4,
        [
            [1, 1, 1, 0, 0],
            [0, 1, w + 1, 1, 0],
            [1, 1, 1, w + 1, 1],
            [0, 0, w, 1, 1],
            [1, w + 1, 1, 1, w],
        ],
    )
    M = QuaternaryMatroid(reduced_matrix=A)
    M.rename("FY10: " + repr(M))
    return M


def PP10():
    """
    Return the matroid `PP10`.

    An excluded minor for `P_4`-representable matroids. UPF is `U_1^{(2)}`.
    Has a :func:`TQ8 <sage.matroids.database.brettell_matroids.TQ8>`-minor
    (e.g. delete 'a' and contract 'e') and a
    :func:`PP9 <sage.matroids.database.brettell_matroids.PP9>` (and hence
    :func:`P8p <sage.matroids.database.brettell_matroids.P8p>`) minor
    (contract 'x').

    EXAMPLES::

        sage: PP10 = matroids.catalog.PP10()
        sage: M = PP10.delete('a').contract('e')
        sage: M.is_isomorphic(matroids.catalog.TQ8())
        True
        sage: M = PP10.contract('x')
        sage: M.is_isomorphic(matroids.catalog.PP9())
        True

    """
    GF4 = GF(4, 'w')
    w = GF4('w')
    A = Matrix(
        GF4,
        [
            [w + 1, 0, w + 1, 0, w],
            [w, w, 1, w, 1],
            [w + 1, w + 1, 0, w + 1, 1],
            [1, 0, 1, w + 1, 1],
            [w, 1, w + 1, w, w + 1],
        ],
    )
    M = QuaternaryMatroid(
        reduced_matrix=A,
        groundset=['z', 'f', 'c', 'g', 'e', 'b', 'a', 'h', 'd', 'x']
    )
    M.rename("PP10: " + repr(M))
    return M


def FU10():
    """
    Return the matroid `FU10`.

    An excluded minor for `P_4`-representable matroids. UPF is `G`. Self-dual.

    EXAMPLES::

        sage: M = matroids.catalog.FU10()
        sage: M.is_isomorphic(M.dual())
        True

    """
    GF4 = GF(4, 'w')
    w = GF4('w')
    A = Matrix(
        GF4,
        [
            [0, 1, w, 1, 1],
            [w, w + 1, 1, 1, w],
            [1, 1, 0, w + 1, 0],
            [1, 1, 0, w, w + 1],
            [w + 1, w, w + 1, w, 0],
        ],
    )
    M = QuaternaryMatroid(reduced_matrix=A)
    M.rename("FU10: " + repr(M))
    return M


def D10():
    """
    Return the matroid `D10`.

    An excluded minor for `P_4`-representable matroids.
    UPF is `G`. Has a
    :func:`TQ8 <sage.matroids.database.brettell_matroids.TQ8>`-minor.
    In a `DY^*`-equivalence class of `13` matroids.

    EXAMPLES::

        sage: M = matroids.catalog.D10()
        sage: M.has_minor(matroids.catalog.TQ8())
        True

    """
    GF4 = GF(4, 'w')
    w = GF4('w')
    A = Matrix(
        GF4,
        [
            [w, 1, w, 1, w + 1, w],
            [w, 0, w + 1, w + 1, w, w],
            [w + 1, 0, 0, w + 1, w + 1, w + 1],
            [w + 1, 1, 0, 1, w, 0],
        ],
    )
    M = QuaternaryMatroid(reduced_matrix=A)
    M.rename("D10: " + repr(M))
    return M


def UK10():
    """
    Return the matroid `UK10`.

    An excluded minor for `G`-representable matroids
    (and `GF(5)`-representable matroids).
    Not self-dual. UPF is `GF(4)`.

    EXAMPLES::

        sage: M = matroids.catalog.UK10()
        sage: M.is_isomorphic(M.dual())
        False

    """
    GF4 = GF(4, 'w')
    w = GF4('w')
    A = Matrix(
        GF4,
        [
            [1, w, w + 1, w, w + 1],
            [1, w, w, w + 1, w],
            [1, w + 1, w + 1, 0, w],
            [1, 1, w, 0, w],
            [w + 1, 0, 0, 1, w],
        ],
    )
    M = QuaternaryMatroid(reduced_matrix=A)
    M.rename("UK10: " + repr(M))
    return M


def PK10():
    """
    Return the matroid `PK10`.

    An excluded minor for `G`-representable matroids
    (and `GF(5)`-representable matroids).
    Not self-dual. UPF is `GF(4)`.

    EXAMPLES::

        sage: M = matroids.catalog.PK10()
        sage: M.is_isomorphic(M.dual())
        False

    """
    GF4 = GF(4, 'w')
    w = GF4('w')
    A = Matrix(
        GF4,
        [
            [1, 1, w, 0, w + 1],
            [0, 1, 1, 1, 1],
            [w + 1, w, w, w + 1, w],
            [0, 1, w, w + 1, 1],
            [w + 1, w + 1, 0, 0, 1],
        ],
    )
    M = QuaternaryMatroid(reduced_matrix=A)
    M.rename("PK10: " + repr(M))
    return M


def GK10():
    """
    Return the matroid `GK10`.

    An excluded minor for `G`-representable matroids
    (and `GF(5)`-representable matroids).
    Not self-dual. UPF is `GF(4)`.

    EXAMPLES::

        sage: M = matroids.catalog.GK10()
        sage: M.is_isomorphic(M.dual())
        False

    """
    GF4 = GF(4, 'w')
    w = GF4('w')
    A = Matrix(
        GF4,
        [
            [1, 1, 0, 1, 1],
            [1, 0, 0, w, w],
            [w, w + 1, 1, 1, 0],
            [w, w + 1, w + 1, w + 1, w + 1],
            [1, w, w, w + 1, 1],
        ],
    )
    gk10 = QuaternaryMatroid(reduced_matrix=A)
    gk10.rename("GK10: " + repr(gk10))
    return gk10


def FT10():
    """
    Return the matroid `FT10`.

    An excluded minor for `G`-representable matroids
    (and `GF(5)`-representable matroids).
    Self-dual. UPF is `GF(4)`.

    EXAMPLES::

        sage: M = matroids.catalog.FT10()
        sage: M.is_isomorphic(M.dual())
        True

    """
    GF4 = GF(4, 'w')
    w = GF4('w')
    A = Matrix(
        GF4,
        [
            [w, 0, w, w + 1, w + 1],
            [0, 1, w + 1, w, 1],
            [w, 1, 0, w + 1, w + 1],
            [w, 1, 0, 0, w],
            [0, 1, w, 0, 1],
        ],
    )
    M = QuaternaryMatroid(reduced_matrix=A)
    M.rename("FT10: " + repr(M))
    return M


def TK10():
    """
    Return the matroid `TK10`.

    An excluded minor for `G`-representable matroids
    (and `GF(5)`-representable matroids).
    Self-dual. UPF is `GF(4)`.

    EXAMPLES::

        sage: M = matroids.catalog.TK10()
        sage: M.is_isomorphic(M.dual())
        True

    """
    GF4 = GF(4, 'w')
    w = GF4('w')
    A = Matrix(
        GF4,
        [
            [1, 1, 0, 0, w],
            [0, w, 0, w + 1, 1],
            [w + 1, 0, w + 1, w, w + 1],
            [w, 0, 1, 0, w],
            [0, w, 1, w, 0],
        ],
    )
    M = QuaternaryMatroid(reduced_matrix=A)
    M.rename("TK10: " + repr(M))
    return M


def KT10():
    """
    Return the matroid `KT10`.

    An excluded minor for `G`-representable matroids
    (and `GF(5)`-representable matroids).
    Self-dual. UPF is `GF(4)`.

    EXAMPLES::

        sage: M = matroids.catalog.KT10()
        sage: M.is_isomorphic(M.dual())
        True

    """
    GF4 = GF(4, 'w')
    w = GF4('w')
    A = Matrix(
        GF4,
        [
            [0, 1, 1, w, 0],
            [0, 1, 0, w + 1, 1],
            [w + 1, 0, 1, w + 1, w + 1],
            [w, w + 1, w + 1, 1, w],
            [w + 1, w + 1, w + 1, 1, 1],
        ],
    )
    M = QuaternaryMatroid(reduced_matrix=A)
    M.rename("KT10: " + repr(M))
    return M


def TU10():
    """
    Return the matroid `TU10`.

    An excluded minor for `G`-representable matroids
    (and `GF(5)`-representable matroids).
    Self-dual. UPF is `GF(4)`.

    EXAMPLES::

        sage: M = matroids.catalog.TU10()
        sage: M.is_isomorphic(M.dual())
        True

    """
    GF4 = GF(4, 'w')
    w = GF4('w')
    A = Matrix(
        GF4,
        [
            [1, w + 1, 1, 0, w],
            [w, 0, 1, w + 1, w + 1],
            [w, w, w + 1, w + 1, 1],
            [w + 1, 0, w + 1, 1, w + 1],
            [w + 1, w + 1, 1, w, 1],
        ],
    )
    M = QuaternaryMatroid(reduced_matrix=A)
    M.rename("TU10: " + repr(M))
    return M


def UT10():
    """
    Return the matroid `UT10`.

    An excluded minor for `G`-representable matroids
    (and `GF(5)`-representable matroids).
    Self-dual. UPF is `I`.

    EXAMPLES::

        sage: M = matroids.catalog.UT10()
        sage: M.is_isomorphic(M.dual())
        True

    """
    GF4 = GF(4, 'w')
    w = GF4('w')
    A = Matrix(
        GF4,
        [
            [w, w + 1, 0, w + 1, 0],
            [w + 1, w + 1, 1, w, 1],
            [1, 0, 1, w + 1, w + 1],
            [w + 1, w + 1, 1, 1, w],
            [1, w + 1, 1, w, w + 1],
        ],
    )
    M = QuaternaryMatroid(reduced_matrix=A)
    M.rename("UT10: " + repr(M))
    return M


def FK10():
    """
    Return the matroid `FK10`.

    An excluded minor for `G`-representable matroids
    (and `GF(5)`-representable matroids).
    Self-dual. UPF is `GF(4)`.

    EXAMPLES::

        sage: M = matroids.catalog.FK10()
        sage: M.is_isomorphic(M.dual())
        True

    """
    GF4 = GF(4, 'w')
    w = GF4('w')
    A = Matrix(
        GF4,
        [
            [0, 0, 1, 1, w],
            [w, 1, w, 1, 1],
            [1, 1, 0, 0, w + 1],
            [w + 1, 0, w + 1, 0, 1],
            [w + 1, w + 1, 1, 1, w + 1],
        ],
    )
    M = QuaternaryMatroid(reduced_matrix=A)
    M.rename("FK10: " + repr(M))
    return M


def KF10():
    """
    Return the matroid `KF10`.

    An excluded minor for `G`-representable matroids
    (and `GF(5)`-representable matroids).
    Self-dual. UPF is `GF(4)`.

    EXAMPLES::

        sage: M = matroids.catalog.KF10()
        sage: M.is_isomorphic(M.dual())
        True

    """
    GF4 = GF(4, 'w')
    w = GF4('w')
    A = Matrix(
        GF4,
        [
            [w + 1, w + 1, 1, w, 1],
            [0, w + 1, w, 1, 0],
            [0, w, 0, 1, w + 1],
            [w + 1, 0, w, w + 1, 1],
            [w + 1, 1, 0, w + 1, 0],
        ],
    )
    M = QuaternaryMatroid(reduced_matrix=A)
    M.rename("KF10: " + repr(M))
    return M


# 11 elements:


def FA11():
    """
    Return the matroid `FA11`.

    An excluded minor for `P_4`-representable matroids. UPF is `PT`. In a
    `DY^*`-equivalence class of `6` matroids. Has an
    :func:`FF10 <sage.matroids.database.brettell_matroids.FF10>`-minor (delete
    `10`).

    EXAMPLES::

        sage: FA11 = matroids.catalog.FA11()
        sage: FF10 = matroids.catalog.FF10()
        sage: FF10.is_isomorphic(FA11.delete(10))
        True

    """
    GF4 = GF(4, 'w')
    w = GF4('w')
    A = Matrix(
        GF4,
        [
            [w, 0, w, w, 1, 0],
            [1, w, 0, w, w, 1],
            [0, w, 1, w + 1, 0, w],
            [0, w, 0, w + 1, 0, 1],
            [w + 1, w + 1, w + 1, 0, w, 0],
        ],
    )
    M = QuaternaryMatroid(
        reduced_matrix=A, groundset=[1, 3, 4, 2, 8, 7, 9, 0, 5, 10, 6]
    )
    M.rename("FA11: " + repr(M))
    return M


# 12 elements:


def FR12():
    """
    Return the matroid `FR12`.

    An excluded minor for `K_2`-representable matroids.
    UPF is `P_4`. Self-dual.

    EXAMPLES::

        sage: M = matroids.catalog.FR12()
        sage: M.is_isomorphic(M.dual())
        True

    """
    GF4 = GF(4, 'w')
    w = GF4('w')
    A = Matrix(
        GF4,
        [
            [0, 1, 1, 1, 0, 1],
            [1, 1, 1, 0, 1, 1],
            [1, 1, 0, 0, 0, 1],
            [1, 0, 0, 0, w + 1, 1],
            [0, 1, 0, w + 1, 0, 1],
            [1, 1, 1, 1, 1, w + 1],
        ],
    )
    M = QuaternaryMatroid(reduced_matrix=A)
    M.rename("FR12: " + repr(M))
    return M


def GP12():
    """
    Return the matroid `GP12`.

    An excluded minor for `K_2`-representable matroids.
    UPF is `G`. Not self-dual.

    EXAMPLES::

        sage: M = matroids.catalog.GP12()
        sage: M.is_isomorphic(M.dual())
        False

    """
    GF4 = GF(4, 'w')
    w = GF4('w')
    A = Matrix(
        GF4,
        [
            [1 + w, 1 + w, w, 1 + w, 0, 0],
            [1, 0, w, 1 + w, 0, 0],
            [1, 0, 1, 0, 1 + w, 1 + w],
            [1, 1, 0, 1, w, w],
            [1, 0, 1, 1, 0, 1 + w],
            [1, 1, 1, 1, 1, 1 + w],
        ],
    )
    M = QuaternaryMatroid(reduced_matrix=A)
    M.rename("GP12: " + repr(M))
    return M


def FQ12():
    """
    Return the matroid `FQ12`.

    An excluded minor for `P_4`-representable matroids. UPF is `PT`. Has` a
    :func:`PP9 <sage.matroids.database.brettell_matroids.PP9>`-minor (contract
    `4` and `7`, delete `6`) and
    :func:`FF10 <sage.matroids.database.brettell_matroids.FF10>`-minor
    (contract 'c' and delete 'd').

    EXAMPLES::

        sage: FQ12 = matroids.catalog.FQ12()
        sage: PP9 = matroids.catalog.PP9()
        sage: PP9.is_isomorphic(FQ12.contract([4,7]).delete(6))
        True
        sage: FF10 = matroids.catalog.FF10()
        sage: FF10.is_isomorphic(FQ12.contract('c').delete('d'))
        True

    """
    GF4 = GF(4, 'w')
    w = GF4('w')
    A = Matrix(
        GF4,
        [
            [0, 0, w, w, 1, 0],
            [0, 0, w + 1, w + 1, 1, 1],
            [1, 1, w, 1, 1, 1],
            [w, 0, 1, 1, 0, 0],
            [w, w, w + 1, w + 1, 1, 1],
            [0, 1, 1, w, w + 1, 1],
        ],
    )
    M = QuaternaryMatroid(
        reduced_matrix=A, groundset=[7, 4, 5, 9, 2, 1, 0, 6, 'd', 'c', 8, 3]
    )
    M.rename("FQ12: " + repr(M))
    return M


def FF12():
    """
    Return the matroid `FF12`.

    An excluded minor for `P_4`-representable matroids. Self-dual. UPF is
    `(Q(a,b),<-1,a,b,a-2,a-1,a+1,b-1,ab-a+b,ab-a-b,ab-a-2b>)`. Has an
    :func:`FF10 <sage.matroids.database.brettell_matroids.FF10>`-minor
    (contract 'c' and delete 'd').

    EXAMPLES::

        sage: M = matroids.catalog.FF12()
        sage: M.is_isomorphic(M.dual())
        True
        sage: FF10 = matroids.catalog.FF10()
        sage: FF10.is_isomorphic(M.contract('c').delete('d'))
        True

    """
    GF4 = GF(4, 'w')
    w = GF4('w')
    A = Matrix(
        GF4,
        [
            [1, 1, 0, 1, 0, 0],
            [1, 1, w, 1, 0, 1],
            [w, w + 1, 1, 0, 1, 1],
            [1, 1, w, 1, w + 1, 0],
            [1, 1, 0, 0, w + 1, 0],
            [1, w + 1, 1, 0, w + 1, w],
        ],
    )
    M = QuaternaryMatroid(
        reduced_matrix=A, groundset=[0, 4, 'c', 3, 5, 'd', 8, 9, 2, 7, 1, 6]
    )
    M.rename("FF12: " + repr(M))
    return M


def FZ12():
    """
    Return the matroid `FZ12`.

    An excluded minor for `K_2`- and `G`-representable matroids
    (and `H_2`- and `GF(5)`-representable matroids).
    UPF is `W`. Not self-dual.

    EXAMPLES::

        sage: M = matroids.catalog.FZ12()
        sage: M.is_isomorphic(M.dual())
        False

    """
    GF4 = GF(4, 'w')
    w = GF4('w')
    A = Matrix(
        GF4,
        [
            [1, w + 1, 0, w + 1, 0, w + 1],
            [w + 1, w + 1, w, 0, w, 1],
            [w, 1, 0, w, 0, w],
            [w + 1, 1, 1, w + 1, 1, w],
            [w, w, 1, 0, 0, 0],
            [w + 1, 1, 0, w, 1, w],
        ],
    )
    M = QuaternaryMatroid(reduced_matrix=A)
    M.rename("FZ12: " + repr(M))
    return M


def UQ12():
    """
    Return the matroid `UQ12`.

    An excluded minor for `K_2` and `G`-representable matroids
    (and `H2` and `GF(5)`-representable matroids).
    UPF is `P_{pappus}`. Self-dual.

    EXAMPLES::

        sage: M = matroids.catalog.UQ12()
        sage: M.is_isomorphic(M.dual())
        True

    """
    GF4 = GF(4, 'w')
    w = GF4('w')
    A = Matrix(
        GF4,
        [
            [1, 0, 0, w + 1, 1, 0],
            [w + 1, w, w + 1, 1, 1, 1],
            [w + 1, w, w + 1, w + 1, w, 1],
            [1, 0, 0, w, 1, w + 1],
            [1, 0, 1, w, 1, w],
            [1, 1, 1, w, 1, w + 1],
        ],
    )
    M = QuaternaryMatroid(reduced_matrix=A)
    M.rename("UQ12: " + repr(M))
    return M


def FP12():
    """
    Return the matroid `FP12`.

    An excluded minor for `K_2`- and `G`-representable matroids
    (and `H_2`- and `GF(5)`-representable matroids).
    UPF is `W`. Self-dual.

    EXAMPLES::

        sage: M = matroids.catalog.FP12()
        sage: M.is_isomorphic(M.dual())
        True

    """
    GF4 = GF(4, 'w')
    w = GF4('w')
    A = Matrix(
        GF4,
        [
            [0, w + 1, 1, 0, 1, w],
            [0, w + 1, 1, 0, w + 1, 0],
            [w + 1, 1, w, 0, w + 1, w],
            [w, 1, w, 1, w, w + 1],
            [w + 1, 0, w + 1, w, w + 1, 0],
            [w, 0, w + 1, w + 1, w, 0],
        ],
    )
    M = QuaternaryMatroid(reduced_matrix=A)
    M.rename("FP12: " + repr(M))
    return M


def FS12():
    """
    Return the matroid `FS12`.

    An excluded minor for `G`-representable matroids
    (and `GF(5)`-representable matroids).
    Rank `5`. UPF is `GF(4)`.

    EXAMPLES::

        sage: M = matroids.catalog.FS12()
        sage: M.rank()
        5

    """
    GF4 = GF(4, 'w')
    w = GF4('w')
    A = Matrix(
        GF4,
        [
            [1, 1, 1, 1, 1, 0, 1],
            [0, 1, w + 1, w, w + 1, 1, 1],
            [w, w + 1, 0, 0, w + 1, 0, 0],
            [0, 0, w + 1, 0, 0, 1, w],
            [1, 0, w, w, w, 1, 0],
        ],
    )
    M = QuaternaryMatroid(reduced_matrix=A)
    M.rename("FS12: " + repr(M))
    return M


def UK12():
    """
    Return the matroid `UK12`.

    An excluded minor for `G`-representable matroids
    (and `GF(5)`-representable matroids).
    Self-dual. UPF is I.

    EXAMPLES::

        sage: M = matroids.catalog.UK12()
        sage: M.is_isomorphic(M.dual())
        True

    """
    GF4 = GF(4, 'w')
    w = GF4('w')
    A = Matrix(
        GF4,
        [
            [0, w + 1, 1, 0, 0, w],
            [w, 1, w, w + 1, w, w + 1],
            [1, w + 1, w + 1, 0, 0, 0],
            [0, w, 1, 1, w + 1, 1],
            [0, w, 1, 1, 0, w + 1],
            [w, w, w + 1, w, w, 1],
        ],
    )
    M = QuaternaryMatroid(reduced_matrix=A)
    M.rename("UK12: " + repr(M))
    return M


def UA12():
    """
    Return the matroid `UA12`.

    An excluded minor for `G`-representable matroids
    (and `GF(5)`-representable matroids).
    Not self-dual. UPF is `GF(4)`.

    EXAMPLES::

        sage: M = matroids.catalog.UA12()
        sage: M.is_isomorphic(M.dual())
        False

    """
    GF4 = GF(4, 'w')
    w = GF4('w')
    A = Matrix(
        GF4,
        [
            [0, w + 1, w, w + 1, w + 1, 0],
            [1, 1, 1, w + 1, w, 1],
            [1, w + 1, 0, 1, w + 1, 1],
            [0, 0, 0, w + 1, w, 1],
            [0, w + 1, 0, w, w + 1, 1],
            [1, w, w + 1, w + 1, w, 1],
        ],
    )
    M = QuaternaryMatroid(reduced_matrix=A)
    M.rename("UA12: " + repr(M))
    return M


def AK12():
    """
    Return the matroid `AK12`.

    An excluded minor for `G`-representable matroids
    (and `GF(5)`-representable matroids).
    Not self-dual. UPF is `GF(4)`.

    EXAMPLES::

        sage: M = matroids.catalog.AK12()
        sage: M.is_isomorphic(M.dual())
        False

    """
    GF4 = GF(4, 'w')
    w = GF4('w')
    A = Matrix(
        GF4,
        [
            [0, w, 0, 0, w + 1, w],
            [w + 1, w, 0, w, w + 1, w + 1],
            [0, w, w + 1, 0, w, 0],
            [1, 0, w, 0, 0, w + 1],
            [0, 1, 0, 1, 1, 0],
            [1, 0, 1, 1, 0, 1],
        ],
    )
    M = QuaternaryMatroid(reduced_matrix=A)
    M.rename("AK12: " + repr(M))
    return M


def FK12():
    """
    Return the matroid `FK12`.

    An excluded minor for `G`-representable matroids
    (and `GF(5)`-representable matroids). Self-dual.
    UPF is `GF(4)`.

    EXAMPLES::

        sage: M = matroids.catalog.UT10()
        sage: M.is_isomorphic(M.dual())
        True

    """
    GF4 = GF(4, 'w')
    w = GF4('w')
    A = Matrix(
        GF4,
        [
            [w + 1, w, w, 0, w, w + 1],
            [w, 1, 1, w + 1, w + 1, w],
            [1, w + 1, w, 0, w + 1, 0],
            [w, 1, 1, w, w + 1, w + 1],
            [w + 1, w + 1, w, 0, w, 0],
            [1, w, w, w, 1, 1],
        ],
    )
    M = QuaternaryMatroid(reduced_matrix=A)
    M.rename("FK12: " + repr(M))
    return M


def KB12():
    """
    Return the matroid `KB12`.

    An excluded minor for `G`-representable matroids
    (and `GF(5)`-representable matroids). Self-dual.
    UPF is `GF(4)`.

    EXAMPLES::

        sage: M = matroids.catalog.UT10()
        sage: M.is_isomorphic(M.dual())
        True

    """
    GF4 = GF(4, 'w')
    w = GF4('w')
    A = Matrix(
        GF4,
        [
            [1, 0, w, 0, 0, 1],
            [1, w, 0, w, 1, w + 1],
            [1, 1, w + 1, 0, 1, w + 1],
            [w, w, 1, w, 0, 0],
            [1, 1, 1, 0, 0, 0],
            [w, w, 1, w, 1, 1],
        ],
    )
    M = QuaternaryMatroid(reduced_matrix=A)
    M.rename("KB12: " + repr(M))
    return M


def AF12():
    """
    Return the matroid `AF12`.

    An excluded minor for `G`-representable matroids
    (and `GF(5)`-representable matroids). Self-dual.
    UPF is `GF(4)`.

    EXAMPLES::

        sage: M = matroids.catalog.UT10()
        sage: M.is_isomorphic(M.dual())
        True

    """
    GF4 = GF(4, 'w')
    w = GF4('w')
    A = Matrix(
        GF4,
        [
            [1, 0, 0, 0, 1, 1],
            [0, 1, 0, w, w, w + 1],
            [0, 1, 0, 0, w + 1, w + 1],
            [w, 1, 1, 0, 0, 1],
            [0, 1, w + 1, w, w, 1],
            [1, 1, 1, w + 1, w + 1, w],
        ],
    )
    M = QuaternaryMatroid(reduced_matrix=A)
    M.rename("AF12: " + repr(M))
    return M


def NestOfTwistedCubes():
    r"""
    Return the NestOfTwistedCubes matroid.

    A matroid with no `U(2,4)`-detachable pairs (only `\{e_i,f_i\}` pairs are
    detachable).

    EXAMPLES::

        sage: M = matroids.catalog.NestOfTwistedCubes()
        sage: M.is_3connected()
        True

    """
    # utility function
    def complement(groundset, subset):
        return list(set(groundset).difference(subset))

    gs = ["e1", "e2", "e3", "e4", "e5", "e6",
          "f1", "f2", "f3", "f4", "f5", "f6"]
    M = CircuitClosuresMatroid(
        groundset=gs,
        circuit_closures={
            3: [
                ["e1", "e2", "f3", "f4"],
                ["e3", "e4", "f5", "f6"],
                ["e5", "e6", "f1", "f2"],
                ["e4", "e5", "f1", "f3"],
                ["e1", "e3", "f6", "f2"],
                ["e6", "e2", "f4", "f5"],
                ["e2", "e5", "f3", "f6"],
                ["e1", "e4", "f2", "f5"],
                ["e3", "e6", "f1", "f4"],
                ["e5", "e1", "f4", "f6"],
                ["e4", "e6", "f2", "f3"],
                ["e2", "e3", "f5", "f1"],
                ["e2", "e4", "f6", "f1"],
                ["e6", "e1", "f3", "f5"],
                ["e3", "e5", "f2", "f4"],
            ],
            5: [
                complement(gs, ["e1", "e2", "f5", "f6"]),
                complement(gs, ["e3", "e4", "f1", "f2"]),
                complement(gs, ["e5", "e6", "f3", "f4"]),
                complement(gs, ["e4", "e5", "f6", "f2"]),
                complement(gs, ["e1", "e3", "f4", "f5"]),
                complement(gs, ["e6", "e2", "f1", "f3"]),
                complement(gs, ["e2", "e5", "f1", "f4"]),
                complement(gs, ["e1", "e4", "f3", "f6"]),
                complement(gs, ["e3", "e6", "f2", "f5"]),
                complement(gs, ["e5", "e1", "f2", "f3"]),
                complement(gs, ["e4", "e6", "f5", "f1"]),
                complement(gs, ["e2", "e3", "f4", "f6"]),
                complement(gs, ["e2", "e4", "f3", "f5"]),
                complement(gs, ["e6", "e1", "f2", "f4"]),
                complement(gs, ["e3", "e5", "f6", "f1"]),
            ],
            6: [gs],
        },
    )
    return M


# 13 elements:


def XY13():
    """
    Return the matroid `XY13`.

    An excluded minor for `G`-representable matroids
    (and `GF(5)`-representable matroids). UPF is `GF(4)`.

    EXAMPLES::

        sage: M = matroids.catalog.XY13()
        sage: M.is_3connected()
        True

    """
    GF4 = GF(4, 'w')
    w = GF4('w')
    A = Matrix(
        GF4,
        [
            [0, 0, 1, 1, 0, 1, 1],
            [w, 1, w, w + 1, 1, 1, w + 1],
            [0, 0, w + 1, 1, 1, w, 1],
            [0, w, 1, 1, w + 1, 1, 1],
            [w, w + 1, w, w + 1, 1, 1, w],
            [1, 0, 0, 1, 0, w, 0],
        ],
    )
    M = QuaternaryMatroid(reduced_matrix=A)
    M.rename("XY13: " + repr(M))
    return M


# 14 elements:


def N3():
    """
    Return the matroid `N3`.

    An excluded minor for dyadic matroids (and `GF(5)`-representable matroids).
    UPF is `GF(3)`. `4`- (but not `5`-) connected. Self-dual.

    EXAMPLES::

        sage: N3 = matroids.catalog.N3()
        sage: N3.is_isomorphic(N3.dual())
        True
        sage: N3.is_kconnected(4)
        True
        sage: N3.is_kconnected(5)
        False

    """
    A = Matrix(
        GF(3),
        [
            [2, 0, 0, 2, 1, 1, 2],
            [1, 2, 0, 0, 2, 0, 2],
            [0, 1, 2, 1, 0, 0, 2],
            [0, 2, 2, 0, 0, 0, 2],
            [1, 0, 0, 0, 1, 0, 2],
            [2, 0, 0, 1, 2, 1, 1],
            [1, 1, 1, 2, 2, 2, 0],
        ],
    )
    M = TernaryMatroid(reduced_matrix=A)
    M.rename("N3: " + repr(M))
    return M


def N3pp():
    """
    Return the matroid `N3pp`.

    An excluded minor for `K_2`-representable matroids. Self-dual.
    Obtained by relaxing the two complementary circuit-hyperplanes of
    :func:`N4 <sage.matroids.database.brettell_matroids.N4>`. Not
    `P_4`-representable, but `O`-representable, and hence representable
    over all fields of size at least four.

    EXAMPLES::

        sage: M = matroids.catalog.N3pp()
        sage: M.is_isomorphic(M.dual())
        True

    """
    GF4 = GF(4, 'w')
    w = GF4('w')
    A = Matrix(
        GF4,
        [
            [0, 1, 0, 1, 0, w, w],
            [1, w, 1, 0, 1, 0, 1],
            [1, 0, 0, 0, w, w, w],
            [1, 0, 0, 0, 1, 0, 1],
            [1, 1, 1, 0, 1, 0, 0],
            [1, w, 1, w, 1, 1, 1],
            [1, 1, 0, 1, 0, 0, 0],
        ],
    )
    M = QuaternaryMatroid(reduced_matrix=A)
    M.rename("N3=: " + repr(M))
    return M


def UP14():
    """
    Return the matroid `UP14`.

    An excluded minor for `K_2`-representable matroids.
    Has disjoint circuit-hyperplanes.
    UPF is `W`. Not self-dual.

    EXAMPLES::

        sage: M = matroids.catalog.UP14()
        sage: M.is_isomorphic(M.dual())
        False

    """
    GF4 = GF(4, 'w')
    w = GF4('w')
    A = Matrix(
        GF4,
        [
            [1, w, w, 1, w, 0, 0],
            [w, w, w, 1, w, w, 0],
            [w, w, 1, w, 1, 0, 1],
            [1, 1, 0, 1, 0, 0, 0],
            [w, w, 1, w, w, w, 1],
            [0, w, 1, 1, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 1],
        ],
    )
    M = QuaternaryMatroid(reduced_matrix=A)
    M.rename("UP14: " + repr(M))
    return M


def VP14():
    """
    Return the matroid `VP14`.

    An excluded minor for `K_2`-representable matroids.
    Has disjoint circuit-hyperplanes.
    UPF is `W`. Not self-dual.

    EXAMPLES::

        sage: M = matroids.catalog.VP14()
        sage: M.is_isomorphic(M.dual())
        False

    """
    GF4 = GF(4, 'w')
    w = GF4('w')
    A = Matrix(
        GF4,
        [
            [w, 0, 1, 1, w, 1, 1],
            [w, w, 1, 1, w, 1, w],
            [1, 1, 0, 1, 1, w, 0],
            [1, 1, 0, 1, 0, 0, 0],
            [0, 0, 0, w, 0, 1, 1],
            [1, 0, 0, w, 1, 0, 0],
            [1, 1, 1, 1, w, 1, 0],
        ],
    )
    M = QuaternaryMatroid(reduced_matrix=A)
    M.rename("VP14: " + repr(M))
    return M


def FV14():
    """
    Return the matroid `FV14`

    An excluded minor for `P_4`-representable matroids.
    Not self-dual. UPF is `PT`.

    EXAMPLES::

        sage: M = matroids.catalog.FV14()
        sage: M.is_isomorphic(M.dual())
        False

    """
    GF4 = GF(4, 'w')
    w = GF4('w')
    A = Matrix(
        GF4,
        [
            [0, 1, 0, 1, 1, 1, 1],
            [0, 1, 0, 1, 0, 1, 0],
            [1, 0, 0, 1, 1, 1, 1],
            [0, 1 - w, 1, 1, 1 - w, 1 - w, 1],
            [0, 0, 1, 0, 1 - w, -w, 1],
            [1 - w, 0, -1, -w, 0, 0, -w],
            [1, 0, 0, 1, 0, 0, 1],
        ],
    )
    M = QuaternaryMatroid(reduced_matrix=A)
    M.rename("FV14: " + repr(M))
    return M


def OW14():
    """
    Return the matroid `OW14`.

    An excluded minor for `P_4`-representable matroids.
    Self-dual. UPF is `Orthrus`.

    EXAMPLES::

        sage: M = matroids.catalog.OW14()
        sage: M.is_isomorphic(M.dual())
        True

    """
    GF4 = GF(4, 'w')
    w = GF4('w')
    A = Matrix(
        GF4,
        [
            [0, 1, 1, w, 1, 0, w],
            [0, w + 1, 1, w, w + 1, 0, w + 1],
            [0, w + 1, 1, w, 0, w + 1, w + 1],
            [1, 1, w + 1, w + 1, 0, 1, 1],
            [1, 0, 0, w, 0, 0, w],
            [1, 0, 1, 0, 1, 0, 0],
            [0, 1, 0, w, 0, 1, 0],
        ],
    )
    M = QuaternaryMatroid(reduced_matrix=A)
    M.rename("OW14: " + repr(M))
    return M


def FM14():
    """
    Return the matroid `FM14`.

    An excluded minor for `P_4`-representable matroids.
    Self-dual. UPF is `PT`.

    EXAMPLES::

        sage: M = matroids.catalog.FM14()
        sage: M.is_isomorphic(M.dual())
        True

    """
    GF4 = GF(4, 'w')
    w = GF4('w')
    A = Matrix(
        GF4,
        [
            [1, 0, w, 1, 1, w, 0],
            [0, 1, 0, 0, 1, 1, 1],
            [0, 1, 0, 0, w, w, 1],
            [w, 1, 0, w, 0, 1, 1],
            [0, 1, 1, 0, 0, 0, 1],
            [1, w, w, 0, 0, 0, 0],
            [0, w, 0, 1, 0, w, 0],
        ],
    )
    M = QuaternaryMatroid(reduced_matrix=A)
    M.rename("FM14: " + repr(M))
    return M


# 15 elements:


def FA15():
    """
    Return the matroid `FA15`.

    An excluded minor for `O`-representable matroids. UPF is `PT`.
    In a `DY^*`-equivalence class of `6` matroids. Has an
    :func:`SQ14 <sage.matroids.database.brettell_matroids.N3pp>`-minor.

    EXAMPLES::

        sage: M = matroids.catalog.FA15()
        sage: M.has_minor(matroids.catalog.N3pp())
        True

    """
    GF4 = GF(4, 'w')
    w = GF4('w')
    A = Matrix(
        GF4,
        [
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 1, 1, 1, 1, 0, 1],
            [0, 0, 1, 0, 0, 1, 0, 1],
            [0, 0, w, w, 0, 1, 1, 1],
            [1, 1, 0, 0, 0, 0, w, w],
            [w, 0, 1, 1, 1, 1, 0, 0],
            [w, w, 1, 1, 0, 0, 0, 0],
        ],
    )
    M = QuaternaryMatroid(reduced_matrix=A)
    M.rename("FA15: " + repr(M))
    return M


# 16 elements:


def N4():
    """
    Return the matroid `N4`.

    An excluded minor for dyadic matroids (and `GF(5)`-representable matroids).
    UPF is `GF(3)`. `4`- (but not `5`-) connected. Self-dual.

    EXAMPLES::

        sage: N4 = matroids.catalog.N4()
        sage: N4.is_isomorphic(N4.dual())
        True
        sage: N4.is_kconnected(4)
        True
        sage: N4.is_kconnected(5)
        False

    """
    A = Matrix(
        GF(3),
        [
            [2, 0, 2, 1, 2, 1, 0, 0],
            [2, 1, 0, 2, 0, 2, 2, 0],
            [2, 0, 2, 0, 0, 1, 0, 0],
            [2, 0, 2, 2, 2, 2, 2, 2],
            [0, 1, 1, 1, 1, 1, 1, 1],
            [2, 1, 0, 0, 0, 2, 0, 0],
            [2, 0, 0, 2, 2, 2, 2, 0],
            [1, 0, 1, 2, 1, 2, 1, 1],
        ],
    )
    M = TernaryMatroid(reduced_matrix=A)
    M.rename("N4: " + repr(M))
    return M
