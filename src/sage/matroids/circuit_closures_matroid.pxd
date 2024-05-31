from sage.matroids.matroid cimport Matroid

cdef class CircuitClosuresMatroid(Matroid):
    cdef dict _circuit_closures  # _CC
    cpdef frozenset groundset(self)
    cpdef int _rank(self, frozenset X)
    cpdef full_rank(self)
    cpdef bint _is_independent(self, frozenset F)
    cpdef frozenset _max_independent(self, frozenset F)
    cpdef frozenset _circuit(self, frozenset F)
    cpdef dict circuit_closures(self)
    cpdef _is_isomorphic(self, other, certificate=*)
    cpdef relabel(self, mapping)
