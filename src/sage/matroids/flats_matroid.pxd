from .matroid cimport Matroid
from sage.combinat.posets.lattices import FiniteLatticePoset
from .set_system cimport SetSystem

cdef class FlatsMatroid(Matroid):
    cdef frozenset _groundset  # _E
    cdef int _matroid_rank  # _R
    cdef dict _F  # flats
    cpdef frozenset groundset(self)
    cpdef int _rank(self, frozenset X)
    cpdef full_rank(self)
    cpdef frozenset _closure(self, frozenset X)
    cpdef bint _is_closed(self, frozenset X)

    # enumeration
    cpdef SetSystem flats(self, long k)
    cpdef list whitney_numbers2(self)

    # isomorphism and relabeling
    cpdef _is_isomorphic(self, other, certificate=*)
    cpdef relabel(self, mapping)

    # verification
    cpdef bint is_valid(self)

cdef class LatticeOfFlatsMatroid(FlatsMatroid):
    cdef object _L  # lattice_of_flats
    cpdef list whitney_numbers(self)
    cpdef bint is_valid(self)
