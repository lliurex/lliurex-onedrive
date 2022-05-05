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
SPACE_CREATION_MESSAGE=1
SEARCH_LIBRARY_MESSAGE=2
SPACE_DUPLICATE_ERROR=-1
SPACE_LIBRARIES_EMPTY_ERROR=-2


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
		self.reuseToken=args[1]
		self.ret=[]

	#def __init__

	def run (self,*args):
		
		self.ret=Bridge.onedriveMan.createSpace(self.spaceInfo,self.reuseToken)
	
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
		self._closePopUp=[True,""]
		self._authUrl=Bridge.onedriveMan.authUrl
		self._showSpaceSettingsMessage=[False,"","Information"]
		self._showSpaceFormMessage=[False,"","Information"]
		self.reuseToken=False
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
		if len(libraryEntries)>0:
			for item in libraryEntries:
				if item["idLibrary"]!="":
					self._libraryModel.appendRow(item["idLibrary"],item["nameLibrary"])
		else:
			self.showSpaceFormMessage=[True,SPACE_LIBRARIES_EMPTY_ERROR,"Error"]
	
	#def _updateLibraryModel

	@Slot(int)
	def moveToSpaceOption(self,option):
		
		self.spacesCurrentOption=option

	#def moveToSpaceOption

	@Slot('QVariantList')
	def getSharePointLibraries(self,data):

		self.reuseToken=True
		self.tempConfig=False
		self.data=data

		if Bridge.onedriveMan.checkIfEmailExists(self.data[0]):
			self.gatherLibraries()
		else:
			self.tempConfig=True
			self.spacesCurrentOption=2

	#def getSharePointLibraries

	def gatherLibraries(self):

		self.closePopUp=[False,SEARCH_LIBRARY_MESSAGE]
		self.gatherLibrariesT=GatherLibraries(self.data)
		self.gatherLibrariesT.start()
		self.gatherLibrariesT.finished.connect(self._gatherLibraries)
	
	#def gatherLibraries

	def _gatherLibraries(self):

		self.closePopUp=[True,""]
		self._updateLibraryModel()

	#def _gatherLibraries

	@Slot('QVariantList')
	def createSpace(self,spaceInfo):

		self.showSpaceFormMessage=[False,"","Information"]
		self.spaceInfo=spaceInfo
		
		if not Bridge.onedriveMan.checkDuplicate(spaceInfo)[0]:
			ret=Bridge.onedriveMan.checkPreviousLocalFolder(spaceInfo)
			if spaceInfo[1]=="onedrive":
				if Bridge.onedriveMan.checkDuplicate(spaceInfo)[1]:
					self.reuseToken=True
					self.addSpace()
				else:
					self.reuseToken=False
					self.spacesCurrentOption=2
			else:
				if self.reuseToken:
					self.addSpace()
		else:
			self.showSpaceFormMessage=[True,SPACE_DUPLICATE_ERROR,"Error"]

	#def createSpace

	@Slot(str)
	def getToken(self,token):

		Bridge.onedriveMan.createToken(token)
		self.spacesCurrentOption=1
		if not self.tempConfig:
			self.addSpace()
		else:
			self.gatherLibraries()

	#def getToken

	def addSpace(self):

		self.closePopUp=[False,SPACE_CREATION_MESSAGE]
		self.createSpaceT=CreateSpace(self.spaceInfo,self.reuseToken)
		self.createSpaceT.start()
		self.createSpaceT.finished.connect(self._addSpace)

	#def createSpace

	def _addSpace(self):

		self._updateSpacesModel()
		self.closePopUp=[True,""]
		self.reuseToken=False
		self.tempConfig=False
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
	closePopUp=Property('QVariantList',_getClosePopUp,_setClosePopUp, notify=on_closePopUp)

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
