import QtQuick 2.6
import QtQuick.Controls 2.6
import QtQuick.Layouts 1.3
import QtQuick.Window 2.2

Rectangle{
    width: 600
    height: 615

    visible: true

    GridLayout{
        id: closeApp
        rows: 1
        flow: GridLayout.TopToBottom
        anchors.centerIn:parent

        RowLayout {
            Layout.fillWidth: true
            Layout.alignment:Qt.AlignHCenter

            Text{
                id:closetext
                text:i18nd("lliurex-onedrive", "You can close the application")
                font.family: "Quattrocento Sans Bold"
                font.pointSize: 10
                Layout.alignment:Qt.AlignHCenter
            }
        }
    }
}