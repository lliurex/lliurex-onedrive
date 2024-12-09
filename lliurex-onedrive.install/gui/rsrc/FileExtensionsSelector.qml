import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import org.kde.plasma.components as PC3



Rectangle{
    width:110
    height:85
    border.color: "#d3d3d3"
    property alias selectorEnabled:extensionsSelector.enabled

    PC3.ScrollView{
        implicitWidth:parent.width
        implicitHeight:parent.height
        anchors.leftMargin:10

        ListView{
            id:extensionsSelector
            anchors.fill:parent
            anchors.bottomMargin:10
            enabled:selectorEnabled
            clip: true
            focus:true
                  
            model:syncStackBridge.fileExtensionsModel
               
            delegate:Item{
                width:40
                height:40
                  
                Row{
                    spacing:5
                    anchors.fill:parent
                    anchors.margins:15
                    
                    CheckBox{
                        id:checkBoxId
                        anchors.leftMargin:10
                        checked:isChecked
                        onToggled:{
                            syncStackBridge.getFileExtensionChecked([name,checked])
                        }
                    }

                    Label{
                        text:name
                    }
                }
           }
                
        Layout.alignment:Qt.AlignLeft
        Layout.bottomMargin:10

        }
    }
}
