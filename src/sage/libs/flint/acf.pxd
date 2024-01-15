# distutils: libraries = flint
# distutils: depends = flint/acf.h

################################################################################
# This file is auto-generated by the script
#   SAGE_ROOT/src/sage_setup/autogen/flint_autogen.py.
# Do not modify by hand! Fix and rerun the script instead.
################################################################################

from libc.stdio cimport FILE
from sage.libs.gmp.types cimport *
from sage.libs.mpfr.types cimport *
from sage.libs.flint.types cimport *

cdef extern from "flint_wrap.h":
    void acf_init(acf_t x) noexcept
    void acf_clear(acf_t x) noexcept
    void acf_swap(acf_t z, acf_t x) noexcept
    slong acf_allocated_bytes(const acf_t x) noexcept
    arf_ptr acf_real_ptr(acf_t z) noexcept
    arf_ptr acf_imag_ptr(acf_t z) noexcept
    void acf_set(acf_t z, const acf_t x) noexcept
    bint acf_equal(const acf_t x, const acf_t y) noexcept
    int acf_add(acf_t res, const acf_t x, const acf_t y, slong prec, arf_rnd_t rnd) noexcept
    int acf_sub(acf_t res, const acf_t x, const acf_t y, slong prec, arf_rnd_t rnd) noexcept
    int acf_mul(acf_t res, const acf_t x, const acf_t y, slong prec, arf_rnd_t rnd) noexcept
    void acf_approx_inv(acf_t res, const acf_t x, slong prec, arf_rnd_t rnd) noexcept
    void acf_approx_div(acf_t res, const acf_t x, const acf_t y, slong prec, arf_rnd_t rnd) noexcept
    void acf_approx_sqrt(acf_t res, const acf_t x, slong prec, arf_rnd_t rnd) noexcept
    void acf_approx_dot(acf_t res, const acf_t initial, int subtract, acf_srcptr x, slong xstep, acf_srcptr y, slong ystep, slong len, slong prec, arf_rnd_t rnd) noexcept
