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
		self.synAll=True
		self.filterFile="sync_list"
		self.filterFileHash=".sync_list.hash"
		self.foldersSelected=[]
		self.foldersUnSelected=[]
		self.includeFolders=[]
		self.excludeFolders=[]
	
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

		spaces=self.onedriveConfig["spacesList"]
		for item in spaces:
			tmp={}
			tmp["name"]=item["localFolder"]
			tmp["status"]=""
			tmp["isRunning"]=False
			self.spacesConfigData.append(tmp)
	
	#def getSpacesConfig

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
			print("Respuesta %s"%(str()))
			if rc not in [0,1]:
				return False

		self._createSpaceServiceUnit(spaceType)
		self._updateOneDriveConfig(spaceInfo)
		self._manageEmptyToken()
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

		self.serviceFile=""

		if spaceType=="onedrive":
			self.serviceFile="onedrive_%s.service"%self.spaceSuffixName
		else:
			self.serviceFile="sharepoint_%s.service"%self.folderSuffixName.lower()

		if not os.path.exists(os.path.join(self.userSystemdPath,self.serviceFile)):
			shutil.copyfile(self.serviceTemplatePath,os.path.join(self.userSystemdPath,self.serviceFile))
			configFile=configparser.ConfigParser()
			configFile.optionxform=str
			configFile.read(os.path.join(self.userSystemdPath,self.serviceFile))
			tmpCommand=configFile.get("Service","ExecStart")
			tmpCommand=tmpCommand.replace("{{CONF_PATH}}",self.spaceConfPath)
			configFile.set("Service","ExecStart",tmpCommand)
			with open(os.path.join(self.userSystemdPath,self.serviceFile),'w') as fd:
				configFile.write(fd)

		self.manageAutostart(True,self.spaceConfPath,self.serviceFile)
				
	#def _createSpaceServiceUnit

	def _updateOneDriveConfig(self,spaceInfo):

		tmp={}
		tmp["email"]=spaceInfo[0]
		tmp["type"]=spaceInfo[1]
		tmp["sharepoint"]=spaceInfo[2]
		tmp["library"]=spaceInfo[3]
		tmp["localFolder"]=os.path.basename(self.spaceLocalFolder)
		tmp["configPath"]=self.spaceConfPath
		tmp["systemd"]=self.serviceFile
		if spaceInfo[4]!=None:
			tmp["drive_id"]=spaceInfo[4]
		else:
			tmp["drive_id"]=""

		self.onedriveConfig["spacesList"].append(tmp)
		with open(self.onedriveConfigFile,'w') as fd:
			json.dump(self.onedriveConfig,fd)

	#def _updateOneDriveConfig

	def _manageEmptyToken(self):

		emptyToken=os.path.join(self.spaceConfPath,'".emptyToken"')
		f=open(emptyToken,'w')
		f.close()

	#def _manageEmptyToken

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

	def getInitialDownload(self,spaceConfPath=None):

		if spaceConfPath==None:
			spaceConfPath=self.spaceConfPath
	
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

		for item in self.onedriveConfigFile['spacesList']:
			if item["localFolder"]==spaceName:
				self.spaceLocalFolder=item["localFolder"]
				self.spaceConfPath=item["configPath"]
				self.spaceServiceFile=item["systemd"]
				break

		spaceConfigFilePath=os.path.join(self.spaceConfPath,'config')
		self.readSpaceConfigFile(spaceConfigFilePath)
		if not self.isAutoStartEnabled(self.spaceServiceFile):
			self.autoStartEnabled=False
			self.currentConfig[0]=False
		else:
			self.autoStartEnabled=True
			self.currentConfig[0]=True

		if self.existsFilterFile():
			self.syncAll=False
			self.readFilterFile(self.spaceConfPath)
			self.currentSyncConfig[0]=self.syncAll
			self.currentSyncConfig[1]=self.foldersSelected
			self.currentSyncConfig[2]=self.foldersUnSelected
		else:
			self.synAll=True
			self.foldersSelected=[]
			self.foldersUnSelected=[]
		
	#def loadSpaceSettings

	def readFilterFile(self,spaceConfPath):

		self.includeFolders=[]
		self.excludeFolders=[]
		self.foldersSelected=[]
		self.foldersUnSelected=[]

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

	def isOnedriveRunning(self,spaceConfPath):

		onedriveCommand='onedrive --monitor --confdir="%s"'%spaceConfPath

		if os.system('ps -ef | grep "%s" | grep -v "grep" 1>/dev/null'%onedriveCommand)==0:
			return True
		else:
			return False

	#def isOnedriveRunning

	def isAutoStartEnabled(self,serviceFile):

		tmpService=os.path.join(self.userSystemdPath,"serviceFile")
		tmpAutoStartService=os.path.join(self.userSystemdAutoStartPath,"serviceFile")

		if os.path.exists(tmpService) and os.path.exists(tmpAutoStartService):
			return True

		return False

	#def isAutoStartEnabled

	def manageAutostart(self,enable,spaceConfPath,serviceUnit):

		isOnedriveRunning=self.isOnedriveRunning(spaceConfPath)
		serviceUnit=os.path.join(self.userSystemdPath,serviceUnit)

		if enable:
			cmd="systemctl --user enable %s"%serviceUnit
			
		else:
			cmd="systemctl --user disable %s"%serviceUnit

		p=subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
		poutput=p.communicate()
		rc=p.returncode

		if rc !=0:
			return True
		else:
			return False
	
	#def manageAutostart


#class OnedriveManager
