import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQml.Models 2.8
import org.kde.plasma.components 2.0 as Components


Components.ListItem{

    id: listSpaceItem
    property string idSpace
    property string nameSpace
    property int statusSpace
    property bool isRunningSpace
    property bool localFolderWarning

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
        height:visible?40:0
        Text{
            id: spaceName
            text: nameSpace
            width:500
            elide:Text.ElideMiddle
            clip: true
            anchors.leftMargin:15
            anchors.verticalCenter:parent.verticalCenter
        }

        Image {
            id:spaceStatusIcon
            source:{
                if ((statusSpace==0) && (!localFolderWarning)){
                    "/usr/share/icons/breeze/status/16/state-ok.svg"
                }else{
                    "/usr/share/icons/breeze/status/16/state-warning.svg"
                }

            }
            sourceSize.width:32
            sourceSize.height:32
            anchors.leftMargin:15
            anchors.left:spaceName.right
            anchors.verticalCenter:parent.verticalCenter

        }  

        Image {
            id:spaceRunningIcon
            source:{
                if (isRunningSpace){
                    "/usr/share/icons/breeze/status/16/media-playback-playing.svg"
                }else{
                    "/usr/share/icons/breeze/status/16/media-playback-stopped.svg"
                }

            }
            sourceSize.width:32
            sourceSize.height:32
            anchors.leftMargin:15
            anchors.left:spaceStatusIcon.right
            anchors.verticalCenter:parent.verticalCenter

        }      

        Button{
            id:manageSpaceBtn
            display:AbstractButton.IconOnly
            icon.name:"configure.svg"
            anchors.leftMargin:15
            anchors.left:spaceRunningIcon.right
            anchors.verticalCenter:parent.verticalCenter
            visible:listSpaceItem.ListView.isCurrentItem
            ToolTip.delay: 1000
            ToolTip.timeout: 3000
            ToolTip.visible: hovered
            ToolTip.text:i18nd("lliurex-onedrive","Clic to manage this space")
            onClicked:onedriveBridge.loadSpace(idSpace)
        }

    }
}
