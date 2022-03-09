from PySide2.QtCore import QObject,Signal,Slot,QThread,Property,QTimer,Qt,QModelIndex
import os 
import OnedriveManager
import sys
import threading
import time
import copy
import Model

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

class CreateAccount(QThread):

	def __init__(self,*args):
		
		QThread.__init__(self)
		self.ret=[]
		self.initialDownload=""

	#def __init__

	def run (self,*args):
		
		self.ret=Bridge.onedriveMan.createAccount()
		if self.ret:
			if Bridge.onedriveMan.isConfigured():
				self.initialDownload=Bridge.onedriveMan.getInitialDownload()

	#def run

#class CreateAccount

class GatherInfo(QThread):

	def __init__(self,*args):
		
		QThread.__init__(self)
		self.isOnedriveRunning=False
		self.localFolderEmpty=False
		self.localFolderRemoved=False
		self.accountStatus=1
		self.freeSpace=""

	#def _init__

	def run(self,*args):
		
		time.sleep(1)
		Bridge.onedriveMan.loadConfg()
		self.isOnedriveRunning=Bridge.onedriveMan.isOnedriveRunning()
		self.localFolderEmpty,self.localFolderRemoved=Bridge.onedriveMan.checkLocalFolder()
		if not self.localFolderRemoved:
			error,self.accountStatus,self.freeSpace=Bridge.onedriveMan.getAccountStatus()

	#def run

#class GatherInfo

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

class ApplySettingsChanges(QThread):

	def __init__(self,*args):

		QThread.__init__(self)
		self.ret=[]
		self.initialConfig=args[0]
	
	#def __init

	def run(self,*args):

		self.ret=Bridge.onedriveMan.applyChanges(self.initialConfig)

	#def run

#class ApplySettingsChanges

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

class RemoveAccount(QThread):

	def __init__(self,*args):

		QThread.__init__(self)
		self.ret=[]

	#def __init

	def run(self,*args):

		self.ret=Bridge.onedriveMan.removeAccount()

	#def run

#class RemoveAccount

