r"""
This module contains driver functions to easily access the collections of
matroids in the database. These functions can be viewed by typing ``matroids.``
and hitting the ``tab`` button.

AUTHORS:
- Giorgos Mousa (2023-12-08): initial version

Functions
=========
"""
# **********************************************************************
#       Copyright (C) 2023 Giorgos Mousa <gmousa@proton.me>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#  as published by the Free Software Foundation; either version 2 of
#  the License, or (at your option) any later version.
#                  https://www.gnu.org/licenses/
# **********************************************************************


def AllMatroids(n, r=-1, type="all"):
    """
    Return an iterator of all matroids of certain number of elements
    (and, optionally, of specific rank and type).
    This collection is retrieved from
    Yoshitake Matsumoto's ``Database of Matroids``.

    INPUT:

    - ``n`` -- an integer (1 <= n <= 9).
      The number of elements of the matroids.
    - ``r`` -- (optional) an integer (1 <= r <= n).
      The rank of the matroids.
    - ``type`` -- (default: ``all``) a string.
      The type of the matroids, either ``all``, ``simple``,
      or ``unorientable``.

    OUTPUT:

    an iterator over matroids

    EXAMPLES::

        sage: for M in matroids.AllMatroids(2):
        ....:     M
        allr0n02#0: Matroid of rank 0 on 2 elements with 1 bases
        allr1n02#0: Matroid of rank 1 on 2 elements with 2 bases
        allr1n02#1: Matroid of rank 1 on 2 elements with 1 bases
        allr2n02#0: Matroid of rank 2 on 2 elements with 1 bases
        sage: for M in matroids.AllMatroids(5, 3, "simple"):
        ....:     M
        simpler3n05#0: Matroid of rank 3 on 5 elements with 10 bases
        simpler3n05#1: Matroid of rank 3 on 5 elements with 9 bases
        simpler3n05#2: Matroid of rank 3 on 5 elements with 8 bases
        simpler3n05#3: Matroid of rank 3 on 5 elements with 6 bases

    TESTS::

        sage: all_n = [1, 2, 4, 8, 17, 38, 98, 306, 1724, 383172]
        sage: for i in range(0, 8 + 1):
        ....:     assert len(matroids.AllMatroids(i)) == all_n[i]
        ....:     for M in matroids.AllMatroids(i):
        ....:         assert M.is_valid()
        sage: all = [
        ....:     [   1,    1,    1,    1,    1,    1,    1,    1,     1,      1,     1,      1,    1],
        ....:     [None,    1,    2,    3,    4,    5,    6,    7,     8,      9,    10,     11,   12],
        ....:     [None, None,    1,    3,    7,   13,   23,   37,    58,     87,   128,    183,  259],
        ....:     [None, None, None,    1,    4,   13,   38,  108,   325,   1275, 10037, 298491, None],
        ....:     [None, None, None, None,    1,    5,   23,  108,   940, 190214,  None,   None, None],
        ....:     [None, None, None, None, None,    1,    6,   37,   325, 190214,  None,   None, None],
        ....:     [None, None, None, None, None, None,    1,    7,    58,   1275,  None,   None, None],
        ....:     [None, None, None, None, None, None, None,    1,     8,     87, 10037,   None, None],
        ....:     [None, None, None, None, None, None, None, None,     1,      9,   128, 298491, None],
        ....:     [None, None, None, None, None, None, None, None,  None,      1,    10,    183, None],
        ....:     [None, None, None, None, None, None, None, None,  None,   None,     1,     11,  259],
        ....:     [None, None, None, None, None, None, None, None,  None,   None,  None,      1,   12],
        ....:     [None, None, None, None, None, None, None, None,  None,   None,  None,   None,    1]
        ....: ]
        sage: for r in range(0, 12 + 1): # long time
        ....:     for n in range(r, 12 + 1):
        ....:         if all[r][n] and all[r][n] < 100000:
        ....:             assert len(matroids.AllMatroids(n, r)) == all[r][n]
        ....:             for M in matroids.AllMatroids(n, r):
        ....:                 assert M.is_valid()
        sage: simple = [
        ....:     [   1, None, None, None, None, None, None, None,  None,   None, None,   None, None],
        ....:     [None,    1, None, None, None, None, None, None,  None,   None, None,   None, None],
        ....:     [None, None,    1,    1,    1,    1,    1,    1,     1,      1,    1,      1,    1],
        ....:     [None, None, None,    1,    2,    4,    9,   23,    68,    383, 5249, 232928, None],
        ....:     [None, None, None, None,    1,    3,   11,   49,   617, 185981, None,   None, None]
        ....: ]
        sage: for r in range(0, 4 + 1): # long time
        ....:     for n in range(r, 12 + 1):
        ....:         if simple[r][n] and simple[r][n] < 100000:
        ....:             assert len(matroids.AllMatroids(n, r, "simple")) == simple[r][n]
        ....:             for M in matroids.AllMatroids(n, r, "simple"):
        ....:                 assert M.is_valid() and M.is_simple()
        sage: unorientable = [
        ....:     [1,  3,    18,  201, 9413],
        ....:     [1, 34, 12284, None, None]
        ....: ]
        sage: for r in range(0, 1 + 1): # long time
        ....:     for n in range(0, 4 + 1):
        ....:         if unorientable[r][n]:
        ....:             assert len(matroids.AllMatroids(n + 7, r + 3, "unorientable")) == unorientable[r][n]
        ....:             for M in matroids.AllMatroids(n + 7, r + 3, "unorientable"):
        ....:                 assert M.is_valid()
    """
    from sage.matroids.basis_matroid import BasisMatroid
    from sage.env import SAGE_SRC
    import os

    Matroids = []
    if r == -1:
        for rnk in range(0, n + 1):
            Matroids += AllMatroids(n, rnk, type)
        return Matroids

    if r == 0 or r == n:
        M = BasisMatroid(groundset=range(n), bases=[range(r)])
        M.rename(
            type + "r" + str(r) + "n" + str(n).zfill(2) + "#" + '0'
            + ": " + repr(M)
        )
        Matroids += [M]
        return Matroids

    rp = min(r, n - r) if (type == "all") else r
    filename = os.path.join(
        SAGE_SRC, "sage", "matroids", "database", "yoshitake_matsumoto",
        type + "_matroids",
        type + "r" + str(rp) + "n" + str(n).zfill(2) + ".txt"
    )  # type: ignore
    fin = open(filename, "r")

    import itertools
    perms = list(itertools.combinations(range(n), rp))
    perms.reverse()
    cnt = 0
    while True:
        line = fin.readline()
        if not line:
            break

        B, i = [], 0
        for b in perms[::1]:
            if line[i] == '*':
                B.append(list(b))
            i += 1

        M = BasisMatroid(groundset=range(n), bases=B)
        if type == "all" and n - r < r:
            M = M.dual()
        M.rename(
            type + "r" + str(r) + "n" + str(n).zfill(2) + "#" + str(cnt)
            + ": " + repr(M)
        )
        Matroids += [M]
        cnt += 1

    fin.close()
    return Matroids


