import numpy as np
import sys
import board
import adafruit_lsm9ds1
import imufusion



# Create sensor object, communicating over the board's default I2C bus
i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
sensor = adafruit_lsm9ds1.LSM9DS1_I2C(i2c)
time_interval = 0.01
sample_rate = int(1 / time_interval)

ahrs = imufusion.Ahrs()
ahrs.settings = imufusion.Settings(10,  # gain
                                    10,  # acceleration rejection
                                    20,  # magnetic rejection
                                    5 * sample_rate)  # rejection timeout

def update_heading_data():
    gyroscope = np.array(lsm9ds1.gyro)
    accelerometer = np.array(lsm9ds1.acceleration)
    magnetometer = np.array(lsm9ds1.magnetic)

    # Update AHRS with gyroscope, accelerometer, and magnetometer data
    ahrs.update(gyroscope, accelerometer, magnetometer, time_interval)

    # Get heading angle from AHRS output
    heading = get_heading_from_ahrs_output(ahrs)
    print(f'Heading: {heading}')

def get_heading_from_ahrs_output(ahrs):
    # Extract heading angle from AHRS output
    # This can be obtained directly from AHRS output or by converting quaternion to Euler angles
    # You may need to adjust this based on the AHRS implementation
    heading = np.degrees(ahrs.quaternion.to_euler()[2])  # Assuming yaw angle represents heading
    return heading

while True:
    update_heading_data()
