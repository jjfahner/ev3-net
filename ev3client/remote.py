import socket


################################################################################
#
# Class representing a remote EV3
#
class RemoteEV3:

    #
    # Members
    #
    __slots__ = [
        'remote_ip', 
        'remote_port',
        'socket',
        'recv_buffer'
    ]


    #
    # Construction
    #
    def __init__(self, remote_ip, remote_port):
        
        # Connect to brick
        self.remote_ip = remote_ip
        self.remote_port = remote_port
        self.recv_buffer = bytes()
        self.__connect()

    #
    # Determine name to use for a specific device
    #
    def get_name(self, class_name, device_name):
        self.__send_packet('name' + ':' + class_name + ':' + device_name)
        name = self.__recv_packet().decode()
        if len(name) < 1:
            raise ValueError('Could not find device ' + class_name + ':' + device_name)
        return name

    #
    # Get an attribute
    #
    def get_attribute(self, name, attribute):
        self.__send_packet('get:' + name + '/' + attribute)
        return self.__recv_packet().strip().decode()

    #
    # Set an attribute
    #
    def set_attribute(self, name, attribute, value):
        if not isinstance(value, str):
            value = str(value)
        self.__send_packet('set:' + name + '/' + attribute + ':' + value)

    #
    # Connect to remote ev3
    #
    def __connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.remote_ip, self.remote_port))
        # TODO we probably want a version handshake

    #
    # Send packet
    #
    def __send_packet(self, command):

        # Convert command to bytes
        if isinstance(command, str):
            command = command.encode()

        # Build integer-prefixed command and send it
        data = (len(command) + 4).to_bytes(4, byteorder='little') + command
        self.socket.sendall(data)

    #
    # Recv packet
    #
    def __recv_packet(self):
        
        # Receive data until an entire response is available
        while True:

            # Check the receive buffer for a complete response length
            if len(self.recv_buffer) >= 4:

                # Extract the response length
                data_len = int.from_bytes(self.recv_buffer[:4], byteorder='little')
                if len(self.recv_buffer) >= data_len:

                    # Extract the response
                    data = self.recv_buffer[4:data_len]
                    self.recv_buffer = self.recv_buffer[data_len:]
                    return data

            # Receive more data from the server
            self.recv_buffer += self.socket.recv(1024)
