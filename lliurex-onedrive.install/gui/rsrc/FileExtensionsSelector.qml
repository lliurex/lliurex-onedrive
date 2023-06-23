import QtQuick 2.6
import QtQuick.Controls 2.6
import QtQuick.Layouts 1.12
import org.kde.plasma.components 3.0 as PC3



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
                  
            model:onedriveBridge.fileExtensionsModel
               
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
                            onedriveBridge.getFileExtensionChecked([name,checked])
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
