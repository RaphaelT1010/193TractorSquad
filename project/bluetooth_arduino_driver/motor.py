
import pigpio
import time
import subprocess


# Start the pigpiod daemon


class motor:
    def __init__(self):
        #subprocess.run(['sudo', 'pigpiod'])
        self.pi = pigpio.pi()

        # Check if pigpio daemon is running
        if not self.pi.connected:
            print("Failed to connect to pigpio daemon")
            exit()

        # Define GPIO pins for PWM control
        # if start and end buttons are front of robot 
        # from perspective where looking from the front
        self.PWM_PIN_1 = 23  # GPIO pin for motor 1 : right motors
        self.PWM_PIN_2 = 24  # GPIO pin for motor 2 : left motors 

        # Set PWM range (standard for RC control is 1000-2000 microseconds)
        self.PWM_RANGE = 20000  # microseconds for one period

        # Set the frequency for PWM (e.g., 50Hz for RC control)
        self.PWM_FREQUENCY = 50

        # Set the initial speed for both motors (range 0-100)
        self.INITIAL_SPEED = 20
        
        # set the inital time duration for motors to run
        self.TIME_DURATION = 0.5 
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

    def move_left_motor_forward(self, speed = 78):
        self.set_motor_speed(self.PWM_PIN_2, speed)
    
    def move_left_motor_backwards(self, speed = -70):
        self.set_motor_speed(self.PWM_PIN_2, speed)

    def move_right_motor_forward(self, speed = -90):
        self.set_motor_speed(self.PWM_PIN_1, speed)

    def move_right_motor_backwards(self, speed = 59):
        self.set_motor_speed(self.PWM_PIN_1, speed)

    def drive_forward(self):
        self.move_left_motor_forward()
        self.move_right_motor_forward()        
        time.sleep(self.TIME_DURATION)

    def drive_backwards(self):
        self.move_left_motor_backwards()
        self.move_right_motor_backwards()
        
        time.sleep(self.TIME_DURATION)

    def turn_left(self):
        self.move_left_motor_forward()
        self.move_right_motor_forward(-80)        
        time.sleep(self.TIME_DURATION)

    def turn_right(self):
        self.move_left_motor_forward(78)
        self.move_right_motor_forward(-30)    
        time.sleep(self.TIME_DURATION)

    def stop(self):
        self.set_motor_speed(self.PWM_PIN_1, -10)
        self.set_motor_speed(self.PWM_PIN_2, -10)

    def pivotCW(self):
        self.move_left_motor_forward()
        self.move_right_motor_backwards()    
        time.sleep(0.4)

    def pivotCCW(self):
        self.move_right_motor_forward()
        self.move_left_motor_backwards()    
        time.sleep(0.4)

    def face_correct_heading(self, adj_heading, adj_direction):
        if abs(adj_heading) < 10:
            return
        else: 
            num_of_pivots = int(abs(adj_heading//20))
            print(num_of_pivots)
            match (adj_direction):
                case "CW":            
                    for i in range(num_of_pivots):
                        self.pivotCW()
                case "CCW":
                    for i in range(num_of_pivots):
                        self.pivotCCW()

        self.stop()
'''
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
