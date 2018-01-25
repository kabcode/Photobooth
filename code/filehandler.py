#!/usr/bin/env python3
# created by kabcode@gmail.com
# information and further details can be found under www.kabelitzens.de

"""
This module takes care of the files. Especially the storage of images. 
The default is to save images to the SD-Card without any changes. With
the advanced features more processing can be done and the images can be
to an online drive.
"""

# libraries import
from pathlib import Path
import cv2
import time

class FileHandler():
	
	# constuctor
	def __init__(self):
		self.current_folder = Path.cwd().parent
		self.image_folder = self.setup_image_folder()
		self.storage_methods = ['default']
		print("Imagefolder: " + str(self.image_folder))
		
	# create a folder for the taken images
	# the folder has the current date as name
	def setup_image_folder(self):
		image_folder = self.current_folder.parent.joinpath(time.strftime('%Y%m%d'))
		if image_folder.exists():
			pass
		else:
			image_folder.mkdir()
		return image_folder
		
		
	# storing images by set methods
	def save_photo(self, photo):
		for method in self.storage_methods:
			if method == 'default':
				self.save_to_sd(photo)
				
				
	# storing to sd card by generating saving path
	def save_to_sd(self, photo):
		image_name = (self.image_folder).joinpath(time.strftime('%H%M%S'))
		print(image_name)
		cv2.imwrite(str(image_name)+ ".jpeg", photo)
		
		
		

