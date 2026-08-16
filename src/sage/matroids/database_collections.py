r"""
Collections of matroids

This module contains functions that access the collections of matroids in the
database. Each of these functions returns an iterator over the nonparametrized
matroids from the corresponding collection. These functions can be viewed by
typing ``matroids.`` + :kbd:`Tab`.

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


def AllMatroids(r, n, type='all'):
    r"""
    Iterate over all matroids of certain number of elements (and, optionally,
    of specific rank and type).

    INPUT:

    - ``r`` -- integer; the rank of the matroids (`0 \le r`)
    - ``n`` -- integer; the number of elements of the matroids (`\le r \le n`)
    - ``type`` -- string (default: ``'all'``); the type of the matroids. Must
      be one of the following:

      * ``'all'`` -- all matroids; available: (r=*, n=0-9), (r<=3, n=0-12),
        (r=4, n=0-9)
      * ``'unorientable'`` -- all unorientable matroids; the rank `r` must be
        specified; available: (r=3, n=7-11), (r=4, n=7-9)
      * any other type for which there exists an ``is_type`` method;
        availability same as for ``'all'``

    EXAMPLES::

        sage: for r in range(3):
        ....:     for M in matroids.AllMatroids(r, 2):                                  # optional - matroid_database
        ....:         M
        r00n02_all_#0: Matroid of rank 0 on 2 elements with 1 bases
        r01n02_all_#0: Matroid of rank 1 on 2 elements with 2 bases
        r01n02_all_#1: Matroid of rank 1 on 2 elements with 1 bases
        r02n02_all_#0: Matroid of rank 2 on 2 elements with 1 bases

    ::

        sage: for M in matroids.AllMatroids(3, 5, 'simple'):                            # optional - matroid_database
        ....:     M
        r03n05_simple_#0: Matroid of rank 3 on 5 elements with 10 bases
        r03n05_simple_#1: Matroid of rank 3 on 5 elements with 9 bases
        r03n05_simple_#2: Matroid of rank 3 on 5 elements with 8 bases
        r03n05_simple_#3: Matroid of rank 3 on 5 elements with 6 bases

    ::

        sage: for M in matroids.AllMatroids(3, 6, type='paving'):                       # optional - matroid_database
        ....:     M
        r03n06_paving_#0: Matroid of rank 3 on 6 elements with 20 bases
        r03n06_paving_#1: Matroid of rank 3 on 6 elements with 19 bases
        r03n06_paving_#2: Matroid of rank 3 on 6 elements with 18 bases
        r03n06_paving_#3: Matroid of rank 3 on 6 elements with 18 bases
        r03n06_paving_#4: Matroid of rank 3 on 6 elements with 17 bases
        r03n06_paving_#5: Matroid of rank 3 on 6 elements with 16 bases
        r03n06_paving_#6: Matroid of rank 3 on 6 elements with 16 bases
        r03n06_paving_#7: Matroid of rank 3 on 6 elements with 15 bases
        r03n06_paving_#8: Matroid of rank 3 on 6 elements with 10 bases

    ::

        sage: # optional - matroid_database
        sage: for M in matroids.AllMatroids(4, 10):
        ....:     M
        Traceback (most recent call last):
        ...
        ValueError: (r=4, n=10, type='all') is not available in the database
        sage: for M in matroids.AllMatroids(3, 12, 'unorientable'):
        ....:     M
        Traceback (most recent call last):
        ...
        ValueError: (r=3, n=12, type='unorientable') is not available in the database
        sage: for M in matroids.AllMatroids(2, 4, type='nice'):
        ....:     M
        Traceback (most recent call last):
        ...
        AttributeError: The type 'nice' is not available. There needs to be an 'is_nice()'
        attribute for the type to be supported.

    REFERENCES:

    The underlying database was retrieved from Yoshitake Matsumoto's Database
    of Matroids; see [Mat2012]_. It has also been supplemented with the output
    of the `matroid-generator <https://github.com/gmou3/matroid-generator>`_.

    TESTS::

        sage: # optional - matroid_database
        sage: all_n = [1, 2, 4, 8, 17, 38, 98, 306, 1724, 383172]
        sage: for n in range(0, 8 + 1):
        ....:     assert sum(M.is_valid() for r in range(0, n + 1)
        ....:                for M in matroids.AllMatroids(r, n)) == all_n[n]
        sage: all = [
        ....:     [     1,     1,      1,    1,    1,    1,    1,    1,     1,      1,     1,      1,    1],
        ....:     [  None,     1,      2,    3,    4,    5,    6,    7,     8,      9,    10,     11,   12],
        ....:     [  None,  None,      1,    3,    7,   13,   23,   37,    58,     87,   128,    183,  259],
        ....:     [  None,  None,   None,    1,    4,   13,   38,  108,   325,   1275, 10037, 298491, None],
        ....:     [  None,  None,   None, None,    1,    5,   23,  108,   940, 190214,  None,   None, None],
        ....:     [  None,  None,   None, None, None,    1,    6,   37,   325, 190214,  None,   None, None],
        ....:     [  None,  None,   None, None, None, None,    1,    7,    58,   1275,  None,   None, None],
        ....:     [  None,  None,   None, None, None, None, None,    1,     8,     87, 10037,   None, None],
        ....:     [  None,  None,   None, None, None, None, None, None,     1,      9,   128, 298491, None],
        ....:     [  None,  None,   None, None, None, None, None, None,  None,      1,    10,    183, None],
        ....:     [  None,  None,   None, None, None, None, None, None,  None,   None,     1,     11,  259],
        ....:     [  None,  None,   None, None, None, None, None, None,  None,   None,  None,      1,   12],
        ....:     [  None,  None,   None, None, None, None, None, None,  None,   None,  None,   None,    1]
        ....: ]
        sage: for r in range(0, 12 + 1):  # long time
        ....:     for n in range(r, 12 + 1):
        ....:         if all[r][n] and all[r][n] < 1000:
        ....:             assert sum(M.is_valid() for M in matroids.AllMatroids(r, n)) == all[r][n]
        ....:             for M in matroids.AllMatroids(r, n):
        ....:                 assert M.is_valid()
        sage: simple = [
        ....:     [    1,  None,   None, None, None, None, None, None,  None,  None,  None,   None, None],
        ....:     [ None,     1,   None, None, None, None, None, None,  None,  None,  None,   None, None],
        ....:     [ None,  None,      1,    1,    1,    1,    1,    1,     1,     1,     1,      1,    1],
        ....:     [ None,  None,   None,    1,    2,    4,    9,   23,    68,   383,  5249, 232928, None],
        ....:     [ None,  None,   None, None,    1,    3,   11,   49,   617, 185981, None,   None, None]
        ....: ]
        sage: for r in range(0, 4 + 1):  # long time
        ....:     for n in range(r, 12 + 1):
        ....:         if simple[r][n] and simple[r][n] < 1000:
        ....:             assert sum(M.is_valid() and M.is_simple() for M in matroids.AllMatroids(r, n)) == simple[r][n]
        ....:             for M in matroids.AllMatroids(r, n, 'simple'):
        ....:                 assert M.is_valid() and M.is_simple()
        sage: unorientable = [
        ....:     [1,  3,    18,  201, 9413],
        ....:     [1, 34, 12284, None, None]
        ....: ]
        sage: for r in range(0, 1 + 1):  # long time
        ....:     for n in range(0, 4 + 1):
        ....:         if unorientable[r][n] and unorientable[r][n] < 1000:
        ....:             assert sum(M.is_valid() for M in matroids.AllMatroids(r+3, n+7, 'unorientable')) == unorientable[r][n]
        ....:             for M in matroids.AllMatroids(r+3, n+7, 'unorientable'):
        ....:                 assert M.is_valid()
    """
    from sage.matroids.basis_matroid import BasisMatroid
    from sage.features.databases import DatabaseMatroids
    DatabaseMatroids().require()
    import matroid_database

    if type != 'all' and type != 'unorientable':
        try:
            getattr(BasisMatroid, 'is_' + type)
        except AttributeError:
            raise AttributeError(
                "The type '%s' is not available. " % type +
                "There needs to be an 'is_%s()' attribute for the " % type +
                "type to be supported."
            )

    type_db = 'all' if (type != 'unorientable') else 'unorientable'
    matroids_colex = getattr(matroid_database, type_db + '_matroids_colex')

    try:
        matroids_colex(r, n).__next__()
    except ValueError:
        raise ValueError(
            "(r=%s, n=%s, type='%s')" % (r, n, type)
            + " is not available in the database"
        )

    cnt = 0
    for colex in matroids_colex(r, n):
        M = BasisMatroid(rank=r, groundset=range(n), colex=colex)
        M.rename(f'r{r:02d}n{n:02d}_{type}_#{cnt}: {repr(M)}')
        if type == 'all' or type == 'unorientable':
            yield M
            cnt += 1
        else:
            f = getattr(M, 'is_' + type)
            if f():
                yield M
                cnt += 1


def OxleyMatroids():
    """
    Iterate over Oxley's matroid collection.

    EXAMPLES::

        sage: OM = list(matroids.OxleyMatroids()); len(OM)
        44
        sage: import random
        sage: M = random.choice(OM)
        sage: M.is_valid()
        True

    .. SEEALSO::

        :mod:`Matroid catalog <sage.matroids.matroids_catalog>`, under
        ``Oxley's matroid collection``.

    REFERENCES:

    These matroids are the nonparametrized matroids that appear in the Appendix
    ``Some Interesting Matroids`` in [Oxl2011]_ (p. 639-64).
    """
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

    lst = [U24,  # 4
           U25, U35,  # 5
           K4, Whirl3, Q6, P6, U36, R6,  # 6
           Fano, FanoDual, NonFano, NonFanoDual, O7, P7,  # 7
           AG32, AG32prime,
           R8, F8, Q8, L8, S8,
           Vamos, T8, J, P8, P8pp,
           Wheel4, Whirl4,  # 8
           K33dual, K33, AG23, TernaryDowling3, R9, Pappus, NonPappus,  # 9
           K5, K5dual, R10, NonDesargues,  # 10
           R12, ExtendedTernaryGolayCode, T12,  # 12
           PG23]  # 13
    for M in lst:
        yield M()


def BrettellMatroids():
    """
    Iterate over Brettell's matroid collection.

    EXAMPLES::

        sage: BM = list(matroids.BrettellMatroids()); len(BM)
        68
        sage: import random
        sage: M = random.choice(BM)
        sage: M.is_valid()
        True

    .. SEEALSO::

        :mod:`Matroid catalog <sage.matroids.matroids_catalog>`, under
        ``Brettell's matroid collection``.
    """
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

    lst = [RelaxedNonFano, TippedFree3spike,  # 7
           AG23minusDY, TQ8, P8p, KP8, Sp8, Sp8pp, LP8, WQ8,  # 8
           BB9, TQ9, TQ9p, M8591, PP9, BB9gDY, A9, FN9, FX9, KR9, KQ9,  # 9
           UG10, FF10, GP10, FZ10, UQ10, FP10, TQ10, FY10, PP10, FU10, D10,
           UK10, PK10, GK10, FT10, TK10, KT10, TU10, UT10, FK10, KF10,  # 10
           FA11,  # 11
           FR12, GP12, FQ12, FF12, FZ12, UQ12, FP12, FS12, UK12, UA12, AK12,
           FK12, KB12, AF12, NestOfTwistedCubes,  # 12
           XY13,  # 13
           N3, N3pp, UP14, VP14, FV14, OW14, FM14,  # 14
           FA15,  # 15
           N4]  # 16
    for M in lst:
        yield M()


def VariousMatroids():
    """
    Iterate over various other named matroids.

    EXAMPLES::

        sage: VM = list(matroids.VariousMatroids()); len(VM)
        16
        sage: import random
        sage: M = random.choice(VM)
        sage: M.is_valid()
        True

    .. SEEALSO::

        :mod:`Matroid catalog <sage.matroids.matroids_catalog>`, under
        ``Collection of various matroids``.
    """
    from sage.matroids.database_matroids import (
        NonVamos, NotP8, AG23minus,
        P9, R9A, R9B, Block_9_4, TicTacToe,
        N1, Block_10_5, Q10,
        BetsyRoss,
        N2,
        D16, Terrahawk,
        ExtendedBinaryGolayCode
    )

    lst = [NonVamos, NotP8, AG23minus,  # 8
           P9, R9A, R9B, Block_9_4, TicTacToe,  # 9
           N1, Block_10_5, Q10,  # 10
           BetsyRoss,  # 11
           N2,  # 12
           D16, Terrahawk,  # 16
           ExtendedBinaryGolayCode]  # 24
    for M in lst:
        yield M()
