import QtQuick 2.6
import QtWebEngine 1.10
import QtQuick.Controls 2.6
import QtQuick.Layouts 1.12
import QtQuick.Dialogs 1.3


Rectangle {
    width: 725
    height: 615
    visible: true
    WebEngineView {
        id:webEngine
        anchors.fill:parent
        url: "https://login.microsoftonline.com/common/oauth2/v2.0/authorize?client_id=d50ca740-c83f-4d1b-b616-12c519384f0c&scope=Files.ReadWrite%20Files.ReadWrite.all%20Sites.Read.All%20Sites.ReadWrite.All%20offline_access&response_type=code&redirect_uri=https://login.microsoftonline.com/common/oauth2/nativeclient"
        profile.persistentCookiesPolicy:WebEngineProfile.NoPersistentCookies
        onLoadingChanged:{
            var ret=loadRequest.url.toString()
            if (ret.indexOf("nativeclient?code=")===48){
                onedriveBridge.createAccount(ret);

            }
        }
        
    }

    function closeConnection(){
        webEngine.action(webEngine.Stop)

    }
    Dialog{
        id: previousDialog
        visible:onedriveBridge.showPreviousDialog
        title:"Lliurex Onedrive"+" - "+i18nd("lliurex-onedrive","Account")
        modality:Qt.WindowModal

        contentItem: Rectangle {
            color: "#ebeced"
            implicitWidth: 700
            implicitHeight: 105
            anchors.topMargin:5
            anchors.leftMargin:5

            Image{
                id:previousDialogIcon
                source:"/usr/share/icons/breeze/status/64/dialog-warning.svg"

            }
            
            Text {
                id:previousDialogText
                text:i18nd("lliurex-onedrive","A local OneDrive folder containing content has been detected on this computer.\nIf you link this computer with OneDrive, the existing content in that folder will be added to OneDrive.\nDo you want to continue with the pairing process?")
                font.family: "Quattrocento Sans Bold"
                font.pointSize: 10
                anchors.left:previousDialogIcon.right
                anchors.verticalCenter:previousDialogIcon.verticalCenter
                anchors.leftMargin:10
            
            }
          

            DialogButtonBox {
                buttonLayout:DialogButtonBox.KdeLayout
                anchors.bottom:parent.bottom
                anchors.right:parent.right
                anchors.topMargin:15

                Button {
                    id:previousDialogApplyBtn
                    display:AbstractButton.TextBesideIcon
                    icon.name:"dialog-ok.svg"
                    text: i18nd("lliurex-onedrive","Accept")
                    font.family: "Quattrocento Sans Bold"
                    font.pointSize: 10
                    DialogButtonBox.buttonRole: DialogButtonBox.ApplyRole
                }

                Button {
                    id:previousDialogCancelBtn
                    display:AbstractButton.TextBesideIcon
                    icon.name:"dialog-cancel.svg"
                    text: i18nd("lliurex-onedrive","Cancel")
                    font.family: "Quattrocento Sans Bold"
                    font.pointSize: 10
                    DialogButtonBox.buttonRole:DialogButtonBox.RejectRole
                }

                onApplied:{
                    previousDialog.close()                  
            
                }

                onRejected:{
                    previousDialog.close()
                    onedriveBridge.cancelCreateAccount()

                }
            }
        }
  }

}
