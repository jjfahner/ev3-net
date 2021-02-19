#
# This is the client part of the ev3 network interface
#

import socket
import time


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
    # Dictionary holding instances of remote EV3s
    #
    __instance_dict = { }


    #
    # Get a remote EV3 instance for a specific IP and port
    #
    @staticmethod
    def get_instance(remote_ip, remote_port):

        # Combine ip and port into key and find existing instance
        key = remote_ip + ':' + str(remote_port)
        val = RemoteEV3.__instance_dict.get(key)

        # If not found, create an instance and cache it
        if val == None:
            val = RemoteEV3(remote_ip, remote_port)
            RemoteEV3.__instance_dict[key] = val

        return val


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
        return self.__recv_packet().decode()

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


    #
    # Connect to remote ev3
    #
    def __connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.remote_ip, self.remote_port))
        # TODO we probably want a version handshake


#
# Class representing a remote device
#
class Device:

    #
    # Member data
    #
    __slots__ = [
        '_ev3',
        '_name',
        '_cache'
    ]


    #
    # Construction
    #
    def __init__(self, remote_ip, remote_port, class_name, device_name):        
        self._ev3   = RemoteEV3.get_instance(remote_ip, remote_port)
        self._name  = self._ev3.get_name(class_name, device_name)
        self._cache = {}

    #
    # Get an attribute
    #
    def get_attribute(self, attribute):
        return self._ev3.get_attribute(self._name, attribute)

    #
    # Get an attribute as int
    #
    def get_attribute_int(self, attribute):
        return int(self.get_attribute(attribute))

    #
    # Set an attribute
    #
    def set_attribute(self, attribute, value):
        return self._ev3.set_attribute(self._name, attribute, value)

    #
    # Get cached attribute
    #
    def get_cached_attribute(self, attribute):
        value = self._cache.get(attribute)

        if value == None:
            value = self.get_attribute(attribute)
            self._cache[attribute] = value

        return value

    #
    # Clear a cached attribute
    #
    def clear_cached_attribute(self, attribute):
        self._cache.pop(attribute, None)

    #
    # Attributes
    #
    address     = property(fget = lambda self : self.get_cached_attribute('address'))
    command     = property(fset = lambda self, value : self.set_attribute('command', value))
    commands    = property(fget = lambda self : self.get_cached_attribute('commands'))
    driver_name = property(fget = lambda self : self.get_cached_attribute('driver_name'))



