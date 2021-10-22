import QtQuick 2.6
import QtQuick.Controls 2.6
import QtQuick.Layouts 1.15
import QtQuick.Dialogs 1.3


Rectangle{
    width: 700
    height: 615
    visible: true

    GridLayout{
        id: loadGrid
        rows: 4
        flow: GridLayout.TopToBottom
        anchors.centerIn:parent

        RowLayout{
            Layout.fillWidth: true
            Layout.alignment:Qt.AlignHCenter

            Rectangle{
                color:"transparent"
                width:30
                height:30
                
                AnimatedImage{
                    source: "/usr/share/lliurex-onedrive/rsrc/loading.gif"
                    transform: Scale {xScale:0.15;yScale:0.15}
                }
            }
        }

        RowLayout{
            Layout.fillWidth: true
            Layout.alignment:Qt.AlignHCenter

            Text{
                id:loadtext
                text:i18nd("lliurex-onedrive", "Loading. Wait a moment...")
                font.family: "Quattrocento Sans Bold"
                font.pointSize: 10
                Layout.alignment:Qt.AlignHCenter
            }
        }
    }
    Dialog{
        id: downloadDialog
        visible:onedriveBridge.showDownloadDialog
        title:"Lliurex Onedrive"+" - "+i18nd("lliurex-onedrive","Synchronization options")
        modality:Qt.WindowModal

        contentItem: Rectangle {
            color: "#ebeced"
            implicitWidth: 700
            implicitHeight: 105
            anchors.topMargin:5
            anchors.leftMargin:5

            Image{
                id:dialogIcon
                source:"/usr/share/icons/breeze/status/64/dialog-warning.svg"

            }
            
            Text {
                id:dialogText
                text:i18nd("lliurex-onedrive","Its content in OneDrive is approximately ")+onedriveBridge.initialDownload+i18nd("lliurex-onedrive","\nThe space available on the computer is ")+onedriveBridge.hddFreeSpace+
                i18nd("lliurex-onedrive","\nDo you want to sync all the content or do you prefer to select the content to sync?")
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


}