"""
This file (./sol/nonlinear_doctest.sage) was *autogenerated* from ./sol/nonlinear.tex,
with sagetex.sty version 2011/05/27 v2.3.1.
It contains the contents of all the sageexample environments from this file.
You should be able to doctest this file with:
sage -t ./sol/nonlinear_doctest.sage
It is always safe to delete this file; it is not used in typesetting your
document.

Sage example in ./sol/nonlinear.tex, line 17::

  sage: def intervalgen(f, phi, s, t):
  ....:     assert (f(s) * f(t) < 0), \
  ....:            'Wrong arguments: f(%s) * f(%s) >= 0)'%(s, t)
  ....:     yield s
  ....:     yield t
  ....:     while 1:
  ....:         u = phi(s, t)
  ....:         yield u
  ....:         fu = f(u)
  ....:         if fu == 0:
  ....:             return
  ....:         if fu * f(s) < 0:
  ....:             t = u
  ....:         else:
  ....:             s = u

Sage example in ./sol/nonlinear.tex, line 40::

  sage: f(x) = 4 * x - 1
  sage: a, b = 0, 1
  sage: phi(s, t) = (s + t) / 2
  sage: list(intervalgen(f, phi, a, b))
  [0, 1, 1/2, 1/4]

Sage example in ./sol/nonlinear.tex, line 49::

  sage: from types import GeneratorType, FunctionType
  sage: def checklength(u, v, w, prec):
  ....:     return abs(v - u) < 2 * prec
  sage: def iterate(series,check=checklength,prec=10^-5,maxit=100):
  ....:     assert isinstance(series, GeneratorType)
  ....:     assert isinstance(check, FunctionType)
  ....:     niter = 2
  ....:     v, w = next(series), next(series)
  ....:     while (niter <= maxit):
  ....:         niter += 1
  ....:         u, v, w = v, w, next(series)
  ....:         if check(u, v, w, prec):
  ....:             print('After {0} iterations: {1}'.format(niter, w))
  ....:             return
  ....:     print('Failed after {0} iterations'.format(maxit))

Sage example in ./sol/nonlinear.tex, line 76::

  sage: f(x) = 4 * sin(x) - exp(x) / 2 + 1
  sage: a, b = RR(-pi), RR(pi)
  sage: def phi(s, t): return RR.random_element(s, t)
  sage: random = intervalgen(f, phi, a, b)
  sage: iterate(random, maxit=10000) # random
  After 19 iterations: 2.15848379485564

Sage example in ./sol/nonlinear.tex, line 93::

  sage: basering.<x> = PolynomialRing(SR, 'x')
  sage: p = x^2 + x
  sage: p.roots(multiplicities=False)
  [-1, 0]

Sage example in ./sol/nonlinear.tex, line 101::

  sage: from collections import deque
  sage: basering = PolynomialRing(SR, 'x')
  sage: q, method = None, None
  sage: def quadraticgen(f, r, s):
  ....:     global q, method
  ....:     t = r - f(r) / f.derivative()(r)
  ....:     method = 'newton'
  ....:     yield t
  ....:     pts = deque([(p, f(p)) for p in (r, s, t)], maxlen=3)
  ....:     while True:
  ....:         q = basering.lagrange_polynomial(pts)
  ....:         roots = [r for r in q.roots(multiplicities=False) \
  ....:                          if CC(r).is_real()]
  ....:         approx = None
  ....:         for root in roots:
  ....:             if (root - pts[2][0]) * (root - pts[1][0]) < 0:
  ....:                 approx = root
  ....:                 break
  ....:             elif (root - pts[0][0]) * (root - pts[1][0]) < 0:
  ....:                 pts.pop()
  ....:                 approx = root
  ....:                 break
  ....:         if approx:
  ....:             method = 'quadratic'
  ....:         else:
  ....:             method = 'dichotomy'
  ....:             approx = (pts[1][0] + pts[2][0]) / 2
  ....:         pts.append((approx, f(approx)))
  ....:         yield pts[2][0]

Sage example in ./sol/nonlinear.tex, line 141::

  sage: basering = PolynomialRing(SR, 'x')
  sage: a, b = pi/2, pi
  sage: f(x) = 4 * sin(x) - exp(x) / 2 + 1
  sage: generator = quadraticgen(f, a, b)
  sage: next(generator)
  1/2*pi - (e^(1/2*pi) - 10)*e^(-1/2*pi)
"""
