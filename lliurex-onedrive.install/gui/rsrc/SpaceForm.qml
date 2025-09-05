import org.kde.plasma.core 2.0 as PlasmaCore
import org.kde.kirigami 2.12 as Kirigami
import QtQuick 2.6
import QtQuick.Controls 2.6
import QtQuick.Layouts 1.12
import QtQuick.Dialogs 1.3


Rectangle{
    color:"transparent"

    Text{ 
        text:mainStackBridge.requiredMigration?i18nd("lliurex-onedrive","Configuration Migration"):i18nd("lliurex-onedrive","New space")
        font.family: "Quattrocento Sans Bold"
        font.pointSize: 16
    }
    GridLayout{
        id:newSpaceLayout
        rows:2
        flow: GridLayout.TopToBottom
        rowSpacing:10
        anchors.left:parent.left
        width:parent.width-10
 
        Kirigami.InlineMessage {
            id: newSpaceMessageLabel
            visible:addSpaceStackBridge.showSpaceFormMessage[0]
            text:getTextMessage()
            type:getTypeMessage()
            Layout.minimumWidth:650
            Layout.fillWidth:true
            Layout.topMargin: 40
        }

        GridLayout{
            id: newSpaceOptions
            columns: 2
            flow: GridLayout.LeftToRight
            columnSpacing:15
            rowSpacing:20
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
                text:addSpaceStackBridge.formData[0]
                validator:RegExpValidator { regExp:/\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*/ }
                implicitWidth:400
                onTextChanged:{
                    addSpaceStackBridge.resetSharePoints()
                }
            }

            Text{
                id:spaceType
                Layout.alignment:Qt.AlignRight|Qt.AlignTop
                text:i18nd("lliurex-onedrive","Space Type:")
                font.family: "Quattrocento Sans Bold"
                font.pointSize: 10
           }

            ButtonGroup{
                buttons:typeOptions.children
            }

            Column{
                id:typeOptions
                spacing:5
                Layout.alignment:Qt.AlignTop

                RadioButton{
                    id:oneDriveOption
                    checked:addSpaceStackBridge.formData[1]==0?true:false
                    text:i18nd("lliurex-onedrive","OneDrive")
                    onToggled:{
                        if (checked){
                            addSpaceStackBridge.resetSharePoints()
                        }
                    }
                }

                RadioButton{
                    id:oneDriveBackupOption
                    checked:addSpaceStackBridge.formData[1]==3?true:false
                    text:i18nd("lliurex-onedrive","OneDrive-Backup")
                    onToggled:{
                        if (checked){
                            addSpaceStackBridge.resetSharePoints()
                        }
                    }
                }

                RadioButton{
                    id:sharePointOption
                    checked:addSpaceStackBridge.formData[1]==1?true:false
                    text:i18nd("lliurex-onedrive","SharePoint")
                    enabled:!addSpaceStackBridge.requiredMigration
                    onToggled:{
                        if (spaceMailEntry.acceptableInput){
                            addSpaceStackBridge.getSpaceSharePoints([spaceMailEntry.text,1])
                        }else{
                            sharePointOption.checked=false
                            oneDriveOption.checked=true
                            oneDriveBackupOption.checked=false
                        }
                    }
                }
            }

            Text{
                id:spaceSharePoint
                Layout.alignment:Qt.AlignRight
                text:i18nd("lliurex-onedrive","SharePoint name:")
                font.family: "Quattrocento Sans Bold"
                font.pointSize: 10
                visible:sharePointVisible()
            }
            ComboBox{
                id:spaceSharePointEntry
                font.pointSize:10
                textRole:"nameSharePoint"
                model:addSpaceStackBridge.sharePointModel
                implicitWidth:400
                visible:sharePointVisible()
                onActivated:addSpaceStackBridge.getSharePointLibraries(spaceSharePointEntry.currentText)
            }
            Text{
                id:spaceLibrary
                Layout.alignment:Qt.AlignRight
                text:i18nd("lliurex-onedrive","Library to sync:")
                font.family: "Quattrocento Sans Bold"
                font.pointSize: 10
                visible:libraryVisible()
            }
            ComboBox{
                id:spaceLibraryEntry
                font.pointSize:10
                textRole:"nameLibrary"
                valueRole:"idLibrary"
                model:addSpaceStackBridge.libraryModel
                implicitWidth:400
                visible:libraryVisible()
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
            enabled:getEnabledStatus()
            Keys.onReturnPressed: applyBtn.clicked()
            Keys.onEnterPressed: applyBtn.clicked()
            onClicked:{
                var type=""
                if (oneDriveOption.checked){
                    type="onedrive"
                }else{
                    if (oneDriveBackupOption.checked){
                        type="onedriveBackup"
                    }else{
                        if (sharePointOption.checked){
                            type="sharepoint"
                        }
                    }
                }
                addSpaceStackBridge.checkData([spaceMailEntry.text,type,spaceSharePointEntry.currentText,spaceLibraryEntry.currentText,spaceLibraryEntry.currentValue])
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
                if (!addSpaceStackBridge.requiredMigration){
                    mainStackBridge.moveToSpaceOption(0);
                }else{
                     mainStackBridge.moveToSpaceOption(3);
                   
                }
            }
        }
    } 

    CustomPopup{
        id:spaceFormPopup
        
    }

    ChangesDialog{
        id:previousFolderDialog
        dialogIcon:"/usr/share/icons/breeze/status/64/dialog-warning.svg"
        dialogTitle:"Lliurex Onedrive"+" - "+i18nd("lliurex-onedrive","New space")
        dialogVisible:addSpaceStackBridge.showPreviousFolderDialog
        dialogMsg:i18nd("lliurex-onedrive","The local folder (with content) to be used for synchronization has been detected.\nIf you link this computer with this OneDrive/SharePoint space, the existing content in that folder will be added to OneDrive/SharePoint.\nDo you want to continue with the pairing process?")
        dialogWidth:700
        dialogHeight:120
        btnAcceptVisible:false
        btnAcceptText:""
        btnDiscardText:i18nd("lliurex-onedrive","Accept")
        btnDiscardIcon:"dialog-ok.svg"
        btnCancelText:i18nd("lliurex-onedrive","Cancel")
        btnCancelIcon:"dialog-cancel.svg"

        Connections{
            target:previousFolderDialog
            function onDiscardDialogClicked(){
                previousFolderDialog.close()
                addSpaceStackBridge.managePreviousFolderDialog(0)                 
            }
            function onRejectDialogClicked(){
                previousFolderDialog.close()
                addSpaceStackBridge.managePreviousFolderDialog(1)                 
            }
        }
    }
   
    ChangesDialog{
        id:downloadDialog
        dialogIcon:"/usr/share/icons/breeze/status/64/dialog-warning.svg"
        dialogTitle:"Lliurex Onedrive"+" - "+i18nd("lliurex-onedrive","New space")
        dialogVisible:addSpaceStackBridge.showDownloadDialog
        dialogMsg:i18nd("lliurex-onedrive","Its content in OneDrive/SharePoint is approximately ")+addSpaceStackBridge.initialDownload+i18nd("lliurex-onedrive","\nThe space available on the computer is ")+addSpaceStackBridge.hddFreeSpace+getLastMessage()
        dialogWidth:710
        dialogHeight:120
        btnAcceptVisible:false
        btnAcceptText:""
        btnDiscardText:addSpaceStackBridge.withHDDSpace?i18nd("lliurex-onedrive","Start syncing all content"):i18nd("lliurex-onedrive","Select content to synchronize and/or review settings")
        btnDiscardIcon:addSpaceStackBridge.withHDDSpace?"dialog-ok.svg":"configure.svg"
        btnCancelText:addSpaceStackBridge.withHDDSpace?i18nd("lliurex-onedrive","Select content to synchronize and/or review settings"):i18nd("lliurex-onedrive","Cancel")
        btnCancelIcon:addSpaceStackBridge.withHDDSpace?"configure.svg":"dialog-cancel.svg"
        Connections{
            target:downloadDialog
            function onDiscardDialogClicked(){
                if (addSpaceStackBridge.withHDDSpace){
                    addSpaceStackBridge.manageDownloadDialog("All")
                }else{
                    addSpaceStackBridge.manageDownloadDialog("Custom")
                }
            }
            function onRejectDialogClicked(){
                if (addSpaceStackBridge.withHDDSpace){
                    addSpaceStackBridge.manageDownloadDialog("Custom")
                }else{
                    addSpaceStackBridge.manageDownloadDialog("Cancel")
                }
            }
        }               
    
    }

    ChangesDialog{
        id:backupDialog
        dialogIcon:"/usr/share/icons/breeze/status/64/dialog-warning.svg"
        dialogTitle:"Lliurex Onedrive"+" - "+i18nd("lliurex-onedrive","New space")
        dialogVisible:addSpaceStackBridge.showBackupDialog
        dialogMsg:i18nd("lliurex-onedrive","You're going to set up a space that will only send files from your computer to the LLIUREX_ONEDRIVE_BACKUP folder in your OneDrive account. Remember:\n- Don't delete o rename the LLIUREX_ONEDRIVE_BACKUP folder from your computer\n- Files copied to the local folder LLIUREX_ONEDRIVE_BACKUP on your computer will be deleted from it once they are sent to the corresponding OneDrive account")
        dialogWidth:700
        dialogHeight:140
        btnAcceptVisible:true
        btnAcceptText:i18nd("lliurex-onedrive","Start now")
        btnDiscardText:i18nd("lliurex-onedrive","Review settings")
        btnDiscardIcon:"configure.svg"
        btnCancelText:i18nd("lliurex-onedrive","Cancel")
        btnCancelIcon:"dialog-cancel.svg"
        Connections{
            target:backupDialog
            function onDialogApplyClicked(){
                addSpaceStackBridge.manageBackupDialog("Start")
            }
            function onDiscardDialogClicked(){
                addSpaceStackBridge.manageBackupDialog("Custom")
            }
            function onRejectDialogClicked(){
                addSpaceStackBridge.manageBackupDialog("Cancel")
            }
        }               
    
    }

    function getTextMessage(){
        switch (addSpaceStackBridge.showSpaceFormMessage[1]){
            case -1:
                var msg=i18nd("lliurex-onedrive","A OneDrive/SharePoint space associated with the indicated email is already being synced");
                break
            case -2:
                var msg=i18nd("lliurex-onedrive","No libraries found for the indicated SharePoint");
                break
            case -14:
                var msg=i18nd("lliurex-onedrive","No SharePoints found for the indicated email");
                break
            case -15:
                var msg=i18nd("lliurex-onedrive","Unable to migrate old configuration");
                break
            case -19:
                var msg=i18nd("lliurex-onedrive","Unable to get authorization to sync space.\nWait a moment and try again")
                break
            default:
                var msg=""
                break;
        }
        return msg
    }

    function getTypeMessage(){

        switch (addSpaceStackBridge.showSpaceFormMessage[2]){
            case "Information":
                return Kirigami.MessageType.Information
            case "Ok":
                return Kirigami.MessageType.Positive
            case "Error":
                return Kirigami.MessageType.Error
        }
    }

    function getEnabledStatus(){

        var correctMail=spaceMailEntry.acceptableInput
        if (correctMail){
            if (oneDriveOption.checked || oneDriveBackupOption.checked){
                return true
            }else{
                if ((spaceSharePointEntry.length!=0) && (spaceLibraryEntry.currentText!="")){
                    return true
                }
            }
        }
        return false
    }

    function sharePointVisible(){

        if (sharePointOption.checked){
            if (spaceSharePointEntry.count>0){
                return true
            }
        }
        return false
    }

    function libraryVisible(){

        if (sharePointOption.checked){
            if ((spaceSharePointEntry.length!=0) && (spaceLibraryEntry.count>0)){
                 return true
            }
        }
        return false
    }

    function getLastMessage(){

        if (addSpaceStackBridge.withHDDSpace){
            var msg=i18nd("lliurex-onedrive","\nThe content that is synchronized will reduce available space on the computer.\nDo you want to start syncing or select the content and/or review settings?")
        }else{
            var msg=i18nd("lliurex-onedrive","\nThere is no space available on the HDD to sync all the content.\nDo you want to select the content and/or review settings or cancel the space settings?")
        }
        return msg

    }
}



