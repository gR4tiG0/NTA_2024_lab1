from sage.all import *
import logging


logging.basicConfig(level=logging.DEBUG)

TR_PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
 
def trivialFactor(n:int) -> int:
    for i in TR_PRIMES:
        logging.debug(f"Testing prime {i}...")
        if n % i == 0:
            logging.debug(f"Factor found: {i}")
            return i
    return n

def rhoPolard(n:int, f:Polynomial, x0:int) -> int:
    points = []
    x, y, d = x0, f(x0), 1
    counter = 1

    while d == 1:
        if x in points: break
        points += [x]
        logging.debug(f"counter {counter}: x = {x}, y = {y}")
        x = f(x)
        y = f(f(y))
        d = gcd(x - y, n)
        logging.debug(f"Checking gcd({x} - {y}, {n}) = {d}")
        counter += 1
    
    assert n % int(d) == 0
    return int(d)


def rpFactor(n:int) -> int:
    Zn = Integers(n)
    R = PolynomialRing(Zn, 'x')
    f = R('x^2 + 1')
    x0 = Zn(2)
    logging.debug(f"Applying parameters: n = {n}, f = {f}, x0 = {x0}")
    return rhoPolard(n, f, x0)