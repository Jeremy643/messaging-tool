from socket import socket, AF_INET, SOCK_STREAM, gethostbyname, gethostname
from threading import Thread, Lock
import pickle


class Client:

    SERVER = gethostbyname(gethostname())
    PORT = 5050
    ADDR = (SERVER, PORT)
    BUFSIZ = 512
    HEADER = 10

    def __init__(self, name):
        self.name = name
        self.new_messages = []
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        # self.client_socket.bind(self.ADDR)
        self.client_socket.connect(self.ADDR)
        self.receive_thread = Thread(target=self.receive_messages)
        self.receive_thread.start()
        self.lock = Lock()
    
    def __repr__(self):
        return f'{self.__class__.__name__}({self.name})'
    
    def read_messages(self):
        """ Return and then clear new messages. """
        for i in range(len(self.new_messages)):
            yield self.new_messages.pop(0)
    
    def receive_messages(self):
        """ Receive all messages sent from the server. """
        connected = True
        while connected:
            full_msg = b''
            first_msg = True
            while True:
                received_msg = self.client_socket.recv(self.BUFSIZ)
                if received_msg:
                    if first_msg:
                        msg_len = int(received_msg[:self.HEADER])
                        first_msg = False
                    
                    full_msg += received_msg

                    if (len(full_msg) - self.HEADER) == msg_len:
                        client_msg = pickle.loads(full_msg[self.HEADER:])
                        self.lock.acquire()
                        self.new_messages.append(client_msg)
                        self.lock.release()
                        first_msg = True
                        break
                else:
                    connected = False
                    break

    def send_message(self, msg):
        '''
        Send the user's message to the server.
        Parameter:
        msg (string): The user's message.
        '''
        msg = pickle.dumps((self.name, msg))
        send_msg = bytes(f'{len(msg):<{self.HEADER}}', 'utf-8') + msg
        self.client_socket.send(send_msg)