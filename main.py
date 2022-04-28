from lib.scheduler import Scheduler, Command, InstantCommand
from lib.spark import Spark
from lib.encoder import Encoder
from time import time, sleep
from math import sin
import pigpio
# import RPi.GPIO as GPIO
import atexit

scheduler = Scheduler()
pi = pigpio.pi()
atexit.register(lambda: pi.stop())

e = Encoder(pi, 15)
spark = Spark(pi, 18)

e2 = Encoder(pi, 17)
spark2 = Spark(pi, 19)
cmd = Command(lambda: spark.set_output(e.get_angle()*.8), 10000)
cmd2 = Command(lambda: spark2.set_output(e2.get_angle()*.8), 10000)

scheduler.schedule_command(cmd)
scheduler.schedule_command(cmd2)
while True:
    e.update()
    e2.update()
    # print(round(e.get_angle(), 3))#, round(e.get_rate(), 3))
    scheduler.periodic()