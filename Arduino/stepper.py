import time
import serial
import serial.tools.list_ports as ports
import io

SERIAL_PORT = 'COM3'

class Arduino:

    def __init__(self, arduino_port = ''):
        self.ser = serial.Serial()
        self.ser.port = arduino_port
        self.ser.baudrate = 9600
        self.ser.open()

    def __del__(self):
        self.ser.close()

    def Turn(self):
        ser = self.ser
        ser.write(b'START\n')
        time.sleep(1.5)
        while ser.in_waiting > 0:
            l = ser.readline()
            print(l)
        # time.sleep(1)

    def GetPortsList(self):
        prts = ports.comports()
        return prts

def main():

    ser = serial.Serial()
    sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))

    ser.port = SERIAL_PORT
    ser.baudrate = 9600
    ser.open()

    while(True):
        ser.write(b'START\n')
        # sio.write('START\n')
        # sio.flush()
        # sr = sio.readline()
        # print(sr)
        time.sleep(3)
        while ser.in_waiting > 0:
            l = ser.readline()
            print(l)


    ser.close()    

if __name__ == '__main__':
    main()