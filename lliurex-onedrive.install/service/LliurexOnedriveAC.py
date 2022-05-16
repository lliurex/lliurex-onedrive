import os
import subprocess
import json
from threading import Thread
from queue import Queue
import time


MAX_CHECK_FOLDER_INTERVAL=5
MAX_CHECK_STATUS_INTERVAL=30
MAX_STATUS_WORKER=2

class checkSpaceLocalFolder(Thread):

	def __init__(self,queue):

		Thread.__init__(self)
		self.queue=queue

	#def __init__

	def run(self):

		spaceLocalFolder,spaceConfigPath,spaceService,self.userSystemdAutoStartPath=self.queue.get()

		self.localFolderEmptyToken=os.path.join(spaceConfigPath,".localFolderEmptyToken");
		self.localFolderRemovedToken=os.path.join(spaceConfigPath,".localFolderRemovedToken");
		emptyToken=os.path.join(spaceConfigPath,".emptyToken")

		if os.path.exists(spaceLocalFolder):
			if os.listdir(spaceLocalFolder):
				if os.path.exists(self.localFolderEmptyToken):
					self._manageFolderToken(False,False)
				if os.path.exists(emptyToken):
					os.remove(emptyToken)
			else:
				if not os.path.exists(emptyToken):
					if not os.path.exists(self.localFolderEmptyToken):
						self._manageFolderToken(False,True)
					
					self._stopClient(spaceConfigPath,spaceService)
				else:
					self._manageFolderToken(False,False)
		else:
			if not os.path.exists(self.localFolderRemovedToken):
				self._manageFolderToken(True,False)

			self._stopClient(spaceConfigPath,spaceService)

		self._manageAutoStart(spaceConfigPath,spaceService)

		self.queue.task_done()

	#def run

	def _manageFolderToken(self,remove,empty):

		if remove:
			if not os.path.exists(self.localFolderRemovedToken):
				with open(self.localFolderRemovedToken,'w') as fd:
					pass
		else:
			if os.path.exists(self.localFolderRemovedToken):
				os.remove(self.localFolderRemovedToken)

		if empty:
			if not os.path.exists(self.localFolderEmptyToken):
				with open(self.localFolderEmptyToken,'w') as fd:
					pass
		else:
			if os.path.exists(self.localFolderEmptyToken):
				os.remove(self.localFolderEmptyToken)

	#def _manageFolderToken

	def _stopClient(self,spaceConfigPath,spaceService):

		if self._isOneDriveRunning(spaceConfigPath):
			cmd="systemcl --user stop %s"%spaceService
			try:
				p=subprocess.run(cmd,shell=True,check=True)
			except subprocess.CalledProcessError as e:
				pass

	#def _stòpClient

	def _isOnedriveRunning(self,spaceConfigPath):

		onedriveCommand='onedrive --monitor --confdir="%s"'%spaceConfigPath

		if os.system('ps -ef | grep "%s" | grep -v "grep" 1>/dev/null'%onedriveCommand)==0:
			return True
		else:
			return False

	#def isOnedriveRunning

	def _manageAutoStart(self,spaceConfigPath,spaceService):

		lockAutoStartToken=os.path.join(spaceConfigPath,".lockAutoStartToken")

		if os.path.exists(os.path.join(self.userSystemdAutoStartPath,spaceService)):
			if os.path.exists(self.localFolderEmptyToken) or os.path.exists(self.localFolderRemovedToken):
				if not os.path.exist(lockAutoStartToken):
					with open(lockAutoStartToken,'w') as fd:
						pass
					cmd="systemctl --user disable %s"%spaceService
					try:
						p=subprocess.run(cmd,shell=True,check=True)
					except subprocess.CalledProcessError as e:
						pass
			else:
				if os.path.exists(lockAutoStartToken):
					os.remove(lockAutoStartToken)
		else:
		    if not os.path.exists(self.localFolderEmptyToken) and not os.path.exists(self.localFolderRemovedToken):
		    	if os.path.exists(lockAutoStartToken):
		    		os.remove(lockAutoStartToken)
		    		cmd="systemctl --user enable %s"%spaceService
		    		try:
		    			p=subprocess.run(cmd,shell=True,check=True)
		    		except subprocess.CalledProcessError as e:
		    			pass

	#def _manageAutoStart

#class checkSpaceLocalFolder

