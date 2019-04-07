import socket

def receive_line(socket, remainder = "", line_terminator="\n", buffer_size=1024):
    """Receives one line and returns the line and remainder"""

    while True:
        try:
            msg = socket.recv(buffer_size).decode("utf8")
            pre, sep, tail = msg.partition(line_terminator)
            if sep:
                return (remainder + pre, tail)
            else:
                remainder += pre
        except OSError:
            return (None, remainder)
