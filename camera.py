from picamera import PiCamera
from time import sleep
import datetime as dt
import os
import boto3
from dotenv import load_dotenv
import threading
load_dotenv()

s3 = boto3.client('s3')

def upload_to_aws(local_file, bucket, s3_file):
	s3.upload_file(local_file,bucket,s3_file)
	sleep(1.5)
	os.remove(local_file)

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
	threading.Thread(target = upload_to_aws, args=(filepath,'input-project2',filename)).start()

	
while True:
	camera_record()
