#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2017-18 Richard Hull and contributors
# See LICENSE.rst for details.
# PYTHON_ARGCOMPLETE_OK

"""
Display a video clip.

Make sure to install the av system packages:

  $ sudo apt-get install -y libavformat-dev libavcodec-dev libavdevice-dev libavutil-dev libswscale-dev libavresample-dev libavfilter-dev

And the pyav package (might take a while):

  $ sudo -H pip install av
"""

import sys
import os.path
from demo_opts import get_device
import time, threading
import signal

import PIL

try:
    import av
except ImportError:
    print("The pyav library could not be found. Install it using 'sudo -H pip install av'.")
    sys.exit()

frames = 0
last_frames = 0
display_on = True
fps_timer = None

def fps():
    global frames, last_frames, display_on, fps_timer
    print(f"FPS: [{frames-last_frames}]", end='\r')
    sys.stdout.flush()
    last_frames = frames
    fps_timer = threading.Timer(1, fps)
    fps_timer.start()

def display_loop():
    global display_on, device, fps_timer

    device = get_device()
    device.persist = True

    fps_timer = threading.Timer(1, fps)
    fps_timer.start()

    img_i = 1

    while True and display_on:
        global frames
        frames = frames + 1

        img = PIL.Image.open('/home/pi/img/output{:06d}.png'.format(img_i))

        img_i = img_i + 1
        if img_i > 600:
            img_i = 1

#        print(img.width, img.height, device.width, device.height,
#                img.width != device.width, img.height != device.height)
#        from time import perf_counter
#        t1_start = perf_counter()
        if img.width != device.width or img.height != device.height:
            # resize video to fit device
            size = device.width, device.height
            img = img.resize(size, PIL.Image.ANTIALIAS)
#        t1_stop = perf_counter()
#        print("T:", t1_stop-t1_start)
            print("A:", img.width, img.height, device.width, device.height)

        device.display(img)
    device.cleanup()
    if fps_timer:
        fps_timer.cancel()

def receiveSignal(signalNumber, frame):
    global display_on, device
    print('Received:', signalNumber)
    if not display_on:
        threading.Thread(target=display_loop).start()
        display_on = True
    else:
        display_on = False
    return

if __name__ == "__main__":
    try:
        signal.signal(signal.SIGUSR1, receiveSignal)
        threading.Thread(target=display_loop).start()
        # loop forever
        while True:
            time.sleep(3600)
    except KeyboardInterrupt:
        pass
