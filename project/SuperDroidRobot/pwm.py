import pigpio
import time

# Initialize pigpio library
pi = pigpio.pi()

# Check if pigpio daemon is running
if not pi.connected:
    print("Failed to connect to pigpio daemon")
    exit()

# Define GPIO pins for PWM control
PWM_PIN_1 = 23  # GPIO pin for motor 1
PWM_PIN_2 = 24  # GPIO pin for motor 2

# Set PWM range (standard for RC control is 1000-2000 microseconds)
PWM_RANGE = 1000  # Adjust as needed

# Set the frequency for PWM (e.g., 50Hz for RC control)
PWM_FREQUENCY = 50

# Set the initial speed for both motors (range 0-100)
INITIAL_SPEED = 5

# Configure PWM pins
pi.set_mode(PWM_PIN_1, pigpio.OUTPUT)
pi.set_mode(PWM_PIN_2, pigpio.OUTPUT)
pi.set_PWM_frequency(PWM_PIN_1, PWM_FREQUENCY)
pi.set_PWM_frequency(PWM_PIN_2, PWM_FREQUENCY)
pi.set_PWM_range(PWM_PIN_1, PWM_RANGE)
pi.set_PWM_range(PWM_PIN_2, PWM_RANGE)

def set_motor_speed(pin, speed):
    # Convert speed (0-100) to PWM duty cycle (0-PWM_RANGE)
    pulse_width = int(speed / 100 * PWM_RANGE)
    # Ensure pulse_width is within range
    pulse_width = max(0, min(pulse_width, PWM_RANGE))
    # Set PWM duty cycle
    pi.set_PWM_dutycycle(pin, pulse_width)

# Example: Stop both motors
set_motor_speed(PWM_PIN_1, 0)
set_motor_speed(PWM_PIN_2, 0)
time.sleep(2)

try:
    while True:
        # Example: Drive both motors forward at half speed
        print("Set speed to half fowards")
        set_motor_speed(PWM_PIN_1, INITIAL_SPEED)
        set_motor_speed(PWM_PIN_2, -INITIAL_SPEED)
        time.sleep(2)

	# Example: Stop both motors
        set_motor_speed(PWM_PIN_1, 0)
        set_motor_speed(PWM_PIN_2, 0)
        time.sleep(2)

        # Example: Drive both motors backward at half speed
        print("set speed to half backwards")
        set_motor_speed(PWM_PIN_1, -INITIAL_SPEED)
        set_motor_speed(PWM_PIN_2, INITIAL_SPEED)
        time.sleep(2)

        # Example: Stop both motors
        set_motor_speed(PWM_PIN_1, 0)
        set_motor_speed(PWM_PIN_2, 0)
        time.sleep(2)

except KeyboardInterrupt:
    # Cleanup on exit
    set_motor_speed(PWM_PIN_1, 0)
    set_motor_speed(PWM_PIN_2, 0)
    pi.stop()
