import socket
import json
import os
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

def menu():
    print("1. Chat Encrypted")
    print("2. Unencrypted Chat")
    print("3. Users")
    print("4. View Chat History")
    print("5. Exit")

def messageencryption(key, msg):
    cipher = AES.new(key, AES.MODE_EAX)
    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(msg.encode())
    return nonce, ciphertext, tag

def chatencryption():
    # Load username from file
    with open('username.json', 'r') as file:
        username = json.load(file)['username']

    print("NOW chating with a user.")
    client_id = input("Enter name of user you want to chat with: ")

    # Establish TCP connection
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as chat_socket:
            chat_socket.connect(('localhost', 6001))  # Connect to chat responder
            print("you have successfully connected to chat server.")

            # Generate a random AES key
            key = get_random_bytes(16)

            # Start chat
            while True:
                message = input("Please input message: ")
                if message.lower() == 'exit':
                    break

                nonce, ciphertext, tag = messageencryption(key, message)
                payload = json.dumps({'username': username, 'nonce': nonce.hex(), 'ciphertext': ciphertext.hex(), 'tag': tag.hex()})
                chat_socket.sendall(payload.encode('utf-8'))

    except ConnectionRefusedError:
        print("Chat responder is not available. Please try again later.")
    except Exception as e:
        print(f"Error: {e}")

def unencryptedchat():
    # Load username from file
    with open('username.json', 'r') as file:
        username = json.load(file)['username']

    print("Chatting with a user.")
    client_id = input("Enter the username of the user you want to chat with: ")

    # Establish TCP connection
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as chat_socket:
            chat_socket.connect(('localhost', 6001))  # Connect to chat responder
            print("Connected to chat server.")

            # Start unencrypted chat
            while True:
                message = input("Enter your message: ")
                if message.lower() == 'exit':
                    break

                payload = json.dumps({'username': username, 'unencrypted_message': message})
                chat_socket.sendall(payload.encode('utf-8'))

    except ConnectionRefusedError:
        print("Chat responder is not available. Please try again later.")
    except Exception as e:
        print(f"Error: {e}")

def viewusers():
    print("Viewing users.")
    try:
        with open('users.json', 'r') as file:
            users = json.load(file)['users']
            for user in users:
                print(user)
    except FileNotFoundError:
        print("No users found.")
    except Exception as e:
        print(f"Error: {e}")

def viewhistory():
    print("Viewing chat history.")
    try:
        folder = 'chat_history'
        if os.path.exists(folder):
            files = os.listdir(folder)
            for file in files:
                with open(os.path.join(folder, file), 'r') as chat_log:
                    print(f"Chat history for {file}:")
                    print(chat_log.read())
        else:
            print("No chat history found.")
    except Exception as e:
        print(f"Error: {e}")

def chat_initiator():
    while True:
        menu()
        choice = input("Enter your choice: ")

        if choice == '1':
            chatencryption()
        elif choice == '2':
            unencryptedchat()
        elif choice == '3':
            viewusers()
        elif choice == '4':
            viewhistory()
        elif choice == '5':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    chat_initiator()
