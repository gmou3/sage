from .matroid cimport Matroid
from .set_system cimport SetSystem

cdef class FlatsMatroid(Matroid):
    cdef frozenset _groundset  # _E
    cdef int _matroid_rank  # _R
    cdef dict _F  # flats
    cpdef frozenset groundset(self)
    cpdef int _rank(self, frozenset X)
    cpdef full_rank(self)
    cpdef bint _is_independent(self, frozenset X)

    # enumeration
    cpdef SetSystem flats(self, long k)
    cpdef list whitney_numbers2(self)

    # isomorphism and relabeling
    cpdef _is_isomorphic(self, other, certificate=*)
    cpdef relabel(self, mapping)

    # verification
    cpdef bint is_valid(self)
