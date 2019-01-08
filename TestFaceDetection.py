import urllib
import cv2
import numpy as np
from time import gmtime, strftime
import dlib
import imutils

cameraURL = 'http://admin:capstech@10.10.14.78:80/image.jpg'

haarcascade_face_file_path = 'haarcascade_frontalface_default.xml'

detector = dlib.get_frontal_face_detector()

# init
face_cascade = cv2.CascadeClassifier(haarcascade_face_file_path)

# for loading
def LoadImageFromIPCamera(url):
	imgFromURL = urllib.urlopen(url)
	imgNp = np.array(bytearray(imgFromURL.read()),dtype=np.uint8)
	img = cv2.imdecode(imgNp,-1)
	return img

# for processing
def getFacesDetection(img):
	beta = 0
	alpha = 1.5

	img = np.int16(img)
	img = img*(alpha/127+1) - alpha + beta
	img = np.clip(img,0,255)
	img = np.uint8(img)


	cv2.imshow('Source',img)
	dets = detector(img,1)

	for i,d in enumerate(dets):
		x = d.left()
		y = d.top()
		width = d.right() - x
		height = d.bottom() - y

		cv2.rectangle(img,(x,y),(x + width,y + height),(0,255,0),2)


	cv2.imshow('Detected Face',img)


def savingFacesData(faces,saveFolder):
	for face in faces:
		cv2.imwrite(saveFolder + "face_" + strftime("%H:%M:%S",gmtime()) + ".png",face)



#run in main
def main():
	while True:
		cameraImg = LoadImageFromIPCamera(cameraURL)
		getFacesDetection(cameraImg)

		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

	cv2.destroyAllWindows()


main()
