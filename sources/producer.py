#!/usr/bin/env python3
from pwn import *

N = 33101008296138101


def main() -> None:
    r = remote('0.0.0.0', 1337)
    r.recvuntil(b': ')
    r.sendline(str(N).encode())
    print(r.recvall().decode())
    r.close()


if __name__ == "__main__":
    main()
