from ev3client.device import Device


#
# Sensor base class
#
class Sensor(Device):

    #
    # Construction
    #
    def __init__(self, remote_ip, remote_port, name_pattern='*'):
        super(Sensor, self).__init__(remote_ip, remote_port, 'lego-sensor', name_pattern)


    #
    # Attributes
    #
    decimals    = property(fget = lambda self : self.get_cached_attribute('decimals'))
    mode        = property(fget = lambda self : self.get_attribute('mode'), fset = lambda self, mode : self.set_attribute('mode', mode))
    modes       = property(fget = lambda self : self.get_cached_attribute('modes'))
    num_values  = property(fget = lambda self : int(self.get_attribute('num_values')))

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
# Color sensor
#
class ColorSensor(Sensor):

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
    def __init__(self, remote_ip, remote_port, device_name):
        super(ColorSensor, self).__init__(remote_ip, remote_port, device_name)
        if self.driver_name != 'lego-ev3-color':
            raise ValueError('Sensor is not a color sensor')

    #
    # color
    #
    color = property(fget = lambda self : self.value())


#
# Gyro sensor
#
class GyroSensor(Sensor):

    #
    # Mode strings
    #
    MODE_GYRO_ANG   = 'GYRO-ANG'
    MODE_GYRO_RATE  = 'GYRO-RATE'
    MODE_GYRO_FAS   = 'GYRO-FAS'
    MODE_GYRO_GA    = 'GYRO-G&A'
    MODE_GYRO_CAL   = 'GYRO-CAL'
    MODE_TILT_RATE  = 'TILT-RATE' 
    MODE_TILT_ANG   = 'TILT-ANG'

    #
    # Mode list
    #
    Modes = (MODE_GYRO_ANG, MODE_GYRO_RATE, MODE_GYRO_FAS, MODE_GYRO_GA, MODE_GYRO_CAL, MODE_TILT_RATE, MODE_TILT_ANG) 

    #
    # Construction
    #
    def __init__(self, remote_ip, remote_port, device_name):
        super(GyroSensor, self).__init__(remote_ip, remote_port, device_name)
        if self.driver_name != 'lego-ev3-gyro':
            raise ValueError('Sensor is not a gyro sensor')
