#!/usr/bin/env python
# created by kabcode@gmail.com
# information and further details can be found under www.kabelitzens.de

"""
This python class is for different language options
It contains the current language as well as the other language options
"""

from os import scandir

class LanguageAdapter:
	 
	
	def __init__(self, photobooth_folder):
		self.current_language = "en"
		self.language_folder = os.path.join(photobooth_folder, languages)
		
	def change_language(self, language):
		self.current_language = language
		
	def list_languages(self):
		languages = [f.name for f in os.scandir(self.language_folder) if f.is_file()]
				