def OxleyMatroids():
    """
    Return an iterator of (nonparameterized) matroids as listed in the
    Appendix ``Some Interesting Matroids`` in [Oxl2011]_.

    EXAMPLES::

        sage: for M in matroids.OxleyMatroids(): # long time
        ....:     assert M.is_valid()
    """
    Matroids = []
    from sage.matroids.database.oxley_matroids import (
        U24, U25, U35, K4, Whirl3, Q6, P6, U36, R6,
        Fano, FanoDual, NonFano, NonFanoDual, O7, P7,
        AG32, AG32prime, R8, F8, Q8, L8, S8, Vamos, T8, J, P8, P8pp,
        Wheel4, Whirl4,
        K33dual, K33, AG23, TernaryDowling3, Pappus, NonPappus,
        K5, K5dual, R10,  # NonDesargues,
        R12,  # S_5_6_12,
        T12,
        PG23
    )

    lst = {
        4: [U24],
        5: [U25, U35],
        6: [K4, Whirl3, Q6, P6, U36, R6],
        7: [Fano, FanoDual, NonFano, NonFanoDual, O7, P7],
        8: [
            AG32, AG32prime,
            R8, F8, Q8, L8, S8,
            Vamos, T8, J, P8, P8pp,
            Wheel4, Whirl4
        ],
        9: [K33dual, K33, AG23, TernaryDowling3, Pappus, NonPappus],
        10: [K5, K5dual, R10],
        12: [R12, T12],
        13: [PG23],
    }
    for i in lst:
        for M in lst[i]:
            Matroids.append(M())
    return Matroids


