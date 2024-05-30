import pigpio
import time

# Initialize pigpio library
pi = pigpio.pi()

# Check if pigpio daemon is running
if not pi.connected:
    print("Failed to connect to pigpio daemon")
    exit()

# Define the GPIO pin for software serial
SOFT_TX_PIN = 23
BAUD_RATE = 9600

# Open a software serial connection on GPIO 23 with baudrate 9600
pi.bb_serial_read_open(SOFT_TX_PIN, BAUD_RATE)

def send_command(command):
    pi.wave_clear()
    # Convert the command to a bit stream
    waveform = []
    for bit in range(8):
        level = pigpio.PI_HIGH if command & (1 << (7 - bit)) else pigpio.PI_LOW
        waveform.append(pigpio.pulse(level, not level, int(1e6 / BAUD_RATE)))
    pi.wave_add_generic(waveform)
    wave_id = pi.wave_create()
    pi.wave_send_once(wave_id)
    while pi.wave_tx_busy():
        time.sleep(0.001)

def drive_motor_1(speed):
    # Motor 1 forward: 0x00 to 0x7F (0 to 127)
    # Motor 1 backward: 0x80 to 0xFF (128 to 255)
    command = speed & 0xFF  # Ensure command is within byte range
    send_command(command)

def drive_motor_2(speed):
    # Motor 2 forward: 0x00 to 0x7F (0 to 127)
    # Motor 2 backward: 0x80 to 0xFF (128 to 255)
    command = (speed & 0xFF) + 1  # Motor 2 commands are offset by 1
    send_command(command)

try:
    while True:
        # Example: Drive motor 1 forward at half speed
        drive_motor_1(64)  # 50% forward speed
        time.sleep(2)

        # Example: Drive motor 1 backward at half speed
        drive_motor_1(192)  # 50% backward speed (128 + 64)
        time.sleep(2)

        # Example: Stop motor 1
        drive_motor_1(0)  # Stop
        time.sleep(2)

except KeyboardInterrupt:
    # Stop motors on exit
    drive_motor_1(0)
    drive_motor_2(0)
    pi.bb_serial_read_close(SOFT_TX_PIN)
    pi.stop()

