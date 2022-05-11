import threading
import time
import os
import subprocess
import json
import math
import shutil 
import copy
import psutil
import re
import unicodedata
import configparser
import tempfile


class OnedriveManager:
	
	def __init__(self):

		self.user=os.environ["USER"]
		self.llxOnedriveConfigDir="/home/%s/.config/lliurex-onedrive-config/"%(self.user)
		self.onedriveConfigFile=os.path.join(self.llxOnedriveConfigDir,"onedriveConfig.json")
		self.onedriveConfig={}
		self.spacesConfigData=[]
		self.librariesConfigData=[]
		self.authUrl="https://login.microsoftonline.com/common/oauth2/v2.0/authorize?client_id=d50ca740-c83f-4d1b-b616-12c519384f0c&scope=Files.ReadWrite%20Files.ReadWrite.all%20Sites.Read.All%20Sites.ReadWrite.All%20offline_access&response_type=code&redirect_uri=https://login.microsoftonline.com/common/oauth2/nativeclient"
		self.userTokenPath="/home/%s/.onedriveAuth/"%(self.user)
		self.configTemplatePath="/usr/share/lliurex-onedrive/llx-data/config"
		self.serviceTemplatePath="/usr/share/lliurex-onedrive/llx-data/template.service"
		self.userSystemdPath="/home/%s/.config/systemd/user"%self.user
		self.userSystemdAutoStartPath=os.path.join(self.userSystemdPath,"default.target.wants")
		self.onedriveConfigDir="/home/%s/.config/onedrives"%self.user
		self.sharePointConfigDir="/home/%s/.config/sharepoints"%self.user
		self.spaceLocalFolder=""
		self.spaceSuffixName=""
		self.folderSuffixName=""
		self.spaceConfPath=""
		self.tempConfigPath=""
		self.customizeConfigParam=['sync_dir','drive_id','monitor_interval','rate_limit']
		self.bandWidth=[{"name":"128 KB/s","value":"131072"},{"name":"256 KB/s","value":"262144"},{"name":"512 KB/s","value":"524288"},{"name":"1 MB/s","value":"1048576"},{"name":"10 MB/s","value":"10485760"},{"name":"20 MB/s","value":"20971520"},{"name":"30 MB/s","value":"31457280"},{"name":"50 MB/s","value":"52428800"},{"name":"100 MB/s","value":"104857600"}]
		self.bandWidthNames=[]
		for item in self.bandWidth:
			self.bandWidthNames.append(item["name"])
		
		self.autoStartEnabled=True
		self.rateLimit=2
		self.monitorInterval=1
		self.currentConfig=[self.autoStartEnabled,self.monitorInterval,self.rateLimit]
		self.syncAll=True
		self.filterFileName="sync_list"
		self.filterFileHashName=".sync_list.hash"
		self.foldersSelected=[]
		self.foldersUnSelected=[]
		self.includeFolders=[]
		self.excludeFolders=[]
		self.currentSyncConfig=[self.syncAll,self.foldersSelected,self.foldersUnSelected]
		self.envConfFiles=[".config.backup",".config.hash","items.sqlite3","items.sqlite3-shm","items.sqlite3-wal"]
		self.createEnvironment()

	#def __init__

	def createEnvironment(self):

		if not os.path.exists(self.llxOnedriveConfigDir):
			os.mkdir(self.llxOnedriveConfigDir)

		if not os.path.exists(self.userSystemdPath):
			tmpPath="/home/%s/.config/systemd"%self.user
			if not os.path.exists(tmpPath):
				os.mkdir(tmpPath)
			os.mkdir(self.userSystemdPath)

		if not os.path.exists(self.onedriveConfigDir):
			os.mkdir(self.onedriveConfigDir)

		if not os.path.exists(self.sharePointConfigDir):
			os.mkdir(self.sharePointConfigDir)

	#def createEnvironment

	def loadOneDriveConfig(self):

		self.readOneDriveConfig()
		self.getSpacesConfig()
		#self.initSpacesSettings()
		
	#def loadOneDriveConfig

	def readOneDriveConfig(self):

		if os.path.exists(self.onedriveConfigFile):
			with open(self.onedriveConfigFile,'r') as fd:
				tmpConfig=json.load(fd)
				self._checkCurrentConfig(tmpConfig)
		else:
			self.onedriveConfig={}
			self.onedriveConfig["spacesList"]=[]
			with open(self.onedriveConfigFile,'w') as fd:
				json.dump(self.onedriveConfig,fd)

	#def readOneDriveConfig

	def _checkCurrentConfig(self,currentConfig):

		currentSpacesList=copy.deepcopy(currentConfig["spacesList"])
		removeCount=0
		for i in range(len(currentSpacesList)-1,-1,-1):
			tokenPath=os.path.join(currentSpacesList[i]["configPath"],'refresh_token')
			if not os.path.exists(tokenPath):
				currentSpacesList.pop(i)
				removeCount+=1

		if removeCount>0:
			currentConfig["spacesList"]=currentSpacesList
			with open(self.onedriveConfigFile,'w') as fd:
				json.dump(currentConfig,fd)
		
		self.onedriveConfig=currentConfig

	#def _checkCurrentConfig

	def getSpacesConfig(self):

		self.spacesConfigData=[]
		spaces=self.onedriveConfig["spacesList"]
		for item in spaces:
			tmp={}
			tmp["name"]=os.path.basename(item["localFolder"])
			tmp["status"]=""
			tmp["isRunning"]=False
			self.spacesConfigData.append(tmp)
	
	#def getSpacesConfig

	def initSpacesSettings(self):

		self.spaceLocalFolder=""
		self.spaceConfPath=""
		self.spaceServiceFile=""
		self.spaceSuffixName=""
		self.folderSuffixName=""
		self.tempConfigPath=""	
		self.librariesConfigData=[]
		self.autoStartEnabled=True
		self.rateLimit=2
		self.monitorInterval=1
		self.currentConfig=[self.autoStartEnabled,self.monitorInterval,self.rateLimit]
		self.syncAll=True
		self.filterFile=""
		self.filerFileHash=""
		self.errorFolder=False
		self.foldersSelected=[]
		self.foldersUnSelected=[]
		self.includeFolders=[]
		self.excludeFolders=[]

	#def initSpacesSettings

	def checkIfEmailExists(self,email):

		for item in self.onedriveConfig["spacesList"]:
			if item["email"]==email:
				tokenPath=os.path.join(item["configPath"],'refresh_token')
				if os.path.exists(tokenPath):
					return True
		return False

	#def checkIfEmailExists

	def getSharePointLibraries(self,email,sharePoint):

		self.librariesConfigData=[]
		confDir=""
		for item in self.onedriveConfig["spacesList"]:
			if item["email"]==email:
				confDir=item["configPath"]
				break

		if confDir=="":
			ret=self.createTempConfig()
			confDir=self.tempConfigPath

		cmd='onedrive --get-O365-drive-id "%s" --confdir="%s"'%(sharePoint,confDir)
		p=subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
		pout,perror=p.communicate()

		if len(perror)==0:
			if len(pout)>0:
				pout=pout.decode().split("\n")

			for i in range(len(pout)-1,-1,-1):
				if 'Library Name:' in pout[i] or 'drive_id:' in pout[i]:
					pass
				else:
					pout.pop(i)	

			for i in range(0,len(pout)-1,2):
				tmp={}
				tmp['idLibrary']=pout[i+1].split(":")[1].strip()
				tmp['nameLibrary']=pout[i].split(":")[1].strip()
				self.librariesConfigData.append(tmp)

	#def getSharePointLibraries

	def checkDuplicate(self,spaceInfo):

		spaceEmail=spaceInfo[0]
		spaceType=spaceInfo[1]
		spaceId=spaceInfo[4]
		
		matchId=0
		duplicateSpace=False
		existsMail=False

		if self.checkIfEmailExists(spaceEmail):
			existsMail=True
			if spaceType=="onedrive":
				for item in self.onedriveConfig["spacesList"]:
					if item["email"]==spaceEmail and item["type"]=="onedrive":
						duplicateSpace=True
						break
			else:
				for item in self.onedriveConfig["spacesList"]:
					if item["id"]==spaceId:
						duplicateSpace=True
						break

		return [duplicateSpace,existsMail]

	#def checkDuplicate

	def checkPreviousLocalFolder(self,spaceInfo):

		self.spaceLocalFolder=""

		self._getSpaceSuffixName(spaceInfo)

		if spaceInfo[1]=="onedrive":
			self.spaceLocalFolder="/home/%s/OneDrive_%s"%(self.user,self.spaceSuffixName)
		else:
			self.spaceLocalFolder="/home/%s/SharePoint_%s/%s"%(self.user,self.spaceSuffixName,self.folderSuffixName)
		
		if os.path.exists(self.spaceLocalFolder):
			if os.listdir(self.spaceLocalFolder):
				return True

		return False

	#def checkPreviousLocalFolder

	def createToken(self,token):
		
		if not os.path.exists(self.userTokenPath):
			os.mkdir(self.userTokenPath)

		self.urlDoc=os.path.join(self.userTokenPath,"urlToken")
		self.tokenDoc=os.path.join(self.userTokenPath,"keyToken")
		with open(self.urlDoc,'w') as fd:
			fd.write(self.authUrl)
		with open(self.tokenDoc,'w') as fd:
			fd.write(token)

	#def createToken

	def createSpace(self,spaceInfo,reuseToken):

		spaceEmail=spaceInfo[0]
		spaceType=spaceInfo[1]
		spaceId=spaceInfo[4]

		self._createSpaceConfFolder(spaceType,spaceId)
		if reuseToken:
			self._copyToken(spaceEmail)
			if spaceType=="sharepoint":
				if os.path.exists(self.tempConfigPath) and len(self.tempConfigPath)>0:
					self._deleteTempConfig()
		else:
			cmd='/usr/bin/onedrive --auth-files %s:%s --confdir="%s"'%(self.urlDoc,self.tokenDoc,self.spaceConfPath)
			p=subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
			poutput=p.communicate()
			rc=p.returncode
			if rc not in [0,1]:
				return False

		self._createSpaceServiceUnit(spaceType)
		self._updateOneDriveConfig(spaceInfo)
		self._manageEmptyToken()
		self._createAuxVariables()
		self.loadOneDriveConfig()

		return True

	#def createSpace 

	def _createSpaceConfFolder(self,spaceType,spaceId):

		self.spaceConfPath=""
		createConfig=False

		if spaceType=="onedrive":
			tmpFolder="onedrive_%s"%self.spaceSuffixName
			self.spaceConfPath=os.path.join(self.onedriveConfigDir,tmpFolder)
			if not os.path.exists(os.path.join(self.onedriveConfigDir,tmpFolder)):
				createConfig=True
		else:
			self.spaceConfPath=os.path.join(self.sharePointConfigDir,self.folderSuffixName.lower())
			if not os.path.exists(os.path.join(self.sharePointConfigDir,self.folderSuffixName.lower())):
				createConfig=True 

		if createConfig:
			os.mkdir(self.spaceConfPath)
			shutil.copy(self.configTemplatePath,self.spaceConfPath)
			
			with open(os.path.join(self.spaceConfPath,"config"),'r') as fd:
				lines=fd.readlines()
			
			with open(os.path.join(self.spaceConfPath,"config"),'w') as fd:
				for line in lines:
					if 'sync_dir =' in line:
						tmpLine=line.replace("{{LOCAL_FOLDER}}",self.spaceLocalFolder)
						fd.write(tmpLine)
					else:
						if spaceType=="sharepoint" and 'drive_id' in line:
							newLine='drive_id = "%s"'%spaceId
							tmpLine=line.replace('# drive_id = ""',newLine)
							fd.write(tmpLine)
						else:
							fd.write(line)
		else:
			spaceConfigFilePath=os.path.join(self.spaceConfPath,'config')
			self.readSpaceConfigFile(spaceConfigFilePath)

	#def _createSpaceConfFolder

	def readSpaceConfigFile(self,spaceConfigFilePath,newAccount=False):

		if os.path.exists(spaceConfigFilePath):
			customParam=self._readCustomParams(spaceConfigFilePath)
			self.monitorInterval="{:.0f}".format(int(customParam['monitor_interval'])/60)
			self.currentConfig[1]=self.monitorInterval

			for i in range(len(self.bandWidth)):
				if self.bandWidth[i]["value"]==customParam['rate_limit']:
					self.rateLimit=i
					self.currentConfig[2]=self.rateLimit
					break

			if newAccount:
				self._updateOneDriveConfig(customParam)

	#def readConfigFile

	def _readCustomParams(self,spaceConfigFilePath):

		customParam={}

		with open(spaceConfigFilePath,'r') as fd:
			lines=fd.readlines()
			for line in lines:
				for param in self.customizeConfigParam:
					tmpLine=line.split("=")
					if param==tmpLine[0].strip():
						value=tmpLine[1].split("\n")[0].strip().split('"')[1]
						customParam[param]=value

		return customParam 

	#def _readCustomParams

	def _updateConfigFile(self,customParam):

		shutil.copy(self.configTemplatePath,self.spaceConfPath)
		configFile=os.path.join(self.spaceConfPath,'config')

		with open(configFile,'r') as fd:
			lines=fd.readlines()

		with open(configFile,'w') as fd:
			for line in lines:
				for param in customParam:
					tmpLine=line.split("=")
					if param==tmpLine[0].strip():
						value=tmpLine[1].split("\n")[0].strip().split('"')[1]
						if value!=customParam[param]:
							line=param+' = '+'"'+customParam[param]+'"\n'
						break
				
				fd.write(line)

	#def _updateConfigFile

	def _copyToken(self,email):

		if not os.path.exists(self.tempConfigPath):
			for item in self.onedriveConfig["spacesList"]:
				if email==item["email"]:
					configPath=item["configPath"]
					break
		else:
			configPath=self.tempConfigPath

		tokenPath=os.path.join(configPath,'refresh_token')

		if os.path.exists(tokenPath):
			shutil.copyfile(tokenPath,os.path.join(self.spaceConfPath,'refresh_token'))

	#def _copyToken

	def _createSpaceServiceUnit(self,spaceType):

		self.spaceServiceFile=""

		if spaceType=="onedrive":
			self.spaceServiceFile="onedrive_%s.service"%self.spaceSuffixName
		else:
			self.spaceServiceFile="sharepoint_%s.service"%self.folderSuffixName.lower()

		if not os.path.exists(os.path.join(self.userSystemdPath,self.spaceServiceFile)):
			shutil.copyfile(self.serviceTemplatePath,os.path.join(self.userSystemdPath,self.spaceServiceFile))
			configFile=configparser.ConfigParser()
			configFile.optionxform=str
			configFile.read(os.path.join(self.userSystemdPath,self.spaceServiceFile))
			tmpCommand=configFile.get("Service","ExecStart")
			tmpCommand=tmpCommand.replace("{{CONF_PATH}}",self.spaceConfPath)
			configFile.set("Service","ExecStart",tmpCommand)
			with open(os.path.join(self.userSystemdPath,self.spaceServiceFile),'w') as fd:
				configFile.write(fd)

		self.manageAutostart(True)
				
	#def _createSpaceServiceUnit

	def _updateOneDriveConfig(self,spaceInfo):

		tmp={}
		tmp["email"]=spaceInfo[0]
		tmp["type"]=spaceInfo[1]
		tmp["sharepoint"]=spaceInfo[2]
		tmp["library"]=spaceInfo[3]
		tmp["localFolder"]=self.spaceLocalFolder
		tmp["configPath"]=self.spaceConfPath
		tmp["systemd"]=self.spaceServiceFile
		if spaceInfo[4]!=None:
			tmp["drive_id"]=spaceInfo[4]
		else:
			tmp["drive_id"]=""

		self.onedriveConfig["spacesList"].append(tmp)
		with open(self.onedriveConfigFile,'w') as fd:
			json.dump(self.onedriveConfig,fd)

	#def _updateOneDriveConfig

	def _manageEmptyToken(self):

		emptyToken=os.path.join(self.spaceConfPath,".emptyToken")
		f=open(emptyToken,'w')
		f.close()

	#def _manageEmptyToken

	def _createAuxVariables(self):
		
		self.filterFile=os.path.join(self.spaceConfPath,self.filterFileName)
		self.filterFileHash=os.path.join(self.spaceConfPath,self.filterFileHashName)
		self.localFolderEmptyToken=os.path.join(self.spaceConfPath,".localFolderEmptyToken")
		self.localFolderRemovedToken=os.path.join(self.spaceConfPath,".localFolderRemovedToken")

	#def _createAuxVariables

	def _getSpaceSuffixName(self,spaceInfo):

		email=spaceInfo[0]
		spaceType=spaceInfo[1]
		spaceName=spaceInfo[2]
		spaceLibrary=spaceInfo[3]

		self.spaceSuffixName=""
		self.folderSuffixName=""

		tmpName=email.split('@')[0]
		tmpName=re.sub('[^0-9a-zA-Z]+', '', tmpName).lower()
		tmpOrganization=email.split('@')[1].split(".")[0].lower()
		self.spaceSuffixName=tmpOrganization+"_"+tmpName
		
		if spaceType=="sharepoint":
			tmpSharePoint=self._stripAccents(spaceName)
			tmpSharePoint=re.sub('[^0-9a-zA-Z]+', '_', tmpSharePoint)
			tmpLibrary=self._stripAccents(spaceLibrary)
			tmpLibrary=re.sub('[^0-9a-zA-Z]+', '_', tmpLibrary)
			self.folderSuffixName=tmpSharePoint+"_"+tmpLibrary

	#def _getSpaceSuffixName

	def _stripAccents(self,text):

		try:
			text = unicode(text, 'utf-8')
		except NameError:
			pass

		text = unicodedata.normalize('NFD', text).encode('ascii', 'ignore').decode("utf-8")

		return str(text)

	#def _stripAccents

	def createTempConfig(self):

		self.tempConfigPath=tempfile.mkdtemp("_sharepoint")
		self.tempFolder=os.path.join(self.tempConfigPath,"Sharepoint")

		shutil.copy(self.configTemplatePath,self.tempConfigPath)

		with open(os.path.join(self.tempConfigPath,"config"),'r') as fd:
			lines=fd.readlines()
			
		with open(os.path.join(self.tempConfigPath,"config"),'w') as fd:
			for line in lines:
				if 'sync_dir' in line:
					tmpLine=line.replace("{{LOCAL_FOLDER}}",self.tempFolder)
					fd.write(tmpLine)
				else:
					fd.write(line)

		cmd='/usr/bin/onedrive --auth-files %s:%s --confdir="%s"'%(self.urlDoc,self.tokenDoc,self.tempConfigPath)
		p=subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
		poutput=p.communicate()
		rc=p.returncode
		if rc not in [0,1]:
			return False

		return True

	#def createTempConfig(self):

	def _deleteTempConfig(self):

		cmd='onedrive --logout --confdir="%s"'%self.tempConfigPath
		p=subprocess.run(cmd,shell=True,check=True)
		shutil.rmtree(self.tempConfigPath)

	#def _deleteTempConfig

	def isConfigured(self,spaceConfPath=None):

		if spaceConfPath==None:
			spaceConfPath=self.spaceConfPath

		token=os.path.join(spaceConfPath,"refresh_token")

		if os.path.exists(token):
			return True
		else:
			return False

	#def isConfigured

	def getHddFreeSpace(self):

		hdd=psutil.disk_usage('/home')
		hddFreeSpace=self._formatFreeSpace(hdd.free)
		return hddFreeSpace

	#def getHddFreeSpace

	def getInitialDownload(self):

		download=""
		cmd='/usr/bin/onedrive --display-sync-status --confdir="%s"'%(self.spaceConfPath)
		p=subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
		poutput=p.communicate()[0]
		rc=p.returncode
		if rc==0:
			if type(poutput) is bytes:
				poutput=poutput.decode()

			poutput=poutput.split("\n")

			for line in poutput:
				if 'data to download' in line:
					tmpLine=line.split(":")[1].strip()
					if tmpLine!="":
						download=self._formatInitialDownload(tmpLine)
						break
		
		return download

	#def getInitialDownload

	def _formatInitialDownload(self,value):

		if "KB" in value:
			tmp=value.split(" ")[0]
			tmp=int(tmp)*1024
		elif "MB" in value:
			tmp=value.split(" ")[0]
			tmp=int(tmp)*1024*1024
		elif "GB" in value:
			tmp=value.split(" ")[0]
			tmp=int(tmp)*1024*1024*1024
		else:
			tmp=value.split(" ")[0]
			tmp=int(tmp)

		return self._formatFreeSpace(tmp)
	
	#def _formatInitialDownload

	def _formatFreeSpace(self,freespace):

		size_name = ("B", "KB", "MB", "GB","TB")

		size_bytes=float(freespace)
		
		if size_bytes==0:
			return '0 B'

		i = int(math.floor(math.log(size_bytes, 1024)))
		p = math.pow(1024, i)
		s = round(size_bytes/p,2)
		unit=size_name[i]

		return str(s)+" "+unit

	#def _formatFreeSpace

	def loadSpaceSettings(self,spaceName):

		self.initSpacesSettings()
		for item in self.onedriveConfig['spacesList']:
			if os.path.basename(item["localFolder"])==spaceName:
				self.spaceLocalFolder=item["localFolder"]
				self.spaceConfPath=item["configPath"]
				self.spaceServiceFile=item["systemd"]
				break

		self._createAuxVariables()
		spaceConfigFilePath=os.path.join(self.spaceConfPath,'config')
		self.readSpaceConfigFile(spaceConfigFilePath)
		if not self.isAutoStartEnabled():
			self.autoStartEnabled=False
			self.currentConfig[0]=False

		if self.existsFilterFile():
			self.syncAll=False
			self.readFilterFile(self.spaceConfPath)
			self.currentSyncConfig[0]=self.syncAll
			self.currentSyncConfig[1]=self.foldersSelected
			self.currentSyncConfig[2]=self.foldersUnSelected
		
	#def loadSpaceSettings

	def existsFilterFile(self):

		if os.path.exists(self.filterFile):
			return True
		else:
			if os.path.exists(self.filterFile+".back"):
				self.manageFileFilter("restore")
				return True
			else:
				return False

	#def existsFilterFile

	def readFilterFile(self,spaceConfPath):

		self.includeFolders=[]
		self.excludeFolders=[]

		filterFile=os.path.join(spaceConfPath,self.filterFile)

		with open(filterFile,'r') as fd:
			lines=fd.readlines()
			fd.close()

			for line in lines:
				tmpLine=line.split("\n")[0]
				if tmpLine.startswith("!"):
					self.excludeFolders.append(tmpLine)
					tmpLine=tmpLine.split("!")[1].split("/*")[0]
					if tmpLine not in self.foldersUnSelected:
						self.foldersUnSelected.append(tmpLine)
				else:
					self.includeFolders.append(tmpLine)
					tmpLine=tmpLine.split("/*")[0]
					if tmpLine not in self.foldersSelected:
						self.foldersSelected.append(tmpLine)

	#def readFilterFile			

	def isOnedriveRunning(self,spaceConfPath=None):

		if spaceConfPath==None:
			spaceConfPath=self.spaceConfPath

		onedriveCommand='onedrive --monitor --confdir="%s"'%spaceConfPath

		if os.system('ps -ef | grep "%s" | grep -v "grep" 1>/dev/null'%onedriveCommand)==0:
			return True
		else:
			return False

	#def isOnedriveRunning

	def isAutoStartEnabled(self):

		tmpService=os.path.join(self.userSystemdPath,self.spaceServiceFile)
		tmpAutoStartService=os.path.join(self.userSystemdAutoStartPath,self.spaceServiceFile)

		if os.path.exists(tmpService) and os.path.exists(tmpAutoStartService):
			return True

		return False

	#def isisAutoStartEnabledAutoStartEnabled

	def manageAutostart(self,enable):

		isOnedriveRunning=self.isOnedriveRunning()
		#serviceUnit=os.path.join(self.userSystemdPath,self.spaceServiceFile)

		if enable:
			cmd="systemctl --user enable %s"%self.spaceServiceFile
			
		else:
			cmd="systemctl --user disable %s"%self.spaceServiceFile

		p=subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
		poutput=p.communicate()
		rc=p.returncode

		if rc !=0:
			return True
		else:
			return False
	
	#def manageAutostart

	def manageSync(self,value):

		if value:
			self.manageFileFilter("restore")
			cmd="systemctl --user start %s"%self.spaceServiceFile
		else:
			cmd="systemctl --user stop %s"%self.spaceServiceFile

		try:
			if os.path.exists(self.localFolderEmptyToken):
				self._manageEmptyToken()
			p=subprocess.run(cmd,shell=True,check=True)
			return True
		except subprocess.CalledProcessError as e:
			return False

	#def manageSync

	def getAccountStatus(self,spaceConfPath=None):

		if spaceConfPath==None:
			spaceConfPath=self.spaceConfPath

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
		if self.isConfigured():
			cmd='/usr/bin/onedrive --display-sync-status --verbose --confdir="%s"'%self.spaceConfPath
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
						freespace=self._formatFreeSpace(tmp_freespace)

		else:
			error=True
			code=WITH_OUT_CONFIG

		return [error,code,freespace]

	#def getAccountStatus

	def removeAccount(self):

		if self.isOnedriveRunning():
			ret=self.manageSync(False)
			
		if not self.isOnedriveRunning():
			cmd='/usr/bin/onedrive --logout --confdir="%s" &'%self.spaceConfPath
			p=subprocess.run(cmd,shell=True,check=True)
			time.sleep(2)
			if not self.isConfigured():
				self._removeSystemdConfig()
				self._removeEnvConfigFiles()
				return True
			else:
				return False
		else:
			return False
	
	#def removeAccount

	def _removeSystemdConfig(self):

		error=self.manageAutostart(False)
		if not error:
			serviceFile=os.path.join(self.userSystemdPath,self.spaceServiceFile)
			if os.path.exists(serviceFile):
				os.remove(serviceFile)


	def _removeEnvConfigFiles(self):

		for item in self.envConfFiles:
			tmpPath=os.path.join(self.spaceConfPath,item)
			if os.path.exists(tmpPath):
				os.remove(tmpPath)

		if os.path.exists(self.filterFile):
			os.remove(self.filterFile)
		if os.path.exists(self.filterFileHash):
			os.remove(self.filterFileHash)

	#def _removeEnvConfigFiles

	def checkLocalFolder(self):

		localFolderEmpty=False;
		localFolderRemoved=False;

		self.localFolderEmptyToken=os.path.join(self.spaceConfPath,".localFolderEmptyToken")
		self.localFolderRemovedToken=os.path.join(self.spaceConfPath,".localFolderRemovedToken")
		
		if os.path.exists(self.localFolderEmptyToken):
			localFolderEmpty=True;
		if os.path.exists(self.localFolderRemovedToken):
			localFolderRemoved=True;

		return [localFolderEmpty,localFolderRemoved]

	#def checkLocalFolder

	def getFolderStruct(self,localFolder=False):

		if localFolder:
			if os.path.exists(self.spaceLocalFolder):
				if os.listdir(self.spaceLocalFolder):
					self.getLocalFolderStruct()
				else:
					self.getCloudFolderStruct()
		else:
			self.getCloudFolderStruct()

	#def getFolderStruct	


	def getCloudFolderStruct(self):
		
		self.errorFolder=False
		if not self.isOnedriveRunning():
			self.manageFileFilter("move")

		cmd='onedrive --synchronize --resync --resync-auth --dry-run --verbose --confdir="%s"'%self.spaceConfPath
		p=subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
		out=p.communicate()[0]
		out=out.decode().split("\n")
		syncOut=copy.deepcopy(out)
		rc=p.returncode

		if not self.isOnedriveRunning():
			self.manageFileFilter("restore")
		
		if rc==0:
			folderResyncStruct=self._processingResyncOut(out)
			folderSyncStruct=self._processingSyncOut(syncOut)

			if len(folderResyncStruct)>0:
				for item in folderSyncStruct:
					match=0
					for element in folderResyncStruct:
						if item["path"]==element["path"]:
							match=0
							break
						else:
							match+=1
					if match>0:
						folderResyncStruct.append(item)
			else:
				folderResyncStruct=folderSyncStruct

			self.folderStruct=sorted(folderResyncStruct,key=lambda d: d['path'])
			self._processingFolderStruct()			
			self.folderStructBack=copy.deepcopy(self.folderStruct)
		else:
			self.errorFolder=True
		

	#def getCloudFolderStruct

	def _processingResyncOut(self,out):

		for i in range(len(out)-1,-1,-1):
			if 'local directory' in out[i]:
					pass
			else:
				if 'creating file' in out[i]:
					pass
				else:
					out.pop(i)				

		folderResyncStruct=[]
		for item in out:
			if 'local directory' in item:
				countChildren=0
				tmpList={}
				tmpEntry=item.split(":")[1].strip()
				tmpList["path"]=tmpEntry
				parentPath=os.path.dirname(tmpEntry)
				tmpEntry=tmpEntry.split("/")
				tmpList["isChecked"]=True
				tmpList["isExpanded"]=True
				tmpList["hide"]=False
				if len(tmpEntry)==1:
					tmpList["name"]=tmpEntry[0]
					tmpList["type"]="OneDrive"
					tmpList["subtype"]="parent"
					tmpList["level"]=3
					tmpList["parentPath"]="OneDrive"

				else:
					tmpList["name"]=tmpEntry[-1]
					tmpList["type"]=tmpEntry[-2]
					tmpList["subtype"]="parent"
					tmpList["level"]=len(tmpEntry)*3
					tmpList["parentPath"]=parentPath

				for j in range(0,len(out),1):
					tmpItem2=out[j]
					if 'local directory' in tmpItem2:
						tmpEntry2=out[j].split(":")[1].strip()
						tmpPath=tmpList["path"]+"/"
						if tmpPath in tmpEntry2:
							countChildren+=1

				if countChildren>0:
					tmpList["canExpanded"]=True 
				else:
					tmpList["canExpanded"]=False
				folderResyncStruct.append(tmpList)	

		return folderResyncStruct

	#def _processingResyncOut

	def _processingSyncOut(self,syncOut):		
		
		for i in range(len(syncOut)-1,-1,-1):
			if 'Processing ' in syncOut[i]:
				pass
			else:
				if 'The directory' in syncOut[i]:
					pass
				else:
					if 'The file' in syncOut[i]:
						pass
					else:
						syncOut.pop(i)				

		for i in range(len(syncOut)-1,-1,-1):
			try:
				if 'local state' in syncOut[i]:
					syncOut.pop(i)
				if 'last modified time' in syncOut[i]:
					syncOut.pop(i)	
			except:
				pass
		
		folderSyncStruct=[]
		for i in range(0,len(syncOut)-1,2):
			tmp={}
			tmpItem=syncOut[i]+": "+syncOut[i+1]
			if 'The directory' in tmpItem:
				countChildren=0
				tmpList={}
				tmpEntry=syncOut[i].split("Processing")[1].strip()
				tmpList["path"]=tmpEntry
				parentPath=os.path.dirname(tmpEntry)
				tmpEntry=tmpEntry.split("/")
				tmpList["isChecked"]=True
				tmpList["isExpanded"]=True
				tmpList["hide"]=False
				if len(tmpEntry)==1:
					tmpList["name"]=tmpEntry[0]
					tmpList["type"]="OneDrive"
					tmpList["subtype"]="parent"
					tmpList["level"]=3
					tmpList["parentPath"]="OneDrive"

				else:
					tmpList["name"]=tmpEntry[-1]
					tmpList["type"]=tmpEntry[-2]
					tmpList["subtype"]="parent"
					tmpList["level"]=len(tmpEntry)*3
					tmpList["parentPath"]=parentPath
				
				
				for j in range(0,len(syncOut)-1,2):
					tmpItem2=syncOut[j]+": "+syncOut[j+1]
					if 'The directory' in tmpItem2:
						tmpEntry2=syncOut[j].split("Processing")[1].strip()
						tmpPath=tmpList["path"]+"/"
						if tmpPath in tmpEntry2:
							countChildren+=1

				if countChildren>0:
					tmpList["canExpanded"]=True 
				else:
					tmpList["canExpanded"]=False
				
				folderSyncStruct.append(tmpList)	
			
		try:
			folderSyncStruct.pop(0)
		except Exception as e:
			pass

		return folderSyncStruct

	#def _processingSyncOut

	def _processingFolderStruct(self):

		if self.existsFilterFile():
			self.readFilterFile()
			for item in self.folderStruct:
				tmp="!"+item["path"]+"/*"
				if tmp in self.excludeFolders:
					item["isChecked"]=False
				else:
					if (item["path"]+"/*") not in self.includeFolders:
						tmp=item["type"]+"/*"
						if tmp in self.includeFolders:
							item["isChecked"]=True
						else:
							tmp=item["path"]+"/*"
							for element in self.includeFolders:
								if element.split("/*")[0] in tmp:
									item["isChecked"]=True
									break
								else:	
									item["isChecked"]=False


	#def _processingFolderStruct

	def getLocalFolderStruct(self):

		try:
			folderLocalStruct=self._processingLocalFolder()
			self.errorFolder=False
		except:
			self.errorFolder=True

		self.folderStruct=sorted(folderLocalStruct,key=lambda d: d['path'])
		self._processingFolderStruct()					
		self.folderStructBack=copy.deepcopy(self.folderStruct)
	

	#def getLocalFolderStruct

	def _processingLocalFolder(self):

		folderLocalStruct=[]
		directory=[]
		tmpFolders=[]

		if os.path.exists(self.spaceLocalFolder):
			for base,dirs,file in os.walk(self.spaceLocalFolder):
				if base !=self.spaceLocalFolder:
					directory.append(base)
			
			for item in directory:
				path=os.path.realpath(item)
				tmpFolders.append(path)
			
			
			for item in tmpFolders:
				countChildren=0
				tmpList={}
				tmpEntry=item.split(self.spaceLocalFolder+"/")[1]
				tmpList["path"]=tmpEntry
				parentPath=os.path.dirname(tmpEntry)
				tmpEntry=tmpEntry.split("/")
				tmpList["isChecked"]=True
				tmpList["isExpanded"]=True
				tmpList["hide"]=False
				if len(tmpEntry)==1:
					tmpList["name"]=tmpEntry[0]
					tmpList["type"]="OneDrive"
					tmpList["subtype"]="parent"
					tmpList["level"]=3
					tmpList["parentPath"]="OneDrive"

				else:
					tmpList["name"]=tmpEntry[-1]
					tmpList["type"]=tmpEntry[-2]
					tmpList["subtype"]="parent"
					tmpList["level"]=len(tmpEntry)*3
					tmpList["parentPath"]=parentPath


				for j in range(0,len(tmpFolders),1):
					tmpItem2=tmpFolders[j]
					tmpEntry2=tmpFolders[j]
					tmpPath=tmpList["path"]+"/"
					if tmpPath in tmpEntry2:
						countChildren+=1

				if countChildren>0:
					tmpList["canExpanded"]=True 
				else:
					tmpList["canExpanded"]=False
				folderLocalStruct.append(tmpList)	
		
		return folderLocalStruct

	#def _processingLocalFolder		

	def manageFileFilter(self,action):

		if action=="move":
			if os.path.exists(self.filterFile):
				os.rename(self.filterFile,self.filterFile+".back")
			if os.path.exists(self.filterFileHash):
				os.rename(self.filterFileHash,self.filterFileHash+".back")				
		elif action=="restore":
			if os.path.exists(self.filterFile+".back"):
				os.rename(self.filterFile+".back",self.filterFile)
			if os.path.exists(self.filterFileHash+".back"):
				os.rename(self.filterFileHash+".back",self.filterFileHash)

	#def manageFileFilter

	def applySettingsChanges(self,value):

		SYSTEMD_ERROR=-10
		WRITE_CONFIG_ERROR=-20
		MULTIPLE_SETTINGS_ERROR=-30

		errorSD=False
		errorMI=False
		errorRL=False

		if value[0]!=self.currentConfig[0]:
			errorSD=self.manageAutostart(value[0])
			if not errorSD:
				self.currentConfig[0]=value[0]
			
		if value[1]!=self.currentConfig[1]:
			errorMI=self.manageMonitorInterval(value[1])
			if not errorMI:
				self.currentConfig[1]=value[1]
			
		if value[2]!=self.currentConfig[2]:
			errorRL=self.manageRateLimit(value[2])
			if not errorRL:
				self.currentConfig[2]=value[2]
			
		
		if errorSD and not errorMI and not errorRL:
			return[True,SYSTEMD_ERROR]

		elif errorSD and (errorMI or errorRL):
			return [True,MULTIPLE_SETTINGS_ERROR]

		elif not errorSD and (errorMI or errorRL):
			return [True,WRITE_CONFIG_ERROR]

		elif not errorSD and errorMI and errorRL:
			return [True,WRITE_CONFIG_ERROR]

		else:
			return[False,'']

	#def applyChanges

	def manageMonitorInterval(self,value):

		value=str(int(value)*60)
		return self._writeConfigFile('monitor_interval',value)

	#def manageMonitorInterval

	def manageRateLimit(self,index):

		value=self.bandWidth[index]["value"]
		return self._writeConfigFile('rate_limit',value)

	#def manageRateLimit

	def _writeConfigFile(self,param,value):

		configFile=os.path.join(self.spaceConfPath,'config')
		if os.path.exists(configFile):
			try:
				with open(configFile,'r') as fd:
					lines=fd.readlines()
					fd.close()

				with open(configFile,'w') as fd:

					for line in lines:
						if  param in line:
							tmp_line=param+' = '+'"'+value+'"\n'
							fd.write(tmp_line)
						else:
							fd.write(line)

					fd.close()
					return False
			except:
				return True
		else:
			return True

	#def _writeConfigFile

	def testOnedrive(self):

		if not os.path.exists(self.userTokenPath):
			os.mkdir(self.userTokenPath)

		testFileName=os.path.basename(self.spaceLocalFolder)+"_test.txt"
		self.testPath=os.path.join(self.userTokenPath,testFileName)
		if os.path.exists(self.testPath):
			os.remove(self.testPath)

		cmd="echo SYNC-DISPLAY-STATUS >>%s"%self.testPath
		os.system(cmd)
		cmd='/usr/bin/onedrive --display-sync-status --verbose --confdir="%s" >>%s 2>&1'%(self.spaceConfPath,self.testPath)
		p=subprocess.call(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)

		cmd="echo TEST SYNCHRONIZE >>%s"%self.testPath
		os.system(cmd)
		cmd='/usr/bin/onedrive --synchronize --dry-run --verbose --confdir="%s" >>%s 2>&1'%(self.spaceConfPath,self.testPath)
		p=subprocess.call(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)

		return

	#def testOnedrive

	def repairOnedrive(self):

		running=self.isOnedriveRunning()
		if os.path.exists(self.localFolderRemovedToken):
			self._manageEmptyToken()
		ret=self._syncResync()
		return ret

	#def repairDB

	def _syncResync(self):

		cmd='/usr/bin/onedrive --synchronize --resync --resync-auth --confdir="%s"'%self.spaceConfPath

		p=subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
		ret=p.communicate()
		rc=p.returncode

		if rc!=0:
			return False
		else:
			return True

	#def _syncResync

#class OnedriveManager
