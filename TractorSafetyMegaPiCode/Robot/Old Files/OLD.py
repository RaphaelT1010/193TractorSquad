import serial
import sys,time,math,random
import signal
from time import ctime,sleep
import glob,struct
from multiprocessing import Process,Manager,Array
import threading

class mSerial():
    ser = None
    def __init__(self):
        print(self)

    def start(self, port='/dev/ttyUSB0'):
        self.ser = serial.Serial(port,115200,timeout=10)

    def device(self):
        return self.ser

    def serialPorts(self):
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')
        result = []
        for port in ports:
            s = serial.Serial()
            s.port = port
            s.close()
            result.append(port)
        return result

    def writePackage(self,package):
        self.ser.write(package)
        sleep(0.01)

    def read(self):
        return self.ser.read()

    def isOpen(self):
        return self.ser.isOpen()

    def inWaiting(self):
        return self.ser.inWaiting()

    def close(self):
        self.ser.close()
M1 = 9
M2 = 10
A0 = 14
A1 = 15
A2 = 16
A3 = 17
A4 = 18
A6 = 19
A7 = 20
A8 = 21
A9 = 22
A10 = 23
A11 = 24

class MegaPi():
    def __init__(self):
        print("init MegaPi")
        signal.signal(signal.SIGINT, self.exit)
        self.manager = Manager()
        self.__selectors = self.manager.dict()
        self.buffer = []
        self.bufferIndex = 0
        self.isParseStart = False
        self.exiting = False
        self.isParseStartIndex = 0

    def __del__(self):
        self.exiting = True

    def start(self,port='/dev/ttyUSB0'):
        self.device = mSerial()
        self.device.start(port)
        sys.excepthook = self.excepthook
        th = threading.Thread(target=self.__onRead,args=(self.onParse,))
        th.start()

    def excepthook(self, exctype, value, traceback):
        self.close()

    def close(self):
        self.device.close()

    def exit(self, signal, frame):
        self.exiting = True
        sys.exit(0)

    def __onRead(self,callback):
        while True:
            if(self.exiting==True):
                break
            try:	
                if self.device.isOpen()==True:
                    n = self.device.inWaiting()
                    for i in range(n):
                        r = ord(self.device.read())
                        callback(r)
                    sleep(0.01)
                else:	
                    sleep(0.5)
            except Exception as ex:
                print(str(ex))
                self.close()
                sleep(1)
    def __writePackage(self,pack):
        self.device.writePackage(pack)

    def __writeRequestPackage(self,deviceId,port,callback):
        extId = ((port<<4)+deviceId)&0xff
        self.__doCallback(extId,callback)
        self.__writePackage(bytearray([0xff,0x55,0x4,extId,0x1,deviceId,port]))


    def motorRun(self,port,speed):
        self.__writePackage(bytearray([0xff,0x55,0x6,0x0,0x2,0xa,port]+self.short2bytes(speed)))

    def stopAllMotors(self):
        self.motorRun(1,0)
        self.motorRun(2,0)
        self.motorRun(M1,0)
        self.motorRun(M2,0)

    def moveForward(self):
        self.motorRun(1,-50)
        self.motorRun(2,50)
        self.motorRun(M1,-50)
        self.motorRun(M2,50)
    
    def moveBackwards(self):
        self.motorRun(1,50)
        self.motorRun(2,-50)
        self.motorRun(M1,50)
        self.motorRun(M2,-50)


    def onParse(self, byte):
        position = 0
        value = 0	
        self.buffer+=[byte]
        bufferLength = len(self.buffer)
        if bufferLength >= 2:
            if (self.buffer[bufferLength-1]==0x55 and self.buffer[bufferLength-2]==0xff):
                self.isParseStart = True
                self.isParseStartIndex = bufferLength-2	
            if (self.buffer[bufferLength-1]==0xa and self.buffer[bufferLength-2]==0xd and self.isParseStart==True):			
                self.isParseStart = False
                position = self.isParseStartIndex+2
                extID = self.buffer[position]
                position+=1
                type = self.buffer[position]
                position+=1
                # 1 byte 2 float 3 short 4 len+string 5 double
                if type == 1:
                    value = self.buffer[position]
                if type == 2:
                    value = self.readFloat(position)
                if(value<-512 or value>1023):
                    value = 0
                if type == 3:
                    value = self.readShort(position)
                if type == 4:
                    value = self.readString(position)
                if type == 5:
                    value = self.readDouble(position)
                if type == 6:
                    value = self.readLong(position)
                if(type<=6):
                    self.responseValue(extID,value)
                self.buffer = []

    def readFloat(self, position):
        v = [self.buffer[position], self.buffer[position+1],self.buffer[position+2],self.buffer[position+3]]
        return struct.unpack('<f', struct.pack('4B', *v))[0]

    def readShort(self, position):
        v = [self.buffer[position], self.buffer[position+1]]
        return struct.unpack('<h', struct.pack('2B', *v))[0]

    def readString(self, position):
        l = self.buffer[position]
        position+=1
        s = ""
        for i in range(l):
            s += self.buffer[position+i].charAt(0)
        return s
    def readDouble(self, position):
        v = [self.buffer[position], self.buffer[position+1],self.buffer[position+2],self.buffer[position+3]]
        return struct.unpack('<f', struct.pack('4B', *v))[0]

    def readLong(self, position):
        v = [self.buffer[position], self.buffer[position+1],self.buffer[position+2],self.buffer[position+3]]
        return struct.unpack('<l', struct.pack('4B', *v))[0]

    def responseValue(self, extID, value):
        self.__selectors["callback_"+str(extID)](value)

    def __doCallback(self, extID, callback):
        self.__selectors["callback_"+str(extID)] = callback

    def float2bytes(self,fval):
        val = struct.pack("f",fval)
        #return [ord(val[0]),ord(val[1]),ord(val[2]),ord(val[3])]
        return [val[0],val[1],val[2],val[3]]

    def long2bytes(self,lval):
        val = struct.pack("=l",lval)
        #return [ord(val[0]),ord(val[1]),ord(val[2]),ord(val[3])]
        return [val[0],val[1],val[2],val[3]]

    def short2bytes(self,sval):
        val = struct.pack("h",sval)
        #return [ord(val[0]),ord(val[1])]
        return [val[0],val[1]]
    def char2byte(self,cval):
        val = struct.pack("b",cval)
        #return ord(val[0])
        return val[0]

def main():
    bot = MegaPi()
    bot.start()
    bot.moveForward
    

if __name__ == "__main__":
    main()
