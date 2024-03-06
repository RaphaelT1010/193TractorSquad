import time
import serial.tools.list_ports
import adafruit_gps

# Find the GPS serial port
def find_gps_port():
    ports = list(serial.tools.list_ports.comports())
    for port in ports:
        if "GPS" in port.description.upper():
            return port.device
    return None

# Create a serial connection to the GPS module
gps_port = find_gps_port()
if gps_port:
    uart = serial.Serial(gps_port, baudrate=9600, timeout=10)
    gps = adafruit_gps.GPS(uart)
    print(f"Connected to GPS module on {gps_port}")
else:
    print("GPS module not found. Check your connections and try again.")
    exit()

# Main loop to read GPS data and print coordinates
try:
    while True:
        gps.update()

        if gps.has_fix:
            print("Latitude: {0:.6f} degrees".format(gps.latitude))
            print("Longitude: {0:.6f} degrees".format(gps.longitude))
            print("Fix quality: {}".format(gps.fix_quality))
            print("Satellites: {}".format(gps.satellites))
            print("Altitude: {} meters".format(gps.altitude_meters))
            print("Speed: {} m/s".format(gps.speed_mps))
            print("Course: {} degrees".format(gps.track_angle_deg))
            time.sleep(1)

except KeyboardInterrupt:
    uart.close()

