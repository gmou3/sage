from .matroid cimport Matroid
from sage.graphs.generic_graph_pyx cimport GenericGraph_pyx

cdef class GraphicMatroid(Matroid):
    cdef frozenset _groundset
    cdef readonly GenericGraph_pyx _G
    cdef dict _vertex_map
    cdef dict _groundset_edge_map
    cpdef frozenset groundset(self)
    cpdef int _rank(self, frozenset X)
    cpdef _vertex_stars(self)
    cpdef _minor(self, contractions, deletions)
    cpdef _has_minor(self, N, bint certificate=*)
    cpdef _corank(self, X)
    cpdef _is_circuit(self, X)
    cpdef _closure(self, X)
    cpdef frozenset _max_independent(self, frozenset X)
    cpdef _max_coindependent(self, X)
    cpdef frozenset _circuit(self, frozenset X)
    cpdef _coclosure(self, X)
    cpdef _is_closed(self, X)
    cpdef _is_isomorphic(self, other, certificate=*)
    cpdef _isomorphism(self, other)
    cpdef bint is_valid(self)
    cpdef is_graphic(self)
    cpdef is_regular(self)
    cpdef graph(self)
    cpdef vertex_map(self)
    cpdef list groundset_to_edges(self, X)
    cpdef _groundset_to_edges(self, X)
    cpdef subgraph_from_set(self, X)
    cpdef _subgraph_from_set(self, X)
    cpdef graphic_extension(self, u, v=*, element=*)
    cpdef graphic_coextension(self, u, v=*, X=*, element=*)
    cpdef twist(self, X)
    cpdef one_sum(self, X, u, v)
    cpdef regular_matroid(self)
    cpdef relabel(self, mapping)
