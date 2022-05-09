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
SPACE_CREATION_ERROR=-3


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
		self.initialDownload=""
		self.ret=[]

	#def __init__

	def run (self,*args):
		
		self.ret=Bridge.onedriveMan.createSpace(self.spaceInfo,self.reuseToken)
		if self.ret:
			if Bridge.onedriveMan.isConfigured():
				self.initialDownload=Bridge.onedriveMan.getInitialDownload()
		
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
		self.tempConfig=False
		self._showPreviousFolderDialog=False
		self._initialDownload=""
		self._hddFreeSpace=""
		self._showDownloadDialog=False
		self._showAccountMessage=[False,""]
		self._manageCurrentOption=0
		self._spaceLocalFolder=""
		self._autoStartEnabled=Bridge.onedriveMan.autoStartEnabled
		self._monitorInterval=int(Bridge.onedriveMan.monitorInterval)
		self._rateLimit=int(Bridge.onedriveMan.rateLimit)	
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

	#def _getSpacesCurrentOption	

	def _setSpacesCurrentOption(self,spacesCurrentOption):
		
		if self._spacesCurrentOption!=spacesCurrentOption:
			self._spacesCurrentOption=spacesCurrentOption
			self.on_spacesCurrentOption.emit()

	#def _setSpacesCurrentOption

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

	def _getShowPreviousFolderDialog(self):

		return self._showPreviousFolderDialog

	#def _getShowSpaceFormMessage	

	def _setShowPreviousFolderDialog(self,showPreviousFolderDialog):
		
		if self._showPreviousFolderDialog!=showPreviousFolderDialog:
			self._showPreviousFolderDialog=showPreviousFolderDialog
			self.on_showPreviousFolderDialog.emit()

	#def _setShowPreviousFolderDialog
	
	def _getInitialDownload(self):

		return self._initialDownload

	#def _getInitialDownload	

	def _setInitialDownload(self,initialDownload):
		
		if self._initialDownload!=initialDownload:
			self._initialDownload=initialDownload
			self.on_initialDownload.emit()

	#def _setInitialDownload

	def _getHddFreeSpace(self):

		return self._hddFreeSpace

	#def _getHddFreeSpace	

	def _setHddFreeSpace(self,hddFreeSpace):
		
		if self._hddFreeSpace!=hddFreeSpace:
			self._hddFreeSpace=hddFreeSpace		
			self.on_hddFreeSpace.emit()

	#def _setHddFreeSpace

	def _getShowDownloadDialog(self):

		return self._showDownloadDialog
	
	#def _getShowDownloadDialog

	def _setShowDownloadDialog(self,showDownloadDialog):

		if self._showDownloadDialog!=showDownloadDialog:
			self._showDownloadDialog=showDownloadDialog
			self.on_showDownloadDialog.emit()

	#def _setShowDownloadDialog

	def _getShowAccountMessage(self):

		return self._showAccountMessage

	#def _getShowAccountMessage

	def _setShowAccountMessage(self,showAccountMessage):

		if self._showAccountMessage!=showAccountMessage:
			self._showAccountMessage=showAccountMessage	
			self.on_showAccountMessage.emit()

	#def _setShowAccountMessage

	def _getManageCurrentOption(self):

		return self._manageCurrentOption

	#def _getManageCurrentOption	

	def _setManageCurrentOption(self,manageCurrentOption):
		
		if self._manageCurrentOption!=manageCurrentOption:
			self._manageCurrentOption=manageCurrentOption
			self.on_manageCurrentOption.emit()

	#def _setManageCurrentOption

	def _getSpaceLocalFolder(self):

		return self._spaceLocalFolder
	
	#def _getSpaceLocalFolder

	def _setSpaceLocalFolder(self,spaceLocalFolder):

		if self._spaceLocalFolder!=spaceLocalFolder:
			self._spaceLocalFolder=spaceLocalFolder
			self.on_spaceLocalFolder.emit()

	#def _setSpaceLocalFolder
	
	def _getAutoStartEnabled(self):
		
		return self._autoStartEnabled

	#def _getAutoStartEnabled

	def _setAutoStartEnabled(self,autoStartEnabled):

		if self._autoStartEnabled!=autoStartEnabled:
			self._autoStartEnabled=autoStartEnabled		
			self.on_autoStartEnabled.emit()

	#def _setAutoStartEnabled

	def _getRateLimit(self):

		return self._rateLimit

	#def _getRateLimit

	def _setRateLimit(self,rateLimit):

		if self._rateLimit!=int(rateLimit):
			self._rateLimit=int(rateLimit)
			self.on_rateLimit.emit()

	#def _setRateLimit

	def _getMonitorInterval(self):
		
		return self._monitorInterval

	#def _getMonitorInterval

	def _setMonitorInterval(self,monitorInterval):

		if self._monitorInterval!=int(monitorInterval):
			self._monitorInterval=int(monitorInterval)
			self.on_monitorInterval.emit()

	#def _setMonitorInterval

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
		
		self.showSpaceSettingsMessage=[False,"","Information"]
		self.showSpaceFormMessage=[False,"","Information"]
		self._libraryModel.clear()
		self.spacesCurrentOption=option

	#def moveToSpaceOption

	@Slot('QVariantList')
	def getSharePointLibraries(self,data):

		self._showSpaceFormMessage=[False,"","Information"]
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
		self.closeGui=False
		self.gatherLibrariesT=GatherLibraries(self.data)
		self.gatherLibrariesT.start()
		self.gatherLibrariesT.finished.connect(self._gatherLibraries)
	
	#def gatherLibraries

	def _gatherLibraries(self):

		self._updateLibraryModel()
		self.closePopUp=[True,""]
		self.closeGui=True

	#def _gatherLibraries

	@Slot('QVariantList')
	def checkData(self,spaceInfo):

		self.showSpaceFormMessage=[False,"","Information"]
		self.spaceInfo=spaceInfo
		self.checkDuplicate=Bridge.onedriveMan.checkDuplicate(spaceInfo)
		
		if not self.checkDuplicate[0]:
			ret=Bridge.onedriveMan.checkPreviousLocalFolder(spaceInfo)
			if ret:
				self.showPreviousFolderDialog=True
			else:
				self.createSpace()
		else:
			self.showSpaceFormMessage=[True,SPACE_DUPLICATE_ERROR,"Error"]

	#def checkData

	@Slot(str)
	def getToken(self,token):

		Bridge.onedriveMan.createToken(token)
		self.spacesCurrentOption=1
		if not self.tempConfig:
			self.addSpace()
		else:
			self.gatherLibraries()

	#def getToken

	@Slot(int)
	def managePreviousFolderDialog(self,response):

		self.showPreviousFolderDialog=False

		if response==0:
			self.createSpace()
		else:
			self._libraryModel.clear()
			self.spacesCurrentOption=0

	#def managePreviousFolderDialog

	def createSpace(self):

		if self.spaceInfo[1]=="onedrive":
			if self.checkDuplicate[1]:
				self.reuseToken=True
				self.addSpace()
			else:
				self.reuseToken=False
				self.spacesCurrentOption=2
		else:
			if self.reuseToken:
				self.addSpace()

	#def createSpace

	def addSpace(self):

		self.closePopUp=[False,SPACE_CREATION_MESSAGE]
		self.closeGui=False
		self.createSpaceT=CreateSpace(self.spaceInfo,self.reuseToken)
		self.createSpaceT.start()
		self.createSpaceT.finished.connect(self._addSpace)

	#def createSpace

	def _addSpace(self):

		self._updateSpacesModel()
		self.closePopUp=[True,""]
		self.reuseToken=False
		self.tempConfig=False
		self.closeGui=True
		self._libraryModel.clear()

		if self.createSpaceT.ret:
			self.spaceLocalFolder=Bridge.onedriveMan.spaceLocalFolder
			self.hddFreeSpace=Bridge.onedriveMan.getHddFreeSpace()
			self.initialDownload=self.createSpaceT.initialDownload
			if self.initialDownload!="":
				self.showDownloadDialog=True
			else:
				self.showSpaceSettingsMessage=[True,SPACE_CREATION_SUCCESSFULL,"Ok"]		
		else:
			self.showSpaceSettingsMessage=[True,SPACE_CREATION_ERROR,"Error"]		

	#def _createSpace

	@Slot(str)
	def manageDownloadDialog(self,option):

		self.showDownloadDialog=False
		if option=="All":
			self._initialStartUp()
		else:
			self.currentStack=2
			self.manageCurrentOption=0

	#def manageDownloadDialog
	
	@Slot()
	def goHome(self):

		self.currentStack=1
		self.spacesCurrentOption=0

	#def goHome

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

	on_showPreviousFolderDialog=Signal()
	showPreviousFolderDialog=Property(bool,_getShowPreviousFolderDialog,_setShowPreviousFolderDialog, notify=on_showPreviousFolderDialog)

	on_initialDownload=Signal()
	initialDownload=Property(str,_getInitialDownload,_setInitialDownload,notify=on_initialDownload)

	on_hddFreeSpace=Signal()
	hddFreeSpace=Property(str,_getHddFreeSpace,_setHddFreeSpace,notify=on_hddFreeSpace)

	on_showDownloadDialog=Signal()
	showDownloadDialog=Property(bool,_getShowDownloadDialog,_setShowDownloadDialog,notify=on_showDownloadDialog)

	on_showAccountMessage=Signal()
	showAccountMessage=Property('QVariantList',_getShowAccountMessage,_setShowAccountMessage,notify=on_showAccountMessage)

	on_manageCurrentOption=Signal()
	manageCurrentOption=Property(int,_getManageCurrentOption,_setManageCurrentOption, notify=on_manageCurrentOption)

	on_spaceLocalFolder=Signal()
	spaceLocalFolder=Property(str,_getSpaceLocalFolder,_setSpaceLocalFolder,notify=on_spaceLocalFolder)
	
	on_autoStartEnabled=Signal()
	autoStartEnabled=Property(bool,_getAutoStartEnabled,_setAutoStartEnabled,notify=on_autoStartEnabled)
	
	on_rateLimit=Signal()
	rateLimit=Property(int,_getRateLimit,_setRateLimit,notify=on_rateLimit)

	on_monitorInterval=Signal()
	monitorInterval=Property(int,_getMonitorInterval,_setMonitorInterval,notify=on_monitorInterval)

	authUrl=Property(str,_getAuthUrl,constant=True)
	spacesModel=Property(QObject,_getSpacesModel,constant=True)
	libraryModel=Property(QObject,_getLibraryModel,constant=True)

#class Bridge

if __name__=="__main__":

	pass
