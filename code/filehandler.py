#!/usr/bin/env python3
# created by kabcode@gmail.com
# information and further details can be found under www.kabelitzens.de

"""
This module takes care of the files. Especially the storage of images. 
The default is to save images to the SD-Card without any changes. With
the advanced features more processing can be done and the images can be
to an online drive. At the moment the implementation is for sd card and
Microsoft OneDrive.
"""

# libraries import
from pathlib import Path
import network as nw
import cv2
import time

class FileHandler():
	
	# constuctor
	def __init__(self):
		self.storage_handler = [self.add_storage_location('sd')]
		
	# storing images by set handlers
	def save_photo(self, photo):
		for location in self.storage_handler:
			location.save_photo(photo)
				
	# add storage location for photos
	def add_storage_location(self, method):
		if method not in self.storage_methods:
			self.storage_methods.append(method)
			if method is 'onedrive':
				self.storage_handler.append(OneDriveFileHandler())
	
	# remove storage location
	def remove_storage_location(self, method):
		pass	
		
		

import abc
class GenericFileHandler(abc.ABC):
	
	# setup filehandler
	@abc.abstractmethod
	def setup_storage_location(self):
		pass
		
	# save photo
	def save_photo(self):
		pass
		
	# remove storage location
	def remove_storage_location(self):
		pass
	

class SDFileHandler(GenericFileHandler):
	
	def __init__(self):
		self.storage_location = setup_storage_location()
	
	# create a folder for the taken images
	# the folder has the current date as name
	def setup_storage_location(self):
		current_folder = Path.cwd().parent
		image_folder = self.current_folder.parent.joinpath(time.strftime('%Y%m%d'))
		if image_folder.exists():
			pass
		else:
			image_folder.mkdir()
		return image_folder
		
	# save photo to sd card
	def save_photo(self,photo)
	image_name = (self.storage_location).joinpath(time.strftime('%H%M%S'))
	cv2.imwrite(str(image_name)+ ".jpeg", photo)
	
	def remove_storage_location(self):
		pass
		
	
class OneDriveFileHandler(GenericFileHandler):
	
		# constructor
		def __init__(self):
			
			
		def setup_storage_location(self):
			pass
			
		def remove_storage_location(self):
			pass
			
			
			
		
# for testing this module
if __name__ == '__main__':
	
	fh = FileHandler()
	print(fh.storage_handler)
	print(fh.storage_methods)
	fh.add_storage_location('onedrive')
	print(fh.storage_handler)
	print(fh.storage_methods)
