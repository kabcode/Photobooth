#!/usr/bin/env python3
# created by kabcode@gmail.com
# information and further details can be found under www.kabelitzens.de

"""
This python script is the entry point for the photobooth
"""
# import libs
from pathlib import Path

# import own libs
import language as lg

if __name__ == '__main__':
	
	# get current photobooth folder
	current_folder = Path.cwd().parent
	print(current_folder)
	
	global lang = lg.LanguageAdapter(current_folder)
	print(lang.cl.test)
	lang.set_language('de')
	print(lang.cl.test)
	lang.set_language('it')
	print(lang.cl.test)
	lang.set_language('en')
	print(lang.cl.test)
