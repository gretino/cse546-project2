from picamera import PiCamera
from time import sleep
import datetime as dt
import os
import boto3
from dotenv import load_dotenv
load_dotenv()

s3 = boto3.client('s3')
def camera_record():
	camera = PiCamera()
	filename = dt.datetime.now().strftime("%Y-%m-%d_%H.%M.%S.h264")
	filepath = f'/home/pi/Desktop/{filename}'
	camera.start_preview()
	camera.start_recording(filepath)
	sleep(0.5)
	camera.stop_recording()
	camera.stop_preview()
    camera.close()
	s3.upload_file(filepath,'input-project2',filename)

while True:
	camera_record()





