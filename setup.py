import os

def install_dlib():
	os.system("sudo pip install scipy")

	os.system("sudo pip install scikit-image")

	os.system("sudo pip install dlib")

def install_cv2():
	os.system("sudo pip install opencv-python")

def install_imutils():

	os.system("sudo pip install imutils")

def install_packages():
	install_dlib()
	install_cv2()
	install_imutils()

	print "Ready to use face_recognition_testing.py. Use the command 'python face_recognition_testing.py --help' to see the parameters"

install_packages()
