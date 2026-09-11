"""
Matroid Realization Space
=========================

SageMath translation of the OSCAR (Julia) matroid realization space module.
"""
from collections import Counter, defaultdict
from cysignals.alarm import alarm, cancel_alarm, AlarmInterrupt
from itertools import combinations
from sage.all import (
    ZZ, QQ, GF,
    PolynomialRing,
    matrix, zero_matrix,
    gcd, lcm,
)
from sage.arith.misc import is_prime, is_prime_power
from sage.graphs.graph import Graph
from sage.matroids.utilities import cmp_elements_key
from sage.rings.polynomial.multi_polynomial_ring_base import MPolynomialRing_base
from sage.rings.polynomial.polynomial_ring import PolynomialRing_general
from sage.rings.ring import Fields
import json
import operator


def _is_poly_ring(R):
    """True if R is a multivariate or univariate polynomial ring."""
    return isinstance(R, (MPolynomialRing_base, PolynomialRing_general))


def _change_ring(f, R):
    if hasattr(f, 'change_ring'):
        return f.change_ring(R.base_ring())
    return R(f)

# ---------------------------------------------------------------------------
# MatroidRealizationSpace
# ---------------------------------------------------------------------------


class MatroidRealizationSpace:
    """
    Represents the realization space of a matroid.

    Attributes
    ----------
    defining_ideal     : sage Ideal
    inequations        : list of ring elements — must all be nonzero in any realization
    ambient_ring       : polynomial ring (or base field/ring when no free variables remain)
    realization_matrix : matrix over ambient_ring, or None
    char               : characteristic (int or None)
    q                  : prime-power field size (int or None)
    ground_ring        : ZZ, QQ, GF(p), …
    one_realization    : bool — True when this records a single concrete realization
    """

    def __init__(self, basis, defining_ideal, inequations, ambient_ring,
                 realization_matrix, char, q, ground_ring):
        self.basis = frozenset(basis)
        self.defining_ideal = defining_ideal
        self.inequations = list(inequations)
        self.ambient_ring = ambient_ring
        self.realization_matrix = realization_matrix
        self.char = char
        self.q = q
        self.ground_ring = ground_ring
        self.one_realization = False
        self._is_realizable = None   # cached tri-state: None / True / False

    # ------------------------------------------------------------------
    # Pretty printing
    # ------------------------------------------------------------------

    def __repr__(self):
        lines = []
        if self._is_realizable is False:
            if self.char is None and self.q is None:
                return "The matroid is not realizable."
            return "The matroid is not realizable over the specified field or characteristic."

        if self.one_realization:
            lines.append("One realization is given by")
        elif self._is_realizable is True:
            lines.append("The realizations are parametrized by")
        else:
            lines.append("The realization space is")

        if self.realization_matrix is not None:
            lines.append(str(self.realization_matrix))
        lines.append("in " + str(self.ambient_ring))

        I = self.defining_ideal
        if I is not None and not I.is_zero():
            lines.append("within the vanishing set of the ideal")
            lines.append(str(I))

        if self.inequations:
            lines.append("avoiding the zero loci of the polynomials")
            lines.append(str(self.inequations))

        return "\n".join(lines)

    # ------------------------------------------------------------------
    # Realizability
    # ------------------------------------------------------------------

    def is_realizable(self):
        """
        Determine whether this realization space is non-empty over some field,
        i.e. whether the matroid is realizable over some field.
        """
        if self._is_realizable is not None:
            return self._is_realizable

        I = self.defining_ideal
        ineqs = self.inequations

        if not _is_poly_ring(self.ambient_ring):
            if I.is_one():
                self._is_realizable = False
            elif I.is_zero():
                self._is_realizable = all(f != 0 for f in ineqs)
            else:
                n = gcd(I.gens())
                self._is_realizable = any(
                    all(GF(p)(f) != 0 for f in ineqs) for p, _ in n.factor())
            return self._is_realizable

        for p in I.minimal_associated_primes():
            if all(p.reduce(ineq) != 0 for ineq in ineqs):
                self._is_realizable = True
                return True

        self._is_realizable = False
        return False

    def concrete_realization(self, q):
        r"""
        Return a concrete ``MatroidRealizationSpace`` over `GF(q)`.

        A return value of ``None`` signifies that the matroid is not
        `q`-realizable.
        """
        p, _ = is_prime_power(q, get_data=True)
        if self.char is not None and self.char != 0 and self.char != p:
            raise ValueError(f"q={q} has characteristic {p}, but the realization "
                             f"space requires characteristic {self.char}")

        F = GF(q)
        zero = F(0)
        R = (self.ambient_ring.change_ring(F)
             if hasattr(self.ambient_ring, 'change_ring') else F)
        gens = R.gens()

        def raw_terms(g):
            if not hasattr(g, 'dict'):
                return [((0,) * len(gens), g)]
            return list(g.dict().items())

        gens_raw_terms = [raw_terms(g) for g in self.defining_ideal.gens()]
        ineqs_raw_terms = [raw_terms(g) for g in self.inequations]

        appearance_by_index = [0] * len(gens)
        for terms in gens_raw_terms + ineqs_raw_terms:
            seen = set()
            for exp, _ in terms:
                for j, e in enumerate(exp):
                    if e != 0:
                        seen.add(j)
            for j in seen:
                appearance_by_index[j] += 1

        order = sorted(range(len(gens)), key=lambda j: (-appearance_by_index[j], str(gens[j])))
        variables = [gens[j] for j in order]
        n = len(variables)
        var_index = {v: i for i, v in enumerate(variables)}
        domains = [list(F) for _ in range(n)]
        raw_to_sorted = [var_index[gens[j]] for j in range(len(gens))]

        def terms_from_raw(raw_terms_list):
            """Build (sorted-index exponent dict, F coefficient) pairs from an
            already-extracted raw term list -- no second g.dict() call."""
            terms = []
            for exp, c in raw_terms_list:
                e = {raw_to_sorted[j]: exp[j] for j in range(len(gens)) if exp[j] != 0}
                terms.append((e, F(c)))
            return terms

        rels_terms = [(terms_from_raw(t), operator.eq) for t in gens_raw_terms]
        rels_terms.extend([(terms_from_raw(t), operator.ne) for t in ineqs_raw_terms])

        def return_rs(subs):
            A = self.realization_matrix
            if A is not None:
                A = A.change_ring(R).subs(subs).change_ring(F)
            RS_q = MatroidRealizationSpace(self.basis, F.ideal(zero), [],
                                           F, A, p, q, F)
            RS_q.one_realization = True
            RS_q._is_realizable = True
            return RS_q

        if not _is_poly_ring(R):
            def as_constant(terms):
                return sum((c for _, c in terms), zero)
            if not all(op(as_constant(terms), zero) for terms, op in rels_terms):
                return None
            return return_rs({})

        rels_with_supp = []
        for terms, op in rels_terms:
            supp = set()
            for e, _ in terms:
                supp.update(e.keys())
            rels_with_supp.append((terms, op, supp))

        def prune(terms, op, supp):
            if not supp:
                c = terms[0][1] if terms else zero
                return None if not op(c, zero) else []
            if len(supp) == 1:
                i = next(iter(supp))
                def eval_at(val):
                    total = zero
                    for e, coeff in terms:
                        total += coeff * val ** e.get(i, 0)
                    return total
                domains[i] = [c for c in domains[i] if op(eval_at(c), zero)]
                return []
            return [(terms, op, supp)]

        if not all(domains):
            return None

        # Encode and manipulate raw polynomials to avoid using the slow
        # `f.subs` method in the inner loop of backtrack
        def compile_terms(f):
            terms = []
            exps = f.exponents()
            coeffs = f.coefficients()
            for exp, coeff in zip(exps, coeffs):
                e = {raw_to_sorted[j]: ej for j, ej in enumerate(exp) if ej != 0}
                terms.append((e, coeff))
            return terms

        def group_by_pivot(terms, k):
            """Return a dict mapping pivot exponent to list of
            (exponent_dict, coeff) pairs."""
            groups = defaultdict(list)
            for e, coeff in terms:
                pv = e.get(k, 0)
                rest = [(idx, pw) for idx, pw in e.items() if idx != k]
                groups[pv].append((rest, coeff))
            return groups

        reduced_rels = []
        for terms, op, supp in rels_with_supp:
            res = prune(terms, op, supp)
            if res is None:
                return None
            reduced_rels.extend(res)

        rels_by_level = defaultdict(list)
        for terms, op, supp in reduced_rels:
            k = max(supp)
            groups = group_by_pivot(terms, k)
            max_p = max(groups)
            coeff_buf = [zero] * (max_p + 1)
            rels_by_level[k].append((groups, max_p, op, coeff_buf))

        for k in rels_by_level:
            rels_by_level[k].sort(key=lambda r: r[1])  # ascending max_p

        subs = [None] * n

        def backtrack(k, subs):
            if k == n:
                return subs
            candidates = domains[k]
            for groups, max_p, op, coeff_buf in rels_by_level[k]:
                if not candidates:
                    break
                for i in range(max_p + 1):
                    coeff_buf[i] = zero
                for pw, terms in groups.items():
                    # compute coeff of univariate poly
                    s = zero
                    for rest, coeff in terms:
                        term = coeff
                        for idx, pw2 in rest:
                            term *= subs[idx] if pw2 == 1 else subs[idx] ** pw2
                        s += term
                    coeff_buf[max_p - pw] = s
                new_candidates = []
                for val in candidates:
                    # evaluate univariate poly and check result
                    result = coeff_buf[0]
                    for i in range(1, max_p + 1):
                        result = result * val + coeff_buf[i]
                    if op(result, zero):
                        new_candidates.append(val)
                candidates = new_candidates
            for val in candidates:
                subs[k] = val
                res = backtrack(k + 1, subs)
                if res is not None:
                    return res
            return None

        subs = backtrack(0, subs)
        if subs is None:
            return None
        return return_rs({variables[k]: subs[k] for k in range(n)})

