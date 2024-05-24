import time
import serial
import adafruit_gps
from serial.serialutil import SerialException

NUM_GPS_ITERATIONS = 5

class GPS:
    def __init__(self, port='/dev/ttyUSB0', baudrate=9600, timeout=10):
        try:
            # pyserial library for UART access
            self.uart = serial.Serial(port, baudrate, timeout=timeout)
            # Create a GPS module instance.
            self.gps = adafruit_gps.GPS(self.uart, debug=False)
            # Turn on the basic GGA and RMC info (what you typically want)
            self.gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")
            # Set update rate to once a second (1hz) which is what you typically want.
            self.gps.send_command(b"PMTK220,1000")
            self.last_print = time.monotonic()
            
            # Wait until a fix is obtained
            self.obtain_gps_fix()
                    
            print("Successfully initialized GPS")

        except SerialException as e:
            print(f"Could not open port {port}: {e}")

    def obtain_gps_fix(self, timeout=30):
        start_time = time.monotonic()
        try:
            while not self.gps.has_fix:
                self.gps.update()
                current = time.monotonic()
                if current - self.last_print >= 1.0:
                    self.last_print = current
                    print("Waiting for fix...")
                if current - start_time > timeout:
                    print("Timeout waiting for GPS fix")
                    return False
            return True
        except AttributeError:
            print("GPS object does not have attribute 'gps'")
            return False

    def obtain_coords(self):        
        if not self.obtain_gps_fix():
            print("Could not obtain GPS fix.")
            return
        
        total_latitude = 0
        total_longitude = 0
        for i in range(NUM_GPS_ITERATIONS):
            time.sleep(0.1)  # Small delay to avoid overwhelming the sensor
            self.gps.update()
            if self.gps.latitude is not None and self.gps.longitude is not None:
                latitude = self.gps.latitude
                longitude = self.gps.longitude
                total_latitude += latitude
                total_longitude += longitude
                print("Latitude: {0:.6f} degrees".format(latitude))
                print("Longitude: {0:.6f} degrees".format(longitude))
            else:
                print("GPS data not available for iteration {}".format(i+1))

        # [0] = latitude, [1] = longit
        coordinates = []

        if NUM_GPS_ITERATIONS > 0:
            coordinates[0] = total_latitude / NUM_GPS_ITERATIONS
            coordinates[1] = total_longitude / NUM_GPS_ITERATIONS
            print("Average Latitude: {0:.6f} degrees".format(coordinates[0]))
            print("Average Longitude: {0:.6f} degrees".format(coordinates[1]))
        
        return coordinates
        
    def obtain_satellites(self):
        if not self.obtain_gps_fix():
            print("Could not obtain GPS fix.")
            return
        self.gps.update()
        if self.gps.satellites is not None:
            print("# satellites: {}".format(self.gps.satellites))
        else:
            print("Satellites data not available.")

    def get_altitude(self):
        if not self.obtain_gps_fix():
            print("Could not obtain GPS fix.")
            return
        self.gps.update()
        if self.gps.altitude_m is not None:
            print("Altitude: {} meters".format(self.gps.altitude_m))
        else:
            print("Altitude data not available.")

    def get_speed(self):
        if not self.obtain_gps_fix():
            print("Could not obtain GPS fix.")
            return
        self.gps.update()
        if self.gps.speed_knots is not None:
            print("Speed: {} knots".format(self.gps.speed_knots))
        else:
            print("Speed data not available.")

    def get_track_angle(self):
        if not self.obtain_gps_fix():
            print("Could not obtain GPS fix.")
            return
        self.gps.update()
        if self.gps.track_angle_deg is not None:
            print("Track angle: {} degrees".format(self.gps.track_angle_deg))
            return self.gps.track_angle_deg
        else:
            print("Track angle data not available.")

    def get_horizontal_dilution(self):
        if not self.obtain_gps_fix():
            print("Could not obtain GPS fix.")
            return
        self.gps.update()
        if self.gps.horizontal_dilution is not None:
            print("Horizontal dilution: {}".format(self.gps.horizontal_dilution))
        else:
            print("Horizontal dilution data not available.")

    def get_height_geoid(self):
        if not self.obtain_gps_fix():
            print("Could not obtain GPS fix.")
            return
        self.gps.update()
        if self.gps.height_geoid is not None:
            print("Height geoid: {} meters".format(self.gps.height_geoid))
        else:
            print("Height geoid data not available.")

# Example usage
gps_device = GPS()
gps_device.obtain_coords()
gps_device.obtain_satellites()
