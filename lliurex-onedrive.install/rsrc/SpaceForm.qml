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
        id:newSpaceLayout
        rows:2
        flow: GridLayout.TopToBottom
        rowSpacing:10
        Layout.fillWidth: true
        anchors.horizontalCenter:parent.horizontalCenter

        Kirigami.InlineMessage {
            id: newSpaceMessageLabel
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
            Layout.topMargin: newSpaceMessageLabel.visible?0:50

            Text{
                id:spaceMail
                Layout.alignment:Qt.AlignRight
                text:i18nd("lliurex-onedrive","Associated email:")
                font.family: "Quattrocento Sans Bold"
                font.pointSize: 10
            }
            TextField{
                id:spaceMailEntry
                font.pointSize:10
                horizontalAlignment:TextInput.AlignLeft
                focus:true
                implicitWidth:400
            }

            Text{
                id:spaceType
                Layout.alignment:Qt.AlignRight
                Layout.bottomMargin:10
                text:i18nd("lliurex-onedrive","Kind of space:")
                font.family: "Quattrocento Sans Bold"
                font.pointSize: 10
            }

            ColumnLayout{
                id:typeOptions
                spacing:5
                Layout.alignment:Qt.AlignLeft
                Layout.bottomMargin:10

                Label{
                    text:""
                }
                RadioButton{
                    id:oneDriveOption
                    text:"OneDrive"
                }

                RadioButton{
                    id:sharePointOption
                    text:"SharePoint"
                }
            }
            Text{
                id:spaceSharePoint
                Layout.bottomMargin:10
                Layout.alignment:Qt.AlignRight
                text:i18nd("lliurex-onedrive","SharePoint name:")
                font.family: "Quattrocento Sans Bold"
                font.pointSize: 10
                visible:sharePointOption.checked
            }
            TextField{
                id:spaceSharePointEntry
                font.pointSize:10
                Layout.bottomMargin:10
                horizontalAlignment:TextInput.AlignLeft
                focus:true
                implicitWidth:400
                visible:sharePointOption.checked
            }

            Text{
                id:spaceLibrary
                Layout.alignment:Qt.AlignRight
                text:i18nd("lliurex-onedrive","Library to sync:")
                font.family: "Quattrocento Sans Bold"
                font.pointSize: 10
                visible:sharePointOption.checked
            }
            ComboBox{
                id:spaceLibraryEntry
                font.pointSize:10
                textRole:"name"
                valueRole:"id"
                model:onedriveBridge.libraryModel
                implicitWidth:400
                visible:sharePointOption.checked
            }
        }
    }
    RowLayout{
        id:btnBox
        anchors.bottom: parent.bottom
        anchors.right:parent.right
        anchors.bottomMargin:15
        anchors.rightMargin:10
        spacing:10

        Button {
            id:applyBtn
            visible:true
            focus:true
            display:AbstractButton.TextBesideIcon
            icon.name:"dialog-ok.svg"
            text:i18nd("lliurex-onedrive","Apply")
            Layout.preferredHeight:40
            enabled:true
            Keys.onReturnPressed: applyBtn.clicked()
            Keys.onEnterPressed: applyBtn.clicked()
            onClicked:{
                oneDriveAuth.authUrl=onedriveBridge.authUrl
                /*onedriveBridge.moveToSpaceOption(2)*/
                onedriveBridge.getSharePointLibraries([spaceMailEntry.text,spaceSharePointEntry.text])
            }
        }
        Button {
            id:cancelBtn
            visible:true
            focus:true
            display:AbstractButton.TextBesideIcon
            icon.name:"dialog-cancel.svg"
            text:i18nd("lliurex-onedrive","Cancel")
            Layout.preferredHeight: 40
            enabled:true
            Keys.onReturnPressed: cancelBtn.clicked()
            Keys.onEnterPressed: cancelBtn.clicked()
            onClicked:{
                onedriveBridge.moveToSpaceOption(0)
            }
        }
    } 
}