# ---------------------------------------------------------------------------
# Factorisation helpers
# ---------------------------------------------------------------------------


_factor_cache = {}


def _factor_cached(f):
    try:
        ring_key = str(f.parent())
    except Exception:
        ring_key = ""
    key = (ring_key, str(f))
    if key not in _factor_cache:
        _factor_cache[key] = f.factor()
    return _factor_cache[key]


def _normalize_poly(f):
    """Normalize polynomial to have positive leading coefficient."""
    try:
        lc = f.lc()
        if lc < 0:
            return -f
        return f
    except Exception:
        return f


def _gens_prime_divisors(polys):
    result = []
    for f in polys:
        if f == 0:
            continue
        for p, _ in _factor_cached(f):
            normalized = _normalize_poly(p)
            if normalized not in result:
                result.append(normalized)
    return result


def _stepwise_saturation(I, ineqs):
    """
    Saturate ideal I w.r.t. each element of ineqs sequentially.

    Processes ineqs in order of ascending total degree: saturating by a
    low-degree (cheap) generator first tends to simplify/shrink I quickly,
    which usually makes the remaining, higher-degree saturations faster
    than if they'd been run against the original, larger ideal. This is a
    heuristic (not guaranteed optimal for every ideal), but it's a
    reasonable default and costs nothing extra to apply.

    Note: I : (f1...fk)^\\infty is independent of the order the fi are
    processed in (saturation by a product equals iterated saturation,
    regardless of order) — only the runtime is affected by ordering, not
    the result.
    """
    R = I.ring()
    for f in sorted(ineqs, key=lambda f: f.degree()):
        I = I.saturation(R.ideal([f]))[0]
    return I


