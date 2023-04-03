from PySide2.QtCore import QObject,Signal,Slot,QThread,Property,QTimer,Qt,QModelIndex
import os 
import OnedriveManager
import sys
import threading
import time
import copy
import SpacesModel
import SharePointModel
import LibraryModel
import FolderModel

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
SPACE_GET_FOLDER_MESSAGE=10
SPACE_FOLDER_RESTORE_MESSAGE=11
APPLY_SPACE_CHANGES_MESSAGE=12
SPACE_RUNNING_TEST_MESSAGE=13
SPACE_RUNNING_REPAIR_MESSAGE=14
SPACE_GLOBAL_WARNING=15
SEARCH_SPACE_SHAREPOINT=16
SPACE_MIGRATION_MESSAGE=17
TOOLS_DEFAULT_MESSAGE=18
UPDATE_TOKEN_MESSAGE=19
SPACE_MIGRATION_SUCCESS=20

SPACE_DUPLICATE_ERROR=-1
SPACE_LIBRARIES_EMPTY_ERROR=-2
SPACE_CREATION_ERROR=-3
CHANGE_SYNC_OPTIONS_ERROR=-4
CHANGE_SYNC_FOLDERS_ERROR=-5
START_SYNCHRONIZATION_ERROR=-10
STOP_SYNCHRONIZATION_ERROR=-11
LOCAL_FOLDER_EMPTY=-12
LOCAL_FOLDER_REMOVED=-13
SPACE_SHAREPOINT_EMPTY_ERROR=-14
SPACE_MIGRATION_ERROR=-15
UPDATE_TOKEN_ERROR=-16
GET_TOKEN_ERROR=-19
HDD_SPACE_AVAILABLE_ERROR=-20

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
		self.ret=[]

	#def __init__

	def run (self,*args):
		
		self.ret=Bridge.onedriveMan.createSpace(self.spaceInfo,self.reuseToken)

	#def run

#class CreateSpace

class GatherSharePoints(QThread):

	def __init__(self,*args):
		
		QThread.__init__(self)
		self.dataSP=args[0]
		self.ret=True

	#def __init__

	def run (self,*args):
		
		self.ret=Bridge.onedriveMan.getSpaceSharePoints(self.dataSP)

	#def run

#class GatherSharePoints 

class GatherLibraries(QThread):

	def __init__(self,*args):
		
		QThread.__init__(self)
		self.dataSP=args[0]

	#def __init__

	def run (self,*args):
		
		Bridge.onedriveMan.getSharePointLibraries(self.dataSP)

	#def run 

#class GatherLibraries

class GatherSpaceSettings(QThread):

	def __init__(self,*args):
		
		QThread.__init__(self)
		self.spaceToLoad=args[0]

	#def _init__

	def run(self,*args):
		
		time.sleep(1)
		self.matchSpace=Bridge.onedriveMan.loadSpaceSettings(self.spaceToLoad)

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
		if self.ret:
			Bridge.onedriveMan.loadOneDriveConfig()
			Bridge.onedriveMan.removeACService()

	#def run

#class RemoveAccount

class ApplySyncChanges(QThread):

	def __init__(self,*args):

		QThread.__init__(self)
		self.ret=[]
		self.initialSyncConfig=args[0]
		self.keepFolders=args[1]
	
	#def __init

	def run(self,*args):

		self.ret=Bridge.onedriveMan.applySyncChanges(self.initialSyncConfig,self.keepFolders)

	#def run

#class ApplySyncChanges

class ApplySettingsChanges(QThread):

	def __init__(self,*args):

		QThread.__init__(self)
		self.ret=[]
		self.initialConfig=args[0]
	
	#def __init

	def run(self,*args):

		self.ret=Bridge.onedriveMan.applySettingsChanges(self.initialConfig)

	#def run

#class ApplySettingsChanges

class TestOneDrive(QThread):

	def __init__(self,*args):

		QThread.__init__(self)

	#def __init

	def run(self,*args):

		Bridge.onedriveMan.testOnedrive()

	#def run

#class TestOneDrive

class RepairOneDrive(QThread):

	def __init__(self,*args):

		QThread.__init__(self)

	#def __init

	def run(self,*args):

		Bridge.onedriveMan.repairOnedrive()

	#def run

#class RepairOneDrive

class MigrateSpace(QThread):

	def __init__(self,*args):
		QThread.__init__(self)
		self.spaceInfo=args[0]
		self.ret=[]

	#def __init__

	def run (self,*args):
		
		self.ret=Bridge.onedriveMan.migrateSpace(self.spaceInfo)
	
	#def run

#class MigrateSpace


