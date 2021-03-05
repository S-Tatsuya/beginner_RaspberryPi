import RPi.GPIO as GPIO
from time import sleep
import subprocess

def my_callback(channel):
	global isPlaying
	global process
	if channel == 27:
		if isPlaying == False:
			isPlaying = True
			GPIO.output(25, GPIO.HIGH)
			args = ['mplayer', '-ao', 'alsa:device=hw=1,0', 'test.mp3']
			process = subprocess.Popen(args)
			# print("start")
		else:
			isPlaying = False
			GPIO.output(25,GPIO.LOW)
			args = ['kill', str(process.pid)]
			subprocess.Popen(args)
			# print("end")

GPIO.setmode(GPIO.BCM)
GPIO.setup(25, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(27, GPIO.RISING, callback=my_callback, bouncetime=200)

isPlaying = False
process = None

try:
	while True:
		# print(isPlaying)
		sleep(0.01)

except KeyboardInterrupt:
	pass

GPIO.cleanup()
