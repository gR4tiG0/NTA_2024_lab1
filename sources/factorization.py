from sage.all import *
import logging
from tools import millerRabinPT as isPrime, ContFrac

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


def baseGen(n:int) -> list:
    base = [-1]
    L = exp(pow(log(n)*log(log(n)), 1/2))
    logging.debug(f"Generating base for n = {n} with L = {L}")
    logging.debug(round(pow(L, 1/sqrt(2))))
    for i in range(2, round(pow(L, 1/sqrt(2)))):
        if isPrime(i) and kronecker(n, i) == 1:
            base += [i]
    logging.debug(f"Base generated: {base}")   
    return base

def baseRepr(n:int,base:list) -> list:
    if n == 1:
        return None
    base_representation = [0]*len(base)
    if n < 0:
        base_representation[0] = 1
        n = -n
    for i,e in enumerate(base[1:]):
        curr_c = 0
        while n % e == 0:
            n //= e
            curr_c += 1
        base_representation[i+1] = curr_c % 2
    if n != 1:
        return None
    return base_representation


def cfrac(n:int) -> int:
    base = baseGen(n)
    k = len(base)
    inc = 0
    logging.debug(f"k: {k}")
    #frac = continued_fraction_list(sqrt(n)) # sagemath method, idk if I can use it
    #getting enough flat numbers
    frac = ContFrac(n, inc)
    b = [0,1]
    b_pointer = 0
    b_s = {}
    vectors = {}
    while True:
        if len(b_s.keys()) == k:
            break
        ai = frac.getNext()
        bi = (ai*b[b_pointer+1] + b[b_pointer]) % n

        b_pointer += 1
        b += [bi]
        bs = pow(bi,2,n)
        if bs > n//2: bs -= n
        vb = baseRepr(bs, base)
        if vb:
            #logging.debug(f"ai: {ai}, bi: {bi}, bs: {bs}, p: {b_pointer}")
            b_s[bs] = bi
            vectors[bs] = vb

    # logging.debug(f"b_s: {b_s}")
    # logging.debug(f"vectors: {vectors}")
    F = GF(2)
    vs_m = [vector(F, v) for v in vectors.values()]
    M = matrix(F, vs_m).transpose()
    solution_space = M.right_kernel().basis()

    for i in solution_space:
        solv = list(i)
        # logging.debug(f"solv: {solv}")
        Xv,Yv = [],[]
        for c,j in enumerate(solv):
            if j == 1:
                Xv += [list(b_s.values())[c]]
                Yv += [list(b_s.keys())[c]]   
        #logging.debug(f"Xv: {Xv}, Yv: {Yv}")
        x = mul(Xv) % n 
        y = int(sqrt(mul(Yv))) % n
        #logging.debug(f"x: {x}, y: {y}")
        if (x != y) and (x != -y + n):
            f1,f2 = gcd(x-y,n),gcd(x+y,n)
            # logging.debug(b_s.values())
            # logging.debug(f"Xv: {Xv}, Yv: {Yv}")
            # logging.debug(f"Factors found: {f1}, {f2}")
            if 1 < f1 < n and 1 < f2 < n:
                logging.debug(f"Factors found: {f1}, {f2}")
                return gcd(x-y,n)#, gcd(x+y,n)

