import threading
import socket

host = "127.0.0.1" #localhost

port = 55555

#starting a server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

#Lists for the clients and their nikcnames
clients = []
nikcnames = []

# sending messages to all connected users
def broadcast(messages):
    for client in clients:
        client.send(messages)

# handling messages from client
def handle(client):
    while True:
        try:
            # Broadcasting Messages
            message = client.recv(1024)
            broadcast(message)
        except:
            # Removing and closing clients
            index = client.index(client)
            clients.remove(client)
            client.close()
            nikcname = nikcnames[index]
            broadcast('{} left!'.format(nikcname).encode('ascii'))
            nikcnames.remove(nikcname)
            break
    

# Recieving / Listening Function
def recieve():
    while True:
        # Accept connection
        client, address = server.accept()
        print('connected with {}'.format(str(address)))

        # request and store nickname
        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nikcnames.append(nickname)
        clients.append(client)

        # Print and broadcast nikcname
        print('Nickname is {}'.format(nickname))
        broadcast("{} joined!".format(nickname).encode('ascii'))
        client.send("connected to server!".encode('ascii'))

        # Start handling thread for client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print('Server is listening..')
recieve()