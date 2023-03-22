import QtQuick 2.6
import QtQuick.Controls 2.6
import QtQml.Models 2.6
import org.kde.plasma.components 3.0 as Components


Rectangle {
    property alias structModel:listFolder.model
    property alias listCount:listFolder.count
    property alias structEnabled:listFolder.enabled

    id:folderTable
    visible: onedriveBridge.showFolderStruct
    width: 650; height: 240

    ListModel{
        id: folderModel
    }
    PlasmaExtras.ScrollArea{
        implicitWidth:parent.width
        implicitHeight:folderTable.height
        anchors.leftMargin:10
    
        ListView{
            id: listFolder
            anchors.fill:parent
            height: parent.height
            model:onedriveBridge.model
            enabled:structEnabled
            delegate: listdelegate
            clip: true
            boundsBehavior: Flickable.StopAtBounds
         }         
    }
    Component{
        id: listdelegate
        Rectangle{
            id: menuItem
            width: 660
            height:visible?30:0
            visible:{
                if ((type === "parent")||(type==="file")){
                    true
                }else{
                    if ((subtype==="parent")&&(!hide)){
                        true
                    }else{
                       false
                    }
                }

            }
            color:"white"

            states: State {
                name: "expanded"
                when: isExpanded
                PropertyChanges {
                    target: menuItem
                    visible: true
                }
            }

            transitions:[
                Transition {
                    from: ""
                    to: "expanded"
                    reversible: true
                    SequentialAnimation {
                        PropertyAnimation { property: "visible"; duration: 5 }
                    }
                }
            ]

            Image{
                id:menuOptionIcon
                source:{
                    if (isExpanded){
                        "/usr/share/icons/breeze/actions/22/go-down.svg"
                    }else{
                        "/usr/share/icons/breeze/actions/22/go-next.svg"
                    }
                }
                visible:canExpanded
                anchors.left:parent.left
                anchors.verticalCenter:parent.verticalCenter
                anchors.leftMargin:5*level
                MouseArea{
                    function expand(isExpanded,path,name) {
                        var sub=[]
                        for(var i = 0; i < listFolder.count; ++i) {
                            var item=onedriveBridge.getModelData(i)
                            if (item["path"]===path){
                                onedriveBridge.updateModel([i,"isExpanded",isExpanded])
                            }else{
                                if((item["parentPath"] === path) || (sub.includes(item["parentPath"]))){
                                    onedriveBridge.updateModel([i,"isExpanded",isExpanded])
                                    if (item["subtype"]==="parent"){
                                        sub.push(item["path"])
                                        onedriveBridge.updateModel([i,"hide",!isExpanded])
                                    }
                                }
                            }
                        }
                    } 
                    anchors.fill:parent
                    onClicked:{
                        if ((type == "parent") || (subtype=="parent")) {
                            if (isExpanded == false) {
                                expand(true,path,name)
                            }else{
                                expand(false,path,name)
                            }
                            isExpanded = !isExpanded
                        }
                    }
                }
            }

            CheckBox {
                id:folderCheck
                checked:isChecked
                function check(isChecked) {
                    var sub=[]
                    for(var i = 0; i < listFolder.count; ++i) {
                        var item=onedriveBridge.getModelData(i)
                        if (item["path"]===path){
                            onedriveBridge.updateModel([i,"isChecked",isChecked])
                        }else{
                            if((item["parentPath"] === path) || (sub.includes(item["parentPath"]))){
                                onedriveBridge.updateModel([i,"isChecked",isChecked])
                                onedriveBridge.folderChecked([item["path"],isChecked])
                                if (item["subtype"]==="parent"){
                                    sub.push(item["path"])
                                 }
                            }

                        }
                        if (isChecked){
                            if (!item["isChecked"]){
                                if (item["parentPath"]!="OneDrive"){
                                    var refPath=item["path"]+"/"
                                    if (path.includes(refPath)){
                                        if (isParentChecked(item["parentPath"])){
                                            onedriveBridge.updateModel([i,"isChecked",isChecked])
                                            onedriveBridge.folderChecked([item["path"],isChecked])
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
                onToggled:{
                    if ((type==="parent")||(subtype==="parent")){
                        check(folderCheck.checked)
                    }
                    onedriveBridge.folderChecked([path,folderCheck.checked])
                }

                anchors.left:menuOptionIcon.right
                anchors.verticalCenter:parent.verticalCenter
            }

            Image{
                id:folderIcon
                source:{
                    if ((type==="parent")||(subtype==="parent")){
                        "/usr/share/icons/breeze/places/22/folder-black.svg"
                    }else{
                        "/usr/share/icons/breeze/mimetypes/22/none.svg"
                    }
                }
                visible:true
                anchors.left:folderCheck.right
                anchors.verticalCenter:parent.verticalCenter
            }

            Text{
                id: text
                text: name
                width:300
                clip: true
                anchors.left:folderIcon.right
                anchors.leftMargin:5
                anchors.verticalCenter:parent.verticalCenter
            }
        }
    }

    function isParentChecked(parentPath){

        for(var i = 0; i < listFolder.count; ++i) {
            var item=onedriveBridge.getModelData(i)
            if (item["path"]==parentPath){
                if (item["isChecked"]){
                    return true
                }
            }
        }
        return false
    }
}

