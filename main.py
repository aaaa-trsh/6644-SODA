from lib.scheduler import Scheduler
from subsystems.drive import Drivetrain
import pigpio
import atexit
# import webapp

scheduler = Scheduler()
pi = pigpio.pi()
atexit.register(lambda: pi.stop())

# e = Encoder(pi, 17)
drivetrain = Drivetrain(pi)

while True:
    drivetrain.tank_drive(drivetrain.get_left_distance()/2, drivetrain.get_right_distance()/2)
    drivetrain.periodic()
    scheduler.periodic()