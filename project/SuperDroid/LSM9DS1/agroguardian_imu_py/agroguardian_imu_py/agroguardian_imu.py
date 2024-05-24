# -*- coding: utf-8 -*-

import board
import busio
import datetime
import adafruit_lsm9ds1
from digitalio import DigitalInOut, Direction
import numpy as np
import sys
sys.path.insert(1, '~/kadd-pi/src')
from madgwick_py import madgwickahrs as mw 

ERROR_SAMPLES = 100

class AgroGuardianImu:
    """
    LSM9DS1 Wrapper Class for AgroGuardian

    This class contains methods for interacting with the IMU module onboard AgroGuardian.
    It is built off of the :class:`adafruit_lsm9ds1` library and extends its functionality by wrapping 
    both configuration data members and a Madgwick filter from :class:`madgwick_py.madgwickahrs`.

    :param connection: wiring configuration of sensor, defaults to "i2c"
    :type connection: string, optional, "i2c" or "spi" depending on configuration
    :param madgwick_sample_period: time between each sample utilized by the Madgwick filter, 
        defaults to None utilizing :class:`madgwickahrs` default of 1/256
    :type madgwick_sample_period: float, optional, number/fraction of seconds between IMU samples
    """

    def __init__(self, connection="i2c", madgwick_sample_period=None):
        """
        Constructor
        
        Create a LSM9DS1 IMU instance
        """
        assert connection == 'i2c' or connection == 'spi', "connection param should be 'i2c' or 'spi'"

        if connection == "i2c":
            i2c = busio.I2C(board.SCL, board.SDA)
            self._sensor = adafruit_lsm9ds1.LSM9DS1_I2C(i2c)
        elif connection == "spi":
            spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
            csag = DigitalInOut(board.D5)
            csag.direction = Direction.OUTPUT
            csag.value = True
            csm = DigitalInOut(board.D6)
            csm.direction = Direction.OUTPUT
            csm.value = True
            self._sensor = adafruit_lsm9ds1.LSM9DS1_SPI(spi, csag, csm)

        self._madgwick = mw.MadgwickAHRS(sampleperiod=madgwick_sample_period)

    @property
    def accelerometer(self):
        """
        Class property to read current accelerometer values

        :return: current accelerometer values [X, Y, Z]
        :rtype: :class:`numpy.array`
        """
        accelX, accelY, accelZ = self._sensor.acceleration
        return np.array([accelX, accelY, accelZ])
    
    @property
    def gyroscope(self):
        """
        Class property to read current gyroscope values

        :return: current gyroscope values [X, Y, Z]
        :rtype: :class:`numpy.array`
        """
        gyroX, gyroY, gyroZ = self._sensor.gyro
        return np.array([gyroX, gyroY, gyroZ]) * (np.pi/180)

    @property
    def magnetometer(self):
        """
        Class property to read current magnetometer values

        :return: current magnetometer values [X, Y, Z]
        :rtype: :class:`numpy.array`
        """
        magX, magY, magZ = self._sensor.magnetic
        return  np.array([magX, magY, magZ])

    @property
    def madgwick_orientation(self):
        """
        Class property to get the current madgwick orientation prediction WITHOUT updating model

        :return: current orientation in degrees [X, Y, Z]
        :rtype: :class:`numpy.array`
        """
        return np.array([self._madgwick.orientation_degrees[0], self._madgwick.orientation_degrees[2], self._madgwick.orientation_degrees[1]])

    @property
    def madgwick_gravity_magnitudes(self):
        """
        Class property to get the magnitude of gravity on each axis represented by values (-1,1) where -1 is fully inverted
        and 1 is fully upright

        :return: gravity magnitudes for all three axes [X, Y, Z]
        :rtype: :class:`numpy.array`
        """
        q = self._madgwick.quaternion.q
        gx = 2 * (q[1]*q[3] - q[0]*q[2])
        gy = 2 * (q[0]*q[1] + q[2]*q[3])
        gz = q[0]*q[0] - q[1]*q[1] - q[2]*q[2] + q[3]*q[3]

        return np.array([gx, gy, gz])

    def determine_error(self):
        """
        Determine Accelerometer Error by taking mean of 100 samples

        :return: errors for all 3 axes formatted as [X, Y, Z]
        :rtype: :class:`numpy.array`
        """
        total = np.zeros((1,3))

        for i in range(ERROR_SAMPLES):
            total += self.accelerometer

        return total[0] / ERROR_SAMPLES

    def read(self, round_to=5):
        """
        Legacy method to read all 9 Degrees of Freedom (9DoF) of the sensors current state at the 
        current timestamp.

        Reads X,Y,Z for: accelerometer, gyroscope, and magnetometer.

        :param round_to: number of decimal places output should be rounded to, defaults to 5
        :type round_to: int, optional

        :return: timestamp and parameters retrieved from sensor
        :rtype: dict, {time,accel[X,Y,Z],gyro[X,Y,Z],mag[X,Y,Z]}
        """
        assert isinstance(round_to, int), "round_to must be an integer"

        accelX, accelY, accelZ = self._sensor.acceleration
        gyroX, gyroY, gyroZ = self._sensor.gyro
        magX, magY, magZ = self._sensor.magnetic

        accelX, accelY, accelZ = round(accelX, 5), round(accelY, 5), round(accelZ,5)
        gyroX, gyroY, gyroZ = round(gyroX, 5), round(gyroY, 5), round(gyroZ,5)
        magX, magY, magZ = round(magX, 5), round(magY, 5), round(magZ,5)

        sample = {
            'time': datetime.datetime.now(),
            'accelX': round(accelX, round_to),
            'accelY': round(accelY, round_to),
            'accelZ': round(accelZ, round_to),
            'gyroX': round(gyroX, round_to),
            'gyroY': round(gyroY, round_to),
            'gyroZ': round(gyroZ, round_to),
            'magX': round(magX, round_to),
            'magY': round(magY, round_to),
            'magZ': round(magZ, round_to)
        }

        return sample
    
    def update_madgwick_6dof_orientation(self):
        """
        Madgwick orientation prediction update step. Utilizes accelerometer and gyroscope.

        Must be called frequently within a loop at around `madgwick_sample_period` to maintain accuracy.

        :return: current orientation in degrees [X, Y, Z]
        :rtype: :class:`numpy.array` 
        """
        self._madgwick.update_imu(self.gyroscope, self.accelerometer)
        return np.array([self._madgwick.orientation_degrees[0], self._madgwick.orientation_degrees[2], self._madgwick.orientation_degrees[1]])

    def update_madgwick_9dof_orientation(self):
        """
        Madgwick orientation prediction update step. Utilizes accelerometer, gyroscope, and magnetometer.

        :return: current orientation in degrees [X, Y, Z]
        :rtype: :class:`numpy.array`
        """
        self._madgwick.update(self.gyroscope, self.accelerometer, self.magnetometer)
        return np.array([self._madgwick.orientation_degrees[0], self._madgwick.orientation_degrees[2], self._madgwick.orientation_degrees[1]])

    def update_madgwick_6dof_quaternion(self):
        """
        Madgwick orientation prediction update step. Utilizes accelerometer and gyroscope.

        :return: quaternion coefficients [a, b, c, d]
        :rtype: :class:`numpy.array`
        """
        self._madgwick.update_imu(self.gyroscope, self.accelerometer)
        return self._madgwick.quaternion.q
