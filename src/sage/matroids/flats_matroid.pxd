from .matroid cimport Matroid
from .set_system cimport SetSystem

cdef class FlatsMatroid(Matroid):
    cdef dict _F  # flats
    cdef object _L  # lattice of flats
    cpdef frozenset groundset(self)

    cpdef int _rank(self, frozenset X)
    cpdef frozenset _closure(self, frozenset X)
    cpdef bint _is_closed(self, frozenset X)

    cpdef full_rank(self)

    # enumeration
    cpdef SetSystem flats(self, long k)
    cpdef list whitney_numbers(self)
    cpdef list whitney_numbers2(self)

    # isomorphism and relabeling
    cpdef _is_isomorphic(self, other, certificate=*)
    cpdef Matroid relabel(self, mapping)

    # verification
    cpdef bint is_valid(self)
