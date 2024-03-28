from random import randint
from math import sqrt, floor
# extended euclidean algorithm
def xgcd(a:int, b:int) -> list:
    if a == 0:
        return b, 0, 1
    else:
        gcd, x, y = xgcd(b % a, a)
        return [gcd, y - (b // a) * x, x]

# miller rabin primality test
def millerRabinPT(p:int, k:int = 5) -> bool:
    if p == 2 or p == 3:
        return True
    
    if p <= 1 or p % 2 == 0:
        return False
    
    s, d = 0, p - 1
    while d % 2 == 0:
        s += 1
        d //= 2

    for _ in range(k):
        x = randint(1, p - 1)
        g, _, _ = xgcd(x, p)
        if g > 1:
            return False
        
        x = pow(x, d, p)
        if (x == 1) or (x == p - 1):
            continue
        else:
            for _ in range(s):
                x = pow(x, 2, p)
                if x == p - 1:
                    break
                elif x == 1:
                    return False
            else:
                return False
            
    return True


class ContFrac:
    def __init__(self, n:int, inc:int):
        self.n = n
        self.v = 1
        self.alpha = sqrt(n)
        self.a = floor(self.alpha) + inc
        print("a init:",self.a)
        self.u = self.a
        self.frac = [self.a]

    def getNext(self) -> int:
        res = self.a
        self.v = (self.n - self.u**2) // self.v
        self.alpha = (sqrt(self.n) + self.u) / self.v
        self.a = floor(self.alpha)
        self.frac += [self.a]
        self.u = self.a * self.v - self.u
        return res
        
