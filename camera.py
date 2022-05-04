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
    new_name = dt.datetime.now().strftime("%Y-%m-%d_%H.%M.%S.%f.h264")
    new_path = f'/home/pi/Desktop/{new_name}'
    os.rename(local_file, new_path)
    s3.upload_file(new_path, bucket, new_name)
    sleep(1.5)
    os.remove(new_path)


def camera_record():
    camera = PiCamera()
    camera.resolution = (160, 160)
    filename = dt.datetime.now().strftime("%Y-%m-%d_%H.%M.%S.%f.h264")
    filepath = f'/home/pi/Desktop/{filename}'
    camera.start_preview()
    camera.start_recording(filepath)
    sleep(0.3)
    camera.stop_recording()
    camera.stop_preview()
    camera.close()
    threading.Thread(target=upload_to_aws, args=(filepath, 'ccproject-2', filename)).start()


while True:
    camera_record()
