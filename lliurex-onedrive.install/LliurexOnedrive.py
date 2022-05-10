from PySide2.QtCore import QObject,Signal,Slot,QThread,Property,QTimer,Qt,QModelIndex
import os 
import OnedriveManager
import sys
import threading
import time
import copy
import SpacesModel
import LibraryModel
import Model

import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)


SPACE_CREATION_SUCCESSFULL=0
SPACE_CREATION_MESSAGE=1
SEARCH_LIBRARY_MESSAGE=2
SPACE_LOADING_SETTINGS=3
DISABLE_SYNC_OPTIONS=4
CHANGE_SYNC_OPTIONS_OK=5
START_SYNC_MESSAGE=6
STOP_SYNC_MESSAGE=7
CHECKING_STATUS_MESSAGE=8
REMOVE_SPACE_MESSAGE=9
APPLY_SPACE_SETTINGS_MESSAGE=10

SPACE_DUPLICATE_ERROR=-1
SPACE_LIBRARIES_EMPTY_ERROR=-2
SPACE_CREATION_ERROR=-3
CHANGE_SYNC_OPTIONS_ERROR=-4
CHANGE_SYNC_FOLDERS_ERROR=-5
START_SYNCHRONIZATION_ERROR=-10
STOP_SYNCHRONIZATION_ERROR=-11
LOCAL_FOLDER_EMPTY=-12
LOCAL_FOLDER_REMOVED=-13


class GatherInfo(QThread):

	def __init__(self,*args):
		
		QThread.__init__(self)

	#def _init__

	def run(self,*args):
		
		time.sleep(1)
		Bridge.onedriveMan.loadOneDriveConfig()

	#def run

#class GatherInfo

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

class GatherSpaceSettings(QThread):

	def __init__(self,*args):
		
		QThread.__init__(self)
		self.isOnedriveRunning=False
		self.localFolderEmpty=False
		self.localFolderRemoved=False
		self.accountStatus=0
		self.freeSpace=""
		self.spaceToLoad=args[0]

	#def _init__

	def run(self,*args):
		
		time.sleep(1)
		Bridge.onedriveMan.loadSpaceSettings(self.spaceToLoad)
		self.isOnedriveRunning=Bridge.onedriveMan.isOnedriveRunning()
		self.localFolderEmpty,self.localFolderRemoved=Bridge.onedriveMan.checkLocalFolder()
		'''
		if not self.localFolderRemoved:
			error,self.accountStatus,self.freeSpace=Bridge.onedriveMan.getAccountStatus()
		'''
	#def run

#class GatherSpaceSettings

class GetFolderStruct(QThread):

	def __init__(self,*args):
		
		QThread.__init__(self)
		self.localFolder=args[0]

	#def __init

	def run(self,*args):

		Bridge.onedriveMan.getFolderStruct(self.localFolder)
	
	#def run

#class GetFolderStruct

class ManageSync(QThread):
	
	def __init__(self,*args):
		
		QThread.__init__(self)
		self.startAction=args[0]
		self.ret=[]
	
	#def __init

	def run(self,*args):

		self.ret=Bridge.onedriveMan.manageSync(self.startAction)

	#def run

#class ManageSync

class AccountStatus(QThread):

	def __init__(self,*args):

		QThread.__init__(self)
		self.ret=[]
	
	#def __init

	def run(self,*args):

		self.ret=Bridge.onedriveMan.getAccountStatus()

	#def run

#class AccountStatus

class RemoveAccount(QThread):

	def __init__(self,*args):

		QThread.__init__(self)
		self.ret=[]

	#def __init

	def run(self,*args):

		self.ret=Bridge.onedriveMan.removeAccount()

	#def run

#class RemoveAccount

