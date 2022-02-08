from __future__ import annotations
from math import sqrt
from numpy import array as _array, r_, nonzero, ones
import numpy as np
from functools import lru_cache as cache  # Python 3.9
from helpers.utils import timer
from numba import njit as jit

REMEMBER_PRIMES_UP_TO = 1000000


@jit
def gcd_fast(a: int, b: int) -> int:
    matrix = [
        _array([a, 1, 0]),
        _array([b, 0, 1]),
    ]
    i: int = 0
    while a % b:
        matrix.append(matrix[i]-(a//b)*matrix[i+1])
        i += 1
        a, b = matrix[i][0], matrix[i+1][0]
    return b


@jit
def gcd_fast_with_s_t(a: int, b: int) -> int:
    matrix = [
        _array([a, 1, 0]),
        _array([b, 0, 1]),
    ]
    i: int = 0
    while a % b:
        matrix.append(matrix[i]-(a//b)*matrix[i+1])
        i += 1
        a, b = matrix[i][0], matrix[i+1][0]
    matrix.append(matrix[i]-(a//b)*matrix[i+1])
    return b, matrix[i+1][1], matrix[i+1][2]


def gcd_with_print(a: int, b: int, return_s_t: bool = False) -> int:
    matrix = [
        _array([a, 1, 0]),
        _array([b, 0, 1]),
    ]
    i: int = 0
    while a % b:
        matrix.append(matrix[i]-(a//b)*matrix[i+1])
        i += 1
        a, b = matrix[i][0], matrix[i+1][0]
    matrix.append(matrix[i]-(a//b)*matrix[i+1])
    for line in str(_array(matrix)).splitlines()[:-1]:
        print(line[1:])
    if return_s_t:
        return b, matrix[i+1][1], matrix[i+1][2]
    return b


def gcd(a: int, b: int, return_s_t: bool = False, do_print: bool = False):
    if do_print:
        return gcd_with_print(a, b, return_s_t)
    if return_s_t:
        return gcd_fast_with_s_t(a, b)
    return gcd_fast(a, b)


@jit
def lcm(a: int, b: int) -> int:
    return a//gcd_fast(a, b)*b


@jit
def totient(n: int) -> int:
    return sum([gcd_fast(n, i) == 1 for i in range(1, n+1)])


@cache
def primes_up_to(n):
    if n < 6:
        if n < 2:
            return []
        elif n == 2:
            return [2]
        elif n < 5:
            return [2, 3]
        else:
            return [2, 3, 5]
    n += 1
    sieve = ones(n//3 + (n % 6 == 2), dtype=np.bool)
    sieve[0] = False
    for i in range(int(n**0.5)//3+1):
        if sieve[i]:
            k = 3*i+1 | 1
            sieve[((k*k)//3)::2*k] = False
            sieve[(k*k+4*k-2*k*(i & 1))//3::2*k] = False
    return r_[2, 3, ((3*nonzero(sieve)[0]+1) | 1)]


@cache
def primes_up_to_as_set(n: int) -> set[int]:
    return set(primes_up_to(n))


_primes = primes_up_to_as_set(REMEMBER_PRIMES_UP_TO)


def is_prime(n: int) -> bool:
    if n <= REMEMBER_PRIMES_UP_TO:
        return n in _primes
    raise NotImplementedError("This have not been implemented yet.")


@jit
def inverse(n: int, mod: int) -> int:
    _gdc, s, _ = gcd_fast_with_s_t(n, mod)
    if _gdc == 1:
        return s % mod


def prime_factorize(n: int) -> list[int]:
    factors = []
    primes = primes_up_to(min(int(sqrt(n))+3, 1000000))
    i = 0
    while n > 1 and i < len(primes):
        while n % primes[i] == 0:
            n = n // primes[i]
            factors.append(primes[i])
        i += 1
    return factors


def crt_n_ai(n: int, mods: list[int]) -> list[int]:
    return [n % mod for mod in mods]


def crt_ai_n(ai: list[int], mods: list[int]) -> int:
    pass


if __name__ == "__main__":
    assert gcd(10, 12) == 2
    assert gcd(8, 13) == 1
    assert gcd(13, 8) == 1
    assert lcm(10, 12) == 60
    assert gcd(8, 13, return_s_t=True) == (1, 5, -3)
    assert totient(6) == 2
    assert totient(100) == 40
    assert totient(301) == 252
    assert totient(1) == 1
    assert totient(0) == 0
    assert inverse(3, 7) == 5
    assert inverse(4, 9) == 7
    assert prime_factorize(8) == [2, 2, 2]
    assert prime_factorize(9) == [3, 3]
    assert prime_factorize(10) == [2, 5]
    assert crt_n_ai(11, [5, 7]) == [1, 4]
    # print(primes_up_to(11))

    # with timer():
    #     for i in range(1000, 1500):
    #         totient(i)

    # with timer():
    #     for i in range(1000, 1500):
    #         totient(i)

    # with timer():
    #     len(primes_up_to(200000000))

    # with timer():
    #     print(len(primes_up_to(200000000)))
    # for i in range(14):
    #     print(i, primes_up_to(i))
    # with timer():
    #     for i in range(REMEMBER_PRIMES_UP_TO):
    #         isPrime(i)
