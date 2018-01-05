#!/usr/bin/env python3
# created by kabcode@gmail.com
# information and further details can be found under www.kabelitzens.de

"""
This python class is for different language options
It contains the current language as well as the other language options
"""

from pathlib import Path
from importlib import util
import tokenize

class LanguageAdapter:
	 
	
	def __init__(self, photobooth_folder):
		self.current_language = "en"
		self.language_folder = photobooth_folder.joinpath('languages')
		self.language_list = []
		self.list_languages()
		self.cl = None
		self.set_language(self.current_language)
		
	def set_language(self, language):
		language_module = language+'.py'
		print(language_module)
		if language_module in self.language_list:
			self.current_language = language
			_spec = util.spec_from_file_location(language, self.language_folder.joinpath(language_module).__str__())
			if _spec is None:
				print("Error - Cannot find specified file.")
			else:
				_module = util.module_from_spec(_spec)
				_spec.loader.exec_module(_module)
				print("Changed language to " + language)
				self.cl = _module
		else:
			print("Error - language not available.")
		
	def list_languages(self):
		for item in Path(self.language_folder).glob('*.py'):
			if item.is_file():
				self.language_list.append(item.name)
				
				
