import QtQuick 2.6
import QtQuick.Controls 2.6
import QtQuick.Layouts 1.15


Popup {
    id:popUpWaiting
    width:400
    height:80
    anchors.centerIn: Overlay.overlay
    modal:true
    focus:true
    closePolicy:Popup.NoAutoClose
    property alias popupMessage:popupText.text

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
                text:popupMessage
                font.pointSize: 10
                Layout.alignment:Qt.AlignHCenter
            }
        }
    }
}