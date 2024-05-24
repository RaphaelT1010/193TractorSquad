import time
import board
import busio
import adafruit_lsm9ds1
from madgwick_py import madgwickahrs as mw
import numpy as np


i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_lsm9ds1.LSM9DS1_I2C(i2c)
ahrs = mw.MadgwickAHRS()

while True:
    # Update internal Quaternion fo new heading based on gyro(rad/s) and accel(any units)


    # Convert gyro data from degrees to radians and create a NumPy array
    gyro_data = np.array([float(i) * np.pi / 180 for i in sensor.gyro])

    # Convert acceleration data to floats and create a NumPy array
    acceleration_data = np.array([float(i) for i in sensor.acceleration])

    magnetometer_data = np.array([float(i) for i in sensor.magnetic])
    # Update the AHRS with the processed sensor data
    ahrs.update(gyro_data, acceleration_data, magnetometer_data)

    heading = ahrs.quaternion.to_euler_angles()
    heading = [i*180/np.pi for i in heading]
    print(f"Roll: {heading[0]} Pitch: {heading[1]} Yaw: {heading[2]}")
    #print(f"Yaw: {heading[2]}")        
