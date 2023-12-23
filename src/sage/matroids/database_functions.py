r"""
Collections of matroids

This module contains functions that access the collections of matroids in the
database. Each of these functions returns a complete list of the
nonparametrized matroids from the corresponding collection. These functions
can be viewed by typing ``matroids.`` + :kbd:`Tab`.

AUTHORS:

- Giorgos Mousa (2023-12-08): initial version

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


def AllMatroids(n, r=-1, type="all"):
    r"""
    Return a list of all matroids of certain number of elements (and,
    optionally, of specific rank and type).

    INPUT:

    - ``n`` -- an integer; the number of elements of the matroids
    - ``r`` -- an integer (optional, `0 \le r \le n`); the rank of the matroids
    - ``type`` -- a string (default: ``all``); the type of the matroids.
      Either ``all``, ``simple``, or ``unorientable``. If the type is set to
      ``simple``, or ``unorientable``, then the rank must be specified.

    OUTPUT:

    a list of matroids

    EXAMPLES::

        sage: for M in matroids.AllMatroids(2):
        ....:     M
        all_n02_r00_#0: Matroid of rank 0 on 2 elements with 1 bases
        all_n02_r01_#0: Matroid of rank 1 on 2 elements with 2 bases
        all_n02_r01_#1: Matroid of rank 1 on 2 elements with 1 bases
        all_n02_r02_#0: Matroid of rank 2 on 2 elements with 1 bases
        sage: for M in matroids.AllMatroids(5, 3, "simple"):
        ....:     M
        simple_n05_r03_#0: Matroid of rank 3 on 5 elements with 10 bases
        simple_n05_r03_#1: Matroid of rank 3 on 5 elements with 9 bases
        simple_n05_r03_#2: Matroid of rank 3 on 5 elements with 8 bases
        simple_n05_r03_#3: Matroid of rank 3 on 5 elements with 6 bases

    REFERENCES:

    This collection was retrieved from Yoshitake Matsumoto's Database of
    Matroids, see [Mat2012]_.

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
        ....:         if all[r][n] and all[r][n] < 1000:
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
        ....:         if simple[r][n] and simple[r][n] < 1000:
        ....:             assert len(matroids.AllMatroids(n, r, "simple")) == simple[r][n]
        ....:             for M in matroids.AllMatroids(n, r, "simple"):
        ....:                 assert M.is_valid() and M.is_simple()
        sage: unorientable = [
        ....:     [1,  3,    18,  201, 9413],
        ....:     [1, 34, 12284, None, None]
        ....: ]
        sage: for r in range(0, 1 + 1): # long time
        ....:     for n in range(0, 4 + 1):
        ....:         if unorientable[r][n] and unorientable[r][n] < 1000:
        ....:             assert len(matroids.AllMatroids(n + 7, r + 3, "unorientable")) == unorientable[r][n]
        ....:             for M in matroids.AllMatroids(n + 7, r + 3, "unorientable"):
        ....:                 assert M.is_valid()

    """
    from sage.matroids.constructor import Matroid
    from sage.env import SAGE_EXTCODE
    import os

    Matroids = []
    if r == -1:
        for rnk in range(0, n + 1):
            Matroids += AllMatroids(n, rnk, type)
        return Matroids

    if r == 0 or r == n:
        M = Matroid(groundset=range(n), bases=[range(r)])
        M.rename(
            type + "_n" + str(n).zfill(2) + "_r" + str(r).zfill(2) + "_#"
            + "0" + ": " + repr(M)
        )
        Matroids += [M]
        return Matroids

    rp = min(r, n - r) if (type == "all") else r
    file = os.path.join(
        str(SAGE_EXTCODE), "matroids", "database",
        type + "_matroids",
        type + "r" + str(rp) + "n" + str(n).zfill(2) + ".txt"
    )  # type: ignore
    fin = open(file, "r")

    cnt = 0
    while True:
        line = fin.readline()
        if not line:
            break

        M = Matroid(groundset=range(n), rank=rp, revlex=line[:-1])

        if type == "all" and n - r < r:
            M = M.dual()
        M.rename(
            type + "_n" + str(n).zfill(2) + "_r" + str(r).zfill(2) + "_#"
            + str(cnt) + ": " + repr(M)
        )
        Matroids += [M]
        cnt += 1

    fin.close()
    return Matroids


def OxleyMatroids():
    """
    Return the list of Oxley's matroids.

    EXAMPLES::

        sage: OM = matroids.OxleyMatroids(); len(OM)
        44
        sage: import random
        sage: M = random.choice(OM)
        sage: M.is_valid()
        True

    .. SEEALSO::

        :mod:`Matroid catalog <sage.matroids.matroids_catalog>`, under
        ``Oxley's matroid collection``.

    REFERENCES:

    These matroids are the nonparametrized matroids that appear in the
    Appendix ``Some Interesting Matroids`` in [Oxl2011]_ (p. 639-64).

    TESTS::

        sage: for M in matroids.OxleyMatroids():
        ....:     assert M.is_valid()

    """
    Matroids = []
    from sage.matroids.database_matroids import (
        U24, U25, U35, K4, Whirl3, Q6, P6, U36, R6,
        Fano, FanoDual, NonFano, NonFanoDual, O7, P7,
        AG32, AG32prime, R8, F8, Q8, L8, S8, Vamos, T8, J, P8, P8pp,
        Wheel4, Whirl4,
        K33dual, K33, AG23, TernaryDowling3, R9, Pappus, NonPappus,
        K5, K5dual, R10, NonDesargues,
        R12, ExtendedTernaryGolayCode, T12,
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
        9: [K33dual, K33, AG23, TernaryDowling3, R9, Pappus, NonPappus],
        10: [K5, K5dual, R10, NonDesargues],
        12: [R12, ExtendedTernaryGolayCode, T12],
        13: [PG23],
    }
    for i in lst:
        for M in lst[i]:
            Matroids.append(M())
    return Matroids


def BrettellMatroids():
    """
    Return the list of Brettell's matroids.

    EXAMPLES::

        sage: BM = matroids.BrettellMatroids(); len(BM)
        68
        sage: import random
        sage: M = random.choice(BM)
        sage: M.is_valid()
        True

    .. SEEALSO::

        :mod:`Matroid catalog <sage.matroids.matroids_catalog>`, under
        ``Brettell's matroid collection``.

    TESTS::

        sage: for M in matroids.BrettellMatroids():
        ....:     assert M.is_valid()

    """
    Matroids = []
    from sage.matroids.database_matroids import (
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
    Return a list of various other named matroids.

    EXAMPLES::

        sage: VM = matroids.VariousMatroids(); len(VM)
        16
        sage: import random
        sage: M = random.choice(VM)
        sage: M.is_valid()
        True

    .. SEEALSO::

        :mod:`Matroid catalog <sage.matroids.matroids_catalog>`, under
        ``Collection of various matroids``.

    TESTS::

        sage: for M in matroids.VariousMatroids():
        ....:     assert M.is_valid()

    """
    Matroids = []
    from sage.matroids.database_matroids import (
        NonVamos, NotP8, AG23minus,
        P9, R9A, R9B, Block_9_4, TicTacToe,
        N1, Block_10_5, Q10,
        BetsyRoss,
        N2,
        D16, Terrahawk,
        ExtendedBinaryGolayCode
    )

    lst = {
        8: [NonVamos, NotP8, AG23minus],
        9: [P9, R9A, R9B, Block_9_4, TicTacToe],
        10: [N1, Block_10_5, Q10],
        11: [BetsyRoss],
        12: [N2],
        16: [D16, Terrahawk],
        24: [ExtendedBinaryGolayCode],
    }
    for i in lst:
        for M in lst[i]:
            Matroids.append(M())
    return Matroids


def rename_and_relabel(M, name=None, groundset=None):
    """
    Return a renamed and relabeled matroid.

    This is a helper function for easily renaming and relabeling matroids upon
    definition in the context of the database of matroids.

    INPUT:

    - ``M`` -- a matroid
    - ``name`` -- a string (optional)
    - ``groundset`` -- a string (optional)

    OUTPUT:

    a matroid

    """
    if groundset is not None:
        if len(groundset) != len(M.groundset()):
            raise ValueError(
                "The groundset should be of size %s (%s given)." %
                (len(M.groundset()), len(groundset))
            )
        M = M.relabel(dict(zip(M.groundset(), groundset)))

    if name is not None:
        M.rename(name+": " + repr(M))

    return M
