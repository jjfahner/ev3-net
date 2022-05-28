#!/usr/bin/env python3

#
# Imports
#
from connection import Connection
from local import LocalEV3
from device import Device
from motor import Motor
from trace import Trace

#
# Server class
#
class Server:

    #
    # Members
    #
    __slots__ = [
        '_connection',
        '_ev3',
        '_handlers'
    ]

    #
    # Construction
    #
    def __init__(self):
        self._ev3 = LocalEV3()
        self._connection = Connection()

        # Setup handler map
        self._handlers = {
            'name' :    self.handle_name,
            'get' :     self.handle_get,
            'set' :     self.handle_set
        }

    #
    # Main loop
    #
    def main(self):

        # Listen for connections
        self._connection.listen()

        # Main server loop
        while True:

            # Accept connection
            self._connection.accept()
            
            # Message handler loop
            while True:

                # Receive message
                result, msg = self._connection.recv()
                if not result:
                    break

                # Dispatch message
                self.handle(msg)
            
            # Connection failed
            Trace.Info('Connection closed')

            # Reset the ev3
            self.reset()
            

    #
    # Request handler
    #                    
    def handle(self, msg):

        # Split into parts
        parts = msg.decode().split(':')
        if len(parts) < 1:
            return False

        # Show command
        Trace.Verbose('Executing command', parts)

        # Find handler
        handler = self._handlers.get(parts[0])
        if handler is None:
            raise Exception('No handler for message', parts)

        # Invoke handler
        handler(parts)

    #
    # Handle name message
    #
    def handle_name(self, msg_parts):
        class_name  = msg_parts[1]
        device_name = msg_parts[2]
        self._connection.send(self._ev3.get_name(class_name, device_name))

    #
    # Handle attribute get message
    #
    def handle_get(self, msg_parts):
        name = msg_parts[1]
        attr = msg_parts[2] 
        self._connection.send(self._ev3.get_attribute(name, attr))

    #
    # Handle attribute set message
    #
    def handle_set(self, msg_parts):
        name = msg_parts[1]
        attr = msg_parts[2]
        val  = msg_parts[3] 
        self._ev3.set_attribute(name, attr, val)

    #
    # Reset the ev3
    # - Stop motors
    #
    def reset(self):
        for i in range(0, 4):
            port_name = 'out' + 'ABCD'[i]
            device = Device('tacho-motor', port_name, None, self._ev3)
            if not device.name is None and 'motor' in device.driver_name:
                Trace.Info('Stopping motor', port_name)
                device.command = 'stop'

#
# Run server as script
#
if __name__ == "__main__":

    # Set trace level
    #Trace.level = Trace.TRACE_LEVEL_VERBOSE

    # Enable info tracing
    Trace.Info('Starting ev3-net server...')
    
    # Create server instance
    server = Server()

    # Run server main loop
    server.main()