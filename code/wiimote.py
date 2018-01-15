#!/usr/bin/env python3
# created by kabcode@gmail.com
# information and further details can be found under www.kabelitzens.de

"""
This module wraps the cwiid lib for more convenient handling of
the wiiremote  
"""

# imports
import cwiid
import time

class WiimoteAdapter:
	
	def __init__(self):
		self.wiimote = self.connect()
		
	# establish bluetooth connection to wiimote	
	def connect(self):
		try:
			print("Connecting...")
			wii = cwiid.Wiimote()
		except:
			print("Error - No wiimote found.")
			return None

		wii.rumble = 1
		time.sleep(1)
		wii.rumble = 0
		print ("Wiimote connected.")
		# set wiimote in button mode
		wii.rpt_mode = cwiid.RPT_BTN    
		return wii
		
	# close connection to wiimote
	def disconnect(self):
		for i in range(2):
			self.wiimote.rumble = 1
			time.sleep(0.5)
			self.wiimote.rumble = 0
			time.sleep(0.5)
		self.wiimote.close()
		
		
	# get action defined by button state
	def get_action(self):
		
		buttons = self.wiimote.state['buttons']
		
		# if "A" button is pressed: print "ACTION"
		if(buttons & cwiid.BTN_A):
			return "ACTION"
			
		# if "+" and "-" are pressed: shutdoen photobooth
		if (buttons - cwiid.BTN_PLUS - cwiid.BTN_MINUS == 0):
			return "EXIT"
	
		
