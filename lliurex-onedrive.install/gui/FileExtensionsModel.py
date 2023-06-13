#!/usr/bin/python3
import os
import sys
from PySide2 import QtCore, QtGui, QtQml

class FileExtensionsModel(QtCore.QAbstractListModel):

	NameRole= QtCore.Qt.UserRole + 1000
	IsCheckedRole=QtCore.Qt.UserRole +1001

	def __init__(self,parent=None):
		
		super(FileExtensionsModel, self).__init__(parent)
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
			if role == FileExtensionsModel.NameRole:
				return item["name"]
			elif role == FileExtensionsModel.IsCheckedRole:
				return item["isChecked"]

	#def data

	def roleNames(self):
		
		roles = dict()
		roles[FileExtensionsModel.NameRole] = b"name"
		roles[FileExtensionsModel.IsCheckedRole] = b"isChecked"

		return roles

	#def roleNames

	def appendRow(self,ne,ic):
		
		tmpId=[]
		for item in self._entries:
			tmpId.append(item["name"])
		if ne not in tmpId:
			self.beginInsertRows(QtCore.QModelIndex(), self.rowCount(),self.rowCount())
			self._entries.append(dict(name=ne,isChecked=ic))
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
			if param in ["isChecked"]:
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
	
#class FileExtensionsModel
