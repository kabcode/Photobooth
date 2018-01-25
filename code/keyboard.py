#!/usr/bin/env python3
# created by kabcode@gmail.com
# information and further details can be found under www.kabelitzens.de

"""
The keyboard is the default controller when no other controller is 
available. The on_press function translates the keyboard input to 
actions for the core module.
"""

# libraries import
import time
import controller
from pynput import keyboard

class KeyboardAdapter(controller.ControllerInterface):
	
	# setup controller abilities
	def __init__(self):
		# set the current action according to pressed key
		def on_press(key):
			if key == keyboard.Key.space:
				self.current_action = "PHOTO"

			if key == keyboard.Key.esc:
				self.current_action = "EXIT"
		
		self.listener = keyboard.Listener(on_press=on_press)
		self.current_action = []
		self.connect()

	# stop keyboard listener
	def disconnect(self):
		self.listener.stop()
		
	# get current state of keyboard controller
	def is_active(self):
			return self.listener.running()
				
	# get action defined by button state, after returnig an action reset
	def get_action(self):
		return_action = self.current_action
		self.current_action	= []
		return return_action
	
	# establish starts thread that listen to keyboard	
	def connect(self):
		self.listener.start()
		
		
		
