import socket
import json
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

def decrypt_message(key, nonce, ciphertext, tag):
    cipher = AES.new(key, AES.MODE_EAX, nonce)
    decrypted_message = cipher.decrypt_and_verify(ciphertext, tag)
    return decrypted_message.decode()

def chat_responder():
    # Define the server address and port
    server_address = ('localhost', 6001)

    # Create a TCP/IP socket
    chat_responder_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the server address
    chat_responder_socket.bind(server_address)

    # Listen for incoming connections
    chat_responder_socket.listen(1)

    print("Chat responder is listening for incoming connections...")

    while True:
        # Wait for a connection
        print("Waiting for a connection...")
        connection, client_address = chat_responder_socket.accept()

        try:
            print(f"Connection established with {client_address}")

            # Receive data from the client
            data = connection.recv(1024).decode()
            json_data = json.loads(data)

            # Extract user information and message
            username = json_data.get('username')
            encrypted_message = json_data.get('ciphertext')
            unencrypted_message = json_data.get('unencrypted_message')

            if encrypted_message:
                # If the message is encrypted, decrypt it
                key = get_random_bytes(16)  # Assume shared secret key is already established
                nonce = bytes.fromhex(json_data['nonce'])
                ciphertext = bytes.fromhex(json_data['ciphertext'])
                tag = bytes.fromhex(json_data['tag'])
                decrypted_message = decrypt_message(key, nonce, ciphertext, tag)
                print(f"Encrypted message received from {username}: {decrypted_message}")
            elif unencrypted_message:
                # If the message is unencrypted, handle it as is
                print(f"Unencrypted message received from {username}: {unencrypted_message}")
            else:
                print("Invalid message format.")

        except Exception as e:
            print(f"Error: {e}")

        finally:
            # Clean up the connection
            connection.close()

if __name__ == "__main__":
    chat_responder()
