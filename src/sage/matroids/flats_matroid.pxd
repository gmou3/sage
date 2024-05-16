from sage.matroids.matroid cimport Matroid

cdef class FlatsMatroid(Matroid):
    cdef frozenset _groundset  # _E
    cdef int _matroid_rank  # _R
    cdef dict _F  # flats
    cpdef frozenset groundset(self)
    cpdef int _rank(self, frozenset X)
    cpdef full_rank(self)
    cpdef bint _is_independent(self, X)

    # enumeration
    cpdef flats(self, k)
    cpdef list whitney_numbers2(self)

    # isomorphism and relabeling
    cpdef _is_isomorphic(self, other, certificate=*)
    cpdef relabel(self, mapping)

    # verification
    cpdef bint is_valid(self)
