class VigenereCipher:
    def __init__(self, key):
        self.key = key

    def encrypt(self, message):
        encrypted_message = ""
        key_index = 0

        for char in message:
            if char.isalpha():
                key_char = self.key[key_index % len(self.key)]
                key_index += 1

                shift = ord(key_char.upper()) - ord('A')
                if char.isupper():
                    encrypted_char = chr((ord(char) + shift - ord('A')) % 26 + ord('A'))
                else:
                    encrypted_char = chr((ord(char) + shift - ord('a')) % 26 + ord('a'))

                encrypted_message += encrypted_char
            else:
                encrypted_message += char

        return encrypted_message

    def decrypt(self, encrypted_message):
        decrypted_message = ""
        key_index = 0

        for char in encrypted_message:
            if char.isalpha():
                key_char = self.key[key_index % len(self.key)]
                key_index += 1

                shift = ord(key_char.upper()) - ord('A')
                if char.isupper():
                    decrypted_char = chr((ord(char) - shift - ord('A')) % 26 + ord('A'))
                else:
                    decrypted_char = chr((ord(char) - shift - ord('a')) % 26 + ord('a'))

                decrypted_message += decrypted_char
            else:
                decrypted_message += char

        return decrypted_message
