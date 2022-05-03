import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQml.Models 2.8
import org.kde.plasma.components 2.0 as Components



Rectangle {
    property alias structModel:listSpace.model
    property alias listCount:listSpace.count

    id:spaceTable
    visible: true
    width: 660; height: 125
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
        focus: true
        boundsBehavior: Flickable.StopAtBounds
        highlight: Rectangle { color: "#add8e6"; opacity:0.8;border.color:"#53a1c9" }
        highlightMoveDuration: 0
        highlightResizeDuration: 0
        delegate: ListDelegateSpaceItem{
            width:spaceTable.width
            name:model.name
        }

     } 

}