# ---------------------------------------------------------------------------
# Fundamental circuits basis graph
# ---------------------------------------------------------------------------

def _fundamental_circuits_basis_graph(M, basis):
    """
    Build the bipartite incidence graph G(D#) between basis elements and
    non-basis elements (via fundamental circuits).

    Returns
    -------
    E_dict     : {frozenset({b_elem, e}): (row_index, e)}
    G          : sage Graph
    fund_circs : list of fundamental circuits, one per non-basis element
                 (in the same order as `non_basis`)
    """
    row_idx = {b_elem: idx for idx, b_elem in enumerate(sorted(basis))}
    non_basis = sorted(M.groundset() - basis)
    fund_circs = [M._fundamental_circuit(basis, e) for e in non_basis]

    E_dict = {}
    edges = []
    for e, circ in zip(non_basis, fund_circs):
        for b_elem in circ - {e}:
            E_dict[frozenset((b_elem, e))] = (row_idx[b_elem], e)
            edges.append((b_elem, e))

    G = Graph(edges, multiedges=False)
    return E_dict, G, fund_circs


# ---------------------------------------------------------------------------
# Core matrix construction
# ---------------------------------------------------------------------------

def _realization_space_matrix(M, basis, F):
    """
    Build the initial realization matrix with free variables.

    Returns (R, mat) where R is the ambient (polynomial) ring and mat is
    an r × n matrix over R.
    """
    r = M.rank()
    n = len(M.groundset())

    E_dict, G_sharp, fund_circs = _fundamental_circuits_basis_graph(M, basis)
    SF = {
        frozenset((u, v)) for G in G_sharp.connected_components_subgraphs()
        for (u, v, _) in G.min_spanning_tree(check_weight=False)
    }

    # Count free variables
    nvars = sum(len(c) - 1 for c in fund_circs)
    nvars -= len(SF)
    nvars = max(nvars, 0)

    if nvars > 0:
        names = [f'x{i}' for i in range(1, nvars + 1)]
        R = PolynomialRing(F, nvars, names)

        # Singular's fast det() computation needs a field
        if F in Fields():
            Q = R
        else:
            Q = PolynomialRing(F.fraction_field(), nvars, names)

        xs = list(Q.gens())
    else:
        R = F
        Q = F
        xs = []

    mat = zero_matrix(Q, r, n)
    one = Q.one()

    # Identity block for basis columns
    for i, b_elem in enumerate(sorted(basis)):
        mat[i, b_elem] = one

    var_counter = 0
    for key, (row_idx, col_elem) in E_dict.items():
        if key in SF:
            mat[row_idx, col_elem] = one
        else:
            mat[row_idx, col_elem] = xs[var_counter]
            var_counter += 1

    return R, mat


# ---------------------------------------------------------------------------
# Simplify: handle loops and parallel elements
# ---------------------------------------------------------------------------

def _simplify_for_realization_space(M, basis):
    """
    Reduce M to a simple matroid on one representative per parallel class.

    Returns
    -------
    Ms           : Matroid (simple, on representative elements)
    expand_fn    : function(simple_mat) -> full n-column matrix
    """
    E = sorted(M.groundset(), key=cmp_elements_key)
    loops = M.loops()

    M = M.delete(M.loops())

    parallel_classes = M.flats(1)

    def get_rep(F):
        if basis is not None:
            e = F & basis
            if len(e) == 1:
                return next(iter(e))
        return min(F, key=cmp_elements_key)

    reps = [get_rep(F) for F in parallel_classes]
    rep_of = {e: get_rep(F) for F in parallel_classes for e in F}
    rep_col = {r: i for i, r in enumerate(reps)}

    # Restrict to representatives
    M = M.delete([e for e in M.groundset() if e not in reps])
    M = M.relabel(rep_col)

    def expand_to_full(simple_mat):
        R = simple_mat.base_ring()
        r = simple_mat.nrows()
        full = zero_matrix(R, r, len(E))
        for j_idx, e in enumerate(E):
            if e in loops:
                continue
            col = rep_col[rep_of[e]]
            for i in range(r):
                full[i, j_idx] = simple_mat[i, col]
        return full

    return M, reps, rep_col, expand_to_full


