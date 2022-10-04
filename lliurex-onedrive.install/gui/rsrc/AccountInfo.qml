import org.kde.plasma.core 2.0 as PlasmaCore
import org.kde.kirigami 2.12 as Kirigami
import QtQuick 2.6
import QtQuick.Controls 2.6
import QtQuick.Layouts 1.12
import QtQuick.Dialogs 1.3


Rectangle{
    color:"transparent"

    Text{ 
        text:i18nd("lliurex-onedrive","Space Info")
        font.family: "Quattrocento Sans Bold"
        font.pointSize: 16
    }
    GridLayout{
        id:generalOptionsLayout
        rows:2
        flow: GridLayout.TopToBottom
        rowSpacing:10
        Layout.fillWidth: true
        anchors.horizontalCenter:parent.horizontalCenter

        Kirigami.InlineMessage {
            id: accountMessageLabel
            visible:onedriveBridge.showAccountMessage[0]
            text:getTextOption(onedriveBridge.showAccountMessage[1])
            type:onedriveBridge.showAccountMessage[2]=="OK"?Kirigami.MessageType.Positive:Kirigami.MessageType.Error;
            Layout.minimumWidth:650
            Layout.maximumWidth:650
            Layout.topMargin: 40
        }

        GridLayout{
            id: optionsAccount
            columns: 2
            flow: GridLayout.LeftToRight
            columnSpacing:10
            Layout.alignment:Qt.AlignHCenter
            Layout.topMargin: accountMessageLabel.visible?0:50

            Text{
                id:spaceMailText
                Layout.bottomMargin:10
                Layout.alignment:Qt.AlignRight
                text:i18nd("lliurex-onedrive","Associated email:")
                font.family: "Quattrocento Sans Bold"
                font.pointSize: 10
            }

            Text{
                id:spaceMailValue
                text:onedriveBridge.spaceBasicInfo[0]
                font.family: "Quattrocento Sans Bold"
                font.pointSize: 10
                Layout.alignment:Qt.AlignLeft
                Layout.bottomMargin:10
            }
      
           Text{
                id:spaceTypeText
                Layout.bottomMargin:10
                Layout.alignment:Qt.AlignRight
                text:i18nd("lliurex-onedrive","Space Type:")
                font.family: "Quattrocento Sans Bold"
                font.pointSize: 10
            }

           Text{
                id:spaceTypeValue
                text:onedriveBridge.spaceBasicInfo[2]=="onedrive"?  "OneDrive":"SharePoint"
                font.family: "Quattrocento Sans Bold"
                font.pointSize: 10
                Layout.alignment:Qt.AlignLeft
                Layout.bottomMargin:10
            }

            Text{
                id:sharePointText
                Layout.bottomMargin:10
                Layout.alignment:Qt.AlignRight
                text:i18nd("lliurex-onedrive","SharePoint:")
                font.family: "Quattrocento Sans Bold"
                font.pointSize: 10
                visible:onedriveBridge.spaceBasicInfo[2]=="sharepoint"?true:false
            }

           Text{
                id:sharePointValue
                text:onedriveBridge.spaceBasicInfo[3]
                Layout.maximumWidth:400
                elide:Text.ElideMiddle
                font.family: "Quattrocento Sans Bold"
                font.pointSize: 10
                Layout.alignment:Qt.AlignLeft
                Layout.bottomMargin:10
                visible:onedriveBridge.spaceBasicInfo[2]=="sharepoint"?true:false
            }

            Text{
                id:libraryText
                Layout.bottomMargin:10
                Layout.alignment:Qt.AlignRight
                text:i18nd("lliurex-onedrive","Library:")
                font.family: "Quattrocento Sans Bold"
                font.pointSize: 10
                visible:onedriveBridge.spaceBasicInfo[2]=="sharepoint"?true:false
            }

            Text{
                id:libraryValue
                text:onedriveBridge.spaceBasicInfo[4]
                font.family: "Quattrocento Sans Bold"
                font.pointSize: 10
                Layout.alignment:Qt.AlignLeft
                Layout.bottomMargin:10
                visible:onedriveBridge.spaceBasicInfo[2]=="sharepoint"?true:false
            }

            Text{
                id:syncFolderText
                Layout.bottomMargin:10
                Layout.alignment:Qt.AlignRight
                text:i18nd("lliurex-onedrive","Local folder:")
                font.family: "Quattrocento Sans Bold"
                font.pointSize: 10
            }
            RowLayout{
                id:folderRow
                spacing:10
                Layout.alignment:Qt.AlignLeft
                Layout.bottomMargin:10

                Text{
                    id:syncFolderPath
                    text:onedriveBridge.spaceLocalFolder
                    Layout.maximumWidth:400
                    elide:Text.ElideMiddle
                    font.family: "Quattrocento Sans Bold"
                    font.pointSize: 10
                    Layout.alignment:Qt.AlignVCenter
                }

                Button {
                    id:openFolderBtn
                    display:AbstractButton.IconOnly
                    icon.name:"document-open-folder.svg"
                    Layout.preferredHeight: 35
                    ToolTip.delay: 1000
                    ToolTip.timeout: 3000
                    ToolTip.visible: hovered
                    ToolTip.text:i18nd("lliurex-onedrive","Click to open local folder of space")

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
                text:onedriveBridge.freeSpace==""?i18nd("lliurex-onedrive","Information not available"):onedriveBridge.freeSpace
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
                spacing:10
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
                    ToolTip.text:onedriveBridge.isOnedriveRunning?i18nd("lliurex-onedrive","Click to stop syncing with space"):i18nd("lliurex-onedrive","Click to start syncing with space")
                    hoverEnabled:true
                    enabled:!onedriveBridge.localFolderRemoved
                    onClicked:{
                        if (!onedriveBridge.localFolderEmpty){
                            changeSyncStatus()
                        }else{
                            startEmptyDialog.open()
                        }
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
                spacing:10
                Layout.alignment:Qt.AlignLeft
                Layout.bottomMargin:10

                Text{
                    id:syncStatusValue
                    text:getTextOption(onedriveBridge.accountStatus)
                    font.family: "Quattrocento Sans Bold"
                    font.pointSize: 10
                    Layout.maximumWidth:300
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
                    enabled:!onedriveBridge.localFolderRemoved
                    ToolTip.delay: 1000
                    ToolTip.timeout: 3000
                    ToolTip.visible: hovered
                    ToolTip.text:{
                        i18nd("lliurex-onedrive","Click to update status information")
                  } 
                    onClicked:{
                        onedriveBridge.checkAccountStatus()
                        
                    }
                }
            } 

            Text{
                id:unlinkAccountText
                text:i18nd("lliurex-onedrive","Unlink from space:")
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
                ToolTip.text:i18nd("lliurex-onedrive","Click to unlink from space")
            
                hoverEnabled:true
                onClicked:{
                    unlinkDialog.open();
                }
            }
        }
    }
    ChangesDialog{
        id:unlinkDialog
        dialogIcon:"/usr/share/icons/breeze/status/64/dialog-question.svg"
        dialogTitle:"Lliurex Onedrive"+" - "+i18nd("lliurex-onedrive","Account")
        dialogMsg:i18nd("lliurex-onedrive","Are you sure you want to unlink this computer from this space?.\nThe files will stop syncing, but the contents of the space\nwill not be erased")
        dialogWidth:560
        btnAcceptVisible:false
        btnAcceptText:""
        btnDiscardText:i18nd("lliurex-onedrive","Accept")
        btnDiscardIcon:"dialog-ok.svg"
        btnCancelText:i18nd("lliurex-onedrive","Cancel")
        btnCancelIcon:"dialog-cancel.svg"
        Connections{
            target:unlinkDialog
            function onDiscardDialogClicked(){
                unlinkDialog.close()
                onedriveBridge.removeAccount()
            }
            function onRejectDialogClicked(){
                unlinkDialog.close()
            }
        }

    }
    ChangesDialog{
        id:startEmptyDialog
        dialogIcon:"/usr/share/icons/breeze/status/64/dialog-warning.svg"
        dialogTitle:"Lliurex Onedrive"+" - "+i18nd("lliurex-onedrive","Account")
        dialogMsg:i18nd("lliurex-onedrive","The local folder of space is empty.\nAre you sure you want to start the synchronization?\nThis action can lead to deletion of files stored on OneDrive/SharePoint")
        dialogWidth:560
        btnAcceptVisible:false
        btnAcceptText:""
        btnDiscardText:i18nd("lliurex-onedrive","Accept")
        btnDiscardIcon:"dialog-ok.svg"
        btnCancelText:i18nd("lliurex-onedrive","Cancel")
        btnCancelIcon:"dialog-cancel.svg"

        Connections{
            target:startEmptyDialog
            function onDiscardDialogClicked(){
                startEmptyDialog.close()
                changeSyncStatus()
            }
            function onRejectDialogClicked(){
                startEmptyDialog.close()
            }
        }        

    }

    CustomPopup{
        id:accountPopup
    }

    function getTextOption(errorCode){

        var additionalText=i18nd("lliurex-onedrive","\nWait a moment and update the status\nIf persist run a LliureX-OneDrive test")
        var helpText=i18nd("lliurex-onedrive","Consult the help to solve the situation")
        switch (errorCode) {
            case 0:
                var msg=i18nd("lliurex-onedrive","All remote content synchronized");
                break;
            case 2:
                var msg=i18nd("lliurex-onedrive","Remote content pending syncing");
                break;
            case 3:
                var msg=i18nd("lliurex-onedrive","Information not available");
                break;
            case 20:
                var msg=i18nd("lliurex-onedrive","Configuration migration completed successfully");
                break;
            case -1:
                var msg=i18nd("lliurex-onedrive","Microsoft OneDrive API return an error")+additionalText;
                break;
            case -2:
                var msg=i18nd("lliurex-onedrive","Unable to connect with Microsoft OneDrive")+additionalText;
                break;
            case -3:
                var msg=i18nd("lliurex-onedrive","Problems with local file system")+additionalText;
                break;
            case -4:
                var msg=i18nd("lliurex-onedrive","Your free space is 0");
                break;
            case -5:
                var msg=i18nd("lliurex-onedrive","Information about yor quota information is restricted\nMaybe your free space is 0");
                break;
            case -6:
                var msg=i18nd("lliurex-onedrive","Problems with database")+additionalText;
                break;
            case -7:
                var msg=i18nd("lliurex-onedrive","The authorization to access your account has expired");
                break;
            case 4:
            case -8:
                var msg=i18nd("lliurex-onedrive","Uploading pending changes");
                break;
            case -9:
                var msg=i18nd("lliurex-onedrive","Microsoft OneDrive not available")+additionalText;
                break;
            case -10:
                var msg=i18nd("lliurex-onedrive","Unable to start synchronization")
                break;
            case -11:
                var msg=i18nd("lliurex-onedrive","Unable to stop synchronization")
                break;
            case -12:
                var msg=i18nd("lliurex-onedrive","The local folder of space is empty. ")+helpText
                break;
            case -13:
                var msg=i18nd("lliurex-onedrive","The local folder of space not exist. ")+helpText
                break;
            case " ":
                var msg=""
                break;
            default:
                var msg=i18nd("lliurex-onedrive","Information not available")+additionalText;
                break;
        }
        return msg
    }

    function changeSyncStatus(){
        onedriveBridge.manageSync(!onedriveBridge.isOnedriveRunning);
    }
}



