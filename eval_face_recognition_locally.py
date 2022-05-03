from picamera import PiCamera
from time import sleep
import datetime as dt
import os
from dotenv import load_dotenv
import subprocess

load_dotenv()

folder_path = f'/home/pi/Desktop/temp/'
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

def camera_record():
    camera = PiCamera()
    camera.resolution = (160, 160)
    filename = dt.datetime.now().strftime("%Y-%m-%d_%H.%M.%S.%f.jpg")
    filepath = f'/home/pi/Desktop/temp/{filename}'
    camera.start_preview()
    sleep(3)
    camera.capture(filepath)
    camera.stop_preview()
    camera.close()
    command = f'python eval_face_recognition.py --img_path "{filepath}"'
    print(subprocess.check_output(command, shell=True))


while True:
    camera_record()