# ---------------------------------------------------------------------------
# Heuristic basis selection
# ---------------------------------------------------------------------------

def _find_good_basis_heuristically(M):
    """Choose a basis minimising circuit–basis incidences."""
    best_score = float('inf')
    for b in M.bases():
        score = sum(len(M._fundamental_circuit(b, e))
                    for e in M.groundset() - b)
        if score < best_score:
            best_score = score
            best_basis = b
    return best_basis


# ---------------------------------------------------------------------------
# Reduction helpers
# ---------------------------------------------------------------------------

def _clean(f, R, sgens):
    """Remove from f any irreducible factors that appear in sgens_set."""
    if f == 0:
        return f
    fac = _factor_cached(f)
    result = R(fac.unit())
    for p, e in fac:
        if p not in sgens:
            result *= p ** e
    return result


def _find_solution_v(v, igens, sgens, R, FR):
    best, best_cost = None, (float('inf'), float('inf'))
    for f in igens:
        if f.degree(v) != 1:
            continue
        den = f.coefficient({v: 1})
        den_factors = [p for p, _ in _factor_cached(den)]
        if not all(d in sgens for d in den_factors):
            continue
        t = FR(den * v - f) / FR(den)
        cost = (t.numerator().number_of_terms(), t.numerator().total_degree())
        if cost < best_cost:
            best_cost = cost
            best = t
    return best, best_cost


def _sub_v(v, t, f, R, FR):
    """
    Substitute v -> t in f (t may be a fraction-field element).
    Returns an element of R (the numerator after clearing denominators).
    """
    result = FR(f).subs({v: t})
    if hasattr(result, "numerator"):
        return R(result.numerator())
    return R(result)


def _new_sgens(v, t, sgens, R, FR):
    result = []
    for g in sgens:
        if not hasattr(g, 'variables') or v not in g.variables():
            if g not in result:
                result.append(g)
            continue
        ng = _sub_v(v, t, g, R, FR)
        if ng == 0:
            return [R(0)]
        fac = _factor_cached(ng)
        for p, _ in fac:
            if p not in result:
                result.append(p)
    return result


def _new_igens(v, t, igens, sgens, R, FR):
    result = []
    for f in igens:
        nf = _clean(_sub_v(v, t, f, R, FR), R, sgens)
        if nf == 1:
            return [R(1)]
        if nf != 0 and nf not in result:
            result.append(nf)
    return result


def _matrix_sub_v(v, t, mat, R, FR):
    """
    Apply substitution v -> t to every entry of mat.
    Clears denominators column-by-column so the result lives in R.
    """
    nr, nc = mat.nrows(), mat.ncols()

    subbed = matrix(FR, nr, nc,
                    [FR(mat[i, j]).subs({v: t})
                     for i in range(nr) for j in range(nc)])

    result = zero_matrix(R, nr, nc)
    for c in range(nc):
        col_denoms = [FR(subbed[r, c]).denominator() for r in range(nr)]
        lc = col_denoms[0]
        for d in col_denoms[1:]:
            lc = lc.lcm(d)
        for r in range(nr):
            result[r, c] = R((FR(subbed[r, c]) * lc).numerator())
    return result


# ---------------------------------------------------------------------------
# reduce_realization_space
# ---------------------------------------------------------------------------

def _reduce_ideal_one_step(igens, sgens, ideal_vars, R, FR, X):
    # Rank all candidates first (find_solution_v is fast)
    candidates = []
    for v in ideal_vars:
        t, cost = _find_solution_v(v, igens, sgens, R, FR)
        if t is not None:
            candidates.append((cost, v, t))
    candidates.sort()  # try cheapest first

    if not candidates:
        return igens, sgens, X, None, None, True

    # Try each candidate; skip to next if substitution times out
    for cost, best_v, best_t in candidates:
        timed_out = False
        alarm(30)
        try:
            sgens_new = _new_sgens(best_v, best_t, sgens, R, FR)
            if [R(0)] == sgens_new:
                cancel_alarm()
                return None, None, None, None, None, True

            igens_new = _new_igens(best_v, best_t, igens, sgens_new, R, FR)
            if [R(1)] == igens_new:
                cancel_alarm()
                return None, None, None, None, None, True

            X_new = _matrix_sub_v(best_v, best_t, X, R, FR) if X is not None else X
            cancel_alarm()
        except AlarmInterrupt:
            timed_out = True

        if timed_out:
            print(f"Alarm on {best_v}, trying next candidate...")
            continue

        return igens_new, sgens_new, X_new, best_v, best_t, False

    # All candidates timed out
    print("All candidates timed out.")
    print(igens, sgens)
    return igens, sgens, X, None, None, True


