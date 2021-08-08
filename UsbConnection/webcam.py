import time
import cv2.cv2 as cv

print ('cv.__version__:',cv.__version__)


class Cam():

    def __init__(self):
        self.cams_dict = {}
        self.using_cam = None
        self.SearchCams()

    def __del__(self):
        cv.destroyAllWindows()

    def SearchCams(self):
        for i in range(3):
            cam = cv.VideoCapture(i)
            if cam.isOpened():
                self.cams_dict[i] = cam
                print(cam.getBackendName(), i)

    def SetUsingCam(self, cam_num):
        self.using_cam = self.cams_dict[cam_num]

    def GetImageFromUsingCam(self):
        cam = self.using_cam
        ret, img = cam.read()
        if ret:
            cv.imshow(cam.getBackendName(), img)
##            cv.imwrite(str(time.time()) + '.jpg', img)
            cv.waitKey(1)

    def GetImagesFromAllCams(self):
        for key in self.cams_dict.keys():
            cam = self.cams_dict[key]
            ret, img = cam.read()
            cv.imshow(cam.getBackendName(), img)
            cv.imwrite(cam.getBackendName() + str(key) + '.jpg',img)



def main():
    cams = Cam()

    cams.SetUsingCam(1)

    for i in range(100):
        time.sleep(0.20)
        cams.GetImageFromUsingCam()
        
##    cams.GetImagesFromAllCams()
    pass


if __name__ == '__main__':
    main()
