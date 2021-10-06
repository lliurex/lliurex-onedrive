import threading
import time
import os
import subprocess
import json
import math
from shutil import copyfile


class OnedriveManager:
	
	def __init__(self):

		self.user=os.environ["USER"]
		self.userFolder="/home/%s/OneDrive"%(self.user)
		self.configTemplate="/usr/share/lliurex-onedrive/llx-data/config"
		self.authUrl="https://login.microsoftonline.com/common/oauth2/v2.0/authorize?client_id=d50ca740-c83f-4d1b-b616-12c519384f0c&scope=Files.ReadWrite%20Files.ReadWrite.all%20Sites.Read.All%20Sites.ReadWrite.All%20offline_access&response_type=code&redirect_uri=https://login.microsoftonline.com/common/oauth2/nativeclient"
		self.userTokenPath="/home/%s/.onedriveAuth/"%(self.user)
		self.testPath=os.path.join(self.userTokenPath,"test_onedrive.txt")
		self.onedriveUrl="https://login.microsoftonline.com/common/oauth2/v2.0/authorize?client_id=d50ca740-c83f-4d1b-b616-12c519384f0c&scope=Files.ReadWrite%20Files.ReadWrite.all%20Sites.Read.All%20Sites.ReadWrite.All%20offline_access&response_type=code&redirect_uri=https://login.microsoftonline.com/common/oauth2/nativeclient"
		self.authToken=""
		self.bandWidth=[{"name":"128 KB/s","value":"131072"},{"name":"256 KB/s","value":"262144"},{"name":"512 KB/s","value":"524288"},{"name":"1 MB/s","value":"1048576"},{"name":"10 MB/s","value":"10485760"},{"name":"20 MB/s","value":"20971520"},{"name":"30 MB/s","value":"31457280"},{"name":"50 MB/s","value":"52428800"},{"name":"100 MB/s","value":"104857600"}]
		self.bandWidthNames=[]
		for item in self.bandWidth:
			self.bandWidthNames.append(item["name"])
		self.internalOnedriveFolder="/home/%s/.config/onedrive"%(self.user)
		self.configFile=os.path.join(self.internalOnedriveFolder,"config")
		self.systemdFile="/home/%s/.config/systemd/user/onedrive.service"%(self.user)
		self.autoStartEnabled=True
		self.rateLimit=2
		self.monitorInterval=1
		self.currentConfig=[self.autoStartEnabled,self.monitorInterval,self.rateLimit]
	
	#def __init__

	def loadConfg(self):

		if self.isConfigured():
			self.readConfigFile()
			if not self.isAutoStartEnabled():
				self.autoStartEnabled=False
				self.currentConfig[0]=False
		
	#def loadConfg
	
	def isConfigured(self):

		token=os.path.join(self.internalOnedriveFolder,"refresh_token")

		if os.path.exists(token):
			return True
		else:
			return False

	#def isConfigured

	def readConfigFile(self):

		if os.path.exists(self.configFile):
			with open(self.configFile,'r') as fd:
				lines=fd.readlines()
				for line in lines:
					if 'monitor_interval' in line:
						value=line.split("=")[1].split("\n")[0].strip().split('"')[1]
						self.monitorInterval="{:.0f}".format(int(value)/60)
						self.currentConfig[1]=self.monitorInterval

					elif 'rate_limit' in line:
						value=line.split("=")[1].split("\n")[0].strip().split('"')[1]
						for i in range(len(self.bandWidth)):
							if self.bandWidth[i]["value"]==value:
								self.rateLimit=i
								self.currentConfig[2]=self.rateLimit
								break
				fd.close()
	
	#def readConfigFile

	def createAccount(self):

		if not os.path.exists(self.userTokenPath):
			os.mkdir(self.userTokenPath)

		urlDoc=os.path.join(self.userTokenPath,"urlToken")
		tokenDoc=os.path.join(self.userTokenPath,"keyToken")
		f=open(urlDoc,'w')
		f.write(self.onedriveUrl)
		f.close()
		f=open(tokenDoc,'w')
		f.write(self.authToken)
		f.close()

		cmd="/usr/bin/onedrive --auth-files %s:%s"%(urlDoc,tokenDoc)
		p=subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
		poutput=p.communicate()
		rc=p.returncode
		if rc in [0,1]:
			copyfile(self.configTemplate,os.path.join(self.internalOnedriveFolder,'config'))
			ret=self.manageSync(True)
			return True
		else:
			return False

	#def createAccount

	def isAutoStartEnabled(self):

		if os.path.exists(self.systemdFile):
			return False

		return True

	#def isAutostartEnabled

	def isOnedriveRunning(self):

		if os.system("ps -ef | grep '/usr/bin/onedrive --monitor' | grep -v 'grep' 1>/dev/null")==0:
			return True
		else:
			return False

	#def isOnedriveRunning

	def applyChanges(self,value):

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
	
	def manageAutostart(self,value,remove=False):

		isOnedriveRunning=self.isOnedriveRunning()

		if value:
			cmd="systemctl --user unmask onedrive.service"
			p=subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
			poutput=p.communicate()
			rc=p.returncode

			if rc !=0:
				return True

			else:
				return False
		else:
			if not remove:
				cmd="systemctl --user mask onedrive.service"
			else:
				cmd="systemctl --user unmask onedrive.service"

			p=subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
			poutput=p.communicate()
			rc=p.returncode
			
			if rc !=0:
				return True				

		return False

	#def manageAutostart

	def manageMonitorInterval(self,value):

		value=str(int(value)*60)
		return self._writeConfigFile('monitor_interval',value)

	#def manageMonitorInterval

	def manageRateLimit(self,index):

		value=self.bandWidth[index]["value"]
		return self._writeConfigFile('rate_limit',value)

	#def manageRateLimit

	def _writeConfigFile(self,param,value):

		if os.path.exists(self.configFile):
			try:
				with open(self.configFile,'r') as fd:
					lines=fd.readlines()
					fd.close()

				with open(self.configFile,'w') as fd:

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

	def manageSync(self,value):

		if value:
			if not os.path.exists(self.systemdFile):
				cmd="systemctl --user start onedrive.service"
			else:
				cmd="/usr/bin/onedrive --monitor &"
		else:
			if self._isSystemdActive():
				cmd="systemctl --user stop onedrive.service"
			else:
				cmd="ps -ef | grep '/usr/bin/onedrive --monitor' | grep -v grep | awk '{print $2}' | xargs kill -9"				
		
		try:
			p=subprocess.run(cmd,shell=True,check=True)
			return True
		except subprocess.CalledProcessError as e:
			return False

	#def manageSync

	def _isSystemdActive(self):

		cmd="systemctl --user is-active onedrive.service"
		p=subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
		poutput=p.communicate()[0]
		
		if type(poutput) is bytes:
			poutput=poutput.decode()		
		poutput=poutput.split('\n')[0]

		if poutput=="active":
			return True
		else:
			return False

	#def _isSystemdActive

	def removeAccount(self):

		ret=self.manageSync(False)
		if not self.isOnedriveRunning():
			ret=self.manageAutostart(False,True)
			cmd="/usr/bin/onedrive --logout &"
			p=subprocess.run(cmd,shell=True,check=True)
			return True
		else:
			return False
	
	#def removeAccount

	def getAccountStatus(self):

		MICROSOFT_API_ERROR="-1"
		UNABLE_CONNECT_MICROSOFT_ERROR="-2"
		LOCAL_FILE_SYSTEM_ERROR="-3"
		ZERO_SPACE_AVAILABLE_ERROR="-4"
		QUOTA_RESTRICTED_ERROR="-5"
		DATABASE_ERROR="-6"
		UNAUTHORIZED_ERROR="-7"
		UPLOADING_CANCEL_ERROR="-8"
		SERVICE_UNAVAILABLE="-9"

		ALL_SYNCHRONIZE_MSG="0"
		OUT_OF_SYNC_MSG="2"
		WITH_OUT_CONFIG="1"


		error=False
		code=""
		freespace=""
		if self.isConfigured():
			cmd="/usr/bin/onedrive --display-sync-status --verbose"
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
					elif 'Free Space' in item:
						tmp_freespace=item.split(':')[1].strip()
						freespace=self._formatFreeSpace(tmp_freespace)

		else:
			error=True
			code=WITH_OUT_CONFIG

		return [error,code,freespace]

	#def getAccountStatus

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

	def repairOnedrive(self):

		running=self.isOnedriveRunning()
		ret=self._syncResync()
		return ret

	#def repairDB

	def _syncResync(self):

		cmd="/usr/bin/onedrive --synchronize --resync"

		p=subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
		ret=p.communicate()
		rc=p.returncode

		if rc!=0:
			return False
		else:
			return True

	#def _syncResync
	
	def testOnedrive(self):

		if not os.path.exists(self.userTokenPath):
			os.mkdir(self.userTokenPath)

		if os.path.exists(self.testPath):
			os.remove(self.testPath)

		cmd="echo SYNC-DISPLAY-STATUS >>%s"%self.testPath
		os.system(cmd)
		cmd="/usr/bin/onedrive --display-sync-status --verbose >>%s 2>&1"%self.testPath
		p=subprocess.call(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)

		cmd="echo TEST SYNCHRONIZE >>%s"%self.testPath
		os.system(cmd)
		cmd="/usr/bin/onedrive --synchronize --dry-run --verbose >>%s 2>&1"%self.testPath
		p=subprocess.call(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)

		return

	#def testOnedrive

	def folderStruct(self):

		cmd='onedrive --synchronize --dry-run --verbose'
		p=subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
		out=p.communicate()[0]
		out=out.decode().split("\n")

		for i in range(len(out)-1,-1,-1):
			if 'Processing ' in out[i]:
				pass
			else:
				if 'The directory' in out[i]:
					pass
				else:
					if 'The file' in out[i]:
						pass
					else:
						out.pop(i)				

		for i in range(len(out)-1,-1,-1):
			if 'local state' in out[i]:
				out.pop(i)
			if 'last modified time' in out[i]:
				out.pop(i)	

		FolderStruct=[]
		for i in range(0,len(out)-1,2):
			tmp={}
			tmp_item=out[i]+": "+out[i+1]
			if 'The directory' in tmp_item:
				countChildren=0
				tmp_list={}
				tmp_entry=out[i].split("Processing")[1].strip()
				tmp_list["path"]=tmp_entry
				tmp_entry=tmp_entry.split("/")
				tmp_list["isChecked"]=False
				tmp_list["isExpanded"]=False
				tmp_list["hide"]=True
				if len(tmp_entry)==1:
					tmp_list["name"]=tmp_entry[0]
					tmp_list["type"]="Onedrive"
					tmp_list["subtype"]="parent"
					tmp_list["level"]=3

				else:
					tmp_list["name"]=tmp_entry[-1]
					tmp_list["type"]=tmp_entry[-2]
					tmp_list["subtype"]="parent"
					tmp_list["level"]=len(tmp_entry)*3

				for j in range(0,len(out)-1,2):
					tmp_item2=out[j]+": "+out[j+1]
					if 'The directory' in tmp_item2:
						tmp_entry2=out[j].split("Processing")[1].strip()
						if tmp_list["path"] in tmp_entry2:
							countChildren+=1

				if countChildren>1:
					tmp_list["canExpanded"]=True 
				else:
					tmp_list["canExpanded"]=False
				FolderStruct.append(tmp_list)	
		try:
			FolderStruct.pop(0)
		except Exception as e:
			pass
		return FolderStruct

	#def folderStruct 
		
#class OnedriveManager
