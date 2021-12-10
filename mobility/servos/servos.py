import RPi.GPIO as GPIO
import time


# GPIO INITIALIZATION
FRONT_SERVO_PIN = 23
SERVO_UP_DOWN_PIN = 9
SERVO_LEFT_RIGHT_PIN = 11


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
  time.sleep((20 - pulse_width / 1000)/1000)

#for i in range(10):
    # FRONT SONAR SERVO RANGE
    # left max 135 = -45
    # right max 45 = 45
    # UP DOWN SERVO RANGE
    # center is 22 = 0
    # backward  max 107 = 85 (looking straight up)
    # forward max -3 = -25
    # LEFT RIGHT SERVO RANGE
    # left max 170 = 70
    # right max 30 = -70
    # center 100 = 0
    #servo_pulse(FRONT_SERVO_PIN, 90-45)
    #servo_pulse(SERVO_UP_DOWN_PIN, 22+85)
 #  servo_pulse(SERVO_LEFT_RIGHT_PIN,100-70)

def move_camera_x(angle):
    for i in range(10):
        if angle > 170:
            angle = 170
        if angle < 30:
            angle = 30
        servo_pulse(SERVO_LEFT_RIGHT_PIN, angle)

def center_camera_x():
    move_camera_x(100)

def move_camera_y(angle):
    for i in range(10):
        if angle > 107:
            angle = 107
        if angle < -3:
            angle = -3
        servo_pulse(SERVO_UP_DOWN_PIN, angle)

def center_camera_y():
    move_camera_y(22)


def move_sonar(angle):
    for i in range(10):
        if angle > 105:
            angle = 105
        if angle < 35:
            angle = 35
        servo_pulse(FRONT_SERVO_PIN, angle)

def center_sonar():
    move_sonar(70)

def scan_left_right():
    angle = 170
    move_camera_x(170)
    while angle != 30:
        angle -= 1
        move_camera_x(angle)

def scan_up_down():
    angle = 107
    move_camera_x(107)
    while angle != -1:
        angle -= 1
        move_camera_y(angle)
