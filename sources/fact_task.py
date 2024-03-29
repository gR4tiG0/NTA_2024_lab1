#!/usr/bin/env python3
from factorization import *
import time


NUMBERS = [3009182572376191, 1021514194991569, 4000852962116741, 15196946347083, 499664789704823, 269322119833303, 679321846483919, 96267366284849, 61333127792637, 2485021628404193]

def main() -> None:
    for number in NUMBERS:
        print(f"Number to factor: {number}")
        start = time.time()
        fct = rpFactor(number)
        end = time.time()
        if 1 < fct < number:
            print(f"Factor found using Rho Pollard method: {fct}")
            print(f"Time elapsed: {end - start}")
        else:
            print(f"Rho Pollard method failed to find a factor for {number}")

        start = time.time()
        fct = cfrac(number)
        end = time.time()
        if 1 < fct < number:
            print(f"Factor found using Continued Fraction method: {fct}")
            print(f"Time elapsed: {end - start}")
        else:
            print(f"Continued Fraction method failed to find a factor for {number}")
    


if __name__ == "__main__":
    main()
