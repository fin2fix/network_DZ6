#!/bin/python3

# В код добавлена возможность переписки и нейминга полльзователей на русском и многих других языках (из UTF-8)
# а также добавлено логирование чата (построчная запись всех сообщений чата в файл)
import socket
import threading

# Connection Data
host = '10.131.0.34'
port = 55555

# Starting Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# Lists For Clients and Their Nicknames
clients = []
nicknames = []

# Sending Messages To All Connected Clients
def broadcast(message):
    saveHistory(message)
    for client in clients:
        client.send(message)

# ДОБАВЛЕНА ФУНКЦИЯ 
# Saving Chat history into a file
def saveHistory(message):
    try:
        line = message.decode()
        with open("chathistory.txt", "a") as file:
            file.write(line + '\n')
    except:
        print("ERROR: unable to save message into chathistory.txt")

# Handling Messages From Clients
def handle(client):
    while True:
        try:
            # Broadcasting Messages
            message = client.recv(1024)
            broadcast(message)
        except:
            # Removing And Closing Clients
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast('{} left!'.format(nickname).encode('UTF-8'))
            nicknames.remove(nickname)
            break

# Receiving / Listening Function
def receive():
    while True:
        # Accept Connection
        client, address = server.accept()
        print("Connected with {}".format(str(address)))

        # Request And Store Nickname
        client.send('NICK'.encode('UTF-8'))
        nickname = client.recv(1024).decode('UTF-8')
        nicknames.append(nickname)
        clients.append(client)

        # Print And Broadcast Nickname
        print("Nickname is {}".format(nickname))
        broadcast("{} joined!".format(nickname).encode('UTF-8'))
        client.send('Connected to server!'.encode('UTF-8'))

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print("Server if listening...")
receive()
