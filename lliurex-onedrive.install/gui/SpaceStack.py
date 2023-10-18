from PySide2.QtCore import QObject,Signal,Slot,QThread,Property,QTimer,Qt,QModelIndex
import os 
import sys
import threading
import time
import copy

import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)


SPACE_LOADING_SETTINGS=3
DISABLE_SYNC_OPTIONS=4
START_SYNC_MESSAGE=6
STOP_SYNC_MESSAGE=7
CHECKING_STATUS_MESSAGE=8
REMOVE_SPACE_MESSAGE=9
TOOLS_DEFAULT_MESSAGE=18
SPACE_MIGRATION_SUCCESS=20

START_SYNCHRONIZATION_ERROR=-10
STOP_SYNCHRONIZATION_ERROR=-11
LOCAL_FOLDER_EMPTY=-12
LOCAL_FOLDER_REMOVED=-13


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

class Bridge(QObject):

	def __init__(self,ticket=None):

		QObject.__init__(self)

		self.core=Core.Core.get_core()
		Bridge.onedriveMan=self.core.onedrivemanager
		self._showAccountMessage=[False,"","Error"]
		self._manageCurrentOption=0
		self._spaceBasicInfo=["","","","",""]
		self._spaceLocalFolder=""
		self._isOnedriveRunning=False
		self._accountStatus=0
		self._freeSpace=""
		self.initStartUp=False
		self.moveToStack=""
		self.moveToOption=""
		self._localFolderEmpty=False
		self._localFolderRemoved=False
		self.removeAction=False

	#def __init__
	
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
	
	def _getFreeSpace(self):

		return self._freeSpace

	#def _getFreeSpace	

	def _setFreeSpace(self,freeSpace):
		
		if self._freeSpace!=freeSpace:
			self._freeSpace=freeSpace
			self.on_freeSpace.emit()	
	
	#def _setFreeSpace

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

	@Slot(int)
	def moveToManageOption(self,option):
		
		if self.manageCurrentOption!=option:
			self.moveToOption=option
			self.core.settingsStack.showSettingsMessage=[False,'']
			self.core.toolStack.updateSpaceAuth=False
			if self.core.settingsStack.settingsChanged:
				self.core.settingsStack.showSettingsDialog=True
			elif self.core.syncStack.syncCustomChanged:
				self.core.syncStack.showSynchronizePendingDialog=True
			elif self.core.syncStack.skipFileChanged:
				self.core.syncStack.showSynchronizePendingDialog=True
			else:
				self.manageCurrentOption=option
				self.moveToOption=""

	#def moveToManageOption

	def _initialStartUp(self):

		self.initStartUp=True
		
		self.core.mainStack.closePopUp=[False,START_SYNC_MESSAGE]
		self.manageSyncT=ManageSync(True)
		self.manageSyncT.start()
		self.manageSyncT.finished.connect(self._endInitialStartUp)
		
	#def _initialStartUp

	def _endInitialStartUp(self):

		self.isOnedriveRunning=self.manageSyncT.ret[1]

		if not self.isOnedriveRunning:
			self.showAccountMessage=[True,START_SYNCHRONIZATION_ERROR,"Error"]
			self.core.mainStack.currentStack=2
			self.manageCurrentOption=0
			self.core.mainStack.spacesCurrentOption=0
			self.core.mainStack.closePopUp=[True,""]
			self.core.mainStack.closeGui=True

		else:
			self.core.mainStack._updateSpacesModelInfo('isRunning')
			self.checkAccountStatus()

	#def _endInitialStartUp
	
	@Slot(str)
	def loadSpace(self,idSpace):

		self.core.mainStack.closePopUp=[False,SPACE_LOADING_SETTINGS]
		self.core.mainStack.closeGui=False
		self.getSpaceSettings=GatherSpaceSettings(idSpace)
		self.getSpaceSettings.start()
		self.getSpaceSettings.finished.connect(self._loadSpace)

	#def loadSpace

	def _loadSpace(self):

		if self.getSpaceSettings.matchSpace:
			self._initializeVars()
			self.core.settingsStack._getInitialSettings()
	
			if not self.localFolderRemoved:
				if not self.core.syncStack.syncAll:
					if not self.localFolderEmpty:
						self.core.syncStack.gatherFolderStruct()
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
				self.core.toolStack.showToolsMessage=[True,TOOLS_DEFAULT_MESSAGE,"Information"]
			else:
				self.core.toolStack.showToolsMessage=[False,TOOLS_DEFAULT_MESSAGE,"Information"]
		else:
			self.core.mainStack.closePopUp=[True,""]
			self.core.mainStack.closeGui=True
			self.core.mainStack.currentStack=1

	#def _loadAccount

	def _endLoading(self):

		if not self.core.syncStack.syncAll:
			self.core.syncStack._updateFolderStruct()
		else:
			self.core.syncStack._folderModel.resetModel()
			self.core.syncStack.showFolderStruct=False
			
		self.core.syncStack._updateFileExtensionsModel()
		
		if self.isOnedriveRunning:
			self.core.syncStack.showSynchronizeMessage=[True,DISABLE_SYNC_OPTIONS,"Information"]
		else:
			self.core.syncStack.showSynchronizeMessage=[False,DISABLE_SYNC_OPTIONS,"Information"]
		
		self.checkSpaceLocalFolderTimer=QTimer(None)
		self.checkSpaceLocalFolderTimer.timeout.connect(self.checkSpaceLocalFolder)
		self.checkSpaceLocalFolderTimer.start(5000)

		self.core.mainStack.closePopUp=[True,""]
		self.core.mainStack.closeGui=True

		if self.core.mainStack.requiredMigration:
			self.showAccountMessage=[True,SPACE_MIGRATION_SUCCESS,"OK"]
			self.core.mainStack.requiredMigration=False
			self.core.mainStack.spacesCurrentOption=0

		self.core.mainStack.currentStack=2
		self.manageCurrentOption=0
	
	#def _endLoading

	def _initializeVars(self):

		self.spaceBasicInfo=Bridge.onedriveMan.spaceBasicInfo
		self.spaceLocalFolder=os.path.basename(Bridge.onedriveMan.spaceLocalFolder)
		self.core.syncStack.syncAll=Bridge.onedriveMan.syncAll
		self.core.syncStack.initialSyncConfig=copy.deepcopy(Bridge.onedriveMan.currentSyncConfig)
		self.isOnedriveRunning=Bridge.onedriveMan.isOnedriveRunning()
		self.localFolderEmpty=Bridge.onedriveMan.localFolderEmpty
		self.localFolderRemoved=Bridge.onedriveMan.localFolderRemoved
		self.showAccountMessage=[False,"","Error"]
		self.accountStatus=Bridge.onedriveMan.accountStatus
		self.freeSpace=Bridge.onedriveMan.freeSpace
		self.core.syncStack._folderModel.resetModel()
		self.core.syncStack.skipFileExtensions=copy.deepcopy(Bridge.onedriveMan.currentSyncConfig[3])

	#def _initializeVars

	@Slot()
	def goHome(self):

		self.core.toolStack.updateSpaceAuth=False
		if not self.core.settingsStack.settingsChanged and not self.core.syncStack.syncCustomChanged and not self.core.syncStack.skipFileChanged:
			self.core.mainStack.currentStack=1
			self.core.mainStack.spacesCurrentOption=0
			self.manageCurrentOption=0
			self.moveToStack=""
			try:
				self.checkSpaceLocalFolderTimer.stop()
			except:
				pass
		else:
			self.moveToStack=1
			if self.core.settingsStack.settingsChanged:
				self.core.settingsStack.showSettingsDialog=True
			else:
				self.core.syncStack.showSynchronizePendingDialog=True

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

		self.core.mainStack.closePopup=[False,msg]
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
			self.core.mainStack._updateSpacesModelInfo('isRunning')
		
		self.isOnedriveRunning=self.manageSyncT.ret[1]
		if self.isOnedriveRunning:
			self.core.syncStack.showSynchronizeMessage=[True,DISABLE_SYNC_OPTIONS,"Information"]
		else:
			self.core.syncStack.showSynchronizeMessage=[False,DISABLE_SYNC_OPTIONS,"Information"]

		self.core.mainStack.closePopUp=[True,""]
	
	#def _manageSync

	@Slot()
	def checkAccountStatus(self):

		if not self.initStartUp:
			self.core.mainStack.closePopUp=[False,CHECKING_STATUS_MESSAGE]
		self.getAccountStatus=AccountStatus()
		self.getAccountStatus.start()
		self.getAccountStatus.finished.connect(self._checkAccountStatus)

	#def checkAccountStatus

	def _checkAccountStatus(self):

		if self.initStartUp:
			self.core.syncStack.showSynchronizeMessage=[True,DISABLE_SYNC_OPTIONS,"Information"]
			self.core.mainStack.currentStack=2
			self.manageCurrentOption=0
			self.core.mainStack.spacesCurrentOption=0
			self.initStartUp=False
			if self.isOnedriveRunning:
				self.core.toolStack.showToolsMessage=[True,TOOLS_DEFAULT_MESSAGE,"Information"]

		self.core.mainStack.closePopUp=[True,""]
		self.core.mainStack.closeGui=True
		self.core.mainStack._updateSpacesModelInfo("status")
		self.accountStatus=self.getAccountStatus.ret[1]
		self.freeSpace=self.getAccountStatus.ret[2]

	#def _checkAccountStatus 

	@Slot()
	def removeAccount(self):

		self.core.mainStack.closePopUp=[False,REMOVE_SPACE_MESSAGE]
		self.core.mainStack.closeGui=False
		self.removeAccountT=RemoveAccount()
		self.removeAccountT.start()
		self.removeAccountT.finished.connect(self._removeAccount)

	#def removeAccount

	def _removeAccount(self):

		if self.removeAccountT.ret:
			self.core.mainStack._updateSpacesModel()
			Bridge.onedriveMan.removeOrganizationDirectoryFile()
			self.core.mainStack.currentStack=1
			self.core.mainStack.spacesCurrentOption=0
			self.manageCurrentOption=0
			self.removeAction=True
		else:
			self.showAccountMessage=[True,STOP_SYNCHRONIZATION_ERROR,"Error"]	
	
		self.core.mainStack.closePopUp=[True,""]
		self.core.mainStack.closeGui=True

	#def _removeAccount

	def _manageGoToStack(self):

		if self.moveToOption!="":
			self.manageCurrentOption=self.moveToOption
			self.moveToOption=""
			self.core.settingsStack.showSettingsMessage=[False,'']
		elif self.moveToStack!="":
			self.core.mainStack.currentStack=self.moveToStack
			self.core.mainStack.spacesCurrentOption=0
			self.manageCurrentOption=0
			self.moveToStack=""
			try:
				self.checkSpaceLocalFolderTimer.stop()
			except:
				pass

	#def _manageGoToStack

	def checkSpaceLocalFolder(self):

		self.isOnedriveRunning=Bridge.onedriveMan.isOnedriveRunning()
		
		if self.isOnedriveRunning:
			self.core.syncStack.showSynchronizeMessage=[True,DISABLE_SYNC_OPTIONS,"Information"]
			if not self.core.toolStack.updateSpaceAuth:
				self.core.toolStackshowToolsMessage=[True,TOOLS_DEFAULT_MESSAGE,"Information"]
		else:
			if not self.core.toolStack.updateSpaceAuth:
				self.core.toolStack.showToolsMessage=[False,TOOLS_DEFAULT_MESSAGE,"Information"]
			if not self.core.syncStack.changedSyncWorked:
				self.core.syncStack.showSynchronizeMessage=[False,DISABLE_SYNC_OPTIONS,"Information"]

		self.localFolderEmpty,self.localFolderRemoved=Bridge.onedriveMan.checkLocalFolder(Bridge.onedriveMan.spaceConfPath)
	
		if self.localFolderEmpty:
			self.showAccountMessage=[True,LOCAL_FOLDER_EMPTY,"Error"]
		else:
			if self.localFolderRemoved:
				self.showAccountMessage=[True,LOCAL_FOLDER_REMOVED,"Error"]
			else:
				self.showAccountMessage=[False,"","Error"]

	#def checkSpaceLocalFolder

	on_accountStatus=Signal()
	accountStatus=Property(int,_getAccountStatus,_setAccountStatus, notify=on_accountStatus)

	on_freeSpace=Signal()
	freeSpace=Property(str,_getFreeSpace,_setFreeSpace, notify=on_freeSpace)

	on_showAccountMessage=Signal()
	showAccountMessage=Property('QVariantList',_getShowAccountMessage,_setShowAccountMessage,notify=on_showAccountMessage)

	on_manageCurrentOption=Signal()
	manageCurrentOption=Property(int,_getManageCurrentOption,_setManageCurrentOption, notify=on_manageCurrentOption)

	on_spaceBasicInfo=Signal()
	spaceBasicInfo=Property('QVariantList',_getSpaceBasicInfo,_setSpaceBasicInfo,notify=on_spaceBasicInfo)

	on_spaceLocalFolder=Signal()
	spaceLocalFolder=Property(str,_getSpaceLocalFolder,_setSpaceLocalFolder,notify=on_spaceLocalFolder)
	
	on_freeSpace=Signal()
	freeSpace=Property(str,_getFreeSpace,_setFreeSpace, notify=on_freeSpace)

	on_localFolderEmpty=Signal()
	localFolderEmpty=Property(bool,_getLocalFolderEmpty,_setLocalFolderEmpty,notify=on_localFolderEmpty)

	on_localFolderRemoved=Signal()
	localFolderRemoved=Property(bool,_getLocalFolderRemoved,_setLocalFolderRemoved,notify=on_localFolderRemoved)

	on_isOnedriveRunning=Signal()
	isOnedriveRunning=Property(bool,_getIsOnedriveRunning,_setIsOnedriveRunning, notify=on_isOnedriveRunning)

#class Bridge

import Core
