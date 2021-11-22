
import org.kde.plasma.core 2.0 as PlasmaCore
import org.kde.kirigami 2.6 as Kirigami
import QtQuick 2.6
import QtQuick.Controls 2.6
import QtQuick.Layouts 1.12


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
            Layout.minimumWidth:650
            Layout.maximumWidth:650
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
                onActivated:{
                    onedriveBridge.getRateLimit(bandwidthValues.currentIndex)
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
                settingsPopup.open()
                delay(1, function() {
                    if (onedriveBridge.closePopUp){
                        settingsPopup.close(),
                        timer.stop();
                    }
                })
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
        popupMessage:i18nd("lliurex-onedrive", "Saving changes. Wait a moment...")
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

}
