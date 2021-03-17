# -*- coding:utf-8 -*-
import RPi.GPIO as GPIO
from time import sleep

def readadc(adcnum, clockpin, mosipin, misopin, cspin):
	if adcnum > 7 or adcnum < 0:
		return -1

	GPIO.output(cspin, GPIO.HIGH)
	GPIO.output(clockpin, GPIO.LOW)
	GPIO.output(cspin, GPIO.LOW)

	commandout = adcnum
	commandout |= 0x18
	commandout <<= 3
	for i in range(5):
		if commandout & 0x80:
			GPIO.output(mosipin, GPIO.HIGH)
		else:
			GPIO.output(mosipin, GPIO.LOW)

		commandout <<= 1
		GPIO.output(clockpin, GPIO.HIGH)
		GPIO.output(clockpin, GPIO.LOW)

	adcout = 0

	for i in range(13):
		GPIO.output(clockpin, GPIO.HIGH)
		GPIO.output(clockpin, GPIO.LOW)
		adcout <<= 1
		if i > 0 and GPIO.input(misopin) == GPIO.HIGH:
			adcout |= 0x1
	GPIO.output(cspin, GPIO.HIGH)
	return adcout


def servo_duty_hwpwm(val):
	val_min = 0
	val_max = 4095
	servo_min = 3.5	# 最小デューティー比3.5%を10000倍して格納
	servo_max = 10	# 最大デューティー比10%を10000倍して格納
	duty = int((servo_min - servo_max) * (val - val_min) / (val_max - val_min) + servo_max)
	# 参考
	# duty = int((servo_max - servo_min) * (val - val_min) / (val_max - val_min) + servo_min)
	return duty

GPIO.setmode(GPIO.BCM)
SPICLK = 11
SPIMOSI = 10
SPIMISO = 9
SPICS = 8

GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICS, GPIO.OUT)

GPIO.setup(25, GPIO.OUT)
p = GPIO.PWM(25, 50)
p.start(0)
adc_pin0 = 0

try:
	while True:
		inputVal0 = readadc(adc_pin0, SPICLK, SPIMOSI, SPIMISO, SPICS)
		duty = servo_duty_hwpwm(inputVal0)
		print(duty)
		p.ChangeDutyCycle(duty)
		sleep(0.2)

except KeyboardInterrupt:
	pass

p.stop()
GPIO.cleanup()
