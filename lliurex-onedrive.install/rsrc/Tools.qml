import org.kde.plasma.core 2.0 as PlasmaCore
import org.kde.kirigami 2.6 as Kirigami
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
            visible:onedriveBridge.isOnedriveRunning?true:false
            text:i18nd("lliurex-onedrive","Some options can only be executed if the synchronization is stopped")
            type:Kirigami.MessageType.Information;
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
                text:i18nd("lliurex-onedrive","Run a OneDrive test:")
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
                ToolTip.text:i18nd("lliurex-onedrive","Click to run an OneDrive test command")

                onClicked:{
                    toolsPopup.open()
                    toolsPopup.popupMessage=i18nd("lliurex-onedrive", "Executing test. Wait a moment...")
                    delay(1000, function() {
                        if (onedriveBridge.closePopUp){
                            toolsPopup.close(),
                            timer.stop();
                        }
                    })
                    onedriveBridge.testOnedrive();
                }
            }

            Text{
                id:repairText
                text:i18nd("lliurex-onedrive","Repair OneDrive:")
                Layout.bottomMargin:20
                Layout.alignment: Qt.AlignRight | Qt.AlignVCenter
            }

            Button {
                id:repairBtn
                display:AbstractButton.IconOnly
                icon.name:"kt-start.svg"
                Layout.preferredHeight: 30
                Layout.alignment: Qt.AlignLeft | Qt.AlignVCenter
                Layout.bottomMargin:20
                hoverEnabled:true
                enabled:!onedriveBridge.isOnedriveRunning && !onedriveBridge.localFolderEmpty
                ToolTip.delay: 1000
                ToolTip.timeout: 3000
                ToolTip.visible: hovered
                ToolTip.text:i18nd("lliurex-onedrive","Click to run an OneDrive client repair command")

                onClicked:{
                    if (onedriveBridge.localFolderRemoved){
                        repairRemovedDialog.open()
                    }else{
                        repair()
                    }
                    
                }   
            } 
     
       }
    }

    Dialog {
        id: repairRemovedDialog
        modality:Qt.WindowModal
        title:"Lliurex Onedrive"+" - "+i18nd("lliurex-onedrive","Tools")

        contentItem: Rectangle {
            color: "#ebeced"
            implicitWidth: 550
            implicitHeight: 105
            anchors.topMargin:5
            anchors.leftMargin:5

            Image{
                id:repairRemovedDialogIcon
                source:"/usr/share/icons/breeze/status/64/dialog-warning.svg"

            }
            
            Text {
                id:repairRemovedDialogText
                text:i18nd("lliurex-onedrive","Local OneDrive folder not exists.\nAre you sure you want to repair OneDrive?\nThis action can lead to deletion of files stored on OneDrive")
                font.family: "Quattrocento Sans Bold"
                font.pointSize: 10
                anchors.left:repairRemovedDialogIcon.right
                anchors.verticalCenter:repairRemovedDialogIcon.verticalCenter
                anchors.leftMargin:10
            
            }

            DialogButtonBox {
                buttonLayout:DialogButtonBox.KdeLayout
                anchors.bottom:parent.bottom
                anchors.right:parent.right
                anchors.topMargin:15

                Button {
                    id:repairRemovedDialogApplyBtn
                    display:AbstractButton.TextBesideIcon
                    icon.name:"dialog-ok.svg"
                    text: i18nd("lliurex-onedrive","Accept")
                    font.family: "Quattrocento Sans Bold"
                    font.pointSize: 10
                    DialogButtonBox.buttonRole: DialogButtonBox.ApplyRole
                }
                Button {
                    id:repairRemovedDialogCancelBtn
                    display:AbstractButton.TextBesideIcon
                    icon.name:"dialog-cancel.svg"
                    text: i18nd("lliurex-onedrive","Cancel")
                    font.family: "Quattrocento Sans Bold"
                    font.pointSize: 10
                    DialogButtonBox.buttonRole:DialogButtonBox.RejectRole
                }

                onApplied:{
                    repairRemovedDialog.close()
                    repair()
                
                }
                onRejected:{
                    repairRemovedDialog.close()

                }

            }
        }
     }
    
    CustomPopup{
        id:toolsPopup
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

    function repair(){
        toolsPopup.open()
        toolsPopup.popupMessage=i18nd("lliurex-onedrive", "Executing repair command. Wait a moment...")
        delay(1000, function() {
            if (onedriveBridge.closePopUp){
                toolsPopup.close(),
                timer.stop();
            }
        })
        onedriveBridge.repairOnedrive();
    }

}

