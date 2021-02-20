#!/usr/bin/env python3

from sys import stderr
from time import sleep

from trace import Trace
from device import EV3
from motor import MediumMotor, LargeMotor
from sensor import ColorSensor, GyroSensor, TouchSensor, UltrasonicSensor

# Debug printing
def DbgPrint(*args, **kwargs):
    print(*args, **kwargs, file=stderr)
    return

# Set trace level
#Trace.level = Trace.TRACE_LEVEL_VERBOSE

# Set default instance
EV3.set_default_instance(EV3.get_remote_instance('192.168.10.6', 44444))
#EV3.set_default_instance(EV3.get_local_instance())

# Create objects
motor_c = LargeMotor('outC')
motor_b = MediumMotor('outB')
color_1 = ColorSensor('in1')
gyro_1  = GyroSensor('in3')
us_1    = UltrasonicSensor('in4')
touch_1 = TouchSensor('in2')

# Set color mode
#color_1.mode = ColorSensor.MODE_RGB_RAW
color_1.mode = ColorSensor.MODE_COL_COLOR

# Start rotating
motor_c.run_timed(100, 5000)
motor_b.run_timed(100, 5000)

# Inspect sensed color
while motor_b.state == 'running':
    DbgPrint('Color', ColorSensor.Colors[color_1.color].ljust(6), '| Gyro', str(gyro_1.value()).rjust(3), '| US', str(us_1.value()).rjust(3), '| Touch', touch_1.value())
    sleep(0.5)

# End
DbgPrint("End")
