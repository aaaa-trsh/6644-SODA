from lib.spark import Spark
from lib.encoder import Encoder
from lib.pid import PID
from constants import DrivetrainConstants

class Drivetrain():
    def __init__(self, pi):
        self.pi = pi

        self.left_encoder = Encoder(pi, DrivetrainConstants.LEFT_ENCODER_BCM)
        self.left_spark = Spark(pi, DrivetrainConstants.LEFT_CONTROLLER_BCM)

        self.right_encoder = Encoder(pi, DrivetrainConstants.RIGHT_ENCODER_BCM)
        self.right_spark = Spark(pi, DrivetrainConstants.RIGHT_CONTROLLER_BCM)

    def periodic(self):
        self.left_encoder.update()
        self.right_encoder.update()
    
    def get_left_distance(self):
        return self.left_encoder.get_rotations()# * DrivetrainConstants.WHEEL_DIAMETER * math.pi
    
    def get_right_distance(self):
        return self.right_encoder.get_rotations()# * DrivetrainConstants.WHEEL_DIAMETER * math.pi
        
    def arcade_drive(self, throttle, turn):
        self.left_spark.set_output(throttle - turn)
        self.right_spark.set_output(throttle + turn)
        # print(throttle - turn, throttle + turn)

    def tank_drive(self, left, right):
        self.left_spark.set_output(left)
        self.right_spark.set_output(right)
        # print(left, right)