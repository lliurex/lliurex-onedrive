import QtQuick 2.6
import QtQuick.Controls 2.6
import QtQuick.Layouts 1.12


Popup {
    id:popUpWaiting
    width:500
    height:80
    anchors.centerIn: Overlay.overlay
    modal:true
    focus:true
    visible:!onedriveBridge.closePopUp[0]
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
                    transform: Scale {xScale:0.15;yScale:0.15}
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
        switch (onedriveBridge.closePopUp[1]){
            case 1:
                var msg=i18nd("lliurex-onedrive","Creating a new space. Wait a moment...");
                break;
            case 2:
                var msg=i18nd("lliurex-onedrive","Looking for libraries. Wait a moment...");
                break
            default:
                var msg=""
                break;
        }
        return msg
    }
}