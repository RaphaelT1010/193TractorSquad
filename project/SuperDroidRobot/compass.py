import numpy as np
import time
import adafruit_lsm9ds1
import board
import busio
from math import sqrt, atan2, pi

# Initialize I2C bus and sensor
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_lsm9ds1.LSM9DS1_I2C(i2c)

# For low pass filtering
filtered_x_value = 0.0
filtered_y_value = 0.0

def degrees_to_heading(degrees):
    if (degrees > 337) or (degrees >= 0 and degrees <= 22):
        return 'N'
    elif degrees > 22 and degrees <= 67:
        return "NE"
    elif degrees > 67 and degrees <= 112:
        return "E"
    elif degrees > 112 and degrees <= 157:
        return "SE"
    elif degrees > 157 and degrees <= 202:
        return "S"
    elif degrees > 202 and degrees <= 247:
        return "SW"
    elif degrees > 247 and degrees <= 292:
        return "W"
    elif degrees > 292 and degrees <= 337:
        return "NW"
    return ""

def low_pass_filter(raw_value, remembered_value):
    alpha = 0.8
    filtered = (alpha * remembered_value) + (1.0 - alpha) * raw_value
    return filtered

def calibrate(count=256, delay=200):
    offset = (0, 0, 0)
    scale = (1, 1, 1)

    magnetometer_data = np.array([float(i) for i in sensor.magnetic])
    minx = maxx = magnetometer_data[0]
    miny = maxy = magnetometer_data[1]
    minz = maxz = magnetometer_data[2]

    while count:
        time.sleep(delay / 1000)  # Convert milliseconds to seconds
        magnetometer_data = np.array([float(i) for i in sensor.magnetic])
        minx = min(minx, magnetometer_data[0])
        maxx = max(maxx, magnetometer_data[0])
        miny = min(miny, magnetometer_data[1])
        maxy = max(maxy, magnetometer_data[1])
        minz = min(minz, magnetometer_data[2])
        maxz = max(maxz, magnetometer_data[2])
        count -= 1
        print(count)

    offset_x = (maxx + minx) / 2
    offset_y = (maxy + miny) / 2
    offset_z = (maxz + minz) / 2
    offset = (offset_x, offset_y, offset_z)

    avg_delta_x = (maxx - minx) / 2
    avg_delta_y = (maxy - miny) / 2
    avg_delta_z = (maxz - minz) / 2
    avg_delta = (avg_delta_x + avg_delta_y + avg_delta_z) / 3

    scale_x = avg_delta / avg_delta_x
    scale_y = avg_delta / avg_delta_y
    scale_z = avg_delta / avg_delta_z
    scale = (scale_x, scale_y, scale_z)

    return offset, scale

def get_reading(offset, scale):
    global filtered_x_value, filtered_y_value
    magnetometer_data = np.array([float(i) for i in sensor.magnetic])

    for i in range(3):
        magnetometer_data[i] -= offset[i]
        magnetometer_data[i] *= scale[i]

    mag_x = magnetometer_data[0]
    mag_y = magnetometer_data[1]

    filtered_x_value = low_pass_filter(mag_x, filtered_x_value)
    filtered_y_value = low_pass_filter(mag_y, filtered_y_value)
    az = 90 - atan2(filtered_y_value, filtered_x_value) * 180 / pi

    if az < 0:
        az += 360

    heading = degrees_to_heading(az)
    print(heading)
    print(az)

def testing():
    offset, scale = calibrate()
    while True:
        get_reading(offset, scale)
        time.sleep(0.1)  # Small delay to avoid overwhelming the sensor

# Run the testing function
testing()
