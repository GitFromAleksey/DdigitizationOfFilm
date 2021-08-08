import time
import serial
import serial.tools.list_ports
import threading
import multiprocessing 

print('import:', __name__)
##------------------------------------------------------------------------------
##class SerialPort():
class SerialPort():

    def __init__(self):
        self.using_port = None
        self.aval_ports = []
        self.LoggerCallback = None
        self.write_queue = multiprocessing.Queue()

    def SetLoggerCallback(self, LoggerCallback):
        self.LoggerCallback = LoggerCallback

    def Logger(self, info):
        if self.LoggerCallback != None:
            self.LoggerCallback(info)
        print(info)

    def SetPort(self, port_name):
        self.Logger('SetPort:'+ port_name)
        self.using_port = serial.Serial()
        self.using_port.setPort(port_name)
        self.using_port.writeTimeout = 2
##        self.using_port = serial.Serial(
##                port = port_name,
##                baudrate = 9600, #115200
##                parity = serial.PARITY_NONE,
##                stopbits = serial.STOPBITS_ONE,
##                bytesize = serial.EIGHTBITS,
##                timeout = 0)
        self.Logger('BAUDRATES:' + str(self.using_port.BAUDRATES))
        self.Logger('BYTESIZES:' + str(self.using_port.BYTESIZES))
        self.Logger('PARITIES:' + str(self.using_port.PARITIES))
        self.Logger('STOPBITS:' + str(self.using_port.STOPBITS))
        self.Logger(str(self.using_port))

    def ClosePort(self):
        self.using_port.close()

    def OpenPort(self):
        if self.using_port == None:
            self.Logger('select port name')
            return
        self.Logger('OpenPort:' + self.using_port.port)
        if self.using_port.isOpen():
            self.Logger('Port:' + self.using_port.port + ' is open')
            return
        try:
            self.Logger('Try OpenPort:' + self.using_port.port)
            self.using_port.open()
            self.Logger(str(self.using_port))
            th_read = threading.Thread(target = self.ReadFromPort)
            th_read.start()
            th_write = threading.Thread(target = self.WritePortThread)
            th_write.start()
        except(OSError, serial.SerialException):
            self.Logger('Error open port:' + str(OSError))

    def ReadFromPort(self):
        self.Logger('strart read from port')
        while self.using_port.isOpen():
            time.sleep(0.01)
            self.Logger(str(self.using_port.read()))
        self.Logger('stop read from port:' + self.using_port.port)

    def WriteData(self, data_bytes):
        for d in data_bytes:
            self.write_queue.put(bytes([d]))

    def WritePortThread(self):
        while self.using_port.isOpen():
            time.sleep(0.1)
            while self.write_queue.qsize() > 0:
                data = self.write_queue.get()
                self.Logger('WritePortThread: ' + str(data))
                self.using_port.write(data)

    def ClosePort(self):
        self.using_port.close()
        self.Logger('Port close:'+ self.using_port.port)

    def GetListAvaliablePorts(self):
        return self.aval_ports

    def GetUsingPort(self):
        return self.using_port

    def GetAllPorts(self):
        self.UpdatePortsList()
        port_list = []
        for port_name, desc, hwid in sorted(self.port_list):
            port_list.append(port_name)
            self.Logger(port_name)
        return port_list

    def UpdatePortsList(self):
        '''Обновляет список доступных в системе COM портов'''
        self.port_list = serial.tools.list_ports.comports()
        for port in self.port_list:
            self.Logger('Port:' + str(port))

    def CheckAllPortsThread(self):
        th = threading.Thread(target = self.CheckAllPorts)
        th.start()

    def CheckAllPorts(self):
        self.UpdatePortsList()
        '''составляет список доступных портов'''
        if len(self.port_list) == 0:
            return
        for port_name, desc, hwid in sorted(self.port_list):
            if self.CheckPort(port_name) == True:
                self.aval_ports.append(port_name)

        self.Logger('Avaliable ports:'+ str(self.aval_ports))
        return self.aval_ports

    def CheckPort(self, port_name):
        '''Проверка порта на занятость'''
        try:
            self.Logger('CheckPort:'+ port_name)
            s = serial.Serial(port_name)
            s.close()
            self.Logger('Avaliable')
            return True
        except(OSError, serial.SerialException):
            self.Logger('Not Avaliable')
            return False

##------------------------------------------------------------------------------
def main():
    serial_port = SerialPort()
    serial_port.GetAllPorts()
    port_name = input('Input port name:')
    serial_port.SetPort(port_name)
    serial_port.OpenPort()

    time.sleep(1)
    data_bytes = b'hello!'
    serial_port.WriteData(data_bytes)
    time.sleep(10)
    serial_port.ClosePort()
##    serial_port.CheckAllPortsThread()
    time.sleep(1)
    print('exit main')



if __name__ == '__main__':
    main()
