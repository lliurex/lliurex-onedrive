import org.kde.plasma.core 2.0 as PlasmaCore
import org.kde.kirigami 2.6 as Kirigami
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
                closing=true,
                timer.stop(),           
                mainWindow.close();
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

            SyncWaiting{
                id:syncWaiting
            }

            SpacesOptions{
                id:spacesOptions
            }
            AccountOptions{
                id:accountOptions
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

}

