import org.kde.plasma.core as PlasmaCore
import org.kde.kirigami as Kirigami
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Dialogs


Rectangle{
    color:"transparent"

    Text{ 
        text:i18nd("lliurex-onedrive","Settings")
        font.family: "Quattrocento Sans Bold"
        font.pointSize: 16
    }

    GridLayout{
        id:generalLayout
        rows:2
        flow: GridLayout.TopToBottom
        rowSpacing:10
        anchors.horizontalCenter:parent.horizontalCenter
        width:parent.width-20

        Kirigami.InlineMessage {
            id: settingsMessageLabel
            visible:settingsStackBridge.showSettingsMessage[0]
            text:getMessageText()
            type: {
                if (settingsStackBridge.showSettingsMessage[1]==""){
                    Kirigami.MessageType.Positive;
                }else{
                    Kirigami.MessageType.Error;
                }
            }
            Layout.minimumWidth:640
            Layout.fillWidth:true
            Layout.topMargin: 40
        }

        GridLayout{
            id: settingsGrid
            columns: 2
            flow: GridLayout.LeftToRight
            columnSpacing:10
            Layout.topMargin: settingsMessageLabel.visible?0:50
            Layout.alignment:Qt.AlignHCenter
            Layout.rightMargin:15

            Text{
                id:autoStartText
                text:i18nd("lliurex-onedrive","Synchronization start:")
                font.family: "Quattrocento Sans Bold"
                font.pointSize:10
                Layout.bottomMargin:10
                Layout.alignment:Qt.AlignRight
            }

            CheckBox {
                id:autoStartValue
                text:i18nd("lliurex-onedrive","Start when booting the system")
                checked:settingsStackBridge.autoStartEnabled
                enabled:getEnabledStatus()
                font.family: "Quattrocento Sans Bold"
                font.pointSize: 10
                focusPolicy: Qt.NoFocus
                onToggled:settingsStackBridge.manageAutoStart(autoStartValue.checked);
                Layout.bottomMargin:10
                Layout.alignment:Qt.AlignLeft
            }

            Text {
                id:monitorIntervalText
                text:i18nd("lliurex-onedrive","Synchronize remote changes every (in minutes):")
                font.family: "Quattrocento Sans Bold"
                font.pointSize: 10
                Layout.alignment:Qt.AlignRight
                Layout.bottomMargin:10
            }

            SpinBox{
                id:monitorIntervalValues
                from:5
                to:60
                stepSize:1
                value:settingsStackBridge.monitorInterval
                Layout.alignment:Qt.AlignLeft
                Layout.bottomMargin:10
                enabled:getEnabledStatus()
                onValueModified:{
                    settingsStackBridge.getMonitorInterval(value)
                }
            }

            Text{
                id:bandwidth
                text:i18nd("lliurex-onedrive","Download/Upload network bandwidth:")
                font.family: "Quattrocento Sans Bold"
                font.pointSize: 10
                Layout.alignment:Qt.AlignRight
                Layout.bottomMargin:10
            }

            ComboBox{
                id:bandwidthValues
                currentIndex:settingsStackBridge.rateLimit
                model:settingsStackBridge.bandWidthNames
                Layout.alignment:Qt.AlignLeft
                Layout.bottomMargin:10
                Layout.preferredWidth:100
                enabled:getEnabledStatus()
                onActivated:{
                    settingsStackBridge.getRateLimit(bandwidthValues.currentIndex)
                }
            }
            Text{
                id:skipSizeText
                text:i18nd("lliurex-onedrive","Maximun fize size to sync:")
                font.family: "Quattrocento Sans Bold"
                font.pointSize: 10
                Layout.alignment:Qt.AlignRight
                Layout.bottomMargin:10
            }
            RowLayout{
                CheckBox {
                    id:skipSizeCB
                    text:i18nd("lliurex-onedrive","Don't sync files larger than")
                    font.family: "Quattrocento Sans Bold"
                    font.pointSize: 10
                    focusPolicy: Qt.NoFocus
                    checked:settingsStackBridge.skipSize[0]
                    enabled:getEnabledStatus()
                    Layout.bottomMargin:10
                    Layout.rightMargin:5
                    Layout.alignment:Qt.AlignLeft
                    onToggled:settingsStackBridge.getSkipSize([skipSizeCB.checked,skipSizeValues.currentIndex])

                }
                ComboBox{
                    id:skipSizeValues
                    currentIndex:settingsStackBridge.skipSize[1]
                    model:settingsStackBridge.maxFileSizeNames
                    enabled:skipSizeCB.checked
                    Layout.alignment:Qt.AlignVCenter
                    Layout.bottomMargin:10
                    Layout.preferredWidth:100
                    onActivated:{
                        settingsStackBridge.getSkipSize([skipSizeCB.checked,skipSizeValues.currentIndex])
                    }
                }
            }
            Text{
                id:fileNotifications
                text:i18nd("lliurex-onedrive","Show notifications:")
                Layout.alignment: Qt.AlignRight
                Layout.bottomMargin:10

            }
            CheckBox {
                id:fileNotificationsValue
                text:i18nd("lliurex-onedrive","Notifications of actions on files/folders")
                checked:settingsStackBridge.fileNotificationsEnabled
                enabled:getEnabledStatus()
                font.family: "Quattrocento Sans Bold"
                font.pointSize: 10
                focusPolicy: Qt.NoFocus
                onToggled:settingsStackBridge.manageFileNotifications(fileNotificationsValue.checked)
                Layout.bottomMargin:10
                Layout.alignment:Qt.AlignLeft
                ToolTip.delay: 1000
                ToolTip.timeout: 3000
                ToolTip.visible: hovered
                ToolTip.text:i18nd("lliurex-onedrive","Click to receive notifications about file uploads/downloads and file and folders deletions")
            }
            Text{
                id:managementLog
                text:i18nd("lliurex-onedrive","Log management:")
                Layout.alignment: Qt.AlignRight

            }

            CheckBox {
                id:enableLogCB
                text:i18nd("lliurex-onedrive","Activate log")
                checked:settingsStackBridge.logEnabled
                enabled:true
                font.family: "Quattrocento Sans Bold"
                font.pointSize: 10
                focusPolicy: Qt.NoFocus
                onToggled:settingsStackBridge.getLogEnabled(enableLogCB.checked)
            }
            Text{

            }    
            Row{
                id:logRow
                spacing:10

                Text{
                   id:sizeLog
                   text:i18nd("lliurex-onedrive","Log file size:")
                   anchors.verticalCenter:manageLogBtn.verticalCenter
                }
                Text{
                    id:sizeLogValue
                    text:settingsStackBridge.logSize
                    anchors.verticalCenter:manageLogBtn.verticalCenter
                }
                Button {
                    id:manageLogBtn
                    display:AbstractButton.IconOnly
                    icon.name:"configure.svg"
                    Layout.preferredHeight: 30
                    Layout.alignment: Qt.AlignVCenter
                    hoverEnabled:true
                    enabled:{
                        if (settingsStackBridge.logSize!=""){
                            true
                        }else{
                            false
                        }
                    }
                    ToolTip.delay: 1000
                    ToolTip.timeout: 3000
                    ToolTip.visible: hovered
                    ToolTip.text:i18nd("lliurex-onedrive","Click to manage log file")

                    onClicked:optionsMenu.open()

                    Menu{
                        id:optionsMenu
                        y: manageLogBtn.height
                        x:-(optionsMenu.width-manageLogBtn.width/2)

                        MenuItem{
                            icon.name:"document-preview-archive.svg"
                            text:i18nd("lliurex-onedrive","View log file")
                            onClicked:{
                                settingsStackBridge.openSpaceLogFile()
                            }
                        }
                        MenuItem{
                            icon.name:"delete.svg"
                            text:i18nd("lliurex-onedrive","Delete log file")
                            onClicked:{
                                removeLogDialog.open()
                            }
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

        Button {
            id:applyBtn
            visible:true
            enabled:settingsStackBridge.settingsChanged
            display:AbstractButton.TextBesideIcon
            icon.name:"dialog-ok.svg"
            text:i18nd("lliurex-onedrive","Apply")
            Layout.preferredHeight: 40

            onClicked:{
              settingsStackBridge.applySettingsChanges()
            }
        }
        Button {
            id:cancelBtn
            visible:true
            enabled:settingsStackBridge.settingsChanged
            display:AbstractButton.TextBesideIcon
            icon.name:"dialog-cancel.svg"
            text:i18nd("lliurex-onedrive","Cancel")
            Layout.preferredHeight: 40

            onClicked:{
                settingsStackBridge.cancelSettingsChanges()
            }
        }
    

    }

    CustomPopup{
        id:settingsPopup
    }

    ChangesDialog{
        id:settingsChangesDialog
        dialogIcon:"/usr/share/icons/breeze/status/64/dialog-warning.svg"
        dialogVisible:settingsStackBridge.showSettingsDialog
        dialogMsg:i18nd("lliurex-onedrive","The settings of space have changed.\nDo you want apply the changes or discard them?")
        dialogWidth:400
        dialogHeight:120
        btnAcceptVisible:true
        btnAcceptText:i18nd("lliurex-onedrive","Apply")
        btnDiscardVisible:true
        btnDiscardText:i18nd("lliurex-onedrive","Discard")
        btnDiscardIcon:"delete.svg"
        btnCancelText:i18nd("lliurex-onedrive","Cancel")
        btnCancelIcon:"dialog-cancel.svg"
        Connections{
            target:settingsChangesDialog
            function onDialogApplyClicked(){
                settingsStackBridge.manageSettingsDialog("Accept")
            }
            function onDiscardDialogClicked(){
                settingsStackBridge.manageSettingsDialog("Discard")           
            }
            function onRejectDialogClicked(){
                closeTimer.stop()
                settingsStackBridge.manageSettingsDialog("Cancel")       
            }

        }
    }

    ChangesDialog{
        id:removeLogDialog
        dialogIcon:"/usr/share/icons/breeze/status/64/dialog-question.svg"
        dialogMsg:i18nd("lliurex-onedrive","Are you sure you want to delete log file?")
        dialogWidth:400
        dialogHeight:120
        btnAcceptVisible:false
        btnAcceptText:""
        btnDiscardVisible:true
        btnDiscardText:i18nd("lliurex-onedrive","Accept")
        btnDiscardIcon:"dialog-ok.svg"
        btnCancelText:i18nd("lliurex-onedrive","Cancel")
        btnCancelIcon:"dialog-cancel.svg"
        Connections{
            target:removeLogDialog
            function onDiscardDialogClicked(){
                removeLogDialog.close()
                settingsStackBridge.removeLogFile()
            }
            function onRejectDialogClicked(){
                removeLogDialog.close()
            }
        }

    }
  
    function getMessageText(){

        switch (settingsStackBridge.showSettingsMessage[1]){
            case -10:
                var msg=i18nd("lliurex-onedrive","Failed to change synchronization boot configuration");
                break;
            case -20:
                var msg=i18nd("lliurex-onedrive","Failed to write configuration file");
                break;
            case -30:
                var msg=i18nd("lliurex-onedrive","Failed to apply configuration changes");
                break;
            default :
                var msg=i18nd("lliurex-onedrive","The changes will take effect the next time you start session or synchronization");
                break;
        }
        return msg
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

    function getEnabledStatus(){
        if ((spaceStackBridge.localFolderRemoved)||(spaceStackBridge.localFolderEmpty)||(spaceStackBridge.isUpdateRequired)){
            return false
        }else{
            return true
        }
    }


}
