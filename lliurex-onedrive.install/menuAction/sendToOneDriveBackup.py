#! /usr/bin/python3
from PySide2.QtWidgets import QApplication
from PySide2.QtCore import QUrl, QObject, Slot, Signal, Property,QThread
from PySide2.QtQml import QQmlApplicationEngine
from PySide2.QtGui import QIcon

import os
import sys
import subprocess
import time

class Worker(QObject):

	_finished=Signal(int)
	_progress=Signal(int)

	def __init__(self,*args):

		QObject.__init__(self)
		self.filesToCopy=args[0]
		self.pathToCopy=args[1]
		self.ret=0

	#def __init__

	def run (self):

		errorCount=0
		filesProgress=0

		try:
			for item in self.filesToCopy:
				filesProgress+=1
				self._progress.emit(filesProgress)
				try:
					cmd="cp -r %s %s"%(item,self.pathToCopy)
					ret=subprocess.run(cmd,shell=True,check=True)
				except subprocess.CalledProcessError as e:
					errorCount+=1

			self._finished.emit(errorCount)
		except Exception as e:
			print(str(e))
			self._finished.emit(0)

	#def run


#class CopyFiles

class SendToOnedriveBackup(QObject):

	NO_FILES_TO_COPY=-1
	NO_DEST_PATH=-2
	ERROR_COPY_FILES=-3

	COPY_FILES=0
	COPY_FILES_SUCCESS=1

	def __init__(self):
		
		QObject.__init__(self)
		self._dialogMsgCode=SendToOnedriveBackup.COPY_FILES
		self._filesToCopy=0
		self._filesProgress=0
		self._showProgressBar=False
		self._progressBarValue=0.0
		self.canClose=False
		self.copyFiles()

	#def __init

	def _getDialogMsgCode(self):

		return self._dialogMsgCode

	#def _getDialogMsgCode

	def _setDialogMsgCode(self,dialogMsgCode):

		if self._dialogMsgCode!=dialogMsgCode:
			self._dialogMsgCode=dialogMsgCode
			self.on_dialogMsgCode.emit()

	#def _setDialogMsgCode

	def _getFilesToCopy(self):

		return self._filesToCopy

	#def _getFilesToCopu

	def _setFilesToCopy(self,filesToCopy):

		if self._filesToCopy!=filesToCopy:
			self._filesToCopy=filesToCopy
			self.on_filesToCopy.emit()

	#def _setFilesToCopy

	def _getFilesProgress(self):

		return self._filesProgress

	#def _getFilesProgress

	def _setFilesProgress(self,filesProgress):

		if self._filesProgress!=filesProgress:
			self._filesProgress=filesProgress
			self.on_filesProgress.emit()

	#def _setFilesProgress

	def _getShowProgressBar(self):

		return self._showProgressBar

	#def _getShowProgressBar

	def _setShowProgressBar(self,showProgressBar):

		if self._showProgressBar!=showProgressBar:
			self._showProgressBar=showProgressBar
			self.on_showProgressBar.emit()

	#def _setShowProgressBar

	def _getProgressBarValue(self):

		return self._progressBarValue

	#def _getProgressBarValue

	def _setProgressBarValue(self,progressBarValue):

		if self._progressBarValue!=progressBarValue:
			self._progressBarValue=progressBarValue
			self.on_progressBarValue.emit()

	#def _setProgressBarValue

	def copyFiles(self):

		filesToCopy=sys.argv[1].split(" ")

		self.filesToCopy=len(filesToCopy)
		self.filesProgress=0
		pathToCopy="/tmp/Prueba/"
		errorCount=0
		if self.filesToCopy>0:
			if os.path.exists(pathToCopy):
				self.showProgressBar=True
				self.copyFilesT=QThread()
				self.worker=Worker(filesToCopy,pathToCopy)
				self.worker.moveToThread(self.copyFilesT)
				self.copyFilesT.started.connect(self.worker.run)
				self.worker._finished.connect(self._copyFilesRet)
				self.worker._progress.connect(self._updateProgress)
				self.copyFilesT.start()

			else:
				self.dialogMsgCode=SendToOnedriveBackup.NO_DEST_PATH
				self.canClose=True
		else:
			self.dialogMsgCode=SendToOnedriveBackup.NO_FILES_TO_COPY
			self.canClose=True

	#def copyFiles

	def _copyFilesRet(self,ret):

		self.copyFilesT.quit
		self.showProgressBar=False
		self.canClose=True

		if ret==0:
			self.dialogMsgCode=SendToOnedriveBackup.COPY_FILES_SUCCESS
		else:
			self.dialogMsgCode=SendToOnedriveBackup.ERROR_COPY_FILES

	#def _copyFilesRet

	def _updateProgress(self,fileProgress):

		self.filesProgress=fileProgress
		self.progressBarValue=round((self.filesProgress-1)/self.filesToCopy,2)

	#def _updateProgress

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

	on_filesToCopy=Signal()
	filesToCopy=Property(int,_getFilesToCopy,_setFilesToCopy,notify=on_filesToCopy)

	on_filesProgress=Signal()
	filesProgress=Property(int,_getFilesProgress,_setFilesProgress,notify=on_filesProgress)	

	on_showProgressBar=Signal()
	showProgressBar=Property(bool,_getShowProgressBar,_setShowProgressBar,notify=on_showProgressBar)

	on_progressBarValue=Signal()
	progressBarValue=Property(float,_getProgressBarValue,_setProgressBarValue,notify=on_progressBarValue)

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

	engine.quit.connect(QApplication.quit)
	app.setWindowIcon(QIcon("/usr/share/icons/hicolor/scalable/apps/lliurex-onedrive-backup.svg"));
	ret=app.exec_()
	del engine
	del app
	sys.exit(ret)

#def __main__
