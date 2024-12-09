import org.kde.plasma.core as PlasmaCore
import org.kde.kirigami as Kirigami
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts


Rectangle{
    color:"transparent"

    Text{ 
        text:i18nd("lliurex-onedrive","Migration information")
        font.family: "Quattrocento Sans Bold"
        font.pointSize: 16
    }
           
    Row{
        id:textRow
        anchors.top: parent.top
        anchors.left:parent.left
        anchors.topMargin:40
        anchors.rightMargin:10      

        Text{
            id:informationText
            text:i18nd("lliurex-onedrive","In order to continue using LliureX-OneDrive it is necessary to migrate the current configurarion.\nBefore starting the process it is recommended to consult the help.\nDuring the migration process the synchronization will be stopped.Once finished,you can start the synchronization again.\nTo start the migration clik Continue")
            horizontalAlignment:Text.AlignJustify
            width:640
            wrapMode:Text.WordWrap
            font.family: "Quattrocento Sans Bold"
            font.pointSize: 10

       }
    }
    Row{
       id:btnBox
       anchors.bottom: parent.bottom
       anchors.right:parent.right
       anchors.bottomMargin:15
       anchors.rightMargin:10
       spacing:10

       Button {
            id:continueBtn
            visible:true
            focus:true
            display:AbstractButton.TextBesideIcon
            icon.name:"dialog-ok.svg"
            text:i18nd("lliurex-onedrive","Continue")
            Keys.onReturnPressed: applyBtn.clicked()
            Keys.onEnterPressed: applyBtn.clicked()
            onClicked:{
                spaceStackBridge.moveToSpaceOption(1)
            }
       }
    } 
}



