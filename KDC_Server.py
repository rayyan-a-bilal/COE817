from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.fernet import Fernet
import socket
import threading

# Generate KDC's asymmetric key pair
kdc_private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)

kdc_public_key = kdc_private_key.public_key()


def encrypt_with_public_key(public_key_pem, message):
    public_key = load_pem_public_key(public_key_pem)
    encrypted = public_key.encrypt(
        message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return encrypted


def handle_client(client_socket, client_address):
    print(f"Connection from {client_address} has been established.")

    client_public_key_pem = client_socket.recv(4096)
    print(f"Received public key from {client_address}")

    symmetric_master_key = Fernet.generate_key()
    print(f"Generated symmetric master key for {client_address}: {symmetric_master_key.decode()}")

    encrypted_master_key = encrypt_with_public_key(client_public_key_pem, symmetric_master_key)
    print(f"Encrypted symmetric master key for {client_address}: {encrypted_master_key.hex()}")

    client_socket.send(encrypted_master_key)
    print(f"Sent encrypted master key to {client_address}")

    client_socket.close()


def start_kdc_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 9999))
    server.listen(5)
    print("KDC Server listening on port 9999...")

    while True:
        client, address = server.accept()
        print(f"Accepted connection from {address[0]}:{address[1]}")
        client_handler = threading.Thread(target=handle_client, args=(client,))
        client_handler.start()


if __name__ == "__main__":
    start_kdc_server()