def reduce_realization_space(MRS):
    """Elimination loop working on raw generator lists."""
    R = MRS.ambient_ring
    if not _is_poly_ring(R):
        return MRS
    FR = R.fraction_field()
    igens = MRS.defining_ideal.gens()
    sgens = MRS.inequations
    X = MRS.realization_matrix
    elim = {}
    ideal_vars = set().union(*(f.variables() for f in igens))
    while True:
        igens_new, sgens_new, X_new, v, t, done = _reduce_ideal_one_step(
            igens, sgens, ideal_vars, R, FR, X
        )
        if igens_new is None:
            MRS._is_realizable = False
            return MRS
        if done:
            break
        igens = igens_new
        sgens = sgens_new
        X = X_new
        for x in elim:
            elim[x] = _sub_v(v, t, elim[x], R, FR)
        elim[v] = t
        ideal_vars.remove(v)

    # Build reduced ring without eliminated variables
    xs = list(R.gens())
    kept = [v for v in xs if v not in elim]
    kept_names = ['x{}'.format(i + 1) for i in range(len(kept))]
    if len(kept) == 0:
        R_new = R.base_ring()
        phi = R.hom([R_new(0)] * len(xs), R_new)
    else:
        R_new = PolynomialRing(R.base_ring(), len(kept), kept_names)
        new_gens = {str(v): R_new.gen(i) for i, v in enumerate(kept)}
        images = [new_gens.get(str(v), R_new(0)) for v in xs]
        phi = R.hom(images, R_new)

    I_new = R_new.ideal([phi(f) for f in igens]) if igens else R_new.ideal([R_new(0)])
    sgens_new = [phi(g) for g in sgens]

    # Detect unrealizable
    if R_new(0) in sgens_new or I_new.is_one():
        MRS_new = MatroidRealizationSpace(
            MRS.basis, I_new, sgens_new, R_new, None, MRS.char, MRS.q, MRS.ground_ring
        )
        MRS_new._is_realizable = False
        return MRS_new

    sgens_new = _gens_prime_divisors([g for g in sgens_new if g != 0])

    X_new = X.apply_map(phi) if X is not None else None

    return MatroidRealizationSpace(
        MRS.basis, I_new, sgens_new, R_new, X_new, MRS.char, MRS.q, MRS.ground_ring
    )


# ---------------------------------------------------------------------------
# realization_space  (main public function)
# ---------------------------------------------------------------------------

def realization_space(M, basis=None, saturate=False, simplify=True, char=None,
                      q=None, ground_ring=None, compute_matrix=True):
    """
    Compute the matroid realization space of matroid M.

    Parameters
    ----------
    M           : SageMath Matroid
    basis       : iterable or None — basis specifying the identity columns
    saturate    : bool — saturate defining ideal w.r.t. inequations (slow)
    simplify    : bool — eliminate variables where possible
    char        : int or None — characteristic of coefficient field
    q           : int or None — prime power; work over GF(q)
    ground_ring : Ring or None — override base ring (default ZZ)

    Returns
    -------
    MatroidRealizationSpace
    """
    if ground_ring is None:
        ground_ring = ZZ

    if basis is not None:
        basis = frozenset(basis)
        if basis not in M.bases():
            raise ValueError("The given basis is not valid.")

    if char is not None and char != 0 and not is_prime(char):
        raise ValueError("The characteristic must be 0 or a prime number.")

    if q is not None:
        if not is_prime_power(q):
            raise ValueError("q must be a prime power.")
        p, _ = is_prime_power(q, get_data=True)
        if char is not None and char != p:
            raise ValueError("The given characteristic doesn't match q.")
        char = p

    if char == 0:
        ground_ring = QQ
    elif char is not None:
        ground_ring = GF(char)

    # Simplify: remove loops and parallel elements
    Ms, reps, rep_col, expand_fn = _simplify_for_realization_space(M, basis)

    # Choose working basis
    if basis is not None:
        work_basis = frozenset(rep_col[e] for e in basis)
    else:
        work_basis = _find_good_basis_heuristically(Ms)
        basis = frozenset(e for e in reps if rep_col[e] in work_basis)

    R, mat = _realization_space_matrix(Ms, work_basis, ground_ring)

    eqs = []
    ineqs = []

    if not _is_poly_ring(R):
        # No free variables
        full_mat = expand_fn(mat)
        RS = MatroidRealizationSpace(
            basis, R.ideal([R(0)]), [], R, full_mat, char, q, ground_ring
        )
        RS._is_realizable = True
        return RS

    # Collect inequations from bases
    for B in Ms.bases():
        sub = mat.matrix_from_columns(B)
        col_det = R(sub.determinant())
        ineqs.append(col_det)

        if col_det == 0:
            ineqs.append(col_det)
            RS = MatroidRealizationSpace(
                basis, R.ideal(eqs), ineqs, R, None, char, q, ground_ring
            )
            RS._is_realizable = False
            return RS

    # Collect equations from nonbases
    for NB in Ms.nonbases():
        sub = mat.matrix_from_columns(NB)
        col_det = R(sub.determinant())
        eqs.append(col_det)

    def_ideal = R.ideal(eqs) if eqs else R.ideal([R(0)])
    mat = mat.change_ring(R)

    if simplify:
        gb = def_ideal.groebner_basis()
        def_ideal = R.ideal(gb)

        if def_ideal.is_one():
            RS = MatroidRealizationSpace(
                basis, def_ideal, ineqs, R, None, char, q, ground_ring
            )
            RS._is_realizable = False
            return RS

        ineqs = _gens_prime_divisors(ineqs)

    RS = MatroidRealizationSpace(
        basis, def_ideal, ineqs, R,
        mat if compute_matrix else None,
        char, q, ground_ring,
    )

    # GF(q): add Frobenius equations x^q = x
    if q is not None and _is_poly_ring(RS.ambient_ring):
        R2 = RS.ambient_ring
        frob_eqs = [x**q - x for x in R2.gens()]
        I2 = RS.defining_ideal + R2.ideal(frob_eqs)
        RS.defining_ideal = I2
        if I2.is_one():
            RS._is_realizable = False
            return RS

    if simplify:
        RS = reduce_realization_space(RS)

    # Optional saturation
    if saturate and _is_poly_ring(RS.ambient_ring):
        RS.defining_ideal = _stepwise_saturation(RS.defining_ideal, RS.inequations)
        RS._is_realizable = not RS.defining_ideal.is_one()
        return RS

    if simplify and saturate:
        RS = reduce_realization_space(RS)

    # Filter redundant inequations
    # if simplify:
    #     non_redundant = []
    #     I = RS.defining_ideal
    #     for ineq in RS.inequations:
    #         combined = I + RS.ambient_ring.ideal([ineq])
    #         if not combined.is_one():
    #             non_redundant.append(ineq)
    #     RS.inequations = non_redundant

    # Expand simple realization matrix back to full n columns
    if RS.realization_matrix is not None:
        RS.realization_matrix = expand_fn(RS.realization_matrix)

    return RS


