#!/usr/bin/env python3
from pwn import *

N = 33101008296138101
Ns = [901667173167834173, 323324583518541583, 2500744714570633849, 691534156424661573, 1184056490329830239, 1449863225586482579, 778320232076288167, 1515475730401555091, 341012868237902669, 7442109405582674149]

def main() -> None:
    for n in Ns:
        r = remote('0.0.0.0', 1337)
        r.recvuntil(b': ')
        r.sendline(str(n).encode())
        print(r.recvall().decode())
        r.close()


if __name__ == "__main__":
    main()
