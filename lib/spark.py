import pigpio
import atexit
import subprocess
class Spark:
    dcBounds = [11, 29, 31, 50]
    instances = []
    @classmethod
    def cleanup(cls):
        print("STOP")
        for instance in cls.instances:
            subprocess.call(f"pigs hp {instance.pin} 10 00000".split(" "))

    def __init__(self, pi, pin):
        self.pi = pi
        self.pin = pin
        #int((Spark.maxDC + Spark.minDC)/2
        # self.pi.hardware_PWM(18, 200, 30 * 10000)
        # self._pwm = GPIO.PWM(pin, (Spark.maxDC + Spark.minDC)/2 * 10000)
        # self._pwm.start((Spark.maxDC + Spark.minDC)/2)
        self.pi.set_PWM_dutycycle(self.pin, int(255 * .3))
        self.pi.set_PWM_frequency(self.pin, 200)
        self.__inverted = False
        Spark.instances.append(self)

    def output_to_duty(self, output):
        if (self.__inverted):
            output *= -1
        
        def lerp(a, b, t):
            return a + (b - a) * t
        if output > 0:
            return min(lerp(Spark.dcBounds[2], Spark.dcBounds[3], output), Spark.dcBounds[3])
        else:
            return max(lerp(Spark.dcBounds[1], Spark.dcBounds[0], -output), Spark.dcBounds[0])

    def set_inverted(self, value):
        self.__inverted = value

    def set_output(self, output):
        self.pi.set_PWM_dutycycle(self.pin, int(255 * self.output_to_duty(output)/100))
atexit.register(lambda: Spark.cleanup())
