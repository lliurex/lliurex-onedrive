
import QtQuick 2.6
import QtQuick.Controls 2.6
import QtQuick.Layouts 1.15
import QtQuick.Dialogs 1.3


Rectangle{
    color:"transparent"

    Text{ 
        text:i18nd("lliurex-onedrive","Account")
        font.family: "Quattrocento Sans Bold"
        font.pointSize: 16
    }

    GridLayout{
        id: optionsAccount
        columns: 2
        flow: GridLayout.LeftToRight
        columnSpacing:10
        anchors.horizontalCenter:parent.horizontalCenter

        Text{
            id:syncFolderText
            Layout.topMargin:50
            Layout.bottomMargin:10
            Layout.alignment:Qt.AlignRight
            text:i18nd("lliurex-onedrive","OneDrive Folder:")
            font.family: "Quattrocento Sans Bold"
            font.pointSize: 10
        }

        Row {
            id:folderRow
            spacing:5
            Layout.topMargin:50
            Layout.alignment:Qt.AlignLeft
            Layout.bottomMargin:10

            Text{
                id:syncFolderPath
                text:onedriveBridge.userFolder
                font.family: "Quattrocento Sans Bold"
                font.pointSize: 10
                anchors.verticalCenter:openFolderBtn.verticalCenter
            }

            Button {
                id:openFolderBtn
                display:AbstractButton.IconOnly
                icon.name:"document-open-folder.svg"
                Layout.preferredHeight: 35
                ToolTip.delay: 1000
                ToolTip.timeout: 3000
                ToolTip.visible: hovered
                ToolTip.text:i18nd("lliurex-onedrive","Click to open OneDrive Folder")

                hoverEnabled:true
                onClicked:{
                    onedriveBridge.openFolder()
                }
            }
        }

        Text{
            id:freeSpaceText
            text:i18nd("lliurex-onedrive","Free Space:")
            font.family: "Quattrocento Sans Bold"
            font.pointSize: 10
            Layout.alignment:Qt.AlignRight
            Layout.bottomMargin:10
        }

        Text{
            id:freeSpaceValue
            text:onedriveBridge.freeSpace
            font.family: "Quattrocento Sans Bold"
            font.pointSize: 10
            Layout.alignment:Qt.AlignLeft
            Layout.bottomMargin:10
        }

        Text{
            id:clientStatusText
            text:i18nd("lliurex-onedrive","Synchronization:")
            font.family: "Quattrocento Sans Bold"
            font.pointSize: 10
            Layout.alignment:Qt.AlignRight
            Layout.bottomMargin:10
        }

        Row{
            id:clientRow
            spacing:5
            Layout.alignment:Qt.AlignLeft
            Layout.bottomMargin:10

            Text{
                id:clientStatusValue
                text:onedriveBridge.isOnedriveRunning?i18nd("lliurex-onedrive","Running"):i18nd("lliurex-onedrive","Stopped")
                font.family: "Quattrocento Sans Bold"
                font.pointSize: 10
                anchors.verticalCenter:startMonitorBtn.verticalCenter
            }

            Button {
                id:startMonitorBtn
                display:AbstractButton.IconOnly
                icon.name:!onedriveBridge.isOnedriveRunning?"kt-start.svg":"kt-stop.svg"
                Layout.preferredHeight: 35
                ToolTip.delay: 1000
                ToolTip.timeout: 3000
                ToolTip.visible: hovered
                ToolTip.text:onedriveBridge.isOnedriveRunning?i18nd("lliurex-onedrive","Click to stop syncing with OneDrive"):i18nd("lliurex-onedrive","Click to start syncing with OneDrive")
                hoverEnabled:true
                onClicked:{
                    accountPopup.open()
                    accountPopup.popupMessage=onedriveBridge.isOnedriveRunning?i18nd("lliurex-onedrive","Stopping synchronization. Wait a moment..."):i18nd("lliurex-onedrive","Starting synchronization. Wait a moment...")
                    delay(1000, function() {
                        if (onedriveBridge.closePopUp){
                            accountPopup.close(),
                            timer.stop();
                        }
                    })
            
                    onedriveBridge.manageSync(!onedriveBridge.isOnedriveRunning);
                }
            }
        }

        Row{
            id:syncTextRow
            Layout.alignment:Qt.AlignRight|Qt.AlignVCenter
            Layout.bottomMargin:10

            Text{
                id:syncStatusText
                text:i18nd("lliurex-onedrive","Status:")
                font.family: "Quattrocento Sans Bold"
                font.pointSize: 10
                anchors.verticalCenter:parent.verticalCenter
            }
        }

        Row{
            id:syncRow
            spacing:5
            Layout.alignment:Qt.AlignLeft
            Layout.bottomMargin:10

            Text{
                id:syncStatusValue
                text:getTextOption()
                font.family: "Quattrocento Sans Bold"
                font.pointSize: 10
                anchors.verticalCenter:parent.verticalCenter
            }

            Button {
                id:syncNowBtn
                display:AbstractButton.IconOnly
                icon.name:"view-refresh.svg"
                Layout.preferredHeight: 35
                Layout.alignment:Qt.AlignLeft
                Layout.bottomMargin:10
                anchors.verticalCenter:parent.verticalCenter
                hoverEnabled:true
                ToolTip.delay: 1000
                ToolTip.timeout: 3000
                ToolTip.visible: hovered
                ToolTip.text:{
                    i18nd("lliurex-onedrive","Click to update status information")
              }    
                onClicked:{
                    accountPopup.open()
                    accountPopup.popupMessage=i18nd("lliurex-onedrive", "Checking status. Wait a moment...")
                    delay(1000, function() {
                        if (onedriveBridge.closePopUp){
                            accountPopup.close(),
                            timer.stop();
                        }
                    })

                    onedriveBridge.checkAccountStatus()
                    
                }
            }
        } 

        Text{
            id:unlinkAccountText
            text:i18nd("lliurex-onedrive","Unlink from OneDrive account:")
            font.family: "Quattrocento Sans Bold"
            font.pointSize: 10
            Layout.alignment:Qt.AlignRight
        }

        Button {
            id:deleteAccountBtn
            display:AbstractButton.IconOnly
            icon.name:"delete.svg"
            Layout.preferredHeight: 35
            Layout.alignment:Qt.AlignLeft
            ToolTip.delay: 1000
            ToolTip.timeout: 3000
            ToolTip.visible: hovered
            ToolTip.text:i18nd("lliurex-onedrive","Click to unlink from OneDrive account")
        
            hoverEnabled:true
            onClicked:{
                unlinkDialog.open();
            }
        }
    }

    Dialog {
        id: unlinkDialog
        modality:Qt.WindowModal
        title:"Lliurex Onedrive"+" - "+i18nd("lliurex-onedrive","Account")

        contentItem: Rectangle {
            color: "#ebeced"
            implicitWidth: 550
            implicitHeight: 105
            anchors.topMargin:5
            anchors.leftMargin:5

            Image{
                id:dialogIcon
                source:"/usr/share/icons/breeze/status/64/dialog-question.svg"

            }
            
            Text {
                id:dialogText
                text:i18nd("lliurex-onedrive","Are you sure you want to unlink this computer from OneDrive account?.\nThe files will stop syncing, but the contents of the OneDrive folder\nwill not be erased")
                font.family: "Quattrocento Sans Bold"
                font.pointSize: 10
                anchors.left:dialogIcon.right
                anchors.verticalCenter:dialogIcon.verticalCenter
                anchors.leftMargin:10
            
            }

            DialogButtonBox {
                buttonLayout:DialogButtonBox.KdeLayout
                anchors.bottom:parent.bottom
                anchors.right:parent.right
                anchors.topMargin:15

                Button {
                    id:dialogApplyBtn
                    display:AbstractButton.TextBesideIcon
                    icon.name:"dialog-ok.svg"
                    text: i18nd("lliurex-onedrive","Accept")
                    font.family: "Quattrocento Sans Bold"
                    font.pointSize: 10
                    DialogButtonBox.buttonRole: DialogButtonBox.ApplyRole
                }

                Button {
                    id:dialogCancelBtn
                    display:AbstractButton.TextBesideIcon
                    icon.name:"dialog-cancel.svg"
                    text: i18nd("lliurex-onedrive","Cancel")
                    font.family: "Quattrocento Sans Bold"
                    font.pointSize: 10
                    DialogButtonBox.buttonRole:DialogButtonBox.RejectRole
                }

                onApplied:{
                    onedriveBridge.removeAccount()
                    unlinkDialog.close()
                
                }

                onRejected:{
                    unlinkDialog.close()

                }
            }
        }
     }

     CustomPopup{
        id:accountPopup
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

    function getTextOption(){

        switch (onedriveBridge.accountStatus) {
            case "0":
                var sync=i18nd("lliurex-onedrive","All synchronized");
                break;
            case "2":
                var sync=i18nd("lliurex-onedrive","Remote content pending syncing");
                break;
            case "-401":
                var sync=i18nd("lliurex-onedrive","Error: The authorization to access your account has expired");
                break;
            case "-2":
                var sync=i18nd("lliurex-onedrive","Error: No network connection detected");
                break;
            case "-3":
            case "-5":
                var sync=i18nd("lliurex-onedrive","Error: OneDrive must be repair");
                break;
            case "-416":
                var sync=i18nd("lliurex-onedrive","Uploading pending changes");
                break;
            default:
                var sync=i18nd("lliurex-onedrive","Unknown. Wait a moment and update the status");
                break;
        }
        return sync
    }
}
