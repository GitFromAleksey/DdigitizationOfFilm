import os
import time
import datetime
##import serial
##import serial.tools.list_ports
##import random
##from struct import *
##from collections import namedtuple

import comport
import filmgui
import webcam

LOG_FILE_NAME = 'log_'
LOG_FILE_EXT = '.txt'

serial_port = comport.SerialPort()
gui = filmgui.FilmGui()
cam = webcam.Cam()

## -----------------------------------------------------------------------------
def LogToFile(data):
    dt = datetime.datetime.now()
    f_name = LOG_FILE_NAME + dt.strftime("%d.%m.%Y_%H") + LOG_FILE_EXT
    log_string = dt.strftime("[%d.%m.%Y %H.%M.%S.%f] - ") + str(data) + '\r'
    print(log_string)
    f = open(f_name, 'a')
    f.write(log_string)
    f.close()
## -----------------------------------------------------------------------------
def ComboCalback(args):
    port_name = args.widget.get()
    print('ComboCalback:', port_name)
    serial_port.SetPort(port_name)
## -----------------------------------------------------------------------------
def CallbackButtonSearchPorts(args):
    print('CallbackButtonSearchPorts press:',args)
##    serial_port.CheckAllPortsThread()
##    aval_ports = serial_port.GetListAvaliablePorts()
    aval_ports = serial_port.GetAllPorts()
    gui.ComboBoxAddItems(aval_ports)
## -----------------------------------------------------------------------------
def CallbackButtonOpenPort(args):
    print('CallbackButtonOpenPort press:',args)
    serial_port.OpenPort()
## -----------------------------------------------------------------------------
def CallbackButtonGetImage(args):
    print('CallbackButtonGetImage press:',args)
    cam.GetImageFromUsingCam()
## -----------------------------------------------------------------------------
def CallBackSerialPortInfo(text):
    gui.TextBoxAddText(text)
## -----------------------------------------------------------------------------
def main():

    gui.ComboBoxBind(ComboCalback)
    gui.ButtonSearchPortsBind(CallbackButtonSearchPorts)
    gui.ButtonOpenPortBind(CallbackButtonOpenPort)
    gui.ButtonGetImageBind(CallbackButtonGetImage)

    serial_port.SetLoggerCallback(CallBackSerialPortInfo)

    cam.SetUsingCam(0)
    cam.SetLoggerCallback(CallBackSerialPortInfo)
    cam.GetImageFromUsingCam()

    gui.Start()
    print('main program exit')
##    LogToFile(123)
##    jLink_port = ''
##    ports_dict = {}
##
##    ports = serial.tools.list_ports.comports()
##    for port, desc, hwid in sorted(ports):
##        print("{}: {} [{}]".format(port, desc, hwid))
##
##    com_number = input('Input COM port number:')
##    for port, desc, hwid in sorted(ports):
##        name = 'COM' + com_number
##        if port.find(name) > -1:
##            print("{}: {} [{}]".format(port, desc, hwid))
##            jLink_port = name
##
##    if len(jLink_port) == 0:
##        print('invalid COM port number')
##        return
##
##    ser = serial.Serial(
##        port = jLink_port,
##        baudrate = 9600, #115200
##        parity = serial.PARITY_NONE,
##        stopbits = serial.STOPBITS_ONE,
##        bytesize = serial.EIGHTBITS,
##        timeout = 0)
##
##    ret = 'ret\r'
##    cnt = 0
##
##    while True:
##        rx_bytes = ser.readline()
##        
##        if len(rx_bytes):
##            LogToFile('rx_bytes: ' + ':'.join('{:02x}'.format(b) for b in rx_bytes))
##
##            if tx_bytes:
####                LogToFile('tx_bytes: ' + ':'.join('{:02x}'.format(b) for b in tx_bytes))
##                ser.write(tx_bytes)


if __name__ == '__main__':
    main()
