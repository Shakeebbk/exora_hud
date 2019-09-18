import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import time
import os

GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering

IN_PIN = 13
toggle = 1
def button_callback(channel):
    global toggle, IN_PIN

    if GPIO.input(IN_PIN) == 0:
        time.sleep(0.5)
        if GPIO.input(IN_PIN) == 0:
            if toggle:
                toggle = 0
            else:
                toggle = 1
            os.system('~/exora_hud/run_exora_toggle.sh')
            print(f"Button pressed {toggle}", end='\r')

GPIO.setup(IN_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Set pin 10 to be an input pin and set initial value to be pulled low (off)

GPIO.add_event_detect(IN_PIN,GPIO.FALLING,callback=button_callback) # Setup event on pin 10 rising edge

import signal
signal.pause()

GPIO.cleanup()
