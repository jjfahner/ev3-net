# ev3-net
Lego EV3 network interface for Python

After working with ev3dev-lang-python for a little while, I decided to implemented a client-server Python EV3 interface that lets you run the code on a different machine.

ev3-net lets you connect as many EV3 bricks as you like, and manage all of them from the same host Python program running on a separate machine. 
While this incurs some latency (obviously dependent on your local network and quality of your WiFi adapter), it means you're not limited by the
EV3's single-threaded processor in terms of the logic you're running. 
