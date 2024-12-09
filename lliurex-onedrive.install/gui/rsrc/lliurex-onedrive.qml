import org.kde.plasma.core 2.0 as PlasmaCore
import org.kde.kirigami 2.12 as Kirigami
import QtQuick 2.6
import QtQuick.Controls 2.6
import QtQuick.Layouts 1.12
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
    Component.onCompleted: {
        x = Screen.width / 2 - width / 2
        y = Screen.height / 2 - height/0.4
    }

    onClosing: {
        close.accepted=closing;
        mainStackBridge.closeOnedrive()
        delay(100, function() {
            if (mainStackBridge.closeGui){
                closing=true,
                closeTimer.stop(),           
                mainWindow.close();
            }
        })
    }

    ColumnLayout {
        id: mainLayout
        anchors.fill: parent
        anchors.margins: margin
        Layout.minimumWidth:820
        Layout.minimumHeight:635

        RowLayout {
            id: bannerBox
            Layout.alignment:Qt.AlignTop

            Rectangle{
                color: "#000000"
                Layout.minimumWidth:mainLayout.width
                Layout.preferredWidth:mainLayout.width
                Layout.fillWidth:true
                Layout.minimumHeight:120
                Layout.maximumHeight:120
                Image{
                    id:banner
                    source: "/usr/share/lliurex-onedrive/rsrc/lliurex-onedrive.png"
                    asynchronous:true
                    anchors.centerIn:parent
                }
            }
        }

        StackView {
            id: mainView
            property int currentIndex:mainStackBridge.currentStack
            Layout.minimumWidth: 725
            Layout.preferredWidth: 725
            Layout.alignment:Qt.AlignHCenter
            Layout.leftMargin:0
            Layout.fillWidth:true
            Layout.fillHeight: true
            initialItem:syncView
            onCurrentIndexChanged:{
                switch (currentIndex){
                    case 0:
                        mainView.replace(syncView)
                        break;
                    case 1:
                        mainView.replace(spaceView)
                        break;
                    case 2:
                        mainView.replace(accountView)
                        break;
                }
            }
            replaceEnter: Transition {
                PropertyAnimation {
                    property: "opacity"
                    from: 0
                    to:1
                    duration: 600
                }
            }
            replaceExit: Transition {
                PropertyAnimation {
                    property: "opacity"
                    from: 1
                    to:0
                    duration: 600
                }
            }

            Component{
                id:syncView
                SyncWaiting{
                    id:syncWaiting
                }
            }
            Component{
                id:spaceView
                SpacesOptions{
                    id:spacesOptions
                }
            }
            Component{
                id:accountView
                AccountOptions{
                    id:accountOptions
                }
            }
        }

    }

    Timer{
        id:closeTimer
    }

    function delay(delayTime,cb){
        closeTimer.interval=delayTime;
        closeTimer.repeat=true;
        closeTimer.triggered.connect(cb);
        closeTimer.start()
    }

}

