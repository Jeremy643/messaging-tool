from client import Client
from threading import Thread
import time


CONNECT_MSG = '!CONNECT'
DISCONNECT_MSG = '!DISCONNECT'


def connect_user():
    """ Create and return user """
    while True:
        # get user's name
        name = input('Enter your name: ')
        client = Client(name)
        client.send_message(CONNECT_MSG)
        return client

def send_message(client):
    """ Get user message and send it """
    while True:
        msg = input()
        client.send_message(msg)
        if msg == DISCONNECT_MSG:
            break

def receive_message(client):
    while True:
        for new_msg in client.read_messages():
            name, msg = new_msg
            if msg == CONNECT_MSG:
                print(f'<<{name} has connected. Say hello!>>')
            elif msg == DISCONNECT_MSG:
                print(f'<<{name} has disconnected.>>')
            else:
                print(f'{name}> {msg}')

if __name__ == '__main__':
    client = connect_user()
    send_thread = Thread(target=send_message, args=(client,))
    send_thread.start()
    receive_thread = Thread(target=receive_message, args=(client,), daemon=True)
    receive_thread.start()