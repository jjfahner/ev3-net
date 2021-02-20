#
# Imports
#
from socket import SocketIO, socket, AF_INET, SOCK_STREAM
from trace import Trace

class Connection:

    __slots__ = [
        '_listen_socket',
        '_client_socket',
        '_remote_address',
        '_recv_buffer'
    ]

    #
    # Default port
    #
    DEFAULT_PORT = 44444

    #
    # Construction
    #
    def __init__(self):
        pass

    #
    # Listen for connections
    #
    def listen(self, address = '0.0.0.0', port = DEFAULT_PORT):
        self._listen_socket = socket(AF_INET, SOCK_STREAM)
        self._listen_socket.bind((address, port))
        self._listen_socket.listen()
        Trace.Info('Listening on', address, ':', port)

    #
    # Accept connection
    #
    def accept(self):

        # Release existing client socket
        self._client_socket = None

        # Clear receive buffer
        self._recv_buffer = bytes()
        
        # Accept new connection
        self._client_socket, self._remote_address = self._listen_socket.accept()
        Trace.Info('Connection from', self._remote_address)

        # Mark socket blocking
        self._client_socket.setblocking(True)

    #
    # Establish connection
    #
    def connect(self, address, port = DEFAULT_PORT):
        # Clear receive buffer
        self._recv_buffer = bytes()

        # Create new socket and connect        
        self._client_socket = socket(AF_INET, SOCK_STREAM)
        self._client_socket.connect((address, port))

        # Mark socket blocking
        self._client_socket.setblocking(True)

    # Send packet
    def send(self, msg, *args):

        # Combine message and arguments
        parts = list()
        parts.append(msg)
        parts.extend(args)

        # Join all argument parts as trimmed strings, and encode
        msg = ':'.join(map(lambda v : str(v).strip(), parts)).encode()

        # Compose packet
        data = (len(msg) + 4).to_bytes(4, byteorder='little') + msg
        
        # Send packet
        self._client_socket.sendall(data)

    # Receive packet
    def recv(self):

        # Receive data until an entire response is available
        while True:

            # Check the receive buffer for a complete response length
            if len(self._recv_buffer) >= 4:

                # Extract the response length
                data_len = int.from_bytes(self._recv_buffer[:4], byteorder='little')
                if len(self._recv_buffer) >= data_len:

                    # Extract the response
                    data = self._recv_buffer[4:data_len]
                    self._recv_buffer = self._recv_buffer[data_len:]
                    return True, data

            # Receive more data from the server
            try:
                received = self._client_socket.recv(1024)
                if len(received) == 0:
                    return False, None
            except:
                return False, None

            # Append to buffer
            self._recv_buffer += received
