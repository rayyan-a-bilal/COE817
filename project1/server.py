import socket
from vigenere_cipher import VigenereCipher

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define the server address and port
server_address = ('localhost', 12345)

# Bind the socket to the address and port
server_socket.bind(server_address)

# Listen for incoming connections
server_socket.listen(1)

# Accept a connection
print('Waiting for a connection...')
client_socket, client_address = server_socket.accept()
print(f'Connected to {client_address}')

# Vigenere key
vigenere_key = "TMU"
cipher = VigenereCipher(vigenere_key)

while True:
    # Receive the encrypted message from the client
    encrypted_message = client_socket.recv(1024).decode()
    if not encrypted_message:
        break

    # Display the received encrypted message
    print(f"Received Encrypted Message: {encrypted_message}")

    # Decrypt the message
    decrypted_message = cipher.decrypt(encrypted_message)

    # Display the decrypted message
    print(f"Decrypted Message: {decrypted_message}")

    # Get the response from the server
    response = input("Enter Server Response: ")

    # Encrypt the response
    encrypted_response = cipher.encrypt(response)

    # Send the encrypted response to the client
    client_socket.send(encrypted_response.encode())

# Close the connection
client_socket.close()
server_socket.close()