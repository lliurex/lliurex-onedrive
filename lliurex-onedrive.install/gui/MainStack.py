from PySide2.QtCore import QObject,Signal,Slot,QThread,Property,QTimer,Qt,QModelIndex
import os 
import sys
import threading
import time
import copy
import SpacesModel

import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)


SPACE_GLOBAL_WARNING=15

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

class Bridge(QObject):


	def __init__(self,ticket=None):

		QObject.__init__(self)
		self.core=Core.Core.get_core()
		Bridge.onedriveMan=self.core.onedrivemanager
		self._spacesModel=SpacesModel.SpacesModel()
		self._currentStack=0
		self._spacesCurrentOption=0
		self._closeGui=False
		self._closePopUp=[True,""]
		self._showSpaceSettingsMessage=[False,"","Information"]
		self._requiredMigration=False
		self.checkGlobalLocalFolderTimer=QTimer(None)
		self.checkGlobalLocalFolderTimer.timeout.connect(self.getGlobalLocalFolderInfo)
		self.checkGlobalStatusTimer=QTimer(None)
		self.checkGlobalStatusTimer.timeout.connect(self.getGlobalStatusInfo)
		self.waitForUpdateGlobalMessage=10

		if len(sys.argv)>1:
			self.spaceToManage=sys.argv[1]
		else:
			self.spaceToManage=""

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
				self.core.spaceStack.loadSpace(self.spaceToManage)
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

	def _getSpacesModel(self):

		return self._spacesModel

	#def _getSpacesModel

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

	def _getRequiredMigration(self):

		return self._requiredMigration

	#def _getRequiredMigration

	def _setRequiredMigration(self,requiredMigration):

		if self._requiredMigration!=requiredMigration:
			self._requiredMigration=requiredMigration
			self.on_requiredMigration.emit()

	#def setRequiredMigration

	def _updateSpacesModel(self):

		ret=self._spacesModel.clear()
		spacesEntries=Bridge.onedriveMan.spacesConfigData
		for item in spacesEntries:
			if item["id"]!="":
				self._spacesModel.appendRow(item["id"],item["name"],item["status"],item["isRunning"],item["localFolderWarning"])
	
	#def _updateSpacesModel

	def _updateSpacesModelInfo(self,param):

		updatedInfo=Bridge.onedriveMan.spacesConfigData
		if len(updatedInfo)>0:
			for i in range(len(updatedInfo)):
				index=self._spacesModel.index(i)
				self._spacesModel.setData(index,param,updatedInfo[i][param])

	#def _updateSpacesModelInfo

	@Slot(int)
	def moveToSpaceOption(self,option):
		
		Bridge.onedriveMan.initSpacesSettings()
		Bridge.onedriveMan.deleteTempConfig()
		moveTo=True
		if option==1:
			if not (Bridge.onedriveMan.thereAreHDDAvailableSpace()):
				moveTo=False

		if moveTo:
			self.core.addSpaceStack.formData=["",0]
			self.showSpaceSettingsMessage=[False,"","Information"]
			self.core.addSpaceStack.showSpaceFormMessage=[False,"","Information"]
			self.core.addSpaceStack._libraryModel.clear()
			self.spacesCurrentOption=option
		else:
			self.waitForUpdateGlobalMessage=0
			self.showSpaceSettingsMessage=[True,HDD_SPACE_AVAILABLE_ERROR,"Error"]

	#def moveToSpaceOption

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

		if not self.core.spaceStack.removeAction:
			if self.core.settingsStack.settingsChanged:
				self.closeGui=False
				self.core.settingsStack.showSettingsDialog=True
			else:
				if self.core.syncStack.syncCustomChanged or self.core.syncStack.skipFileChanged:
					self.closeGui=False
					if self.closePopUp[0]:
						self.core.syncStack.showSynchronizePendingDialog=True
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

	on_closeGui=Signal()
	closeGui=Property(bool,_getCloseGui,_setCloseGui, notify=on_closeGui)

	on_closePopUp=Signal()
	closePopUp=Property('QVariantList',_getClosePopUp,_setClosePopUp, notify=on_closePopUp)

	on_showSpaceSettingsMessage=Signal()
	showSpaceSettingsMessage=Property('QVariantList',_getShowSpaceSettingsMessage,_setShowSpaceSettingsMessage, notify=on_showSpaceSettingsMessage)

	on_requiredMigration=Signal()
	requiredMigration=Property(bool,_getRequiredMigration,_setRequiredMigration, notify=on_requiredMigration)

	spacesModel=Property(QObject,_getSpacesModel,constant=True)

#class Bridge

import Core
