r"""
Multivariate Tropical Polynomial Semirings

This module provides the implementation of parent and element class for 
multivariate tropical polynomials. When working with multivariate case, the
tropical roots is no longer a point. Instead it become a curve in 2d, a
surface in 3d, and a hypersurface in higher dimension.

AUTHORS:

- Verrel Rievaldo Wijaya

EXAMPLES:

Construct multivariate tropical polynomial semirings::

    sage: T = TropicalSemiring(QQ, use_min=False)
    sage: R = PolynomialRing(T, 'a,b')
    sage: R
    Multivarite Tropical Polynomial Semiring in a, b over Rational Field
    
Create an element by inputting a dictionary::

    sage: dict1 = {(1,0):0, (0,1):-1, (1,1):3}
    sage: p1 = R(dict1); p1
    3*a*b + 0*a + (-1)*b

We can also create an element by converting from classical polynomial::

    sage: S.<a,b> = QQ[]
    sage: f = a + b + a*b
    sage: p2 = R(f); p2
    1*a*b + 1*a + 1*b

Some basic arithmetic operations::

    sage: p1 + p2
    3*a*b + 1*a + 1*b
    sage: p1 * p2
    4*a^2*b^2 + 4*a^2*b + 1*a^2 + 4*a*b^2 + 1*a*b + 0*b^2
    sage: T(2) * p1
    5*a*b + 2*a + 1*b
    sage: p1(T(1),T(2))
    6

Let's look at the different result for tropical curve and graph of tropical
polynomial in two variables when the min-plus or max-plus algebra is used:

    sage: T = TropicalSemiring(QQ, use_min=True)
    sage: R = PolynomialRing(T, 'a,b')
    sage: dict1 = {(1,0):0, (0,1):-1, (1,1):3}
    sage: p1 = R(dict1)
    sage: p1.tropical_hypersurface()
    Tropical curve of 3*a*b + 0*a + (-1)*b are 
    [[(t1 - 1, t1), [t1 >= -3], 1]
    [(t1, -3), [t1 <= -4], 1]
    [(-4, t1), [t1 <= -3], 1]]
    sage: plot(p1.tropical_hypersurface())
    sage: p1.plot3d()

    sage: T = TropicalSemiring(QQ, use_min=False)
    sage: R = PolynomialRing(T, 'a,b')
    sage: dict1 = {(1,0):0, (0,1):-1, (1,1):3}
    sage: p1 = R(dict1)
    sage: p1.tropical_hypersurface()
    Tropical curve of 3*a*b + 0*a + (-1)*b are 
    [[(t1 - 1, t1), [t1 <= -3], 1]
    [(t1, -3), [t1 >= -4], 1]
    [(-4, t1), [t1 >= -3], 1]]
    sage: plot(p1.tropical_hypersurface())
    sage: p1.plot3d()

TESTS:

    sage: -p1
    Traceback (most recent call last):
    ...
    ArithmeticError: cannot negate any non-infinite element

REFERENCES:

    - [Bru2013]_
    - [Fil2017]_

"""

# ****************************************************************************
#       Copyright (C) 2024 Verrel Rievaldo Wijaya <verrelrievaldo@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#                  https://www.gnu.org/licenses/
# ****************************************************************************

from sage.rings.polynomial.multi_polynomial import MPolynomial
from sage.rings.polynomial.multi_polynomial_element import MPolynomial_polydict
from sage.structure.parent import Parent
from sage.structure.unique_representation import UniqueRepresentation
from sage.rings.polynomial.polydict import ETuple
from sage.rings.semirings.tropical_variety import TropicalCurve, TropicalVariety
from sage.plot.plot3d.list_plot3d import list_plot3d
from sage.symbolic.ring import SR

