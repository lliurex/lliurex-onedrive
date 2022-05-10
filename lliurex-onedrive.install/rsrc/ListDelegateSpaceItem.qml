import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQml.Models 2.8
import org.kde.plasma.components 2.0 as Components


Components.ListItem{

    id: listSpaceItem
    property string name

    enabled:true

    onContainsMouseChanged: {
        if (containsMouse) {
            listSpace.currentIndex = index
        } else {
            listSpace.currentIndex = -1
        }

    }

    Item{
        id: menuItem
        height:visible?30:0
        Text{
            id: spaceName
            text: name
            width:400
            clip: true
            anchors.leftMargin:5
            anchors.verticalCenter:parent.verticalCenter
        }

        Button{
            id:manageSpaceBtn
            display:AbstractButton.IconOnly
            icon.name:"configure.svg"
            anchors.left:spaceName.right
            visible:listSpaceItem.ListView.isCurrentItem
            ToolTip.delay: 1000
            ToolTip.timeout: 3000
            ToolTip.visible: hovered
            ToolTip.text:i18nd("lliurex-onedrive","Clic to manage this space")
            onClicked:onedriveBridge.loadSpace(name)
        }

    }
}
