import socket
import json
import time
from datetime import datetime

# Constants
CLOCK_GAP = 8  # seconds
# Ensure that DESTINATION_IP is your network's broadcast address; adjust as necessary.
FINAL_IP = "192.168.1.255"
FINAL_PORT = 6000

# Helper function to generate a current timestamp for logging
def timenow():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Function to store the username in a JSON file
def save_username(username):
    with open('username.json', 'w') as file:
        json.dump({"username": username}, file)

# Function to load the username from the JSON file if it exists
def loadusername():
    try:
        with open('username.json', 'r') as file:
            data = json.load(file)
            return data['username']
    except FileNotFoundError:
        print("No username.json file found.")
        return None

# Service Announcer function
def service_announcer():
    username = input("Please input your username: ")
    save_username(username)

    # Create a UDP socket for sending announcements
    broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    while True:
        # Create a message in JSON format
        message = json.dumps({"username": username})

        # Send the message to the specific IP address and port
        broadcast_socket.sendto(message.encode(), (FINAL_IP, FINAL_PORT))

        # Print a confirmation message with the current timestamp
        print(f"{timenow()}: Announced presence to {FINAL_IP}:{FINAL_PORT}.")

        # Pause before sending the next announcement
        time.sleep(CLOCK_GAP)

# Execute the service announcer if this script is run directly
if __name__ == "__main__":
    service_announcer()
