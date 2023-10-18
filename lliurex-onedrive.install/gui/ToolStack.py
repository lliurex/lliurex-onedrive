from PySide2.QtCore import QObject,Signal,Slot,QThread,Property,QTimer,Qt,QModelIndex
import os 
import sys
import threading
import time
import copy

import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)


SPACE_RUNNING_TEST_MESSAGE=13
SPACE_RUNNING_REPAIR_MESSAGE=14
TOOLS_DEFAULT_MESSAGE=18
UPDATE_TOKEN_MESSAGE=19
FOLDERS_DIRECTOY_APPLY_RUNNING=21
FOLDERS_DIRECTOY_REMOVE_RUNNING=22

UPDATE_TOKEN_ERROR=-16

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

class FoldersDirectory(QThread):

	def __init__(self,*args):

		QThread.__init__(self)
		self.enable=args[0]

	#def __init__

	def run (self):

		time.sleep(1)
		ret=Bridge.onedriveMan.manageFoldersDirectory(self.enable)

	#def run

#class FoldersDirectory

class Bridge(QObject):

	def __init__(self,ticket=None):

		QObject.__init__(self)

		self.core=Core.Core.get_core()
		Bridge.onedriveMan=self.core.onedrivemanager

		self._showToolsMessage=[False,TOOLS_DEFAULT_MESSAGE,"Information"]
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

		self.core.mainStack.closePopUp=[False,SPACE_RUNNING_TEST_MESSAGE]
		self.testOnedriveT=TestOneDrive()
		self.testOnedriveT.start()
		self.testOnedriveT.finished.connect(self._testOnedrive)

	#def testOnedrive
	
	def _testOnedrive(self):

		if os.path.exists(Bridge.onedriveMan.testPath):
			cmd="xdg-open %s"%Bridge.onedriveMan.testPath
			os.system(cmd)
		self.core.mainStack.closePopUp=[True,""]

	#def _testOnedrive

	@Slot()
	def repairOnedrive(self):

		self.core.mainStack.closePopUp=[False,SPACE_RUNNING_REPAIR_MESSAGE]
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

		ret=Bridge.onedriveMan.updateSpaceAuth()
		
		if ret:
			self.showToolsMessage=[True,UPDATE_TOKEN_MESSAGE,"Ok"]
		else:
			self.showToolsMessage=[True,UPDATE_TOKEN_ERROR,"Error"]
		
	#def updateSpaceAuthorization

	@Slot(bool)
	def manageFoldersDirectory(self,enable):

		if enable:
			self.core.mainStack.closePopUp=[False,FOLDERS_DIRECTOY_APPLY_RUNNING]
		else:
			self.core.mainStack.closePopUp=[False,FOLDERS_DIRECTOY_REMOVE_RUNNING]

		self.foldersDirectoryT=FoldersDirectory(enable)
		self.foldersDirectoryT.start()
		self.foldersDirectoryT.finished.connect(self._manageFoldersDirectory)
	
	#def manageFoldersDirectory

	def _manageFoldersDirectory(self):

		self.core.mainStack.closePopUp=[True,""]

	#def _manageFoldersDirectory

	on_showToolsMessage=Signal()
	showToolsMessage=Property('QVariantList',_getShowToolsMessage,_setShowToolsMessage,notify=on_showToolsMessage)

#class Bridge

import Core
