#!/usr/bin/env python3

import sys


import OnedriveManager
import ToolStack
import SettingsStack
import SyncStack
import SpaceStack
import AddSpaceStack
import MainStack

class Core:
	
	singleton=None
	DEBUG=False
	
	@classmethod
	def get_core(self):
		
		if Core.singleton==None:
			Core.singleton=Core()
			Core.singleton.init()

		return Core.singleton
		
	
	def __init__(self,args=None):

	
		self.dprint("Init...")
		
	#def __init__
	
	def init(self):

	
		self.onedriveManager=OnedriveManager.OnedriveManager()
		self.toolStack=ToolStack.Bridge()
		self.settingsStack=SettingsStack.Bridge()
		self.syncStack=SyncStack.Bridge()
		self.spaceStack=SpaceStack.Bridge()
		self.addSpaceStack=AddSpaceStack.Bridge()
		self.mainStack=MainStack.Bridge()
		
		self.mainStack.initBridge()
	
		
	#def init

	def dprint(self,msg):
		
		if Core.DEBUG:
			
			print("[CORE] %s"%msg)
	
	#def  dprint
