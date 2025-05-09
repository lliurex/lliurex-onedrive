import org.kde.plasma.components as Components
import org.kde.plasma.components as PC3
import org.kde.kirigami as Kirigami
import QtQuick
import QtQuick.Controls
import QtQml.Models


Rectangle {
    property alias structModel:listSpace.model
    property alias listCount:listSpace.count

    id:spaceTable
    visible: true
    width: 650; height: 312
    color:"white"
    border.color: "#d3d3d3"

    PC3.ScrollView{
        implicitWidth:parent.width
        implicitHeight:parent.height
        anchors.leftMargin:10

        ListView{
            id: listSpace
            anchors.fill:parent
            height: parent.height
            model:structModel
            enabled:true
            currentIndex:-1
            clip: true
            focus:true
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
                width: parent.width - (Kirigami.Units.largeSpacing * 4)
                visible: listSpace.count==0?true:false
                text: i18nd("lliurex-onedrive","No space is being sinced")
            }
        } 
     }
}

