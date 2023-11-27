import QtQuick 2.6
import QtQuick.Controls 2.6
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
        width:parent.width-manageSpaceBtn.width
        Text{
            id: spaceName
            text: nameSpace
            width:{
                if (listSpaceItem.ListView.isCurrentItem){
                    parent.width-(spaceStatusIcon.width+spaceRunningIcon.width+manageSpaceBtn.width+20)
                }else{
                    parent.width-(spaceStatusIcon.width+spaceRunningIcon.width+20)
                }
            }
            elide:Text.ElideMiddle
            clip: true
            anchors.leftMargin:15
            anchors.verticalCenter:parent.verticalCenter
        }

        Image {
            id:spaceStatusIcon
            source:getStatusIcon(statusSpace,localFolderWarning)
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
            ToolTip.text:i18nd("lliurex-onedrive","Click to manage this space")
            onClicked:spaceStackBridge.loadSpace(idSpace)
        }

    }

    function getStatusIcon(statusSpace,localFolderWarning){

       if (localFolderWarning){
            return "/usr/share/icons/breeze/status/16/state-warning.svg"
        }else{
            switch (statusSpace){
                case 0:
                    return "/usr/share/icons/breeze/status/16/state-ok.svg"
                    break;
                case 3:
                    return "/usr/share/icons/breeze/status/16/state-offline.svg"
                    break;
                case 2:
                case 4:
                    return "/usr/share/icons/breeze/status/16/state-sync.svg"
                    break;
                default:
                    return "/usr/share/icons/breeze/status/16/state-warning.svg"
                    break
            }
               
        }
    }

}
