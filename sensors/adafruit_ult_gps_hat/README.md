# NOTES

1. Must disable console [https://learn.adafruit.com/adafruit-ultimate-gps-hat-for-raspberry-pi/pi-setup](https://learn.adafruit.com/adafruit-ultimate-gps-hat-for-raspberry-pi/pi-setup)

2. Install gpsd
	```sh
	sudo apt-get install gpsd gpsd-clients
	```

3. Disable current gpsd service - `sudo systemctl disable gpsd.socket`

4. Run gpsd (every reboot) - `sudo gpsd /dev/serial0 -F /var/run/gpsd.sock`

5. Install `pip3 install gpsd-py3`, see [https://github.com/MartijnBraam/gpsd-py3](https://github.com/MartijnBraam/gpsd-py3)
