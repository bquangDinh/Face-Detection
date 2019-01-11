import cv2
import face_recognition
import argparse
import pickle
import numpy as np

#some constants

#for drawing
RECTANGLE_COLOR = (0,255,0)
RECTANGLE_WEIGHT = 2

FONT_TYPE = cv2.FONT_HERSHEY_SIMPLEX
FONT_SIZE = 0.75
FONT_COLOR = (255,0,255)
FONT_WEIGHT = 2

ap = argparse.ArgumentParser()
ap.add_argument("-i","--input_video",help="The path of the video to process")
ap.add_argument("-wc","--webcam_index",help="Enter the integer which is the camera index. The default is 1",default=0,type=int)
ap.add_argument("-d","--detection_method",required=True,help="The method to detect. Choose between 'hog' or 'cnn'. The default is 'cnn'",default='cnn',type=str)
ap.add_argument("-ef","--encoding_file",required=True)
args = vars(ap.parse_args())

def loadEncodingData():
	print "Loading Encoding File ..."

	data = pickle.loads(open(args["encoding_file"],"rb").read())

	print "Loading finished !"

	print ("Names: {}".format(np.unique(data["names"])))

	return data["encodings"],data["names"]

def preProcessing(img):

	img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

	return img

def processInput(img,known_encodings,known_names):
	face_locations = face_recognition.face_locations(img,model=args["detection_method"])
	encodings = face_recognition.face_encodings(img,face_locations)

	names = []

	for encoding in encodings:
		matches = face_recognition.compare_faces(known_encodings,encoding)

		name = "Unknown"

		#for voting
		if True in matches:
			matchedIndex = [i for (i,b) in enumerate(matches) if b]
			counts = {}

			for i in matchedIndex:
				name = known_names[i]
				counts[name] = counts.get(name,0) + 1

			#Ex: {Dinh,Dinh,Dinh,Uyen,Uyen,Uyen,Uyen,Nhan,Nhan}
			#==> Max is Uyen ==> Uyen
			name = max(counts,key=counts.get)

		names.append(name)

	return face_locations,names

def drawFaces(img,face_locations,names):
	img = cv2.cvtColor(img,cv2.COLOR_RGB2BGR)

	for ((top,right,bottom,left),name) in zip(face_locations,names):
		cv2.rectangle(img,(left,top),(right,bottom),RECTANGLE_COLOR,RECTANGLE_WEIGHT)
		
		threshold = 15
		y = top - threshold if top - threshold > threshold else top + threshold

		cv2.putText(img,name,(left,y),FONT_TYPE,FONT_SIZE,FONT_COLOR,FONT_WEIGHT,cv2.LINE_AA)

	return img


def main():
	if(args["input_video"]):
		cap = cv2.VideoCapture(args["input_video"])
	else:
		if(args["webcam_index"] != None):
			cap = cv2.VideoCapture(args["webcam_index"])
		else:
			print "No input video. Exit the program."
			return 

	known_encodings,known_names = loadEncodingData()

	while (cap.isOpened()):
		ret,frame = cap.read()

		if ret == True:
			img = preProcessing(frame)

			face_locations,names = processInput(img,known_encodings,known_names)

			final_img = drawFaces(img,face_locations,names)

			cv2.imshow('faces',final_img)

			if cv2.waitKey(1) & 0xFF == ord('q'):
				break
		else:
			break

	cap.release()
	cv2.destroyAllWindows()

main()