import org.kde.plasma.core 2.1 as PlasmaCore
import org.kde.kirigami 2.12 as Kirigami
import QtQuick 2.6
import QtQuick.Controls 2.6
import QtQuick.Layouts 1.12
import QtQuick.Dialogs 1.3

Rectangle{
    color:"transparent"
    Text{ 
        text:i18nd("lliurex-onedrive","Synchronized spaces")
        font.family: "Quattrocento Sans Bold"
        font.pointSize: 16
    }

    GridLayout{
        id:generalSpacesLayout
        rows:2
        flow: GridLayout.TopToBottom
        rowSpacing:10
        Layout.fillWidth: true
        anchors.left:parent.left
        enabled:true
        Kirigami.InlineMessage {
            id: messageLabel
            visible:onedriveBridge.showSpaceSettingsMessage[0]
            text:getTextMessage()
            type:getTypeMessage()
            Layout.minimumWidth:660
            Layout.maximumWidth:660
            Layout.topMargin: 40
        }

        GridLayout{
            id: optionsGrid
            rows: 1
            flow: GridLayout.TopToBottom
            rowSpacing:5
            Layout.topMargin: messageLabel.visible?0:50

            SpaceList{
                id:spacesList
                structModel:onedriveBridge.spacesModel
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
            icon.name:"list-add.svg"
            text:i18nd("lliurex-onedrive","New space")
            Layout.preferredHeight:40
            Keys.onReturnPressed: applyBtn.clicked()
            Keys.onEnterPressed: applyBtn.clicked()
            onClicked:{
                informationDialog.open()
            }
        }
    } 

    CustomPopup{
        id:spaceSettingsPopup
        
    }

    ChangesDialog{
        id:informationDialog
        dialogIcon:"/usr/share/icons/breeze/status/64/dialog-warning.svg"
        dialogTitle:"Lliurex Onedrive"+" - "+i18nd("lliurex-onedrive","New space")
        dialogVisible:false
        dialogMsg:i18nd("lliurex-onedrive","The content that is synchronized will reduce available space on the computer.\nDo you want to continue with the pairing process?")
        dialogWidth:550
        btnAcceptVisible:false
        btnAcceptText:""
        btnDiscardText:i18nd("lliurex-onedrive","Accept")
        btnDiscardIcon:"dialog-ok.svg"
        btnCancelText:i18nd("lliurex-onedrive","Cancel")
        btnCancelIcon:"dialog-cancel.svg"

        Connections{
            target:informationDialog
            function onDiscardDialogClicked(){
                informationDialog.close()
                onedriveBridge.moveToSpaceOption(1)                 
            }
            function onRejectDialogClicked(){
                informationDialog.close()
                                
            }
        }
    }       


    function getTextMessage(){
        switch (onedriveBridge.showSpaceSettingsMessage[1]){
            case 0:
                var msg=i18nd("lliurex-onedrive","The new space to synchronize has been configured successfully")
                break;
            case 15:
                var msg=i18nd("lliurex-onedrive","One or more spaces require your attention")
                break;
            case -3:
                var msg=i18nd("lliurex-onedrive","An error occurred during setup. Wait a moment and try again")
                break;
            case -17:
                var msg=i18nd("lliurex-onedrive","The available space in HDD is less than 10 GB")
                break;
            case -18:
                var msg=i18nd("lliurex-onedrive","The available space in HDD is less than 5 GB. No more content will be synced")
                break;
            case -20:
                var msg=i18nd("lliurex-onedrive","There is not enough space in HDD to sync more spaces")
                break;
            default:
                var msg=""
                break;
        }
        return msg
    }

    function getTypeMessage(){

        switch (onedriveBridge.showSpaceSettingsMessage[2]){
            case "Information":
                return Kirigami.MessageType.Information
            case "Ok":
                return Kirigami.MessageType.Positive
            case "Error":
                return Kirigami.MessageType.Error
            case "Warning":
                return Kirigami.MessageType.Warning
        }
    }
} 