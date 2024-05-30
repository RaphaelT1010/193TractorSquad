import serial

class motor:
    def __init__(self, port='/dev/ttyACM0', baudrate=9600):
        self.ser = serial.Serial(port, baudrate)

    def drive_forward(self):
        cmd = b'w\r\n'
        self.ser.write(cmd)

    def drive_backwards(self):
        cmd = b's\r\n'
        self.ser.write(cmd)

    def turn_left(self):
        cmd = b'a\r\n'
        self.ser.write(cmd)

    def turn_right(self):
        cmd = b'd\r\n'
        self.ser.write(cmd)

    def stop(self):
        cmd = b'stop\r\n'
        self.ser.write(cmd)

    def pivotCW(self):
        print("Pivot Clockwise")
        self.ser.write(b'CC\r\n')

    def pivotCCW(self):
        print("Pivot Counterclockwise")
        self.ser.write(b'CCW\r\n')

    def faceCorrectHeading(self, destHeading, currentHeading):
        print(f"currentHeading: {currentHeading}")
        print(f"destHeading: {destHeading}")

        resultheading = destHeading - currentHeading
        resultheading = (resultheading + 360) % 360  # Normalize to 0-360

        if resultheading > 180:
            resultheading -= 360  # Normalize to -180 to 180

        if resultheading < 0:
            self.pivotCW()
        else:
            self.pivotCCW()

