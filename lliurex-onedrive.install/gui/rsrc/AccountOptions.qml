import QtQuick 2.6
import QtQuick.Controls 2.6
import QtQuick.Layouts 1.12


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
            optionIcon:"/usr/share/icons/breeze/actions/24/arrow-left.svg"
            Connections{
                function onMenuOptionClicked(){
                    onedriveBridge.goHome();
                }
            }
        }  
        Rectangle{
            width:120
            height:475
            border.color: "#d3d3d3"
            GridLayout{
                id: menuGrid
                rows:4 
                flow: GridLayout.TopToBottom
                rowSpacing:0

                MenuOptionBtn {
                    id:infoItem
                    optionText:i18nd("lliurex-onedrive","Space")
                    optionIcon:"/usr/share/icons/breeze/places/16/folder.svg"
                    Connections{
                        function onMenuOptionClicked(){
                            onedriveBridge.moveToManageOption(0)
                        }
                    }
                }
                
                MenuOptionBtn {
                    id:synchronizeItem
                    optionText:i18nd("lliurex-onedrive","Synchronize")
                    optionIcon:"/usr/share/icons/breeze/actions/16/view-refresh.svg"
                    Connections{
                        function onMenuOptionClicked(){
                            onedriveBridge.moveToManageOption(1)
                        }
                    }
                }

                MenuOptionBtn {
                    id:settingsItem
                    optionText:i18nd("lliurex-onedrive","Settings")
                    optionIcon:"/usr/share/icons/breeze/actions/16/configure.svg"
                    Connections{
                        function onMenuOptionClicked(){
                            onedriveBridge.moveToManageOption(2)
                        }
                    }
                }
                MenuOptionBtn {
                    id:toolsItem
                    optionText:i18nd("lliurex-onedrive","Tools")
                    optionIcon:"/usr/share/icons/breeze/actions/16/tools.svg"
                    Connections{
                        function onMenuOptionClicked(){
                            onedriveBridge.moveToManageOption(3)
                        }
                    }
                }
                
            }
        }
    }

    StackView {
        id: manageView
        property int currentOption:onedriveBridge.manageCurrentOption
        implicitHeight: 450
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
                duration: 600
            }
        }
        replaceExit: Transition {
            PropertyAnimation {
                property: "opacity"
                from: 1
                to:0
                duration: 600
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
                authUrl:onedriveBridge.authUrl
            }
        }
    }
}

