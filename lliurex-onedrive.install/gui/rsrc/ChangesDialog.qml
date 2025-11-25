import QtQuick      
import QtQuick.Controls
import QtQuick.Layouts
import org.kde.plasma.components as PC

Popup {
    id: customDialog
    property alias dialogIcon:dialogIcon.source
    property alias dialogVisible:customDialog.visible
    property alias dialogMsg:dialogText.text
    property alias dialogWidth:container.implicitWidth
    property alias dialogHeight:container.implicitHeight
    property alias btnAcceptVisible:dialogApplyBtn.visible
    property alias btnAcceptText:dialogApplyBtn.text
    property alias btnDiscardText:dialogDiscardBtn.text
    property alias btnDiscardIcon:dialogDiscardBtn.icon.name
    property alias btnCancelText:dialogCancelBtn.text
    property alias btnCancelIcon:dialogCancelBtn.icon.name
    signal dialogApplyClicked
    signal discardDialogClicked
    signal rejectDialogClicked

    visible:dialogVisible
    modal:true
    focus:true
    closePolicy:Popup.NoAutoClose
    anchors.centerIn:Overlay.overlay
    background:Rectangle{
        color:"#ebeced"
        border.color:"#b8b9ba"
        border.width:1
        radius:5.0
    }
    
    contentItem: Rectangle {
        id:container
        color: "transparent"
        width: dialogWidth
        height: dialogHeight
        anchors.topMargin:10
        Image{
            id:dialogIcon
            source:dialogIcon
        }
        
        Text {
            id:dialogText
            text:dialogMsg
            font.family: "Quattrocento Sans Bold"
            font.pointSize: 10
            anchors.left:dialogIcon.right
            anchors.verticalCenter:dialogIcon.verticalCenter
            anchors.leftMargin:10
            width:600
            wrapMode:Text.WordWrap
        
        }
      
        RowLayout {
            id:bntBox
            anchors.bottom:parent.bottom
            anchors.right:parent.right
            anchors.topMargin:5
            anchors.bottomMargin:5
            anchors.rightMargin:10
            spacing:10

            PC.Button {
                id:dialogApplyBtn
                display:AbstractButton.TextBesideIcon
                icon.name:"dialog-ok.svg"
                text: btnAcceptText
                focus:true
                visible:btnAcceptVisible
                font.family: "Quattrocento Sans Bold"
                font.pointSize: 10
                onClicked:{
                    dialogApplyClicked()
                }
            }

            Button {
                id:dialogDiscardBtn
                display:AbstractButton.TextBesideIcon
                icon.name:btnDiscardIcon
                text: btnDiscardText
                focus:true
                font.family: "Quattrocento Sans Bold"
                font.pointSize: 10
                onClicked:{
                    discardDialogClicked()
                }


            }

            PC.Button {
                id:dialogCancelBtn
                display:AbstractButton.TextBesideIcon
                icon.name:btnCancelIcon
                text: btnCancelText
                focus:true
                font.family: "Quattrocento Sans Bold"
                font.pointSize: 10
                onClicked:{
                    rejectDialogClicked()
                }
        
            }
        }
    }
 }
