from picamera import PiCamera
from time import sleep
import datetime as dt
import os
from dotenv import load_dotenv

load_dotenv()


def camera_record():
    camera = PiCamera()
    camera.resolution = (160, 160)
    filename = dt.datetime.now().strftime("%Y-%m-%d_%H.%M.%S.%f.h264")
    filepath = f'/home/pi/Desktop/temp/{filename}'
    camera.start_preview()
    sleep(3)
    camera.capture(filepath)
    camera.stop_preview()
    camera.close()
    os.system(f'python eval_face_recognition.py --img_path "{filepath}"')


while True:
    camera_record()
