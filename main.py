from lib.scheduler import Scheduler, Command, InstantCommand
from lib.spark import Spark
from lib.encoder import Encoder
from time import time, sleep
from subsystems.drive import Drivetrain
from math import sin
import pigpio
import atexit
import webapp

scheduler = Scheduler()
pi = pigpio.pi()
atexit.register(lambda: pi.stop())

drivetrain = Drivetrain(pi)

scheduler.schedule_command(
    Command(
        lambda: drivetrain.tank_drive(
            drivetrain.get_left_distance(), 
            drivetrain.get_right_distance()
        ), 
        10000
))

while True:
    drivetrain.periodic()
    scheduler.periodic()