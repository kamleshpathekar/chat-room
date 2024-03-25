import socket
import threading


# choosing nickname
nickname = input("Choose your nickname: ")
if nickname == 'admin':
    password = input('Enter a password for admin: ')


# Connecting to server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 55555))

stop_thread = False

# Listening to sevver and sending nickname
def recieve():
    while True:
        global stop_thread
        if stop_thread:
            break
        try:
            # Recieve message from server
            # If 'NICK' send nickname
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
                next_message = client.recv(1024).decode('ascii')
                if next_message == 'PASS':
                    client.send(password.encode('ascii'))
                    if client.recv(1024).decode('ascii') == 'REFUSE':
                        print('Connection was refused! Wrong password!')
                        stop_thread = True
            else:
                print(message)
        except:
            # Close Connection when error
            print("An eeror occured!")
            client.close()
            break

# Sending message to server
def write():
    while True:
        if stop_thread:
            break
        message = '{} {}'.format(nickname, input(''))
        if message[len(nickname)+2:].startswith('/'):
            if nickname =='admin':
                if message[len(nickname)+2:].startswith('/kick'):
                    client.send(f'KICK {message[len(nickname)+2+6:]}'.encode('ascii'))
                elif message[len(nickname)+2:].startswith('/ban'):
                    client.send(f'KICK {message[len(nickname)+2+5:]}'.encode('ascii'))
        else:
            client.send(message.encode('ascii'))


# Starting thread for listening and Writing
recieve_thread = threading.Thread(target=recieve)
recieve_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()