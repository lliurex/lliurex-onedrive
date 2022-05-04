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


SPACE_CREATION_SUCCESSFULL=0
SPACE_DUPLICATE_ERROR=-1

class GatherInfo(QThread):

	def __init__(self,*args):
		
		QThread.__init__(self)

	#def _init__

	def run(self,*args):
		
		time.sleep(1)
		Bridge.onedriveMan.loadOneDriveConfig()

	#def run

class CreateSpace(QThread):

	def __init__(self,*args):
		
		QThread.__init__(self)
		self.spaceInfo=args[0]
		self.ret=[]

	#def __init__

	def run (self,*args):
		
		self.ret=Bridge.onedriveMan.createSpace(self.spaceInfo)
	
	#def run

#class CreateSpace

class GatherLibraries(QThread):

	def __init__(self,*args):
		
		QThread.__init__(self)
		self.dataSP=args[0]

	#def __init__

	def run (self,*args):
		
		Bridge.onedriveMan.getSharePointLibraries(self.dataSP[0],self.dataSP[1])

	#def run 

#class GatherLibraries

class Bridge(QObject):

	onedriveMan=OnedriveManager.OnedriveManager()

	def __init__(self,ticket=None):

		QObject.__init__(self)

		self._spacesModel=SpacesModel.SpacesModel()
		self._libraryModel=LibraryModel.LibraryModel()
		self._currentStack=0
		self._spacesCurrentOption=0
		self._closeGui=False
		self._closePopUp=True
		self._authUrl=Bridge.onedriveMan.authUrl
		self._showSpaceSettingsMessage=[False,"","Information"]
		self._showSpaceFormMessage=[False,"","Information"]
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

	def _getClosePopUp(self):

		return self._closePopUp

	#def _getClosePopUp	

	def _setClosePopUp(self,closePopUp):
		
		if self._closePopUp!=closePopUp:
			self._closePopUp=closePopUp
			self.on_closePopUp.emit()

	#def _setClosePopUp		

	def _getShowSpaceSettingsMessage(self):

		return self._showSpaceSettingsMessage

	#def _getShowSpaceSettingsMessage	

	def _setShowSpaceSettingsMessage(self,showSpaceSettingsMessage):
		
		if self._showSpaceSettingsMessage!=showSpaceSettingsMessage:
			self._showSpaceSettingsMessage=showSpaceSettingsMessage
			self.on_showSpaceSettingsMessage.emit()

	#def _setShowSpaceSettingsMessage				

	def _getShowSpaceFormMessage(self):

		return self._showSpaceFormMessage

	#def _getShowSpaceFormMessage	

	def _setShowSpaceFormMessage(self,showSpaceFormMessage):
		
		if self._showSpaceFormMessage!=showSpaceFormMessage:
			self._showSpaceFormMessage=showSpaceFormMessage
			self.on_showSpaceFormMessage.emit()

	#def _setShowSpaceFormMessage

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
			if item["idLibrary"]!="":
				self._libraryModel.appendRow(item["idLibrary"],item["nameLibrary"])
	
	#def _updateLibraryModel

	@Slot(int)
	def moveToSpaceOption(self,option):
		
		self.spacesCurrentOption=option

	#def moveToSpaceOption

	@Slot('QVariantList')
	def getSharePointLibraries(self,data):

		print("recibido")
		print(data)

		if Bridge.onedriveMan.checkIfEmailExists(data[0]):
			self.closePopUp=False
			self.gatherLibraries=GatherLibraries(data)
			self.gatherLibraries.start()
			self.gatherLibraries.finished.connect(self._getSharePointLibraries)

		else:
			print("nothing to do")
	
	#def getSharePointLibraries

	def _getSharePointLibraries(self):

		self.closePopUp=True
		self._updateLibraryModel()

	#def _getSharePointLibraries

	@Slot('QVariantList')
	def createSpace(self,spaceInfo):

		self.showSpaceFormMessage=[False,"","Information"]
		self.spaceInfo=spaceInfo
		if not Bridge.onedriveMan.checkDuplicate(spaceInfo):
			ret=Bridge.onedriveMan.checkPreviousLocalFolder(spaceInfo)
			self.spacesCurrentOption=2
		else:
			self.showSpaceFormMessage=[True,SPACE_DUPLICATE_ERROR,"Error"]

	#def createSpace

	@Slot(str)
	def getToken(self,token):

		Bridge.onedriveMan.createToken(token)
		self.spacesCurrentOption=1
		self.closePopUp=False
		self.createSpaceT=CreateSpace(self.spaceInfo)
		self.createSpaceT.start()
		self.createSpaceT.finished.connect(self._createSpace)

	#def getToken

	def _createSpace(self):

		self._updateSpacesModel()
		self.closePopUp=True
		if self.createSpaceT.ret:
			self.spacesCurrentOption=0
			self.showSpaceSettingsMessage=[True,SPACE_CREATION_SUCCESSFULL,"Ok"]		
	
	#def _createSpace

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

	on_closePopUp=Signal()
	closePopUp=Property(bool,_getClosePopUp,_setClosePopUp, notify=on_closePopUp)

	on_showSpaceSettingsMessage=Signal()
	showSpaceSettingsMessage=Property('QVariantList',_getShowSpaceSettingsMessage,_setShowSpaceSettingsMessage, notify=on_showSpaceSettingsMessage)

	on_showSpaceFormMessage=Signal()
	showSpaceFormMessage=Property('QVariantList',_getShowSpaceFormMessage,_setShowSpaceFormMessage, notify=on_showSpaceFormMessage)

	authUrl=Property(str,_getAuthUrl,constant=True)
	spacesModel=Property(QObject,_getSpacesModel,constant=True)
	libraryModel=Property(QObject,_getLibraryModel,constant=True)

#class Bridge

if __name__=="__main__":

	pass
