#!/usr/bin/env python3
# created by kabcode@gmail.com
# information and further details can be found under www.kabelitzens.de

"""
This python script is wifi connection module for the photobooth. It uses
the wifi module pywifi (to install: pip3 install pywifi). All available
networks are listed and the user can chose which one to use.  
"""

# imports
import pywifi
import requests
from pywifi import const
from time import sleep

class NetworkAdapter:
	
	# initiation of the wifi adapter
	def __init__(self):
		self.iface = self.find_wifi_interface()
		if self.iface == None:
			print("Error - Cannot find wifi interface.")
		
		
	# choose wifi interface	
	def find_wifi_interface(self, interface_name="wlan0"):
		wifi = pywifi.PyWiFi()
		ifaces = wifi.interfaces()
		for item in ifaces:
			if item.name() == interface_name:
				iface = item
				return iface
		return None
		
	# find available wifi networks	
	def find_wifi_networks(self):
		self.iface.scan()
		sleep(2)
		wifi_list = self.iface.scan_results()
		return wifi_list
		
	# connect to a wifi network
	def select_wifi(self,ssid):
		wifi_list = self.find_wifi_networks()
		for item in wifi_list:
			if item.ssid == ssid:
				return item
		return None
		
	# connect to selected wifi network
	def connect_to_wifi(self, ssid, password=None):
		wifi = self.select_wifi(ssid)
				
		if wifi:
			print("Connecting to " + wifi.ssid)
			
			# wifi is encrypted
			if all(algo > const.AKM_TYPE_NONE for algo in wifi.akm):
				print("Wifi is encrypted.")
				if password:
					wifi.key = password
					
					self.iface.add_network_profile(wifi)
					self.iface.connect(wifi)
					while(self.iface.status()==const.IFACE_CONNECTING):
						pass
												
					print(self.iface.status())
					if self.iface.status() == const.IFACE_DISCONNECTED:	
						print("Error - Wrong password given.")
					if self.iface.status() == const.IFACE_CONNECTED:
						print("Connection established.")
						
				else:
					print("Error - No password given.")
			
			else:
				
				# connectiong to wifi
				self.iface.add_network_profile(wifi)
				self.iface.connect(wifi)
				if self.iface.status() == const.IFACE_DISCONNECTED:	
					print("Unknown Error - Something went wrong.")
				if self.iface.status() > const.IFACE_SCANNING:
					print("Connection established.")
				
		# no cell returned
		else:
			print("Error - Selected wifi not found")

    # check for internet connection with the selected wifi
    def check_internet_connection(self):
		if self.iface.status == const.IFACE_CONNECTED:
			req = []
			try:
				req = requests.get("https://google.com")
			except:
				print("Error - Internet network connection lost.")
		else:
			print("Error - No wifi connection.")
				
			
		
		
			
	
	
	
		
