import RPi.GPIO as GPIO
import time
import threading


class Servo:
    def __init__(self):
        self.servo_pin = 5
        self.duty_cycle = 7.5     # Should be the centre for a SG90

        # Configure the Pi to use pin names (i.e. BCM) and allocate I/O
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.servo_pin, GPIO.OUT)

        # Create PWM channel on the servo pin with a frequency of 50Hz
        self.pwm_servo = GPIO.PWM(self.servo_pin, 50)
        self.pwm_servo.start(self.duty_cycle)

        self.running = False
        self.DELAY = 1.5
        self.ZAP_TIME = 0.5

    def __del__(self):
        GPIO.cleanup()

    def _set_not_running(self):
        self.running = False

    def _set_servo(self, rotation):
        if self.running:
            return

        self.running = True
        self.pwm_servo.ChangeDutyCycle(rotation)
        threading.Timer(self.DELAY, self._set_not_running).start()

    def set_on(self):
        self._set_servo(1)

    def set_off(self):
        self._set_servo(10)

    def _unzap(self):
        self.pwm_servo.ChangeDutyCycle(1)

    def zap(self):
        if self.running:
            return

        self.running = True
        self.pwm_servo.ChangeDutyCycle(10)
        threading.Timer(self.ZAP_TIME, self._unzap).start()
        threading.Timer(self.DELAY, self._set_not_running).start()
