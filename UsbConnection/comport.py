import serial
import serial.tools.list_ports

print('import:', __name__)
##------------------------------------------------------------------------------
class SerialPort():
    def __init__(self):
        self.using_port = None
        self.aval_ports = []

    def SetPort(self, port_name):
        print('SetPort:', port_name)
        self.using_port = serial.Serial(
                port = port_name,
                baudrate = 9600, #115200
                parity = serial.PARITY_NONE,
                stopbits = serial.STOPBITS_ONE,
                bytesize = serial.EIGHTBITS,
                timeout = 0)

    def OpenPort(self):
        if self.using_port == None:
            print('select port name')
            return
        print(self.using_port)
        try:
            print('OpenPort:')
            self.using_port.open()
        except(OSError, serial.SerialException):
            print('Error open port:')

##    def OpenPort(self, port_name):
##        try:
##            print('OpenPort:', port_name)
####            self.using_port = serial.Serial(port_name)
##            self.using_port = serial.Serial(
##                port = port_name,
##                baudrate = 9600, #115200
##                parity = serial.PARITY_NONE,
##                stopbits = serial.STOPBITS_ONE,
##                bytesize = serial.EIGHTBITS,
##                timeout = 0)
##            self.using_port.open()
##        except(OSError, serial.SerialException):
##            print('Error open port:', port_name)

    def ClosePort(self):
        self.using_port.close()
        print('Port close:', self.using_port.port)

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
            print('Port:', port)

    def CheckAllPorts(self):
        self.UpdatePortsList()
        '''составляет список доступных портов'''
        if len(self.port_list) == 0:
            return
        for port_name, desc, hwid in sorted(self.port_list):
            if self.CheckPort(port_name) == True:
                self.aval_ports.append(port_name)

        print('Avaliable ports:', self.aval_ports)
        return self.aval_ports

    def CheckPort(self, port_name):
        '''Проверка порта на занятость'''
        try:
            print('CheckPort:', port_name)
            s = serial.Serial(port_name)
            s.close()
            print('Avaliable')
            return True
        except(OSError, serial.SerialException):
            print('Not Avaliable')
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
