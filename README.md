# Face-Recognition

![alt text](https://raw.githubusercontent.com/bquangDinh/Face-Detection/master/output.jpg)

In this week, I haved built some python script using face_recognition library to recognize my friends. I put it here for anyone want to contribute this bullshit project :D.

You can found the face_recognition library [here](https://github.com/ageitgey/face_recognition). By the way, thanks for someone had built this library. It's very powerful :D.

## Installation
### 1.Install virtual workspace
Using these commands to install virtualenv workspace. The virtual workspace is the environment for dlib library.

```bash
sudo pip install virtualenv
mkdir ~/.virtualenv
sudo pip install virtualenvwrapper
export WORKON_HOME=~/.virtualenvs
. /usr/local/bin/virtualenvwrapper.sh
```
After installed. Use this command to create a new virtualenv

```bash
mkvirtualenv <workspace name>
```
To access and switch between environments. Using workon.

```bash
workon <project name>
```
Make sure you had the environment to jump into before.

For more details for installing virtualenv [here](
https://medium.com/@aaditya.chhabra/virtualenv-with-virtualenvwrapper-on-ubuntu-34850ab9e765)


### 2.Install some needing packages

There are some packages you need install them before. To make it easily. I made a simple script to install all of them just use one line. Make sure you had jumped into the your virtualev workspace and in the my git project folder. Run file setup.py to install needing packages.

```bash
python setup.py
```

If something gone wrong while installing. You can open my setup.py file and look thourgh because it's very simple and you can install those packages by yourselves.

After that, so everthing done. Enjoy :D

## Guideline

First thing you need to do is building your faces database. 
Your structure database should be like this:

* FaceDataFolder/
  * NameOfPerson1
      * Image1.jpg
      * Image2.jpg
      * ... (so on)
  * NameOfPerson2/
      * Image1.jpg
      * Image2.jpg
      * ... (so on)
  
 

Next thing is build your encoding file which is extracted from your database. It's very necessary to do a lot of things.

There are two ways to do that and it's very simple

If you want to use image to recognition. You can run face_recognition_image.py and it will build your encoding file and recognize your input image in one time. Here is some parameters of this file

The second way to build your encoding file is using face_encodings.py file instead.

```bash
-dt/--dataset (required) : path to input face dataset
-o/--output_encodings (required) : encodings file name for saving
-de/--detection_method : Choose between 'cnn' or 'hog'. The default setting is cnn
```
Example:

```bash
python face_encodings.py --dataset="FaceData" --output_encodings="encodings.db" --detection_method="hog"
```

You will need this file if you want to work with video

There are parameters of face_recognition_image.py file:

```bash
-e/--encoding_dataset : Path to input dataset
-i/--input_image (required) : The input image to recognize
-o/--output_image (required) : The output image to save
-de/--detection_method (default: cnn) : You can choose between 'cnn' or 'hog'. Use cnn give you more accuracy than hog but slower than hog. Make sure you have a strongly computer to do that if you don't want to wait a long time.
-ef/--encoding_file : Path to save encoding data.
-s/--save_encoding_file: If you choose --encoding_file, you have to tell the program where it should be saved.
```
Example:

This example will build your database, save encoding data to file and return a output image:

```bash
python face_recognition_image.py --encoding_dataset="FaceData" --input_image="input.jpg" --output_image="output.jpg" --detection_method="hog" --save_encoding_file
```

The next example will reuse your encoding file that you saved before:

```bash
python face_recognition_image.py --encoding_file="encoding.db" --input_image="input.jpg" --output_image="output.jpg" 
```

Notice the above example will detect faces in the image by cnn. That is the default setting.

### Video

If you want to play with video. You can you either face_recognition_video.py or face_recognition_image.py. If you run face_recognition_video.py file, then you need build the encoding file first. There are parameters in this file:

```bash
-e/--encoding_dataset : Path to input dataset
-i/--input_video : The input video to recognize
-wc/--webcam_index : You can use your webcam. webcam index is the index of the camera that you want to use in case you using many camera. By default it is 0
-d/--detection_method (default: cnn)(required) : You can choose between 'cnn' or 'hog'. Use cnn give you more accuracy than hog but slower than hog. Make sure you have a strongly computer to do that if you don't want to wait a long time. I suggest you run hog instead, cnn option will take a very long time to compute so it can lead to crash.
-ef/--encoding_file : Path to your encoding file.
```
Example:

This below example will take a video and process

```bash
python face_recognition_video.py --input_video="video.avi" --detection_method="hog" --encoding_file="encodings.db"
```

This below example will use your webcam

```bash
python face_recognition_video.py --webcam_index=0 --detection_method="hog" --encoding_file="encodings.db"
```

There are some options in my code that you can change by your mind. Open face_recognition_video.py file and just change it's value

```bash
RECTANGLE_COLOR = (0,255,0)
RECTANGLE_WEIGHT = 2

FONT_TYPE = cv2.FONT_HERSHEY_SIMPLEX
FONT_SIZE = 0.75
FONT_COLOR = (255,0,255)
FONT_WEIGHT = 2
```

## Use for your program
If you want to use recognized face data. You can reuse my code. Make sure you haved the encodings file and face_recognition_image.py in your project folder.

Example: 

```bash
from face_recognition_image import processingFaceData,loadEncodings

encoding_file = "encodings.db"

known_encodings,known_names = loadEncodings(encoding_file)

face_locations,names = processingFaceData(yourimage,known_encodings,names)

# with once face location corresponding to the name of the face

#example

for face_location,name in zip(face_locations,names):
 (top,right,bottom,left) = face_location
 
 #Draw a rectangle with top right bottom and left coordinates

```

In this program, it have no option to save output video because the output video can really bad quality. I don't know why but in this time I don't make it. This project just is a practice :D So try your best, change my code and you can make it :D

