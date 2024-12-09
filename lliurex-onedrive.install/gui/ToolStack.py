from PySide6.QtCore import QObject,Signal,Slot,QThread,Property,QTimer,Qt,QModelIndex
import os 
import sys
import threading
import time
import copy

import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)


class TestOneDrive(QThread):

	def __init__(self,*args):

		QThread.__init__(self)

	#def __init

	def run(self,*args):

		Bridge.onedriveManager.testOnedrive()

	#def run

#class TestOneDrive

class RepairOneDrive(QThread):

	def __init__(self,*args):

		QThread.__init__(self)

	#def __init

	def run(self,*args):

		Bridge.onedriveManager.repairOnedrive()

	#def run

#class RepairOneDrive

class FoldersDirectory(QThread):

	def __init__(self,*args):

		QThread.__init__(self)
		self.enable=args[0]

	#def __init__

	def run (self):

		time.sleep(1)
		ret=Bridge.onedriveManager.manageFoldersDirectory(self.enable)

	#def run

#class FoldersDirectory

class UpdateOneDrive(QThread):

	def __init__(self,*args):

		QThread.__init__(self)
		self.ret=False

	#def __init__

	def run (self):

		time.sleep(1)
		self.ret=Bridge.onedriveManager.updateOneDrive()

	#def run


#class UpdateOneDrive

class Bridge(QObject):

	SPACE_RUNNING_TEST_MESSAGE=13
	SPACE_RUNNING_REPAIR_MESSAGE=14
	TOOLS_DEFAULT_MESSAGE=18
	UPDATE_TOKEN_MESSAGE=19
	FOLDERS_DIRECTOY_APPLY_RUNNING=21
	FOLDERS_DIRECTOY_REMOVE_RUNNING=22
	UPDATE_RUNNING_MESSAGE=23
	UPDATE_PROCESS_SUCCESS=24

	UPDATE_TOKEN_ERROR=-16
	UPDATE_PROCESS_ERROR=-17

	def __init__(self,ticket=None):

		QObject.__init__(self)

		self.core=Core.Core.get_core()
		Bridge.onedriveManager=self.core.onedriveManager

		self._showToolsMessage=[False,Bridge.TOOLS_DEFAULT_MESSAGE,"Information"]
		self.updateSpaceAuth=False

	#def __init__
	
	def _getShowToolsMessage(self):

		return self._showToolsMessage

	#def _getShowToolsMessage

	def _setShowToolsMessage(self,showToolsMessage):

		if self._showToolsMessage!=showToolsMessage:
			self._showToolsMessage=showToolsMessage
			self.on_showToolsMessage.emit() 

	#def _setShowToolsMessage

	@Slot()
	def testOnedrive(self):

		self.core.mainStack.closePopUp=[False,Bridge.SPACE_RUNNING_TEST_MESSAGE]
		self.testOnedriveT=TestOneDrive()
		self.testOnedriveT.start()
		self.testOnedriveT.finished.connect(self._testOnedrive)

	#def testOnedrive
	
	def _testOnedrive(self):

		if os.path.exists(Bridge.onedriveManager.testPath):
			cmd="xdg-open %s"%Bridge.onedriveManager.testPath
			os.system(cmd)
		self.core.mainStack.closePopUp=[True,""]

	#def _testOnedrive

	@Slot()
	def repairOnedrive(self):

		self.core.mainStack.closePopUp=[False,Bridge.SPACE_RUNNING_REPAIR_MESSAGE]
		self.repairOneDriveT=RepairOneDrive()
		self.repairOneDriveT.start()
		self.repairOneDriveT.finished.connect(self._repairOnedrive)

	#def reparirOnedrive

	def _repairOnedrive(self):

		self.core.spaceStack.checkAccountStatus()

	#def _repairOnedrive

	@Slot()
	def updateAuth(self):

		self.core.addSpaceStack.authUrl=self.core.addSpaceStack.loginUrl+self.core.spaceStack.spaceBasicInfo[0]
		self.updateSpaceAuth=True
		self.core.spaceStack.manageCurrentOption=4

	#def updateAuth

	def updateSpaceAuthorization(self):

		ret=Bridge.onedriveManager.updateSpaceAuth()
		
		if ret:
			self.showToolsMessage=[True,Bridge.UPDATE_TOKEN_MESSAGE,"Ok"]
		else:
			self.showToolsMessage=[True,Bridge.UPDATE_TOKEN_ERROR,"Error"]
		
	#def updateSpaceAuthorization

	@Slot(bool)
	def manageFoldersDirectory(self,enable):

		if enable:
			self.core.mainStack.closePopUp=[False,Bridge.FOLDERS_DIRECTOY_APPLY_RUNNING]
		else:
			self.core.mainStack.closePopUp=[False,Bridge.FOLDERS_DIRECTOY_REMOVE_RUNNING]

		self.foldersDirectoryT=FoldersDirectory(enable)
		self.foldersDirectoryT.start()
		self.foldersDirectoryT.finished.connect(self._manageFoldersDirectory)
	
	#def manageFoldersDirectory

	def _manageFoldersDirectory(self):

		self.core.mainStack.closePopUp=[True,""]

	#def _manageFoldersDirectory

	@Slot()
	def updateOneDrive(self):

		self.core.mainStack.closePopUp=[False,Bridge.UPDATE_RUNNING_MESSAGE]
		self.updateOneDriveT=UpdateOneDrive()
		self.updateOneDriveT.start()
		self.updateOneDriveT.finished.connect(self._updateOneDriveRet)

	#def updateOneDrive

	def _updateOneDriveRet(self):

		self.core.mainStack.closePopUp=[True,""]

		if self.updateOneDriveT.ret:
			self.showToolsMessage=[True,Bridge.UPDATE_PROCESS_SUCCESS,"Ok"]
			self.core.spaceStack.isUpdateRequired=Bridge.onedriveManager.isUpdateRequired
		else:
			self.showToolsMessage=[True,Bridge.UPDATE_PROCESS_ERROR,"Error"]

	#def _updateOneDriveRet

	on_showToolsMessage=Signal()
	showToolsMessage=Property('QVariantList',_getShowToolsMessage,_setShowToolsMessage,notify=on_showToolsMessage)

#class Bridge

import Core
