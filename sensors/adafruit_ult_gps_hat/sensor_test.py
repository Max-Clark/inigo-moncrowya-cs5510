import gpsd
import time
from math import cos, sin, pi, radians

# Connect to the local gpsd
gpsd.connect()

    """ Class representing geo information returned by GPSD
    Use the attributes to get the raw gpsd data, use the methods to get parsed and corrected information.
    :type mode: int
    :type sats: int
    :type sats_valid: int
    :type lon: float
    :type lat: float
    :type alt: float
    :type track: float
    :type hspeed: float
    :type climb: float
    :type time: str
    :type error: dict[str, float]
    :var self.mode: Indicates the status of the GPS reception, 0=No value, 1=No fix, 2=2D fix, 3=3D fix
    :var self.sats: The number of satellites received by the GPS unit
    :var self.sats_valid: The number of satellites with valid information
    :var self.lon: Longitude in degrees
    :var self.lat: Latitude in degrees
    :var self.alt: Altitude in meters
    :var self.track: Course over ground, degrees from true north
    :var self.hspeed: Speed over ground, meters per second
    :var self.climb: Climb (positive) or sink (negative) rate, meters per second
    :var self.time: Time/date stamp in ISO8601 format, UTC. May have a fractional part of up to .001sec precision.
    :var self.error: GPSD error margin information
    GPSD error margin information
    -----------------------------
    c: ecp: Climb/sink error estimate in meters/sec, 95% confidence.
    s: eps: Speed error estinmate in meters/sec, 95% confidence.
    t: ept: Estimated timestamp error (%f, seconds, 95% confidence).
    v: epv: Estimated vertical error in meters, 95% confidence. Present if mode is 3 and DOPs can be
            calculated from the satellite view.
    x: epx: Longitude error estimate in meters, 95% confidence. Present if mode is 2 or 3 and DOPs
            can be calculated from the satellite view.
    y: epy: Latitude error estimate in meters, 95% confidence. Present if mode is 2 or 3 and DOPs can
            be calculated from the satellite view.
    """


#Note: angle is from x axis
def get_lat_long_of_object(angle_deg, distance_m, robot_latitude, robot_longitude):
	angle_rad = radians(angle_deg)
	
	lat0 = cos(pi / 180.0 * robot_latitude)

	longitude = robot_longitude + (180/pi) * (distance_m / 6378137) / cos(lat0) * cos(angle_rad)
	latitude = robot_latitude + (180/pi) * (distance_m / 6378137) * sin(angle_rad)
	
	return (latitude, longitude)

while True:
	print(get_lat_long_of_object(1,1,1,1))
	time.sleep(1)
	
	# Get gps position
	packet = gpsd.get_current()
	
	print(packet)

	# See the inline docs for GpsResponse for the available data
	print(packet.position())