class ApplySettingsChanges(QThread):

	def __init__(self,*args):

		QThread.__init__(self)
		self.ret=[]
		self.initialConfig=args[0]
	
	#def __init

	def run(self,*args):

		self.ret=Bridge.onedriveMan.applySettingsChanges(self.initialConfig)

	#def run


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
		self._showSettingsDialog=False
		self._isOnedriveRunning=False
		self._accountStatus=0
		self._bandWidthNames=Bridge.onedriveMan.bandWidthNames
		self._freeSpace=""
		self._settingsChanged=False
		self._showSettingsMessage=[False,""]
		self._showAccountMessage=[False,""]
		self._infoStackType="Configuration"
		self._showSynchronizeMessage=[False,DISABLE_SYNC_OPTIONS,"Information"]
		self._showSynchronizeDialog=False
		self.initialConfig=copy.deepcopy(Bridge.onedriveMan.currentConfig)
		self.initialSyncConfig=copy.deepcopy(Bridge.onedriveMan.currentSyncConfig)
		self._syncAll=Bridge.onedriveMan.syncAll
		self._syncCustomChanged=False
		self.keepFolders=True
		self._initialDownload=""
		self._hddFreeSpace=""
		self._showDownloadDialog=False
		self._showPreviousDialog=False
		self._currentOptionsStack=0
		self.errorGetFolder=False
		self.changedSyncWorked=False
		self._localFolderEmpty=False
		self._localFolderRemoved=False
		self.folderEntries=[{"path":"OneDrive", "name": "OneDrive","isChecked":True, "isExpanded": True,"type":"parent","subtype":"root","hide":False,"level":1,"canExpanded":True,"parentPath":""}]
		self._folderModel=Model.MyModel(self.folderEntries)
		self.removeAction=False
		self.moveToOption=""
		self.moveToStack=""
		self.initStartUp=False
		
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

	def _getAccountStatus(self):

		return self._accountStatus

	#def _getAccountStatus	

	def _setAccountStatus(self,accountStatus):
		
		if self._accountStatus!=accountStatus:
			self._accountStatus=accountStatus
			self.on_accountStatus.emit()	

	#def _setAccountStatus 

	def _getFreeSpace(self):

		return self._freeSpace

	#def _getFreeSpace	

	def _setFreeSpace(self,freeSpace):
		
		if self._freeSpace!=freeSpace:
			self._freeSpace=freeSpace
			self.on_freeSpace.emit()	
	
	#def _setFreeSpace

	def _getBandWidthNames(self):
		
		return self._bandWidthNames

	#def _getBandWidthNames

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

	def _getFolderModel(self):
		
		return self._folderModel

	#def _getFolderModel

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

	def _getFreeSpace(self):

		return self._freeSpace

	#def _getFreeSpace	

	def _setFreeSpace(self,freeSpace):
		
		if self._freeSpace!=freeSpace:
			self._freeSpace=freeSpace
			self.on_freeSpace.emit()	
	
	#def _setFreeSpace

	def _getSettingsChanged(self):

		return self._settingsChanged

	#def _getSettingsChanged

	def _setSettingsChanged(self,settingsChanged):

		if self._settingsChanged!=settingsChanged:
			self._settingsChanged=settingsChanged
			self.on_settingsChanged.emit()

	#def _setSettingsChanged

	def _getShowSettingsMessage(self):

		return self._showSettingsMessage

	#def _getShowSettingsMessage
	
	def _setShowSettingsMessage(self,showSettingsMessage):

		if self._showSettingsMessage!=showSettingsMessage:
			self._showSettingsMessage=showSettingsMessage
			self.on_showSettingsMessage.emit()

	#def _setShowSettingsMessage

	def _getShowSettingsDialog(self):

		return self._showSettingsDialog

	#def _getShowSettingsDialog
	
	def _setShowSettingsDialog(self,showSettingsDialog):

		if self._showSettingsDialog!=showSettingsDialog:
			self._showSettingsDialog=showSettingsDialog
			self.on_showSettingsDialog.emit()

	#def _setShowSettingsDialog

	'''
	def _getShowUnlinkDialog(self):

		return self._showUnlinkDialog

	#def _getShowUnlinkDialog
	
	def _setShowUnlinkDialog(self,showUnlinkDialog):

		if self._showUnlinkDialog!=showUnlinkDialog:
			self._showUnlinkDialog=showUnlinkDialog
			self.on_showUnlinkDialog.emit()

	#def _setShowUnlinkDialog
	'''
	def _getShowAccountMessage(self):

		return self._showAccountMessage

	#def _getShowAccountMessage

	def _setShowAccountMessage(self,showAccountMessage):

		if self._showAccountMessage!=showAccountMessage:
			self._showAccountMessage=showAccountMessage	
			self.on_showAccountMessage.emit()

	#def _setShowAccountMessage

	def _getShowSynchronizeDialog(self):

		return self._showSynchronizeDialog

	#def _getShowSynchronizeDialog
	
	def _setShowSynchronizeDialog(self,showSynchronizeDialog):

		if self._showSynchronizeDialog!=showSynchronizeDialog:
			self._showSynchronizeDialog=showSynchronizeDialog
			self.on_showSynchronizeDialog.emit()

	#def _setShowSynchronizeDialog

	def _getShowSynchronizeMessage(self):

		return self._showSynchronizeMessage

	#def _getShowSynchronizeMessage
	
	def _setShowSynchronizeMessage(self,showSynchronizeMessage):

		if self._showSynchronizeMessage!=showSynchronizeMessage:
			self._showSynchronizeMessage=showSynchronizeMessage
			self.on_showSynchronizeMessage.emit()

	#def _setShowSynchronizeMessage

	def _getSyncAll(self):

		return self._syncAll

	#def _getSyncAll
	
	def _setSyncAll(self,syncAll):

		if self._syncAll!=syncAll:
			self._syncAll=syncAll
			self.on_syncAll.emit()

	#def _setSyncAll	

	def _getSyncCustomChanged(self):

		return self._syncCustomChanged

	#def _getSyncCustomChanged

	def _setSyncCustomChanged(self,syncCustomChanged):

		if self._syncCustomChanged!=syncCustomChanged:
			self._syncCustomChanged=syncCustomChanged
			self.on_syncCustomChanged.emit()

	#def _setSyncCustomChanged

	def _getLocalFolderEmpty(self):

		return self._localFolderEmpty
	
	#def _getLocalFolderEmpty

	def _setLocalFolderEmpty(self,localFolderEmpty):

		if self._localFolderEmpty!=localFolderEmpty:
			self._localFolderEmpty=localFolderEmpty
			self.on_localFolderEmpty.emit()

	#def _setLocalFolderEmpty
	
	def _getLocalFolderRemoved(self):

		return self._localFolderRemoved
	
	#def _getLocalFolderRemoved

	def _setLocalFolderRemoved(self,localFolderRemoved):

		if self._localFolderRemoved!=localFolderRemoved:
			self._localFolderRemoved=localFolderRemoved
			self.on_localFolderRemoved.emit()

	#def _setLocalFolderRemoved

	def _getIsOnedriveRunning(self):

		return self._isOnedriveRunning

	#def _getIsOnedriveRunning	

	def _setIsOnedriveRunning(self,isOnedriveRunning):
		
		if self._isOnedriveRunning!=isOnedriveRunning:
			self._isOnedriveRunning=isOnedriveRunning
			self.on_isOnedriveRunning.emit()	

	#def _setIsOnedriveRunning

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
		
		Bridge.onedriveMan.initSpacesSettings()
		self.showSpaceSettingsMessage=[False,"","Information"]
		self.showSpaceFormMessage=[False,"","Information"]
		self._libraryModel.clear()
		self.spacesCurrentOption=option

	#def moveToSpaceOption

	@Slot('QVariantList')
	def getSharePointLibraries(self,data):

		self.showSpaceFormMessage=[False,"","Information"]
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

	@Slot(int)
	def moveToManageOption(self,option):
		
		if self.manageCurrentOption!=option:
			self.moveToOption=option
			if self.settingsChanged:
				self.showSettingsDialog=True
			elif self.syncCustomChanged:
				self.showSynchronizeMessage
			else:
				self.manageCurrentOption=option
				self.moveToOption=""

	#def moveToSpaceOption

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
			self.spaceLocalFolder=os.path.basename(Bridge.onedriveMan.spaceLocalFolder)
			self.hddFreeSpace=Bridge.onedriveMan.getHddFreeSpace()
			self.initialDownload=self.createSpaceT.initialDownload
			self.isOnedriveRunning=Bridge.onedriveMan.isOnedriveRunning()
			self._getInitialSettings()
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

	def _initialStartUp(self):

		self.manageSync=ManageSync(True)
		self.manageSync.start()
		self.manageSync.finished.connect(self._endInitialStartUp)
		
	#def _initialStartUp

	def _endInitialStartUp(self):

		self.isOnedriveRunning=Bridge.onedriveMan.isOnedriveRunning()
		self.initStartUp=True
		
		if not self.isOnedriveRunning:
			self.showAccountMessage=[True,START_SYNCHRONIZATION_ERROR]
			self.currentStack=2
			self.manageCurrentOption=0
		else:
			self.checkAccountStatus()

	#def _endInitialStartUp
	
	@Slot(str)
	def loadSpace(self,space):

		self.closePopUp=[False,SPACE_LOADING_SETTINGS]
		self.closeGui=False
		self.getSpaceSettings=GatherSpaceSettings(space)
		self.getSpaceSettings.start()
		self.getSpaceSettings.finished.connect(self._loadSpace)

	#def gotToSpace

	def _loadSpace(self):

		self._getInitialSettings()
		self.spaceLocalFolder=os.path.basename(Bridge.onedriveMan.spaceLocalFolder)
		self.syncAll=Bridge.onedriveMan.syncAll
		self.initialSyncConfig=copy.deepcopy(Bridge.onedriveMan.currentSyncConfig)
		self.isOnedriveRunning=self.getSpaceSettings.isOnedriveRunning
		self.localFolderEmpty=self.getSpaceSettings.localFolderEmpty
		self.localFolderRemoved=self.getSpaceSettings.localFolderRemoved

		if not self.localFolderRemoved:
			self.accountStatus=self.getSpaceSettings.accountStatus
			self.freeSpace=self.getSpaceSettings.freeSpace
			if not self.syncAll:
				if not self.localFolderEmpty:
					self.getFolderStruct=GetFolderStruct(True)
					self.getFolderStruct.start()
					self.getFolderStruct.finished.connect(self._endLoading)

				else:
					self._endLoading()
			else:
				self._endLoading()
		else:
			self._endLoading()

	#def _loadAccount

	def _endLoading(self):

		if not self.syncAll:
			if self.isOnedriveRunning:
				self.showSynchronizeMessage=[True,DISABLE_SYNC_OPTIONS,"Information"]
			self._updateFolderStruct()

		self.closePopUp=[True,""]
		self.closeGui=True

		self.currentStack=2
		self.manageCurrentOption=0
	
	#def _endLoading

	def _updateFolderStruct(self):

		self.errorGetFolder=Bridge.onedriveMan.errorFolder
		self._insertModelEntries()
		
		if self.errorGetFolder:
			self.showSynchronizeMessage=[True,CHANGE_SYNC_FOLDERS_ERROR,"Error"]

	#def _updateFolderStruct

	def _insertModelEntries(self):

		ret=self._folderModel.resetModel()
		entries=Bridge.onedriveMan.folderStruct
		for item in entries:
			self._folderModel.appendRow(item["path"],item["name"],item["isChecked"],item["isExpanded"],item["type"],item["subtype"],item["hide"],item["level"],item["canExpanded"],item["parentPath"])

	#def _insertModelEntries

	def _getInitialSettings(self):

		self.autoStartEnabled=Bridge.onedriveMan.autoStartEnabled
		self.monitorInterval=int(Bridge.onedriveMan.monitorInterval)
		self.rateLimit=int(Bridge.onedriveMan.rateLimit)
		self.initialConfig=copy.deepcopy(Bridge.onedriveMan.currentConfig)

	#def _getInitialConfig

	@Slot()
	def goHome(self):

		if not self.settingsChanged:
			self.currentStack=1
			self.spacesCurrentOption=0
			self.moveToStack=""
		else:
			self.moveToStack=1
			self.showSettingsDialog=True

	#def goHome

	@Slot()
	def openFolder(self):

		self.open_folder_t=threading.Thread(target=self._openFolder)
		self.open_folder_t.daemon=True
		self.open_folder_t.start()

	#def openFolder

	def _openFolder(self):

		cmd="xdg-open "+os.path.join(Bridge.onedriveMan.spaceLocalFolder)
		os.system(cmd)

	#def _openFolder

	@Slot(bool)
	def manageSync(self,startSync):

		if startSync:
			msg=START_SYNC_MESSAGE
		else:
			msg=STOP_SYNC_MESSAGE

		self.closePopup=[False,msg]
		self.isRunningBefore=Bridge.onedriveMan.isOnedriveRunning()
		self.manageSyncT=ManageSync(startSync)
		self.manageSyncT.start()
		self.manageSyncT.finished.connect(self._manageSync)

	#def manageSync

	def _manageSync(self):

		self.isOnedriveRunning=Bridge.onedriveMan.isOnedriveRunning()
		if self.isRunningBefore==self.isOnedriveRunning:
			if self.isRunningBefore:
				self.showAccountMessage=[True,STOP_SYNCHRONIZATION_ERROR]
			else:
				self.showAccountMessage=[True,START_SYNCHRONIZATION_ERROR]
		else:
			self.showAccountMessage=[False,""]

		
		if self.isOnedriveRunning:
			self.showSynchronizeMessage=[True,DISABLE_SYNC_OPTIONS,"Information"]
		else:
			self.showSynchronizeMessage=[False,DISABLE_SYNC_OPTIONS,"Information"]


		self.closePopUp=[True,""]
	
	#def _manageSync

	@Slot()
	def checkAccountStatus(self):

		if not self.initStartUp:
			self.closePopUp=[False,CHECKING_STATUS_MESSAGE]
		self.getAccountStatus=AccountStatus()
		self.getAccountStatus.start()
		self.getAccountStatus.finished.connect(self._checkAccountStatus)

	#def checkAccountStatus

	def _checkAccountStatus(self):

		if self.initStartUp:
			self.showSynchronizeMessage=[True,DISABLE_SYNC_OPTIONS,"Information"]
			self.currentStack=2
			self.initStartUp=False
		else:
			self.closePopUp=[True,""]

		self.accountStatus=self.getAccountStatus.ret[1]
		self.freeSpace=self.getAccountStatus.ret[2]

	#def _checkAccountStatus 

	@Slot()
	def removeAccount(self):

		self.closePopUp=[False,REMOVE_SPACE_MESSAGE]
		self.closeGui=False
		#self.showUnlinkDialog=False
		self.removeAccountT=RemoveAccount()
		self.removeAccountT.start()
		self.removeAccountT.finished.connect(self._removeAccount)

	#def removeAccount

	def _removeAccount(self):

		if self.removeAccountT.ret:
			Bridge.onedriveMan.loadOneDriveConfig()
			self._updateSpacesModel()
			self.currentStack=1
			self.spacesCurrentOption=0
			self.removeAction=True
		else:
			self.showAccountMessage=[True,STOP_SYNCHRONIZATION_ERROR]	
	
		self.closePopUp=[True,""]
		self.closeGui=True

	#def _removeAccount

	@Slot(bool)
	def manageAutoStart(self,value):
		
		if value!=self.initialConfig[0]:
			if value!=Bridge.onedriveMan.currentConfig[0]:
				self.settingsChanged=True
			else:
				self.settingsChanged=False
			self.initialConfig[0]=value
			self.autoStartEnabled=value
		else:
			self.settingsChanged=False

	#def manageAutoStart

	@Slot(int)
	def getMonitorInterval(self,value):

		if value!=self.initialConfig[1]:
			if value!=Bridge.onedriveMan.currentConfig[1]:
				self.settingsChanged=True
			else:
				self.settingsChanged=False
			self.monitorInterval=int(value)
			self.initialConfig[1]=int(value)
		else:
			self.settingsChanged=False

	#def getMonitorInterval

	@Slot(int)
	def getRateLimit(self,value):

		if value!=self.initialConfig[2]:
			if value!=Bridge.onedriveMan.currentConfig[2]:
				self.settingsChanged=True
			else:
				self.settingsChanged=False
			self.rateLimit=int(value)
			self.initialConfig[2]=int(value)
		else:
			self.settingsChanged=False

	#def getRateLimit

	@Slot()
	def applySettingsChanges(self):

		self.closePopUp=[False,APPLY_SPACE_SETTINGS_MESSAGE]
		self.closeGui=False
		self.applySettingsChangesT=ApplySettingsChanges(self.initialConfig)
		self.applySettingsChangesT.start()
		self.applySettingsChangesT.finished.connect(self._applySettingsChanges)

	#def applySettingsChanges

	def _applySettingsChanges(self):

		self.initialConfig=copy.deepcopy(Bridge.onedriveMan.currentConfig)
		self.closePopUp=[True,""]
		self.showSettingsMessage=[True,self.applySettingsChangesT.ret[1]]
		self.showSettingsDialog=False

		if not self.applySettingsChangesT.ret[0]:
			if not self.syncCustomChanged:
				self.closeGui=True
			self.settingsChanged=False
		else:
			self.moveToOption=""
			self.moveToStack=""

		if self.moveToOption!="":
			self.manageCurrentOption=self.moveToOption
			self.showSettingsMessage=[False,""]
			self.moveToOption=""
		elif self.moveToStack!="":
			self.showSettingsMessage=[False,""]
			self.currentStack=self.moveToStack
			self.spacesCurrentOption=0
			self.moveToStack=""

	#def _applySettingsChanges

	@Slot()
	def cancelSettingsChanges(self):

		self.hideSettingsMessage()
		self.settingsChanged=False
		self.showSettingsDialog=False
		self.initialConfig=copy.deepcopy(Bridge.onedriveMan.currentConfig)
		self.autoStartEnabled=self.initialConfig[0]
		self.monitorInterval=int(self.initialConfig[1])
		self.rateLimit=self.initialConfig[2]
		if self.moveToOption!="":
			self.manageCurrentOption=self.moveToOption
			self.moveToOption=""
		elif self.moveToStack!="":
			self.currentStack=self.moveToStack
			self.moveToStack=""

	#def cancelSettingsChanges

	@Slot()
	def hideSettingsMessage(self):

		self.showSettingsMessage=[False,'']

	#def hideSettingsMessage

	@Slot(str)
	def manageSettingsDialog(self,action):
		
		if action=="Accept":
			self.applySettingsChanges()
		elif action=="Discard":
			self.cancelSettingsChanges()
		elif action=="Cancel":
			self.closeGui=False
			self.showSettingsDialog=False
			self.moveToOption=""
	
	#def manageSettingsDialog

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

		if not self.removeAction:
			if self.settingsChanged:
				self.closeGui=False
				self.showSettingsDialog=True
			else:
				if self.syncCustomChanged:
					self.closeGui=False
					if self.closePopUp[0]:
						self.showSynchronizeDialog=True
				else:
					if self.closePopUp[0]:
						#Bridge.onedriveMan.manageFileFilter("restore")
						self.closeGui=True
					else:
						self.closeGui=False
		else:
			self.closeGui=True

	#def closeOnedrive
	
	on_currentStack=Signal()
	currentStack=Property(int,_getCurrentStack,_setCurrentStack, notify=on_currentStack)

	on_spacesCurrentOption=Signal()
	spacesCurrentOption=Property(int,_getSpacesCurrentOption,_setSpacesCurrentOption, notify=on_spacesCurrentOption)

	on_accountStatus=Signal()
	accountStatus=Property(int,_getAccountStatus,_setAccountStatus, notify=on_accountStatus)

	on_freeSpace=Signal()
	freeSpace=Property(str,_getFreeSpace,_setFreeSpace, notify=on_freeSpace)

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

	on_freeSpace=Signal()
	freeSpace=Property(str,_getFreeSpace,_setFreeSpace, notify=on_freeSpace)

	on_settingsChanged=Signal()
	settingsChanged=Property(bool,_getSettingsChanged,_setSettingsChanged, notify=on_settingsChanged)

	on_showSettingsMessage=Signal()
	showSettingsMessage=Property('QVariantList',_getShowSettingsMessage,_setShowSettingsMessage,notify=on_showSettingsMessage)
	
	on_showSettingsDialog=Signal()
	showSettingsDialog=Property(bool,_getShowSettingsDialog,_setShowSettingsDialog,notify=on_showSettingsDialog)

	'''
	on_showUnlinkDialog=Signal()
	showUnlinkDialog=Property(bool,_getShowUnlinkDialog,_setShowUnlinkDialog,notify=on_showUnlinkDialog)
	'''
	on_showAccountMessage=Signal()
	showAccountMessage=Property('QVariantList',_getShowAccountMessage,_setShowAccountMessage,notify=on_showAccountMessage)

	on_syncAll=Signal()
	syncAll=Property(bool,_getSyncAll,_setSyncAll,notify=on_syncAll)

	on_showSynchronizeMessage=Signal()
	showSynchronizeMessage=Property('QVariantList',_getShowSynchronizeMessage,_setShowSynchronizeMessage,notify=on_showSynchronizeMessage)

	on_showSynchronizeDialog=Signal()
	showSynchronizeDialog=Property(bool,_getShowSynchronizeDialog,_setShowSynchronizeDialog,notify=on_showSynchronizeDialog)
	
	on_syncCustomChanged=Signal()
	syncCustomChanged=Property(bool,_getSyncCustomChanged,_setSyncCustomChanged,notify=on_syncCustomChanged)

	on_localFolderEmpty=Signal()
	localFolderEmpty=Property(bool,_getLocalFolderEmpty,_setLocalFolderEmpty,notify=on_localFolderEmpty)

	on_localFolderRemoved=Signal()
	localFolderRemoved=Property(bool,_getLocalFolderRemoved,_setLocalFolderRemoved,notify=on_localFolderRemoved)

	on_isOnedriveRunning=Signal()
	isOnedriveRunning=Property(bool,_getIsOnedriveRunning,_setIsOnedriveRunning, notify=on_isOnedriveRunning)

	authUrl=Property(str,_getAuthUrl,constant=True)
	spacesModel=Property(QObject,_getSpacesModel,constant=True)
	libraryModel=Property(QObject,_getLibraryModel,constant=True)
	bandWidthNames=Property('QVariant',_getBandWidthNames,constant=True)
	folderModel=Property(QObject,_getFolderModel,constant=True)

#class Bridge

if __name__=="__main__":

	pass
