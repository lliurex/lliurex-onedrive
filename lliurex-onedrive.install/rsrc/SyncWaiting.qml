import QtQuick 2.6
import QtQuick.Controls 2.6
import QtQuick.Layouts 1.12
import QtQuick.Dialogs 1.3


Rectangle{
    width: 700
    height: 615
    visible: true

    GridLayout{
        id: loadGrid
        rows: 4
        flow: GridLayout.TopToBottom
        anchors.centerIn:parent

        RowLayout{
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

        RowLayout{
            Layout.fillWidth: true
            Layout.alignment:Qt.AlignHCenter

            Text{
                id:loadtext
                text:i18nd("lliurex-onedrive", "Loading. Wait a moment...")
                font.family: "Quattrocento Sans Bold"
                font.pointSize: 10
                Layout.alignment:Qt.AlignHCenter
            }
        }
    }
}