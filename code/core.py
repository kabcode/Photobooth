#!/usr/bin/env python3
# created by kabcode@gmail.com
# information and further details can be found under www.kabelitzens.de

"""
This is the core component of the photobooth. It makes use of all modules
and has the logic build in. 
"""

# libraries that are always needed
from pathlib import Path
import language as lg
import time

# imports for own controller and camera module
import wiimote  as wm
import picam as pc

class Photobooth:
	
	# at initialization of photobooth
	def __init__(self):
		self.controller = []
		self.image_folder= []
		self.current_folder = []
		self.run_setup()
		
	def run_setup(self):
		print("Run setup")
		
		# get current photobooth folder
		self.current_folder = Path.cwd().parent
		self.image_folder = self.setup_image_folder()
		print(self.image_folder)
		
		# load default language
		global lang
		lang = lg.LanguageAdapter(self.current_folder)
		
		# initialize controller
		self.controller = wm.WiimoteAdapter()
		if self.controller is None:
			print("Error - No controller")
			
		# initialize camera
		self.camera = pc.PicameraAdapter()
				
	# create a folder for the taken images
	# the folder has the current date as name
	def setup_image_folder(self):
		image_folder = self.current_folder.parent.joinpath(time.strftime('%Y%m%d'))
		if image_folder.exists():
			pass
		else:
			image_folder.mkdir()
		return image_folder
		
	# save photo in image folder
	def save_photo(self, photo):
		pass
		
	# take a photo as PIL object with the connected camera
	def take_photo(self):
		photo = self.camera.take_picture()
		save_photo(photo)
				
	# start photobooth main function
	def start(self):
		i = 0
		while True:
			
			time.sleep(0.08) # avoid endless test texts by pressing a button
			
			# get the action from controller
			action = self.controller.get_action()
		
			if action == "EXIT":
				self.controller.disconnect()
				break
				
			if action == "PHOTO":
				self.take_photo()
				pass
		
		
		
