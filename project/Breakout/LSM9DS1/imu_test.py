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
    ahrs.update_imu(np.array([float(i)*np.pi/180 for i in list(sensor.gyro)]), \
                     np.array(np.array([float(i) for i in list(sensor.acceleration)])))
    heading = ahrs.quaternion.to_euler_angles()
    heading = [i*180/np.pi for i in heading]
    print(f"Roll: {heading[0]} Pitch: {heading[1]} Yaw: {heading[2]}")
    #print(f"Yaw: {heading[2]}")        
'''
import agroguardian_imu_py
from agroguardian_ekf_py import ekf
import sys

imu = agroguardian_imu_py.AgroGuardianImu()
#pose_model = ekf.ExtendedKalmanFilter(0,0)

error = imu.determine_error()

ahrs = mw.MadgwickAHRS()
#print(imu.determine_error())

while True:
    imu_f_sample = imu.accelerometer[0:2] - error[0:2]
    imu_f_sample = np.append(imu_f_sample, imu.accelerometer[2])
    imu_w_sample = imu.gyroscope * (np.pi/180)
    imu_m_sample = imu.magnetometer

    # pose_model.set_next_state(imu_f_sample, imu_w_sample)
    # orientation = pose_model.euler_angles * 180/np.pi

    ahrs.update(imu_w_sample.tolist(), imu_f_sample.tolist(), imu_m_sample.tolist())
    #orientation = ahrs.orientation_degrees

    # sys.stdout.write(f"\rInversion: "
    #                 + f"aX: {round(imu_f_sample[0],3):<10}"
    #                 + f"aY: {round(imu_f_sample[1],3):<10}"
    #                 + f"aZ: {round(imu_f_sample[2],3):<10}"
    #                 + f"gX: {round(imu_w_sample[0],3):<10}"
    #                 + f"gY: {round(imu_w_sample[1],3):<10}"
    #                 + f"gZ: {round(imu_w_sample[2],3):<10}"
    #                 + f"X: {round(orientation[0],3):<10}"
    #                 + f"Y: {round(orientation[2],3):<10}"
    #                 + f"Z: {round(orientation[1],3):<10}")
    # sys.stdout.flush()   

    # print(imu.update_madgwick_6dof_orientation())
    print(imu.update_madgwick_9dof_orientation())
    #print(pose_model.position_estimate())
'''
