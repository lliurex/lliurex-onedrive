
import QtQuick 2.6
import QtQuick.Controls 2.6
import QtQuick.Layouts 1.15
import org.kde.plasma.core 2.0 as PlasmaCore
import org.kde.kirigami 2.6 as Kirigami


Rectangle{
    color:"transparent"
    Text{ 
        Layout.leftMargin: 0
        text:i18nd("lliurex-onedrive","Synchronize")
        font.family: "Quattrocento Sans Bold"
        font.pointSize: 16
    }

    GridLayout{
        id:generalLayout
        rows:2
        flow: GridLayout.TopToBottom
        rowSpacing:10
        Layout.fillWidth: true
        anchors.left:parent.left

        Kirigami.InlineMessage {
            id: messageLabel
            visible:false
            text:i18nd("lliurex-onedrive","The changes will be applied when the client is restarted")
            type:Kirigami.MessageType.Positive;
            Layout.minimumWidth:650
            Layout.maximumWidth:650
            Layout.topMargin: 40
        }

        GridLayout{
            id: optionsGrid
            rows: 3
            flow: GridLayout.TopToBottom
            rowSpacing:10
            Layout.topMargin: messageLabel.visible?0:50

            CheckBox {
                id:syncAll
                text:i18nd("lliurex-onedrive","Synchronize all content of OneDrive")
                checked:!syncCustom.checked
                font.pointSize: 10
                focusPolicy: Qt.NoFocus
                onToggled:{
                    console.log("apretado")
                }

                Layout.bottomMargin:10
                Layout.alignment:Qt.AlignLeft
            }

            Row{
                id:customRow
                spacing:10
                Layout.alignment:Qt.AlignLeft
                Layout.bottomMargin:10

            
                CheckBox {
                    id:syncCustom
                    text:i18nd("lliurex-onedrive","Synchronize only those content")
                    checked:!syncAll.checked
                    font.pointSize: 10
                    focusPolicy: Qt.NoFocus
                    onToggled:{
                        if (checked){
                            folderList.structVisible=false
                            synchronizePopup.open()
                            synchronizePopup.popupMessage=i18nd("lliurex-onedrive", "Gathering folder structure. Wait a moment...")
                            delay(1000, function() {
                                console.log(onedriveBridge.closePopUp)
                                if (onedriveBridge.closePopUp){
                                    synchronizePopup.close(),
                                    timer.stop(),
                                    folderList.structVisible=true;
                                    folderList.structModel=onedriveBridge.model
                                }
                            })
                            onedriveBridge.updateFolderStruct()
                       }
                    }
                    anchors.verticalCenter:parent.verticalCenter
                }

                Button {
                    id:updateStructbtn
                    display:AbstractButton.IconOnly
                    icon.name:"view-refresh.svg"
                    enabled:syncCustom.checked
                    Layout.preferredHeight: 35
                    anchors.verticalCenter:parent.verticalCenter
                    ToolTip.delay: 1000
                    ToolTip.timeout: 3000
                    ToolTip.visible: hovered
                    ToolTip.text:i18nd("lliurex-onedrive","Update the folder structure")

                    hoverEnabled:true
                    onClicked:{
                        folderList.structVisible=false
                        synchronizePopup.open()
                        synchronizePopup.popupMessage=i18nd("lliurex-onedrive", "Gathering folder structure. Wait a moment...")
                        delay(1000, function() {
                            if (onedriveBridge.closePopUp){
                                synchronizePopup.close(),
                                timer.stop(),
                                folderList.structModel=onedriveBridge.model
                                folderList.structVisible=true;
                            }
                        })
                        onedriveBridge.updateFolderStruct()
                    }
                }
            }
            FolderList{
                id:folderList
            }
        }
    }

    RowLayout{
        id:btnBox
        anchors.bottom: parent.bottom
        anchors.right:parent.right
        anchors.bottomMargin:15
        anchors.rightMargin:15

        Button {
            id:applyBtn
            visible:true
            display:AbstractButton.TextBesideIcon
            icon.name:"dialog-ok.svg"
            text:i18nd("lliurex-onedrive","Apply")
            Layout.preferredHeight: 40

            onClicked:{
                messageLabel.visible=!messageLabel.visible
            }
        }
    }

    CustomPopup{
        id:synchronizePopup
     }

    Timer{
        id:timer
    }

    function delay(delayTime,cb){
        timer.interval=delayTime;
        timer.repeat=true;
        timer.triggered.connect(cb);
        timer.start()
    }

}
