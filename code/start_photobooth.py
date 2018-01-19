#!/usr/bin/env python3
# created by kabcode@gmail.com
# information and further details can be found under www.kabelitzens.de

"""
This python script is the entry point for the photobooth
"""
# import libs
import core
import picam as pc
import time

if __name__ == '__main__':
	
	
	#booth = core.Photobooth()
	#booth.start()

	cam = pc.PicameraAdapter()
	cam.activate_preview()
	time.sleep(5)
	cam.deactivate_preview()
	
	cam.take_picture()
