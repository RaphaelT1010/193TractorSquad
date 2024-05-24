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

