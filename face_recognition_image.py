import face_recognition
import cv2
import argparse
from imutils import paths
import os
import pickle

ap = argparse.ArgumentParser()
ap.add_argument("-e","--encoding_dataset",help="path to input dataset to encoding. Ex: Dataset/people1.png, people2.png ....")
ap.add_argument("-i","--input_image",required=True,help="The input image to recognize")
ap.add_argument("-o","--output_image",required=True,help="The path of output image to save")
ap.add_argument("-de","--detection_method",type=str,default="cnn",help="The method to detect. Choose 'hog' or 'cnn'")
ap.add_argument("-ef","--encoding_file",help="path to encoding file")
ap.add_argument("-s","--save_encoding_file",help="path to saved file")

args = vars(ap.parse_args())

def listImageFile():
	print "Loading File ..."
	dataset = args["encoding_dataset"]
	imagePaths = list(paths.list_images(dataset))

	for img in imagePaths:
		print img

	return imagePaths

def createEncodings():
	imageFiles = listImageFile()
	print "Creating Encoding Data..."

	known_encodings = []
	known_names = []

	for img_file in imageFiles:
		print ("[INFO] processing image: ",img_file)

		img = face_recognition.load_image_file(img_file)
		boxes = face_recognition.face_locations(img,model=args["detection_method"])

		name = img_file.split(os.path.sep)[-2]

		encodin_img = face_recognition.face_encodings(img,boxes)[0]

		known_encodings.append(encodin_img)
		known_names.append(name)

	print "Encoding data is done !"

	return known_encodings,known_names

def loadEncodings(encodingFile):
	data = pickle.loads(open(encodingFile,"rb").read())

	return data["encodings"],data["names"]


def writeEncodingDataToFile(known_encodings,known_names):
	print "Saving encoding file ..."

	data = {"encodings": known_encodings,"names": known_names}

	f = open(args["save_encoding_file"],"wb")

	f.write(pickle.dumps(data))

	f.close()

	print "Saving is done !"

def saveImage(img,inverseColor=True):
	if(inverseColor):
		img = cv2.cvtColor(img,cv2.COLOR_RGB2BGR)

	cv2.imwrite(args["output_image"],img)

def loadImage():
	input_img = face_recognition.load_image_file(args["input_image"])
	return input_img

def processingFaceData(input_img,known_encodings,known_names):
	face_locations = face_recognition.face_locations(input_img,model=args["detection_method"])

	encodings = face_recognition.face_encodings(input_img,face_locations)

	names = []

	for encoding in encodings:

		matches = face_recognition.compare_faces(known_encodings,encoding)

		name = "Unknown"

		if True in matches:
			matchedIndex = [i for (i,b) in enumerate(matches) if b]

			#create a dictionary includes a pair value which are the name and the number of the name approach	
			counts = {}

			for i in matchedIndex:
				name = known_names[i]
				counts[name] = counts.get(name,0) + 1

			name = max(counts,key=counts.get)

		names.append(name)

	return face_locations,names

def drawFaces(input_img,face_locations,names):
	for ((top,right,bottom,left),name) in zip(face_locations,names):
		cv2.rectangle(input_img,(left,top),(right,bottom),(0,255,0),2)
		y = top - 15 if top - 15 > 15 else top + 15
		cv2.putText(input_img,name,(left,y),cv2.FONT_HERSHEY_SIMPLEX,0.75,(0,255,0),2,cv2.LINE_AA)

	input_img = cv2.cvtColor(input_img,cv2.COLOR_RGB2BGR)
	cv2.imshow('faces',input_img)
	cv2.waitKey(0)

	return input_img


def main():
	if(args["encoding_dataset"]):
		known_encodings,known_names = createEncodings()	
	else:
		if(args["encoding_file"]):
			known_encodings,known_names = loadEncodings(args["encoding_file"])
		else:
			print "Encoding Data is not set. You are missing some important parameter."
			return

	if(args["save_encoding_file"]):
		if(args["encoding_file"]):
			print "Detect encoding file in the parameters. Saving file will be ignored"
		else:
			writeEncodingDataToFile(known_encodings,known_names)

	if(known_encodings and known_names):
		img = loadImage()
		face_locations,names =  processingFaceData(img,known_encodings,known_names)
		img = drawFaces(img,face_locations,names)
		saveImage(img,False)

	else:
		print "Encoding data is not found. Something gone wrong !"

main()
