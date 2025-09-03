#! /usr/bin/python3
from PySide2.QtWidgets import QApplication
from PySide2.QtCore import QUrl, QObject, Slot, Signal, Property,QThread
from PySide2.QtQml import QQmlApplicationEngine
from PySide2.QtGui import QIcon

import os
import sys
import subprocess
import time
import tempfile
import threading

class CheckWorker(QObject):

	NO_FILES_TO_COPY=-1
	NO_DEST_PATH=-2

	_finished=Signal('QVariantList')

	def __init__(self,*args):

		QObject.__init__(self)
		self.filesToCopy=sys.argv[1].replace(" /","#/")
		self.destPath=sys.argv[2]
	
	#def __init__

	def run(self):

		time.sleep(1)

		filesToCopy=self.filesToCopy.split("#")
	
		if len(filesToCopy)>0:
			if os.path.exists(self.destPath):
				errorsReportPath=tempfile.mkstemp('_oneDriveBackupError.txt')[1]
				self._finished.emit([True,filesToCopy,self.destPath,errorsReportPath])
			else:
				self._finished.emit([False,CheckWorker.NO_DEST_PATH])
		else:
			self._finised.emit([False,CheckWorker.NO_FILES_TO_COPY])

	#def run

#class CheckWorker

class CopyWorker(QObject):

	_finished=Signal(int)
	_progress=Signal('QVariantList')

	def __init__(self,*args):

		QObject.__init__(self)
		self.filesToCopy=args[0]
		self.destPath=args[1]
		self.errorsReportPath=args[2]
		self.ret=0

	#def __init__

	def run (self):

		errorCount=[]
		filesProgress=0

		for item in self.filesToCopy:
			filesProgress+=1
			self._progress.emit([filesProgress,item])
			time.sleep(0.05)
			try:
				cmd="cp -r '%s' %s"%(item,self.destPath)
				ret=subprocess.run(cmd,shell=True,check=True)
			except subprocess.CalledProcessError as e:
				errorCount.append("- %s - Error: %s"%(item,str(e)))

		if len(errorCount)>0:
			try:
				with open(self.errorsReportPath,'w') as fd:
					fd.write("Errors detected during copying\n")
					fd.write("-------------------------------\n")
					for item in errorCount:
						fd.write(item+"\n")
			except Exception as e:
				print(e)

		self._finished.emit(len(errorCount))
	
	#def run

#class CopyWorker

