"""
Matroid Realization Space
=========================

SageMath translation of the OSCAR (Julia) matroid realization space module.
"""

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


def _is_poly_ring(R):
    """True if R is a multivariate or univariate polynomial ring."""
    return isinstance(R, (MPolynomialRing_base, PolynomialRing_general))

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

        if not _is_poly_ring(self.ambient_ring):
            self._is_realizable = not self.defining_ideal.is_one()
            return self._is_realizable

        for p in self.defining_ideal.minimal_associated_primes():
            if all(p.reduce(ineq) != 0 for ineq in self.inequations):
                self._is_realizable = True
                return True

        self._is_realizable = False
        return False

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
    E_dict  : {(u,v): (row_index, col_elem)} — edge key is (max, min)
    G       : sage Graph
    """
    E_dict = {}
    edges = []

    fund_circs = [M.fundamental_circuit(basis, e)
                  for e in sorted(M.groundset() - basis, key=cmp_elements_key)]

    for circ in fund_circs:
        non_basis_in = circ - basis
        if len(non_basis_in) != 1:
            continue
        r = next(iter(non_basis_in))

        for idx, b_elem in enumerate(basis):
            if b_elem in circ:
                u, v = sorted([r, b_elem], key=cmp_elements_key)
                if (u, v) not in E_dict:
                    E_dict[(u, v)] = (idx, r)
                    edges.append((u, v))

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
    E = sorted(M.groundset(), key=cmp_elements_key)
    n = len(E)
    r = M.rank()

    elem_to_idx = {e: i for i, e in enumerate(E)}

    E_dict, G_sharp, fund_circs = _fundamental_circuits_basis_graph(M, basis)
    SF = {
        tuple(sorted([u, v], key=cmp_elements_key))
        for G in G_sharp.connected_components_subgraphs()
        for (u, v, _) in G.min_spanning_tree(check_weight=False)
    }

    # Circuits restricted to basis elements (for variable count)
    fund_circs_basis = [c & basis for c in fund_circs]

    # Count free variables
    nvars = (n - r) * r
    nvars -= sum(r - len(c) for c in fund_circs_basis)
    nvars -= len(SF)
    nvars = max(nvars, 0)

    if nvars > 0:
        names = ['{}{}'.format('x', i) for i in range(1, nvars + 1)]
        R = PolynomialRing(F, nvars, names)
        xs = list(R.gens())
    else:
        R = F
        xs = []

    mat = zero_matrix(R, r, n)

    # Identity block for basis columns
    for i, b_elem in enumerate(basis):
        col = elem_to_idx[b_elem]
        mat[i, col] = R(1)

    var_counter = 0
    for key, (row_idx, col_elem) in E_dict.items():
        col = elem_to_idx[col_elem]
        if key in SF:
            mat[row_idx, col] = R(1)
        else:
            mat[row_idx, col] = xs[var_counter]
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

    return M, expand_to_full


# ---------------------------------------------------------------------------
# Heuristic basis selection
# ---------------------------------------------------------------------------

def _find_good_basis_heuristically(M):
    """Choose a basis minimising circuit–basis incidences."""
    best_score = float('inf')
    for b in M.bases():
        score = sum(len(M.fundamental_circuit(b, e))
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

    # ---- Build reduced ring without eliminated variables -----------------
    xs = list(R.gens())
    kept = [v for v in xs if v not in elim]
    kept_names = ['x{}'.format(i+1) for i in range(len(kept))]
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

    # sgens_new = _gens_prime_divisors([g for g in sgens_new if g != 0])

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

    # --- Simplify: remove loops and parallel elements ---
    Ms, expand_fn = _simplify_for_realization_space(M, basis)

    # --- Choose working basis ---
    if basis is None:
        basis = _find_good_basis_heuristically(Ms)

    polyR, mat = _realization_space_matrix(Ms, basis, ground_ring)

    eqs = []
    ineqs = []

    if not _is_poly_ring(polyR):
        # No free variables
        full_mat = expand_fn(mat)
        RS = MatroidRealizationSpace(
            basis, polyR.ideal([polyR(0)]), [], polyR, full_mat, char, q, ground_ring
        )
        RS._is_realizable = True
        return RS


    B = Ms.bases()
    E_idx = {
        e: i for i, e in
        enumerate(sorted(Ms.groundset(), key=cmp_elements_key))
    }

    # --- Collect equations and inequations from all r-subsets ---
    for col_elems in combinations(Ms.groundset(), Ms.rank()):
        col_set = frozenset(col_elems)
        col_indices = [E_idx[e] for e in col_elems]
        sub = mat.matrix_from_columns(col_indices)
        col_det = sub.determinant()
        is_basis = col_set in B

        if is_basis and col_det == 0:
            ineqs.append(col_det)
            RS = MatroidRealizationSpace(
                basis, polyR.ideal(eqs), ineqs, polyR, None, char, q, ground_ring
            )
            RS._is_realizable = False
            return RS

        if is_basis:
            ineqs.append(col_det)
        else:
            eqs.append(col_det)

    def_ideal = polyR.ideal(eqs) if eqs else polyR.ideal([polyR(0)])
    gb = def_ideal.groebner_basis()
    def_ideal = polyR.ideal(gb)

    if def_ideal.is_one():
        RS = MatroidRealizationSpace(
            basis, def_ideal, ineqs, polyR, None, char, q, ground_ring
        )
        RS._is_realizable = False
        return RS

    ineqs = _gens_prime_divisors(ineqs)

    RS = MatroidRealizationSpace(
        basis, def_ideal, ineqs, polyR,
        mat if compute_matrix else None,
        char, q, ground_ring,
    )

    # --- GF(q): add Frobenius equations x^q = x ---
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

    # --- Optional saturation ---
    if saturate and _is_poly_ring(RS.ambient_ring):
        RS.defining_ideal = _stepwise_saturation(RS.defining_ideal, RS.inequations)
        RS._is_realizable = not RS.defining_ideal.is_one()
        return RS

    if simplify and saturate:
        RS = reduce_realization_space(RS)

    # --- Filter redundant inequations ---
    # if simplify:
    #     non_redundant = []
    #     I = RS.defining_ideal
    #     for ineq in RS.inequations:
    #         combined = I + RS.ambient_ring.ideal([ineq])
    #         if not combined.is_one():
    #             non_redundant.append(ineq)
    #     RS.inequations = non_redundant

    # --- Expand simple realization matrix back to full n columns ---
    if RS.realization_matrix is not None:
        RS.realization_matrix = expand_fn(RS.realization_matrix)

    return RS


# ---------------------------------------------------------------------------
# realization  (find a single concrete realization)
# ---------------------------------------------------------------------------

def realization(M_or_RS, basis=None, saturate=False, simplify=True,
                char=None, q=None):
    """
    Find one concrete realization of the matroid (or realization space).

    Returns a MatroidRealizationSpace with one_realization=True.
    """
    if isinstance(M_or_RS, MatroidRealizationSpace):
        RS = M_or_RS
    else:
        RS = realization_space(M_or_RS, basis=basis, saturate=saturate,
                               simplify=simplify, char=char, q=q)

    if char is None and q is None:
        raise ValueError("A field or characteristic must be specified.")

    if not RS.is_realizable():
        return RS

    R = RS.ambient_ring
    if not _is_poly_ring(R):
        RS.one_realization = True
        return RS

    I = RS.defining_ideal
    eqs = list(I.gens())

    dim_I = I.dimension()

    if dim_I == 0:
        try:
            for p in I.minimal_associated_primes():
                if all(not p.reduce(ineq) == 0 for ineq in RS.inequations):
                    RS_new = MatroidRealizationSpace(
                        RS.basis, p, [], R, RS.realization_matrix, RS.char, RS.q, RS.ground_ring
                    )
                    RS_new = reduce_realization_space(RS_new)
                    RS_new.one_realization = True
                    return RS_new
        except Exception:
            pass
        RS.one_realization = True
        return RS

    # Positive-dimensional: specialise first d variables
    d = min(dim_I, R.ngens())
    base_val = 7 if (char is None or char == 0) else char
    upper = min(base_val**d, 1000)

    found = False
    I_new = I
    ineqs_new = list(RS.inequations)

    for counter in range(upper):
        # Little-endian base-b digits, matching Oscar's digits()
        vals = []
        tmp = counter
        for _ in range(d):
            vals.append(tmp % base_val)
            tmp //= base_val

        spec_eqs = [R.gen(i) - vals[i] for i in range(d)]
        I_try = R.ideal(eqs + spec_eqs)
        I_try = R.ideal(I_try.groebner_basis())
        if I_try.is_one():
            continue

        gb_list = list(I_try.gens())
        ineqs_try = [f.reduce(gb_list) for f in RS.inequations]
        if R(0) in ineqs_try:
            continue

        # I_try = _stepwise_saturation(I_try, ineqs_try)
        # if I_try.is_one():
        #     continue

        I_new = I_try
        ineqs_new = ineqs_try
        found = True
        break

    if not found:
        return RS

    RS_new = MatroidRealizationSpace(
        RS.basis, I_new, ineqs_new, R, RS.realization_matrix, RS.char, RS.q, RS.ground_ring
    )
    RS_new = reduce_realization_space(RS_new)
    RS_new.one_realization = True
    return RS_new
