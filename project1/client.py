import socket
from vigenere_cipher import VigenereCipher

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define the server address and port
server_address = ('localhost', 12345)

# Connect to the server
client_socket.connect(server_address)

# Vigenere key
vigenere_key = "TMU"
cipher = VigenereCipher(vigenere_key)

while True:
    # Get user input for the question
    question = input("Enter Your Question: ")

    # Encrypt the question
    encrypted_question = cipher.encrypt(question)

    # Send the encrypted question to the server
    client_socket.send(encrypted_question.encode())

    # Receive the encrypted answer from the server
    encrypted_answer = client_socket.recv(1024).decode()

    # Display the received encrypted answer
    print(f"Received Encrypted Answer: {encrypted_answer}")

    # Decrypt the answer
    decrypted_answer = cipher.decrypt(encrypted_answer)

    # Display the decrypted answer
    print(f"Decrypted Answer: {decrypted_answer}")

# Close the connection
client_socket.close()
