import os
import sys
from PySide2 import QtCore, QtGui, QtQml

class FolderModel(QtCore.QAbstractListModel):

    PathRole = QtCore.Qt.UserRole + 1000
    NameRole = QtCore.Qt.UserRole + 1001
    IsCheckedRole = QtCore.Qt.UserRole + 1002
    IsExpandedRole = QtCore.Qt.UserRole + 1003
    TypeRole = QtCore.Qt.UserRole + 1004
    SubTypeRole=QtCore.Qt.UserRole + 1005
    LevelRole=QtCore.Qt.UserRole + 1006
    HideRole=QtCore.Qt.UserRole + 1007
    CanExpandedRole=QtCore.Qt.UserRole + 1008
    ParentPathRole=QtCore.Qt.UserRole + 1009


    def __init__(self, entries, parent=None):

        super(FolderModel, self).__init__(parent)
        self._entries = entries

    #def __init__

    def rowCount(self, parent=QtCore.QModelIndex()):

        if parent.isValid(): return 0
        return len(self._entries)

    #def rowCount

    def data(self, index, role=QtCore.Qt.DisplayRole):

        if 0 <= index.row() < self.rowCount() and index.isValid():
            item = self._entries[index.row()]
            if role == FolderModel.PathRole:
                return item["path"]
            elif role == FolderModel.NameRole:
                return item["name"]
            elif role == FolderModel.IsCheckedRole:
                return item["isChecked"]
            elif role == FolderModel.IsExpandedRole:
            	return item["isExpanded"]
            elif role == FolderModel.TypeRole:
            	return item["type"]
            elif role == FolderModel.SubTypeRole:
            	return item["subtype"]
            elif role == FolderModel.LevelRole:
            	return item["level"]
            elif role == FolderModel.HideRole:
            	return item["hide"]
            elif role==FolderModel.CanExpandedRole:
                return item["canExpanded"]
            elif role==FolderModel.ParentPathRole:
                return item["parentPath"]
    #def data

    def roleNames(self):

        roles = dict()
        roles[FolderModel.PathRole] = b"path"
        roles[FolderModel.NameRole] = b"name"
        roles[FolderModel.IsCheckedRole] = b"isChecked"
        roles[FolderModel.IsExpandedRole] = b"isExpanded"
        roles[FolderModel.TypeRole] = b"type"
        roles[FolderModel.SubTypeRole] = b"subtype"
        roles[FolderModel.HideRole] = b"hide"
        roles[FolderModel.LevelRole] = b"level"
        roles[FolderModel.CanExpandedRole]=b"canExpanded"
        roles[FolderModel.ParentPathRole]=b"parentPath"

        return roles

    #def roleName

    def appendRow(self,p, n, ic, ie, t, st, h, l, ce, pp):

        self.beginInsertRows(QtCore.QModelIndex(), self.rowCount(),self.rowCount())
        self._entries.append(dict(path=p, name=n, isChecked=ic, isExpanded=ie, type=t, subtype=st, hide=h, level=l, canExpanded=ce, parentPath=pp))
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

#class FolderModel