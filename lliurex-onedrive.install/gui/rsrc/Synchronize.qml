import org.kde.plasma.core 2.0 as PlasmaCore
import org.kde.kirigami 2.6 as Kirigami
import QtQuick 2.6
import QtQuick.Controls 2.6
import QtQuick.Layouts 1.12
import QtQuick.Dialogs 1.3


Rectangle{
    property alias structModel:folderList.structModel

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
            visible:onedriveBridge.showSynchronizeMessage[0]
            text:getTextMessage()
            type:getTypeMessage()
            Layout.minimumWidth:650
            Layout.maximumWidth:650
            Layout.topMargin: 40
            Layout.leftMargin: 10
        }

        GridLayout{
            id: optionsGrid
            rows: 3
            flow: GridLayout.TopToBottom
            rowSpacing:10
            Layout.topMargin: messageLabel.visible?0:50

            CheckBox {
                id:syncAll
                text:i18nd("lliurex-onedrive","Synchronize all content of space")
                checked:onedriveBridge.syncAll
                enabled:getEnabledStatus()
                font.pointSize: 10
                focusPolicy: Qt.NoFocus
                onToggled:{
                    onedriveBridge.getSyncMode(checked)
                    
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
                    checked:!onedriveBridge.syncAll
                    enabled:getEnabledStatus()
                    font.pointSize: 10
                    focusPolicy: Qt.NoFocus
                    onToggled:onedriveBridge.getSyncMode(!checked)
                    anchors.verticalCenter:parent.verticalCenter
                }

                Button {
                    id:updateStructbtn
                    display:AbstractButton.IconOnly
                    icon.name:"view-refresh.svg"
                    enabled:{
                        if ((onedriveBridge.localFolderRemoved)||(onedriveBridge.localFolderEmpty)){
                            false
                        }else{
                            if ((syncCustom.checked)&&(!onedriveBridge.isOnedriveRunning)){
                                true
                            }else{
                                false
                            }
                        }
                    }

                    Layout.preferredHeight: 35
                    anchors.verticalCenter:parent.verticalCenter
                    ToolTip.delay: 1000
                    ToolTip.timeout: 3000
                    ToolTip.visible: hovered
                    ToolTip.text:i18nd("lliurex-onedrive","Click to update the space folder structure")
                    hoverEnabled:true
                    onClicked:onedriveBridge.updateFolderStruct(false)
                }
            }
            FolderList{
                id:folderList
                structModel:onedriveBridge.folderModel
                structEnabled:getEnabledStatus()
            }
        }
    }

    RowLayout{
        id:btnBox
        anchors.bottom: parent.bottom
        anchors.right:parent.right
        anchors.bottomMargin:15
        anchors.rightMargin:15
        spacing:10

        Button {
            id:applyBtn
            visible:true
            display:AbstractButton.TextBesideIcon
            icon.name:"dialog-ok.svg"
            text:i18nd("lliurex-onedrive","Apply")
            Layout.preferredHeight: 40
            enabled:{
                if ((onedriveBridge.syncCustomChanged)&&(!onedriveBridge.isOnedriveRunning)){
                    true
                }else{
                    false
                }
            }
            onClicked:{
                onedriveBridge.applySyncBtn()
            }
        }
        Button {
            id:cancelBtn
            visible:true
            display:AbstractButton.TextBesideIcon
            icon.name:"dialog-cancel.svg"
            text:i18nd("lliurex-onedrive","Cancel")
            Layout.preferredHeight: 40
            enabled:{
                if ((onedriveBridge.syncCustomChanged)&&(!onedriveBridge.isOnedriveRunning)){
                    true
                }else{
                    false
                }
            }            
            onClicked:onedriveBridge.cancelSyncChanges()
        }
    }

    ChangesDialog{
        id:syncDialog
        dialogIcon:"/usr/share/icons/breeze/status/64/dialog-question.svg"
        dialogTitle:"Lliurex Onedrive"+" - "+i18nd("lliurex-onedrive","Synchronize")
        dialogVisible:onedriveBridge.showSynchronizeDialog
        dialogMsg:{
            if (!syncAll.checked){
                i18nd("lliurex-onedrive","Applying the changes will only sync the content of the selected folders\nDo you want to delete the rest of the folders from this computer?")
            }else{
                i18nd("lliurex-onedrive","Applying the changes will sync all the content of your space")
            }
        }
        dialogWidth:700
        btnAcceptVisible:!syncAll.checked
        btnAcceptText:i18nd("lliurex-onedrive","Yes, delete unselected folders")
        btnDiscardText:{
            if (!syncAll.checked){
                i18nd("lliurex-onedrive","No, keep folders unselected")
            }else{
                i18nd("lliurex-onedrive","Accept")
            }
                        
        }
        btnDiscardIcon:"dialog-ok.svg"
        btnCancelText:i18nd("lliurex-onedrive","Cancel")
        btnCancelIcon:"dialog-cancel.svg"
        Connections{
            target:syncDialog
            function onDialogApplyClicked(){
                onedriveBridge.manageSynchronizeDialog("Accept")
            }
            function onDiscardDialogClicked(){
                onedriveBridge.manageSynchronizeDialog("Keep")  
            }
            function onRejectDialogClicked(){
                onedriveBridge.manageSynchronizeDialog("Cancel")
            }
        }
    }       
    ChangesDialog{
        id:pendingDialog
        dialogIcon:"/usr/share/icons/breeze/status/64/dialog-warning.svg"
        dialogTitle:"Lliurex Onedrive"+" - "+i18nd("lliurex-onedrive","Synchronize")
        dialogVisible:onedriveBridge.showSynchronizePendingDialog
        dialogMsg:i18nd("lliurex-onedrive","There are pending changes related to synchronization.\nDo you want apply the changes or discard them?")
        dialogWidth:400
        btnAcceptVisible:true
        btnAcceptText:i18nd("lliurex-onedrive","Apply")
        btnDiscardText:i18nd("lliurex-onedrive","Discard")
        btnDiscardIcon:"delete.svg"
        btnCancelText:i18nd("lliurex-onedrive","Cancel")
        btnCancelIcon:"dialog-cancel.svg"
        Connections{
            target:pendingDialog
            function onDialogApplyClicked(){
                onedriveBridge.manageSynchronizePendingDialog("Accept")
            }
            function onDiscardDialogClicked(){
                onedriveBridge.manageSynchronizePendingDialog("Discard")  
            }
            function onRejectDialogClicked(){
                onedriveBridge.manageSynchronizePendingDialog("Cancel")
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

    function getTextMessage(){

        switch (onedriveBridge.showSynchronizeMessage[1]){

            case 4:
                var msg=i18nd("lliurex-onedrive","Functionality available only if sync is stopped");
                break

            case 5:
                var msg=i18nd("lliurex-onedrive","Changes applied correctly");
                break

            case -4:
                var msg=i18nd("lliurex-onedrive","An error occurred while applying the changes");
                break
                
            case -5:
                var msg=i18nd("lliurex-onedrive","An error occurred while getting the space folder structure");
                break

            default:
                var msg=""
                break
        }
        return msg

    }

    function getTypeMessage(){

        switch (onedriveBridge.showSynchronizeMessage[2]){

            case "Information":
                return Kirigami.MessageType.Information

            case "Ok":
                return Kirigami.MessageType.Positive

            case "Error":
                return Kirigami.MessageType.Error

        }


    }

    function getEnabledStatus(){
        if ((onedriveBridge.localFolderRemoved)||(onedriveBridge.localFolderEmpty)){
            return false
        }else{
            if (onedriveBridge.isOnedriveRunning){
                return false
            }else{
                return true
            }
        }
    }

}
