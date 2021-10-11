import os
import sys
from PySide2 import QtCore, QtGui, QtQml

class MyModel(QtCore.QAbstractListModel):
    NameRole = QtCore.Qt.UserRole + 1000
    IsCheckedRole = QtCore.Qt.UserRole + 1001
    IsExpandedRole = QtCore.Qt.UserRole + 1002
    TypeRole = QtCore.Qt.UserRole + 1003
    SubTypeRole=QtCore.Qt.UserRole + 1004
    LevelRole=QtCore.Qt.UserRole + 1005
    HideRole=QtCore.Qt.UserRole + 1006
    CanExpandedRole=QtCore.Qt.UserRole + 1007


    def __init__(self, entries, parent=None):
        super(MyModel, self).__init__(parent)
        self._entries = entries

    #def __init__

    def rowCount(self, parent=QtCore.QModelIndex()):
        if parent.isValid(): return 0
        return len(self._entries)

    #def rowCount

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if 0 <= index.row() < self.rowCount() and index.isValid():
            item = self._entries[index.row()]
            if role == MyModel.NameRole:
                return item["name"]
            elif role == MyModel.IsCheckedRole:
                return item["isChecked"]
            elif role == MyModel.IsExpandedRole:
            	return item["isExpanded"]
            elif role == MyModel.TypeRole:
            	return item["type"]
            elif role == MyModel.SubTypeRole:
            	return item["subtype"]
            elif role == MyModel.LevelRole:
            	return item["level"]
            elif role == MyModel.HideRole:
            	return item["hide"]
            elif role==MyModel.CanExpandedRole:
                return item["canExpanded"]
    #def data

    def roleNames(self):
        roles = dict()
        roles[MyModel.NameRole] = b"name"
        roles[MyModel.IsCheckedRole] = b"isChecked"
        roles[MyModel.IsExpandedRole] = b"isExpanded"
        roles[MyModel.TypeRole] = b"type"
        roles[MyModel.SubTypeRole] = b"subtype"
        roles[MyModel.HideRole] = b"hide"
        roles[MyModel.LevelRole] = b"level"
        roles[MyModel.CanExpandedRole]=b"canExpanded"

        return roles
    #def roleName

    def appendRow(self,n, ic, ie, t, st, h, l,ce):
        self.beginInsertRows(QtCore.QModelIndex(), self.rowCount(),self.rowCount())
        self._entries.append(dict(name=n, isChecked=ic, isExpanded=ie, type=t, subtype=st, hide=h, level=l, canExpanded=ce))
        self.endInsertRows()

    #def appendRow

    def setData(self, index, param, value, role=QtCore.Qt.EditRole):
        if role == QtCore.Qt.EditRole:
            row = index.row()
            if param in ["isChecked","isExpanded","hide","canExpanded"]:
                self._entries[row][param]=value
                self.dataChanged.emit(index,index)
                return True
            else:
                return False

    #def setData

    def resetModel(self):
        count=self.rowCount()-1
        self.beginRemoveRows(QtCore.QModelIndex(), 1, count)
        for i in range(count,-1,-1):
            if i!=0:
                self._entries.pop(i)
        self.endRemoveRows()
           
    #def resetModel
