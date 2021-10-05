import QtQuick 2.6
import QtQuick.Controls 2.6
import QtQml.Models 2.6

Rectangle {
    property alias structVisible:folderTable.visible

    id:folderTable
    visible: structVisible
    width: 660; height: 240

    ListModel{
        id: folderModel
    }    
    ListView{
        id: listFolder
        anchors.fill:parent
        height: parent.height
        model:onedriveBridge.model
        delegate: listdelegate
        clip: true
        boundsBehavior: Flickable.StopAtBounds
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
            border.width: 0.4

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
                visible:{
                    if ((type==="parent")||(subtype==="parent")){
                        true
                    }else{
                        false
                    }

                }
                anchors.left:parent.left
                anchors.verticalCenter:parent.verticalCenter
                anchors.leftMargin:5*level
                MouseArea{
                    function expand(isExpanded,name) {
                        var sub=[]
                        for(var i = 0; i < listFolder.count; ++i) {
                            var item=onedriveBridge.getModelData(i)
                            if (item["name"]===name){
                                onedriveBridge.updateModel([i,"isExpanded",isExpanded])
                            }else{
                                if((item["type"] === name) || (sub.includes(item["type"]))){
                                    onedriveBridge.updateModel([i,"isExpanded",isExpanded])
                                    if (item["subtype"]==="parent"){
                                        sub.push(item["name"])
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
                                expand(true,name)
                            }else{
                                expand(false,name)
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
                    var sub=""
                    for(var i = 0; i < listFolder.count; ++i) {
                        var item=onedriveBridge.getModelData(i)
                        if (item["name"]===name){
                            onedriveBridge.updateModel([i,"isChecked",isChecked])
                        }else{
                            if((item["type"] === name) || (item["type"]===sub)){
                                onedriveBridge.updateModel([i,"isChecked",isChecked])
                                onedriveBridge.folderChecked([item["name"],isChecked])
                                if (item["subtype"]==="parent"){
                                    var sub=item["name"]
                                }
                            }
                        }
                    }
                }
                onToggled:{
                    if ((type==="parent")||(subtype==="parent")){
                        check(folderCheck.checked)
                    }
                    console.log(isChecked)
                    onedriveBridge.folderChecked([name,folderCheck.checked])
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
}

