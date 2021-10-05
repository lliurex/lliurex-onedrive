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

START_SYNCHRONIZATION_ERROR=-1
STOP_SYNCHRONIZATION_ERROR=-2

class Bridge(QObject):

	def __init__(self,ticket=None):

		QObject.__init__(self)

		self.onedriveMan=OnedriveManager.OnedriveManager()
		self.entries=[{ "name": "Onedrive","isChecked":False, "isExpanded": False,"type":"parent","subtype":"root","hide":False,"level":1}]
		self._model=Model.MyModel(self.entries)
		self._isConfigured=self.onedriveMan.isConfigured()
		self._autoStartEnabled=self.onedriveMan.autoStartEnabled
		self._monitorInterval=int(self.onedriveMan.monitorInterval)
		self._rateLimit=int(self.onedriveMan.rateLimit)	
		self._userFolder=self.onedriveMan.userFolder
		self._currentStack=1
		self._closeGui=False
		self._closePopUp=True
		self._showSettingsDialog=False
		self._isOnedriveRunning=False
		self._accountStatus=1
		self._bandWidthNames=self.onedriveMan.bandWidthNames
		self._freeSpace=""
		self._settingsChanged=False
		self._showSettingsMessage=[False,""]
		self._showAccountMessage=[False,""]
		self._infoStackType="Configuration"
		self.initialConfig=copy.deepcopy(self.onedriveMan.currentConfig)
		self.initBridge()

	#def _init__

	def initBridge(self):

		if self._isConfigured:
			self.currentStack=1
			t = threading.Thread(target=self._loadAccount)
			t.daemon=True
			t.start()
		else:
			self.currentStack=0
	
	#def initBridge
	
	def _loadAccount(self):

		self.onedriveMan.loadConfg()
		self.autoStartEnabled=self.onedriveMan.autoStartEnabled
		self.monitorInterval=int(self.onedriveMan.monitorInterval)
		self.rateLimit=int(self.onedriveMan.rateLimit)
		self.initialConfig=copy.deepcopy(self.onedriveMan.currentConfig)

		self.isOnedriveRunning=self.onedriveMan.isOnedriveRunning()
		error,self.accountStatus,self.freeSpace=self.onedriveMan.getAccountStatus()
		time.sleep(5)
		
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

		self._showAccountMessage=showAccountMessage
		self.on_showAccountMessage.emit()

	#def _setShowAccountMessage

	def _getModel(self):
		return self._model

	#def _getModel

	@Slot(str)
	def createAccount(self,token):

		self.onedriveMan.authToken=token
		self.currentStack=1
		t = threading.Thread(target=self._createAccount)
		t.daemon=True
		t.start()

	#def createAccont

	def _createAccount(self):

		ret=self.onedriveMan.createAccount()
		
		if ret:
			time.sleep(5)
			self.isOnedriveRunning=self.onedriveMan.isOnedriveRunning()
			if not self.isOnedriveRunning:
				self.showAccountMessage=[True,START_SYNCHRONIZATION_ERROR]
			else:
				ret1=self.onedriveMan.getAccountStatus()
				self.accountStatus=ret1[1]
				self.freeSpace=ret1[2]
			self.currentStack=2
		else:
			self.currentStack=3

	#def _createAccount
	
	@Slot()
	def checkAccountStatus(self):

		self.closePopUp=False
		t = threading.Thread(target=self._checkAccountStatus)
		t.daemon=True
		t.start()

	#def checkAccountStatus

	def _checkAccountStatus(self):

		ret=self.onedriveMan.getAccountStatus()
		self.closePopUp=True
		self.accountStatus=ret[1]
		self.freeSpace=ret[2]

	#def _checkAccountStatus 

	@Slot(bool)
	def manageAutoStart(self,value):
		
		if value!=self.initialConfig[0]:
			if value!=self.onedriveMan.currentConfig[0]:
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
			if value!=self.onedriveMan.currentConfig[1]:
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
			if value!=self.onedriveMan.currentConfig[2]:
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

		ret=self.onedriveMan.applyChanges(self.initialConfig)
		self.initialConfig=copy.deepcopy(self.onedriveMan.currentConfig)
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

		self.closePopup=False
		t = threading.Thread(target=self._manageSync,args=(value,))
		t.daemon=True
		t.start()

	#def manageSync

	def _manageSync(self,value):

		isRunningBefore=self.onedriveMan.isOnedriveRunning()
		ret=self.onedriveMan.manageSync(value)
		self.isOnedriveRunning=self.onedriveMan.isOnedriveRunning()
		if isRunningBefore==self.isOnedriveRunning:
			if isRunningBefore:
				self.showAccountMessage=[True,STOP_SYNCHRONIZATION_ERROR]
			else:
				self.showAccountMessage=[True,START_SYNCHRONIZATION_ERROR]
		else:
			self.showAccountMessage=[False,""]

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

		ret=self.onedriveMan.repairOnedrive()
		ret1=self.onedriveMan.getAccountStatus()
		self.accountStatus=ret1[2]
		self.freeSpace=ret1[2]
		self.closePopUp=True

	#def _repairOnedrive
	
	@Slot()
	def removeAccount(self):
		ret=self.onedriveMan.removeAccount()
		self.showUnlinkDialog=False
		if ret:
			self.currentStack=3
			self.infoStackType="Unlink"
		else:
			self.showAccountMessage=[True,STOP_SYNCHRONIZATION_ERROR]	
	
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

		ret=self.onedriveMan.testOnedrive()

		if os.path.exists(self.onedriveMan.testPath):
			cmd="xdg-open %s"%self.onedriveMan.testPath
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
	def updateFolderStruct(self):

		self.closePopUp=False
		t = threading.Thread(target=self._updateFolderStruct)
		t.daemon=True
		t.start()

	#def updateFolderStruct

	def _updateFolderStruct(self):

		ret=self._model.resetModel()
		entries=self.onedriveMan.folderStruct()
		
		for item in entries:
			self._model.appendRow(item["name"],item["isChecked"],item["isExpanded"],item["type"],item["subtype"],item["hide"],item["level"])
		
		time.sleep(5)
		self.closePopUp=True

	#def _uptadeFolderStruct

	@Slot('QVariantList')
	def folderChecked(self,info):
		print('Elemento seleccionado: '+info[0]+" Estado: "+str(info[1]))

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
	'''
	def resetModel(self):
		self._model.resetModel()
	'''
	@Slot()
	def closeOnedrive(self):

		if self.settingsChanged:
			self.closeGui=False
			self.showSettingsDialog=True
		else:
			if self.closePopUp:
				self.closeGui=True
			else:
				self.closeGui=False

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

	bandWidthNames=Property('QVariant',_getBandWidthNames,constant=True)
	model=Property(QObject,_getModel,constant=True)

#class Bridge

if __name__=="__main__":

	pass
