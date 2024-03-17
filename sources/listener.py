#!/usr/bin/env python3
import socket
import logging

logging.basicConfig(level=logging.DEBUG)

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 1337))
    server_socket.listen(1)

    logging.info("Server is listening on port 1337...")

    while True:
        client_socket, client_address = server_socket.accept()
        logging.debug(f"Accepted connection from {client_address}")

        client_socket.sendall(b"Enter name: ")
        name = client_socket.recv(1024).decode('utf-8').strip()

        greeting = f"Hello, {name}!"
        client_socket.sendall(greeting.encode('utf-8'))

        client_socket.close()


if __name__ == "__main__":
    main()