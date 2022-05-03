from picamera import PiCamera
from time import sleep
import datetime as dt

def camera_record():
	camera = PiCamera()
	camera.resolution = (160, 160)
	filename = dt.datetime.now().strftime("%Y-%m-%d_%H.%M.%S.jpg")
	filepath = f'/home/pi/Desktop/{filename}'
	camera.start_preview()
	sleep(2)
	camera.capture(filepath)
	camera.stop_preview()
	camera.close()

while True:
	x=input()
	if (x == ''):
		camera_record()
	else: 
		break
