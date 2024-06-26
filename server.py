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
            msg = message = client.recv(1024)
            if msg.decode('ascii').startswith('KICK'):
                if nikcnames[clients.index(client)] == 'admin':
                    name_to_kick = msg.decode('ascii')[5:]
                    kick_user(name_to_kick)
                else:
                    client.send('Command was refused'.encode('ascii'))
            elif msg.decode('ascii').startswith('BAN'):
                if nikcnames[clients.index(client)] == 'admin':
                    name_to_ban = msg.decode('ascii')[4:]
                    kick_user(name_to_ban)
                    with open('ban.txt', 'a') as f:
                        f.write(f"{name_to_ban}\n")
                    print(f"{name_to_ban} was banned!")
                else:
                    client.send('Command was refused'.encode('ascii'))
            else:
                broadcast(message)
        except:
            # Removing and closing clients
            if client in clients:
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

        with open('bans.txt', 'r') as f:
            bans = f.readlines()

        if nickname+ '\n' in bans:
            client.send('BAN'.encode('ascii'))
            client.close()
            continue

        if nickname == 'admin':
            client.send('PASS'.encode('ascii'))
            password = client.recv(1024).decode('ascii')

            if password != 'adminpass':
                client.send('REFUSE'.encode('ascii'))
                client.close()
                continue

        nikcnames.append(nickname)
        clients.append(client)

        # Print and broadcast nikcname
        print('Nickname is {}'.format(nickname))
        broadcast("{} joined!".format(nickname).encode('ascii'))
        client.send("connected to server!".encode('ascii'))

        # Start handling thread for client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

def kick_user(name):
    if name in nicknames:
        name_index = nikcnames.index[name]
        client_to_kick = clients[name_index]
        clients.remove[client_to_kick]
        client_to_kick.send('You were kicked by admin!'.encode('ascii'))
        client_to_kick.close()
        nikcnames.remove(name)
        broadcast(f"{name} was kicked by admin!".encode('ascii'))

print('Server is listening..')
recieve()
