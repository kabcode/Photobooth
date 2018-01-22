#!/usr/bin/env python3
# created by kabcode@gmail.com
# information and further details can be found under www.kabelitzens.de

"""
This module takes care of the files. Especially the storage of images. 
The default is to save images to the SD-Card without any changes. With
the adveanced features more processing can be done and the images can be
to an online drive.
"""

# libraries import
from pathlib import Path
import time

class FileHandler():
	
	# constuctor
	def __init__(self):
		self.current_folder = Path.cwd().parent
		self.image_folder = self.setup_image_folder()
		print(self.current_folder)
		print(self.image_folder)
		
	# create a folder for the taken images
	# the folder has the current date as name
	def setup_image_folder(self):
		image_folder = self.current_folder.parent.joinpath(time.strftime('%Y%m%d'))
		if image_folder.exists():
			pass
		else:
			image_folder.mkdir()
		return image_folder
		
		

