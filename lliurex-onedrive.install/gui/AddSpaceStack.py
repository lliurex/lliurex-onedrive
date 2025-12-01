from PySide2.QtCore import QObject,Signal,Slot,QThread,Property,QTimer,Qt,QModelIndex
import os 
import sys
import threading
import time
import copy
import SharePointModel
import LibraryModel

import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)


class CreateSpace(QThread):

	def __init__(self,*args):
		
		QThread.__init__(self)
		self.spaceInfo=args[0]
		self.reuseToken=args[1]
		self.ret=[]

	#def __init__

	def run (self,*args):
		
		self.ret=Bridge.onedriveManager.createSpace(self.spaceInfo,self.reuseToken)

	#def run

#class CreateSpace

class GatherSharePoints(QThread):

	def __init__(self,*args):
		
		QThread.__init__(self)
		self.dataSP=args[0]
		self.ret=True

	#def __init__

	def run (self,*args):
		
		self.ret=Bridge.onedriveManager.getSpaceSharePoints(self.dataSP)

	#def run

#class GatherSharePoints 

class GatherLibraries(QThread):

	def __init__(self,*args):
		
		QThread.__init__(self)
		self.dataSP=args[0]

	#def __init__

	def run (self,*args):
		
		Bridge.onedriveManager.getSharePointLibraries(self.dataSP)

	#def run 

#class GatherLibraries

class MigrateSpace(QThread):

	def __init__(self,*args):
		QThread.__init__(self)
		self.spaceInfo=args[0]
		self.ret=[]

	#def __init__

	def run (self,*args):
		
		self.ret=Bridge.onedriveManager.migrateSpace(self.spaceInfo)
	
	#def run

#class MigrateSpace