def BrettellMatroids():
    """
    Return an iterator of interesting matroids as listed in [].

    EXAMPLES::

        sage: for M in matroids.BrettellMatroids(): # long time
        ....:     assert M.is_valid()
    """
    Matroids = []
    from sage.matroids.database.brettell_matroids import (
        RelaxedNonFano, TippedFree3spike,
        AG23minusDY, TQ8, P8p, KP8, Sp8, Sp8pp, LP8, WQ8,
        BB9, TQ9, TQ9p, M8591, PP9, BB9gDY, A9, FN9, FX9, KR9, KQ9,
        UG10, FF10, GP10, FZ10, UQ10, FP10, TQ10, FY10, PP10, FU10, D10, UK10,
        PK10, GK10, FT10, TK10, KT10, TU10, UT10, FK10, KF10,
        FA11,
        FR12, GP12, FQ12, FF12, FZ12, UQ12, FP12, FS12, UK12, UA12, AK12,
        FK12, KB12, AF12, NestOfTwistedCubes,
        XY13,
        N3, N3pp, UP14, VP14, FV14, OW14, FM14,
        FA15,
        N4
    )

    lst = {
        7: [RelaxedNonFano, TippedFree3spike],
        8: [AG23minusDY, TQ8, P8p, KP8, Sp8, Sp8pp, LP8, WQ8],
        9: [BB9, TQ9, TQ9p, M8591, PP9, BB9gDY, A9, FN9, FX9, KR9, KQ9],
        10: [
            UG10, FF10, GP10, FZ10, UQ10, FP10, TQ10, FY10, PP10, FU10, D10,
            UK10, PK10, GK10, FT10, TK10, KT10, TU10, UT10, FK10, KF10
        ],
        11: [FA11],
        12: [
            FR12, GP12, FQ12, FF12, FZ12, UQ12, FP12, FS12, UK12, UA12, AK12,
            FK12, KB12, AF12, NestOfTwistedCubes
        ],
        13: [XY13],
        14: [N3, N3pp, UP14, VP14, FV14, OW14, FM14],
        15: [FA15],
        16: [N4],
    }
    for i in lst:
        for M in lst[i]:
            Matroids.append(M())
    return Matroids


def VariousMatroids():
    """
    Return an iterator of various other named matroids.

    EXAMPLES::

        sage: for M in matroids.VariousMatroids(): # long time
        ....:     assert M.is_valid()
    """
    Matroids = []
    from sage.matroids.database.various_matroids import (
        NonVamos, NotP8, AG23minus,
        P9, R9A, R9B, Block_9_4, TicTacToe,
        N1, Block_10_5, Q10,
        BetsyRoss,
        N2, ExtendedTernaryGolayCode,
        D16, Terrahawk,
        ExtendedBinaryGolayCode
    )

    lst = {
        8: [NonVamos, NotP8, AG23minus],
        9: [P9, R9A, R9B, Block_9_4, TicTacToe],
        10: [N1, Block_10_5, Q10],
        11: [BetsyRoss],
        12: [N2, ExtendedTernaryGolayCode],
        16: [D16, Terrahawk],
        24: [ExtendedBinaryGolayCode],
    }
    for i in lst:
        for M in lst[i]:
            Matroids.append(M())
    return Matroids
