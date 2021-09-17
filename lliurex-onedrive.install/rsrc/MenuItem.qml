import QtQuick 2.6
import QtQuick.Controls 2.6
import QtQuick.Layouts 1.3
import QtQuick.Window 2.2

Item {
	id:menuItem
	property alias optionIcon:menuOptionIcon.source
	property alias optionText:menuOptionText.text
	signal menuOptionClicked()

	Rectangle{
		id:menuOption
		width:150
		height:35
		color:"transparent"
		border.color:"transparent"

		Row{
			spacing:5
			anchors.verticalCenter:menuItem.verticalCenter
			leftPadding:5
            
            Image{
              id:menuOptionIcon
              source:optionIcon
            }

            Text {
              id:menuOptionText
              text:optionText
              anchors.verticalCenter:menuOptionIcon.verticalCenter


            }  
        }

        MouseArea {
        	id: mouseAreaOption
          	anchors.fill: parent
            hoverEnabled:true

            onEntered: {
              menuOption.color="#add8e6"
            }
            onExited: {
              menuOption.color="transparent"
            }
            onClicked: {
            	menuOptionClicked()
            }
       }   
   }
}


