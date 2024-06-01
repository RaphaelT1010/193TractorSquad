
import pigpio
import time
import subprocess

# Start the pigpiod daemon


class motor:
    def __init__(self):
        subprocess.run(['sudo', 'pigpiod'])
        self.pi = pigpio.pi()

        # Check if pigpio daemon is running
        if not self.pi.connected:
            print("Failed to connect to pigpio daemon")
            exit()

        # Define GPIO pins for PWM control
        self.PWM_PIN_1 = 23  # GPIO pin for motor 1
        self.PWM_PIN_2 = 24  # GPIO pin for motor 2

        # Set PWM range (standard for RC control is 1000-2000 microseconds)
        self.PWM_RANGE = 20000  # microseconds for one period

        # Set the frequency for PWM (e.g., 50Hz for RC control)
        self.PWM_FREQUENCY = 50

        # Set the initial speed for both motors (range 0-100)
        self.INITIAL_SPEED = 20

        # Configure PWM pins
        self.pi.set_mode(self.PWM_PIN_1, pigpio.OUTPUT)
        self.pi.set_mode(self.PWM_PIN_2, pigpio.OUTPUT)
        self.pi.set_PWM_frequency(self.PWM_PIN_1, self.PWM_FREQUENCY)
        self.pi.set_PWM_frequency(self.PWM_PIN_2, self.PWM_FREQUENCY)
        self.pi.set_PWM_range(self.PWM_PIN_1, self.PWM_RANGE)
        self.pi.set_PWM_range(self.PWM_PIN_2, self.PWM_RANGE)

    def set_motor_speed(self, pin, speed):
        """
        Set motor speed.
        
        :param pin: GPIO pin connected to the Sabertooth input
        :param speed: Motor speed (-100 to 100)
        """
        # Convert speed (-100 to 100) to PWM pulse width (1000 to 2000 microseconds)
        pulse_width = 1500 + (speed * 5)  # Map speed to 1000-2000 us
        self.pi.set_servo_pulsewidth(pin, pulse_width)

    def drive_forward(self):
        self.set_motor_speed(self.PWM_PIN_1, -40)
        self.set_motor_speed(self.PWM_PIN_2, 28)
        time.sleep(1)

    def drive_backwards(self):
        self.set_motor_speed(self.PWM_PIN_1, 29)
        self.set_motor_speed(self.PWM_PIN_2, -40)
        time.sleep(1)

    def turn_left(self):
        self.set_motor_speed(self.PWM_PIN_1, -50)
        self.set_motor_speed(self.PWM_PIN_2, 28)
        time.sleep(2)

    def turn_right(self):
        self.set_motor_speed(self.PWM_PIN_1, -40)
        self.set_motor_speed(self.PWM_PIN_2, 38)
        time.sleep(2)

    def stop(self):
        self.set_motor_speed(self.PWM_PIN_1, -10)
        self.set_motor_speed(self.PWM_PIN_2, -10)
'''
    def pivotCW(self):
        self.set_motor_speed(self.PWM_PIN_1, self.INITIAL_SPEED-5)
        self.set_motor_speed(self.PWM_PIN_2, self.INITIAL_SPEED)
        time.sleep(2)

    def pivotCCW(self):
        self.set_motor_speed(self.PWM_PIN_1, self.INITIAL_SPEED)
        self.set_motor_speed(self.PWM_PIN_2, self.INITIAL_SPEED-10)
        time.sleep(2)

    def face_correct_heading(self, adj_heading, adj_direction):
        if abs(adj_heading) < 10:
            return
        else: 
            num_of_pivots = adj_direction//10
            match (adj_direction):
                case "CW":            
                    for i in range(num_of_pivots):
                        self.pivotCW()
                case "CCW":
                    for i in range(num_of_pivots):
                        self.pivotCCW()

            self.stop()

    def movement_correction(self, adj_heading, adj_direction):
        if abs(adj_heading) < 10:
            return
        else: 
            match (adj_direction):
                case "CW":            
                    self.turn_left()
                case "CCW":
                    self.turn_right()

        self.drive_forward()

'''