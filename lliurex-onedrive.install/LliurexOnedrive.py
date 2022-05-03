from PySide2.QtCore import QObject,Signal,Slot,QThread,Property,QTimer,Qt,QModelIndex
import os 
import OnedriveManager
import sys
import threading
import time
import copy
import SpacesModel
import LibraryModel

import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

START_SYNCHRONIZATION_ERROR="-10"
STOP_SYNCHRONIZATION_ERROR="-11"
LOCAL_FOLDER_EMPTY="-12"
LOCAL_FOLDER_REMOVED="-13"

DISABLE_SYNC_OPTIONS=0
CHANGE_SYNC_OPTIONS_OK=1
CHANGE_SYNC_OPTIONS_ERROR=-1
CHANGE_SYNC_FOLDERS_ERROR=-2

class GatherInfo(QThread):

	def __init__(self,*args):
		
		QThread.__init__(self)

	#def _init__

	def run(self,*args):
		
		time.sleep(1)
		Bridge.onedriveMan.loadOneDriveConfig()

	#def run

#class GatherInfo

class Bridge(QObject):

	onedriveMan=OnedriveManager.OnedriveManager()

	def __init__(self,ticket=None):

		QObject.__init__(self)

		self._spacesModel=SpacesModel.SpacesModel()
		self._libraryModel=LibraryModel.LibraryModel()
		self._currentStack=0
		self._spacesCurrentOption=0
		self._closeGui=False
		self._authUrl=Bridge.onedriveMan.authUrl
		self.initBridge()

	#def _init__

	def initBridge(self):

		self.currentStack=0
		self.gatherInfo=GatherInfo()
		self.gatherInfo.start()
		self.gatherInfo.finished.connect(self._loadConfig)
	
	#def initBridge
	
	def _loadConfig(self):

		self._updateSpacesModel()
		self.currentStack=1

	#def _loadAccount

	def _getCurrentStack(self):

		return self._currentStack

	#def _getCurrentStack	

	def _setCurrentStack(self,currentStack):
		
		if self._currentStack!=currentStack:
			self._currentStack=currentStack
			self.on_currentStack.emit()

	#def _setCurentStack

	def _getSpacesCurrentOption(self):

		return self._spacesCurrentOption

	#def _getCurrentStack	

	def _setSpacesCurrentOption(self,spacesCurrentOption):
		
		if self._spacesCurrentOption!=spacesCurrentOption:
			self._spacesCurrentOption=spacesCurrentOption
			self.on_spacesCurrentOption.emit()

	#def _setCurentStack

	def _getAuthUrl(self):

		return self._authUrl

	#def _getAuthUrl	

	def _getSpacesModel(self):

		return self._spacesModel

	#def _getSpacesModel

	def _getLibraryModel(self):

		return self._libraryModel

	#def _getLibraryModel

	def _getCloseGui(self):

		return self._closeGui

	#def _getCloseGui	

	def _setCloseGui(self,closeGui):
		
		if self._closeGui!=closeGui:
			self._closeGui=closeGui
			self.on_closeGui.emit()

	#def _setCloseGui					

	def _updateSpacesModel(self):

		ret=self._spacesModel.clear()
		spacesEntries=Bridge.onedriveMan.spacesConfigData
		for item in spacesEntries:
			if item["name"]!="":
				self._spacesModel.appendRow(item["name"])
	
	#def _updateSpacesModel

	def _updateLibraryModel(self):

		ret=self._libraryModel.clear()
		libraryEntries=Bridge.onedriveMan.librariesConfigData
		for item in libraryEntries:
			if item["name"]!="":
				self._libraryModel.appendRow(item["name"],item["id"])
	
	#def _updateLibraryModel

	@Slot(int)
	def moveToSpaceOption(self,option):
		
		self.spacesCurrentOption=option

	#def moveToSpaceOption

	@Slot(str)
	def getToken(self,token):

		Bridge.onedriveMan.createToken(token)
		self.spacesCurrentOption=1

	#def getToken

	@Slot('QVariantList')
	def getSharePointLibraries(self,data):

		Bridge.onedriveMan.getSharePointLibraries(data[0],data[1])
		self._updateLibraryModel()

	@Slot()
	def openHelp(self):
		lang=os.environ["LANG"]

		if 'valencia' in lang:
			self.help_cmd='xdg-open https://wiki.edu.gva.es/lliurex/tiki-index.php?page=Lliurex-Onedrive.'
		else:
			self.help_cmd='xdg-open https://wiki.edu.gva.es/lliurex/tiki-index.php?page=Lliurex-Onedrive'
		
		self.open_help_t=threading.Thread(target=self._openHelp)
		self.open_help_t.daemon=True
		self.open_help_t.start()

	#def openHelp

	def _openHelp(self):

		os.system(self.help_cmd)

	#def _openHelp

	@Slot()
	def closeOnedrive(self):

		self.closeGui=True

	#def closeOnedrive
	
	on_currentStack=Signal()
	currentStack=Property(int,_getCurrentStack,_setCurrentStack, notify=on_currentStack)

	on_spacesCurrentOption=Signal()
	spacesCurrentOption=Property(int,_getSpacesCurrentOption,_setSpacesCurrentOption, notify=on_spacesCurrentOption)

	on_closeGui=Signal()
	closeGui=Property(bool,_getCloseGui,_setCloseGui, notify=on_closeGui)

	authUrl=Property(str,_getAuthUrl,constant=True)
	spacesModel=Property(QObject,_getSpacesModel,constant=True)
	libraryModel=Property(QObject,_getLibraryModel,constant=True)

#class Bridge

if __name__=="__main__":

	pass
