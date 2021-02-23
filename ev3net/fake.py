import io
import os
import stat
from trace import Trace
from motor import Motor

################################################################################
#
# Class representing a fake EV3
#
class FakeEV3:

    #
    # Valid inputs
    #
    INPUT_1 = 'in1'
    INPUT_2 = 'in2'
    INPUT_3 = 'in3'
    INPUT_4 = 'in4'    
    INPUTS  = [INPUT_1, INPUT_2, INPUT_3, INPUT_4]

    #
    # Valid outputs
    #
    OUTPUT_A = 'outA'
    OUTPUT_B = 'outB'
    OUTPUT_C = 'outC'
    OUTPUT_D = 'outD'
    OUTPUTS  = [OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D]
    
    #
    # Members
    #
    __slots__ = [
        '_attrs',
        '_motors',
        '_sensors',
        '_devices',
        '_motor_counter',
        '_sensor_counter'
    ]

    #
    # Construction
    #
    def __init__(self):
        self._attrs     = {}
        self._motors    = {}
        self._sensors   = {}
        self._devices   = {}

        self._motor_counter     = 0
        self._sensor_counter    = 0

    #
    # Add a motor
    #
    def add_motor(self, motor, port):

        # Check port name
        if not port in FakeEV3.OUTPUTS:
            raise ValueError('Invalid output name', port) 

        # Check object type
        if not isinstance(motor, FakeMotor):
            raise ValueError('Adding invalid object of type', motor.__class__.__name__, 'as motor')

        # Make name
        name = 'tacho-motor/motor' + str(self._motor_counter)
        self._motor_counter += 1

        # Set port and name attributes
        motor.add_attribute(FakeAttribute('port',       port, settable = False))
        motor.add_attribute(FakeAttribute('name',       name, settable = False))
        motor.add_attribute(FakeAttribute('address',    name, settable = False))

        # Register motor
        self._motors[port] = motor
        self._devices[name] = motor

    #
    # Add a sensor
    #
    def add_sensor(self, sensor, port):

        # Check port name
        if not port in FakeEV3.INPUTS:
            raise ValueError('Invalid input name', port)

        # Check object type
        if not isinstance(sensor, FakeSensor):
            raise ValueError('Adding invalid object of type ', sensor.__class__.__name__, 'as sensor')

        # Make name
        name = 'lego-sensor/sensor' + str(self._sensor_counter)
        self._sensor_counter += 1

        # Set port and full name
        sensor.add_attribute(FakeAttribute('port',      port, settable = False))
        sensor.add_attribute(FakeAttribute('name',      name, settable = False))
        sensor.add_attribute(FakeAttribute('address',   name, settable = False))

        # Register sensor
        self._sensors[port] = sensor
        self._devices[name] = sensor

    #
    # Determine name to use for a specific device
    #
    def get_name(self, class_name, device_name):
        
        # Check motors
        if class_name == 'tacho-motor':
            motor = self._motors.get(device_name)
            return None if motor is None else motor.get_attribute('name')
 
        # Check sensors
        if class_name == 'lego-sensor':
            sensor = self._sensors.get(device_name)
            return None if sensor is None else sensor.get_attribute('name')
        
        # Unknown device
        return None

    #
    # Get an attribute
    #
    def get_attribute(self, name, attribute):
        
        # Get device
        device = self._devices.get(name)
        if device is None:
            Trace.Warning('Getting', attribute, 'from unknown device', name)
            return None

        # Pass to device
        return device.get_attribute(attribute)

    #
    # Set an attribute
    #
    def set_attribute(self, name, attribute, value):

        # Get device
        device = self._devices.get(name)
        if device is None:
            Trace.Warning('Setting', attribute, 'from unknown device', name)
            return None

        # Pass to device
        return device.set_attribute(attribute, value)


################################################################################
#
# Class representing an attribute
#
class FakeAttribute:

    __slots__ = [
        '_name',
        '_value',
        '_gettable',
        '_settable'
    ]

    def __init__(self, name, value = None, gettable = True, settable = True):
        self._name      = name
        self._value     = value
        self._gettable  = gettable
        self._settable  = settable

    name        = property(fget = lambda self : self._name)
    gettable    = property(fget = lambda self : self._gettable)
    settable    = property(fget = lambda self : self._settable)

    def get(self):
        return self._value

    def set(self, value):
        self._value = value



################################################################################
#
# Class representing an attribute that uses lambdas for get/set
#
class FakeLambdaAttribute(FakeAttribute):

    __slots__ = [
        '_get',
        '_set'
    ]
    
    def __init__(self, name, get = None, set = None):
        super(FakeLambdaAttribute, self).__init__(name, None, get is not None, set is not None)
        self._get = get
        self._set = set

    def get(self):
        return self._get()

    def set(self, value):
        self._set(value)


################################################################################
#
# Class representing a fake integer attribute
#
class FakeIntAttribute(FakeAttribute):

    __slots__ = [
        '_min_val',
        '_max_val'
    ]

    def __init__(self, name, value = None, min_val = None, max_val = None, gettable = True, settable = True):
        super(FakeIntAttribute, self).__init__(name, value, gettable, settable)
        self._min_val = min_val
        self._max_val = max_val

    def get(self):
        return int(super(FakeIntAttribute, self).get())

    def set(self, value):
        if not isinstance(value, int):
            value = int(value)

        if not self._min_val is None and value < self._min_val:
            Trace.Warning('Attempt to set invalid value', str(value), 'on attribute', self.name)
            return

        if not self._max_val is None and value > self._max_val:
            Trace.Warning('Attempt to set invalid value', str(value), 'on attribute', self.name)
            return

        super(FakeIntAttribute, self).set(value)


