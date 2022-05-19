import org.kde.plasma.core 2.0 as PlasmaCore
import org.kde.kirigami 2.6 as Kirigami
import QtQuick 2.6
import QtQuick.Controls 2.6
import QtQuick.Layouts 1.12
import QtQuick.Dialogs 1.3


Rectangle{
    color:"transparent"
    property alias email:spaceMailEntry.text
    property alias onedriveRb:oneDriveOption.checked
    /*property alias sharePoint:spaceSharePointEntry.text*/

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
            visible:onedriveBridge.showSpaceFormMessage[0]
            text:getTextMessage()
            type:getTypeMessage()
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
                validator:RegExpValidator { regExp:/\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*/ }
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
                    checked:true
                    text:"OneDrive"
                }

                RadioButton{
                    id:sharePointOption
                    checked:false
                    text:"SharePoint"
                    onToggled:onedriveBridge.getSpaceSharePoints(spaceMailEntry.text)
                }
            }
            Text{
                id:spaceSharePoint
                Layout.bottomMargin:10
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
                model:onedriveBridge.sharePointModel
                implicitWidth:400
                visible:sharePointVisible()
                onActivated:onedriveBridge.getSharePointLibraries(spaceSharePointEntry.currentText)
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
                model:onedriveBridge.libraryModel
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
                oneDriveAuth.authUrl=onedriveBridge.authUrl
                var type=""
                if (oneDriveOption.checked){
                    type="onedrive"
                }else{
                    type="sharepoint"
                }
                onedriveBridge.checkData([spaceMailEntry.text,type,spaceSharePointEntry.currentText,spaceLibraryEntry.currentText,spaceLibraryEntry.currentValue])
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

    CustomPopup{
        id:spaceFormPopup
        
    }

    Dialog{
        id: previousFolderDialog
        visible:onedriveBridge.showPreviousFolderDialog
        title:"Lliurex Onedrive"+" - "+i18nd("lliurex-onedrive","Account")
        modality:Qt.WindowModal

        contentItem: Rectangle {
            color: "#ebeced"
            implicitWidth: 700
            implicitHeight: 115
            anchors.topMargin:5
            anchors.leftMargin:5

            Image{
                id:previousFolderDialogIcon
                source:"/usr/share/icons/breeze/status/64/dialog-warning.svg"

            }
            
            Text {
                id:previousFolderDialogText
                text:i18nd("lliurex-onedrive","The local folder (with content) to be used for synchronization has been detected.\nIf you link this computer with this OneDrive/SharePoint space, the existing content in that folder\nwill be added to OneDrive/SharePoint.\nDo you want to continue with the pairing process?")
                font.family: "Quattrocento Sans Bold"
                font.pointSize: 10
                anchors.left:previousFolderDialogIcon.right
                anchors.verticalCenter:previousFolderDialogIcon.verticalCenter
                anchors.leftMargin:10
            
            }
          
            DialogButtonBox {
                buttonLayout:DialogButtonBox.KdeLayout
                anchors.bottom:parent.bottom
                anchors.right:parent.right
                anchors.topMargin:15

                Button {
                    id:previousFolderDialogApplyBtn
                    display:AbstractButton.TextBesideIcon
                    icon.name:"dialog-ok.svg"
                    text: i18nd("lliurex-onedrive","Accept")
                    font.family: "Quattrocento Sans Bold"
                    font.pointSize: 10
                    DialogButtonBox.buttonRole: DialogButtonBox.ApplyRole
                }

                Button {
                    id:previousFolderDialogCancelBtn
                    display:AbstractButton.TextBesideIcon
                    icon.name:"dialog-cancel.svg"
                    text: i18nd("lliurex-onedrive","Cancel")
                    font.family: "Quattrocento Sans Bold"
                    font.pointSize: 10
                    DialogButtonBox.buttonRole:DialogButtonBox.RejectRole
                }

                onApplied:{
                    previousFolderDialog.close()
                    onedriveBridge.managePreviousFolderDialog(0)                 
            
                }

                onRejected:{
                    previousFolderDialog.close()
                    onedriveBridge.managePreviousFolderDialog(1)                 

                }
            }
        }
    }

    Dialog{
        id: downloadDialog
        visible:onedriveBridge.showDownloadDialog
        title:"Lliurex Onedrive"+" - "+i18nd("lliurex-onedrive","New Space")
        modality:Qt.WindowModal

        contentItem: Rectangle {
            color: "#ebeced"
            implicitWidth: 700
            implicitHeight: 115
            anchors.topMargin:5
            anchors.leftMargin:5

            Image{
                id:dialogIcon
                source:"/usr/share/icons/breeze/status/64/dialog-warning.svg"

            }
            
            Text {
                id:dialogText
                text:i18nd("lliurex-onedrive","Its content in OneDrive is approximately ")+onedriveBridge.initialDownload+i18nd("lliurex-onedrive","\nThe space available on the computer is ")+onedriveBridge.hddFreeSpace+
                i18nd("lliurex-onedrive","\nThe content that is synchronized will reduce available space on the computer.\nDo you want to sync all the content or do you prefer to select the content to sync?")
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
                    text: i18nd("lliurex-onedrive","Synchronize all content")
                    font.family: "Quattrocento Sans Bold"
                    font.pointSize: 10
                    DialogButtonBox.buttonRole: DialogButtonBox.ApplyRole
                }

                Button {
                    id:dialogCancelBtn
                    display:AbstractButton.TextBesideIcon
                    icon.name:"configure.svg"
                    text: i18nd("lliurex-onedrive","Select content to synchronize")
                    font.family: "Quattrocento Sans Bold"
                    font.pointSize: 10
                    DialogButtonBox.buttonRole:DialogButtonBox.RejectRole
                }

                onApplied:{
                                      
                    onedriveBridge.manageDownloadDialog("All")
                
                }

                onRejected:{
                    onedriveBridge.manageDownloadDialog("Custom")

                }
            }
        }
     }


    function getTextMessage(){
        switch (onedriveBridge.showSpaceFormMessage[1]){
            case -1:
                var msg=i18nd("lliurex-onedrive","A OneDrive space associated with the indicated email is already being synced");
                break
            case -2:
                var msg=i18nd("lliurex-onedrive","No libraries found for the indicated SharePoint");
                break
            case -14:
                var msg=i18nd("lliurex-onedrive","No SharePoints found for the indicated email");
                break
            default:
                var msg=""
                break;
        }
        return msg
    }

    function getTypeMessage(){

        switch (onedriveBridge.showSpaceFormMessage[2]){
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
            if (oneDriveOption.checked){
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
}



