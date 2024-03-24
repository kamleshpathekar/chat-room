import socket
import threading


# choosing nickname
nickname = input("Choose your nickname: ")

# Connecting to server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 55555))

# Listening to sevver and sending nickname
def recieve():
    while True:
        try:
            # Recieve message from server
            # If 'NICK' send nickname
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
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
        message = '{} {}'.format(nickname, input(''))
        client.send(message.encode('ascii'))


# Starting thread for listening and Writing
recieve_thread = threading.Thread(target=recieve)
recieve_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()