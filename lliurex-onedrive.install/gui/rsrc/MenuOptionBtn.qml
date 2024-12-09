import QtQuick
import QtQuick.Controls
import QtQuick.Layouts


Item {
	id:menuItem
	Layout.preferredWidth: 120
	Layout.preferredHeight: 35

	property alias optionIcon:menuOptionIcon.source
	property alias optionText:menuOptionText.text
  property alias optionFontSize:menuOptionText.font.pointSize

	signal menuOptionClicked()

	Rectangle{
		id:menuOption
		width:130
		height:35
		color:"transparent"
		border.color:"transparent"

		Row{
			spacing:5
			anchors.verticalCenter:menuOption.verticalCenter
			leftPadding:5
            
            Image{
              id:menuOptionIcon
              source:optionIcon
            }

            Text {
              id:menuOptionText
              text:optionText
              anchors.verticalCenter:menuOptionIcon.verticalCenter
              font.pointSize:optionFontSize


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


