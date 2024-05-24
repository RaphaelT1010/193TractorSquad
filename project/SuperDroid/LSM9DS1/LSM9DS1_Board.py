import time
import board
import busio
import adafruit_lsm9ds1
from madgwick_py import madgwickahrs as mw
import numpy as np
from math import sqrt, atan2, pi, copysign, sin, cos


i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_lsm9ds1.LSM9DS1_I2C(i2c)
ahrs = mw.MadgwickAHRS()




while True:
    # Convert gyro data from degrees to radians and create a NumPy array
    gyro_data = np.array([float(i) * np.pi / 180 for i in sensor.gyro])

    # Convert acceleration data to floats and create a NumPy array
    acceleration_data = np.array([float(i) for i in sensor.acceleration])

    # Convert magnetometer data to floats and create a NumPy array
    magnetometer_data = np.array([float(i) for i in sensor.magnetic])

    # Update the AHRS with the processed sensor data
    ahrs.update(gyro_data, acceleration_data, magnetometer_data)

    # Get the current heading in Euler angles (radians)
    heading = ahrs.quaternion.to_euler_angles()

    x = heading[0]
    y = heading[1]


    az =  90 - atan2(y, x) * 180 / pi
    if az < 0:
        az += 360

    # Convert Euler angles from radians to degrees
    # heading_degrees = [angle * 180 / np.pi for angle in heading]
    # yaw = heading_degrees[2]
    #if yaw < 0:
     #   yaw += 360
    print(az)
    # Print the roll, pitch, and yaw
    # print(f"Roll: {heading_degrees[0]:.2f}° Pitch: {heading_degrees[1]:.2f}° Yaw: {yaw:.2f}°")