class Bridge(QObject):

	onedriveMan=OnedriveManager.OnedriveManager()

	def __init__(self,ticket=None):

		QObject.__init__(self)

		self._spacesModel=SpacesModel.SpacesModel()
		self._sharePointModel=SharePointModel.SharePointModel()
		self._libraryModel=LibraryModel.LibraryModel()
		self._currentStack=0
		self._spacesCurrentOption=0
		self._closeGui=False
		self._closePopUp=[True,""]
		self.loginUrl="https://login.microsoftonline.com/common/oauth2/v2.0/authorize?client_id=d50ca740-c83f-4d1b-b616-12c519384f0c&scope=Files.ReadWrite%20Files.ReadWrite.all%20Sites.Read.All%20Sites.ReadWrite.All%20offline_access&response_type=code&redirect_uri=https://login.microsoftonline.com/common/oauth2/nativeclient&login_hint="
		self._authUrl=self.loginUrl
		self._showSpaceSettingsMessage=[False,"","Information"]
		self._showSpaceFormMessage=[False,"","Information"]
		self.reuseToken=False
		self.tempConfig=False
		self._formData=["",0]
		self._showPreviousFolderDialog=False
		self._initialDownload=""
		self._hddFreeSpace=""
		self._showDownloadDialog=False
		self._showAccountMessage=[False,"","Error"]
		self._manageCurrentOption=0
		self._spaceBasicInfo=["","","","",""]
		self._spaceLocalFolder=""
		self._autoStartEnabled=Bridge.onedriveMan.autoStartEnabled
		self._monitorInterval=int(Bridge.onedriveMan.monitorInterval)
		self._rateLimit=int(Bridge.onedriveMan.rateLimit)
		self._skipSize=Bridge.onedriveMan.skipSize
		self._logEnabled=Bridge.onedriveMan.logEnabled
		self._logSize=""	
		self._showSettingsDialog=False
		self._isOnedriveRunning=False
		self._accountStatus=0
		self._bandWidthNames=Bridge.onedriveMan.bandWidthNames
		self._maxFileSizeNames=Bridge.onedriveMan.maxFileSizeNames
		self._freeSpace=""
		self._settingsChanged=False
		self._showSettingsMessage=[False,""]
		self._showSynchronizeMessage=[False,DISABLE_SYNC_OPTIONS,"Information"]
		self._showSynchronizeDialog=False
		self._showSynchronizePendingDialog=False
		self.initialConfig=copy.deepcopy(Bridge.onedriveMan.currentConfig)
		self.initialSyncConfig=copy.deepcopy(Bridge.onedriveMan.currentSyncConfig)
		self._syncAll=Bridge.onedriveMan.syncAll
		self._syncCustomChanged=False
		self._showFolderStruct=Bridge.onedriveMan.showFolderStruct
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
		self._folderModel=FolderModel.FolderModel(self.folderEntries)
		self.removeAction=False
		self.moveToOption=""
		self.moveToStack=""
		self.initStartUp=False
		self._requiredMigration=False
		self.checkGlobalLocalFolderTimer=QTimer(None)
		self.checkGlobalLocalFolderTimer.timeout.connect(self.getGlobalLocalFolderInfo)
		self.checkGlobalStatusTimer=QTimer(None)
		self.checkGlobalStatusTimer.timeout.connect(self.getGlobalStatusInfo)
		self._showToolsMessage=[False,TOOLS_DEFAULT_MESSAGE,"Information"]
		self.updateSpaceAuth=False
		self._withHDDSpace=True
		self.waitForUpdateGlobalMessage=10

		if len(sys.argv)>1:
			self.spaceToManage=sys.argv[1]
		else:
			self.spaceToManage=""

		self.initBridge()

	#def _init__

	def initBridge(self):

		self.currentStack=0
		self.gatherInfo=GatherInfo()
		self.gatherInfo.start()
		self.gatherInfo.finished.connect(self._loadConfig)
	
	#def initBridge
	
	def _loadConfig(self):

		if not os.path.exists(Bridge.onedriveMan.oldConfigPath):
			self.checkGlobalLocalFolderTimer.start(1000)
			self.checkGlobalStatusTimer.start(30000)
			if len(Bridge.onedriveMan.onedriveConfig['spacesList'])>0:
				if Bridge.onedriveMan.globalOneDriveFolderWarning or Bridge.onedriveMan.globalOneDriveStatusWarning:
					self.showSpaceSettingsMessage=[True,SPACE_GLOBAL_WARNING,"Warning"]
				
				self._updateSpacesModel()
			if self.spaceToManage!="":
				self.loadSpace(self.spaceToManage)
			else:	
				self.currentStack=1
		else:
			self.requiredMigration=True
			self.currentStack=1
			self.spacesCurrentOption=3

	#def _loadConfig

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

	def _setAuthUrl(self,authUrl):

		if self._authUrl!=authUrl:
			self._authUrl=authUrl
			self.on_authUrl.emit()

	#def _setAuthUrl	

	def _getSpacesModel(self):

		return self._spacesModel

	#def _getSpacesModel

	def _getSharePointModel(self):

		return self._sharePointModel

	#def _getSharePointModel

	def _getLibraryModel(self):

		return self._libraryModel

	#def _getLibraryModel

	def _getFormData(self):

		return self._formData

	#def _getFormData

	def _setFormData(self,formData):

		if self._formData!=formData:
			self._formData=formData
			self.on_formData.emit()

	#def _setFormData

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

	def _getMaxFileSizeNames(self):

		return self._maxFileSizeNames

	#def _getMaxFileSizeNames

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

	def _getSpaceBasicInfo(self):

		return self._spaceBasicInfo

	#def _getSpaceBasicInfo

	def _setSpaceBasicInfo(self,spaceBasicInfo):

		if self._spaceBasicInfo!=spaceBasicInfo:
			self._spaceBasicInfo=spaceBasicInfo
			self.on_spaceBasicInfo.emit()

	#def _setSpaceBasicInfo

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

	def _getSkipSize(self):

		return self._skipSize

	#def _getSkipSize

	def _setSkipSize(self,skipSize):

		if self._skipSize!=skipSize:
			self._skipSize=skipSize
			self.on_skipSize.emit()

	#def _setSkipSize

	def _getLogEnabled(self):

		return self._logEnabled

	#def _getLogEnabled

	def _setLogEnabled(self,logEnabled):

		if self._logEnabled!=logEnabled:
			self._logEnabled=logEnabled
			self.on_logEnabled.emit()

	#def _setLogEnabled

	def _getLogSize(self):

		return self._logSize

	#def _getLogSize

	def _setLogSize(self,logSize):

		if self._logSize!=logSize:
			self._logSize=logSize
			self.on_logSize.emit()

	#def _setLogSize

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

	def _getShowSynchronizeDialog(self):

		return self._showSynchronizeDialog

	#def _getShowSynchronizeDialog
	
	def _setShowSynchronizeDialog(self,showSynchronizeDialog):

		if self._showSynchronizeDialog!=showSynchronizeDialog:
			self._showSynchronizeDialog=showSynchronizeDialog
			self.on_showSynchronizeDialog.emit()

	#def _setShowSynchronizeDialog

	def _getShowSynchronizePendingDialog(self):

		return self._showSynchronizePendingDialog

	#def _getShowSynchronizePendingDialog
	
	def _setShowSynchronizePendingDialog(self,showSynchronizePendingDialog):

		if self._showSynchronizePendingDialog!=showSynchronizePendingDialog:
			self._showSynchronizePendingDialog=showSynchronizePendingDialog
			self.on_showSynchronizePendingDialog.emit()

	#def _setShowSynchronizePendingDialog

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

	def _getShowFolderStruct(self):

		return self._showFolderStruct

	#def _getShowFolderStruct
	
	def _setShowFolderStruct(self,showFolderStruct):

		if self._showFolderStruct!=showFolderStruct:
			self._showFolderStruct=showFolderStruct
			self.on_showFolderStruct.emit()

	#def _setShowFolderStruct	

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

	def _getRequiredMigration(self):

		return self._requiredMigration

	#def _getRequiredMigration

	def _setRequiredMigration(self,requiredMigration):

		if self._requiredMigration!=requiredMigration:
			self._requiredMigration=requiredMigration
			self.on_requiredMigration.emit()

	#def setRequiredMigration

	def _getShowToolsMessage(self):

		return self._showToolsMessage

	#def _getShowToolsMessage

	def _setShowToolsMessage(self,showToolsMessage):

		if self._showToolsMessage!=showToolsMessage:
			self._showToolsMessage=showToolsMessage
			self.on_showToolsMessage.emit() 

	#def _setShowToolsMessage

	def _getWithHDDSpace(self):

		return self._withHDDSpace

	#def _getWithHDDSpace

	def _setWithHDDSpace(self,withHDDSpace):

		if self._withHDDSpace!=withHDDSpace:
			self._withHDDSpace=withHDDSpace
			self.on_withHDDSpace.emit() 

	#def _setWithHDDSpace

	def _updateSpacesModel(self):

		ret=self._spacesModel.clear()
		spacesEntries=Bridge.onedriveMan.spacesConfigData
		for item in spacesEntries:
			if item["id"]!="":
				self._spacesModel.appendRow(item["id"],item["name"],item["status"],item["isRunning"],item["localFolderWarning"])
	
	#def _updateSpacesModel

	def _updateSharePointModel(self):

		ret=self._sharePointModel.clear()
		sharePointsEntries=Bridge.onedriveMan.sharePointsConfigData
		if len(sharePointsEntries)>0:
			for item in sharePointsEntries:
				self._sharePointModel.appendRow(item)
		else:
			self.showSpaceFormMessage=[True,SPACE_SHAREPOINT_EMPTY_ERROR,"Error"]
	
	#def _updateSharePointModel

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
		Bridge.onedriveMan.deleteTempConfig()
		moveTo=True
		if option==1:
			if not (Bridge.onedriveMan.thereAreHDDAvailableSpace()):
				moveTo=False

		if moveTo:
			self.formData=["",0]
			self.showSpaceSettingsMessage=[False,"","Information"]
			self.showSpaceFormMessage=[False,"","Information"]
			self._libraryModel.clear()
			self.spacesCurrentOption=option
		else:
			self.waitForUpdateGlobalMessage=0
			self.showSpaceSettingsMessage=[True,HDD_SPACE_AVAILABLE_ERROR,"Error"]

	#def moveToSpaceOption

	@Slot('QVariantList')
	def getSpaceSharePoints(self,data):

		self.showSpaceFormMessage=[False,"","Information"]
		self.reuseToken=True
		self.tempConfig=False
		self.tmpSpaceEmail=data[0]
		
		if Bridge.onedriveMan.checkIfEmailExists(data[0]):
			self.gatherSharePoints()
		else:
			self.authUrl=self.loginUrl+self.tmpSpaceEmail
			self.tempConfig=True
			self.formData=[data[0],data[1]]
			self.spacesCurrentOption=2

	#def getSpaceSharePoints

	def gatherSharePoints(self):

		self.closePopUp=[False,SEARCH_SPACE_SHAREPOINT]
		self.closeGui=False
		self.gatherSharePointsT=GatherSharePoints(self.tmpSpaceEmail)
		self.gatherSharePointsT.start()
		self.gatherSharePointsT.finished.connect(self._gatherSharePoints)
	
	#def gatherSharePoints

	def _gatherSharePoints(self):

		if self.gatherSharePointsT.ret:
			self._updateSharePointModel()
		else:
			self.showSpaceFormMessage=[True,GET_TOKEN_ERROR,"Error"]

		self.closePopUp=[True,""]
		self.closeGui=True
	
	#def _gatherSharePoints

	@Slot(str)
	def getSharePointLibraries(self,data):

		self.showSpaceFormMessage=[False,"","Information"]
		self.data=data

		self.gatherLibraries()

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

	@Slot()
	def resetSharePoints(self):

		if len(Bridge.onedriveMan.sharePointsConfigData)>0:
			self._sharePointModel.clear()
			Bridge.onedriveMan.sharePointsConfigData=[]

		if len(Bridge.onedriveMan.librariesConfigData)>0:
			self._libraryModel.clear()
			Bridge.onedriveMan.librariesConfigData=[]

	#def resetSharePoints

	@Slot('QVariantList')
	def checkData(self,spaceInfo):

		self.showSpaceFormMessage=[False,"","Information"]
		self.spaceInfo=spaceInfo
		self.formData[0]=spaceInfo[0]
		if spaceInfo[1]=="onedrive":
			self.formData[1]=0
		elif spaceInfo[1]=="sharepoint":
			self.formData[1]=1
		else:
			self.formData[1]=2

		if not self.requiredMigration:
			self.checkDuplicate=Bridge.onedriveMan.checkDuplicate(spaceInfo)
			
			if not self.checkDuplicate[0]:
				ret=Bridge.onedriveMan.checkPreviousLocalFolder(spaceInfo)
				if ret:
					self.showPreviousFolderDialog=True
				else:
					self.createSpace()
			else:
				self.showSpaceFormMessage=[True,SPACE_DUPLICATE_ERROR,"Error"]
		else:
			self.migrateSpace()

	#def checkData

	def migrateSpace(self):

		self.closePopUp=[False,SPACE_MIGRATION_MESSAGE]
		self.closeGui=False
		self.migrateSpaceT=MigrateSpace(self.spaceInfo)
		self.migrateSpaceT.start()
		self.migrateSpaceT.finished.connect(self._migrateSpace)

	#def migrateSpace

	def _migrateSpace(self):

		self._updateSpacesModel()
		self.tempConfig=False

		if self.migrateSpaceT.ret:
			self.spaceBasicInfo=Bridge.onedriveMan.spaceBasicInfo
			self.spaceLocalFolder=os.path.basename(Bridge.onedriveMan.spaceLocalFolder)
			spaceId=Bridge.onedriveMan.spaceId
			self.loadSpace(spaceId)
		else:
			self.closePopUp=[True,""]
			self.closeGui=True
			self.showSpaceFormMessage=[True,SPACE_MIGRATION_ERROR,"Error"]		

	#def _migrateSpace

	@Slot(str)
	def getToken(self,token):

		Bridge.onedriveMan.createToken(token,self.authUrl)
		if not self.updateSpaceAuth:
			self.spacesCurrentOption=1
			if not self.tempConfig:
				self.addSpace()
			else:
				if self.formData[1]!=0:
					self.gatherSharePoints()
				else:
					self.addSpace()

		else:
			self.manageCurrentOption=3
			self.updateSpaceAuthorization()

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
			self.showSettingsMessage=[False,'']
			self.updateSpaceAuth=False
			if self.settingsChanged:
				self.showSettingsDialog=True
			elif self.syncCustomChanged:
				self.showSynchronizePendingDialog=True
			else:
				self.manageCurrentOption=option
				self.moveToOption=""

	#def moveToManageOption

	def createSpace(self):

		if self.spaceInfo[1]=="onedrive":
			if self.checkDuplicate[1]:
				self.reuseToken=True
				self.addSpace()
			else:
				self.authUrl=self.loginUrl+self.spaceInfo[0]
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
		self.reuseToken=False
		self.tempConfig=False
		self._libraryModel.clear()
		self.withHDDSpace=True

		if self.createSpaceT.ret:
			self._initializeVars()
			self._getInitialSettings()
			self.hddFreeSpace=Bridge.onedriveMan.getHddFreeSpace()
			self.initialDownload=Bridge.onedriveMan.initialDownload
			self.showSynchronizeMessage=[False,DISABLE_SYNC_OPTIONS,"Information"]
			self.showFolderStruct=False

			if self.initialDownload!="":
				self.withHDDSpace=Bridge.onedriveMan.thereAreHDDAvailableSpace(True)
				self.showDownloadDialog=True
			else:
				self._initialStartUp()
		else:
			self.closePopUp=[True,""]
			self.closeGui=True
			self.showSpaceFormMessage=[True,GET_TOKEN_ERROR,"Error"]

	#def _createSpace

	@Slot(str)
	def manageDownloadDialog(self,option):

		self.showDownloadDialog=False
		if option=="All":
			self._initialStartUp()
		elif option=="Custom":
			self.currentStack=2
			self.manageCurrentOption=1
			self.spacesCurrentOption=0
			self.closePopUp=[True,""]
			self.closeGui=True
			self.accountStatus=3
		else:
			self.removeAccount()

	#def manageDownloadDialog

	def _initialStartUp(self):

		self.initStartUp=True
		
		self.closePopUp=[False,START_SYNC_MESSAGE]
		self.manageSyncT=ManageSync(True)
		self.manageSyncT.start()
		self.manageSyncT.finished.connect(self._endInitialStartUp)
		
	#def _initialStartUp

	def _endInitialStartUp(self):

		self.isOnedriveRunning=self.manageSyncT.ret[1]

		if not self.isOnedriveRunning:
			self.showAccountMessage=[True,START_SYNCHRONIZATION_ERROR,"Error"]
			self.currentStack=2
			self.manageCurrentOption=0
			self.spacesCurrentOption=0
			self.closePopUp=[True,""]
			self.closeGui=True

		else:
			self._updateSpacesModelInfo('isRunning')
			self.checkAccountStatus()

	#def _endInitialStartUp
	
	@Slot(str)
	def loadSpace(self,idSpace):

		self.closePopUp=[False,SPACE_LOADING_SETTINGS]
		self.closeGui=False
		self.getSpaceSettings=GatherSpaceSettings(idSpace)
		self.getSpaceSettings.start()
		self.getSpaceSettings.finished.connect(self._loadSpace)

	#def loadSpace

	def _loadSpace(self):

		if self.getSpaceSettings.matchSpace:
			self._initializeVars()
			self._getInitialSettings()
	
			if not self.localFolderRemoved:
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
				if self.localFolderRemoved:
					self.showAccountMessage=[True,LOCAL_FOLDER_REMOVED,"Error"]
				elif self.localFolderEmpty:
					self.showAccountMessage=[True,LOCAL_FOLDER_EMPTY,"Error"]
				self._endLoading()
			
			if self.isOnedriveRunning:
				self.showToolsMessage=[True,TOOLS_DEFAULT_MESSAGE,"Information"]
			else:
				self.showToolsMessage=[False,TOOLS_DEFAULT_MESSAGE,"Information"]
		else:
			self.closePopUp=[True,""]
			self.closeGui=True
			self.currentStack=1

	#def _loadAccount

	def _endLoading(self):

		if not self.syncAll:
			self._updateFolderStruct()
		else:
			self._folderModel.resetModel()
			self.showFolderStruct=False
			
		if self.isOnedriveRunning:
			self.showSynchronizeMessage=[True,DISABLE_SYNC_OPTIONS,"Information"]
		else:
			self.showSynchronizeMessage=[False,DISABLE_SYNC_OPTIONS,"Information"]
		
		self.checkSpaceLocalFolderTimer=QTimer(None)
		self.checkSpaceLocalFolderTimer.timeout.connect(self.checkSpaceLocalFolder)
		self.checkSpaceLocalFolderTimer.start(5000)

		self.closePopUp=[True,""]
		self.closeGui=True

		if self.requiredMigration:
			self.showAccountMessage=[True,SPACE_MIGRATION_SUCCESS,"OK"]
			self.requiredMigration=False
			self.spacesCurrentOption=0

		self.currentStack=2
		self.manageCurrentOption=0
	
	#def _endLoading

	def _insertModelEntries(self):

		ret=self._folderModel.resetModel()
		entries=Bridge.onedriveMan.folderStruct
		for item in entries:
			self._folderModel.appendRow(item["path"],item["name"],item["isChecked"],item["isExpanded"],item["type"],item["subtype"],item["hide"],item["level"],item["canExpanded"],item["parentPath"])

	#def _insertModelEntries

	def _initializeVars(self):

		self.spaceBasicInfo=Bridge.onedriveMan.spaceBasicInfo
		self.spaceLocalFolder=os.path.basename(Bridge.onedriveMan.spaceLocalFolder)
		self.syncAll=Bridge.onedriveMan.syncAll
		self.initialSyncConfig=copy.deepcopy(Bridge.onedriveMan.currentSyncConfig)
		self.isOnedriveRunning=Bridge.onedriveMan.isOnedriveRunning()
		self.localFolderEmpty=Bridge.onedriveMan.localFolderEmpty
		self.localFolderRemoved=Bridge.onedriveMan.localFolderRemoved
		self.showAccountMessage=[False,"","Error"]
		self.accountStatus=Bridge.onedriveMan.accountStatus
		self.freeSpace=Bridge.onedriveMan.freeSpace
		self._folderModel.resetModel()
		self.updateSpaceAuth=False

	#def _initializeVars

	def _getInitialSettings(self):

		self.autoStartEnabled=Bridge.onedriveMan.autoStartEnabled
		self.monitorInterval=int(Bridge.onedriveMan.monitorInterval)
		self.rateLimit=int(Bridge.onedriveMan.rateLimit)
		self.skipSize=Bridge.onedriveMan.skipSize
		self.logEnabled=Bridge.onedriveMan.logEnabled
		self.logSize=Bridge.onedriveMan.logSize
		self.initialConfig=copy.deepcopy(Bridge.onedriveMan.currentConfig)

	#def _getInitialSettings

	@Slot()
	def goHome(self):

		self.updateSpaceAuth=False
		if not self.settingsChanged and not self.syncCustomChanged:
			self.currentStack=1
			self.spacesCurrentOption=0
			self.manageCurrentOption=0
			self.moveToStack=""
			try:
				self.checkSpaceLocalFolderTimer.stop()
			except:
				pass
		else:
			self.moveToStack=1
			if self.settingsChanged:
				self.showSettingsDialog=True
			else:
				self.showSynchronizePendingDialog=True

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

		self.startSync=startSync
		if self.startSync:
			msg=START_SYNC_MESSAGE
		else:
			msg=STOP_SYNC_MESSAGE

		self.closePopup=[False,msg]
		self.manageSyncT=ManageSync(self.startSync)
		self.manageSyncT.start()
		self.manageSyncT.finished.connect(self._manageSync)

	#def manageSync

	def _manageSync(self):

		if not self.manageSyncT.ret[0]:
			if self.startSync:
				self.showAccountMessage=[True,STOP_SYNCHRONIZATION_ERROR,"Error"]
			else:
				self.showAccountMessage=[True,START_SYNCHRONIZATION_ERROR,"Error"]
		else:
			self.showAccountMessage=[False,"","Error"]
			self._updateSpacesModelInfo('isRunning')
		
		self.isOnedriveRunning=self.manageSyncT.ret[1]
		if self.isOnedriveRunning:
			self.showSynchronizeMessage=[True,DISABLE_SYNC_OPTIONS,"Information"]
		else:
			self.showSynchronizeMessage=[False,DISABLE_SYNC_OPTIONS,"Information"]

		self.closePopUp=[True,""]
	
	#def _manageSync

	def _updateSpacesModelInfo(self,param):

		updatedInfo=Bridge.onedriveMan.spacesConfigData
		if len(updatedInfo)>0:
			for i in range(len(updatedInfo)):
				index=self._spacesModel.index(i)
				self._spacesModel.setData(index,param,updatedInfo[i][param])

	#def _updateSpacesModelInfo

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
			self.manageCurrentOption=0
			self.spacesCurrentOption=0
			self.initStartUp=False
			if self.isOnedriveRunning:
				self.showToolsMessage=[True,TOOLS_DEFAULT_MESSAGE,"Information"]

		self.closePopUp=[True,""]
		self.closeGui=True
		self._updateSpacesModelInfo("status")
		self.accountStatus=self.getAccountStatus.ret[1]
		self.freeSpace=self.getAccountStatus.ret[2]

	#def _checkAccountStatus 

	@Slot()
	def removeAccount(self):

		self.closePopUp=[False,REMOVE_SPACE_MESSAGE]
		self.closeGui=False
		self.removeAccountT=RemoveAccount()
		self.removeAccountT.start()
		self.removeAccountT.finished.connect(self._removeAccount)

	#def removeAccount

	def _removeAccount(self):

		if self.removeAccountT.ret:
			self._updateSpacesModel()
			Bridge.onedriveMan.removeOrganizationDirectoryFile()
			self.currentStack=1
			self.spacesCurrentOption=0
			self.manageCurrentOption=0
			self.removeAction=True
		else:
			self.showAccountMessage=[True,STOP_SYNCHRONIZATION_ERROR,"Error"]	
	
		self.closePopUp=[True,""]
		self.closeGui=True

	#def _removeAccount

	@Slot(bool)
	def updateFolderStruct(self,localFolder):
		
		self.showSynchronizeMessage=[False,CHANGE_SYNC_OPTIONS_OK,"Information"]
		self.closePopUp=[False,SPACE_GET_FOLDER_MESSAGE]
		self.showFolderStruct=False
		self.getFolderStruct=GetFolderStruct(localFolder)
		self.getFolderStruct.start()
		self.getFolderStruct.finished.connect(self._updateFolderStruct)

	#def updateFolderStruct

	def _updateFolderStruct(self):

		self.errorGetFolder=Bridge.onedriveMan.errorFolder
		self._insertModelEntries()
		self.closePopUp=[True,""]
		self.showFolderStruct=True
		if self.errorGetFolder:
			self.showSynchronizeMessage=[True,CHANGE_SYNC_FOLDERS_ERROR,"Error"]

	#def _updateFolderStruct

	@Slot('QVariantList')
	def folderChecked(self,info):

		Bridge.onedriveMan.updateCheckFolder(info[0],info[1])
		path=info[0]
		if info[1]:
			if path not in self.initialSyncConfig[1]:
				self.initialSyncConfig[1].append(path)
			if path in self.initialSyncConfig[2]:
				self.initialSyncConfig[2].remove(path)
		else:
			if path not in self.initialSyncConfig[2]:
				self.initialSyncConfig[2].append(path)
			if path in self.initialSyncConfig[1]:
				self.initialSyncConfig[1].remove(path)

		if None in self.initialSyncConfig[1]:
			self.initialSyncConfig[1].remove(None)
		self.initialSyncConfig[1].sort()
		if None in self.initialSyncConfig[2]:
			self.initialSyncConfig[2].remove(None)
		self.initialSyncConfig[2].sort()
		if None in Bridge.onedriveMan.currentSyncConfig[1]:
			Bridge.onedriveMan.currentSyncConfig[1].remove(None)
		Bridge.onedriveMan.currentSyncConfig[1].sort()
		if None in Bridge.onedriveMan.currentSyncConfig[2]:
			Bridge.onedriveMan.currentSyncConfig[2].remove(None)
		Bridge.onedriveMan.currentSyncConfig[2].sort()

		if self.initialSyncConfig[1]!=Bridge.onedriveMan.currentSyncConfig[1]:
			self.syncCustomChanged=True
		else:
			if self.initialSyncConfig[2]!=Bridge.onedriveMan.currentSyncConfig[2]:
				self.syncCustomChanged=True
			else:
				self.syncCustomChanged=False

	#def folderChecked

	@Slot(int,result='QVariant')
	def getModelData(self,index):
		
		return self.folderEntries[index]

	#def getModelData

	@Slot('QVariantList')
	def updateModel(self,info):
		
		index = self._folderModel.index(info[0])
		self._folderModel.setData(index,info[1],info[2])
	
	#def updateModel

	def _insertModelEntries(self):

		ret=self._folderModel.resetModel()
		entries=Bridge.onedriveMan.folderStruct
		for item in entries:
			self._folderModel.appendRow(item["path"],item["name"],item["isChecked"],item["isExpanded"],item["type"],item["subtype"],item["hide"],item["level"],item["canExpanded"],item["parentPath"])

	#def _insertModelEntries

	@Slot(bool)
	def getSyncMode(self,value):

		self.hideSynchronizeMessage()

		if value!=self.initialSyncConfig[0]:
			if value!=Bridge.onedriveMan.currentSyncConfig[0]:
				if not value and (len(self.initialSyncConfig[1])>0 or len(self.initialSyncConfig[2])>0):
					self.syncCustomChanged=True
				else:
					if value:
						self.syncCustomChanged=True
					else:
						self.syncCustomChanged=False
			else:
				self.syncCustomChanged=False

			self.syncAll=value
			self.initialSyncConfig[0]=value
		else:
			self.syncCustomChanged=False

		if not value:
			if self._folderModel.rowCount()<2:
				self.updateFolderStruct(True)
			else:
				self.showFolderStruct=True
		else:
			self.showFolderStruct=False

	#def getSyncModel 
	
	@Slot()
	def applySyncBtn(self):
		self.showSynchronizeDialog=True

	#def applySyncBtn

	@Slot()
	def cancelSyncChanges(self):
		
		self.closePopUp=[False,SPACE_FOLDER_RESTORE_MESSAGE]
		
		self.syncCustomChanged=False
		self.initialSyncConfig=copy.deepcopy(Bridge.onedriveMan.currentSyncConfig)
		Bridge.onedriveMan.cancelSyncChanges()
		self.syncAll=self.initialSyncConfig[0]
		if self.syncAll:
			self.showFolderStruct=False
		else:
			self.showFolderStruct=True

		self._insertModelEntries()

		index = self._folderModel.index(0)
		self._folderModel.setData(index,"isChecked",True)

		self.closePopUp=[True,""]
	
	#def cancelSyncChanges

	@Slot(str)
	def manageSynchronizeDialog(self,action):

		if action=="Accept":
			self.keepFolders=False
			self.applySyncChanges()
		elif action=="Keep":
			self.keepFolders=True
			self.applySyncChanges()
		elif action=="Cancel":
			pass		
		self.showSynchronizeDialog=False

	#def manageSynchronizeDialog

	@Slot(str)
	def manageSynchronizePendingDialog(self,action):

		if action=="Accept":
			self.showSynchronizePendingDialog=False
			self.showSynchronizeDialog=True
			#self.applySyncChanges()
		elif action=="Discard":
			self.showSynchronizePendingDialog=False
			self.cancelSyncChanges()
		elif action=="Cancel":
			self.showSynchronizePendingDialog=False

	#def manageSynchronizePendingDialog
	
	def applySyncChanges(self):

		self.showSynchronizeMessage=[False,CHANGE_SYNC_OPTIONS_OK,"Information"]
		self.closePopUp=[False,APPLY_SPACE_CHANGES_MESSAGE]
		self.closeGui=False
		self.changedSyncWorked=True
		self.applySynChangesT=ApplySyncChanges(self.initialSyncConfig,self.keepFolders)
		self.applySynChangesT.start()
		self.applySynChangesT.finished.connect(self._applySyncChanges)

	#def applySyncChanges

	def _applySyncChanges(self):

		self.initialSyncConfig=copy.deepcopy(Bridge.onedriveMan.currentSyncConfig)
		self.syncAll=self.initialSyncConfig[0]
		self.closePopUp=[True,""]
		self.showFolderStruct!=self.syncAll

		if self.applySynChangesT.ret:
			self.showSynchronizeMessage=[True,CHANGE_SYNC_OPTIONS_OK,"Ok"]
			self.closeGui=True
			self.syncCustomChanged=False
		else:
			self.showSynchronizeMessage=[True,CHANGE_SYNC_OPTIONS_ERROR,"Error"]
			self.moveToOption=""
			self.moveToStack=""

		self._manageGoToStack()

	#def _applySyncChanges		

	def _manageGoToStack(self):

		if self.moveToOption!="":
			self.manageCurrentOption=self.moveToOption
			self.moveToOption=""
			self.showSettingsMessage=[False,'']
		elif self.moveToStack!="":
			self.currentStack=self.moveToStack
			self.spacesCurrentOption=0
			self.manageCurrentOption=0
			self.moveToStack=""
			try:
				self.checkSpaceLocalFolderTimer.stop()
			except:
				pass

	#def _manageGoToStack

	@Slot()
	def hideSynchronizeMessage(self):

		if not self.isOnedriveRunning and not self.errorGetFolder:
			self.showSynchronizeMessage=[False,DISABLE_SYNC_OPTIONS,"Information"]
			self.changedSyncWorked=False

	#def hideSynchronizeMessage		

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

	@Slot('QVariantList')
	def getSkipSize(self,value):

		if value!=self.initialConfig[3]:
			if value!=Bridge.onedriveMan.currentConfig[3]:
				self.settingsChanged=True
			else:
				self.settingsChanged=False
			self.skipSize=value
			self.initialConfig[3]=value
		else:
			self.settingsChanged=False

	#def getSkipSize

	@Slot(bool)
	def getLogEnabled(self,value):

		if value!=self.initialConfig[3]:
			if value!=Bridge.onedriveMan.currentConfig[4]:
				self.settingsChanged=True
			else:
				self.settingsChanged=False
			self.initialConfig[4]=value
			self.logEnabled=value
		else:
			self.settingsChanged=False

	#def getLogEnabled

	@Slot()
	def applySettingsChanges(self):

		self.showSettingsMessage=[False,'']
		self.closePopUp=[False,APPLY_SPACE_CHANGES_MESSAGE]
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
			self.closeGui=True
			self.settingsChanged=False
		else:
			self.moveToOption=""
			self.moveToStack=""

		self._manageGoToStack()

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
		self.skipSize=self.initialConfig[3]

		self._manageGoToStack()

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
	def testOnedrive(self):

		self.closePopUp=[False,SPACE_RUNNING_TEST_MESSAGE]
		self.testOnedriveT=TestOneDrive()
		self.testOnedriveT.start()
		self.testOnedriveT.finished.connect(self._testOnedrive)

	#def testOnedrive
	
	def _testOnedrive(self):

		if os.path.exists(Bridge.onedriveMan.testPath):
			cmd="xdg-open %s"%Bridge.onedriveMan.testPath
			os.system(cmd)
		self.closePopUp=[True,""]

	#def _testOnedrive

	@Slot()
	def repairOnedrive(self):

		self.closePopUp=[False,SPACE_RUNNING_REPAIR_MESSAGE]
		self.repairOneDriveT=RepairOneDrive()
		self.repairOneDriveT.start()
		self.repairOneDriveT.finished.connect(self._repairOnedrive)

	#def reparirOnedrive

	def _repairOnedrive(self):

		self.checkAccountStatus()

	#def _repairOnedrive

	@Slot()
	def updateAuth(self):

		self.authUrl=self.loginUrl+self.spaceBasicInfo[0]
		self.updateSpaceAuth=True
		self.manageCurrentOption=4

	#def updateAuth

	def updateSpaceAuthorization(self):

		ret=Bridge.onedriveMan.updateSpaceAuth()
		
		if ret:
			self.showToolsMessage=[True,UPDATE_TOKEN_MESSAGE,"Ok"]
		else:
			self.showToolsMessage=[True,UPDATE_TOKEN_ERROR,"Error"]
		
	#def updateSpaceAuthorization

	@Slot()
	def openSpaceLogFile(self):

		if os.path.exists(Bridge.onedriveMan.logPath):
			cmd="xdg-open %s"%Bridge.onedriveMan.logPath
			os.system(cmd)

	#def openSpaceLogFile

	@Slot()
	def removeLogFile(self):

		if os.path.exists(Bridge.onedriveMan.logPath):
			os.remove(Bridge.onedriveMan.logPath)

		self.logSize=Bridge.onedriveMan.getLogFileSize()

	#def removeLogFile

	def getGlobalLocalFolderInfo(self):

		Bridge.onedriveMan.updateGlobalLocalFolderInfo()
		self._updateSpacesModelInfo('localFolderWarning')	
		self._updateSpacesModelInfo('isRunning')	
		self._manageSpaceSettinsMessage()

	#def getGlobalLocalFolderInfo

	def getGlobalStatusInfo(self):

		localStatusWarning=Bridge.onedriveMan.updateGlobalStatusInfo()
		self._updateSpacesModelInfo('status')	
		self._manageSpaceSettinsMessage()

	#def getGlobalStatusInfo

	def _manageSpaceSettinsMessage(self):

		if self.waitForUpdateGlobalMessage==10:
			if len(Bridge.onedriveMan.onedriveConfig)>0:
				if Bridge.onedriveMan.globalOneDriveFolderWarning or Bridge.onedriveMan.globalOneDriveStatusWarning:
					self.showSpaceSettingsMessage=[True,SPACE_GLOBAL_WARNING,"Warning"]
				else:
					hddAlert=Bridge.onedriveMan.checkHddFreeSpace()
					if hddAlert[0]:
						self.showSpaceSettingsMessage=[True,hddAlert[1],hddAlert[2]]
					else:
						self.showSpaceSettingsMessage=[False,"","Information"]
			else:
				self.showSpaceSettingsMessage=[False,"","Information"]
		else:
			self.waitForUpdateGlobalMessage=self.waitForUpdateGlobalMessage+1

	#def _manageSpaceSettingsMessage

	def checkSpaceLocalFolder(self):

		self.isOnedriveRunning=Bridge.onedriveMan.isOnedriveRunning()
		
		if self.isOnedriveRunning:
			self.showSynchronizeMessage=[True,DISABLE_SYNC_OPTIONS,"Information"]
			if not self.updateSpaceAuth:
				self.showToolsMessage=[True,TOOLS_DEFAULT_MESSAGE,"Information"]
		else:
			if not self.updateSpaceAuth:
				self.showToolsMessage=[False,TOOLS_DEFAULT_MESSAGE,"Information"]
			if not self.changedSyncWorked:
				self.showSynchronizeMessage=[False,DISABLE_SYNC_OPTIONS,"Information"]

		self.localFolderEmpty,self.localFolderRemoved=Bridge.onedriveMan.checkLocalFolder(Bridge.onedriveMan.spaceConfPath)
	
		if self.localFolderEmpty:
			self.showAccountMessage=[True,LOCAL_FOLDER_EMPTY,"Error"]
		else:
			if self.localFolderRemoved:
				self.showAccountMessage=[True,LOCAL_FOLDER_REMOVED,"Error"]
			else:
				self.showAccountMessage=[False,"","Error"]

	#def checkSpaceLocalFolder

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

		Bridge.onedriveMan.deleteTempConfig()

		if not self.removeAction:
			if self.settingsChanged:
				self.closeGui=False
				self.showSettingsDialog=True
			else:
				if self.syncCustomChanged:
					self.closeGui=False
					if self.closePopUp[0]:
						self.showSynchronizePendingDialog=True
				else:
					if self.closePopUp[0]:
						Bridge.onedriveMan.removeLockToken()
						self.closeGui=True
					else:
						self.closeGui=False
		else:
			Bridge.onedriveMan.removeLockToken()
			self.closeGui=True

	#def closeOnedrive
	
	on_currentStack=Signal()
	currentStack=Property(int,_getCurrentStack,_setCurrentStack, notify=on_currentStack)

	on_spacesCurrentOption=Signal()
	spacesCurrentOption=Property(int,_getSpacesCurrentOption,_setSpacesCurrentOption, notify=on_spacesCurrentOption)

	on_authUrl=Signal()
	authUrl=Property(str,_getAuthUrl,_setAuthUrl,notify=on_authUrl)

	on_formData=Signal()
	formData=Property('QVariantList',_getFormData,_setFormData, notify=on_formData)

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

	on_spaceBasicInfo=Signal()
	spaceBasicInfo=Property('QVariantList',_getSpaceBasicInfo,_setSpaceBasicInfo,notify=on_spaceBasicInfo)

	on_spaceLocalFolder=Signal()
	spaceLocalFolder=Property(str,_getSpaceLocalFolder,_setSpaceLocalFolder,notify=on_spaceLocalFolder)
	
	on_autoStartEnabled=Signal()
	autoStartEnabled=Property(bool,_getAutoStartEnabled,_setAutoStartEnabled,notify=on_autoStartEnabled)
	
	on_rateLimit=Signal()
	rateLimit=Property(int,_getRateLimit,_setRateLimit,notify=on_rateLimit)

	on_monitorInterval=Signal()
	monitorInterval=Property(int,_getMonitorInterval,_setMonitorInterval,notify=on_monitorInterval)

	on_skipSize=Signal()
	skipSize=Property('QVariantList',_getSkipSize,_setSkipSize,notify=on_skipSize)
	
	on_logEnabled=Signal()
	logEnabled=Property(bool,_getLogEnabled,_setLogEnabled,notify=on_logEnabled)

	on_logSize=Signal()
	logSize=Property(str,_getLogSize,_setLogSize,notify=on_logSize)
	
	on_freeSpace=Signal()
	freeSpace=Property(str,_getFreeSpace,_setFreeSpace, notify=on_freeSpace)

	on_settingsChanged=Signal()
	settingsChanged=Property(bool,_getSettingsChanged,_setSettingsChanged, notify=on_settingsChanged)

	on_showSettingsMessage=Signal()
	showSettingsMessage=Property('QVariantList',_getShowSettingsMessage,_setShowSettingsMessage,notify=on_showSettingsMessage)
	
	on_showSettingsDialog=Signal()
	showSettingsDialog=Property(bool,_getShowSettingsDialog,_setShowSettingsDialog,notify=on_showSettingsDialog)

	on_syncAll=Signal()
	syncAll=Property(bool,_getSyncAll,_setSyncAll,notify=on_syncAll)

	on_showFolderStruct=Signal()
	showFolderStruct=Property(bool,_getShowFolderStruct,_setShowFolderStruct,notify=on_showFolderStruct)

	on_showSynchronizeMessage=Signal()
	showSynchronizeMessage=Property('QVariantList',_getShowSynchronizeMessage,_setShowSynchronizeMessage,notify=on_showSynchronizeMessage)

	on_showSynchronizeDialog=Signal()
	showSynchronizeDialog=Property(bool,_getShowSynchronizeDialog,_setShowSynchronizeDialog,notify=on_showSynchronizeDialog)

	on_showSynchronizePendingDialog=Signal()
	showSynchronizePendingDialog=Property(bool,_getShowSynchronizePendingDialog,_setShowSynchronizePendingDialog,notify=on_showSynchronizePendingDialog)
	
	on_syncCustomChanged=Signal()
	syncCustomChanged=Property(bool,_getSyncCustomChanged,_setSyncCustomChanged,notify=on_syncCustomChanged)

	on_localFolderEmpty=Signal()
	localFolderEmpty=Property(bool,_getLocalFolderEmpty,_setLocalFolderEmpty,notify=on_localFolderEmpty)

	on_localFolderRemoved=Signal()
	localFolderRemoved=Property(bool,_getLocalFolderRemoved,_setLocalFolderRemoved,notify=on_localFolderRemoved)

	on_isOnedriveRunning=Signal()
	isOnedriveRunning=Property(bool,_getIsOnedriveRunning,_setIsOnedriveRunning, notify=on_isOnedriveRunning)

	on_requiredMigration=Signal()
	requiredMigration=Property(bool,_getRequiredMigration,_setRequiredMigration, notify=on_requiredMigration)

	on_showToolsMessage=Signal()
	showToolsMessage=Property('QVariantList',_getShowToolsMessage,_setShowToolsMessage,notify=on_showToolsMessage)

	on_withHDDSpace=Signal()
	withHDDSpace=Property(bool,_getWithHDDSpace,_setWithHDDSpace,notify=on_withHDDSpace)
	
	spacesModel=Property(QObject,_getSpacesModel,constant=True)
	sharePointModel=Property(QObject,_getSharePointModel,constant=True)
	libraryModel=Property(QObject,_getLibraryModel,constant=True)
	bandWidthNames=Property('QVariant',_getBandWidthNames,constant=True)
	maxFileSizeNames=Property('QVariant',_getMaxFileSizeNames,constant=True)
	folderModel=Property(QObject,_getFolderModel,constant=True)

#class Bridge

if __name__=="__main__":

	pass