# ---------------------------------------------------------------------------
# characteristic_set
# ---------------------------------------------------------------------------

class CharacteristicSet:
    """
    The characteristic set of a matroid,

        χ(M) = {p ∈ P ∪ {0} : M is realizable over some field of
                               characteristic p}.

    As explained in 2.2, exactly one of the following holds:

    * ``finite`` is True  — χ(M) is a finite set of primes (0 is never
      included), stored directly in ``primes``.
    * ``finite`` is False — χ(M) is P ∪ {0} minus a finite set of "excluded"
      primes, stored in ``primes``. (0 is always in χ(M) in this case.)

    Use ``p in cs`` to test membership rather than reading ``primes``
    directly, since the meaning of ``primes`` flips between the two cases.
    """

    def __init__(self, finite, primes, uncertain=()):
        self.finite = bool(finite)
        self.primes = frozenset(int(p) for p in primes)
        self.uncertain = frozenset(int(p) for p in uncertain)

    def __contains__(self, p):
        if self.finite:
            return p in self.primes
        return True if p == 0 else p not in self.primes

    def __iter__(self):
        if not self.finite:
            raise TypeError("characteristic set is infinite; test membership with `in` instead")
        return iter(sorted(self.primes))

    def __eq__(self, other):
        if not isinstance(other, CharacteristicSet):
            return NotImplemented
        return self.finite == other.finite and self.primes == other.primes

    def __repr__(self):
        if self.finite:
            s = "{{{}}}".format(", ".join(str(p) for p in sorted(self.primes)))
        else:
            excluded = sorted(self.primes)
            s = "P ∪ {0}" if not excluded else "(P ∪ {{0}}) \\ {{{}}}".format(
                ", ".join(str(p) for p in excluded))
        if self.uncertain:
            s += "  [unverified: {}]".format(
                ", ".join(str(p) for p in sorted(self.uncertain)))
        return s


def _prime_divisors(n):
    n = ZZ(n)
    if n == 0:
        return set()
    return {int(p) for p, _ in n.factor()}


def characteristic_set(M_or_RS, basis=None, verify=True):
    r"""
    Compute the characteristic set χ(M) of a matroid M.
    """
    if isinstance(M_or_RS, MatroidRealizationSpace):
        RS = M_or_RS
        M = None
    else:
        M = M_or_RS
        RS = realization_space(M, basis=basis, compute_matrix=False)

    if RS.char is not None or RS.q is not None:
        raise ValueError(
            "characteristic_set needs a realization space computed over ZZ "
            "(char=None, q=None), not one already specialized to a fixed "
            "characteristic or field size."
        )

    base_ring = RS.ambient_ring.base_ring() if _is_poly_ring(RS.ambient_ring) else RS.ambient_ring
    if base_ring is not ZZ:
        raise ValueError("characteristic_set needs a realization space defined over ZZ.")

    if RS._is_realizable is False:
        return CharacteristicSet(True, set())

    I = RS.defining_ideal
    Q = RS.inequations

    if not _is_poly_ring(RS.ambient_ring):
        if I.is_one():
            result = CharacteristicSet(True, set())
        elif I.is_zero():
            excluded = set()
            for q in Q:
                excluded |= _prime_divisors(q)
            result = CharacteristicSet(False, excluded)
        else:
            n = gcd([ZZ(g) for g in I.gens()])
            result = CharacteristicSet(True, _prime_divisors(n))
    else:
        R = RS.ambient_ring
        result = _characteristic_set_rabinowitsch(I, Q, R)

    if verify and result.uncertain and M is not None:
        still_excluded = set(result.primes)
        for p in result.uncertain:
            RS_p = realization_space(M, basis=basis, char=p)
            realizable = RS_p.is_realizable()

            if result.finite:
                if not realizable:
                    still_excluded.discard(p)
            else:
                if not realizable:
                    still_excluded.add(p)

        result = CharacteristicSet(result.finite, still_excluded)

    return result


