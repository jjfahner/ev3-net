#
# This is the client part of the ev3 network interface
#

import socket
import time


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
    # Dictionary holding instances of remote EV3s
    #
    __instance_dict = { }


    #
    # Default instance, used if no connection details are supplied to a device
    #
    __default_instance = None


    #
    # Get a remote EV3 instance for a specific IP and port, or the default
    #
    @staticmethod
    def get_instance(remote_ip, remote_port):
        
        # If empty, use the default instance
        if remote_ip == None:
            instance = RemoteEV3.get_default_instance()
        else:
            # Combine ip and port into key and find existing instance
            key = remote_ip + ':' + str(remote_port)
            instance = RemoteEV3.__instance_dict.get(key)

            # If not found, create an instance and cache it
            if instance == None:
                instance = RemoteEV3(remote_ip, remote_port)
                RemoteEV3.__instance_dict[key] = instance

        # If no instance, fail
        if instance == None:
            raise ValueError('No IP address specified, and no default instance available')

        # Return the instance
        return instance

    #
    # Get the default instance
    #
    @staticmethod
    def get_default_instance():
        return RemoteEV3.__default_instance

    #
    # Set the default instance
    #
    @staticmethod
    def set_default_instance(remote_ip, remote_port):
        RemoteEV3.__default_instance = RemoteEV3.get_instance(remote_ip, remote_port)

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


################################################################################
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
    def __init__(self, class_name, device_name, driver_name, remote_ip = None, remote_port = None):        
        
        # Initialize attribute cache
        self._cache = {}

        # Get remote EV3 instance
        self._ev3 = RemoteEV3.get_instance(remote_ip, remote_port)
        
        # Get name, then match the driver name 
        self._name  = self._ev3.get_name(class_name, device_name)
        if self.driver_name != driver_name:
            raise ValueError('Expected driver name ' + driver_name + ', got ' + self.driver_name)

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
