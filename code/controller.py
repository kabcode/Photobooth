#!/usr/bin/env python3
# created by kabcode@gmail.com
# information and further details can be found under www.kabelitzens.de

"""
This module offers the interface for potential controller classes 
"""

# imports
import abc

class ControllerInterface(abc.ABC):
	
	# establish connection to controller
	@abc.abstractmethod
	def connect(self):
		pass
		
	# close connection to wiimote
	@abc.abstractmethod
	def disconnect(self):
		pass
		
		
	# get action defined by controller state
	@abc.abstractmethod
	def get_action(self):
		pass
		
	# check for state of controller
	@abc.abstractmethod
	def is_active(self):
		pass
	
		
