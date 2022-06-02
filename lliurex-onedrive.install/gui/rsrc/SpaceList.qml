import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQml.Models 2.8
import org.kde.plasma.components 2.0 as Components
import org.kde.kirigami 2.16 as Kirigami



Rectangle {
    property alias structModel:listSpace.model
    property alias listCount:listSpace.count

    id:spaceTable
    visible: true
    width: 660; height: 300
    color:"white"
    border.color: "#d3d3d3"

    ListView{
        id: listSpace
        anchors.fill:parent
        height: parent.height
        model:structModel
        enabled:true
        currentIndex:-1
        clip: true
        boundsBehavior: Flickable.StopAtBounds
        highlight: Rectangle { color: "#add8e6"; opacity:0.8;border.color:"#53a1c9" }
        highlightMoveDuration: 0
        highlightResizeDuration: 0
        delegate: ListDelegateSpaceItem{
            width:spaceTable.width
            idSpace:model.id
            nameSpace:model.name
            statusSpace:model.status
            isRunningSpace:model.isRunning
            localFolderWarning:model.localFolderWarning
        }

        Kirigami.PlaceholderMessage { 
            id: emptyHint
            anchors.centerIn: parent
            width: parent.width - (units.largeSpacing * 4)
            visible: listSpace.count==0?true:false
            text: i18nd("lliurex-onedrive","No space is being sinced")
        }

     } 

}

