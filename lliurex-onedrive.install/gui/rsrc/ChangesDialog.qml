import QtQuick 2.6      
import QtQuick.Controls 2.6
import QtQuick.Layouts 1.12
import QtQuick.Dialogs 1.3


Dialog {
    id: customDialog
    property alias dialogIcon:dialogIcon.source
    property alias dialogTitle:customDialog.title
    property alias dialogVisible:customDialog.visible
    property alias dialogMsg:dialogText.text
    property alias dialogWidth:container.implicitWidth
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
    title:dialogTitle
    modality:Qt.WindowModal

    contentItem: Rectangle {
        id:container
        color: "#ebeced"
        implicitWidth: dialogWidth
        implicitHeight: 120
        anchors.topMargin:5
        anchors.leftMargin:5

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
                text: btnAcceptText
                focus:true
                visible:btnAcceptVisible
                font.family: "Quattrocento Sans Bold"
                font.pointSize: 10
                DialogButtonBox.buttonRole: DialogButtonBox.ApplyRole
                Keys.onReturnPressed: dialogApplyBtn.clicked()
                Keys.onEnterPressed: dialogApplyBtn.clicked()

            }

            Button {
                id:dialogDiscardBtn
                display:AbstractButton.TextBesideIcon
                icon.name:btnDiscardIcon
                text: btnDiscardText
                focus:true
                font.family: "Quattrocento Sans Bold"
                font.pointSize: 10
                DialogButtonBox.buttonRole: DialogButtonBox.DestructiveRole
                Keys.onReturnPressed: dialogDiscardBtn.clicked()
                Keys.onEnterPressed: dialogDiscardBtn.clicked()


            }

            Button {
                id:dialogCancelBtn
                display:AbstractButton.TextBesideIcon
                icon.name:btnCancelIcon
                text: btnCancelText
                focus:true
                font.family: "Quattrocento Sans Bold"
                font.pointSize: 10
                DialogButtonBox.buttonRole:DialogButtonBox.RejectRole
                Keys.onReturnPressed: dialogCancelBtn.clicked()
                Keys.onEnterPressed: dialogCancelBtn.clicked()
        
            }

            onApplied:{
                dialogApplyClicked()
            }

            onDiscarded:{
                discardDialogClicked()
            }

            onRejected:{
                rejectDialogClicked()
            }
        }
    }
 }
