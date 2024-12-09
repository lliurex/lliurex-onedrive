from PySide6.QtCore import QObject,Signal,Slot,QThread,Property,QTimer,Qt,QModelIndex
import os 
import sys
import threading
import time
import copy

import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)


class ApplySettingsChanges(QThread):

	def __init__(self,*args):

		QThread.__init__(self)
		self.ret=[]
		self.initialConfig=args[0]
	
	#def __init

	def run(self,*args):

		self.ret=Bridge.onedriveManager.applySettingsChanges(self.initialConfig)

	#def run

#class ApplySettingsChanges

class Bridge(QObject):

	APPLY_SPACE_CHANGES_MESSAGE=12

	def __init__(self,ticket=None):

		QObject.__init__(self)

		self.core=Core.Core.get_core()
		Bridge.onedriveManager=self.core.onedriveManager
		self._showSpaceSettingsMessage=[False,"","Information"]
		self._autoStartEnabled=Bridge.onedriveManager.autoStartEnabled
		self._monitorInterval=int(Bridge.onedriveManager.monitorInterval)
		self._rateLimit=int(Bridge.onedriveManager.rateLimit)
		self._skipSize=Bridge.onedriveManager.skipSize
		self._logEnabled=Bridge.onedriveManager.logEnabled
		self._logSize=""	
		self._showSettingsDialog=False
		self._bandWidthNames=Bridge.onedriveManager.bandWidthNames
		self._maxFileSizeNames=Bridge.onedriveManager.maxFileSizeNames
		self._fileNotificationsEnabled=Bridge.onedriveManager.fileNotificationsEnabled
		self._settingsChanged=False
		self._showSettingsMessage=[False,""]
		self.initialConfig=copy.deepcopy(Bridge.onedriveManager.currentConfig)

	#def __init__
	
	def _getBandWidthNames(self):
		
		return self._bandWidthNames

	#def _getBandWidthNames

	def _getMaxFileSizeNames(self):

		return self._maxFileSizeNames

	#def _getMaxFileSizeNames

	def _getShowSpaceSettingsMessage(self):

		return self._showSpaceSettingsMessage

	#def _getShowSpaceSettingsMessage	

	def _setShowSpaceSettingsMessage(self,showSpaceSettingsMessage):
		
		if self._showSpaceSettingsMessage!=showSpaceSettingsMessage:
			self._showSpaceSettingsMessage=showSpaceSettingsMessage
			self.on_showSpaceSettingsMessage.emit()

	#def _setShowSpaceSettingsMessage				

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

	def _getFileNotificationsEnabled(self):

		return self._fileNotificationsEnabled

	#def _getFileNotificationsEnabled

	def _setFileNotificationsEnabled(self,fileNotificationsEnabled):

		if self._fileNotificationsEnabled!=fileNotificationsEnabled:
			self._fileNotificationsEnabled=fileNotificationsEnabled
			self.on_fileNotificationsEnabled.emit()

	#def _setFileNotificationsEnabled

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

	def _getInitialSettings(self):

		self.autoStartEnabled=Bridge.onedriveManager.autoStartEnabled
		self.monitorInterval=int(Bridge.onedriveManager.monitorInterval)
		self.rateLimit=int(Bridge.onedriveManager.rateLimit)
		self.skipSize=Bridge.onedriveManager.skipSize
		self.logEnabled=Bridge.onedriveManager.logEnabled
		self.logSize=Bridge.onedriveManager.logSize
		self.fileNotificationsEnabled=Bridge.onedriveManager.fileNotificationsEnabled
		self.initialConfig=copy.deepcopy(Bridge.onedriveManager.currentConfig)

	#def _getInitialSettings

	@Slot(bool)
	def manageAutoStart(self,value):
		
		if value!=self.initialConfig[0]:
			self.initialConfig[0]=value
			self.autoStartEnabled=value

		if self.initialConfig!=Bridge.onedriveManager.currentConfig:
			self.settingsChanged=True
		else:
			self.settingsChanged=False

	#def manageAutoStart

	@Slot(int)
	def getMonitorInterval(self,value):

		if value!=self.initialConfig[1]:
			self.monitorInterval=int(value)
			self.initialConfig[1]=int(value)

		if self.initialConfig!=Bridge.onedriveManager.currentConfig:
			self.settingsChanged=True
		else:
			self.settingsChanged=False

	#def getMonitorInterval

	@Slot(int)
	def getRateLimit(self,value):

		if value!=self.initialConfig[2]:
			self.rateLimit=int(value)
			self.initialConfig[2]=int(value)
		
		if self.initialConfig!=Bridge.onedriveManager.currentConfig:
			self.settingsChanged=True
		else:
			self.settingsChanged=False
	
	#def getRateLimit

	@Slot('QVariantList')
	def getSkipSize(self,value):

		if value!=self.initialConfig[3]:
			self.skipSize=value
			self.initialConfig[3]=value
		
		if self.initialConfig!=Bridge.onedriveManager.currentConfig:
			self.settingsChanged=True
		else:
			self.settingsChanged=False

	#def getSkipSize

	@Slot(bool)
	def getLogEnabled(self,value):

		if value!=self.initialConfig[4]:
			self.initialConfig[4]=value
			self.logEnabled=value
		
		if self.initialConfig!=Bridge.onedriveManager.currentConfig:
			self.settingsChanged=True
		else:
			self.settingsChanged=False

	#def getLogEnabled

	@Slot()
	def openSpaceLogFile(self):

		if os.path.exists(Bridge.onedriveManager.logPath):
			cmd="xdg-open %s"%Bridge.onedriveManager.logPath
			os.system(cmd)

	#def openSpaceLogFile

	@Slot()
	def removeLogFile(self):

		if os.path.exists(Bridge.onedriveManager.logPath):
			os.remove(Bridge.onedriveManager.logPath)

		self.logSize=Bridge.onedriveManager.getLogFileSize()

	#def removeLogFile

	@Slot(bool)
	def manageFileNotifications(self,value):

		if value!=self.initialConfig[5]:
			self.initialConfig[5]=value
			self.fileNotificationsEnabled=value

		if self.initialConfig!=Bridge.onedriveManager.currentConfig:
			self.settingsChanged=True
		else:
			self.settingsChanged=False

	#def manageFileNotifications

	@Slot()
	def applySettingsChanges(self):

		self.showSettingsMessage=[False,'']
		self.core.mainStack.closePopUp=[False,Bridge.APPLY_SPACE_CHANGES_MESSAGE]
		self.core.mainStack.closeGui=False
		self.applySettingsChangesT=ApplySettingsChanges(self.initialConfig)
		self.applySettingsChangesT.start()
		self.applySettingsChangesT.finished.connect(self._applySettingsChanges)

	#def applySettingsChanges

	def _applySettingsChanges(self):

		self.initialConfig=copy.deepcopy(Bridge.onedriveManager.currentConfig)
		self.core.mainStack.closePopUp=[True,""]
		self.showSettingsMessage=[True,self.applySettingsChangesT.ret[1]]
		self.showSettingsDialog=False

		if not self.applySettingsChangesT.ret[0]:
			self.core.mainStack.closeGui=True
			self.settingsChanged=False
		else:
			self.core.spaceStack.moveToOption=""
			self.core.spaceStack.moveToStack=""

		self.core.spaceStack._manageGoToStack()

	#def _applySettingsChanges

	@Slot()
	def cancelSettingsChanges(self):

		self.hideSettingsMessage()
		self.settingsChanged=False
		self.showSettingsDialog=False
		self.initialConfig=copy.deepcopy(Bridge.onedriveManager.currentConfig)
		self.autoStartEnabled=self.initialConfig[0]
		self.monitorInterval=int(self.initialConfig[1])
		self.rateLimit=self.initialConfig[2]
		self.skipSize=self.initialConfig[3]
		self.logEnabled=self.initialConfig[4]
		self.fileNotificationsEnabled=self.initialConfig[5]
		self.core.mainStack.closeGui=True
		self.core.spaceStack._manageGoToStack()

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
			self.core.mainStack.closeGui=False
			self.showSettingsDialog=False
			self.core.spaceStack.moveToOption=""
	
	#def manageSettingsDialog

	on_showSpaceSettingsMessage=Signal()
	showSpaceSettingsMessage=Property('QVariantList',_getShowSpaceSettingsMessage,_setShowSpaceSettingsMessage, notify=on_showSpaceSettingsMessage)

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
	
	on_fileNotificationsEnabled=Signal()
	fileNotificationsEnabled=Property(bool,_getFileNotificationsEnabled,_setFileNotificationsEnabled,notify=on_fileNotificationsEnabled)

	on_settingsChanged=Signal()
	settingsChanged=Property(bool,_getSettingsChanged,_setSettingsChanged, notify=on_settingsChanged)

	on_showSettingsMessage=Signal()
	showSettingsMessage=Property('QVariantList',_getShowSettingsMessage,_setShowSettingsMessage,notify=on_showSettingsMessage)
	
	on_showSettingsDialog=Signal()
	showSettingsDialog=Property(bool,_getShowSettingsDialog,_setShowSettingsDialog,notify=on_showSettingsDialog)

	bandWidthNames=Property('QVariant',_getBandWidthNames,constant=True)
	maxFileSizeNames=Property('QVariant',_getMaxFileSizeNames,constant=True)

#class Bridge

import Core