class Bridge(QObject):

	onedriveMan=OnedriveManager.OnedriveManager()

	def __init__(self,ticket=None):

		QObject.__init__(self)

		self.entries=[{"path":"OneDrive", "name": "OneDrive","isChecked":True, "isExpanded": True,"type":"parent","subtype":"root","hide":False,"level":1,"canExpanded":True,"parentPath":""}]
		self._model=Model.MyModel(self.entries)
		self._isConfigured=Bridge.onedriveMan.isConfigured()
		self._autoStartEnabled=Bridge.onedriveMan.autoStartEnabled
		self._monitorInterval=int(Bridge.onedriveMan.monitorInterval)
		self._rateLimit=int(Bridge.onedriveMan.rateLimit)	
		self._userFolder=Bridge.onedriveMan.userFolder
		self._currentStack=1
		self._closeGui=False
		self._closePopUp=True
		self._showSettingsDialog=False
		self._isOnedriveRunning=False
		self._accountStatus=1
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
		self.removeAction=False
		self.initStartUp=False
		self.initBridge()

	#def _init__

	def initBridge(self):

		if self._isConfigured:
			self.isClientRunningTimer=QTimer(None)
			self.isClientRunningTimer.timeout.connect(self.updateClientStatus)
			self.isClientRunningTimer.start(5000)
			self.currentStack=1
			self.gatherInfo=GatherInfo()
			self.gatherInfo.start()
			self.gatherInfo.finished.connect(self._loadAccount)
		else:
			self.currentStack=0
			if Bridge.onedriveMan.checkPreviousLocalFolder():
				self.showPreviousDialog=True
	
	#def initBridge
	
	def _loadAccount(self):

		self._getInitialSettings()
		self.syncAll=Bridge.onedriveMan.syncAll
		self.initialSyncConfig=copy.deepcopy(Bridge.onedriveMan.currentSyncConfig)
		self.isOnedriveRunning=self.gatherInfo.isOnedriveRunning
		self.localFolderEmpty=self.gatherInfo.localFolderEmpty
		self.localFolderRemoved=self.gatherInfo.localFolderRemoved

		if not self.localFolderRemoved:
			self.accountStatus=self.gatherInfo.accountStatus
			self.freeSpace=self.gatherInfo.freeSpace
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

		self.currentStack=2	
	
	#def _endLoading

	def _getInitialSettings(self):

		self.autoStartEnabled=Bridge.onedriveMan.autoStartEnabled
		self.monitorInterval=int(Bridge.onedriveMan.monitorInterval)
		self.rateLimit=int(Bridge.onedriveMan.rateLimit)
		self.initialConfig=copy.deepcopy(Bridge.onedriveMan.currentConfig)

	#def _getInitialConfig

	def _getBandWidthNames(self):
		
		return self._bandWidthNames

	#def _getBandWidthNames

	def _getUserFolder(self):
		
		return self._userFolder

	#def _getUserFolder

	def _getIsConfigured(self):

		return self._isConfigured

	#def _getIsConfigured

	def _getAutoStartEnabled(self):
		
		return self._autoStartEnabled

	#def _getAutoStartEnabled

	def _setAutoStartEnabled(self,autoStartEnabled):

		self._autoStartEnabled=autoStartEnabled
		self.on_autoStartEnabled.emit()

	#def _setAutoStartEnabled

	def _getRateLimit(self):

		return self._rateLimit

	#def _getRateLimit

	def _setRateLimit(self,rateLimit):

		self._rateLimit=int(rateLimit)
		self.on_rateLimit.emit()

	#def _setRateLimit

	def _getMonitorInterval(self):
		
		return self._monitorInterval

	#def _getMonitorInterval

	def _setMonitorInterval(self,monitorInterval):

		self._monitorInterval=int(monitorInterval)
		self.on_monitorInterval.emit()

	#def _setMonitorInterval
	
	def _getCurrentStack(self):

		return self._currentStack

	#def _getCurrentStack	

	def _setCurrentStack(self,currentStack):
		
		self._currentStack=currentStack
		self.on_currentStack.emit()

	#def _setCurentStack

	def _getClosePopUp(self):

		return self._closePopUp

	#def _getClosePopUp	

	def _setClosePopUp(self,closePopUp):
		
		self._closePopUp=closePopUp
		self.on_closePopUp.emit()

	#def _setClosePopUp	

	def _getCloseGui(self):

		return self._closeGui

	#def _getCloseGui	

	def _setCloseGui(self,closeGui):
		
		self._closeGui=closeGui
		self.on_closeGui.emit()

	#def _setCloseGui					

	def _getIsOnedriveRunning(self):

		return self._isOnedriveRunning

	#def _getIsOnedriveRunning	

	def _setIsOnedriveRunning(self,isOnedriveRunning):
		
		if self._isOnedriveRunning!=isOnedriveRunning:
			self._isOnedriveRunning=isOnedriveRunning
			self.on_isOnedriveRunning.emit()	

	#def _setIsOnedriveRunning
	
	def _getAccountStatus(self):

		return self._accountStatus

	#def _getAccountStatus	

	def _setAccountStatus(self,accountStatus):
		
		self._accountStatus=accountStatus
		self.on_accountStatus.emit()	

	#def _setAccountStatus 

	def _getFreeSpace(self):

		return self._freeSpace

	#def _getFreeSpace	

	def _setFreeSpace(self,freeSpace):
		
		self._freeSpace=freeSpace
		self.on_freeSpace.emit()	
	
	#def _setFreeSpace

	def _getSettingsChanged(self):

		return self._settingsChanged

	#def _getSettingsChanged

	def _setSettingsChanged(self,settingsChanged):

		self._settingsChanged=settingsChanged
		self.on_settingsChanged.emit()

	#def _setSettingsChanged

	def _getShowSettingsMessage(self):

		return self._showSettingsMessage

	#def _getShowSettingsMessage
	
	def _setShowSettingsMessage(self,showSettingsMessage):

		self._showSettingsMessage=showSettingsMessage
		self.on_showSettingsMessage.emit()

	#def _setShowSettingsMessage

	def _getShowSettingsDialog(self):

		return self._showSettingsDialog

	#def _getShowSettingsDialog
	
	def _setShowSettingsDialog(self,showSettingsDialog):

		self._showSettingsDialog=showSettingsDialog
		self.on_showSettingsDialog.emit()

	#def _setShowSettingsDialog

	def _getShowUnlinkDialog(self):

		return self._showUnlinkDialog

	#def _getShowUnlinkDialog
	
	def _setShowUnlinkDialog(self,showUnlinkDialog):

		self._showUnlinkDialog=showUnlinkDialog
		self.on_showUnlinkDialog.emit()

	#def _setShowUnlinkDialog

	def _getInfoStackType(self):

		return self._infoStackType

	#def _getInfoStackType

	def _setInfoStackType(self,infoStackType):

		self._infoStackType=infoStackType
		self.on_infoStackType.emit()

	#def _setInfoStackType

	def _getShowAccountMessage(self):

		return self._showAccountMessage

	#def _getShowAccountMessage

	def _setShowAccountMessage(self,showAccountMessage):

		if self._showAccountMessage!=showAccountMessage:
			self._showAccountMessage=showAccountMessage	
			self.on_showAccountMessage.emit()

	#def _setShowAccountMessage

	def _getModel(self):
		return self._model

	#def _getModel

	def _getShowSynchronizeDialog(self):

		return self._showSynchronizeDialog

	#def _getShowSynchronizeDialog
	
	def _setShowSynchronizeDialog(self,showSynchronizeDialog):

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

		self._syncAll=syncAll
		self.on_syncAll.emit()

	#def _setSyncAll	

	def _getSyncCustomChanged(self):

		return self._syncCustomChanged

	#def _getSyncCustomChanged

	def _setSyncCustomChanged(self,syncCustomChanged):

		self._syncCustomChanged=syncCustomChanged
		self.on_syncCustomChanged.emit()

	#def _setSyncCustomChanged

	def _getInitialDownload(self):

		return self._initialDownload

	#def _getInitialDownload	

	def _setInitialDownload(self,initialDownload):
		
		self._initialDownload=initialDownload
		self.on_initialDownload.emit()

	#def _setInitialDownload

	def _getHddFreeSpace(self):

		return self._hddFreeSpace

	#def _getHddFreeSpace	

	def _setHddFreeSpace(self,hddFreeSpace):
		
		self._hddFreeSpace=hddFreeSpace
		self.on_hddFreeSpace.emit()

	#def _setHddFreeSpace

	
	def _getShowDownloadDialog(self):

		return self._showDownloadDialog
	
	#def _getShowDownloadDialog

	def _setShowDownloadDialog(self,showDownloadDialog):

		self._showDownloadDialog=showDownloadDialog
		self.on_showDownloadDialog.emit()

	#def _setShowDownloadDialog
	
	def _getCurrentOptionsStack(self):

		return self._currentOptionsStack
	
	#def _getCurrentOptionsStack

	def _setCurrentOptionsStack(self,currentOptionsStack):

		self._currentOptionsStack=currentOptionsStack
		self.on_currentOptionsStack.emit()

	#def _setCurrentOptionsStack

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

	def _getShowPreviousDialog(self):

		return self._showPreviousDialog
	
	#def _getShowPreviousDialog

	def _setShowPreviousDialog(self,showPreviousDialog):

		self._showPreviousDialog=showPreviousDialog
		self.on_showPreviousDialog.emit()

	#def _setShowPreviousDialog

	@Slot(str)
	def createAccount(self,token):

		Bridge.onedriveMan.authToken=token
		self.currentStack=1
		self.createAccountT=CreateAccount()
		self.createAccountT.start()
		self.createAccountT.finished.connect(self._createAccount)
	
	#def createAccont

	def _createAccount(self):

		if self.createAccountT.ret:
			if Bridge.onedriveMan.isConfigured():
				self._getInitialSettings()
				self.hddFreeSpace=Bridge.onedriveMan.getHddFreeSpace()
				self.initialDownload=self.createAccountT.initialDownload

				if self.initialDownload!="":
					self.showDownloadDialog=True
				else:
					self.currentStack=2
			else:
				self.currentStack=3

		else:
			self.currentStack=3

	#def _createAccount
	
	@Slot(str)
	def manageDownloadDialog(self,option):

		self.showDownloadDialog=False
		if option=="All":
			self._initialStartUp()
		else:
			self.currentOptionsStack=1
			self.currentStack=2

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
		else:
			self.checkAccountStatus()

	#def _endInitialStartUp

	@Slot()
	def checkAccountStatus(self):

		if not self.initStartUp:
			self.closePopUp=False
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
			self.closePopUp=True

		self.accountStatus=self.getAccountStatus.ret[1]
		self.freeSpace=self.getAccountStatus.ret[2]

	#def _checkAccountStatus 

	@Slot(bool)
	def manageAutoStart(self,value):
		
		if value!=self.initialConfig[0]:
			if value!=Bridge.onedriveMan.currentConfig[0]:
				self.settingsChanged=True
			else:
				self.settingsChanged=False
			self.initialConfig[0]=value
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
			self.initialConfig[2]=int(value)
		else:
			self.settingsChanged=False

	#def getRateLimit

	@Slot()
	def applySettingsChanges(self):

		self.closePopUp=False
		self.closeGui=False
		self.applySettingsChangesT=ApplySettingsChanges(self.initialConfig)
		self.applySettingsChangesT.start()
		self.applySettingsChangesT.finished.connect(self._applySettingsChanges)

	#def applySettingsChanges

	def _applySettingsChanges(self):

		self.initialConfig=copy.deepcopy(Bridge.onedriveMan.currentConfig)
		self.closePopUp=True
		self.showSettingsMessage=[True,self.applySettingsChangesT.ret[1]]
		self.showSettingsDialog=False

		if not self.applySettingsChangesT.ret[0]:
			if not self.syncCustomChanged:
				self.closeGui=True
			self.settingsChanged=False

	#def _applySettingsChanges

	@Slot()
	def cancelSettingsChanges(self):

		if not self.syncCustomChanged:
			self.closeGui=True
		
		self.hideSettingsMessage()
		self.settingsChanged=False
		self.showSettingsDialog=False
		self.initialConfig=copy.deepcopy(Bridge.onedriveMan.currentConfig)
		self.autoStartEnabled=self.initialConfig[0]
		self.monitorInterval=int(self.initialConfig[1])
		self.rateLimit=self.initialConfig[2]

	#def cancelSettingsChanges

	@Slot()
	def hideSettingsMessage(self):

		self.showSettingsMessage=[False,'']

	#def hideSettingsMessage

	@Slot(bool)
	def manageSync(self,value):

		self.closePopup=False
		self.isRunningBefore=Bridge.onedriveMan.isOnedriveRunning()
		self.manageSyncT=ManageSync(value)
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


		self.closePopUp=True
	
	#def _manageSync
	
	@Slot()
	def repairOnedrive(self):

		self.closePopUp=False
		self.repairOneDriveT=RepairOneDrive()
		self.repairOneDriveT.start()
		self.repairOneDriveT.finished.connect(self._repairOnedrive)

	#def reparirOnedrive

	def _repairOnedrive(self):

		self.checkAccountStatus()

	#def _repairOnedrive
	
	@Slot()
	def removeAccount(self):

		self.closePopUp=False

		self.showUnlinkDialog=False
		self.removeAccountT=RemoveAccount()
		self.removeAccountT.start()
		self.removeAccountT.finished.connect(self._removeAccount)

	#def removeAccount

	def _removeAccount(self):

		self.closePopUp=True
		if self.removeAccountT.ret:
			self.currentStack=3
			self.infoStackType="Unlink"
			self.removeAction=True
		else:
			self.showAccountMessage=[True,STOP_SYNCHRONIZATION_ERROR]	
	
	#def _removeAccount

	@Slot()
	def openFolder(self):

		self.open_folder_t=threading.Thread(target=self._openFolder)
		self.open_folder_t.daemon=True
		self.open_folder_t.start()

	#def openFolder

	def _openFolder(self):

		cmd="xdg-open "+self._userFolder
		os.system(cmd)

	#def _openFolder

	@Slot()
	def testOnedrive(self):

		self.closePopUp=False
		self.testOnedriveT=TestOneDrive()
		self.testOnedriveT.start()
		self.testOnedriveT.finished.connect(self._testOnedrive)

	#def testOnedrive
	
	def _testOnedrive(self):

		if os.path.exists(Bridge.onedriveMan.testPath):
			cmd="xdg-open %s"%Bridge.onedriveMan.testPath
			os.system(cmd)
		self.closePopUp=True

	#def _testOnedrive

	@Slot(str)
	def manageSettingsDialog(self,action):
		
		if action=="Accept":
			self.applySettingsChanges()
		elif action=="Discard":
			self.cancelSettingsChanges()
		elif action=="Cancel":
			self.closeGui=False
			self.showSettingsDialog=False

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

	@Slot(bool)
	def updateFolderStruct(self,localFolder):
		
		self.showSynchronizeMessage=[False,CHANGE_SYNC_OPTIONS_OK,"Information"]
		self.closePopUp=False
		self.getFolderStruct=GetFolderStruct(localFolder)
		self.getFolderStruct.start()
		self.getFolderStruct.finished.connect(self._updateFolderStruct)

	#def updateFolderStruct

	def _updateFolderStruct(self):

		self.errorGetFolder=Bridge.onedriveMan.errorFolder
		self._insertModelEntries()
		self.closePopUp=True
		
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
		return self.entries[index]

	#def getModelData

	@Slot('QVariantList')
	def updateModel(self,info):
		index = self._model.index(info[0])
		self._model.setData(index,info[1],info[2])
	
	#def updateModel

	def _insertModelEntries(self):

		ret=self._model.resetModel()
		entries=Bridge.onedriveMan.folderStruct
		for item in entries:
			self._model.appendRow(item["path"],item["name"],item["isChecked"],item["isExpanded"],item["type"],item["subtype"],item["hide"],item["level"],item["canExpanded"],item["parentPath"])

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
			self.initialSyncConfig[0]=value
		else:
			self.syncCustomChanged=False

	#def getSyncModel 
	
	@Slot()
	def applySyncBtn(self):
		self.showSynchronizeDialog=True

	#def applySyncBtn

	@Slot()
	def cancelSyncBtn(self):
		
		self.closePopUp=False
		
		self.syncCustomChanged=False
		self.initialSyncConfig=copy.deepcopy(Bridge.onedriveMan.currentSyncConfig)
		Bridge.onedriveMan.cancelSyncChanges()
		self.syncAll=self.initialSyncConfig[0]

		self._insertModelEntries()

		index = self._model.index(0)
		self._model.setData(index,"isChecked",True)

		self.closePopUp=True
	
	#def cancelSyncBtn

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
	
	def applySyncChanges(self):

		self.showSynchronizeMessage=[False,CHANGE_SYNC_OPTIONS_OK,"Information"]
		self.closePopUp=False
		self.closeGui=False
		self.changedSyncWorked=True
		self.applySynChangesT=ApplySyncChanges(self.initialSyncConfig,self.keepFolders)
		self.applySynChangesT.start()
		self.applySynChangesT.finished.connect(self._applySyncChanges)

	#def applySyncChanges

	def _applySyncChanges(self):

		self.initialSyncConfig=copy.deepcopy(Bridge.onedriveMan.currentSyncConfig)
		self.syncAll=self.initialSyncConfig[0]
		self.closePopUp=True
		self.syncCustomChanged=False

		if self.applySynChangesT.ret:
			self.showSynchronizeMessage=[True,CHANGE_SYNC_OPTIONS_OK,"Ok"]
			self.closeGui=True
		else:
			self.showSynchronizeMessage=[True,CHANGE_SYNC_OPTIONS_ERROR,"Error"]
	

	#def _applySyncChanges		

	@Slot()
	def hideSynchronizeMessage(self):

		if not self.isOnedriveRunning and not self.errorGetFolder:
			self.showSynchronizeMessage=[False,DISABLE_SYNC_OPTIONS,"Information"]
			self.changedSyncWorked=False

	#def hideSynchronizeMessage		

	def updateClientStatus(self):

		self.isOnedriveRunning=Bridge.onedriveMan.isOnedriveRunning()
		if self.isOnedriveRunning:
			self.showSynchronizeMessage=[True,DISABLE_SYNC_OPTIONS,"Information"]
		else:
			if not self.changedSyncWorked:
				self.showSynchronizeMessage=[False,DISABLE_SYNC_OPTIONS,"Information"]

		self.localFolderEmpty,self.localFolderRemoved=Bridge.onedriveMan.checkLocalFolder()
	
		if self.localFolderEmpty:
			self.showAccountMessage=[True,LOCAL_FOLDER_EMPTY]
		else:
			if self.localFolderRemoved:
				self.showAccountMessage=[True,LOCAL_FOLDER_REMOVED]
			else:
				self.showAccountMessage=[False,""]

	#def updateClientStatus

	@Slot()
	def cancelCreateAccount(self):

		self.currentStack=3
		self.infoStackType="Cancel"

	#def cancelCreateAccount

	@Slot()
	def closeOnedrive(self):

		if not self.removeAction:
			if self.settingsChanged:
				self.closeGui=False
				self.showSettingsDialog=True
			else:
				if self.syncCustomChanged:
					self.closeGui=False
					if self.closePopUp:
						self.showSynchronizeDialog=True
				else:
					if self.closePopUp:
						Bridge.onedriveMan.manageFileFilter("restore")
						self.closeGui=True
					else:
						self.closeGui=False
		else:
			self.closeGui=True

	#def closeOnedrive
	
	isConfigured=Property(bool,_getIsConfigured,constant=True)
	userFolder=Property(str,_getUserFolder,constant=True)

	on_autoStartEnabled=Signal()
	autoStartEnabled=Property(bool,_getAutoStartEnabled,_setAutoStartEnabled,notify=on_autoStartEnabled)
	
	on_rateLimit=Signal()
	rateLimit=Property(int,_getRateLimit,_setRateLimit,notify=on_rateLimit)

	on_monitorInterval=Signal()
	monitorInterval=Property(int,_getMonitorInterval,_setMonitorInterval,notify=on_monitorInterval)

	on_currentStack=Signal()
	currentStack=Property(int,_getCurrentStack,_setCurrentStack, notify=on_currentStack)

	on_closeGui=Signal()
	closeGui=Property(bool,_getCloseGui,_setCloseGui, notify=on_closeGui)

	on_closePopUp=Signal()
	closePopUp=Property(bool,_getClosePopUp,_setClosePopUp, notify=on_closePopUp)

	on_isOnedriveRunning=Signal()
	isOnedriveRunning=Property(bool,_getIsOnedriveRunning,_setIsOnedriveRunning, notify=on_isOnedriveRunning)

	on_accountStatus=Signal()
	accountStatus=Property(str,_getAccountStatus,_setAccountStatus, notify=on_accountStatus)

	on_freeSpace=Signal()
	freeSpace=Property(str,_getFreeSpace,_setFreeSpace, notify=on_freeSpace)

	on_settingsChanged=Signal()
	settingsChanged=Property(bool,_getSettingsChanged,_setSettingsChanged, notify=on_settingsChanged)

	on_showSettingsMessage=Signal()
	showSettingsMessage=Property('QVariantList',_getShowSettingsMessage,_setShowSettingsMessage,notify=on_showSettingsMessage)
	
	on_showSettingsDialog=Signal()
	showSettingsDialog=Property(bool,_getShowSettingsDialog,_setShowSettingsDialog,notify=on_showSettingsDialog)

	on_showUnlinkDialog=Signal()
	showUnlinkDialog=Property(bool,_getShowUnlinkDialog,_setShowUnlinkDialog,notify=on_showUnlinkDialog)

	on_infoStackType=Signal()
	infoStackType=Property(str,_getInfoStackType,_setInfoStackType,notify=on_infoStackType)

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

	on_initialDownload=Signal()
	initialDownload=Property(str,_getInitialDownload,_setInitialDownload,notify=on_initialDownload)

	on_hddFreeSpace=Signal()
	hddFreeSpace=Property(str,_getHddFreeSpace,_setHddFreeSpace,notify=on_hddFreeSpace)

	on_showDownloadDialog=Signal()
	showDownloadDialog=Property(bool,_getShowDownloadDialog,_setShowDownloadDialog,notify=on_showDownloadDialog)
	
	on_currentOptionsStack=Signal()
	currentOptionsStack=Property(int,_getCurrentOptionsStack,_setCurrentOptionsStack,notify=on_currentOptionsStack)

	on_localFolderEmpty=Signal()
	localFolderEmpty=Property(bool,_getLocalFolderEmpty,_setLocalFolderEmpty,notify=on_localFolderEmpty)

	on_localFolderRemoved=Signal()
	localFolderRemoved=Property(bool,_getLocalFolderRemoved,_setLocalFolderRemoved,notify=on_localFolderRemoved)

	on_showPreviousDialog=Signal()
	showPreviousDialog=Property(bool,_getShowPreviousDialog,_setShowPreviousDialog,notify=on_showPreviousDialog)
	
	on_currentOptionsStack=Signal()
	currentOptionsStack=Property(int,_getCurrentOptionsStack,_setCurrentOptionsStack,notify=on_currentOptionsStack)

	bandWidthNames=Property('QVariant',_getBandWidthNames,constant=True)
	model=Property(QObject,_getModel,constant=True)

#class Bridge

if __name__=="__main__":

	pass
