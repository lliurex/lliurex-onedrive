import QtQuick
import QtQuick.Controls
import QtQuick.Layouts


GridLayout{
    id: optionsGrid
    columns: 2
    flow: GridLayout.LeftToRight
    columnSpacing:10

    GridLayout{
        rows:2
        flow: GridLayout.TopToBottom

        MenuOptionBtn {
            id:goBackBtn
            optionText:i18nd("lliurex-onedrive","Spaces")
            optionFontSize:14
            optionIcon:"/usr/share/icons/breeze/actions/24/go-previous.svg"
            Connections{
                function onMenuOptionClicked(){
                    spaceStackBridge.goHome();
                }
            }
        }  
        Rectangle{
            width:130
            Layout.minimumHeight:475
            Layout.fillHeight:true
            border.color: "#d3d3d3"
            GridLayout{
                id: menuGrid
                rows:4 
                flow: GridLayout.TopToBottom
                rowSpacing:0

                MenuOptionBtn {
                    id:infoItem
                    optionText:i18nd("lliurex-onedrive","Space")
                    optionIcon:"/usr/share/icons/breeze/places/22/folder.svg"
                    Connections{
                        function onMenuOptionClicked(){
                           spaceStackBridge.moveToManageOption(0)
                        }
                    }
                }
                
                MenuOptionBtn {
                    id:synchronizeItem
                    optionText:i18nd("lliurex-onedrive","Synchronize")
                    optionIcon:"/usr/share/icons/breeze/actions/22/view-refresh.svg"
                    Connections{
                        function onMenuOptionClicked(){
                            spaceStackBridge.moveToManageOption(1)
                        }
                    }
                }

                MenuOptionBtn {
                    id:settingsItem
                    optionText:i18nd("lliurex-onedrive","Settings")
                    optionIcon:"/usr/share/icons/breeze/actions/22/configure.svg"
                    Connections{
                        function onMenuOptionClicked(){
                            spaceStackBridge.moveToManageOption(2)
                        }
                    }
                }
                MenuOptionBtn {
                    id:toolsItem
                    optionText:i18nd("lliurex-onedrive","Tools")
                    optionIcon:"/usr/share/icons/breeze/actions/22/tools.svg"
                    Connections{
                        function onMenuOptionClicked(){
                            spaceStackBridge.moveToManageOption(3)
                        }
                    }
                }
                
            }
        }
    }

    StackView {
        id: manageView
        property int currentOption:spaceStackBridge.manageCurrentOption
        Layout.fillWidth:true
        Layout.fillHeight: true
        initialItem:accountView

        onCurrentOptionChanged:{
            switch(currentOption){
                case 0:
                    manageView.replace(accountView)
                    break;
                case 1:
                    manageView.replace(synchronizeView)
                    break;
                case 2:
                    manageView.replace(settingsView)
                    break;
                case 3:
                    manageView.replace(toolsView)
                    break
                case 4:
                    manageView.replace(updateAuthView)
                    break
            }

        }
        replaceEnter: Transition {
            PropertyAnimation {
                property: "opacity"
                from: 0
                to:1
                duration: 60
            }
        }
        replaceExit: Transition {
            PropertyAnimation {
                property: "opacity"
                from: 1
                to:0
                duration: 60
            }
        }

        Component{
            id:accountView
            AccountInfo{
                id:accountInfo
            }
        }
        Component{
            id:synchronizeView
            Synchronize{
                id:synchronize
            }
        }
        Component{
            id:settingsView
            Settings{
                id:settings
            }
        }
        Component{
            id:toolsView
            Tools{
                id:tools
            }
        }
        Component{
            id:updateAuthView
            OnedriveAuth{
                id:oneDriveUpdateAuth
                authUrl:addSpaceStackBridge.authUrl
            }
        }
    }
}

