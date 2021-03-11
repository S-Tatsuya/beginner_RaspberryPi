# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
from time import sleep

def readadc(adcnum, clockpin, mosipin, misopin, cspin):
	if adcnum > 7 or adcnum < 0:
		return -1

	GPIO.output(cspin, GPIO.HIGH)
	GPIO.output(clockpin, GPIO.LOW)
	GPIO.output(cspin, GPIO.LOW)

	commandout = adcnum
	commandout |=0x18
	commandout <<= 3
	for i in range(5):
		# LSBから数えて8ビット目から4ビット目までを送信
		if commandout & 0x80:
			GPIO.output(mosipin, GPIO.HIGH)
		else:
			GPIO.output(mosipin, GPIO.LOW)
		commandout <<= 1
		GPIO.output(clockpin, GPIO.HIGH)
		GPIO.output(clockpin, GPIO.LOW)
	adcout = 0
	# 13ビット読む
	for i in range(13):
		GPIO.output(clockpin, GPIO.HIGH)
		GPIO.output(clockpin, GPIO.LOW)
		adcout <<= 1
		if i > 0 and GPIO.input(misopin) == GPIO.HIGH:
			adcout |= 0x1
	GPIO.output(cspin, GPIO.HIGH)
	return adcout

def led_on():
	GPIO.output(LED, GPIO.HIGH)

def led_off():
	GPIO.output(LED, GPIO.LOW)

def judge_led_lighting(lightness):
	if 2000 >= lightness:
		led_on()
	else:
		led_off()

GPIO.setmode(GPIO.BCM)
# ピンの尾名前を変数として定義
SPICLK = 11
SPIMOSI = 10
SPIMISO = 9
SPICS = 8
# SPI通信用の入出力を定義
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICS, GPIO.OUT)

LED = 25
GPIO.setup(LED, GPIO.OUT)

try:
	while True:
		inputVal0 = readadc(0, SPICLK, SPIMOSI, SPIMISO, SPICS)
		judge_led_lighting(inputVal0)
		print(inputVal0)
		sleep(0.2)

except KeyboardInterrupt:
	pass

GPIO.cleanup()
