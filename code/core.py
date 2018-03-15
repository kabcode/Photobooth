#!/usr/bin/env python3
# created by kabcode@gmail.com
# information and further details can be found under www.kabelitzens.de

"""
This is the core component of the photobooth. It makes use of all modules
and has the logic build in. 
"""

# libraries that needed but not custom
import time
from  PyQt5.QtCore import (QObject, pyqtSlot)

# libraries that are always needed
import language as lg
import filehandler as fh

# imports for own controller and camera module
import wiimote  as wm
import keyboard as kb
import picam as pcm
import network as nw

class Photobooth(QObject):
	
	# at initialization of photobooth
	def __init__(self, parent=None):
		super().__init__(parent)
		self.controller = []
		self.file_handler = []
		self.userinterface = [] 
		self.run_setup()
		
	def run_setup(self):
		print("Run setup")
		
		# file handler takes care of the taken images
		self.file_handler = fh.FileHandler()
		
		# load default language
		global lang
		lang = lg.LanguageAdapter(self.file_handler.current_folder)
		
		# initialize controller (default is keyboard)
		self.controller = wm.WiimoteAdapter()
		if not self.controller.is_active():
			self.controller = kb.KeyboardAdapter()
			print("Set keyboard as default controller")
			
		# initialize camera
		self.camera = pcm.PicameraAdapter()
		print("Setup done.")
		
		# initialize a network connection
		self.network = nw.NetworkAdapter()
		
				
		
	# take a photo as OpenCV object with the connected camera
	def take_photo(self):
		print("take picture")
		photo = self.camera.take_photo()
		# if you need to do fancy stuff with the photo do it here!!
		# photo = self.do_fancy_stuff(photo)
		self.file_handler.save_photo(photo)
		
	@pyqtSlot()
	def started(self):
		print("Running...")
				
	# start photobooth main function
	@pyqtSlot()
	def start(self):
		print("Booth started.")
		i = 0
		while True:
			
			time.sleep(0.1) # avoid endless test texts by pressing a button
			
			# get the action from controller
			action = self.controller.get_action()
		
			if action == "EXIT":
				self.controller.disconnect()
				break
				
			if action == "PHOTO":
				self.take_photo()
				pass
				
			if action == "ERROR":
				break
				
			
		
		
		
