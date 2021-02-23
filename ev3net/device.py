#
# This is the client part of the ev3 network interface
#
from local  import LocalEV3
from remote import RemoteEV3 


################################################################################
#
# Class representing a remote EV3
#
class EV3:

    #
    # Dictionary holding instances of remote EV3s
    #
    __instance_dict = { }

    #
    # Local instance
    #
    __local_instance = None

    #
    # Default instance, used if no connection details are supplied to a device
    #
    __default_instance = None

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
    def set_default_instance(instance):
        RemoteEV3.__default_instance = instance

    #
    # Get the local instance
    #
    @staticmethod
    def get_local_instance():

        # Create first time
        if EV3.__local_instance == None:
            EV3.__local_instance = LocalEV3()

        # Return the instance
        return EV3.__local_instance

    #
    # Get a remote EV3 instance for a specific IP and port, or the default
    #
    @staticmethod
    def get_remote_instance(remote_ip, remote_port):
        
        # Combine ip and port into key and find existing instance
        key = remote_ip + ':' + str(remote_port)
        instance = EV3.__instance_dict.get(key)

        # If not found, create an instance and cache it
        if instance == None:
            instance = RemoteEV3(remote_ip, remote_port)
            EV3.__instance_dict[key] = instance

        # Return the instance
        return instance


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
    def __init__(self, class_name, device_name, driver_name, ev3_instance = None):        
        
        # Initialize attribute cache
        self._cache = {}

        # Get EV3 instance
        self._ev3 = ev3_instance if not ev3_instance == None else EV3.get_default_instance()
        
        # Get name, then match the driver name 
        self._name  = self._ev3.get_name(class_name, device_name)
        if self.driver_name != driver_name:
            raise ValueError('Expected driver name ' + str(driver_name) + ', got ' + str(self.driver_name))

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
