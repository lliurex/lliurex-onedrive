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
		self.onedriveConfigFile="/home/%s/.config/lliurex-onedrive-config/onedriveConfig.json"%(self.user)
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
		self.spaceSuffixName=""
		self.folderSuffixName=""
		self.spaceConfPath=""
		self.tempConfigPath=""
		self.createEnvironment()

	#def __init__

	def createEnvironment(self):

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
				self.onedriveConfig=json.load(fd)
		else:
			self.onedriveConfig={}
			self.onedriveConfig["spacesList"]=[]
			with open(self.onedriveConfigFile,'w') as fd:
				json.dump(self.onedriveConfig,fd)

	#def readOneDriveConfig

	def getSpacesConfig(self):

		spaces=self.onedriveConfig["spacesList"]
		for item in spaces:
			tmp={}
			tmp["name"]=item["localFolder"]
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

		cmd='onedrive --get-O365-drive-id %s --confdir="%s"'%(sharePoint,confDir)
		p=subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
		pout,perror=p.communicate()

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

		self.localFolder=""

		self._getSpaceSuffixName(spaceInfo)

		if spaceInfo[1]=="onedrive":
			self.localFolder="/home/%s/OneDrive_%s"%(self.user,self.spaceSuffixName)
		else:
			self.localFolder="/home/%s/SharePoint_%s/%s"%(self.user,self.spaceSuffixName,self.folderSuffixName)
		
		if os.path.exists(self.localFolder):
			if os.listdir(self.localFolder):
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
		self.loadOneDriveConfig()

		return True

	#def createSpace 

	def _createSpaceConfFolder(self,spaceType,spaceId):

		self.spaceConfPath=""

		if spaceType=="onedrive":
			tmpFolder="onedrive_%s"%self.spaceSuffixName
			if not os.path.exists(os.path.join(self.onedriveConfigDir,tmpFolder)):
				self.spaceConfPath=os.path.join(self.onedriveConfigDir,tmpFolder)
		else:
			if not os.path.exists(os.path.join(self.sharePointConfigDir,self.folderSuffixName.lower())):
				self.spaceConfPath=os.path.join(self.sharePointConfigDir,self.folderSuffixName.lower())

		if self.spaceConfPath!="":
			os.mkdir(self.spaceConfPath)
			shutil.copy(self.configTemplatePath,self.spaceConfPath)
			
			with open(os.path.join(self.spaceConfPath,"config"),'r') as fd:
				lines=fd.readlines()
			
			with open(os.path.join(self.spaceConfPath,"config"),'w') as fd:
				for line in lines:
					if 'sync_dir' in line:
						tmpLine=line.replace("{{LOCAL_FOLDER}}",self.localFolder)
						fd.write(tmpLine)
					else:
						if spaceType=="sharepoint" and 'drive_id' in line:
							newLine='drive_id = "%s"'%spaceId
							tmpLine=line.replace('# drive_id = ""',newLine)
							fd.write(tmpLine)
						else:
							fd.write(line)

	#def _createSpaceConfFolder

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

		if spaceType=="onedrive":
			serviceFile="onedrive_%s.service"%self.spaceSuffixName
		else:
			serviceFile="sharepoint_%s.service"%self.folderSuffixName.lower()

		if not os.path.exists(os.path.join(self.userSystemdPath,serviceFile)):
			shutil.copyfile(self.serviceTemplatePath,os.path.join(self.userSystemdPath,serviceFile))
			configFile=configparser.ConfigParser()
			configFile.optionxform=str
			configFile.read(os.path.join(self.userSystemdPath,serviceFile))
			tmpCommand=configFile.get("Service","ExecStart")
			tmpCommand=tmpCommand.replace("{{CONF_PATH}}",self.spaceConfPath)
			configFile.set("Service","ExecStart",tmpCommand)
			with open(os.path.join(self.userSystemdPath,serviceFile),'w') as fd:
				configFile.write(fd)

	#def _createSpaceServiceUnit

	def _updateOneDriveConfig(self,spaceInfo):

		tmp={}
		tmp["email"]=spaceInfo[0]
		tmp["type"]=spaceInfo[1]
		tmp["sharepoint"]=spaceInfo[2]
		tmp["library"]=spaceInfo[3]
		tmp["localFolder"]=os.path.basename(self.localFolder)
		tmp["configPath"]=self.spaceConfPath
		tmp["id"]=spaceInfo[4]

		self.onedriveConfig["spacesList"].append(tmp)
		with open(self.onedriveConfigFile,'w') as fd:
			json.dump(self.onedriveConfig,fd)

	#def _updateOneDriveConfig

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
	
#class OnedriveManager