def _characteristic_set_rabinowitsch(I, Q, R):
    """
    Build the Rabinowitsch ideal J' = I + (y*g + 1) (g = product of Q) in R[y]
    and read constants / leading coefficients off its Gröbner basis.
    """
    y = 'y_char_set'
    while y in R.variable_names():
        y += '_'
    Rext = PolynomialRing(ZZ, list(R.variable_names()) + [y])
    y = Rext.gens()[-1]
    phi = R.hom(list(Rext.gens()[:-1]))  # codomain inferred as Rext

    g = Rext(1)
    for q in Q:
        g *= phi(q)
    f = y * g + 1

    Jp = Rext.ideal([phi(h) for h in I.gens()] + [f])

    if Jp.is_one():
        return CharacteristicSet(True, set())

    G = [g_ for g_ in Jp.groebner_basis() if g_ != 0]
    constants = [ZZ(g_.constant_coefficient()) for g_ in G if g_.is_constant()]
    constants = [c for c in constants if c != 0]

    leading_coeffs = [ZZ(g_.lc()) for g_ in G]
    gamma = lcm(leading_coeffs) if leading_coeffs else ZZ(1)
    suspects = _prime_divisors(gamma)

    if constants:
        candidates = _prime_divisors(gcd(constants))
        return CharacteristicSet(True, candidates, uncertain=candidates)

    return CharacteristicSet(False, set(), uncertain=suspects)


"""
JSON (de)serialization for MatroidRealizationSpace
====================================================

Standalone module: import it (for its side effect) alongside wherever
MatroidRealizationSpace is defined/used. It monkeypatches to_dict / to_json
/ save_json / from_dict / from_json / load_json onto the class, so any RS
object of that class -- however it was constructed, e.g. via
M.realization_space() -- gains these methods.

Usage
-----
    import matroid_realization_json  # side effect: attaches the methods

    RS = realization_space(M, char=0)
    RS.save_json("my_space.json")

    RS2 = MatroidRealizationSpace.load_json("my_space.json")

or in-memory:

    d = RS.to_dict()          # plain JSON-safe dict
    s = RS.to_json()          # JSON string
    RS2 = MatroidRealizationSpace.from_json(s)

If your MatroidRealizationSpace class lives in a differently-named module,
adjust the import below to match.
"""
# ---------------------------------------------------------------------------
# Ring (de)serialization
# ---------------------------------------------------------------------------


def _ser_ground_ring(ring):
    """Serialize a ground ring (ZZ, QQ, or GF(p)) to a JSON-safe dict."""
    if ring is ZZ:
        return {"kind": "ZZ"}
    if ring is QQ:
        return {"kind": "QQ"}
    try:
        if ring.is_finite() and ring.is_field():
            return {"kind": "GF", "p": int(ring.characteristic())}
    except Exception:
        pass
    raise ValueError("Don't know how to serialize ground ring {!r}".format(ring))


def _deser_ground_ring(data):
    kind = data["kind"]
    if kind == "ZZ":
        return ZZ
    if kind == "QQ":
        return QQ
    if kind == "GF":
        return GF(data["p"])
    raise ValueError("Unknown ground ring kind {!r}".format(kind))


def _ser_ring(R):
    """Serialize ambient_ring: either a polynomial ring or a bare ground ring."""
    if _is_poly_ring(R):
        return {
            "kind": "poly",
            "base_ring": _ser_ground_ring(R.base_ring()),
            "var_names": [str(g) for g in R.gens()],
        }
    return {"kind": "base", "base_ring": _ser_ground_ring(R)}


def _deser_ring(data):
    base = _deser_ground_ring(data["base_ring"])
    if data["kind"] == "poly":
        names = data["var_names"]
        if not names:
            return base
        return PolynomialRing(base, len(names), names)
    return base


def _ring_element_from_str(R, s):
    """Parse a string back into an element of R (poly ring or base ring)."""
    return R(s)


# ---------------------------------------------------------------------------
# Groundset element (de)serialization
# ---------------------------------------------------------------------------
# Matroid groundset elements are usually ints or strings, but the matroid
# library allows arbitrary hashables (including tuples/frozensets). Plain
# ints/strings/floats/bools/None serialize as bare JSON values (no wrapper,
# for compact/readable output); tuples, frozensets, and lists need a
# {"t": ..., "v": ...} wrapper (t=type, v=value) since JSON can't otherwise
# distinguish them from each other or roundtrip them unambiguously.

