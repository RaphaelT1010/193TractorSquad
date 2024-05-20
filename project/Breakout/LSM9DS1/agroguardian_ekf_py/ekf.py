# -*- coding: utf-8 -*-

import sys
import numpy as np
import time
import math
import utm

class ExtendedKalmanFilter:
    def __init__(self, acc_x_err, acc_y_err, gyro_z_err, lat_err, long_err, theta_err):
        """
        Create EKF and initialize variance-covariance matrices with sensor values

        :param acc_x_err: IMU's accelerometer error in terms of m/s^2 for the x axis
        :param acc_y_err: IMU's accelerometer error in terms of m/s^2 for the y axis
        :param gyro_z_err: IMU's gyroscope error in terms of radians/s for the z axis

        :param lat_err: GPS' error for latitude component in meters
        :param long_err: GPS' error for longitude component in meters
        :param theta_err: GPS' track angle error in degrees

        :param yaw: Intial heading for determining intial state
        """
        # UTM Zone
        self._zone = None
        # UTM Zone Letter
        self._zone_letter = None

        # Previous State (instantiated at (0,0,0))
        self._q_prev = None

        # Previous process noise covariance matrix
        self._p_prev = np.array([[0.0, np.nan, np.nan],
                                [np.nan, 0.0, np.nan],
                                [np.nan, np.nan, 0.0]])

        # IMU variance covariance matrix
        self._imu_noise_cov = np.array([[acc_x_err**2, 0, 0],
                                       [0, acc_y_err**2, 0],
                                       [0, 0, gyro_z_err**2]])
        # GPS variance covariance matrix
        self._gps_noise_cov = np.array([[lat_err**2, 0, 0],
                                       [0, long_err**2, 0],
                                       [0, 0, theta_err**2]])
        
        # Previous velocity estimation (intialized at 0)
        self._v_prev = np.array([0.0, 0.0])
        # Previous accelerometer readings (initialized at 0)
        self._ax_prev = 0.0
        self._ay_prev = 0.0
        # Previous gyroscope reading (initialized at 0)
        self._omega_z_prev = 0.0
        # Last time ekf was updated
        self._last_time = time.monotonic()

    def initial_position(self, easting: float, northing: float, zone: int, zone_letter: str):
        """
        Set the intial position for EKF to function
        """
        self._q_prev = np.array([[easting, np.nan, np.nan],
                                 [np.nan, northing, np.nan],
                                 [np.nan, np.nan, 0.0]]) 
        self._zone = zone
        self._zone_letter = zone_letter

    @property
    def utm_position_estimate(self):
        """
        Return most current position estimation in UTM [easting, northing, zone, zone letter]
        """
        if self._q_prev is None:
            return None

        return (self._q_prev[0][0], self._q_prev[1][1], self._zone, self._zone_letter)

    @property
    def lat_long_position_estimate(self):
        """
        Return most current position estimation in Lat, Long [lat, long]
        """
        if self._q_prev is None:
            return None

        return utm.to_latlon(self._q_prev[0][0], self._q_prev[1][1], self._zone, self._zone_letter)

    @property
    def position_estimate(self):
        """
        Retrun most current position estimation 3x3 matrix, [0][0] - Easting, [1][1] - Northing, [2][2] - Heading
        """
        return self._q_prev

    def update(self, ax, ay, omega_z, gps_x_y_heading=None):
        """
        Update the EKF model

        :param ax: x-axis accelerometer reading in m/s^2
        :param ay: y-axis accelerometer reading in m/s^2

        :param gps_x_y_heading=None: numpy array with values [x, y, heading] in m,m,degrees. 
        This represents the gps' current non-stale location fix represented as meters from the center point.
        This parameter is NOT lat, long, heading. This is because our EKF model is [x,y,theta] due to the
        deadreckoning performed by the IMU when GPS is not available.

        NOTE: this behavior can be changed so that the model runs on [lat,long,heading] but will require constant
        conversions from degrees to meters from a center point and ultimately just makes the code more confusing
        """
        if self._q_prev is None:
            raise ValueError("Initial Position has not been set, call intial_position() with utm coordinates for starting point")

        q_next = np.array([[0.0, np.nan, np.nan],
                           [np.nan, 0.0, np.nan],
                           [np.nan, np.nan, 0.0]])

        # Integrate IMU data to predict next state before incorporating potential GPS data
        dt = time.monotonic() - self._last_time
        self._last_time = time.monotonic()

        # Distance along x axis from center point
        q_next[0][0] = self._q_prev[0][0] + (self._v_prev[0] * dt) + (ax - self._ax_prev) * (dt**2 / 2)
        # Distance along y axis from center point
        q_next[1][1] = self._q_prev[1][1] + (self._v_prev[1] * dt) + (ay - self._ay_prev) * (dt**2 / 2)
        # Heading
        q_next[2][2] = self._q_prev[2][2] + (omega_z - self._omega_z_prev) * dt
        self._omega_z_prev = omega_z

        # # Update velocity calculation
        self._v_prev = np.array([self._v_prev[0] + (ax - self._ax_prev) * dt, 
                                 self._v_prev[1] + (ay - self._ay_prev) * dt])
        self._ax_prev, self._ay_prev = ax, ay

        # Update state jacobian
        f_x = np.array([[1, 0, 0],
                       [0, 1, 0],
                       [0, 0, 1]])
        
        # Update noise jacobian
        f_v = np.array([[dt**2 / 2, 0, 0],
                       [0, dt**2 / 2, 0],
                       [0, 0, dt]])

        # Update process noise matrix with IMU noise
        p = (f_x * self._p_prev * f_x.transpose()) + (f_v * self._imu_noise_cov * f_v.transpose())

        if gps_x_y_heading is not None:
            if gps_x_y_heading[2] is None or np.isnan(gps_x_y_heading[2]):
                gps_x_y_heading[2] = 0

            s = p + self._gps_noise_cov

            # Kalman Gain
            k = p / s

            # Innovation
            v = gps_x_y_heading - q_next

            # Update state estimate with gps data
            q_next = q_next + (k * v)

            # Update uncertainty covariance
            p = p - (k * p)

        self._q_prev, self._p_prev = q_next, p