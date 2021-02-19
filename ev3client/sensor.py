from ev3client.device import Device

#
# Color sensor
#
class ColorSensor(Device):

    #
    # Mode strings
    #
    MODE_COL_AMBIENT    = 'COL-AMBIENT'
    MODE_COL_COLOR      = 'COL-COLOR'
    MODE_COL_REFLECT    = 'COL-REFLECT'
    MODE_REF_RAW        = 'REF-RAW'
    MODE_RGB_RAW        = 'RGB-RAW'

    #
    # Mode list
    #
    Modes = (MODE_COL_AMBIENT, MODE_COL_COLOR, MODE_COL_REFLECT, MODE_RGB_RAW, MODE_REF_RAW) 
    
    #
    # Colors
    #
    COLOR_NOCOLOR   = 0
    COLOR_BLACK     = 1
    COLOR_BLUE      = 2
    COLOR_GREEN     = 3
    COLOR_YELLOW    = 4
    COLOR_RED       = 5
    COLOR_WHITE     = 6
    COLOR_BROWN     = 7

    #
    # Color names
    #
    Colors = ('None', 'Black', 'Blue', 'Green', 'Yellow', 'Red', 'White', 'Brown')

    #
    # Construction
    #
    def __init__(self, remote_ip, remote_port, class_name, name_pattern='*'):
        super(ColorSensor, self).__init__(remote_ip, remote_port, class_name, name_pattern)
        if self.driver_name != 'lego-ev3-color':
            raise ValueError('Sensor is not a color sensor')

    #
    # color
    #
    color = property(fget = lambda self : self.value())

    #
    # Value
    #
    def value(self, index = 0):
        return self.get_attribute_int('value' + str(index))

    #
    # Get all values
    #
    def get_values(self):
        values = []
        for i in range(0, self.num_values):
            values.append(self.value(i))
        return values
    values = property(fget = lambda self : self.get_values())

    #
    # Set mode
    #
    def set_mode(self, value):
        self.set_attribute('mode', value)
        self.clear_cached_attribute('num_values')

    #
    # Mode property
    #
    mode = property(
        fget = lambda self : self.get_attribute('mode'), 
        fset = lambda self, mode : self.set_mode(mode))

    #
    # Get number of values
    #
    num_values = property(fget = lambda self : int(self.get_cached_attribute('num_values')))
