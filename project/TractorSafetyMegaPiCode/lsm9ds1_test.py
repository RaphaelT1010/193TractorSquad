import board
import busio
import adafruit_lsm9ds1

try:

	# Create I2C bus
	i2c = busio.I2C(board.SCL, board.SDA)

	# Create LSM9DS1 instance
	sensor = adafruit_lsm9ds1.LSM9DS1_I2C(i2c)

	# Print accelerometer, gyro, and magnetometer readings
	while True:
		accel_x, accel_y, accel_z = sensor.acceleration
		gyro_x, gyro_y, gyro_z = sensor.gyro
		mag_x, mag_y, mag_z = sensor.magnetic

		print('Acceleration (m/s^2): X={0:0.3f} Y={1:0.3f} Z={2:0.3f}'.format(accel_x, accel_y, accel_z))
		print('Gyro (rad/s):        X={0:0.3f} Y={1:0.3f} Z={2:0.3f}'.format(gyro_x, gyro_y, gyro_z))
		print('Magnetic (uT):       X={0:0.3f} Y={1:0.3f} Z={2:0.3f}'.format(mag_x, mag_y, mag_z))

except Exception as e:
	print("An error as occurred:", e)
