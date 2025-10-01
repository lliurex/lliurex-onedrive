import org.kde.plasma.core as PlasmaCore
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Window

ApplicationWindow {
	visible: true
	title: "OneDrive-Backup"
	property int margin: 1
	color:"#eff0f1"
	width: 400
	height: 195
	minimumWidth: 600
	minimumHeight: mainLayout.Layout.minimumHeight + 2 * margin
	maximumWidth: 600
	maximumHeight: mainLayout.Layout.maximumHeight + 2 * margin
	Component.onCompleted: {
	    x = Screen.width/2 - width/2 
        y = Screen.height/2 - height/2

    }

    onClosing:(close)=> {
     	if (bridge.closed(true))
     		close.accepted=true;
        else
        	close.accepted=false;	
              
    }

    ColumnLayout {
    	id: mainLayout
    	anchors.fill: parent
    	anchors.margins: margin
    	
    	Layout.minimumWidth:600
    	Layout.maximumWidth:600
    	Layout.minimumHeight:!bridge.showProgressBar?200:195
    	Layout.maximumHeight:!bridge.showProgressBar?200:195
    	
	   	GridLayout {
	   		id: grid
	   		Layout.topMargin: 5
	   		Layout.bottomMargin: 0
	   		rows: 6
	   		columns: 2
	   		rowSpacing:20


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
	   			height:70
	   			width:550
	   			Layout.fillWidth: true
	   			Layout.leftMargin:10
	   			Text{
	   				id:warningText
	   				text:getMsg(bridge.dialogMsgCode)
	   				font.pointSize: 11
	   				anchors.left: parent.left
	   				/*anchors.verticalCenter:parent.verticalCenter*/
	   				width:500
	   				wrapMode:Text.WordWrap
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
	   				implicitWidth:300
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
	   				width:520
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
	   			Layout.topMargin:20
	   			Layout.fillHeight:true
	   			
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
	 		case -4:
	 			return "/usr/share/icons/breeze/status/64/dialog-error.svg"
	 		case 0:
	 		case 1:
	 			return "/usr/share/icons/breeze/status/64/dialog-information.svg"
	 		case 2:
	 			return "/usr/share/icons/breeze/status/64/dialog-positive.svg"
	 	}
	 }

	function getMsg(code){

	 	var info=i18nd("lliurex-onedrive","These files will be send to your OneDrive account as soon as posible. Once sent, the will be deleted from your local folder.\nPlease verifiy that the transfer is successful by accessing the LLIUREX_ONEDRIVE_BACKUP folder in your OneDrive account")

	 	switch(code){
	 		case -1:
	 			return i18nd("lliurex-onedrive","No files/folders selected to copy")
	 		case -2:
	 			return i18nd("lliurex-onedrive","Folder to copy files not exist")
	 		case -3:
	 			var msg=i18nd("lliurex-onedrive","Copying to local folder has finished with errors.\nErrors detected:")+" "+bridge.errorsDetected
	 			
	 			if (bridge.totalFilesToCopy-bridge.errorsDetected>0){
	 				return msg+"\n"+info
	 			}else{
	 				return msg
	 			}
	 		case -4:
		 		return i18nd("lliurex-onedrive","Invalid arguments")
 			case 0:
	 			return i18nd("lliurex-onedrive","Checking. Wait a moment...")
	 		case 1:
	 			return i18nd("lliurex-onedrive","Copying. Wait a moment...")
	 		case 2:
	 			return i18nd("lliurex-onedrive","Copying to local folder completed successfully")+"\n"+info
	 	}
	}
}  		
