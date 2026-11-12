import os
import sys
from PySide2 import QtCore, QtGui, QtQml

class FolderFilterProxyModel(QtCore.QSortFilterProxyModel):

    def __init__(self, parent=None):
        super(FolderFilterProxyModel, self).__init__(parent)

    def filterAcceptsRow(self, source_row, source_parent):

        model = self.sourceModel()
        if not model or source_row >= len(model._entries):
            return False

        item = model._entries[source_row]
        if item.get("type") == "parent":
            return True
        if item.get("subtype") == "parent" and not item.get("hide", False):
            return True

        return False

    #def filterAcceptsRow

#class FolderFilterProxyModel

class FolderModel(QtCore.QAbstractListModel):

    PathRole = QtCore.Qt.UserRole + 1000
    NameRole = QtCore.Qt.UserRole + 1001
    IsCheckedRole = QtCore.Qt.UserRole + 1002
    IsExpandedRole = QtCore.Qt.UserRole + 1003
    TypeRole = QtCore.Qt.UserRole + 1004
    SubTypeRole = QtCore.Qt.UserRole + 1005
    LevelRole = QtCore.Qt.UserRole + 1006
    HideRole = QtCore.Qt.UserRole + 1007
    CanExpandedRole = QtCore.Qt.UserRole + 1008
    ParentPathRole = QtCore.Qt.UserRole + 1009

    _ROLE_MAP = {
        PathRole: "path",
        NameRole: "name",
        IsCheckedRole: "isChecked",
        IsExpandedRole: "isExpanded",
        TypeRole: "type",
        SubTypeRole: "subtype",
        LevelRole: "level",
        HideRole: "hide",
        CanExpandedRole: "canExpanded",
        ParentPathRole: "parentPath",
    }

    def __init__(self, entries, parent=None):

        super(FolderModel, self).__init__(parent)
        self._entries = entries

    #def __init 

    def rowCount(self, parent=QtCore.QModelIndex()):

        if parent.isValid():
            return 0
        return len(self._entries)

    #def rowCount

    def data(self, index, role=QtCore.Qt.DisplayRole):

        if 0 <= index.row() < len(self._entries) and index.isValid():
            key = self._ROLE_MAP.get(role)
            if key:
                return self._entries[index.row()][key]
        
        return None

    #def data

    def roleNames(self):

        return {
            FolderModel.PathRole: b"path",
            FolderModel.NameRole: b"name",
            FolderModel.IsCheckedRole: b"isChecked",
            FolderModel.IsExpandedRole: b"isExpanded",
            FolderModel.TypeRole: b"type",
            FolderModel.SubTypeRole: b"subtype",
            FolderModel.HideRole: b"hide",
            FolderModel.LevelRole: b"level",
            FolderModel.CanExpandedRole: b"canExpanded",
            FolderModel.ParentPathRole: b"parentPath",
        }

    #def roleNames

    def appendRow(self, p, n, ic, ie, t, st, h, l, ce, pp):

        row = len(self._entries)
        self.beginInsertRows(QtCore.QModelIndex(), row, row)
        self._entries.append(dict(
            path=p, name=n, isChecked=ic, isExpanded=ie,
            type=t, subtype=st, hide=h, level=l,
            canExpanded=ce, parentPath=pp
        ))
        self.endInsertRows()

    #def appendRow

    def appendRows(self, entries):

        if not entries:
            return
        start = len(self._entries)
        end = start + len(entries) - 1
        self.beginInsertRows(QtCore.QModelIndex(), start, end)

        for item in entries:
            self._entries.append(dict(
                path=item["path"],
                name=item["name"],
                isChecked=item["isChecked"],
                isExpanded=item["isExpanded"],
                type=item["type"],
                subtype=item["subtype"],
                hide=item["hide"],
                level=item["level"],
                canExpanded=item["canExpanded"],
                parentPath=item["parentPath"]
            ))

        self.endInsertRows()

    #def appendRows

    def setData(self, index, param, value, role=QtCore.Qt.EditRole):

        if role == QtCore.Qt.EditRole:
            row = index.row()
            if param in ["isChecked", "isExpanded", "hide", "canExpanded"]:
                self._entries[row][param] = value
                self.dataChanged.emit(index, index)
                return True
        
        return False

    #def setData

    def resetModel(self):

        count = len(self._entries) - 1
        if count >= 1:
            self.beginRemoveRows(QtCore.QModelIndex(), 1, count)
            del self._entries[1:]
            self.endRemoveRows()

    #def resetModel

    def expandFolder(self, path, is_expanded):

        sub = set()
        first_row = -1
        last_row = -1

        for i, item in enumerate(self._entries):
            changed = False
            if item["path"] == path:
                item["isExpanded"] = is_expanded
                changed = True
            elif item["parentPath"] == path or item["parentPath"] in sub:
                item["isExpanded"] = is_expanded
                changed = True
                if item.get("subtype") == "parent":
                    sub.add(item["path"])
                    item["hide"] = not is_expanded

            if changed:
                if first_row == -1:
                    first_row = i
                last_row = i

        if first_row != -1:
            self.dataChanged.emit(
                self.index(first_row),
                self.index(last_row),
                [FolderModel.IsExpandedRole, FolderModel.HideRole]
            )

    #def expandFolder

    def checkFolderBatch(self, path, is_checked):

        sub = set()
        first_row = -1
        last_row = -1
        changed_items = []
        checked_paths = {e["path"] for e in self._entries if e.get("isChecked")}

        for i, item in enumerate(self._entries):
            changed = False
            if item["path"] == path:
                if item["isChecked"] != is_checked:
                    item["isChecked"] = is_checked
                    changed_items.append((item["path"], is_checked))
                    changed = True
            elif item["parentPath"] == path or item["parentPath"] in sub:
                if item["isChecked"] != is_checked:
                    item["isChecked"] = is_checked
                    changed_items.append((item["path"], is_checked))
                    changed = True
                if item.get("subtype") == "parent":
                    sub.add(item["path"])

            if is_checked and not item.get("isChecked"):
                if item.get("parentPath") != "OneDrive":
                    ref_path = item["path"] + "/"
                    if ref_path in path and item["parentPath"] in checked_paths:
                        item["isChecked"] = True
                        changed_items.append((item["path"], True))
                        changed = True

            if changed:
                if item["isChecked"]:
                    checked_paths.add(item["path"])
                if first_row == -1:
                    first_row = i
                last_row = i

        if first_row != -1:
            self.dataChanged.emit(
                self.index(first_row),
                self.index(last_row),
                [FolderModel.IsCheckedRole]
            )

        return changed_items

    #def checkFolderBatch

#class FolderModel