class TropicalMPolynomial(MPolynomial_polydict):
    r"""
    Generic multivariate tropical polynomial.

    """

    def plot3d(self):
        """
        Return the 3d plot of ``self``

        OUTPUT: A Graphics3d Object

        EXAMPLE:

            sage: T = TropicalSemiring(QQ, use_min=False)
            sage: R = PolynomialRing(T, 'x,y')
            sage: S.<x,y> = QQ[]
            sage: c1 = 3+2*x+2*y+3*x*y
            sage: dict1 = {(2,0):0, (0,2):0}
            sage: p1 = R(c1) + R(dict1); p1
            0*x^2 + 3*x*y + 2*x + 0*y^2 + 2*y + 3
            sage: p1.plot3d()

        TESTS:

            sage: T = TropicalSemiring(QQ, use_min=True)
            sage: R = PolynomialRing(T, 'x,y,z')
            sage: S.<x,y,z> = QQ[]
            sage: p1 = R(x*y*z)
            sage: p1.plot3d()
            Traceback (most recent call last):
            ...
            NotImplementedError: Can only plot the graph of tropical 
            multivariate polynomial in two variables 

        """
        from sage.arith.srange import srange

        if len(self.parent().variable_names()) == 2:
            axes = self.tropical_hypersurface()._axes()
            xmin, xmax = axes[0][0], axes[0][1]
            ymin, ymax = axes[1][0], axes[1][1]
            step = 0.5
            x_point = srange(xmin-1, xmax+1+step, step)
            y_point = srange(ymin-1, ymax+1+step, step)
            res = []
            T = self.parent().base()
            for x in x_point:
                for y in y_point:
                    val = self(T(x),T(y)).lift()
                    res.append([x,y,val])
            return list_plot3d(res, point_list=True)
        else:
            raise NotImplementedError("Can only plot the graph of tropical" \
                                " multivariate polynomial in two variables")

    def tropical_hypersurface(self):
        r"""
        Return tropical roots of ``self``. In multivariate case, the roots
        can be represented by a tropical hypersurface. For 2 dimensions,
        it is also called a tropical curve

        OUTPUT:

        - tropical_roots -- TropicalCurve object. This object is 
        displayed as list of lists, where the inner list is of the form
        [parametric equation, condition of parameter, order]
        
        EXAMPLES:

        Some examples of tropical curve for tropical polynomials in two 
        variables::

            sage: T = TropicalSemiring(QQ, use_min=False)
            sage: R = PolynomialRing(T, 'x,y')
            sage: dict1 = {(0,0):0, (1,0):0, (0,1):0}
            sage: p1 = R(dict1); p1
            0*x + 0*y + 0
            sage: p1.tropical_hypersurface()
            Tropical curve of 0*x + 0*y + 0 are 
            [[(0, t1), [t1 <= 0], 1]
            [(t1, 0), [t1 <= 0], 1]
            [(t1, t1), [t1 >= 0], 1]]

        ::

            sage: S.<x,y> = QQ[]
            sage: c2 = -1*x^2
            sage: dict2 = {(0,0):0, (1,0):0, (0,2):0}
            sage: p2 = R(c2) + R(dict2); p2
            (-1)*x^2 + 0*x + 0*y^2 + 0
            sage: p2.tropical_hypersurface()
            Tropical curve of (-1)*x^2 + 0*x + 0*y^2 + 0 are 
            [[(0, t1), [t1 <= 0], 1]
            [(t1, 0), [t1 <= 0], 2]
            [(2*t1, t1), [0 <= t1, t1 <= (1/2)], 1]
            [(1, t1), [t1 <= (1/2)], 1]
            [(t1 + 1/2, t1), [(1/2) <= t1], 2]]

        We can also find tropical hypersurface for any tropical polynomials 
        in `n\geq 2` variables:

            sage: T = TropicalSemiring(QQ, use_min=True)
            sage: R = PolynomialRing(T, 'x,y,z')
            sage: S.<x,y,z> = QQ[]
            sage: p1 = R(x*y + (-1/2)*x*z + 4*z^2); p1
            1*x*y + (-1/2)*x*z + 4*z^2
            sage: p1.tropical_hypersurface()
            Tropical hypersurface of 1*x*y + (-1/2)*x*z + 4*z^2 are 
            [[(t1, t2 - 3/2, t2), [t1 - 9/2 <= t2], 1]
            [(2*t1 - t2 + 3, t2, t1), [t2 + 3/2 <= t1], 1]
            [(t1 + 9/2, t2, t1), [t1 <= t2 + 3/2], 1]]

        """
        from sage.symbolic.relation import solve
        from itertools import combinations
        from sage.arith.misc import gcd

        tropical_roots = []
        variables = []
        for name in self.parent().variable_names():
            variables.append(SR.var(name))

        # convert each term to its linear function
        linear_eq = {}
        for key in self.dict():
            eq = 0
            for i,e in enumerate(key):
                eq += variables[i]*e
            eq += self.dict()[key].lift()
            linear_eq[key] = eq

        # checking for all possible combinations of two terms
        for keys in combinations(self.dict(), 2):
            sol = solve(linear_eq[keys[0]]==linear_eq[keys[1]], variables)
            
            # parametric solution of the chosen two terms
            final_sol = []
            for s in sol[0]:
                final_sol.append(s.right())
            xy_interval = []
            xy_interval.append(tuple(final_sol))
            
            # comparing with other terms
            min_max = linear_eq[keys[0]]
            for i,v in enumerate(variables):
                min_max = min_max.subs(v==final_sol[i])
            all_sol_compare = []
            no_solution = False
            for compare in self.dict():
                if compare not in keys:
                    temp_compare = linear_eq[compare]
                    for i, v in enumerate(variables):
                        temp_compare = temp_compare.subs(v==final_sol[i])
                    if self.parent().base()._use_min:
                        sol_compare = solve(min_max < temp_compare, variables)
                    else:
                        sol_compare = solve(min_max > temp_compare, variables)
                    if sol_compare: # if there is solution
                        if isinstance(sol_compare[0], list):
                            if sol_compare[0]:
                                all_sol_compare.append(sol_compare[0][0])
                        else: # solution is unbounded on one side
                            all_sol_compare.append(sol_compare[0])
                    else:
                        no_solution = True
                        break

            # solve the condition for parameter
            if not no_solution:
                parameter = set()
                for sol in all_sol_compare:
                    parameter = parameter.union(set(sol.variables()))
                parameter_solution = solve(all_sol_compare, list(parameter))
                if parameter_solution:
                    xy_interval.append(parameter_solution[0])
                    # calculate order
                    index_diff = []
                    for i in range(len(keys[0])):
                        index_diff.append(abs(keys[0][i]-keys[1][i]))
                    order = gcd(index_diff)
                    xy_interval.append(order)
                    tropical_roots.append(xy_interval)

        if self.parent().ngens() == 2:
            return TropicalCurve(self, tropical_roots)
        else:
            return TropicalVariety(self, tropical_roots)


