import cv2
import face_recognition
import argparse
from time import gmtime, strftime
import os

ap = argparse.ArgumentParser()
ap.add_argument("-s","--saving_folder",type=str,required=True,help="path to the saving folder")
ap.add_argument("-f","--extract_faces",default=False,help="your face will be extracted to the single image")
ap.add_argument("-v","--source_video",help="load from video")
ap.add_argument("-wc","--webcam_index",default=0,type=int,help="your webcam index in case you are using a lot of cameras")
args = vars(ap.parse_args())

def saveImage(img,savingFolder):
	imgName = "img_" + strftime("%H:%M:%S",gmtime()) + ".jpg"
	imgPath = os.path.join(savingFolder,imgName)

	cv2.imwrite(imgPath,img)

	print ("[IMAGE] Saved {}".format(imgPath))

def saveFace(img,box,savingFolder):
	(top,right,bottom,left) = box

	ROI = img[top:bottom,left:right]

	imgName = "face_" + strftime("%H:%M:%S",gmtime()) + ".jpg"
	imgPath = os.path.join(savingFolder,imgName)

	cv2.imwrite(imgPath,ROI)

	print ("[FACE] Saved {}".format(imgPath))

def main():
	if (args["source_video"]):
		cap = cv2.VideoCapture(args["source_video"])
	else:
		cap = cv2.VideoCapture(args["webcam_index"])


	while (cap.isOpened()):

		ret,frame = cap.read()

		rgb_img = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)

		face_locations = face_recognition.face_locations(rgb_img,model="hog")

		if len(face_locations) > 0:

			bgr_save = cv2.cvtColor(rgb_img,cv2.COLOR_RGB2BGR)

			saveImage(bgr_save,args["saving_folder"])

			if (args["extract_faces"]):
				saveFace(bgr_save,face_locations[0],args["saving_folder"])

			for face_location in face_locations:
				(top,right,bottom,left) = face_location

				cv2.rectangle(rgb_img,(left,top),(right,bottom),(0,255,0),2)

		bgr_img = cv2.cvtColor(rgb_img,cv2.COLOR_RGB2BGR)

		cv2.imshow("frame",bgr_img)

		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

	cap.release()
	cv2.destroyAllWindows()

main()