def _ser_elem(e):
    if e is None or isinstance(e, (bool, str)):
        return e
    if isinstance(e, int):
        return int(e)
    if isinstance(e, float):
        return e
    if isinstance(e, frozenset):
        return {"t": "frozenset", "v": [_ser_elem(x) for x in e]}
    if isinstance(e, tuple):
        return {"t": "tuple", "v": [_ser_elem(x) for x in e]}
    if isinstance(e, list):
        return {"t": "list", "v": [_ser_elem(x) for x in e]}
    # Sage Integer, etc.
    try:
        return int(e)
    except Exception:
        return {"t": "str", "v": str(e)}


def _deser_elem(d):
    if not isinstance(d, dict):
        return d  # bare int/str/float/bool/None
    t = d["t"]
    if t == "str":
        return d["v"]
    if t == "frozenset":
        return frozenset(_deser_elem(x) for x in d["v"])
    if t == "tuple":
        return tuple(_deser_elem(x) for x in d["v"])
    if t == "list":
        return [_deser_elem(x) for x in d["v"]]
    raise ValueError("Unknown element tag {!r}".format(t))


# ---------------------------------------------------------------------------
# MatroidRealizationSpace <-> dict / JSON
# ---------------------------------------------------------------------------

def _mrs_to_dict(self):
    """Serialize this realization space to a JSON-safe dict."""
    ring_data = _ser_ring(self.ambient_ring)

    ideal_gens = [str(f) for f in self.defining_ideal.gens()]
    ineq_strs = [str(f) for f in self.inequations]

    if self.realization_matrix is not None:
        mat = self.realization_matrix
        matrix_data = {
            "nrows": mat.nrows(),
            "ncols": mat.ncols(),
            "entries": [[str(mat[i, j]) for j in range(mat.ncols())]
                        for i in range(mat.nrows())],
        }
    else:
        matrix_data = None

    return {
        "basis": [_ser_elem(e) for e in self.basis],
        "ambient_ring": ring_data,
        "defining_ideal_gens": ideal_gens,
        "inequations": ineq_strs,
        "realization_matrix": matrix_data,
        "char": int(self.char) if self.char is not None else None,
        "q": int(self.q) if self.q is not None else None,
        "ground_ring": _ser_ground_ring(self.ground_ring),
        "one_realization": self.one_realization,
        "is_realizable": self._is_realizable,
    }


def _mrs_to_json(self, **kwargs):
    return json.dumps(self.to_dict(), **kwargs)


def _mrs_save_json(self, path, **kwargs):
    with open(path, "w") as fh:
        fh.write(self.to_json(**kwargs))


def _mrs_from_dict(data):
    R = _deser_ring(data["ambient_ring"])
    ground_ring = _deser_ground_ring(data["ground_ring"])

    basis = frozenset(_deser_elem(e) for e in data["basis"])

    gens = [_ring_element_from_str(R, s) for s in data["defining_ideal_gens"]]
    defining_ideal = R.ideal(gens) if gens else R.ideal([R(0)])

    inequations = [_ring_element_from_str(R, s) for s in data["inequations"]]

    md = data["realization_matrix"]
    if md is not None:
        entries = [[_ring_element_from_str(R, s) for s in row] for row in md["entries"]]
        realization_matrix = matrix(R, md["nrows"], md["ncols"], entries)
    else:
        realization_matrix = None

    MRS = MatroidRealizationSpace(
        basis, defining_ideal, inequations, R, realization_matrix,
        data["char"], data["q"], ground_ring,
    )
    MRS.one_realization = data["one_realization"]
    MRS._is_realizable = data["is_realizable"]
    return MRS


def _mrs_from_json(s):
    return MatroidRealizationSpace.from_dict(json.loads(s))


def _mrs_load_json(path):
    with open(path) as fh:
        return MatroidRealizationSpace.from_json(fh.read())


# ---------------------------------------------------------------------------
# Attach as methods on MatroidRealizationSpace
# ---------------------------------------------------------------------------

MatroidRealizationSpace.to_dict = _mrs_to_dict
MatroidRealizationSpace.to_json = _mrs_to_json
MatroidRealizationSpace.save_json = _mrs_save_json
MatroidRealizationSpace.from_dict = staticmethod(_mrs_from_dict)
MatroidRealizationSpace.from_json = staticmethod(_mrs_from_json)
MatroidRealizationSpace.load_json = staticmethod(_mrs_load_json)


# ---------------------------------------------------------------------------
# Bulk save/load for a dict of MatroidRealizationSpace, keyed by index
# ---------------------------------------------------------------------------

def save_realization_spaces_json(RS_dict, path, **kwargs):
    """
    Save a dict {index: MatroidRealizationSpace} to a single JSON file.

    `index` may be an int or string key; it's stored as a string (JSON object
    keys are always strings) and converted back to int on load if possible.
    """
    data = {str(k): rs.to_dict() for k, rs in RS_dict.items()}
    with open(path, "w") as fh:
        json.dump(data, fh, **kwargs)


def load_realization_spaces_json(path):
    """
    Load a JSON file written by save_realization_spaces_json back into a
    dict {index: MatroidRealizationSpace}. Keys that look like ints are
    converted back to int (so `RS[0]`, `RS[1]`, ... works as before).
    """
    with open(path) as fh:
        data = json.load(fh)

    result = {}
    for k, d in data.items():
        try:
            key = int(k)
        except ValueError:
            key = k
        result[key] = MatroidRealizationSpace.from_dict(d)
    return result
