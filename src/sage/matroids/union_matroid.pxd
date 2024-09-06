from sage.matroids.matroid cimport Matroid

cdef class MatroidUnion(Matroid):
    cdef list matroids
    cpdef frozenset groundset(self)
    cpdef int _rank(self, frozenset X) except? -1

cdef class MatroidSum(Matroid):
    cdef list summands
    cpdef frozenset groundset(self)
    cpdef int _rank(self, frozenset X) except? -1

cdef class PartitionMatroid(Matroid):
    cdef dict p
    cpdef frozenset groundset(self)
    cpdef int _rank(self, frozenset X) except? -1
