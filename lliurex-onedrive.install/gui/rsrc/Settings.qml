
import org.kde.plasma.core 2.0 as PlasmaCore
import org.kde.kirigami 2.12 as Kirigami
import QtQuick 2.6
import QtQuick.Controls 2.6
import QtQuick.Layouts 1.12
import QtQuick.Dialogs 1.3


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
        Layout.fillWidth: true
        anchors.horizontalCenter:parent.horizontalCenter

        Kirigami.InlineMessage {
            id: settingsMessageLabel
            visible:onedriveBridge.showSettingsMessage[0]
            text:getMessageText()
            type: {
                if (onedriveBridge.showSettingsMessage[1]==""){
                    Kirigami.MessageType.Positive;
                }else{
                    Kirigami.MessageType.Error;
                }
            }
            Layout.minimumWidth:640
            Layout.maximumWidth:640
            Layout.topMargin: 40
        }

        GridLayout{
            id: settingsGrid
            columns: 2
            flow: GridLayout.LeftToRight
            columnSpacing:10
            Layout.topMargin: settingsMessageLabel.visible?0:50
            Layout.alignment:Qt.AlignHCenter

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
                checked:onedriveBridge.autoStartEnabled
                enabled:getEnabledStatus()
                font.family: "Quattrocento Sans Bold"
                font.pointSize: 10
                focusPolicy: Qt.NoFocus
                onToggled:onedriveBridge.manageAutoStart(autoStartValue.checked);
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
                from:1
                to:60
                stepSize:1
                value:onedriveBridge.monitorInterval
                Layout.alignment:Qt.AlignLeft
                Layout.bottomMargin:10
                enabled:getEnabledStatus()
                onValueModified:{
                    onedriveBridge.getMonitorInterval(value)
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
                currentIndex:onedriveBridge.rateLimit
                model:onedriveBridge.bandWidthNames
                Layout.alignment:Qt.AlignLeft
                Layout.bottomMargin:10
                Layout.preferredWidth:100
                enabled:getEnabledStatus()
                onActivated:{
                    onedriveBridge.getRateLimit(bandwidthValues.currentIndex)
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
                    checked:onedriveBridge.skipSize[0]
                    enabled:getEnabledStatus()
                    Layout.bottomMargin:10
                    Layout.rightMargin:5
                    Layout.alignment:Qt.AlignLeft
                    onToggled:onedriveBridge.getSkipSize([skipSizeCB.checked,skipSizeValues.currentIndex])

                }
                ComboBox{
                    id:skipSizeValues
                    currentIndex:onedriveBridge.skipSize[1]
                    model:onedriveBridge.maxFileSizeNames
                    enabled:skipSizeCB.checked
                    Layout.alignment:Qt.AlignVCenter
                    Layout.bottomMargin:10
                    Layout.preferredWidth:100
                    onActivated:{
                        onedriveBridge.getSkipSize([skipSizeCB.checked,skipSizeValues.currentIndex])
                    }
                }
            }
            Text{
                id:managementLog
                text:i18nd("lliurex-onedrive","Log management:")
                Layout.alignment: Qt.AlignRight

            }

            CheckBox {
                id:enableLogCB
                text:i18nd("lliurex-onedrive","Activate log")
                checked:onedriveBridge.logEnabled
                enabled:true
                font.family: "Quattrocento Sans Bold"
                font.pointSize: 10
                focusPolicy: Qt.NoFocus
                onToggled:onedriveBridge.getLogEnabled(enableLogCB.checked)
            }
            Text{

            }    
            Row{
                id:logRow
                spacing:10

                Text{
                   id:sizeLog
                   text:i18nd("lliurex-onedrive","Current log file size:")
                   anchors.verticalCenter:manageLogBtn.verticalCenter
                }
                Text{
                    id:sizeLogValue
                    text:onedriveBridge.logSize
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
                        if (onedriveBridge.logSize!=""){
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
                        x: manageLogBtn.width/2
                        rightMargin:4*manageLogBtn.width
                        MenuItem{
                            icon.name:"document-preview-archive.svg"
                            text:i18nd("lliurex-onedrive","View log file")
                            onClicked:{
                                onedriveBridge.openSpaceLogFile()
                            }
                        }
                        MenuItem{
                            icon.name:"delete.svg"
                            text:i18nd("lliurex-onedrive","Delete log file")
                            onClicked:{
                                onedriveBridge.removeLogFile()
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
            enabled:onedriveBridge.settingsChanged
            display:AbstractButton.TextBesideIcon
            icon.name:"dialog-ok.svg"
            text:i18nd("lliurex-onedrive","Apply")
            Layout.preferredHeight: 40

            onClicked:{
               onedriveBridge.applySettingsChanges()
            }
        }
        Button {
            id:cancelBtn
            visible:true
            enabled:onedriveBridge.settingsChanged
            display:AbstractButton.TextBesideIcon
            icon.name:"dialog-cancel.svg"
            text:i18nd("lliurex-onedrive","Cancel")
            Layout.preferredHeight: 40

            onClicked:{
               onedriveBridge.cancelSettingsChanges()
            }
        }
    

    }

    CustomPopup{
        id:settingsPopup
    }

    ChangesDialog{
        id:settingsChangesDialog
        dialogIcon:"/usr/share/icons/breeze/status/64/dialog-warning.svg"
        dialogTitle:"Lliurex Onedrive"+" - "+i18nd("lliurex-onedrive","Settings")
        dialogVisible:onedriveBridge.showSettingsDialog
        dialogMsg:i18nd("lliurex-onedrive","The settings of space have changed.\nDo you want apply the changes or discard them?")
        dialogWidth:400
        btnAcceptVisible:true
        btnAcceptText:i18nd("lliurex-onedrive","Apply")
        btnDiscardText:i18nd("lliurex-onedrive","Discard")
        btnDiscardIcon:"delete.svg"
        btnCancelText:i18nd("lliurex-onedrive","Cancel")
        btnCancelIcon:"dialog-cancel.svg"
        Connections{
            target:settingsChangesDialog
            function onDialogApplyClicked(){
                onedriveBridge.manageSettingsDialog("Accept")
            }
            function onDiscardDialogClicked(){
                onedriveBridge.manageSettingsDialog("Discard")           
            }
            function onRejectDialogClicked(){
                onedriveBridge.manageSettingsDialog("Cancel")       
            }

        }
    }
  
    function getMessageText(){

        switch (onedriveBridge.showSettingsMessage[1]){
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
        if ((onedriveBridge.localFolderRemoved)||(onedriveBridge.localFolderEmpty)){
            return false
        }else{
            return true
        }
    }


}
