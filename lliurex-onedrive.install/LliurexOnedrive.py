from PySide2.QtCore import QObject,Signal,Slot,QThread,Property,QTimer,Qt,QModelIndex
import os 
import OnedriveManager
import sys
import threading
import time
import copy

import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

class Bridge(QObject):


	def __init__(self,ticket=None):

		QObject.__init__(self)

		self.onedrive_man=OnedriveManager.OnedriveManager()
		self._autoStartEnabled=self.onedrive_man.autoStartEnabled
		self._monitorInterval=int(self.onedrive_man.monitorInterval)
		self._rateLimit=int(self.onedrive_man.rateLimit)	
		self._userFolder=self.onedrive_man.userFolder
		self._currentStack=1
		self._closeGui=False
		self._closePopUp=False
		self._showSettingsDialog=False
		self._isOnedriveRunning=False
		self._accountStatus=1
		self._bandWidthNames=self.onedrive_man.bandWidthNames
		self._freeSpace="Unknown"
		self._settingsChanged=False
		self._showSettingsMessage=[False,""]
		self.initBridge()

	#def _init__

	def initBridge(self):

		self._isConfigured=self.onedrive_man.is_configured()
		self.initialConfig=copy.deepcopy(self.onedrive_man.currentConfig)
		
		if self._isConfigured:
			self.currentStack=1
			t = threading.Thread(target=self._loadAccount)
			t.daemon=True
			t.start()
		else:
			self.currentStack=0
	
	#def initBridge
	
	def _loadAccount(self):

		self.onedrive_man.loadConfg()
		self.autoStartEnabled=self.onedrive_man.autoStartEnabled
		self.monitorInterval=int(self.onedrive_man.monitorInterval)
		self.rateLimit=int(self.onedrive_man.rateLimit)
		self.initialConfig=copy.deepcopy(self.onedrive_man.currentConfig)

		self.isOnedriveRunning=self.onedrive_man.isOnedriveRunning()
		error,self.accountStatus,self.freeSpace=self.onedrive_man.getAccountStatus()
		time.sleep(2)
		
		self.currentStack=2	
	
	#def _loadAccount

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

	@Slot(str)
	def createAccount(self,token):

		self.onedrive_man.authToken=token
		self.currentStack=1
		t = threading.Thread(target=self._createAccount)
		t.daemon=True
		t.start()

	#def createAccont

	def _createAccount(self):

		ret=self.onedrive_man.createAccount()
		time.sleep(3)
		self.isOnedriveRunning=self.onedrive_man.isOnedriveRunning()
		ret1=self.onedrive_man.getAccountStatus()
		self.accountStatus=ret1[1]
		self.freeSpace=ret1[2]
		self.currentStack=2

	#def _createAccount
	
	@Slot()
	def checkAccountStatus(self):

		self.closePopUp=False
		t = threading.Thread(target=self._checkAccountStatus)
		t.daemon=True
		t.start()

	#def checkAccountStatus

	def _checkAccountStatus(self):

		ret=self.onedrive_man.getAccountStatus()
		self.closePopUp=True
		self.accountStatus=ret[1]
		self.freeSpace=ret[2]

	#def _checkAccountStatus 

	@Slot(bool)
	def manageAutoStart(self,value):
		
		if value!=self.initialConfig[0]:
			if value!=self.onedrive_man.currentConfig[0]:
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
			if value!=self.onedrive_man.currentConfig[1]:
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
			if value!=self.onedrive_man.currentConfig[2]:
				self.settingsChanged=True
			else:
				self.settingsChanged=False
			self.initialConfig[2]=int(value)
		else:
			self.settingsChanged=False

	#def getRateLimit

	@Slot()
	def applyChanges(self):

		self.closePopUp=False
		self.closeGui=False
		t = threading.Thread(target=self._applyChanges)
		t.daemon=True
		t.start()
	
	#def applyChanges

	def _applyChanges(self):

		ret=self.onedrive_man.applyChanges(self.initialConfig)
		self.initialConfig=copy.deepcopy(self.onedrive_man.currentConfig)
		self.closePopUp=True
		self.showSettingsMessage=[True,ret[1]]
		self.showSettingsDialog=False

		if not ret[0]:
			self.closeGui=True
			self.settingsChanged=False

	#def _applyChanges

	@Slot()
	def hideSettingsMessage(self):

		self.showSettingsMessage=[False,'']

	#def hideSettingsMessage

	@Slot(bool)
	def manageSync(self,value):

		#self.isOnedriveRunning=value
		self.closePopup=False
		t = threading.Thread(target=self._manageSync,args=(value,))
		t.daemon=True
		t.start()

	#def manageSync

	def _manageSync(self,value):

		ret=self.onedrive_man.manageSync(value)
		self.isOnedriveRunning=self.onedrive_man.isOnedriveRunning()
		self.closePopUp=True
	
	#def _manageSync
	
	@Slot()
	def repairOnedrive(self):

		self.closePopUp=False
		t = threading.Thread(target=self._repairOnedrive)
		t.daemon=True
		t.start()

	#def reparirOnedrive

	def _repairOnedrive(self):

		ret=self.onedrive_man.repairOnedrive()
		ret1=self.onedrive_man.getAccountStatus()
		self.accountStatus=ret1[2]
		self.freeSpace=ret1[2]
		self.closePopUp=True

	#def _repairOnedrive
	
	@Slot()
	def removeAccount(self):
		self.onedrive_man.removeAccount()
		self.showUnlinkDialog=False
		self.currentStack=3	
	
	#def removeAccount

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
		t = threading.Thread(target=self._testOnedrive)
		t.daemon=True
		t.start()

	#def testOnedrive
	
	def _testOnedrive(self):

		ret=self.onedrive_man.testOnedrive()

		if os.path.exists(self.onedrive_man.testPath):
			cmd="xdg-open %s"%self.onedrive_man.testPath
			os.system(cmd)
		self.closePopUp=True

	#def _testOnedrive

	@Slot(str)
	def manageSettingsDialog(self,action):
		
		if action=="Accept":
			self.applyChanges()
		elif action=="Discard":
			self.closeGui=True
			self.settingsChanged=False
			self.showSettingsDialog=False
		elif action=="Cancel":
			self.closeGui=False
			self.showSettingsDialog=False

	#def manageSettingsDialog

	@Slot()
	def closeOnedrive(self):

		if self.settingsChanged:
			self.closeGui=False
			self.showSettingsDialog=True
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

	bandWidthNames=Property('QVariant',_getBandWidthNames,constant=True)

#class Bridge

if __name__=="__main__":

	pass