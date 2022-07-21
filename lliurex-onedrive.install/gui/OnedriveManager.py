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
import hashlib


class OnedriveManager:
	
	def __init__(self):

		self.user=os.environ["USER"]
		self.llxOnedriveConfigDir="/home/%s/.config/lliurex-onedrive-config/"%(self.user)
		self.onedriveConfigFile=os.path.join(self.llxOnedriveConfigDir,"onedriveConfig.json")
		self.onedriveConfig={}
		self.spacesConfigData=[]
		self.sharePointsConfigData=[]
		self.librariesConfigData=[]
		#self.authUrl="https://login.microsoftonline.com/common/oauth2/v2.0/authorize?client_id=d50ca740-c83f-4d1b-b616-12c519384f0c&scope=Files.ReadWrite%20Files.ReadWrite.all%20Sites.Read.All%20Sites.ReadWrite.All%20offline_access&response_type=code&redirect_uri=https://login.microsoftonline.com/common/oauth2/nativeclient"
		self.userTokenPath="/home/%s/.onedriveAuth/"%(self.user)
		self.configTemplatePath="/usr/share/lliurex-onedrive/llx-data/config"
		self.serviceTemplatePath="/usr/share/lliurex-onedrive/llx-data/template.service"
		self.userSystemdPath="/home/%s/.config/systemd/user"%self.user
		self.userSystemdAutoStartPath=os.path.join(self.userSystemdPath,"default.target.wants")
		self.aCServicePath="/usr/share/lliurex-onedrive/llx-data/"
		self.aCServiceFile="lliurex-onedrive-ac.service"
		self.onedriveConfigDir="/home/%s/.config/onedrive"%self.user
		#self.sharePointConfigDir="/home/%s/.config/sharepoint"%self.user
		#self.sharedFolderConfigDir="/home/%s/.config/sharedfolder"%self.user
		self.spaceBasicInfo=[]
		self.spaceLocalFolder=""
		self.spaceSuffixName=""
		self.folderSuffixName=""
		self.spaceConfPath=""
		self.tempConfigPath=""
		self.customizeConfigParam=['monitor_interval','rate_limit',"skip_size"]
		self.bandWidth=[{"name":"128 KB/s","value":"131072"},{"name":"256 KB/s","value":"262144"},{"name":"512 KB/s","value":"524288"},{"name":"1 MB/s","value":"1048576"},{"name":"10 MB/s","value":"10485760"},{"name":"20 MB/s","value":"20971520"},{"name":"30 MB/s","value":"31457280"},{"name":"50 MB/s","value":"52428800"},{"name":"100 MB/s","value":"104857600"}]
		self.bandWidthNames=[]
		for item in self.bandWidth:
			self.bandWidthNames.append(item["name"])
		self.maxFileSize=[{"name":"50 MB","value":"50"},{"name":"75 MB","value":"75"},{"name":"100 MB","value":"100"},{"name":"150 MB","value":"150"},{"name":"250 MB","value":"250"},{"name":"500 MB","value":"500"},{"name":"1 GB","value":"1024"},{"name":"2 GB","value":"2048"},{"name":"5 GB","value":"5120"},{"name":"10 GB","value":"10240"},{"name":"15 GB","value":"15360"},{"name":"20 GB","value":"20480"},{"name":"25 GB","value":"20480"},{"name":"50 GB","value":"51200"},{"name":"100 GB","value":"102400"}]
		self.maxFileSizeNames=[]
		for item in self.maxFileSize:
			self.maxFileSizeNames.append(item["name"])
		self.autoStartEnabled=True
		self.rateLimit=4
		self.monitorInterval=1
		self.skipSize=[False,0]
		self.currentConfig=[self.autoStartEnabled,self.monitorInterval,self.rateLimit,self.skipSize]
		self.syncAll=True
		self.filterFileName="sync_list"
		self.filterFileHashName=".sync_list.hash"
		self.foldersSelected=[]
		self.foldersUnSelected=[]
		self.includeFolders=[]
		self.excludeFolders=[]
		self.showFolderStruct=False
		self.currentSyncConfig=[self.syncAll,self.foldersSelected,self.foldersUnSelected]
		self.envConfFiles=[".config.backup",".config.hash","items.sqlite3","items.sqlite3-shm","items.sqlite3-wal",".emptyToken",".statusToken",".localFolderEmptyToken",".localFolderRemovedToken",".runToken"]
		self.globalOneDriveFolderWarning=False
		self.globalOneDriveStatusWarning=False
		self.correctStatusCode=[0,1,2]
		self.oldConfigPath=os.path.join(self.onedriveConfigDir,"refresh_token")
		self.filesToMigrate=["items.sqlite3","sync_list",".sync_list.hash","refresh_token"]
		self.oldFilesToDelete=["config",".config.backup",".config.hash","items.sqlite3-shm","items.sqlite3-wal",".emptyToken",".statusToken",".localFolderEmptyToken",".localFolderRemovedToken"]
		self.freeSpaceWarningToken=os.path.join(self.llxOnedriveConfigDir,".hddWarningToken")
		self.freeSpaceErrorToken=os.path.join(self.llxOnedriveConfigDir,".hddErrorToken")
		self.oneDriveDirectoryFile="/usr/share/lliurex-onedrive/llx-data/directoryOneDrive"
		self.organizationDirectoryFile="/usr/share/lliurex-onedrive/llx-data/directoryOrganization"
		self.sharePointDirectoryFile="/usr/share/lliurex-onedrive/llx-data/directorySharePoint"
		self.createEnvironment()
		self.clearCache()


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

		'''
		if not os.path.exists(self.sharePointConfigDir):
			os.mkdir(self.sharePointConfigDir)

		if not os.path.exists(self.sharedFolderConfigDir):
			os.mkdir(self.sharedFolderConfigDir)
		'''
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
		countStatus=0
		countFolder=0
		

		for item in spaces:
			tmp={}
			tmp["id"]=item["id"]
			tmp["name"]=os.path.basename(item["localFolder"])
			status=int(self._readSpaceStatusToken(item['configPath'])[1])
			if status not in self.correctStatusCode:
				countStatus+=1
			tmp["status"]=status
			tmp["isRunning"]=self.isOnedriveRunning(item['configPath'])
			localFolderWarning=self.checkLocalFolder(item['configPath'])
			warning=False
			if localFolderWarning[0] or localFolderWarning[1]:
				countFolder+=1
				warning=True
			tmp["localFolderWarning"]=warning
			self.spacesConfigData.append(tmp)
		
		if countFolder>0:
			self.globalOneDriveFolderWarning=True
		else:
			self.globalOneDriveFolderWarning=False

		if countStatus>0:
			self.globalOneDriveStatusWarning=True
		else:
			self.globaOneDriveStatusWarning=False

	#def getSpacesConfig

	def _readSpaceStatusToken(self,spaceConfPath):

		error=False
		code=0
		freeSpace=''

		spaceStatusToken=os.path.join(spaceConfPath,".statusToken")

		if os.path.exists(spaceStatusToken):
			with open(spaceStatusToken,'r') as fd:
				lines=fd.readlines()

			if len(lines)==3:
				error=lines[0].strip()
				code=lines[1].strip()
				freeSpace=lines[2].strip()
				if freeSpace!="":
					freeSpace=self._formatFreeSpace(freeSpace)

		return [error,code,freeSpace]

	#def readSpaceStatusToken

	def initSpacesSettings(self):

		self.spaceBasicInfo=[]
		self.spaceId=""
		self.spaceLocalFolder=""
		self.spaceConfPath=""
		self.spaceServiceFile=""
		self.spaceSuffixName=""
		self.folderSuffixName=""
		self.tempConfigPath=""	
		self.tmpConfDir=""
		self.sharePointsConfigData=[]
		self.librariesConfigData=[]
		self.autoStartEnabled=True
		self.spaceAccountType=""
		self.initialDownload=""
		self.rateLimit=4
		self.monitorInterval=1
		self.skipSize=[False,0]
		self.currentConfig=[self.autoStartEnabled,self.monitorInterval,self.rateLimit,self.skipSize]
		self.freeSpace=""
		self.accountStatus=0
		self.filterFile=""
		self.filerFileHash=""
		self.errorFolder=False
		self.folderStruct=[]
		self.foldersSelected=[]
		self.foldersUnSelected=[]
		self.includeFolders=[]
		self.excludeFolders=[]
		self.syncAll=True
		self.currentSyncConfig=[self.syncAll,self.foldersSelected,self.foldersUnSelected]
		self.localFolderEmpty=False
		self.localFolderRemoved=False
		self.showFolderStruct=False
	
	#def initSpacesSettings

	def checkIfEmailExists(self,email):

		for item in self.onedriveConfig["spacesList"]:
			if item["email"]==email:
				tokenPath=os.path.join(item["configPath"],'refresh_token')
				if os.path.exists(tokenPath):
					return True
		return False

	#def checkIfEmailExists

	def getSpaceSharePoints(self,email):

		self.sharePointsConfigData=[]
		self.tmpConfDir=""
		
		for item in self.onedriveConfig["spacesList"]:
			if item["email"]==email:
				self.tmpConfDir=item["configPath"]
				break

		if self.tmpConfDir=="":
			ret=self.createTempConfig("sharepoint")
			if ret:
				if os.path.exists(os.path.join(self.tempConfigPath,'refresh_token')):
					self.tmpConfDir=self.tempConfigPath
				else:
					return False
			else:
				return False

		cmd='onedrive --get-O365-drive-id "listAllSharePoints" --dry-run --confdir="%s"'%(self.tmpConfDir)
		p=subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
		pout,perror=p.communicate()

		if len(pout)>0:
			pout=pout.decode().split("\n")
			for item in pout:
				if "*" in item:
					self.sharePointsConfigData.append(item.split("*")[1].strip())

		return True

	#def getSpaceSharePoints
	
	def getSharePointLibraries(self,sharePoint):

		self.librariesConfigData=[]
		
		cmd='onedrive --get-O365-drive-id "%s" --dry-run --confdir="%s"'%(sharePoint,self.tmpConfDir)
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
		driveId=spaceInfo[4]
		
		duplicateSpace=False
		existsMail=False

		if self.checkIfEmailExists(spaceEmail):
			existsMail=True
			if spaceType=="onedrive":
				for item in self.onedriveConfig["spacesList"]:
					if item["email"]==spaceEmail and item["spaceType"]=="onedrive":
						duplicateSpace=True
						break
			elif spaceType=="sharepoint":
				for item in self.onedriveConfig["spacesList"]:
					if item["driveId"]==driveId:
						duplicateSpace=True
						break
	
		return [duplicateSpace,existsMail]

	#def checkDuplicate

	def checkPreviousLocalFolder(self,spaceInfo):

		self.spaceLocalFolder=""

		self._getSpaceSuffixName(spaceInfo)

		if spaceInfo[1]=="onedrive":
			self.spaceLocalFolder="/home/%s/OneDrive-%s"%(self.user,self.spaceSuffixName)
		else:
			self.spaceLocalFolder="/home/%s/%s/%s"%(self.user,self.spaceSuffixName,self.folderSuffixName)
		
		if os.path.exists(self.spaceLocalFolder):
			if os.listdir(self.spaceLocalFolder):
				return True

		return False

	#def checkPreviousLocalFolder

	def createToken(self,token,authUrl):
		
		if not os.path.exists(self.userTokenPath):
			os.mkdir(self.userTokenPath)

		self.urlDoc=os.path.join(self.userTokenPath,"urlToken")
		self.tokenDoc=os.path.join(self.userTokenPath,"keyToken")
		with open(self.urlDoc,'w') as fd:
			fd.write(authUrl)
		with open(self.tokenDoc,'w') as fd:
			fd.write(token)

	#def createToken

	def createSpace(self,spaceInfo,reuseToken):

		spaceEmail=spaceInfo[0]
		spaceAccounType=""
		spaceType=spaceInfo[1]
		spaceName=spaceInfo[2]
		spaceLibrary=spaceInfo[3]
		spaceDriveId=spaceInfo[4]

		self.spaceBasicInfo=[spaceEmail,spaceAccounType,spaceType,spaceName,spaceLibrary]
		
		if not os.path.exists(os.path.join(self.userSystemdPath,self.aCServiceFile)):
			ret=self._stopOldService()
		
		self._createSpaceConfFolder(spaceType,spaceDriveId)
		
		if reuseToken:
			self._copyToken(spaceEmail)
			if spaceType=="sharepoint":
				if os.path.exists(self.tempConfigPath) and len(self.tempConfigPath)>0:
					self.deleteTempConfig()
		else:
			cmd='/usr/bin/onedrive --auth-files %s:%s --confdir="%s"'%(self.urlDoc,self.tokenDoc,self.spaceConfPath)
			p=subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
			poutput=p.communicate()
			rc=p.returncode
			if rc not in [0,1]:
				return False
			else:
				if not os.path.exists(os.path.join(self.spaceConfPath,'refresh_token')):
					return False

		self._manageEmptyToken()
		self._createSpaceServiceUnit(spaceType)
		self._createOneDriveACService()
		if self.isConfigured():
			self.getInitialDownload()
		self._updateOneDriveConfig(spaceInfo)
		self._createAuxVariables()
		self._addDirectoryFile(spaceType)
		self.loadOneDriveConfig()

		return True

	#def createSpace 

	def _createSpaceConfFolder(self,spaceType,spaceDriveId):

		self.spaceConfPath=""
		createConfig=False

		if spaceType=="onedrive":
			tmpFolder="onedrive_%s"%self.spaceSuffixName.lower()
			self.spaceConfPath=os.path.join(self.onedriveConfigDir,tmpFolder)
			if not os.path.exists(self.spaceConfPath):
				createConfig=True
		else:
			tmpSuffixName=re.sub('[^0-9a-zA-Z]+', '_',self.folderSuffixName).lower()
			tmpFolder="sharepoint_%s"%tmpSuffixName
			self.spaceConfPath=os.path.join(self.onedriveConfigDir,tmpFolder)
			if not os.path.exists(self.spaceConfPath):
				createConfig=True 

		if not createConfig:
			spaceConfigFilePath=os.path.join(self.spaceConfPath,'config')
			customParam=self.readSpaceConfigFile(spaceConfigFilePath)
		else:
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
						newLine='drive_id = "%s"'%spaceDriveId
						tmpLine=line.replace('# drive_id = ""',newLine)
						fd.write(tmpLine)
					else:
						fd.write(line)
		
		if not createConfig:
			self.updateConfigFile(customParam)

	#def _createSpaceConfFolder

	def readSpaceConfigFile(self,spaceConfigFilePath):

		if os.path.exists(spaceConfigFilePath):
			customParam=self._readCustomParams(spaceConfigFilePath)
			self.monitorInterval="{:.0f}".format(int(customParam['monitor_interval'])/60)
			self.currentConfig[1]=self.monitorInterval

			for i in range(len(self.bandWidth)):
				if self.bandWidth[i]["value"]==customParam['rate_limit']:
					self.rateLimit=i
					self.currentConfig[2]=self.rateLimit
					break

			self.skipSize[0]=customParam['skip_size'][0]

			for i in range(len(self.maxFileSize)):
				if self.maxFileSize[i]["value"]==customParam['skip_size'][1]:
					self.skipSize[1]=i
					self.currentConfig[3]=self.skipSize
					break
			
			return customParam

	#def readConfigFile

	def _readCustomParams(self,spaceConfigFilePath):

		customParam={}

		if os.path.exists(spaceConfigFilePath):
			customParam["skip_size"]=[False,10]
			with open(spaceConfigFilePath,'r') as fd:
				lines=fd.readlines()
				for line in lines:
					for param in self.customizeConfigParam:
						tmpLine=line.split("=")
						if param=="skip_size":
							if "skip_size" in tmpLine[0]:
								tmpValue=[]
								if "#" in tmpLine[0].strip():
									tmpValue.append(False)
								else:
									tmpValue.append(True)
								tmpValue.append(tmpLine[1].split("\n")[0].strip().split('"')[1])
								customParam[param]=tmpValue
						else:
							if param==tmpLine[0].strip():
								value=tmpLine[1].split("\n")[0].strip().split('"')[1]
								customParam[param]=value

		return customParam 

	#def _readCustomParams

	def updateConfigFile(self,customParam):

		configFile=os.path.join(self.spaceConfPath,'config')

		if os.path.exists(configFile):
			with open(configFile,'r') as fd:
				lines=fd.readlines()

			with open(configFile,'w') as fd:
				for line in lines:
					for param in customParam:
						tmpLine=line.split("=")
						if param=="skip_size":
							if "skip_size" in tmpLine[0]:
								if customParam[param][0]:
									value=tmpLine[1].split("\n")[0].strip().split('"')[1]
									if value!=customParam[param][1]:
										line=param+' = '+'"'+customParam[param][1]+'"\n'
								else:
									if "#" not in tmpLine[1]:
										line='# '+param+' = '+'"'+customParam[param][1]+'"\n'
						else:
							if param==tmpLine[0].strip():
								value=tmpLine[1].split("\n")[0].strip().split('"')[1]
								if value!=customParam[param]:
									line=param+' = '+'"'+customParam[param]+'"\n'
								break
					
					fd.write(line)

	#def updateConfigFile

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
			self.spaceServiceFile="onedrive_%s.service"%self.spaceSuffixName.lower()
		else:
			tmpSuffixName=re.sub('[^0-9a-zA-Z]+', '_',self.folderSuffixName).lower()
			self.spaceServiceFile="sharepoint_%s.service"%tmpSuffixName

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

	def _createOneDriveACService(self):

		if not os.path.exists(os.path.join(self.userSystemdPath,self.aCServiceFile)):
			shutil.copyfile(os.path.join(self.aCServicePath,self.aCServiceFile),os.path.join(self.userSystemdPath,self.aCServiceFile))
			cmd="systemctl --user enable %s"%self.aCServiceFile
			os.system(cmd)
			cmd="systemctl --user start %s"%self.aCServiceFile
			os.system(cmd)

	#def _createOneDriveACService

	def _updateOneDriveConfig(self,spaceInfo):

		tmp={}
		h=hashlib.md5()
		tmpId=spaceInfo[0]+"_"+os.path.basename(self.spaceLocalFolder)
		h.update(tmpId.encode("utf-8"))
		tmp["id"]=h.hexdigest()
		tmp["email"]=spaceInfo[0]
		tmp["accountType"]=self.spaceAccountType
		tmp["spaceType"]=spaceInfo[1]
		tmp["sharepoint"]=spaceInfo[2]
		tmp["library"]=spaceInfo[3]
		tmp["localFolder"]=self.spaceLocalFolder
		tmp["configPath"]=self.spaceConfPath
		tmp["systemd"]=self.spaceServiceFile
		if spaceInfo[4]!=None:
			tmp["driveId"]=spaceInfo[4]
		else:
			tmp["driveId"]=""

		self.spaceId=tmp["id"]
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
		self.lockAutoStartToken=os.path.join(self.spaceConfPath,".lockAutoStartToken")

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
		tmpOrganization=email.split('@')[1]
		if 'edu.gva' in tmpOrganization:
			tmpOrganization="EduGva"
		else:
			tmpOrganization=tmpOrganization.split(".")[0].lower().capitalize()
		
		self.spaceSuffixName=tmpOrganization+"_"+tmpName
		
		if spaceType=="sharepoint":
			tmpSharePoint=self._stripAccents(spaceName)
			tmpSharePoint=re.sub('[^0-9a-zA-Z]+', '_', tmpSharePoint)
			tmpLibrary=self._stripAccents(spaceLibrary)
			tmpLibrary=re.sub('[^0-9a-zA-Z]+', '_', tmpLibrary)
			self.folderSuffixName=tmpSharePoint+"-"+tmpLibrary

	#def _getSpaceSuffixName

	def _stripAccents(self,text):

		try:
			text = unicode(text, 'utf-8')
		except NameError:
			pass

		text = unicodedata.normalize('NFD', text).encode('ascii', 'ignore').decode("utf-8")

		return str(text)

	#def _stripAccents

	def createTempConfig(self,tmpType):

		self.deleteTempConfig()
		if tmpType=="sharepoint":
			self.tempConfigPath=tempfile.mkdtemp("_sharepoint")
		
		self.tempFolder=os.path.join(self.tempConfigPath,tmpType)

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

	def deleteTempConfig(self):

		if os.path.exists(self.tempConfigPath):
			cmd='onedrive --logout --confdir="%s"'%self.tempConfigPath
			p=subprocess.run(cmd,shell=True,check=True)
			shutil.rmtree(self.tempConfigPath)

	#def deleteTempConfig

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

		self.initialDownload=""
		self.spaceAccountType=""

		cmd='/usr/bin/onedrive --display-sync-status --dry-run --verbose --confdir="%s"'%(self.spaceConfPath)
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
						self.initialDownload=self._formatInitialDownload(tmpLine)
				elif 'Account Type:' in line:
					self.spaceAccountType=line.split(":")[1].strip()
		
		#return download

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

	def loadSpaceSettings(self,spaceId):

		self.initSpacesSettings()
		matchSpace=False
		for item in self.onedriveConfig['spacesList']:
			if item["id"]==spaceId:
				self.spaceId=spaceId
				self.spaceBasicInfo=[item["email"],item["accountType"],item["spaceType"],item["sharepoint"],item["library"]]
				self.spaceLocalFolder=item["localFolder"]
				self.spaceConfPath=item["configPath"]
				self.spaceServiceFile=item["systemd"]
				matchSpace=True
				break

		if matchSpace:
			self._createAuxVariables()
			spaceConfigFilePath=os.path.join(self.spaceConfPath,'config')
			self.readSpaceConfigFile(spaceConfigFilePath)
			if not self.isAutoStartEnabled():
				self.autoStartEnabled=False
				self.currentConfig[0]=False

			if self.existsFilterFile():
				self.syncAll=False
				self.readFilterFile()
			else:
				self.syncAll=True

			self.showFolderStruct!=self.syncAll
			self.currentSyncConfig[0]=self.syncAll
			self.currentSyncConfig[1]=self.foldersSelected
			self.currentSyncConfig[2]=self.foldersUnSelected

			statusInfo=self._readSpaceStatusToken(self.spaceConfPath)
			self.accountStatus=int(statusInfo[1])
			self.freeSpace=statusInfo[2]
			self.localFolderEmpty,self.localFolderRemoved=self.checkLocalFolder(self.spaceConfPath)
			
			return True
		return False
		
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

	def readFilterFile(self):

		self.includeFolders=[]
		self.excludeFolders=[]

		filterFile=os.path.join(self.spaceConfPath,self.filterFile)

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

	def isOnedriveRunning(self,spaceConfPath=None,oldCommand=False):

		if spaceConfPath==None:
			spaceConfPath=self.spaceConfPath

		if oldCommand:
			onedriveCommand='onedrive --monitor'
		else:	
			onedriveCommand='onedrive --monitor --confdir="%s"'%spaceConfPath

		if os.system('ps -ef | grep "%s" | grep -v "grep" 1>/dev/null'%onedriveCommand)==0:
			return True
		else:
			return False

	#def isOnedriveRunning

	def isAutoStartEnabled(self):

		tmpService=os.path.join(self.userSystemdPath,self.spaceServiceFile)
		tmpAutoStartService=os.path.join(self.userSystemdAutoStartPath,self.spaceServiceFile)

		if os.path.exists(tmpService):
			if os.path.exists(tmpAutoStartService) or os.path.exists(self.lockAutoStartToken):
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

	def manageSync(self,startSync):

		result=[True,True]
		ok=True

		if startSync:
			self.manageFileFilter("restore")
			if os.path.exists(self.lockAutoStartToken):
				ret=self.manageAutostart(True)
			cmd="systemctl --user start %s"%self.spaceServiceFile
		else:
			cmd="systemctl --user stop %s"%self.spaceServiceFile

		try:
			if os.path.exists(self.localFolderEmptyToken):
				self._manageEmptyToken()
			p=subprocess.run(cmd,shell=True,check=True)
		except subprocess.CalledProcessError as e:
			ok=False
			pass
		
		isOnedriveRunning=self.isOnedriveRunning()
		
		if (startSync and isOnedriveRunning) or (not startSync and not isOnedriveRunning):
			self._updateSpaceConfigData("isRunning",isOnedriveRunning)
			return[ok,isOnedriveRunning]
		else:
			return[ok,isOnedriveRunning]

	#def manageSync

	def getAccountStatus(self,spaceConfPath=None,spaceType=None):

		if spaceConfPath==None:
			spaceConfPath=self.spaceConfPath

		if spaceType==None:
			spaceType=self.spaceBasicInfo[2]

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
		INFORMATION_NOT_AVAILABLE=3
		UPLOADING_PENDING_CHANGES=4

		error=False
		code=INFORMATION_NOT_AVAILABLE=3

		freespace=""
		pendingChanges="0 KB"
		lastPendingChanges="0 KB"


		if self.isConfigured():
			lastPendingChanges=self._getLastPendingChanges()
			cmd='/usr/bin/onedrive --display-sync-status --verbose --dry-run --confdir="%s"'%self.spaceConfPath
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
						else:
							error=False
					elif 'database' in item:
						code=DATABASE_ERROR
					elif 'Unauthorized' in item:
						code=UNAUTHORIZED_ERROR
					elif '416' in item:
						code=UPLOADING_PENDING_CHANGES
						break
					elif 'Unable to query OneDrive' in item:
						code=UNAUTHORIZED_ERROR
						break
					elif '503' in item:
						code=SERVICE_UNAVAILABLE
					elif 'Free Space' in item:
						tmp_freespace=item.split(':')[1].strip()
						if not 'Not Available' in tmp_freespace:
							freespace=self._formatFreeSpace(tmp_freespace)

			if not error and len(poutput)>0:
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
					elif 'download from OneDrive:' in item:
						pendingChanges=item.split(':')[1].strip()
					elif 'Free Space' in item:
						tmp_freespace=item.split(':')[1].strip()
						if not 'Not Available' in tmp_freespace:
							freespace=self._formatFreeSpace(tmp_freespace)

		else:
			error=True
			code=WITH_OUT_CONFIG

		if code==OUT_OF_SYNC_MSG:
			if pendingChanges==lastPendingChanges:
				code=ALL_SYNCHRONIZE_MSG
	
		if error:
			paramValue=1
		else:
			paramValue=0

		self._updateSpaceConfigData('status',paramValue)
		return [error,code,freespace]

	#def getAccountStatus
	
	def _updateSpaceConfigData(self,param,value,spaceId=None):

		if spaceId==None:
			spaceId=self.spaceId

		for item in self.spacesConfigData:
			if item["id"]==spaceId:
				if item[param]!=value:
					item[param]=value
				break		

	#def _updateSpaceInfo	

	def removeAccount(self):

		self.organizationFolder=""

		if self.isOnedriveRunning():
			ret=self.manageSync(False)
			
		if not self.isOnedriveRunning():
			cmd='/usr/bin/onedrive --logout --confdir="%s" &'%self.spaceConfPath
			p=subprocess.run(cmd,shell=True,check=True)
			time.sleep(2)
			if not self.isConfigured():
				self._removeSystemdConfig()
				self._removeEnvConfigFiles()
				self.organizationFolder=os.path.dirname(self.spaceLocalFolder)
				if os.path.exists(os.path.join(self.spaceLocalFolder,".directory")):
					os.remove(os.path.join(self.spaceLocalFolder,".directory"))
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

	#def _removeSystemdConfig

	def removeACService(self):

		if len(self.onedriveConfig["spacesList"])==0:
			if os.path.exists(os.path.join(self.userSystemdAutoStartPath,self.aCServiceFile)):
				cmd="systemctl --user stop %s"%self.aCServiceFile
				os.system(cmd)
				cmd="systemctl --user disable %s"%self.aCServiceFile
				os.system(cmd)
				os.remove(os.path.join(self.userSystemdPath,self.aCServiceFile))

	#def removeACService

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

	def checkLocalFolder(self,spaceConfPath):

		localFolderEmpty=False;
		localFolderRemoved=False;

		localFolderEmptyToken=os.path.join(spaceConfPath,".localFolderEmptyToken")
		localFolderRemovedToken=os.path.join(spaceConfPath,".localFolderRemovedToken")
		
		if os.path.exists(localFolderEmptyToken):
			localFolderEmpty=True;
		if os.path.exists(localFolderRemovedToken):
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

		cmd='onedrive --synchronize --resync --resync-auth --dry-run --verbose --skip-file="*.*" --confdir="%s"'%self.spaceConfPath
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

	def applySyncChanges(self,initialSyncConfig,keepFolders):

		syncAll=initialSyncConfig[0]
		foldersSelected=initialSyncConfig[1]
		foldersUnSelected=initialSyncConfig[2]

		if not syncAll:
			self.createFilterFile(foldersSelected,foldersUnSelected)
			if not keepFolders:
				self._manageEmptyToken()
				if os.path.exists(self.spaceLocalFolder):
					shutil.rmtree(self.spaceLocalFolder)
			self.readFilterFile()
		else:
			#foldersSelected=[]
			#foldersUnSelected=[]
			if os.path.exists(self.filterFile):
				os.remove(self.filterFile)
			if os.path.exists(self.filterFileHash):
				os.remove(self.filterFileHash)

			#self.folderStruct=[]

		self.currentSyncConfig[0]=syncAll
		self.currentSyncConfig[1]=foldersSelected
		self.currentSyncConfig[2]=foldersUnSelected
		self.folderStructBack=copy.deepcopy(self.folderStruct)

		ret=self._syncResync()
		return ret

	#def applySyncChanges

	def createFilterFile(self,foldersSelected,foldersUnSelected):

		folderSelected=[]
		folderUnSelected=[]
		
		for item in self.folderStruct:
			count=0
			if item["isChecked"]:
				if item["path"] not in foldersUnSelected and item["path"] not in foldersSelected:
					if item["type"]=="OneDrive":
						for element in foldersUnSelected:
							if item["path"] in element:
								break
							else:
								count+=1
						if count>0:
							folderSelected.append(item["path"]+"/*")

		
		for i in range(len(foldersUnSelected)-1,-1,-1):
			for element in foldersSelected:
				if len(self.includeFolders)>0:
					tmp=foldersUnSelected[i]+"/*"
					if tmp in self.includeFolders:
						self.includeFolders.remove(tmp)
				try:
					tmpFolder=foldersUnSelected[i]+"/"
					if tmpFolder in element:
						foldersUnSelected.pop(i)
				except:
					pass

		
		for element in foldersSelected:
			folderSelected.append(element+"/*")

		for element in foldersUnSelected:
			folderUnSelected.append("!"+element+"/*")
					
		
		if not self.existsFilterFile():
			with open(self.filterFile,'w') as fd:
				
				for item in folderUnSelected:
					tmpLine=item+"\n"
					fd.write(tmpLine)

				for item in folderSelected:
					tmpLine=item+"\n"
					fd.write(tmpLine)
				fd.close()
		else:
			for item in folderUnSelected:
				if item not in self.excludeFolders:
					self.excludeFolders.append(item)
			
			for item in folderSelected:
				if item not in self.includeFolders:
					self.includeFolders.append(item)
			
			for i in range(len(self.excludeFolders)-1,-1,-1):
				tmpLine=self.excludeFolders[i].split("!")[1]
				match=0
				if tmpLine in folderSelected:
					self.excludeFolders.pop(i)
				else:
					for item in self.folderStruct:
						tmpItem=item["path"]+"/*"
						if tmpItem==tmpLine:
							match=0
							break
						else:
							match+=1
					if match>0:
						self.excludeFolders.pop(i)
			
			for i in range(len(self.includeFolders)-1,-1,-1):
				tmpLine="!"+self.includeFolders[i]
				match=0
				if tmpLine in folderUnSelected:
					self.includeFolders.pop(i)
				else:
					for item in self.folderStruct:
						tmpItem="!"+item["path"]+"/*"
						if tmpItem==tmpLine:
							match=0
							break
						else:
							match+=1
					if match>0:
						self.includeFolders.pop(i)
			
			for i in range(len(self.excludeFolders)-1,-1,-1):
				for element in self.includeFolders:
					try:
						tmp=self.excludeFolders[i].split("!")[1].split("/*")[0]+"/"
						if tmp in element:
							self.excludeFolders.pop(i)
					except:
						pass

			with open(self.filterFile,'w') as fd:
				
				for element in self.excludeFolders:
					fd.write(element+"\n")
				
				for element in self.includeFolders:
					fd.write(element+"\n")
				
				fd.close()
	
	#def createFilterFile

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

	def updateCheckFolder(self,path,checked):

		for item in self.folderStruct:
			if item["path"]==path:
				item["isChecked"]=checked

	#def updateCheckFolder

	def cancelSyncChanges(self):

		if self.folderStruct!=self.folderStructBack:
			self.folderStruct=copy.deepcopy(self.folderStructBack)

	#def cancelSyncChanges

	def applySettingsChanges(self,value):

		SYSTEMD_ERROR=-10
		WRITE_CONFIG_ERROR=-20
		MULTIPLE_SETTINGS_ERROR=-30

		errorSD=False
		errorMI=False
		errorRL=False
		errorSS=False

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
			
		if value[3]!=self.currentConfig[3]:
			errorSS=self.manageSkipSize(value[3])
			if not errorSS:
				self.currentConfig[3]=value[3]

		if errorSD and not errorMI and not errorRL and not errorSS:
			return[True,SYSTEMD_ERROR]

		elif errorSD and (errorMI or errorRL or errorSS):
			return [True,MULTIPLE_SETTINGS_ERROR]

		elif not errorSD and (errorMI or errorRL or errorSS):
			return [True,WRITE_CONFIG_ERROR]

		elif not errorSD and errorMI and errorRL and errorSS:
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

	def manageSkipSize(self,value):

		value[1]=self.maxFileSize[value[1]]["value"]
		return self._writeConfigFile('skip_size',value)

	#def manageSkipSize


	def _writeConfigFile(self,param,value):

		configFile=os.path.join(self.spaceConfPath,'config')
		self.matchParam=True
		if param=="skip_size":
			self.matchParam=False
		if os.path.exists(configFile):
			try:
				with open(configFile,'r') as fd:
					lines=fd.readlines()
					fd.close()

				with open(configFile,'w') as fd:

					for line in lines:
						if  param in line:
							if param =="skip_size":
								self.matchParam=True
								if value[0]: 
									tmpLine=param+' = '+'"'+value[1]+'"\n'
								else:
									tmpLine='# '+param+' = '+'"'+value[1]+'"\n'
							else:
								tmpLine=param+' = '+'"'+value+'"\n'
							
							fd.write(tmpLine)
						else:
							fd.write(line)

					if not self.matchParam:
						if value[0]: 
							line=param+' = '+'"'+value[1]+'"\n'
						else:
							line='# '+param+' = '+'"'+value[1]+'"\n'
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
		cmd='/usr/bin/onedrive --display-sync-status --verbose --dry-run --confdir="%s" >>%s 2>&1'%(self.spaceConfPath,self.testPath)
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

	def updateSpaceAuth(self):

		cmd='/usr/bin/onedrive --reauth --auth-files %s:%s --confdir="%s"'%(self.urlDoc,self.tokenDoc,self.spaceConfPath)
		p=subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
		poutput=p.communicate()
		rc=p.returncode
		if rc not in [0,1]:
			return False

		return True

	#def updateSpaceAuth

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

	def updateGlobalLocalFolderInfo(self):

		count=0

		for item in self.onedriveConfig["spacesList"]:
			tmpSpaceId=item["id"]
			tmpConfigPath=item["configPath"]
			tmpLocalFolderEmpty,tmpLocalFolderRemoved=self.checkLocalFolder(tmpConfigPath)
			if tmpLocalFolderEmpty or tmpLocalFolderRemoved:
				warning=True
				count+=1
			else:
				warning=False
			tmpIsOneDriveRunning=self.isOnedriveRunning(item['configPath'])
			
			self._updateSpaceConfigData("localFolderWarning",warning,tmpSpaceId)
			self._updateSpaceConfigData("isRunning",tmpIsOneDriveRunning,tmpSpaceId)

		if count>0:
			self.globalOneDriveFolderWarning=True
		else:
			self.globalOneDriveFolderWarning=False
	
	#def updateGlobalLocalFolderInfo

	def updateGlobalStatusInfo(self):

		count=0

		for item in self.onedriveConfig["spacesList"]:
			tmpSpaceId=item["id"]
			tmpConfigPath=item["configPath"]
			tmpStatus=int(self._readSpaceStatusToken(item['configPath'])[1])

			if tmpStatus not in self.correctStatusCode:
				count+=1

			self._updateSpaceConfigData("status",tmpStatus,tmpSpaceId)

		if count>0:
			self.globalOneDriveStatusWarning=True
		else:
			self.globalOneDriveStatusWarning=False
	
	#def updateGlobalLocalFolderInfo

	def clearCache(self):

		clear=False
		versionFile="/home/%s/.config/lliurex-onedrive.conf"%self.user
		cachePath1="/home/%s/.cache/lliurex-onedrive"%self.user
		installedVersion=self.getPackageVersion()

		if not os.path.exists(versionFile):
			with open(versionFile,'w') as fd:
				fd.write(installedVersion)
				fd.close()

			clear=True

		else:
			with open(versionFile,'r') as fd:
				fileVersion=fd.readline()
				fd.close()

			if fileVersion!=installedVersion:
				with open(versionFile,'w') as fd:
					fd.write(installedVersion)
					fd.close()
				clear=True
		
		if clear:
			if os.path.exists(cachePath1):
				shutil.rmtree(cachePath1)

	#def clearCache

	def getPackageVersion(self):

		command = "LANG=C LANGUAGE=en apt-cache policy lliurex-onedrive"
		p = subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
		installed = None
		for line in iter(p.stdout.readline,b""):
			if type(line) is bytes:
				line=line.decode()

			stripedline = line.strip()
			if stripedline.startswith("Installed"):
				installed = stripedline.replace("Installed: ","")

		return installed

	#def getPackageVersion

	def migrateSpace(self,spaceInfo):

		spaceEmail=spaceInfo[0]
		spaceAccountType=""
		spaceType=spaceInfo[1]
		spaceName=spaceInfo[2]
		spaceLibrary=spaceInfo[3]
		spaceDriveId=spaceInfo[4]

		self.spaceBasicInfo=[spaceEmail,spaceAccountType,spaceType,spaceName,spaceLibrary]
		ret=self._stopOldService()
		
		if ret:
			self._getSpaceSuffixName(spaceInfo)
			self.spaceLocalFolder="/home/%s/OneDrive-%s"%(self.user,self.spaceSuffixName)
			self._createSpaceConfFolder(spaceType,spaceDriveId)
			if os.path.exists(self.spaceConfPath):
				self._moveOldConfig(self.onedriveConfigDir,self.spaceConfPath)
				oldLocalFolder="/home/%s/OneDrive"%self.user
				try:
					if os.path.exists(oldLocalFolder):
						os.rename(oldLocalFolder,self.spaceLocalFolder)
				except Exception as e:
					self._restoreOldConfig(oldLocalFolder)
					return False

				customParam=self.readSpaceConfigFile(os.path.join(self.onedriveConfigDir,"config"))
				self.updateConfigFile(customParam)
				self._manageEmptyToken()
				self._createSpaceServiceUnit(spaceType)
				self._createOneDriveACService()
				self.getInitialDownload()
				self._updateOneDriveConfig(spaceInfo)
				self._createAuxVariables()
				self._addDirectoryFile(spaceType)
				self.loadOneDriveConfig()
				self._deleteOldFiles()
				return True			
			else:
				return False
		
		return ret

	#def migrateSpace

	def _stopOldService(self):

		oldServicePath=os.path.join(self.userSystemdPath,"onedrive.service")
		ok=True
		alreadyMasked=False
		if not os.path.exists(oldServicePath):
			cmd="systemctl --user stop onedrive.service"
			try:
				p=subprocess.run(cmd,shell=True,check=True)
				
			except subprocess.CalledProcessError as e:
				ok=False
				pass
		
		else:
			alreadyMasked=True
		
		isRunning=self.isOnedriveRunning(self.onedriveConfigDir,True)
		
		if isRunning:
			try:
				cmd="ps -ef | grep 'onedrive --monitor' | grep -v grep | awk '{print $2}' | xargs kill -9"				
				p=subprocess.run(cmd,shell=True,check=True)
			except subprocess.CalledProcessError as e:
				ok=False
				pass
	
		if not alreadyMasked:
			try:	
				cmd="systemctl --user mask onedrive.service"
				p=subprocess.run(cmd,shell=True,check=True)
			
			except subprocess.CalledProcessError as e:
				ok=False
				pass

		return ok

	#def _stopOldService

	def _moveOldConfig(self,origPath,destPath):

		for item in self.filesToMigrate:
			tmpFile=os.path.join(origPath,item)
			if os.path.exists(tmpFile):
				newFile=os.path.join(destPath,item)
				shutil.move(tmpFile,newFile)


	#def _moveOldConfig

	def _restoreOldConfig(self,oldLocalFolder):

		if not os.path.exists(oldLocalFolder):
			if os.path.exists(self.spaceLocalFolder):
				os.rename(self.spaceLocalFolder,oldLocalFolder)
				self._moveOldConfig(self.spaceConfPath,self.onedriveConfigDir)

	#def _restoreOldConfig

	def _deleteOldFiles(self):

		for item in self.oldFilesToDelete:
			tmpFile=os.path.join(self.onedriveConfigDir,item)
			if os.path.exists(tmpFile):
				os.remove(tmpFile)

	#def _deleteOldFiles

	def checkHddFreeSpace(self):

		HDD_FREE_SPACE_WARNING=-17
		HDD_FREE_SPACE_ERROR=-18
		hddAlert=False
		code=""
		msgType="Information"
		
		if os.path.exists(self.freeSpaceWarningToken):
			hddAlert=True
			code=HDD_FREE_SPACE_WARNING
			msgType="Warning"
		elif os.path.exists(self.freeSpaceErrorToken):
			hddAlert=True
			code=HDD_FREE_SPACE_ERROR
			msgType="Error"

		return [hddAlert,code,msgType]

	#def checkHddFreeSpace

	def _addDirectoryFile(self,spaceType):

		if os.path.exists(self.spaceLocalFolder):
			if spaceType=="onedrive":
				shutil.copyfile(self.oneDriveDirectoryFile,os.path.join(self.spaceLocalFolder,".directory"))
			else:
				shutil.copyfile(self.sharePointDirectoryFile,os.path.join(self.spaceLocalFolder,".directory"))
				organizationFolder="/home/%s/%s"%(self.user,self.spaceSuffixName)
				if not os.path.exists(os.path.join(organizationFolder,".directory")):
					shutil.copyfile(self.organizationDirectoryFile,os.path.join(organizationFolder,".directory"))
	
	#def _addDirectoryFile

	def removeOrganizationDirectoryFile(self):

		if self.spaceBasicInfo[2]=="sharepoint":
			removeDirectoryFile=False
			spaces=self.onedriveConfig["spacesList"]

			if len(spaces)==0:
				removeDirectoryFile=True
			else:
				for item in spaces:
					if item["spaceType"]=="sharepoint":
						removeDirectoryFile=False
						break
					else:
						removeDirectoryFile=True

			if removeDirectoryFile:
				if os.path.exists(os.path.join(self.organizationFolder,".directory")):
					os.remove(os.path.join(self.organizationFolder,".directory"))
		
	#def removeOrganizationDirectoryFile

	def _getLastPendingChanges(self):

		lastPendingChanges=""
		if os.path.exists(os.path.join(self.spaceConfPath,".statusToken")):
			with open(os.path.join(self.spaceConfPath,".statusToken"),'r') as fd:
				lastPendingChanges=fd.readlines()[-1].strip()
		
		return lastPendingChanges

	#def _getLastPendingChanges


#class OnedriveManager
