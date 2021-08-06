import socket
import threading

HOST = '127.0.0.1'
PORT = 60000
SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


SERVER.bind((HOST, PORT))
SERVER.listen()

CLIENTS = []
NICKNAMES = []

def broadcast(message):
    for client in CLIENTS:
        client.send(message)

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = CLIENTS.index(client)
            CLIENTS.remove(client)
            client.close()
            nickname = NICKNAMES[index]
            broadcast(f"{nickname} has left the chat".encode('ascii'))
            print(f"{nickname} has left the chat")
            NICKNAMES.remove(nickname)
            break

def receive():
    while True:
        client, address = SERVER.accept()
        print(f"Connected with {str(address)}")

        client.send("NICK".encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        NICKNAMES.append(nickname)
        CLIENTS.append(client)

        print(f"Nickname of the client is {nickname}")
        broadcast(f"{nickname} joined the chat".encode('ascii'))
        client.send('Connected to server'.encode('ascii'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print('server is listening')
receive()