class TropicalMPolynomialSemiring(UniqueRepresentation, Parent):
    """
    Semiring structure of tropical polynomials in multiple variables
    """

    def __init__(self, base_semiring, names):
        Parent.__init__(self, base=base_semiring, names=names)

    Element = TropicalMPolynomial

    def _element_constructor_(self, x):
        """"
        Convert ``x`` into this tropical multivariate polynomial semiring

        INPUT:

        - ``x`` -- dict or MPolynomial

        """
        C = self.element_class
        new_dict = {}
        if isinstance(x, MPolynomial):
            x = x.dict()
        for key, value in x.items(): # convert each coefficient to tropical
            new_dict[key] = self.base()(value)
        return C(self, new_dict)
    
    def _repr_(self):
        return (f"Multivarite Tropical Polynomial Semiring in {', '.join(self.variable_names())}"
            f" over {self.base_ring().base_ring()}")
    
    def random_element(self):
        """
        Return a random element from this semiring
        """
        from sage.rings.polynomial.polynomial_ring_constructor import \
            PolynomialRing
        R = PolynomialRing(self.base().base_ring(), self.variable_names())
        return self(R.random_element())
    
    def gens(self):
        gens = []
        for v in self.variable_names():
            gen = SR.var(v)
            gens.append(gen)
        return tuple(gens)

    def ngens(self):
        return len(self.variable_names())
        