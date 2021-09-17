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

		if self.is_configured():
			self.readConfigFile()
			if not self.isAutoStartEnabled():
				self.autoStartEnabled=False
				self.currentConfig[0]=False
		

	#def loadConfg
	
	def is_configured(self):

		token=os.path.join(self.internalOnedriveFolder,"refresh_token")

		if os.path.exists(token):
			return True
		else:
			return False

	#def is_configured

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
		ret=p.communicate()

		copyfile(self.configTemplate,os.path.join(self.internalOnedriveFolder,'config'))
		
		self.manageSync(True)
		time.sleep(3)
		return True

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
			if isOnedriveRunning and remove:
				cmd="systemctl --user stop onedrive.service"
				p=subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
				poutput=p.communicate()
				rc=p.returncode
			
				if rc !=0:
					return True
			
			else:
				if not remove:
					cmd="systemctl --user mask onedrive.service"
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
			cmd="systemctl --user start onedrive.service"
		else:
			cmd="systemctl --user stop onedrive.service"
		
		p=subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
		poutput=p.communicate()
		rc=p.returncode
		
		if rc !=0:
			return False

		return True				
	
	#def manageSync

	def removeAccount(self):

		ret=self.manageAutostart(False,True)
		cmd="onedrive --logout &"
		p=subprocess.run(cmd,shell=True,check=True)
	
	#def removeAccount

	def getAccountStatus(self):

		'''
			code:
				 0: All synchronized
				 1: With out config
				 2: Pending changes
				-401: Unauthorized
				-2: Network connection
				-3: Internal database error
				-4: Downlodading files
				-5: Resync must be executed
				-416: Uploading pending changes
		'''
		error=False
		code=""
		freespace="Unknow"
		if self.is_configured():
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
					if 'Unauthorized' in item:
						code="-401"
					elif 'Network Connection Issue' in item:
						code="-2"
					elif 'database error' in item:
						code="-3"
					elif '416' in item:
						code="-416"
					elif '--resync is required' in item:
						code="-5"	
					elif 'Free Space' in item:
						tmp_freespace=item.split(':')[1].strip()
						freespace=self._formatFreeSpace(tmp_freespace)

			else:
				poutput=poutput.split('\n')
				for item in poutput:
					if 'No pending' in item:
						code="0"
					elif 'out of sync' in item:
						code="2"
					elif '--resync is required' in item:
						code="-5"	
					elif 'Free Space' in item:
						tmp_freespace=item.split(':')[1].strip()
						freespace=self._formatFreeSpace(tmp_freespace)
					

					'''
					elif 'data to download' in item:
						code="-4"
					'''

		else:
			error=True
			code="1"

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

#class OnedriveManager
