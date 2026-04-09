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
    property alias btnDiscardVisible:dialogDiscardBtn.visible
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
    padding:20
    anchors.centerIn:Overlay.overlay
    background:Rectangle{
        color:"#ebeced"
        border.color:"#b8b9ba"
        border.width:1
        radius:5.0
    }
    
    contentItem: ColumnLayout {
        id:container
        width: dialogWidth
        height: dialogHeight
        spacing:20

        RowLayout {
            Layout.alignment: Qt.AlignTop
            spacing: 20
        

            Image{
                id:dialogIcon
                source:dialogIcon
                Layout.alignment: Qt.AlignTop 
            }
                
            Text {
                id:dialogText
                text:dialogMsg
                font.family: "Quattrocento Sans Bold"
                font.pointSize: 10
                Layout.preferredWidth:550
                Layout.alignment: Qt.AlignTop 
                wrapMode:Text.WordWrap
                
            }
        }
        RowLayout {
            id:bntBox
            Layout.alignment:Qt.AlignRight
            /*anchors.right:parent.right
            anchors.topMargin:5
            anchors.rightMargin:10*/
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
                visible:btnDiscardVisible
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
