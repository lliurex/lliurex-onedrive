import threading
import time
import os
import subprocess
import json
import math
import shutil 
import copy
import psutil


class OnedriveManager:
	
	def __init__(self):

		self.user=os.environ["USER"]
		self.onedriveConfigFile="/home/%s/.config/lliurex-onedrive-config/onedriveConfig.json"%(self.user)
		self.spacesConfigData=[]
		self.librariesConfigData=[]
		self.authUrl="https://login.microsoftonline.com/common/oauth2/v2.0/authorize?client_id=d50ca740-c83f-4d1b-b616-12c519384f0c&scope=Files.ReadWrite%20Files.ReadWrite.all%20Sites.Read.All%20Sites.ReadWrite.All%20offline_access&response_type=code&redirect_uri=https://login.microsoftonline.com/common/oauth2/nativeclient"
		self.userTokenPath="/home/%s/.onedriveAuth/"%(self.user)

	#def __init__

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
			self.onedriveConfig["spacesSync"]=[]
			with open(self.onedriveConfigFile,'w') as fd:
				json.dump(self.onedriveConfig,fd)

	#def readOneDriveConfig

	def getSpacesConfig(self):

		spaces=self.onedriveConfig["spacesSync"]
		for item in spaces:
			tmp={}
			tmp["name"]=item["localFolder"]
			self.spacesConfigData.append(tmp)
	
	#def getSpacesConfig

	def createToken(self,token):
		
		if not os.path.exists(self.userTokenPath):
			os.mkdir(self.userTokenPath)

		urlDoc=os.path.join(self.userTokenPath,"urlToken")
		tokenDoc=os.path.join(self.userTokenPath,"keyToken")
		f=open(urlDoc,'w')
		f.write(self.authUrl)
		f.close()
		f=open(tokenDoc,'w')
		f.write(token)
		f.close()

	#def createToken

	def getSharePointLibraries(self,email,sharePoint):

		self.librariesConfigData=[]
		for item in self.onedriveConfig["spacesSync"]:
			if item["email"]==email:
				confDir=item["configPath"]
				break

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
			tmp['name']=pout[i].split(":")[1].strip()
			tmp['id']=pout[i+1].split(":")[1].strip()
			self.librariesConfigData.append(tmp)


	#def getSharePointLibraries
	
#class OnedriveManager