class getSpaceStatusWorker(Thread):

	def __init__(self,queue):

		Thread.__init__(self)
		self.queue=queue

	#def __init__

	def run(self):

		spaceConfigPath=self.queue.get()
		MICROSOFT_API_ERROR=-1
		UNABLE_CONNECT_MICROSOFT_ERROR=-2
		LOCAL_FILE_SYSTEM_ERROR=-3
		ZERO_SPACE_AVAILABLE_ERROR=-4
		QUOTA_RESTRICTED_ERROR=-5
		DATABASE_ERROR=-6
		UNAUTHORIZED_ERROR=-7
		UPLOADING_CANCEL_ERROR=-8
		SERVICE_UNAVAILABLE=-9

		ALL_SYNCHRONIZE_MSG=0
		OUT_OF_SYNC_MSG=2
		WITH_OUT_CONFIG=1

		error=False
		code=""
		freespace=""
		if os.path.join(spaceConfigPath,'refresh_token'):
			cmd='/usr/bin/onedrive --display-sync-status --verbose --confdir="%s"'%spaceConfigPath
			p=subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
			poutput,perror=p.communicate()

			if type(poutput) is bytes:
				poutput=poutput.decode()

			if type(perror) is bytes:
				perror=perror.decode()

			if len(perror)>0:
				perror=perror.split('\n')
				error=True
				for item in perror:
					if 'OneDrive API returned an error' in item:
						code=MICROSOFT_API_ERROR
					elif 'Cannot connect to' in item:
						code=UNABLE_CONNECT_MICROSOFT_ERROR
						break
					elif 'local file system' in item:
						code=LOCAL_FILE_SYSTEM_ERROR
					elif 'zero space available' in item:
						code=ZERO_SPACE_AVAILABLE_ERROR
						break
					elif 'quota information' in item:
						if spaceType!="sharepoint":
							code=QUOTA_RESTRICTED_ERROR
					elif 'database' in item:
						code=DATABASE_ERROR
					elif 'Unauthorized' in item:
						code=UNAUTHORIZED_ERROR
					elif '416' in item:
						code=UPLOADING_CANCEL_ERROR
						break
					elif 'Unable to query OneDrive' in item:
						code=UNAUTHORIZED_ERROR
						break
					elif '503' in item:
						code=SERVICE_UNAVAILABLE
					elif 'Free Space' in item:
						tmp_freespace=item.split(':')[1].strip()
						freespace=self._formatFreeSpace(tmp_freespace)

			else:
				poutput=poutput.split('\n')
				for item in poutput:
					if 'No pending' in item:
						code=ALL_SYNCHRONIZE_MSG
					elif 'out of sync' in item:
						code=OUT_OF_SYNC_MSG
					elif 'HTTP 403 - Forbidden' in item:
						code=UNAUTHORIZED_ERROR
						error=True
						break
					elif 'Free Space' in item:
						tmp_freespace=item.split(':')[1].strip()
						freespace=tmp_freespace

		else:
			error=True
			code=WITH_OUT_CONFIG
			
		try:
			with open(os.path.join(spaceConfigPath,".statusToken"),'w') as fd:
				tmpLine=str(error)+("\n")
				fd.write(tmpLine)
				tmpLine=str(code)+("\n")
				fd.write(tmpLine)
				tmpLine=str(freespace)+("\n")
				fd.write(tmpLine)
		except:
			pass

		self.queue.task_done()

	#def run


#class getSpaceStatusWorker

class LliurexOneDriveAC:

	def __init__(self):

		self.user=os.environ["USER"]
		self.llxOnedriveConfigDir="/home/%s/.config/lliurex-onedrive-config/"%(self.user)
		self.onedriveConfigFile=os.path.join(self.llxOnedriveConfigDir,"onedriveConfig.json")
		self.userSystemdPath="/home/%s/.config/systemd/user"%self.user
		self.userSystemdAutoStartPath=os.path.join(self.userSystemdPath,"default.target.wants")
		self.folderWorker=False
		self.statusWorker=False
		self.lastFolderCheck=MAX_CHECK_FOLDER_INTERVAL
		self.lastStatusCheck=MAX_CHECK_STATUS_INTERVAL
		self.initWorker()

	#def __ini__

	def initWorker(self):

		self.folderWorkerThread=Thread(target=self.checkSpaceFolder)
		self.folderWorkerThread.setDaemon(True)
		self.folderWorkerThread.start()
		self.statusWorkerThread=Thread(target=self.checkSpaceStatus)
		self.statusWorkerThread.setDaemon(True)
		self.statusWorkerThread.start()
	
	#def initWorker

	def checkSpaceFolder(self):

		while True:
			if not self.folderWorker:
				time.sleep(1)
				self.lastFolderCheck+=1
				if self.lastFolderCheck > MAX_CHECK_FOLDER_INTERVAL:
					folderQ=Queue()
					self.folderWorker=True
					oneDriveSpaces=self.readOneDriveConfig()
		
					for i in range(MAX_STATUS_WORKER):
						workerF=checkSpaceLocalFolder(folderQ)
						workerF.daemon=True
						workerF.start()

					for space in oneDriveSpaces:
						folderQ.put([space["localFolder"],space["configPath"],space["systemd"],self.userSystemdAutoStartPath])

					folderQ.join()
					self.folderWorker=False
					self.lastFolderCheck=0
				
				else:
					self.lastFolderCheck+=1

	#def checkSpaceFolder

	def checkSpaceStatus(self):

		while True:
			if not self.statusWorker:
				time.sleep(1)
				self.lastStatusCheck+=1
				if self.lastStatusCheck > MAX_CHECK_STATUS_INTERVAL:
					workerQ=Queue()
					self.statusWorker=True
					oneDriveSpaces=self.readOneDriveConfig()

					for i in range(MAX_STATUS_WORKER):
						worker=getSpaceStatusWorker(workerQ)
						worker.daemon=True
						worker.start()

					for space in oneDriveSpaces:
						workerQ.put(space["configPath"])

					workerQ.join()

					self.statusWorker=False
					self.lastStatusCheck=0
				else:
					self.lastStatusCheck+=1
	
	#def checkSpaceStatus

	def readOneDriveConfig(self):

		tmpSpacesList=[]

		if os.path.exists(self.onedriveConfigFile):
			with open(self.onedriveConfigFile,'r') as fd:
				tmpOneDriveConfig=json.load(fd)
				try:
					tmpSpacesList=tmpOneDriveConfig['spacesList']
				except:
					pass

		return tmpSpacesList
	
	#def readOneDriveConfig

#class LliurexOneDriveAC

if __name__=="__main__":
	
	LliurexOneDriveAC()
	while True:
		time.sleep(1)
