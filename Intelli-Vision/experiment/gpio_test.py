# from gpiozero import LED, Button
# from signal import pause

# button = Button(2)
# led = LED(17)

# if button.when_pressed:
#     print("button is pressed")
# button.when_pressed = led.on
# button.when_released = led.off

# pause()

import RPi.GPIO as GPIO
import time

led_on = False
count = 0

def setupGPIO():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    GPIO.setup(18, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(23, GPIO.IN, pull_up_down = GPIO.PUD_UP)

def flashLED(count):
    for i in range(count):
        GPIO.output(18,GPIO.HIGH)
        time.sleep(.2)
        GPIO.output(18,GPIO.LOW)
        time.sleep(.2)

def switch(ev=None):
    global led_on, count
    led_on = not led_on
    count += 1

    if led_on == True:
        print("Turning on\tCount: " + str(count))
        GPIO.output(18,GPIO.HIGH)
    else:
        print("Turning off\tCount: " + str(count))
        GPIO.output(18, GPIO.LOW)

def detectButtonPress():
    GPIO.add_event_detect(23,GPIO.FALLING, callback=switch, bouncetime=300)

def waitForEvents():
    while True:
        time.sleep(1)

setupGPIO()
flashLED(5)
detectButtonPress()
waitForEvents()