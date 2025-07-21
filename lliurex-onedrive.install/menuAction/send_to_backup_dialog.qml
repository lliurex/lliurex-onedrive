import org.kde.plasma.core 2.0 as PlasmaCore
import QtQuick 2.6
import QtQuick.Controls 2.6
import QtQuick.Layouts 1.15
import QtQuick.Window 2.2

ApplicationWindow {
	visible: true
	title: "OneDrive-Backup"
	property int margin: 1
	color:"#eff0f1"
	width: 400
	height: mainLayout.implicitHeight + 2 * margin
	minimumWidth: 450
	minimumHeight: mainLayout.Layout.minimumHeight + 2 * margin
	maximumWidth: 450
	maximumHeight: mainLayout.Layout.maximumHeight + 2 * margin
	Component.onCompleted: {
	    x = Screen.width/2 - width/2 
        y = Screen.height/2 - height/2

    }

    onClosing: {
     	if (bridge.closed(true))
     		close.accepted=true;
        else
        	close.accepted=false;	
              
    }

    ColumnLayout {
    	id: mainLayout
    	anchors.fill: parent
    	anchors.margins: margin
    	
    	Layout.minimumWidth:450
    	Layout.maximumWidth:450
    	Layout.minimumHeight:155
    	Layout.maximumHeight:155
    	
	   	GridLayout {
	   		id: grid
	   		Layout.topMargin: 5
	   		Layout.bottomMargin: 0
	   		rows: 5
	   		columns: 2
	   		rowSpacing:10

	   		Rectangle {
	   			color:"transparent"
	   			Layout.rowSpan: 1
	   			Layout.columnSpan: 1
	   			Layout.leftMargin:10
	   			width:60
	   			height:50
	   			Image{
	   				source:getIcon(bridge.dialogMsgCode)
	   				anchors.centerIn:parent
	   			}
	   		}
	   		Rectangle {
	   			color:"transparent"
	   			Layout.rowSpan: 1
	   			Layout.columnSpan: 1
	   			height:50
	   			Layout.fillWidth: true
	   			Layout.leftMargin:10
	   			Text{
	   				id:warningText
	   				text:getMsg(bridge.dialogMsgCode)
	   				font.pointSize: 11
	   				anchors.left: parent.left
	   				anchors.verticalCenter:parent.verticalCenter
	   			}
	   		}
	   		Rectangle {
	   			color:"transparent"
	   			Layout.rowSpan: 1
	   			Layout.columnSpan: 2
	   			Layout.fillWidth: true
	   			height:25
	   			ProgressBar{
	   				id:progressBar
	   				indeterminate:true
	   				visible:bridge.showProgressBar
	   				anchors.centerIn:parent
	   				implicitWidth:250
	   				height:25
	   			}
   			}

   			Rectangle {
	   			color:"transparent"
	   			Layout.rowSpan: 1
	   			Layout.columnSpan: 2
	   			height:15
	   			Layout.fillWidth: true
	   			Layout.leftMargin:10
	   			visible:bridge.showProgressBar
	   			Text{
	   				id:progressText
	   				text:bridge.fileProcessed
	   				font.italic:true 
	   				font.pointSize: 10
	   				anchors.verticalCenter:parent.verticalCenter
	   				width:400
	   				elide:Text.ElideMiddle
	   			}
	   		}

   			
	   		Rectangle {
	   			id:btnBox
	   			color:"transparent"
	   			visible:true
	   			Layout.rowSpan: 1
	   			Layout.columnSpan: 2
	   			Layout.fillWidth: true
	   			Layout.rightMargin:10
	   			Layout.leftMargin:10
	   			height:40
	   			
	   			Button {
		            id:reportBtn
		            visible:bridge.showErrorBtn
		            focus:true
		            anchors.left:parent.left
		            display:AbstractButton.TextBesideIcon
		            icon.name:"document-preview-archive.svg"
		            text:i18nd("lliurex-onedrive","View errors report")
		            Layout.preferredHeight:35
		            onClicked:{
		            	bridge.openErrorsReport()
		            }   			
				}

	   			Button {
		            id:closeBtn
		            visible:!bridge.showProgressBar
		            focus:true
		            anchors.right:parent.right
		            display:AbstractButton.TextBesideIcon
		            icon.name:"dialog-close.svg"
		            text:i18nd("lliurex-onedrive","Close")
		            Layout.preferredHeight:35
		            onClicked:{
		            	bridge.cancelClicked()
		            }   			
				 }
			}
		}
	
	 }

	 function getIcon(code){

	 	switch(code){
	 		case -1:
	 		case -2:
	 		case -3:
	 			return "/usr/share/icons/breeze/status/64/dialog-error.svg"
	 		case 0:
	 			return "/usr/share/icons/breeze/status/64/dialog-information.svg"
	 		case 1:
	 			return "/usr/share/icons/breeze/status/64/dialog-positive.svg"
	 	}
	 }

	function getMsg(code){

	 	switch(code){
	 		case -1:
	 			return i18nd("lliurex-onedrive","No files/folders selected to copy")
	 		case -2:
	 			return i18nd("lliurex-onedrive","Folder to copy files not exist")
	 		case -3:
	 			return i18nd("lliurex-onedrive","Copying has finished with errors.\nErrors detected:")+" "+bridge.errorsDetected
	 		case 0:
	 			return i18nd("lliurex-onedrive","Copying. Wait a moment...")
	 		case 1:
	 			return i18nd("lliurex-onedrive","Copying completed successfully")
	 	}
	}
}  		
