from ev3client.device import Device


################################################################################
#
# Sensor base class
#
class Sensor(Device):

    #
    # Construction
    #
    def __init__(self, device_name, driver_name, ev3_instance = None):
        super(Sensor, self).__init__('lego-sensor', device_name, driver_name, ev3_instance)

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


################################################################################
#
# Color sensor
#
class ColorSensor(Sensor):

    #
    # Driver name
    #
    DRIVER_NAME         = 'lego-ev3-color'

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
    def __init__(self, device_name, ev3_instance = None):
        super(ColorSensor, self).__init__(device_name, ColorSensor.DRIVER_NAME, ev3_instance)

    #
    # color
    #
    color = property(fget = lambda self : self.value())


################################################################################
#
# Gyro sensor
#
class GyroSensor(Sensor):

    #
    # Driver name
    #
    DRIVER_NAME         = 'lego-ev3-gyro'

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
    def __init__(self, device_name, ev3_instance = None):
        super(GyroSensor, self).__init__(device_name, GyroSensor.DRIVER_NAME, ev3_instance)


################################################################################
#
# Touch sensor
#
class TouchSensor(Sensor):

    #
    # Driver name
    #
    DRIVER_NAME     = 'lego-ev3-touch'

    #
    # Mode strings
    #
    MODE_TOUCH      = 'TOUCH'

    #
    # Mode list
    #
    Modes = (MODE_TOUCH) 

    #
    # Construction
    #
    def __init__(self, device_name, ev3_instance = None):
        super(TouchSensor, self).__init__(device_name, TouchSensor.DRIVER_NAME, ev3_instance)


################################################################################
#
# Ultrasonic sensor
#
class UltrasonicSensor(Sensor):

    #
    # Driver name
    #
    DRIVER_NAME         = 'lego-nxt-us'

    #
    # Mode strings
    #
    MODE_US_DIST_CM = 'US-DIST-CM'
    MODE_US_DIST_IN = 'US-DIST-IN'
    MODE_US_SI_CM   = 'US-SI-CM'
    MODE_US_SI_IN   = 'US-SI-IN'
    MODE_US_LISTEN  = 'US-LISTEN'

    #
    # Mode list
    #
    Modes = (MODE_US_DIST_CM, MODE_US_DIST_IN, MODE_US_SI_CM, MODE_US_SI_IN, MODE_US_LISTEN) 

    #
    # Construction
    #
    def __init__(self, device_name, ev3_instance = None):
        super(UltrasonicSensor, self).__init__(device_name, UltrasonicSensor.DRIVER_NAME, ev3_instance)
