from device import Device
import time


################################################################################
#
# Current time in ms
#
def __time_ms():
    return int(round(time.time() * 1000))


################################################################################
#
# Motor class
#
class Motor(Device):

    #
    # Construction
    #
    def __init__(self, device_name, driver_name, ev3_instance = None):
        super(Motor, self).__init__('tacho-motor', device_name, driver_name, ev3_instance)

    #
    # count per rotation
    #
    count_per_rot = property(fget = lambda self : self.get_cached_attribute('count_per_rot'))

    #
    # duty_cycle
    #
    duty_cycle = property(fget = lambda self : self.get_attribute('duty_cycle'))

    #
    # duty_cycle_sp
    #
    duty_cycle_sp = property(
        fget = lambda self : self.get_attribute('duty_cycle_sp'),
        fset = lambda self, value : self.set_attribute('duty_cycle_sp', value))

    #
    # polarity
    #
    polarity = property(
        fget = lambda self : self.get_attribute('polarity'),
        fset = lambda self, value : self.set_attribute('polarity', value))

    #
    # speed
    #
    speed = property(fget = lambda self : self.get_attribute('speed'))

    #
    # speed_sp
    #
    speed_sp = property(
        fget = lambda self : self.get_attribute('speed_sp'),
        fset = lambda self, value : self.set_attribute('speed_sp', value))

    #
    # state
    #
    state = property(fget = lambda self : self.get_attribute('state'))

    #
    # Time
    #
    time_sp = property(
        fget = lambda self : self.get_attribute('time_sp'),
        fset = lambda self, value : self.set_attribute('time_sp', value))

    #
    # Run forever
    #
    def run_forever(self, speed, wait = False):
        self.speed_sp = speed
        self.command = 'run-forever'
        if wait:
            self.wait()
    
    #
    # Run for a defined time
    #
    def run_timed(self, speed, time, wait = False):
        self.speed_sp = speed
        self.time_sp = time
        self.command = 'run-timed'
        if wait:
            self.wait()


    #
    # Wait
    #
    def wait(self, cond = lambda state : state != 'running', timeout = 0):
        
        # Take start time
        start_time = __time_ms() if timeout > 0 else 0

        # Wait loop
        while True:

            # Timeout has elapsed
            if timeout > 0 and __time_ms() - start_time >= timeout:
                return False

            # Check condition
            if cond(self.state):
                return True

            # Sleep a bit, but never longer than is remaining
            sleep_time = 10 if timeout == 0 else min(10, __time_ms() - start_time)            
            if sleep_time > 0:
                time.sleep(0.0001 * sleep_time)


################################################################################
#
# Medium motor class
#
class MediumMotor(Motor):

    #
    # Driver name
    #
    DRIVER_NAME = 'lego-ev3-m-motor'

    #
    # Construction
    #
    def __init__(self, device_name, ev3_instance = None):
        super(Motor, self).__init__('tacho-motor', device_name, MediumMotor.DRIVER_NAME, ev3_instance)


################################################################################
#
# Large motor class
#
class LargeMotor(Motor):

    #
    # Driver name
    #
    DRIVER_NAME = 'lego-ev3-l-motor'

    #
    # Construction
    #
    def __init__(self, device_name, ev3_instance = None):
        super(Motor, self).__init__('tacho-motor', device_name, LargeMotor.DRIVER_NAME, ev3_instance)