class Bridge(QObject):

	SPACE_CREATION_MESSAGE=1
	SEARCH_LIBRARY_MESSAGE=2
	DISABLE_SYNC_OPTIONS=4
	SEARCH_SPACE_SHAREPOINT=16
	SPACE_MIGRATION_MESSAGE=17

	SPACE_DUPLICATE_ERROR=-1
	SPACE_LIBRARIES_EMPTY_ERROR=-2
	SPACE_SHAREPOINT_EMPTY_ERROR=-14
	SPACE_MIGRATION_ERROR=-15
	GET_TOKEN_ERROR=-19	

	def __init__(self,ticket=None):

		QObject.__init__(self)

		self.core=Core.Core.get_core()
		Bridge.onedriveManager=self.core.onedriveManager
		self._sharePointModel=SharePointModel.SharePointModel()
		self._libraryModel=LibraryModel.LibraryModel()
		self.loginUrl="https://login.microsoftonline.com/common/oauth2/v2.0/authorize?client_id=d50ca740-c83f-4d1b-b616-12c519384f0c&scope=Files.ReadWrite%20Files.ReadWrite.all%20Sites.Read.All%20Sites.ReadWrite.All%20offline_access&response_type=code&redirect_uri=https://login.microsoftonline.com/common/oauth2/nativeclient&login_hint="
		self._authUrl=self.loginUrl
		self._showSpaceFormMessage=[False,"","Information"]
		self.reuseToken=False
		self.tempConfig=False
		self._formData=["",0]
		self._showPreviousFolderDialog=False
		self._hddFreeSpace=""
		self._showDownloadDialog=False
		self._initialDownload=""
		self.core.toolStack.updateSpaceAuth=False
		self._withHDDSpace=True
		self._showBackupDialog=False

	#def _init__

	def _getAuthUrl(self):

		return self._authUrl

	#def _getAuthUrl

	def _setAuthUrl(self,authUrl):

		if self._authUrl!=authUrl:
			self._authUrl=authUrl
			self.on_authUrl.emit()

	#def _setAuthUrl	

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

	def _getWithHDDSpace(self):

		return self._withHDDSpace

	#def _getWithHDDSpace

	def _setWithHDDSpace(self,withHDDSpace):

		if self._withHDDSpace!=withHDDSpace:
			self._withHDDSpace=withHDDSpace
			self.on_withHDDSpace.emit() 

	#def _setWithHDDSpace

	def _getShowBackupDialog(self):

		return self._showBackupDialog

	#def _getShowBackupDialog

	def _setShowBackupDialog(self,showBackupDialog):

		if self._showBackupDialog!=showBackupDialog:
			self._showBackupDialog=showBackupDialog
			self.on_showBackupDialog.emit()

	#def _setShowBackupDialog


	def _updateSharePointModel(self):

		ret=self._sharePointModel.clear()
		sharePointsEntries=Bridge.onedriveManager.sharePointsConfigData
		if len(sharePointsEntries)>0:
			for item in sharePointsEntries:
				self._sharePointModel.appendRow(item)
		else:
			self.showSpaceFormMessage=[True,Bridge.SPACE_SHAREPOINT_EMPTY_ERROR,"Error"]
	
	#def _updateSharePointModel

	def _updateLibraryModel(self):

		ret=self._libraryModel.clear()
		libraryEntries=Bridge.onedriveManager.librariesConfigData
		if len(libraryEntries)>0:
			for item in libraryEntries:
				if item["idLibrary"]!="":
					self._libraryModel.appendRow(item["idLibrary"],item["nameLibrary"])
		else:
			self.showSpaceFormMessage=[True,Bridge.SPACE_LIBRARIES_EMPTY_ERROR,"Error"]
	
	#def _updateLibraryModel

	@Slot('QVariantList')
	def getSpaceSharePoints(self,data):

		self.showSpaceFormMessage=[False,"","Information"]
		self.reuseToken=True
		self.tempConfig=False
		self.tmpSpaceEmail=data[0]
		
		if Bridge.onedriveManager.checkIfEmailExists(data[0]):
			self.gatherSharePoints()
		else:
			self.authUrl=self.loginUrl+self.tmpSpaceEmail
			self.tempConfig=True
			self.formData=[data[0],data[1]]
			self.core.mainStack.spacesCurrentOption=2

	#def getSpaceSharePoints

	def gatherSharePoints(self):

		self.core.mainStack.closePopUp=[False,Bridge.SEARCH_SPACE_SHAREPOINT]
		self.core.mainStack.closeGui=False
		self.gatherSharePointsT=GatherSharePoints(self.tmpSpaceEmail)
		self.gatherSharePointsT.start()
		self.gatherSharePointsT.finished.connect(self._gatherSharePoints)
	
	#def gatherSharePoints

	def _gatherSharePoints(self):

		if self.gatherSharePointsT.ret:
			self._updateSharePointModel()
		else:
			self.showSpaceFormMessage=[True,Bridge.GET_TOKEN_ERROR,"Error"]

		self.core.mainStack.closePopUp=[True,""]
		self.core.mainStack.closeGui=True
	
	#def _gatherSharePoints

	@Slot(str)
	def getSharePointLibraries(self,data):

		self.showSpaceFormMessage=[False,"","Information"]
		self.data=data

		self.gatherLibraries()

	#def getSharePointLibraries

	def gatherLibraries(self):

		self.core.mainStack.closePopUp=[False,Bridge.SEARCH_LIBRARY_MESSAGE]
		self.core.mainStack.closeGui=False
		self.gatherLibrariesT=GatherLibraries(self.data)
		self.gatherLibrariesT.start()
		self.gatherLibrariesT.finished.connect(self._gatherLibraries)
	
	#def gatherLibraries

	def _gatherLibraries(self):

		self._updateLibraryModel()
		self.core.mainStack.closePopUp=[True,""]
		self.core.mainStack.closeGui=True

	#def _gatherLibraries

	@Slot()
	def resetSharePoints(self):

		if len(Bridge.onedriveManager.sharePointsConfigData)>0:
			self._sharePointModel.clear()
			Bridge.onedriveManager.sharePointsConfigData=[]

		if len(Bridge.onedriveManager.librariesConfigData)>0:
			self._libraryModel.clear()
			Bridge.onedriveManager.librariesConfigData=[]

	#def resetSharePoints

	@Slot('QVariantList')
	def checkData(self,spaceInfo):

		self.showSpaceFormMessage=[False,"","Information"]
		self.spaceInfo=spaceInfo
		self.formData[0]=spaceInfo[0]
		if spaceInfo[1]=="onedrive":
			self.formData[1]=0
		elif spaceInfo[1]=="onedriveBackup":
			self.formData[1]=3
		elif spaceInfo[1]=="sharepoint":
			self.formData[1]=1
		else:
			self.formData[1]=2

		self.checkDuplicate=Bridge.onedriveManager.checkDuplicate(spaceInfo)
			
		if not self.checkDuplicate[0]:
			ret=Bridge.onedriveManager.checkPreviousLocalFolder(spaceInfo)
			if ret:
				self.showPreviousFolderDialog=True
			else:
				self.createSpace()
		else:
			self.showSpaceFormMessage=[True,Bridge.SPACE_DUPLICATE_ERROR,"Error"]
		
	#def checkData

	def migrateSpace(self):

		self.core.mainStack.closePopUp=[False,Bridge.SPACE_MIGRATION_MESSAGE]
		self.core.mainStack.closeGui=False
		self.migrateSpaceT=MigrateSpace(self.spaceInfo)
		self.migrateSpaceT.start()
		self.migrateSpaceT.finished.connect(self._migrateSpace)

	#def migrateSpace

	def _migrateSpace(self):

		self.core.mainStack._updateSpacesModel()
		self.tempConfig=False

		if self.migrateSpaceT.ret:
			self.core.spaceStack.spaceBasicInfo=Bridge.onedriveManager.spaceBasicInfo
			self.core.spaceStack.spaceLocalFolder=os.path.basename(Bridge.onedriveManager.spaceLocalFolder)
			spaceId=Bridge.onedriveManager.spaceId
			self.core.spaceStack.loadSpace(spaceId)
		else:
			self.core.mainStack.closePopUp=[True,""]
			self.core.mainStack.closeGui=True
			self.showSpaceFormMessage=[True,Bridge.SPACE_MIGRATION_ERROR,"Error"]		

	#def _migrateSpace

	@Slot(str)
	def getToken(self,token):

		Bridge.onedriveManager.createToken(token,self.authUrl)
		if not self.core.toolStack.updateSpaceAuth:
			self.core.mainStack.spacesCurrentOption=1
			if not self.tempConfig:
				self.addSpace()
			else:
				if self.formData[1]!=0:
					self.gatherSharePoints()
				else:
					self.addSpace()

		else:
			self.core.spaceStack.manageCurrentOption=3
			self.core.toolStack.updateSpaceAuthorization()

	#def getToken

	@Slot(int)
	def managePreviousFolderDialog(self,response):

		self.showPreviousFolderDialog=False

		if response==0:
			self.createSpace()
		else:
			self._libraryModel.clear()
			self.core.mainStack.spacesCurrentOption=0

	#def managePreviousFolderDialog

	def createSpace(self):

		if self.spaceInfo[1] in ["onedrive","onedriveBackup"]:
			if self.checkDuplicate[1]:
				self.reuseToken=True
				self.addSpace()
			else:
				self.authUrl=self.loginUrl+self.spaceInfo[0]
				self.reuseToken=False
				self.core.mainStack.spacesCurrentOption=2
		else:
			if self.reuseToken:
				self.addSpace()

	#def createSpace

	def addSpace(self):

		self.core.mainStack.closePopUp=[False,Bridge.SPACE_CREATION_MESSAGE]
		self.core.mainStack.closeGui=False
		self.createSpaceT=CreateSpace(self.spaceInfo,self.reuseToken)
		self.createSpaceT.start()
		self.createSpaceT.finished.connect(self._addSpace)

	#def createSpace

	def _addSpace(self):

		self.core.mainStack._updateSpacesModel()
		self.core.syncStack._updateFileExtensionsModel()
		self.reuseToken=False
		self.tempConfig=False
		self._libraryModel.clear()
		self.withHDDSpace=True

		if self.createSpaceT.ret:
			self.core.spaceStack._initializeVars()
			self.core.settingsStack._getInitialSettings()
			self.core.syncStack.showSynchronizeMessage=[False,self.core.syncStack.DISABLE_SYNC_OPTIONS,"Information"]
			self.core.syncStack.showFolderStruct=False

			if self.spaceInfo[1]!="onedriveBackup":
				self.hddFreeSpace=Bridge.onedriveManager.getHddFreeSpace()
				self.initialDownload=Bridge.onedriveManager.initialDownload
				self.withHDDSpace=Bridge.onedriveManager.thereAreHDDAvailableSpace(True)
				self.showDownloadDialog=True
			else:
				self.showBackupDialog=True
		else:
			self.core.mainStack.closePopUp=[True,""]
			self.core.mainStack.closeGui=True
			self.showSpaceFormMessage=[True,Bridge.GET_TOKEN_ERROR,"Error"]

	#def _createSpace

	@Slot(str)
	def manageDownloadDialog(self,option):

		self.showDownloadDialog=False
		
		if option=="All":
			self.core.spaceStack._initialStartUp()
		elif option=="Custom":
			self.core.mainStack.currentStack=2
			self.core.spaceStack.manageCurrentOption=2
			self.core.mainStack.spacesCurrentOption=0
			self.core.mainStack.closePopUp=[True,""]
			self.core.mainStack.closeGui=True
			self.core.spaceStack.accountStatus=3
		else:
			self.core.spaceStack.removeAccount()

	#def manageDownloadDialog

	@Slot(str)
	def manageBackupDialog(self,option):

		self.showBackupDialog=False
		
		if option=="Start":
			self.core.spaceStack._initialStartUp()
		elif option=="Custom":
			self.core.mainStack.currentStack=2
			self.core.spaceStack.manageCurrentOption=2
			self.core.mainStack.spacesCurrentOption=0
			self.core.mainStack.closePopUp=[True,""]
			self.core.mainStack.closeGui=True
			self.core.spaceStack.accountStatus=3
		else:
			self.core.spaceStack.removeAccount()

	#def manageDownloadDialog

	on_authUrl=Signal()
	authUrl=Property(str,_getAuthUrl,_setAuthUrl,notify=on_authUrl)

	on_formData=Signal()
	formData=Property('QVariantList',_getFormData,_setFormData, notify=on_formData)

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

	on_withHDDSpace=Signal()
	withHDDSpace=Property(bool,_getWithHDDSpace,_setWithHDDSpace,notify=on_withHDDSpace)
	
	on_showBackupDialog=Signal()
	showBackupDialog=Property(bool,_getShowBackupDialog,_setShowBackupDialog,notify=on_showBackupDialog)

	sharePointModel=Property(QObject,_getSharePointModel,constant=True)
	libraryModel=Property(QObject,_getLibraryModel,constant=True)

#class Bridge

import Core
