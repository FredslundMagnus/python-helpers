from numpy import array as _array


def gcd(a: int, b: int, do_print: bool = False, return_s_t: bool = False) -> int:
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
    if do_print:
        for line in str(_array(matrix)).splitlines()[:-1]:
            print(line[1:])
    if return_s_t:
        return b, matrix[i+1][1], matrix[i+1][2]
    return b


def lcm(a: int, b: int) -> int:
    return a//gcd(a, b)*b


def totient(n: int) -> int:
    return sum(gcd(n, i) == 1 for i in range(1, n+1))


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
