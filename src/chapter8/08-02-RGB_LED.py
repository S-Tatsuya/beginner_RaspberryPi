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

GPIO.setmode(GPIO.BCM)
SPICLK = 11
SPIMOSI = 10
SPIMISO = 9
SPICS = 8

GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICS, GPIO.OUT)

G_LED_GPIO = 25
B_LED_GPIO = 24
R_LED_GPIO = 23
GPIO.setup(G_LED_GPIO, GPIO.OUT)
GPIO.setup(B_LED_GPIO, GPIO.OUT)
GPIO.setup(R_LED_GPIO, GPIO.OUT)
pg = GPIO.PWM(G_LED_GPIO, 50)
pb = GPIO.PWM(B_LED_GPIO, 50)
pr = GPIO.PWM(R_LED_GPIO, 50)
pg.start(0)
pb.start(0)
pr.start(0)
adc_ping = 0
adc_pinb = 1
adc_pinr = 2

try:
	while True:
		inputValg = readadc(adc_ping, SPICLK, SPIMOSI, SPIMISO, SPICS)
		inputValb = readadc(adc_pinb, SPICLK, SPIMOSI, SPIMISO, SPICS)
		inputValr = readadc(adc_pinr, SPICLK, SPIMOSI, SPIMISO, SPICS)
		dutyg = inputValg * 100 / 4095
		dutyb = inputValb * 100 / 4095
		dutyr = inputValr * 100 / 4095
		pg.ChangeDutyCycle(dutyg)
		pb.ChangeDutyCycle(dutyb)
		pr.ChangeDutyCycle(dutyr)
		sleep(0.2)

except KeyboardInterrupt:
	pass

pg.stop()
pb.stop()
pr.stop()
GPIO.cleanup()
