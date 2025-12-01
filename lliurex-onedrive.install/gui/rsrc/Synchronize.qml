import org.kde.plasma.core 2.0 as PlasmaCore
import org.kde.plasma.components 3.0 as PC3
import org.kde.kirigami 2.12 as Kirigami
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
        width:parent.width-20
        anchors.left:parent.left
        height:{
            if (syncStackBridge.showFolderStruct){
                parent.height-90
            }else{
                0
            }
        }
        
        Kirigami.InlineMessage {
            id: messageLabel
            visible:syncStackBridge.showSynchronizeMessage[0]
            text:getTextMessage()
            type:getTypeMessage()
            Layout.minimumWidth:640
            Layout.topMargin: 40
            Layout.fillWidth: true
        }

        GridLayout{
            id: optionsGrid
            rows: 4
            flow: GridLayout.TopToBottom
            rowSpacing:10
            Layout.alignment:Qt.AlignTop
            Layout.topMargin: messageLabel.visible?0:50

            CheckBox {
                id:syncAll
                text:i18nd("lliurex-onedrive","Synchronize all folders of space")
                checked:syncStackBridge.syncAll
                enabled:getEnabledStatus()
                font.pointSize: 10
                focusPolicy: Qt.NoFocus
                onToggled:{
                    syncStackBridge.getSyncMode(checked)
                    
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
                    text:i18nd("lliurex-onedrive","Synchronize only those folders")
                    checked:!syncStackBridge.syncAll
                    enabled:getEnabledStatus()
                    font.pointSize: 10
                    focusPolicy: Qt.NoFocus
                    onToggled:syncStackBridge.getSyncMode(!checked)
                    anchors.verticalCenter:parent.verticalCenter
                }

                Button {
                    id:updateStructbtn
                    display:AbstractButton.IconOnly
                    icon.name:"view-refresh.svg"
                    enabled:{
                        if ((spaceStackBridge.localFolderRemoved)||(spaceStackBridge.localFolderEmpty)){
                            false
                        }else{
                            if ((syncCustom.checked)&&(!spaceStackBridge.isOnedriveRunning)){
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
                    onClicked:syncStackBridge.updateFolderStruct(false)
                }
            }

            FolderList{
                id:folderList
                structModel:syncStackBridge.folderModel
                structEnabled:getEnabledStatus()
                Layout.fillHeight:true
                Layout.fillWidth:true
                Layout.minimumHeight:messageLabel.visible?180:210
            }

            Row{
                id:extensionsRow
                spacing:10
                Layout.alignment:Qt.AlignLeft
                Layout.topMargin:10
                Layout.bottomMargin:10
                CheckBox {
                    id:filterExtensions
                    text:i18nd("lliurex-onedrive","Don't sync files with this extensions:")
                    checked:syncStackBridge.skipFileExtensions[0]
                    enabled:getEnabledStatus()
                    font.pointSize: 10
                    focusPolicy: Qt.NoFocus
                    onToggled:syncStackBridge.getSkipFileExtensionsEnable(checked)
                }
                FileExtensionsSelector{
                    id:fileExtensionsSelector
                    selectorEnabled:{
                        if (filterExtensions.enabled){
                            if (filterExtensions.checked){
                                true
                            }else{
                                false
                            }
                        }else{
                            false
                        }
                    }
                }
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
                if (((syncStackBridge.syncCustomChanged)||(syncStackBridge.skipFileChanged))&&(!spaceStackBridge.isOnedriveRunning)){
                    true
                }else{
                    false
                }
            }
            onClicked:{
                syncStackBridge.applySyncBtn()
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
                if (((syncStackBridge.syncCustomChanged)||(syncStackBridge.skipFileChanged))&&(!spaceStackBridge.isOnedriveRunning)){
                    true
                }else{
                    false
                }
            }            
            onClicked:syncStackBridge.cancelSyncChanges()
        }
    }

    ChangesDialog{
        id:syncDialog
        dialogIcon:"/usr/share/icons/breeze/status/64/dialog-question.svg"
        dialogTitle:"Lliurex Onedrive"+" - "+i18nd("lliurex-onedrive","Synchronize")
        dialogVisible:syncStackBridge.showSynchronizeDialog
        dialogMsg:{
            if (!syncAll.checked){
                i18nd("lliurex-onedrive","Applying the changes will only sync the content of the selected folders and have\nthe extensions allowed\nDo you want to delete the rest of the folders from this computer?")
            }else{
                i18nd("lliurex-onedrive","Applying the changes will sync all the content of your space that have\nthe extensions allowed")
            }
        }
        dialogWidth:700
        dialogHeight:120
        btnAcceptVisible:!syncAll.checked
        btnAcceptText:i18nd("lliurex-onedrive","Yes, delete unselected folders")
        btnDiscardVisible:true
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
                syncStackBridge.manageSynchronizeDialog("Accept")
            }
            function onDiscardDialogClicked(){
                syncStackBridge.manageSynchronizeDialog("Keep")  
            }
            function onRejectDialogClicked(){
                syncStackBridge.manageSynchronizeDialog("Cancel")
            }
        }
    }       
    ChangesDialog{
        id:pendingDialog
        dialogIcon:"/usr/share/icons/breeze/status/64/dialog-warning.svg"
        dialogTitle:"Lliurex Onedrive"+" - "+i18nd("lliurex-onedrive","Synchronize")
        dialogVisible:syncStackBridge.showSynchronizePendingDialog
        dialogMsg:i18nd("lliurex-onedrive","There are pending changes related to synchronization.\nDo you want apply the changes or discard them?")
        dialogWidth:450
        dialogHeight:120
        btnAcceptVisible:true
        btnAcceptText:i18nd("lliurex-onedrive","Apply")
        btnDiscardVisible:true
        btnDiscardText:i18nd("lliurex-onedrive","Discard")
        btnDiscardIcon:"delete.svg"
        btnCancelText:i18nd("lliurex-onedrive","Cancel")
        btnCancelIcon:"dialog-cancel.svg"
        Connections{
            target:pendingDialog
            function onDialogApplyClicked(){
                syncStackBridge.manageSynchronizePendingDialog("Accept")
            }
            function onDiscardDialogClicked(){
                syncStackBridge.manageSynchronizePendingDialog("Discard")  
            }
            function onRejectDialogClicked(){
                closeTimer.stop()
                syncStackBridge.manageSynchronizePendingDialog("Cancel")
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

        switch (syncStackBridge.showSynchronizeMessage[1]){

            case 4:
                var msg=i18nd("lliurex-onedrive","Functionality available only if sync is stopped");
                break

            case 5:
                var msg=i18nd("lliurex-onedrive","Changes applied correctly");
                break

            case -4:
                var msg=i18nd("lliurex-onedrive","An error occurred while applying the changes. Press Cancel and resync the space");
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

        switch (syncStackBridge.showSynchronizeMessage[2]){

            case "Information":
                return Kirigami.MessageType.Information

            case "Ok":
                return Kirigami.MessageType.Positive

            case "Error":
                return Kirigami.MessageType.Error

        }


    }

    function getEnabledStatus(){
        if ((spaceStackBridge.localFolderRemoved)||(spaceStackBridge.localFolderEmpty) || (spaceStackBridge.isUpdateRequired)){
            return false
        }else{
            if (spaceStackBridge.isOnedriveRunning){
                return false
            }else{
                return true
            }
        }
    }

}