class SendToOnedriveBackup(QObject):

	ERROR_COPY_FILES=-3
	INVALID_ARGUMENTS=-4

	CHECKING_INFO=0
	COPY_FILES=1
	COPY_FILES_SUCCESS=2

	def __init__(self):
		
		QObject.__init__(self)
		self._dialogMsgCode=SendToOnedriveBackup.CHECKING_INFO
		self._totalFilesToCopy=0
		self._filesProgress=0
		self._fileProcessed=""
		self._showProgressBar=False
		self._showErrorBtn=False
		self._errorsDetected=0
		self.canClose=False
		self.checkInfo()

	#def __init

	def _getDialogMsgCode(self):

		return self._dialogMsgCode

	#def _getDialogMsgCode

	def _setDialogMsgCode(self,dialogMsgCode):

		if self._dialogMsgCode!=dialogMsgCode:
			self._dialogMsgCode=dialogMsgCode
			self.on_dialogMsgCode.emit()

	#def _setDialogMsgCode

	def _getTotalFilesToCopy(self):

		return self._totalFilesToCopy

	#def _getTotalFilesToCopy

	def _setTotalFilesToCopy(self,totalFilesToCopy):

		if self._totalFilesToCopy!=totalFilesToCopy:
			self._totalFilesToCopy=totalFilesToCopy
			self.on_totalFilesToCopy.emit()

	#def _setTotalFilesToCopy

	def _getFilesProgress(self):

		return self._filesProgress

	#def _getFilesProgress

	def _setFilesProgress(self,filesProgress):

		if self._filesProgress!=filesProgress:
			self._filesProgress=filesProgress
			self.on_filesProgress.emit()

	#def _setFilesProgress

	def _getFileProcessed(self):

		return self._fileProcessed

	#def _getFileProcessed

	def _setFileProcessed(self,fileProcessed):

		if self._fileProcessed!=fileProcessed:
			self._fileProcessed=fileProcessed
			self.on_fileProcessed.emit()

	#def _setFileProcessed

	def _getShowProgressBar(self):

		return self._showProgressBar

	#def _getShowProgressBar

	def _setShowProgressBar(self,showProgressBar):

		if self._showProgressBar!=showProgressBar:
			self._showProgressBar=showProgressBar
			self.on_showProgressBar.emit()

	#def _setShowProgressBar

	def _getShowErrorBtn(self):

		return self._showErrorBtn

	#def _getShowErrorBtn

	def _setShowErrorBtn(self,showErrorBtn):

		if self._showErrorBtn!=showErrorBtn:
			self._showErrorBtn=showErrorBtn
			self.on_showErrorBtn.emit()

	#def _setShowErrorBtn

	def _getErrorsDetected(self):

		return self._errorsDetected

	#def _getErrorsDetected

	def _setErrorsDetected(self,errorsDetected):

		if self._errorsDetected!=errorsDetected:
			self._errorsDetected=errorsDetected
			self.on_errorsDetected.emit()

	#def _setErrorsDetected

	def checkInfo(self):

		self.showProgressBar=True
		try:
			self.checkInfoT=QThread()
			self.checkWorker=CheckWorker()
			self.checkWorker.moveToThread(self.checkInfoT)
			self.checkInfoT.started.connect(self.checkWorker.run)
			self.checkWorker._finished.connect(self._checkInfoT)
			self.checkInfoT.start()
		except:
			self.showProgressBar=False
			self.dialogMsgCode=SendToOnedriveBackup.INVALID_ARGUMENTS
			self.canClose=True

	#def checkInfo

	def _checkInfoT(self,ret):

		self.checkInfoT.quit()

		if ret[0]:
			self.filesToCopy=ret[1]
			self.totalFilesToCopy=len(self.filesToCopy)
			self.destPath=ret[2]
			self.errorsReportPath=ret[3]
			self.copyFiles()
		else:
			self.showProgressBar=False
			self.dialogMsgCode=ret[1]
			self.canClose=True

	#def _checkInfoT

	def copyFiles(self):

		self.filesProgress=0
		errorCount=0
		
		self.dialogMsgCode=SendToOnedriveBackup.COPY_FILES
		self.copyFilesT=QThread()
		self.copyWorker=CopyWorker(self.filesToCopy,self.destPath,self.errorsReportPath)
		self.copyWorker.moveToThread(self.copyFilesT)
		self.copyFilesT.started.connect(self.copyWorker.run)
		self.copyWorker._finished.connect(self._copyFilesRet)
		self.copyWorker._progress.connect(self._updateProgress)
		self.copyFilesT.start()
				
	#def copyFiles
	
	def _copyFilesRet(self,ret):

		self.copyFilesT.quit
		self.showProgressBar=False
		
		if ret==0:
			self.dialogMsgCode=SendToOnedriveBackup.COPY_FILES_SUCCESS
		else:
			self.dialogMsgCode=SendToOnedriveBackup.ERROR_COPY_FILES
			self.showErrorBtn=True
			self.errorsDetected=ret

		self.canClose=True

	#def _copyFilesRet

	def _updateProgress(self,fileProgress):

		self.filesProgress=fileProgress[0]
		self.fileProcessed=fileProgress[1]

	#def _updateProgress

	@Slot()
	def openErrorsReport(self):

		self.reportCmd="xdg-open %s"%self.errorsReportPath
		self.openReport=threading.Thread(target=self._openReport)
		self.openReport.daemon=True
		self.openReport.start()

	#def openErrorsReport

	def _openReport(self):

		os.system(self.reportCmd)

	#def _openReport

	@Slot()
	def cancelClicked(self):
		
		app.quit()

	#def cancelClicked

	@Slot(bool,result=bool)
	def closed(self,state):
		
		return self.canClose	

	#def closed	

	on_dialogMsgCode=Signal()
	dialogMsgCode=Property(int,_getDialogMsgCode,_setDialogMsgCode,notify=on_dialogMsgCode)

	on_totalFilesToCopy=Signal()
	totalFilesToCopy=Property(int,_getTotalFilesToCopy,_setTotalFilesToCopy,notify=on_totalFilesToCopy)

	on_filesProgress=Signal()
	filesProgress=Property(int,_getFilesProgress,_setFilesProgress,notify=on_filesProgress)	

	on_fileProcessed=Signal()
	fileProcessed=Property(str,_getFileProcessed,_setFileProcessed,notify=on_fileProcessed)

	on_showProgressBar=Signal()
	showProgressBar=Property(bool,_getShowProgressBar,_setShowProgressBar,notify=on_showProgressBar)

	on_showErrorBtn=Signal()
	showErrorBtn=Property(bool,_getShowErrorBtn,_setShowErrorBtn,notify=on_showErrorBtn)
	
	on_errorsDetected=Signal()
	errorsDetected=Property(int,_getErrorsDetected,_setErrorsDetected,notify=on_errorsDetected)

#class SendToOnedriveBackup

if __name__=="__main__":

	app = QApplication()
	engine = QQmlApplicationEngine()
	engine.clearComponentCache()
	context=engine.rootContext()
	bridge=SendToOnedriveBackup()
	context.setContextProperty("bridge", bridge)

	url = QUrl("/usr/share/lliurex-onedrive/rsrc/send_to_backup_dialog.qml")

	engine.load(url)
	if not engine.rootObjects():
		sys.exit(-1)

	engine.quit.connect(app.quit)
	app.setWindowIcon(QIcon("/usr/share/icons/hicolor/32x32/apps/lliurex-onedrive-backup"));
	ret=app.exec_()
	del engine
	del app
	sys.exit(ret)

#def __main__
