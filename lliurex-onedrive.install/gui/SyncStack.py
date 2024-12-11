from PySide6.QtCore import QObject,Signal,Slot,QThread,Property,QTimer,Qt,QModelIndex
import os 
import sys
import threading
import time
import copy
import FolderModel
import FileExtensionsModel

import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)


class GetFolderStruct(QThread):

	def __init__(self,*args):
		
		QThread.__init__(self)
		self.localFolder=args[0]

	#def __init

	def run(self,*args):

		Bridge.onedriveManager.getFolderStruct(self.localFolder)
	
	#def run

#class GetFolderStruct

class ApplySyncChanges(QThread):

	def __init__(self,*args):

		QThread.__init__(self)
		self.ret=[]
		self.initialSyncConfig=args[0]
		self.keepFolders=args[1]
		self.syncCustomChanged=args[2]
		self.skipFileChanged=args[3]
	
	#def __init

	def run(self,*args):

		self.ret=Bridge.onedriveManager.applySyncChanges(self.initialSyncConfig,self.keepFolders,self.syncCustomChanged,self.skipFileChanged)

	#def run

#class ApplySyncChanges

class Bridge(QObject):

	DISABLE_SYNC_OPTIONS=4
	CHANGE_SYNC_OPTIONS_OK=5
	SPACE_GET_FOLDER_MESSAGE=10
	SPACE_FOLDER_RESTORE_MESSAGE=11
	APPLY_SPACE_CHANGES_MESSAGE=12

	CHANGE_SYNC_OPTIONS_ERROR=-4
	CHANGE_SYNC_FOLDERS_ERROR=-5

	def __init__(self,ticket=None):

		QObject.__init__(self)

		self.core=Core.Core.get_core()
		Bridge.onedriveManager=self.core.onedriveManager
		self._showSynchronizeMessage=[False,Bridge.DISABLE_SYNC_OPTIONS,"Information"]
		self._showSynchronizeDialog=False
		self._showSynchronizePendingDialog=False
		self.initialSyncConfig=copy.deepcopy(Bridge.onedriveManager.currentSyncConfig)
		self._syncAll=Bridge.onedriveManager.syncAll
		self._syncCustomChanged=False
		self._showFolderStruct=Bridge.onedriveManager.showFolderStruct
		self.keepFolders=True
		self.errorGetFolder=False
		self.changedSyncWorked=False
		self.folderEntries=[{"path":"OneDrive", "name": "OneDrive","isChecked":True, "isExpanded": True,"type":"parent","subtype":"root","hide":False,"level":1,"canExpanded":True,"parentPath":""}]
		self._folderModel=FolderModel.FolderModel(self.folderEntries)
		self._fileExtensionsModel=FileExtensionsModel.FileExtensionsModel()
		self._skipFileExtensions=copy.deepcopy(Bridge.onedriveManager.currentSyncConfig[3])
		self._skipFileChanged=False

	#def __init__
	
	def _getFolderModel(self):
		
		return self._folderModel

	#def _getFolderModel

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

	def _getSkipFileExtensions(self):

		return self._skipFileExtensions

	#def _getSkipFileExtensions

	def _setSkipFileExtensions(self,skipFileExtensions):

		if self._skipFileExtensions!=skipFileExtensions:
			self._skipFileExtensions=skipFileExtensions
			self.on_skipFileExtensions.emit()

	#def _setSkipFileExtensions

	def _getFileExtensionsModel(self):

		return self._fileExtensionsModel

	#def _getFileExtensionsModel

	def _getSkipFileChanged(self):

		return self._skipFileChanged

	#def _getSkipFileChanged

	def _setSkipFileChanged(self,skipFileChanged):

		if self._skipFileChanged!=skipFileChanged:
			self._skipFileChanged=skipFileChanged
			self.on_skipFileChanged.emit()

	#def _setSkipFileChanged

	def _updateFileExtensionsModel(self):

		ret=self._fileExtensionsModel.clear()
		Bridge.onedriveManager.updateFileExtensionsModel()
		fileExtensionsEntries=Bridge.onedriveManager.fileExtensionsData
		if len(fileExtensionsEntries)>0:
			for item in fileExtensionsEntries:
				self._fileExtensionsModel.appendRow(item["name"],item["isChecked"])
		
	#def _updateFileExtensionsModel

	def gatherFolderStruct(self):

		self.gatherStruct=GetFolderStruct(True)
		self.gatherStruct.start()
		self.gatherStruct.finished.connect(self.core.spaceStack._endLoading)

	#def gatherFolderStruct

	@Slot(bool)
	def updateFolderStruct(self,localFolder):
		
		self.showSynchronizeMessage=[False,Bridge.CHANGE_SYNC_OPTIONS_OK,"Information"]
		self.core.mainStack.closePopUp=[False,Bridge.SPACE_GET_FOLDER_MESSAGE]
		self.showFolderStruct=False
		self.getFolderStruct=GetFolderStruct(localFolder)
		self.getFolderStruct.start()
		self.getFolderStruct.finished.connect(self._updateFolderStruct)

	#def updateFolderStruct

	def _updateFolderStruct(self):

		self.errorGetFolder=Bridge.onedriveManager.errorFolder
		self._insertModelEntries()
		self.core.mainStack.closePopUp=[True,""]
		self.showFolderStruct=True
		if self.errorGetFolder:
			self.showSynchronizeMessage=[True,Bridge.CHANGE_SYNC_FOLDERS_ERROR,"Error"]

	#def _updateFolderStruct

	@Slot('QVariantList')
	def folderChecked(self,info):

		Bridge.onedriveManager.updateCheckFolder(info[0],info[1])
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
		if None in Bridge.onedriveManager.currentSyncConfig[1]:
			Bridge.onedriveManager.currentSyncConfig[1].remove(None)
		Bridge.onedriveManager.currentSyncConfig[1].sort()
		if None in Bridge.onedriveManager.currentSyncConfig[2]:
			Bridge.onedriveManager.currentSyncConfig[2].remove(None)
		Bridge.onedriveManager.currentSyncConfig[2].sort()

		if self.initialSyncConfig[1]!=Bridge.onedriveManager.currentSyncConfig[1]:
			self.syncCustomChanged=True
		else:
			if self.initialSyncConfig[2]!=Bridge.onedriveManager.currentSyncConfig[2]:
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
		entries=Bridge.onedriveManager.folderStruct
		for item in entries:
			self._folderModel.appendRow(item["path"],item["name"],item["isChecked"],item["isExpanded"],item["type"],item["subtype"],item["hide"],item["level"],item["canExpanded"],item["parentPath"])

	#def _insertModelEntries

	@Slot(bool)
	def getSyncMode(self,value):

		self.hideSynchronizeMessage()

		if value!=self.initialSyncConfig[0]:
			if value!=Bridge.onedriveManager.currentSyncConfig[0]:
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

	@Slot(bool)
	def getSkipFileExtensionsEnable(self,value):

		'''
			value[0]: enable/disable skipFileExtensions
		'''
		self.hideSynchronizeMessage()

		tmpValue=[value,self.skipFileExtensions[1]]

		if tmpValue[0]!=self.skipFileExtensions[0]:
			self.skipFileExtensions=tmpValue
			self.initialSyncConfig[3]=self.skipFileExtensions

		if self.skipFileExtensions!=Bridge.onedriveManager.currentSyncConfig[3]:
			if not self.skipFileExtensions[0]:
				self.skipFileChanged=True
			else:
				if self.skipFileExtensions[0] and len(self.skipFileExtensions[1])>0:
					self.skipFileChanged=True
				else:
					self.skipFileChanged=False
		else:
			self.skipFileChanged=False

	#def getSkipFileExtensionsStatus

	@Slot('QVariantList')
	def getFileExtensionChecked(self,value):

		'''
			value[0]: file extension
			value[1]: checked/unchecked
		'''
		self.hideSynchronizeMessage()
		Bridge.onedriveManager.updateFileExtensionData(value)

		tmpValue=[self.skipFileExtensions[0],sorted(self.skipFileExtensions[1])]
		tmpExtension="*%s"%value[0]
		
		if value[1]:
			if tmpExtension not in tmpValue[1]:
				tmpValue[1].append(tmpExtension)
		else:
			if tmpExtension in tmpValue[1]:
				tmpValue[1].remove(tmpExtension)

		tmpValue[1]=sorted(tmpValue[1])

		if len(tmpValue[1])>0:
			self.skipFileExtensions=tmpValue
			self.initialSyncConfig[3]=self.skipFileExtensions
		else:
			tmpValue=[False,[]]
			self.skipFileExtensions=tmpValue
			self.initialSyncConfig[3]=self.skipFileExtensions

		if self.skipFileExtensions!=Bridge.onedriveManager.currentSyncConfig[3]:
			self.skipFileChanged=True
		else:
			self.skipFileChanged=False

		self._updateFileExtensionsModelInfo()

	#def getFileExtensionChecked

	def _updateFileExtensionsModelInfo(self):

		fileExtensionsEntries=Bridge.onedriveManager.fileExtensionsData
		if len(fileExtensionsEntries)>0:
			for i in range(len(fileExtensionsEntries)):
				index=self._fileExtensionsModel.index(i)
				self._fileExtensionsModel.setData(index,"isChecked",fileExtensionsEntries[i]["isChecked"])

	#def _updateFileExtensionsModelInfo

	@Slot()
	def applySyncBtn(self):
		
		self.showSynchronizeDialog=True

	#def applySyncBtn

	@Slot()
	def cancelSyncChanges(self):
		
		self.core.mainStack.closePopUp=[False,Bridge.SPACE_FOLDER_RESTORE_MESSAGE]
		
		self.syncCustomChanged=False
		self.skipFileChanged=False
		self.initialSyncConfig=copy.deepcopy(Bridge.onedriveManager.currentSyncConfig)
		Bridge.onedriveManager.cancelSyncChanges()
		self.syncAll=self.initialSyncConfig[0]
		if self.syncAll:
			self.showFolderStruct=False
		else:
			self.showFolderStruct=True

		self.skipFileExtensions=self.initialSyncConfig[3]
		self._updateFileExtensionsModel()
		self._insertModelEntries()

		index = self._folderModel.index(0)
		self._folderModel.setData(index,"isChecked",True)

		self.core.mainStack.closePopUp=[True,""]
		self.core.mainStack.closeGui=True
		self.core.spaceStack._manageGoToStack()
	
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
		elif action=="Discard":
			self.showSynchronizePendingDialog=False
			self.cancelSyncChanges()
		elif action=="Cancel":
			self.showSynchronizePendingDialog=False

	#def manageSynchronizePendingDialog
	
	def applySyncChanges(self):

		self.showSynchronizeMessage=[False,Bridge.CHANGE_SYNC_OPTIONS_OK,"Information"]
		self.core.mainStack.closePopUp=[False,Bridge.APPLY_SPACE_CHANGES_MESSAGE]
		self.core.mainStack.closeGui=False
		self.changedSyncWorked=True
		self.applySynChangesT=ApplySyncChanges(self.initialSyncConfig,self.keepFolders,self.syncCustomChanged,self.skipFileChanged)
		self.applySynChangesT.start()
		self.applySynChangesT.finished.connect(self._applySyncChanges)

	#def applySyncChanges

	def _applySyncChanges(self):

		self.initialSyncConfig=copy.deepcopy(Bridge.onedriveManager.currentSyncConfig)
		self.syncAll=self.initialSyncConfig[0]
		self.core.mainStack.closePopUp=[True,""]
		self.showFolderStruct!=self.syncAll
		self.skipFileExtensions=self.initialSyncConfig[3]
		self._updateFileExtensionsModel()

		if self.applySynChangesT.ret:
			self.showSynchronizeMessage=[True,Bridge.CHANGE_SYNC_OPTIONS_OK,"Ok"]
			self.core.mainStack.closeGui=True
			self.syncCustomChanged=False
			self.skipFileChanged=False
		else:
			self.showSynchronizeMessage=[True,Bridge.CHANGE_SYNC_OPTIONS_ERROR,"Error"]
			self.core.spaceStack.moveToOption=""
			self.core.spaceStack.moveToStack=""

		self.core.spaceStack._manageGoToStack()

	#def _applySyncChanges		

	@Slot()
	def hideSynchronizeMessage(self):

		if not self.core.spaceStack.isOnedriveRunning and not self.errorGetFolder:
			self.showSynchronizeMessage=[False,Bridge.DISABLE_SYNC_OPTIONS,"Information"]
			self.changedSyncWorked=False

	#def hideSynchronizeMessage		

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

	on_skipFileExtensions=Signal()
	skipFileExtensions=Property('QVariantList',_getSkipFileExtensions,_setSkipFileExtensions,notify=on_skipFileExtensions)

	on_skipFileChanged=Signal()
	skipFileChanged=Property(bool,_getSkipFileChanged,_setSkipFileChanged,notify=on_skipFileChanged)

	folderModel=Property(QObject,_getFolderModel,constant=True)
	fileExtensionsModel=Property(QObject,_getFileExtensionsModel,constant=True)

#class Bridge

import Core
