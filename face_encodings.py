import face_recognition
import pickle
from imutils import paths
import os
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-dt","--dataset",required=True,help="path to input face dataset")
ap.add_argument("-o","--output_encodings",required=True,help="encodings file name")
ap.add_argument("-de","--detection_method",default="cnn",type=str,help="The method to detect faces. Choose between 'hog' or 'cnn'")
args = vars(ap.parse_args())

def listImageFile():
	print "Loading File ..."

	dataset = args["dataset"]
	imagePaths = list(paths.list_images(dataset))

	for img in imagePaths:
		print img

	return imagePaths

def createEncodings(imageFiles):
	print "Creating Encoding data..."

	known_encodings = []
	known_names = []

	for img_file in imageFiles:
		print ("[INFO] encoding image: {}".format(img_file))

		img = face_recognition.load_image_file(img_file)
		boxes = face_recognition.face_locations(img,model=args["detection_method"])

		name = img_file.split(os.path.sep)[-2]

		encoding_img = face_recognition.face_encodings(img,boxes)

		if len(encoding_img) > 0:
			known_encodings.append(encoding_img[0])
			known_names.append(name)
		else:
			continue

	print "Encoding data is done !"

	return known_encodings,known_names

def writeEncodingDataToFile(known_encodings,known_names):
	print "Saving encoding file ..."

	data = {"encodings": known_encodings,"names": known_names}

	f = open(args["output_encodings"],"wb")

	f.write(pickle.dumps(data))

	f.close()

	print "Saving is finished !"


def main():
	imgFiles = listImageFile()
	known_encodings,known_names = createEncodings(imgFiles)
	writeEncodingDataToFile(known_encodings,known_names)

main()