from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import arcade
import util


class ClientWindow(arcade.Window):
    PORT = 33001
    BUFSIZ = 1024

    def __init__(self, host, name, width, height, title='Client'):
        super().__init__(width, height, title)

        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.client_socket.connect((host, self.PORT))

        self.receive_thread = Thread(target=self.receive, args=(name,))
        self.receive_thread.start()

    def close(self):
        self.send('{quit}')
        self.receive_thread.join()
        super().close()

    def receive(self, name):
        """Handles receiving of messages."""
        self.send(name)
        remainder = ""
        while True:
            (msg, remainder) = util.receive_line(self.client_socket, remainder)
            if msg:
                if msg == '{quit}':
                    break
                else:
                    self.on_message_received(line)

        self.client_socket.close()
        self.client_socket = None
        self.on_message_received('disconnected')

    def send(self, msg):
        """Handles sending of messages."""
        if self.client_socket is not None:
            self.client_socket.sendall(bytes(msg+"\n", "utf8"))

    def on_message_received(self, message):
        pass
