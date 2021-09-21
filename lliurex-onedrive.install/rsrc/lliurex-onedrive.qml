import org.kde.plasma.core 2.0 as PlasmaCore
import org.kde.kirigami 2.6 as Kirigami
import QtQuick 2.6
import QtQuick.Controls 2.6
import QtQuick.Layouts 1.15
import QtQuick.Window 2.2
import QtQuick.Dialogs 1.3



ApplicationWindow {

    property bool closing: false
    id:mainWindow
    visible: true
    title: "Lliurex OneDrive"
    property int margin: 1
    width: mainLayout.implicitWidth + 2 * margin
    height: mainLayout.implicitHeight + 2 * margin
    minimumWidth: mainLayout.Layout.minimumWidth + 2 * margin
    minimumHeight: mainLayout.Layout.minimumHeight + 2 * margin
    maximumWidth: mainLayout.Layout.maximumWidth + 2 * margin
    maximumHeight: mainLayout.Layout.maximumHeight + 2 * margin
    Component.onCompleted: {
        x = Screen.width / 2 - width / 2
        y = Screen.height / 2 - height / 2
    }

    onClosing: {
        close.accepted=closing;
        onedriveBridge.closeOnedrive()
        delay(100, function() {
            if (onedriveBridge.closeGui){
                removeConnection(),
                closing=true,
                timer.stop(),           
                mainWindow.close();

            }else{
                if (!onedriveBridge.showSettingsDialog){
                  timer.stop()
                }
                closing=false;
            }
        })
        
    }

    ColumnLayout {
        id: mainLayout
        anchors.fill: parent
        anchors.margins: margin
        Layout.minimumWidth:800
        Layout.maximumWidth:800
        Layout.minimumHeight:635
        Layout.maximumHeight:635

        RowLayout {
            id: bannerBox
            Layout.alignment:Qt.AlignTop
            Layout.minimumHeight:120
            Layout.maximumHeight:120

            Image{
                id:banner
                source: "/usr/share/lliurex-onedrive/rsrc/lliurex-onedrive.png"
            }
        }

        StackLayout {
            id: stackLayout
            currentIndex:onedriveBridge.currentStack
            implicitWidth: 725
            Layout.alignment:Qt.AlignHCenter
            Layout.leftMargin:0
            Layout.fillWidth:true
            Layout.fillHeight: true

            OnedriveAuth{
                id:onedriveAuth
            }

            SyncWaiting{
                id:syncWaiting
            }

            AccountOptions{
                id:accountOptions
            }

            CloseApp{
                id:closeApp
            }
        }

        Dialog {
            id: customDialog
            visible:onedriveBridge.showSettingsDialog
            title:"Lliurex Onedrive"+" - "+i18nd("lliurex-onedrive","Settings")
            modality:Qt.WindowModal

            contentItem: Rectangle {
                color: "#ebeced"
                implicitWidth: 400
                implicitHeight: 105
                anchors.topMargin:5
                anchors.leftMargin:5


                Image{
                    id:dialogIcon
                    source:"/usr/share/icons/breeze/status/64/dialog-warning.svg"

                }
                
                Text {
                    id:dialogText
                    text:i18nd("lliurex-onedrive","The settings of OneDrive have changed.\nDo you want apply the changes or discard them?")
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
                        text: i18nd("lliurex-onedrive","Apply")
                        font.family: "Quattrocento Sans Bold"
                        font.pointSize: 10
                        DialogButtonBox.buttonRole: DialogButtonBox.ApplyRole
                    }

                    Button {
                        id:dialogDiscardBtn
                        display:AbstractButton.TextBesideIcon
                        icon.name:"delete.svg"
                        text: i18nd("lliurex-onedrive","Discard")
                        font.family: "Quattrocento Sans Bold"
                        font.pointSize: 10
                        DialogButtonBox.buttonRole: DialogButtonBox.DestructiveRole

                    }

                    Button {
                        id:dialogCancelBtn
                        display:AbstractButton.TextBesideIcon
                        icon.name:"dialog-cancel.svg"
                        text: i18nd("lliurex-onedrive","Cancel")
                        font.family: "Quattrocento Sans Bold"
                        font.pointSize: 10
                        DialogButtonBox.buttonRole:DialogButtonBox.RejectRole
                    }

                    onApplied:{
                        onedriveBridge.manageSettingsDialog("Accept")
                    
                    }

                    onDiscarded:{
                        onedriveBridge.manageSettingsDialog("Discard")

                    }

                    onRejected:{
                        onedriveBridge.manageSettingsDialog("Cancel")

                    }
                }
            }
         }

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

    function removeConnection(){
        onedriveAuth.closeConnection()

    }

}

