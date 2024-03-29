#!/usr/bin/env python3
from Crypto.Util.number import getPrime
from factorization import *
import time

# TEST_FACTOR_LEN = [2**i for i in range(4,16)]
TEST_FACTOR_LEN = [8,10,12,14,16,18,20,22,24,26,28,30,32,36,40,44,48,52,56,60,64,72,80,88,96]

def main() -> None:
    for i in TEST_FACTOR_LEN:
        try:
            number = getPrime(i)*getPrime(i)
            print(f"Number to factor: {number}")
            print(f"Number of bits: {number.bit_length()}")
            start = time.time()
            fct = cfrac(number)
            end = time.time()
            if 1 < fct < number:
                print(f"Factor found: {fct}")
                print(f"Time elapsed: {end - start}")

        except Exception as e:
            print(e)
            continue
if __name__ == "__main__":
    main()