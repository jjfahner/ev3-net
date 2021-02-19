import io
import os
import stat
from ev3client.trace import Trace

################################################################################
#
# Class representing a local EV3
#
class LocalEV3:

    #
    # Members
    #
    __slots__ = [
        '_attrs'
    ]

    #
    # Construction
    #
    def __init__(self):
        self._attrs = {}


    #
    # Determine name to use for a specific device
    #
    def get_name(self, class_name, device_name):

        path_root  = '/sys/class/'
        class_path = path_root + class_name

        for subdir in os.listdir(class_path):
            
            device_path = class_path + '/' + subdir
            Trace.Verbose(device_path)
            
            with io.FileIO(device_path + '/address') as f:
                address = f.read().strip().decode()
            
            if device_name in address:
                return class_name + '/' + subdir
        
        return None

    #
    # Get an attribute
    #
    def get_attribute(self, name, attribute):
        
        # Get handle to device
        handle = self.__get_handle(name, attribute)
        if handle == None:
            return None

        # Read and return value
        try:
            return handle.read().strip().decode()
        except Exception as ex:
            Trace.Warning('Read failed on', name, ex)
            return None

    #
    # Set an attribute
    #
    def set_attribute(self, name, attribute, value):

        # Obtain handle to device
        handle = self.__get_handle(name, attribute)
        if handle == None:
            return False

        # Convert to bytes
        if not isinstance(value, bytes):
            if isinstance(value, str):
                value = value.encode()
            else:
                value = str(value).encode()
        
        # Try to execute command
        try:
            handle.write(value)
            handle.flush()
            return True
        except Exception as ex:
            Trace.Warning("Write failed on", name, ex)
            return False

    #
    # Get handle to attribute
    #
    def __get_handle(self, name, attribute):
        
        # Build full name
        full_name = '/sys/class/' + name + '/' + attribute

        # Retrieve from cached handles
        handle = self._attrs.get(full_name)
        if handle != None:
            handle.seek(0)
            return handle

        # Inspect the device
        try:
            mode = stat.S_IMODE(os.stat(full_name)[stat.ST_MODE])
        except:
            Trace.Warning('Cannot stat', full_name)
            return None

        # Determine mode flags
        r_ok = mode & stat.S_IRGRP
        w_ok = mode & stat.S_IWGRP
        if r_ok and w_ok:
            mode_str = 'r+'
        elif w_ok:
            mode_str = 'w'
        elif r_ok:
            mode_str = 'r'
        else:
            Trace.Warning('Cannot access', full_name)
            return None

        # Open the device
        try:
            handle = io.FileIO(full_name, mode_str)
        except:
            Trace.Warning("Cannot open", full_name)
            return None

        # Cache the handle and return it
        self._attrs[full_name] = handle
        return handle
