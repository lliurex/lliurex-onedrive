#!/usr/bin/python3
import os
import sys
from PySide6 import QtCore, QtGui, QtQml

class LibraryModel(QtCore.QAbstractListModel):

	IdLibraryRole= QtCore.Qt.UserRole + 1000
	NameLibraryRole=QtCore.Qt.UserRole + 1001

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
			if role == LibraryModel.IdLibraryRole:
				return item["idLibrary"]
			elif role==LibraryModel.NameLibraryRole:
				return item["nameLibrary"]
	#def data

	def roleNames(self):
		
		roles = dict()
		roles[LibraryModel.IdLibraryRole] = b"idLibrary"
		roles[LibraryModel.NameLibraryRole] = b"nameLibrary"

		return roles

	#def roleName

	def appendRow(self,il,nl):
		
		tmpId=[]
		for item in self._entries:
			tmpId.append(item["idLibrary"])
		if il not in tmpId and il !="":
			self.beginInsertRows(QtCore.QModelIndex(), self.rowCount(),self.rowCount())
			self._entries.append(dict(idLibrary=il,nameLibrary=nl))
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
	
#class LibraryModel
