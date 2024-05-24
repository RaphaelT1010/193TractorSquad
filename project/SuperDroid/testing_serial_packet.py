import pigpio
import time

# Initialize pigpio library
pi = pigpio.pi()

# Define the GPIO pin for software serial (e.g., GPIO 18)
SOFT_TX_PIN = 18

# Set baud rate
BAUD_RATE = 9600

# Open the software serial on the chosen pin
pi.bb_serial_write_open(SOFT_TX_PIN, BAUD_RATE, 8)

def send_command(address, command, data):
    # Create packet
    packet = [address, command, data, (address + command + data) & 0x7F]
    # Send packet
    pi.bb_serial_write(SOFT_TX_PIN, packet)

def drive_forward_motor_1(speed):
    if 0 <= speed <= 127:
        send_command(128, 0, speed)
    else:
        raise ValueError("Speed must be between 0 and 127")

def drive_backward_motor_1(speed):
    if 0 <= speed <= 127:
        send_command(128, 1, speed)
    else:
        raise ValueError("Speed must be between 0 and 127")

def set_min_voltage(volts):
    if 6 <= volts <= 30:
        value = int((volts - 6) * 5)
        send_command(128, 2, value)
    else:
        raise ValueError("Voltage must be between 6 and 30")

def set_max_voltage(volts):
    if 6 <= volts <= 30:
        value = int((volts - 6) * 5)
        send_command(128, 3, value)
    else:
        raise ValueError("Voltage must be between 6 and 30")

try:
    while True:
        # Example: Drive motor 1 forward at half speed
        drive_forward_motor_1(64)
        time.sleep(2)

        # Example: Drive motor 1 backward at half speed
        drive_backward_motor_1(64)
        time.sleep(2)

        # Example: Set minimum voltage to 10V
        set_min_voltage(10)
        time.sleep(2)

        # Example: Set maximum voltage to 24V
        set_max_voltage(24)
        time.sleep(2)

except KeyboardInterrupt:
    # Cleanup on exit
    pi.bb_serial_write_close(SOFT_TX_PIN)
    pi.stop()
