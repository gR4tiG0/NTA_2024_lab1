#!/usr/bin/env python3
import socket
import logging
from tools import millerRabinPT
from factorization import trivialFactor, rpFactor, cfrac


logging.basicConfig(level=logging.DEBUG)

q_,a_,e_,p_ = "[?]", "[*]", "[!]","[+]"



def routine(cs:socket) -> None:
    #factors to be found
    factors = []


    #getting the number from the client
    cs.sendall(f"{q_} n: ".encode('utf-8'))
    n = int(cs.recv(1024).decode('utf-8').strip())
    cs.sendall(f"{a_} Inputed number: {n}\n".encode())



    logging.debug(f"N entered: {n}")
    logging.debug(f"Checking if prime...")

    mr_resp = millerRabinPT(n)
    
    logging.debug(f"Miller-Rabin: {mr_resp}")
    resp = f"{p_} Miller-Rabin primality test: Is prime? - {mr_resp}\n"
    cs.sendall(resp.encode('utf-8'))
    
    if mr_resp:
        #if the number is prime, we send it back to the client and end the routine
        cs.sendall(f"{e_} Response: {n}\n".encode('utf-8'))
        return
    

    
    
    logging.debug("Starting Trial division method...")
    cs.sendall(f"{a_} Starting trial division method...\n".encode('utf-8'))

    factor = 1
    while factor != n:
        factor = trivialFactor(n)
        if factor != n:
            factors += [factor]
            logging.debug(f"Factor found: {factor}")
            cs.sendall(f"{e_} Factor found: {factor}\n".encode('utf-8'))
            n //= factor

    logging.debug(f"Current factors: {factors}; current n: {n}")
    
    if factors != []:
        cs.sendall(f"{p_} Factors found using trivial division method: {factors}\n".encode('utf-8'))
    else:
        cs.sendall(f"{e_} Trivial division method did not give any results\n".encode('utf-8'))    
    
    

    cs.sendall(f"{a_} Starting Pollard's Rho method...\n".encode('utf-8'))

    factor = rpFactor(n)
    if factor != 1:
        logging.debug(f"Factor found: {factor}")

        cs.sendall(f"{p_} Factor found using Pollard's Rho method: {factor}\n".encode('utf-8'))

        factors += [factor]
        n //= factor
    else:
        cs.sendall(f"{e_} Pollard's Rho method did not give any results\n".encode('utf-8'))

    cs.sendall(f"{q_} Starting primalty test for {n}...(again)\n".encode('utf-8'))
    mr_resp = millerRabinPT(n)
    while not mr_resp:

        cs.sendall(f"{a_} N is composite, starting continued fraction factorization method (CFRAC)\n".encode('utf-8'))
        logging.debug(f"Starting continued fraction factorization method...")
        factor = cfrac(n)
        if factor:
            n //= factor
            factors += [factor]
            cs.sendall(f"{p_} Factor found using CFRAC method: {factor}\n".encode('utf-8'))
        else:
            cs.sendall(f"{e_} CFRAC method did not give any results\n".encode('utf-8'))
            break
        mr_resp = millerRabinPT(n)

    cs.sendall(f"{e_} N is prime, adding factor {n}\n".encode('utf-8'))
    factors += [n]
    cs.sendall(f"{e_} Factorization complete: {factors}\n".encode('utf-8'))



def main() -> None:
    #setting up the server
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('0.0.0.0', 1337))
    server_socket.listen(1)

    logging.info("Server is listening on port 1337...")


    #main loop
    while True:
        client_socket, client_address = server_socket.accept()
        logging.debug(f"Accepted connection from {client_address}")
        #starting routine for connected client
        routine(client_socket)

        client_socket.close()


if __name__ == "__main__":
    main()