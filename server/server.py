from socket import socket, AF_INET, SOCK_STREAM, gethostbyname, gethostname
from threading import Thread, Lock
from person import Person
import pickle


SERVER = gethostbyname(gethostname())
PORT = 5050
ADDR = (SERVER, PORT)
BUFSIZ = 512
HEADER = 10
LOCK = Lock()
CONNECT_MSG = '!CONNECT'
DISCONNECT_MSG = '!DISCONNECT'

people = []
server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind(ADDR)


def broadcast(msg, name):
    """ Send new messages to all users, except to the user who sent the message. """
    for person in people:
        if person.name == name:
            continue
        else:
            send_msg = pickle.dumps((name, msg))
            send_msg = bytes(f'{len(send_msg):<{HEADER}}', 'utf-8') + send_msg
            person.client.send(send_msg)


def receive_messages(person):
    """ Listens for new messages from users. """
    new_msg = True
    connected = True
    while connected:
        full_msg = b''
        while True:
            received_msg = person.client.recv(BUFSIZ)
            if received_msg:
                if new_msg:
                    msg_len = int(received_msg[:HEADER])
                    new_msg = False
                
                full_msg += received_msg

                if (len(full_msg) - HEADER) == msg_len:
                    client_name, msg = pickle.loads(full_msg[HEADER:])
                    new_msg = True
                    break

        if not person.name:
            person.name = client_name
        
        print(f'[{client_name}] {msg}')

        if msg == DISCONNECT_MSG:
            LOCK.acquire()
            people.remove(person)
            LOCK.release()
            print(f'[DISCONNECTED] {person.address}')
            connected = False

        broadcast(msg, client_name)
    
    person.client.close()

def client_communication():
    """ The server will run until manually switched off. """
    while True:
        conn, addr = server_socket.accept()
        print(f'[CONNECTED] {addr}')
        person = Person(conn, addr)
        client_thread = Thread(target=receive_messages, args=(person,))
        client_thread.start()
        
        LOCK.acquire()
        people.append(person)
        LOCK.release()

if __name__ == '__main__':
    server_socket.listen()
    print('[STARTING] ...')
    print(f'[LISTENING] {SERVER}')

    communication_thread = Thread(target=client_communication)
    communication_thread.start()
    communication_thread.join()