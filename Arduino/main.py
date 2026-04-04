from stepper import Arduino
from camera import Camera

SERIAL_PORT = 'COM3'

def main():

    ard = Arduino(SERIAL_PORT)
    cam = Camera()
    cam.CamOpen()

    for i in range(10000):
        ard.Turn()
        cam.SaveImage('out/'+str(i)+'.jpg')


    cam.CamClose()

if __name__ == '__main__':
    main()