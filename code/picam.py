#!/usr/bin/env python3
# created by kabcode@gmail.com
# information and further details can be found under www.kabelitzens.de

"""
This module wraps the Picamera lib based on the interface class for
photobooth cameras. For further processing and saving the images are 
returned as Python Imaging Library (PIL) object.
Some methods seem to be senseless because there are already implemented 
in the PiCamera library. Its for consistency with the CameraInterface.
"""

# libraries import
import camera
import picamera as pc
import picamera.array
from time import sleep
from PIL import Image


class PicameraAdapter(camera.CameraInterface):
	
	def __init__(self):
		self.camera = pc.PiCamera()
		self.camera.resolution = (1920, 1080)

	# take a picture and turn it into a PIL image
	def take_photo(self):
		self.give_feedback("take_photo")
		capture = pc.array.PiRGBArray(self.camera)
		self.activate_preview()
		sleep(2)
		self.camera.capture(capture, format='bgr')
		self.deactivate_preview()
		return capture.array
	
	# activate the preview for 
	def activate_preview(self):
		self.give_feedback("activate_preview")
		try:
			self.camera.start_preview(alpha=255,fullscreen=False, window=(0,0,200,200))
		except all:
			print("Problem!")
	
	# deactivate preview
	def deactivate_preview(self):
		self.give_feedback("deactivate_preview")
		self.camera.stop_preview()
		
	# gives feedback for debuging
	def give_feedback(self, msg):
		print("FEEDBACK: " + msg)
		
		
	
