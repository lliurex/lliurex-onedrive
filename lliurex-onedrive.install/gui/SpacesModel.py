#!/usr/bin/python3
import os
import sys
from PySide2 import QtCore, QtGui, QtQml

class SpacesModel(QtCore.QAbstractListModel):

	IdRole= QtCore.Qt.UserRole + 1000
	NameRole= QtCore.Qt.UserRole + 1001
	StatusRole= QtCore.Qt.UserRole + 1002
	IsRunningRole=QtCore.Qt.UserRole+1003
	LocalFolderWarningRole=QtCore.Qt.UserRole+1004

	def __init__(self,parent=None):
		
		super(SpacesModel, self).__init__(parent)
		self._entries =[]
	#def __init__

	def rowCount(self, parent=QtCore.QModelIndex()):
		
		if parent.isValid():
			return 0
		return len(self._entries)

	#def rowCount

	def data(self, index, role=QtCore.Qt.DisplayRole):
		
		if 0 <= index.row() < self.rowCount() and index.isValid():
			item = self._entries[index.row()]
			if role == SpacesModel.IdRole:
				return item["id"]
			elif role == SpacesModel.NameRole:
				return item["name"]
			elif role == SpacesModel.StatusRole:
				return item["status"]
			elif role == SpacesModel.IsRunningRole:
				return item["isRunning"]
			elif role == SpacesModel.LocalFolderWarningRole:
				return item["localFolderWarning"]

	#def data

	def roleNames(self):
		
		roles = dict()
		roles[SpacesModel.IdRole] = b"id"
		roles[SpacesModel.NameRole] = b"name"
		roles[SpacesModel.StatusRole] = b"status"
		roles[SpacesModel.IsRunningRole] = b"isRunning"
		roles[SpacesModel.LocalFolderWarningRole] = b"localFolderWarning"

		return roles

	#def roleName

	def appendRow(self,i,n,s,r,l):
		
		tmpId=[]
		for item in self._entries:
			tmpId.append(item["id"])
		tmpN=n.strip()
		if i not in tmpId and n !="" and len(tmpN)>0:
			self.beginInsertRows(QtCore.QModelIndex(), self.rowCount(),self.rowCount())
			self._entries.append(dict(id=i,name=n,status=s,isRunning=r,localFolderWarning=l))
			self.endInsertRows()

	#def appendRow

	def removeRow(self,index):
		self.beginRemoveRows(QtCore.QModelIndex(),index,index)
		self._entries.pop(index)
		self.endRemoveRows()
	
	#def removeRow

	def setData(self, index, param, value, role=QtCore.Qt.EditRole):
		
		if role == QtCore.Qt.EditRole:
			row = index.row()
			if param in ["status","isRunning","localFolderWarning"]:
				if self._entries[row][param]!=value:
					self._entries[row][param]=value
					self.dataChanged.emit(index,index)
					return True
				else:
					return False
			else:
				return False
	
	#def setData

	def clear(self):
		
		count=self.rowCount()
		self.beginRemoveRows(QtCore.QModelIndex(), 0, count)
		self._entries.clear()
		self.endRemoveRows()
	
	#def clear
	
#class GroupModel
