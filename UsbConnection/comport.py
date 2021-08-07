import serial
import serial.tools.list_ports

print('import:', __name__)
##------------------------------------------------------------------------------
class SerialPort():
    def __init__(self):
        self.using_port = None
        self.aval_ports = []
        self.LoggerCallback = None

    def SetLoggerCallback(self, LoggerCallback):
        self.LoggerCallback = LoggerCallback

    def Logger(self, info):
        if self.LoggerCallback != None:
            self.LoggerCallback(info)
        print(info)

    def SetPort(self, port_name):
        self.Logger('SetPort:'+ port_name)
        self.using_port = serial.Serial(
                port = port_name,
                baudrate = 9600, #115200
                parity = serial.PARITY_NONE,
                stopbits = serial.STOPBITS_ONE,
                bytesize = serial.EIGHTBITS,
                timeout = 0)

    def OpenPort(self):
        if self.using_port == None:
            self.Logger('select port name')
            return
        self.Logger('self.using_port')
        try:
            self.Logger('OpenPort:')
            self.using_port.open()
        except(OSError, serial.SerialException):
            self.Logger('Error open port:')

    def ClosePort(self):
        self.using_port.close()
        self.Logger('Port close:'+ self.using_port.port)

    def GetListAvaliablePorts(self):
        return self.aval_ports

    def GetUsingPort(self):
        return self.using_port

    def GetAllPorts(self):
        self.UpdatePortsList()
        return self.port_list

    def UpdatePortsList(self):
        '''Обновляет список доступных в системе COM портов'''
        self.port_list = serial.tools.list_ports.comports()
        for port in self.port_list:
            self.Logger('Port:' + str(port))
##            print('Port:', port)

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

    port_number = input('Input com number:')
    print(port_number)
    port_name = 'COM' + str(port_number)
    print(port_name)

    serial_port.OpenPort(port_name)

    serial_port.CheckAllPorts()

    serial_port.ClosePort()



if __name__ == '__main__':
    main()
