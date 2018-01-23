#!/usr/bin/env python3
# created by kabcode@gmail.com
# information and further details can be found under www.kabelitzens.de

"""
This module offers the interface for potential camera classes 
"""

# imports
import abc


class CameraInterface(abc.ABC):
	
	@abc.abstractmethod
	def take_photo(self):
		pass
		
	@abc.abstractmethod
	def activate_preview(self):
		pass
		
	@abc.abstractmethod
	def deactivate_preview(self):
		pass
		
	@abc.abstractmethod
	def give_feedback(msg,self):
		pass
