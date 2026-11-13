import QtQuick
import QtQuick.Controls
import org.kde.plasma.components as Components

Rectangle {
    id: folderTable
    property alias structModel: listFolder.model
    property alias listCount: listFolder.count
    property alias structEnabled: listFolder.enabled

    visible: syncStackBridge.showFolderStruct
    width: 650
    height: 240
    border.color: "#d3d3d3"

    Components.ScrollView {
        implicitWidth: parent.width
        implicitHeight: folderTable.height
        anchors.leftMargin: 10

        ListView {
            id: listFolder
            anchors.fill: parent
            model: syncStackBridge.model
            enabled: structEnabled
            delegate: listdelegate
            clip: true
            boundsBehavior: Flickable.StopAtBounds
        }
    }

    Component {
        id: listdelegate

        Item {
            id: menuItem
            width: listFolder.width
            height: 30

            Image {
                id: menuOptionIcon
                source: isExpanded ? "/usr/share/icons/breeze/actions/22/go-down.svg" : "/usr/share/icons/breeze/actions/22/go-next.svg"
                visible: canExpanded
                anchors.left: parent.left
                anchors.verticalCenter: parent.verticalCenter
                anchors.leftMargin: 5 * level

                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        if (type === "parent" || subtype === "parent") {
                            syncStackBridge.expandFolder(path, !isExpanded)
                        }
                    }
                }
            }

            CheckBox {
                id: folderCheck
                checked: isChecked
                anchors.left: menuOptionIcon.right
                anchors.verticalCenter: parent.verticalCenter

                onToggled: {
                    if (type === "parent" || subtype === "parent") {
                        syncStackBridge.checkFolder(path, folderCheck.checked)
                    }
                }
            }

            Image {
                id: folderIcon
                source: "/usr/share/icons/breeze/places/22/folder-black.svg" 
                anchors.left: folderCheck.right
                anchors.verticalCenter: parent.verticalCenter
            }

            Text {
                id: text
                text: name
                width: 300
                clip: true
                anchors.left: folderIcon.right
                anchors.leftMargin: 5
                anchors.verticalCenter: parent.verticalCenter
            }
        }
    }
}