################################################################################
#
# Class representing a fake enum attribute
#
class FakeEnumAttribute(FakeAttribute):

    __slots__ = [
        '_values',
        '_min_val',
        '_max_val'
    ]

    def __init__(self, name, values, value, gettable = True, settable = True):
        super(FakeEnumAttribute, self).__init__(name, value, gettable, settable)
        self._values = values

    def set(self, value):

        if not value in self._values:
            Trace.Warning('Attempt to set invalid value', str(value), 'on attribute', self.name)
            return

        super(FakeEnumAttribute, self).set(value)



################################################################################
#
# Class representing a fake device
#
class FakeDevice:
    
    __slots__ = [
        '_name',
        '_port',
        '_attrs'
    ]

    #
    # Construction
    #
    def __init__(self):
        self._attrs = {}

    #
    # Get an attribute
    #
    def get_attribute(self, attribute):
        
        # Get attribute
        attr = self._attrs.get(attribute)
        if attr is None:
            Trace.Warning('Attempt to get non-existing attribute', attribute)
            return None

        # Check access
        if not attr.gettable:
            Trace.Warning('Attempt to get set-only attribute', attribute)
            return None

        # Return the attribute value
        return attr.get()

    #
    # Set an attribute
    #
    def set_attribute(self, attribute, value):

        # Get attribute
        attr = self._attrs.get(attribute)
        if attr is None:
            Trace.Warning('Attempt to set non-existing attribute', attribute)
            return None

        # Check access
        if not attr.settable:
            Trace.Warning('Attempt to get set-only attribute', attribute)
            return None

        # Set the attribute value
        return attr.set(value)

    #
    # Add an attribute
    #
    def add_attribute(self, attribute):
        self._attrs[attribute.name] = attribute



################################################################################
#
# Class representing a fake motor
#
class FakeMotor(FakeDevice):

    #
    # Member data
    #
    __slots__ = [
        '_handlers',
        '_command',
        '_state'
    ]
    
    #
    # Construction
    #
    def __init__(self):

        # Construct base class first
        super(FakeMotor, self).__init__()

        # Setup members
        self._command   = ''
        self._state     = ''

        # Add state command
        self.add_attribute(FakeLambdaAttribute('state', get = self.get_state))

        # Add commands attribute, use the ones defined in Motor
        self.add_attribute(FakeLambdaAttribute('commands', get = lambda : Motor.COMMANDS))

        # Add command attribute
        self.add_attribute(FakeLambdaAttribute('command', get = self.get_command, set = self.set_command))

        # Setup command handlers
        self._handlers = {
            Motor.CMD_RUN_FOREVER     : self.cmd_run_forever,
            Motor.CMD_RUN_TO_ABS_POS  : self.cmd_run_to_abs_pos,
            Motor.CMD_RUN_TO_REL_POS  : self.cmd_run_to_rel_pos,
            Motor.CMD_RUN_TIMED       : self.cmd_run_timed,
            Motor.CMD_RUN_DIRECT      : self.cmd_run_direct,
            Motor.CMD_STOP            : self.cmd_stop,
            Motor.CMD_RESET           : self.cmd_reset
        }

    #
    # Get state
    #
    def get_state(self):
        return self._state

    #
    # Get command value
    #
    def get_command(self):
        return self._command

    #
    # Set command value
    #
    def set_command(self, command):

        # Get handler
        handler = self._handlers.get(command)
        if handler is None:
            raise ValueError('Invalid command', command, 'for motor')

        # Invoke handler
        return handler()

    #
    # Handle run-forever
    #
    def cmd_run_forever(self):
        pass

    #
    # Handle run-to-abs-pos
    #
    def cmd_run_to_abs_pos(self):
        pass
    
    #
    # Handle run-to-rel-pos
    #
    def cmd_run_to_rel_pos(self):
        pass
    
    #
    # Handle run-timed
    #
    def cmd_run_timed(self):
        pass
    
    #
    # Handle run-direct
    #
    def cmd_run_direct(self):
        pass
    
    #
    # Handle stop
    #
    def cmd_stop(self):
        pass
    
    #
    # Handle reset
    #
    def cmd_reset(self):
        pass
    

################################################################################
#
# Class representing a fake medium motor
#
class FakeMediumMotor(FakeMotor):

    def __init__(self):
        super(FakeMediumMotor, self).__init__()
        self.add_attribute(FakeAttribute('driver_name', 'lego-ev3-m-motor', settable = False))


################################################################################
#
# Class representing a fake medium motor
#
class FakeLargeMotor(FakeMotor):

    def __init__(self):
        super(FakeLargeMotor, self).__init__()
        self.add_attribute(FakeAttribute('driver_name', 'lego-ev3-l-motor', settable = False))


################################################################################
#
# Class representing a fake sensor
#
class FakeSensor(FakeDevice):
    pass


################################################################################
#
# Class representing a fake gyro sensor
#
class FakeGyro(FakeSensor):
    pass
