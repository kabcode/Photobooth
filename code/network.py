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
		self.wifi_connection = self.check_wifi_connection()
		self.internet_connection = self.check_internet_connection()
			
	# choose wifi interface	
	def find_wifi_interface(self, interface_name="wlan0"):
		wifi = pywifi.PyWiFi()
		ifaces = wifi.interfaces()
		for item in ifaces:
			if item.name() == interface_name:
				iface = item
				return iface
		print("Error - Cannot find wifi interface.")
		return None
		
	# find available wifi networks	
	def find_wifi_networks(self):
		if self.iface is not None:
			self.iface.scan()
			sleep(2)
			wifi_list = self.iface.scan_results()
			return wifi_list
		else:
			print("Error - No network interface available.")
			return None
		
	# connect to a wifi network
	def select_wifi(self,ssid=""):
		if(ssid == ""):
			print("Error - No ssid name given.")
			return None
		wifi_list = self.find_wifi_networks()
		for item in wifi_list:
			if item.ssid == ssid:
				return item
		print("Error - Selected wifi not found.")
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
						self.wlan_connection  = True	
				else:
					print("Error - No password given.")
			else:
				# connectiong to wifi without password
				self.iface.add_network_profile(wifi)
				self.iface.connect(wifi)
				if self.iface.status() == const.IFACE_DISCONNECTED:	
					print("Unknown Error - Something went wrong.")
				if self.iface.status() > const.IFACE_SCANNING:
					self.wlan_connection = True
		# no cell returned
		else:
			print("Error - Cannot connect to wifi.")

	# check for wifi connection
	def check_wifi_connection(self):
		if self.iface.status() == const.IFACE_DISCONNECTED:
			return False
		if self.iface.status() == const.IFACE_SCANNING:
			return False
		if self.iface.status() == const.IFACE_CONNECTED:
			return True

    # check for internet connection with the selected wifi
	def check_internet_connection(self):
		if self.wifi_connection:
			req = []
			try:
				req = requests.get("https://google.com")
			except:
				# https request fails
				print("Error - Internet network connection lost.")
				return False
			# https request succeded
			return True
		else:
			print("Error - No wifi connection.")
				
# for testing this module
if __name__ == '__main__':
	
	NA = NetworkAdapter()
	print(NA.wifi_connection)
	print(NA.internet_connection)
		
		
			
	
	
	
		
