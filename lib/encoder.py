from lib.pwm_reader import PWMReader
import pigpio
import time

class Encoder():
    def __init__(self, pi, pin):
        self.pin = pin
        self.reader = PWMReader(pi, pin, 0)

        self.__relative_angle = 0
        self.__prev_relative_angle = 0
        self.__full_rotations = 0
        self.__angle = 0
        self.__prev_angle = 0

        self.__speed_buffer_size = 5
        self.__speed_buffer = [0] * self.__speed_buffer_size

        self.__last_update_ts = time.time()
        self.__cur_update_ts = time.time()

    def get_rotations(self):
        return self.__angle
    
    def get_rate(self):
        return sum(self.__speed_buffer) / self.__speed_buffer_size / (self.__last_update_ts - self.__cur_update_ts) 
    
    def update(self):
        self.__last_update_ts = self.__cur_update_ts

        self.__speed_buffer.append(self.__angle - self.__prev_angle)
        if len(self.__speed_buffer) > self.__speed_buffer_size:
            self.__speed_buffer.pop(0)

        self.__prev_angle = self.__angle
        self.__prev_relative_angle = self.__relative_angle

        self.__relative_angle = self.reader.duty_cycle() / 100

        if self.__prev_relative_angle - self.__relative_angle > 0.9:
            self.__full_rotations += 1
        elif self.__relative_angle - self.__prev_relative_angle > 0.9:
            self.__full_rotations -= 1

        self.__angle = self.__relative_angle + self.__full_rotations
        self.__cur_update_ts = time.time()