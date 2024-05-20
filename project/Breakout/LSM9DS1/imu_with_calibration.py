import threading
import time
import board
import busio
import adafruit_lsm9ds1
from madgwick_py import madgwickahrs as mw
import numpy as np

SAMPLE_SIZE = 500


class KeyListener:
    """Object for listening for input in a separate thread"""

    def __init__(self):
        self._input_key = None
        self._listener_thread = None

    def _key_listener(self):
        while True:
            self._input_key = input()

    def start(self):
        """Start Listening"""
        if self._listener_thread is None:
            self._listener_thread = threading.Thread(
                target=self._key_listener, daemon=True
            )
        if not self._listener_thread.is_alive():
            self._listener_thread.start()

    def stop(self):
        """Stop Listening"""
        if self._listener_thread is not None and it.is_alive():
            self._listener_thread.join()

    @property
    def pressed(self):
        """Return whether enter was pressed since last checked"""
        result = False
        if self._input_key is not None:
            self._input_key = None
            result = True
        return result


def calibrate_magnetometer(sensor, key_listener):
    print("Magnetometer Calibration")
    print("Start moving the board in all directions")
    print("When the magnetic Hard Offset values stop changing, press ENTER to go to the next step")
    print("Press ENTER to continue...")
    while not key_listener.pressed:
        pass

    mag_x, mag_y, mag_z = sensor.magnetic
    min_x = max_x = mag_x
    min_y = max_y = mag_y
    min_z = max_z = mag_z

    while not key_listener.pressed:
        mag_x, mag_y, mag_z = sensor.magnetic

        print(
            "Magnetometer: X: {0:8.2f}, Y:{1:8.2f}, Z:{2:8.2f} uT".format(
                mag_x, mag_y, mag_z
            )
        )

        min_x = min(min_x, mag_x)
        min_y = min(min_y, mag_y)
        min_z = min(min_z, mag_z)

        max_x = max(max_x, mag_x)
        max_y = max(max_y, mag_y)
        max_z = max(max_z, mag_z)

        offset_x = (max_x + min_x) / 2
        offset_y = (max_y + min_y) / 2
        offset_z = (max_z + min_z) / 2

        field_x = (max_x - min_x) / 2
        field_y = (max_y - min_y) / 2
        field_z = (max_z - min_z) / 2

        print(
            "Hard Offset:  X: {0:8.2f}, Y:{1:8.2f}, Z:{2:8.2f} uT".format(
                offset_x, offset_y, offset_z
            )
        )
        print(
            "Field:        X: {0:8.2f}, Y:{1:8.2f}, Z:{2:8.2f} uT".format(
                field_x, field_y, field_z
            )
        )
        print("")
        time.sleep(0.01)

    return offset_x, offset_y, offset_z


def calibrate_gyroscope(sensor, key_listener):
    print("")
    print("")
    print("Gyro Calibration")
    print("Place your gyro on a FLAT stable surface.")
    print("Press ENTER to continue...")
    while not key_listener.pressed:
        pass

    gyro_x, gyro_y, gyro_z = sensor.gyro
    min_x = max_x = gyro_x
    min_y = max_y = gyro_y
    min_z = max_z = gyro_z

    for _ in range(SAMPLE_SIZE):
        gyro_x, gyro_y, gyro_z = sensor.gyro

        print(
            "Gyroscope: X: {0:8.2f}, Y:{1:8.2f}, Z:{2:8.2f} rad/s".format(
                gyro_x, gyro_y, gyro_z
            )
        )

        min_x = min(min_x, gyro_x)
        min_y = min(min_y, gyro_y)
        min_z = min(min_z, gyro_z)

        max_x = max(max_x, gyro_x)
        max_y = max(max_y, gyro_y)
        max_z = max(max_z, gyro_z)

        offset_x = (max_x + min_x) / 2
        offset_y = (max_y + min_y) / 2
        offset_z = (max_z + min_z) / 2

        noise_x = max_x - min_x
        noise_y = max_y - min_y
        noise_z = max_z - min_z

        print(
            "Zero Rate Offset:  X: {0:8.2f}, Y:{1:8.2f}, Z:{2:8.2f} rad/s".format(
                offset_x, offset_y, offset_z
            )
        )
        print(
            "Rad/s Noise:       X: {0:8.2f}, Y:{1:8.2f}, Z:{2:8.2f} rad/s".format(
                noise_x, noise_y, noise_z
            )
        )
        print("")

    return offset_x, offset_y, offset_z


def main():
    i2c = busio.I2C(board.SCL, board.SDA)
    sensor = adafruit_lsm9ds1.LSM9DS1_I2C(i2c)
    ahrs = mw.MadgwickAHRS()

    key_listener = KeyListener()
    key_listener.start()

    # Calibrate magnetometer
    mag_offsets = calibrate_magnetometer(sensor, key_listener)
    print("Final Magnetometer Calibration Values: ", mag_offsets)

    # Calibrate gyroscope
    gyro_offsets = calibrate_gyroscope(sensor, key_listener)
    print("Final Gyro Calibration Values: ", gyro_offsets)

    # Main loop to use calibrated data
    while True:
        # Convert gyro data from degrees to radians and create a NumPy array
        gyro_data = np.array([(float(i) * np.pi / 180) - offset for i, offset in zip(sensor.gyro, gyro_offsets)])

        # Convert acceleration data to floats and create a NumPy array
        acceleration_data = np.array([float(i) for i in sensor.acceleration])

        # Convert magnetometer data to floats and create a NumPy array
        magnetometer_data = np.array([float(i) - offset for i, offset in zip(sensor.magnetic, mag_offsets)])
	
        # Update the AHRS with the processed sensor data
        ahrs.update(gyro_data, acceleration_data, magnetometer_data)

        # Get the current heading in Euler angles (radians)
        heading = ahrs.quaternion.to_euler_angles()

        # Convert Euler angles from radians to degrees
        heading_degrees = [angle * 180 / np.pi for angle in heading]
        yaw = heading_degrees[2] + 180

        # Print the roll, pitch, and yaw
        print(f"Roll: {heading_degrees[0]:.2f}° Pitch: {heading_degrees[1]:.2f}° Yaw: {yaw:.2f}°")
        
        time.sleep(0.1)  # Adjust the sleep time as needed for your application


if __name__ == "__main__":
    main()
