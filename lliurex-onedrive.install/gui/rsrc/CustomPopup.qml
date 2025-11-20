import QtQuick 2.6
import QtQuick.Controls 2.6
import QtQuick.Layouts 1.12


Popup {
    id:popUpWaiting
    width:570
    height:80
    anchors.centerIn: Overlay.overlay
    modal:true
    focus:true
    visible:!mainStackBridge.closePopUp[0]
    closePolicy:Popup.NoAutoClose

    GridLayout{
        id: popupGrid
        rows: 2
        flow: GridLayout.TopToBottom
        anchors.centerIn:parent


        RowLayout {
            Layout.fillWidth: true
            Layout.alignment:Qt.AlignHCenter
            Rectangle{
                color:"transparent"
                width:30
                height:30
                AnimatedImage{
                    source: "/usr/share/lliurex-onedrive/rsrc/loading.gif"
                    transform: Scale {xScale:0.45;yScale:0.45}
                }
            }
        }

        RowLayout {
            Layout.fillWidth: true
            Layout.alignment:Qt.AlignHCenter

            Text{
                id:popupText
                text:getTextMessage()
                font.pointSize: 10
                Layout.alignment:Qt.AlignHCenter
            }
        }
    }

    function getTextMessage(){
        switch (mainStackBridge.closePopUp[1]){
            case 1:
                var msg=i18nd("lliurex-onedrive","Configuring a new space. Wait a moment...");
                break;
            case 2:
                var msg=i18nd("lliurex-onedrive","Looking for libraries. Wait a moment...");
                break
            case 3:
                var msg=i18nd("lliurex-onedrive","Loading space settings. Wait a moment...");
                break
            case 6:
                var msg=i18nd("lliurex-onedrive","Starting the sync. Wait a moment...");
                break
            case 7:
                var msg=i18nd("lliurex-onedrive","Stopping the sync. Wait a moment...");
                break
            case 8:
                var msg=i18nd("lliurex-onedrive","Checking status. Wait a moment...");
                break
            case 9:
                var msg=i18nd("lliurex-onedrive","Unlinking from space. Wait a moment...")
                break
            case 10:
                var msg=i18nd("lliurex-onedrive","Gathering OneDrive/SharePoint folder structure. Wait a moment...")
                break
            case 11:
                var msg=i18nd("lliurex-ondrive","Restoring values . Wait a moment...")
                break
            case 12:
                var msg=i18nd("lliurex-onedrive","Saving changes. Wait a moment...")
                break
            case 13:
                var msg=i18nd("lliurex-onedrive","Running the test. Wait a moment...")
                break
            case 14:
                var msg=i18nd("lliurex-onedrive","Resynchronizing the space. Wait a moment...")
                break
            case 16:
                var msg=i18nd("lliurex-onedrive","Looking for SharePoints. Wait a moment...")
                break
            case 17:
                var msg=i18nd("lliurex-onedrive","Migrating configuration. Wait a moment...")
                break
            case 21:
                var msg=i18nd("lliurex-onedrive","Applying folders indentification. Wait a moment...")
                break
            case 22:
                var msg=i18nd("lliurex-onedrive","Removing folders indentification. Wait a moment...")
                break
            case 23:
                var msg=i18nd("lliurex-onedrive","The consolidation process is running. Wait a moment...")
                break
            default:
                var msg=""
                break;
        }
        return msg
    }
}
