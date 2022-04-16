from picamera import PiCamera
from time import sleep
import datetime as dt
import boto3


def upload_to_aws_s3(local_file, bucket, s3_file):
    s3 = boto3.client('s3')
    s3.upload_file('D:/cc2images/image.png','input-project2','filename')

def camera_record():
	camera = PiCamera()
	filename = dt.datetime.now().strftime("%Y-%m-%d_%H.%M.%S.h264")
	camera.start_preview()
	camera.start_recording('/home/pi/Desktop/filename')
	sleep(0.5)
	camera.stop_recording()
	camera.stop_preview()

	s3_upload.upload_to_aws_s3('/home/pi/Desktop/filename','input-project2','filename')

while true:
	camera_record()





