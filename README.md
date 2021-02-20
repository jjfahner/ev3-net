# ev3-net
Lego EV3 network interface for Python

This library provides access to the Lego EV3 (Mindstorms) programmable brick and its sensors. Key features of ev3-net are:
- Provides full access to many networked EV3s at the same time
- Any networked EV3 running the server script can be controlled using the client library
- Client library can run on individual EV3 bricks, but also on any other machine

At this time, the library provides full access to motors and sensors (other features, like displays, sound, leds etc. TBD).

The primary use case for ev3-net is for large builds requiring multiple EV3s running concurrently. While daisy chaining is possible,
using ev3-net is much easier, and scales to as many EV3s as you would like.

The client library has been designed to run on individual bricks, where a program on one EV3 can control itself and other EV3s, but
it also runs perfectly on a regular desktop or server. This lets you create complex programs to control any number of EV3s, and make
use of compute power that the EV3s simply cannot offer.

An example of a small program that runs on a brick:

```python
# Import motor and sensor classes
from ev3client.motor import MediumMotor
from ev3client.sensor import GyroSensor

# Setup default brick instance to be the local brick
EV3.set_default_instance(EV3.get_local_instance())

# Create motor and sensor
motor = MediumMotor('outA')
sensor = GyroSensor('inA')

# Run motor for a while
motor.run_timed(speed=500, time=15000, wait=False)

# Observe sensor
while motor.state == 'running':
  print('Sensor value:', sensor.value())
```

To run this same program on a computer, run the ev3-net server script on a brick, and make the following change:

```python
# Setup default brick instance to be a remote brick
EV3.set_default_instance(EV3.get_remote_instance('10.0.0.1', 44444)
```

Or pass the instance to the individual objects you're creating:

```python
brick1 = EV3.get_instance('10.0.0.1', 44444)
brick2 = EV3.get_instance('10.0.0.2', 44444)

motor1 = MediumMotor('outA', brick1)
motor2 = MediumMotor('outA', brick2)
```

You can also run a program on an EV3 that controls itself and another EV3:

```python
brick1 = EV3.get_local_instance()
brick2 = EV3.get_instance('10.0.0.2', 44444)

motor1 = MediumMotor('outA', brick1)
motor2 = MediumMotor('outA', brick2)
```

The possibilities are endless, letting you scale up your Lego EV3 projects almost indefinitely.
