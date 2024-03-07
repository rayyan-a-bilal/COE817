import socket
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.fernet import Fernet

def generate_asymmetric_key_pair():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    return private_key, private_key.public_key()

def decrypt_with_private_key(private_key, encrypted_message):
    return private_key.decrypt(
        encrypted_message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

def start_client(client_name):
    try:
        private_key, public_key = generate_asymmetric_key_pair()
        print(f"{client_name}: Generated asymmetric key pair.")

        public_key_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('localhost', 9999))
        print(f"{client_name}: Connected to KDC.")

        client.send(public_key_pem)
        print(f"{client_name}: Sent public key to KDC.")

        encrypted_master_key = client.recv(4096)
        print(f"{client_name}: Received encrypted master key from KDC.")

        master_key = decrypt_with_private_key(private_key, encrypted_master_key)
        print(f"{client_name} decrypted master key: {master_key}")
    except Exception as e:
        print(f"Error in {client_name}: {e}")

if __name__ == "__main__":
    client_name = "Bob"  # Or "B", depending on the client
    start_client(client_name)
