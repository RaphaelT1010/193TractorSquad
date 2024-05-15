import numpy as np
import sys
import board
import adafruit_lsm9ds1
import imufusion
import time



# Create sensor object, communicating over the board's default I2C bus
i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
sensor = adafruit_lsm9ds1.LSM9DS1_I2C(i2c)



mag_hard_iron_correction_values = (0.2023, -0.18634, 0.08519)
gyro_bias_correction_values = (0.1629483022893206, 0.03863722631602448, 0.002977968036215325)

def update_heading_data():
    time.sleep(2)
    gyro_raw = sensor.gyro
    accel_raw = sensor.acceleration
    mag_raw = sensor.magnetic

    gyroscope = np.array(list(gyro_raw))[:3]
    accelerometer = np.array(list(accel_raw))[:3]
    magnetometer = np.array(list(mag_raw))[:3]
    
    
    gyro_corrected = gyroscope - gyro_bias_correction_values
    # Apply magnetometer hard iron correction
    mag_corrected = magnetometer - mag_hard_iron_correction_values

    