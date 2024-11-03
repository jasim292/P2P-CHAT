import json
import socket
from datetime import datetime

def peer_discovery():
    members = {}
    file_path = 'members.json'
    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen_socket.bind(('', 6000))
    print("listening new broadcasts...")

    while True:
        message, addr = listen_socket.recvfrom(2048)
        data = json.loads(message.decode())
        username = data.get('username')
        public_key = data.get('public_key', 'Not Available')
        ip = addr[0]
        members[username] = {'ip': ip, 'public_key': public_key, 'last_seen': datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

        with open(file_path, 'w') as file:
            json.dump(members, file, indent=4)

        print("Updated list of peers:")
        for member, info in members.items():
            print(f"Username: {member}, IP: {info['ip']}, Public Key: {info['public_key']}, Last Seen: {info['last_seen']}")

if __name__ == "__main__":
    peer_discovery()
