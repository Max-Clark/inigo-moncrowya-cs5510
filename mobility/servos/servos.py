import RPi.GPIO as GPIO
import time


# GPIO INITIALIZATION
FRONT_SERVO_PIN = 4
SERVO_UP_DOWN_PIN = 13
SERVO_LEFT_RIGHT_PIN = 14


#Set the GPIO port to BCM encoding mode

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(FRONT_SERVO_PIN,GPIO.OUT,initial=GPIO.HIGH)

GPIO.setup(SERVO_UP_DOWN_PIN,GPIO.OUT,initial=GPIO.HIGH)

GPIO.setup(SERVO_LEFT_RIGHT_PIN,GPIO.OUT,initial=GPIO.HIGH)


# SERVO PULSE
def servo_pulse(servo_pin, angle):
    # C code
  #   int PulseWidth;
  # PulseWidth = (myangle * 11) + 500;
  # digitalWrite(ServoPin, HIGH);
  # delayMicroseconds(PulseWidth);
  # digitalWrite(ServoPin, LOW);
  # delay(20 - PulseWidth / 1000);
  # return;

  pulse_width = (angle * 11) + 500
  GPIO.output(servo_pin, GPIO.HIGH)
  time.sleep(pulse_width / 1000000)
  GPIO.output(servo_pin, GPIO.LOW)
  time.sleep(20 - pulse_width / 1000)


while True:
    servo_pulse(SERVO_LEFT_RIGHT_PIN, 90)
