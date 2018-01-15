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
import wiimote  as wm
import picamera as picam
import time

class Photobooth:
	
	# at initialization of photobooth
	def __init__(self):
		self.controller = []
		self.run_setup()
		
	def run_setup(self):
		print("Run setup")
		
		# get current photobooth folder
		current_folder = Path.cwd().parent
		print(current_folder)
		
		# load default language
		global lang
		lang = lg.LanguageAdapter(current_folder)
		
		# initialize controller
		self.controller = wm.WiimoteAdapter()
		
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
				
		
		
		
