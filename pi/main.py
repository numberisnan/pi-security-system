# Libraries
import RPi.GPIO as GPIO
import time
import json
import requests
import shutil

with open("./o.json", "r+") as file:
	o = json.loads(file.read())
with open("./data.json", "r+") as file:
	data = json.loads(file.read())


def getIntruderInfo():
	cameraip = o["cameraip"]
	# get image
	timestamp = time.time()
	image_url = "http://" + cameraip + "/index.jpg"
	filename = "./photos/" + str(int(timestamp)) + ".jpg"
	r = requests.get(image_url, stream=True)
	if r.status_code == 200:
		print("Image recieved")
		r.raw.decode_content = True
		with open(filename,'wb') as f:
			shutil.copyfileobj(r.raw, f)
		data["events"].append({"imageFile": filename, "timestamp": int(timestamp) })
		with open("./data.json", "w+") as file:
			file.write(json.dumps(data))
		print("Incident Saved")
	else:
		print("Could not get image")

GPIO.setmode(GPIO.BCM)

GPIO_TRIGGER = 18
GPIO_ECHO = 24
BUZZER_PIN = 25

GPIO.setup(BUZZER_PIN, GPIO.OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

def distance():
	# set Trigger to HIGH
	GPIO.output(GPIO_TRIGGER, True)

	# set Trigger after 0.01ms to LOW
	time.sleep(0.00001)
	GPIO.output(GPIO_TRIGGER, False)

	StartTime = time.time()
	StopTime = time.time()

	# save StartTime
	while GPIO.input(GPIO_ECHO) == 0:
			StartTime = time.time()

	# save time of arrival
	while GPIO.input(GPIO_ECHO) == 1:
			StopTime = time.time()

	# time difference between start and arrival
	TimeElapsed = StopTime - StartTime
	# multiply with the sonic speed (34300 cm/s)
	# and divide by 2, because there and back
	distance = (TimeElapsed * 34300) / 2

	return distance

try:
	while True:
		dist = distance()
		if dist < 30:
			print("Intruder Detected")
			getIntruderInfo()
			GPIO.output(BUZZER_PIN, True)
			time.sleep(2)
			GPIO.output(BUZZER_PIN, False)
	# Reset by pressing CTRL + C
except KeyboardInterrupt:
	print("Measurement stopped by User")
	GPIO.cleanup()
