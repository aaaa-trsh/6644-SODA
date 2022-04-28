from lib.spark import Spark
from lib.pid import PID

class Drivetrain():
    def __init__(self):
        self.fl = Spark(1)
        self.bl = Spark(2)
        self.fr = Spark(3)
        self.br = Spark(4)

        self.fr.set_inverted(True)
        self.br.set_inverted(True)

    def arcade_drive(self, throttle, turn):
        self.fl.set_output(throttle - turn)
        self.bl.set_output(throttle - turn)
        self.fr.set_output(throttle + turn)
        self.br.set_output(throttle + turn)
        print(throttle - turn, throttle + turn)

    def tank_drive(self, left, right):
        self.fl.set_output(left)
        self.bl.set_output(left)
        self.fr.set_output(right)
        self.br.set_output(right)
        print(left, right)