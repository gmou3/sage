from sage.matroids.matroid cimport Matroid
from sage.matroids.set_system cimport SetSystem


cdef class CircuitsMatroid(Matroid):
    cdef frozenset _groundset  # _E
    cdef int _matroid_rank  # _R
    cdef dict _k_C
    cdef SetSystem _NSC
    cpdef groundset(self) noexcept
    cpdef _rank(self, X) noexcept
    cpdef full_rank(self) noexcept
    cpdef _is_independent(self, F) noexcept
    cpdef _max_independent(self, F) noexcept
    cpdef _circuit(self, F) noexcept
    cpdef bases(self) noexcept
    cpdef _bases(self) noexcept
    cpdef circuits(self, k=*) noexcept
    cpdef _circuits(self, k=*) noexcept
    cpdef nonspanning_circuits(self) noexcept
    cpdef _nonspanning_circuits(self) noexcept
    cpdef _sort_key(self, x) noexcept
    cpdef _is_isomorphic(self, other, certificate=*) noexcept
    cpdef relabel(self, l) noexcept
    cpdef is_valid(self) noexcept
