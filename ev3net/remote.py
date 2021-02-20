from connection import Connection

################################################################################
#
# Class representing a remote EV3
#
# TODO why the strip everywhere?
#
class RemoteEV3:

    #
    # Members
    #
    __slots__ = [
        '_connection'
    ]


    #
    # Construction
    #
    def __init__(self, remote_ip, remote_port=Connection.DEFAULT_PORT):
        self._connection = Connection()
        self._connection.connect(remote_ip, remote_port)

    #
    # Determine name to use for a specific device
    #
    def get_name(self, class_name, device_name):
        
        # Send message
        self._connection.send('name', class_name, device_name)
        
        # Receive response
        result, data = self._connection.recv()
        if not result:
            raise ValueError('Could not find device ' + class_name + ':' + device_name)

        # Return data
        return data.strip().decode()

    #
    # Get an attribute
    #
    def get_attribute(self, name, attribute):
        
        # Send message
        self._connection.send('get', name, attribute)
        
        # Receive response
        result, data = self._connection.recv()
        if not result:
            raise ValueError('Connection closed')
        
        # Return data
        return data.strip().decode()

    #
    # Set an attribute
    #
    def set_attribute(self, name, attribute, value):
        
        # Send message
        self._connection.send('set', name, attribute, value)
