class PID:
    def __init__(self, p, i, d, f):
        self.p = p
        self.i = i
        self.d = d
        self.f = f
        self.last_error = 0
        self.integral = 0

    def calculate(self, measurement, setpoint):
        error = setpoint - measurement
        self.integral += error
        derivative = error - self.last_error
        output = self.p * error + self.i * self.integral + self.d * derivative + self.f
        self.last_error = error
        return output