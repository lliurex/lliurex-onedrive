import org.kde.plasma.core 2.0 as PlasmaCore
import org.kde.kirigami 2.12 as Kirigami
import QtQuick 2.6
import QtQuick.Controls 2.6
import QtQuick.Layouts 1.12
import QtQuick.Dialogs 1.3

Rectangle{
    color:"transparent"
    Text{ 
        text:i18nd("lliurex-onedrive","Tools")
        font.family: "Quattrocento Sans Bold"
        font.pointSize: 16
    }

    GridLayout{
        id:generalLayout
        rows:2
        flow: GridLayout.TopToBottom
        rowSpacing:10
        Layout.fillWidth: true
        anchors.horizontalCenter:parent.horizontalCenter

        Kirigami.InlineMessage {
            id: messageToolLabel
            visible:onedriveBridge.showToolsMessage[0]
            text:getMessageText()
            type:getTypeMessage()
            Layout.alignment:Qt.AlignLeft
            Layout.minimumWidth:650
            Layout.maximumWidth:650
            Layout.topMargin: 40
        }

        GridLayout{
            id: toolsGrid
            columns: 2
            flow: GridLayout.LeftToRight
            columnSpacing:15
            Layout.alignment:Qt.AlignHCenter
            Layout.fillWidth:true
            Layout.topMargin: messageToolLabel.visible?0:50

            Text{
                id:testText
                text:i18nd("lliurex-onedrive","Run a LliureX-OneDrive test:")
                Layout.bottomMargin:20
                Layout.alignment: Qt.AlignRight | Qt.AlignVCente
            }

            Button {
                id:testBtn
                display:AbstractButton.TextBesideIcon
                icon.name:"kt-start.svg"
                Layout.preferredHeight: 30
                Layout.bottomMargin:20
                Layout.alignment: Qt.AlignLeft | Qt.AlignVCenter
                hoverEnabled:true
                enabled:!onedriveBridge.localFolderRemoved 
                ToolTip.delay: 1000
                ToolTip.timeout: 3000
                ToolTip.visible: hovered
                ToolTip.text:i18nd("lliurex-onedrive","Click to run an LliureX-OneDrive test command")

                onClicked:{
                    onedriveBridge.testOnedrive();
                }
            }

            Text{
                id:repairText
                text:i18nd("lliurex-onedrive","Resynchronize space:")
                Layout.bottomMargin:20
                Layout.alignment: Qt.AlignRight | Qt.AlignVCenter
            }

            Button {
                id:repairBtn
                display:AbstractButton.IconOnly
                icon.name:"view-refresh.svg"
                Layout.preferredHeight: 30
                Layout.alignment: Qt.AlignLeft | Qt.AlignVCenter
                Layout.bottomMargin:20
                hoverEnabled:true
                enabled:!onedriveBridge.isOnedriveRunning && !onedriveBridge.localFolderEmpty
                ToolTip.delay: 1000
                ToolTip.timeout: 3000
                ToolTip.visible: hovered
                ToolTip.text:i18nd("lliurex-onedrive","Click to resynchronize the space")

                onClicked:{
                    repairRemoveDialog.open()
                }   
            }
            Text{
                id:updateAuth
                text:i18nd("lliurex-onedrive","Update authorization to sync space:")
                Layout.bottomMargin:20
                Layout.alignment: Qt.AlignRight | Qt.AlignVCenter
            }
            Button {
                id:updateAuthBtn
                display:AbstractButton.IconOnly
                icon.name:"document-encrypted.svg"
                Layout.preferredHeight: 30
                Layout.alignment: Qt.AlignLeft | Qt.AlignVCenter
                Layout.bottomMargin:20
                hoverEnabled:true
                enabled:!onedriveBridge.isOnedriveRunning && !onedriveBridge.localFolderEmpty
                ToolTip.delay: 1000
                ToolTip.timeout: 3000
                ToolTip.visible: hovered
                ToolTip.text:i18nd("lliurex-onedrive","Click to update authorization to sync space") 
                onClicked:{
                    updateAuthDialog.open()
                }   
            }

       }
    }

    ChangesDialog{
        id:repairRemoveDialog
        dialogIcon:"/usr/share/icons/breeze/status/64/dialog-warning.svg"
        dialogTitle:"Lliurex Onedrive"+" - "+i18nd("lliurex-onedrive","Tools")
        dialogMsg:onedriveBridge.localFolderRemoved?i18nd("lliurex-onedrive","Local space folder not exists.\nAre you sure you want to resynchronize the space?\nThis action can lead to deletion of files stored on OneDrive/SharePoint"):i18nd("lliurex-onedrive","Running this action may cause local files to be overwritten with older versions\ndownloaded from OneDrive/SharePoint.\nAre you sure you want to resynchronize the space?")
        dialogWidth:560
        btnAcceptVisible:false
        btnAcceptText:""
        btnDiscardText:i18nd("lliurex-onedrive","Accept")
        btnDiscardIcon:"dialog-ok.svg"
        btnCancelText:i18nd("lliurex-onedrive","Cancel")
        btnCancelIcon:"dialog-cancel.svg"

        Connections{
            target:repairRemoveDialog
            function onDiscardDialogClicked(){
                repairRemoveDialog.close()
                repair()  
            }
            function onRejectDialogClicked(){
                repairRemoveDialog.close()
            }
        }
    } 

    ChangesDialog{
        id:updateAuthDialog
        dialogIcon:"/usr/share/icons/breeze/status/64/dialog-warning.svg"
        dialogTitle:"Lliurex Onedrive"+" - "+i18nd("lliurex-onedrive","Tools")
        dialogMsg:i18nd("lliurex-onedrive","This action will update the authorization to sync this space.\nAre you sure you want to continue?")
        dialogWidth:560
        btnAcceptVisible:false
        btnAcceptText:""
        btnDiscardText:i18nd("lliurex-onedrive","Accept")
        btnDiscardIcon:"dialog-ok.svg"
        btnCancelText:i18nd("lliurex-onedrive","Cancel")
        btnCancelIcon:"dialog-cancel.svg"

        Connections{
            target:updateAuthDialog
            function onDiscardDialogClicked(){
                updateAuthDialog.close()
                onedriveBridge.updateAuth()  
            }
            function onRejectDialogClicked(){
                updateAuthDialog.close()
                console.log("NO")
            }
        }
    }        
    CustomPopup{
        id:toolsPopup
    }
  
    function repair(){
        onedriveBridge.repairOnedrive();
    }

    function getMessageText(){

        switch (onedriveBridge.showToolsMessage[1]){
            case 18:
                var msg=i18nd("lliurex-onedrive","Some options can only be executed if the synchronization is stopped")
                break;
            case 19:
                var msg=i18nd("lliurex-onedrive","The authorization to sync the space has been updated")
                break;
            case -16:
                var msg=i18nd("lliurex-onedrive","It is not possible to update the authorization to syn the space.\nWait a moment and try again")
                break
        }
        return msg
    }

    function getTypeMessage(){

        switch (onedriveBridge.showToolsMessage[2]){
            case "Information":
                return Kirigami.MessageType.Information
            case "Ok":
                return Kirigami.MessageType.Positive
            case "Error":
                return Kirigami.MessageType.Error
        }
    }

}

