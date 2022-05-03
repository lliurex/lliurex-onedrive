import org.kde.plasma.core 2.0 as PlasmaCore
import org.kde.kirigami 2.6 as Kirigami
import QtQuick 2.6
import QtQuick.Controls 2.6
import QtQuick.Layouts 1.12
import QtQuick.Dialogs 1.3


Rectangle{
    color:"transparent"

    Text{ 
        text:i18nd("lliurex-onedrive","New Space")
        font.family: "Quattrocento Sans Bold"
        font.pointSize: 16
    }
    GridLayout{
        id:addSpaceLayout
        rows:2
        flow: GridLayout.TopToBottom
        rowSpacing:10
        Layout.fillWidth: true
        anchors.horizontalCenter:parent.horizontalCenter

        Kirigami.InlineMessage {
            id: addSpaceMessageLabel
            visible:true
            text:"prueba"
            type:Kirigami.MessageType.Error;
            Layout.minimumWidth:650
            Layout.maximumWidth:650
            Layout.topMargin: 40
        }

        GridLayout{
            id: newSpaceOptions
            columns: 2
            flow: GridLayout.LeftToRight
            columnSpacing:10
            Layout.alignment:Qt.AlignHCenter
            Layout.topMargin: addSpaceMessageLabel.visible?0:50

            Text{
                id:spaceMail
                Layout.bottomMargin:10
                Layout.alignment:Qt.AlignRight
                text:i18nd("lliurex-onedrive","E-Mail:")
                font.family: "Quattrocento Sans Bold"
                font.pointSize: 10
            }
            TextField{
                id:spaceMailEntry
                font.pointSize:10
                horizontalAlignment:TextInput.AlignLeft
                focus:true
                implicitWidth:200
            }
        }
    }
}



