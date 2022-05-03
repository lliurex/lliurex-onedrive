#!/usr/bin/python3
import os
import sys
from PySide2 import QtCore, QtGui, QtQml

class LibraryModel(QtCore.QAbstractListModel):

	NameRole= QtCore.Qt.UserRole + 1000,
	IdRole=QtCore.Qt.UserRole + 1001

	def __init__(self,parent=None):
		
		super(LibraryModel, self).__init__(parent)
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
			if role == LibraryModel.NameRole:
				return item["name"]
			elif role==LibraryModel.IdRole:
				return item["id"]
	#def data

	def roleNames(self):
		
		roles = dict()
		roles[LibraryModel.NameRole] = b"name"
		roles[LibraryModel.IdRole] = b"id"

		return roles

	#def roleName

	def appendRow(self,n,id):
		
		tmpId=[]
		for item in self._entries:
			tmpId.append(item["name"])
		tmpN=n.strip()
		if n not in tmpId and n !="" and len(tmpN)>0:
			self.beginInsertRows(QtCore.QModelIndex(), self.rowCount(),self.rowCount())
			self._entries.append(dict(name=n,id=id))
			self.endInsertRows()

	#def appendRow

	def removeRow(self,index):
		self.beginRemoveRows(QtCore.QModelIndex(),index,index)
		self._entries.pop(index)
		self.endRemoveRows()
	
	#def removeRow

	def clear(self):
		
		count=self.rowCount()
		self.beginRemoveRows(QtCore.QModelIndex(), 0, count)
		self._entries.clear()
		self.endRemoveRows()
	
	#def clear
	
#class GroupModel
