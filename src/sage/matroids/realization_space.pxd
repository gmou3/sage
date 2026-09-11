cpdef list _backtrack(Py_ssize_t k, list subs, Py_ssize_t n, list domains,
                      dict rels_by_level, object zero)


cdef class MatroidRealizationSpace:
    cdef public frozenset basis
    cdef public object defining_ideal
    cdef public list inequations
    cdef public object ambient_ring
    cdef public object realization_matrix
    cdef public object char
    cdef public object q
    cdef public object ground_ring
    cdef public bint one_realization
    cdef public object _is_realizable
    cdef public object _structure_cache
