import socket
import threading


HOST = '127.0.0.1'
PORT = 60000
CLIENT = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

CLIENT.connect((HOST,PORT))

nickname = input("What is your nickname: ")
def receive():
    while True:
        try:
            message = CLIENT.recv(1024).decode('ascii')
            if message == "NICK":
                CLIENT.send(nickname.encode('ascii'))
            else:
                print(message)
        except:
            print("An ERROR occurred!")
            CLIENT.close()
            break


def write():
    while True:
        message = f"{nickname}: {input('')}"
        CLIENT.send(message.encode('ascii'))


receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()