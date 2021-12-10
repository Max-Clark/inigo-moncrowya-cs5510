import pigpio
import time
import board
import adafruit_bno055
import gpsd
import math

#NOTE:
# PIGPIO and GPSD must be ran before starting program!
# sudo pigpiod
# sudo gpsd /dev/serial0 -F /var/run/gpsd.sock

################# ADAFRUIT SONAR ####################

class PwmMeasure:
    def __init__(self, pi, gpio, weighting=0.0):
        self.pi = pi
        self.gpio = gpio
        
        if not (weighting >= 0.0 and weighting <= 1.0):
            weighting = 0.0
        
        self._new = 1.0-weighting
        self._old = weighting
        
        self._high_tick = None
        self._period = None
        self._high = None
        
        pi.set_mode(gpio, pigpio.INPUT)
        
        self._cb = pi.callback(gpio, pigpio.EITHER_EDGE, self._cbf)
    
    def _cbf(self, gpio, level, tick):
        if level == 1:
            if not self._high_tick is None:
                t = pigpio.tickDiff(self._high_tick, tick)
                
                if self._period is None:
                    self._period = t
                else:
                    self._period = (self._old * self._period) + (self._new * t)
            
            self._high_tick = tick
        else:
            if not self._high_tick is None:
                t = pigpio.tickDiff(self._high_tick, tick)
                
                if self._high is None:
                    self._high = t
                else:
                    self._high = (self._old * self._high) + (self._new * t)
    
    def frequency(self):
        if self._high is None:
            return 0.0
            
        return 1000000.0 / self._period
            
    def pulse_width(self):
        if self._high is None:
            return 0.0
            
        return self._high
        
    def duty_cycle(self):
        if self._high is None:
            return 0.0
            
        return 100.0 * self._high / self._period
        
    def cancel(self):
        self._cb.cancel()
        
IN_GPIO = 18  # Named 18 by RPi
pi = pigpio.pi()
p = PwmMeasure(pi, IN_GPIO)

############# END ADAFRUIT SONAR #################

################ START BNO055 ####################

i2c = board.I2C()
sensor = adafruit_bno055.BNO055_I2C(i2c)

################# END BNO055 #####################

#Note: angle is from x axis
def get_lat_long_of_object(angle_deg, distance_m, robot_latitude, robot_longitude):
	angle_rad = math.radians(angle_deg)
	
	lat0 = math.cos(math.pi / 180.0 * robot_latitude)

	longitude = robot_longitude + (180.0 / math.pi) * (distance_m / 6378137) / math.cos(lat0) * math.cos(angle_rad)
	latitude = robot_latitude + (180.0 / math.pi) * (distance_m / 6378137) * math.sin(angle_rad)
	
	return (latitude, longitude)
        
if __name__ == "__main__":
	data = []
	SAMPLE_TIME = 1
	while True:
		try:
			# Connect to the local gpsd
			gpsd.connect()
			while(True):
				euler_angles = sensor.euler
				gps_position = gpsd.get_current().position()
				
				# TODO: Perform frequency/duty cycle checks
				f = p.frequency()
				pw = p.pulse_width()
				dc = p.duty_cycle()
				
				sensed_distance_m = ((pw / 147)*2.54)/100
				
				# TODO: find proper angle to feed equation
				# TODO: figure out which gps loc goes where
				# TODO: figure out max distance cutoff
				obj_position = get_lat_long_of_object(euler_angles[0], 
					sensed_distance_m,
					gps_position[0],
					gps_position[1])
				
				output = (*gps_position, 0, *obj_position, 0)
				
				print(output)
				data.append(output)
				time.sleep(SAMPLE_TIME)
				
		except Exception as e:
			print(e)
		finally:
			time.sleep(SAMPLE_TIME)

