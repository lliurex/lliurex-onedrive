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
                    optionText:i18nd("lliurex-onedrive","Account")
                    optionIcon:"/usr/share/icons/breeze/actions/16/actor.svg"
                    Connections{
                        function onMenuOptionClicked(){
                            onedriveBridge.moveToManageOption(0)
                            /*
                            onedriveBridge.hideSettingsMessage()
                            onedriveBridge.hideSynchronizeMessage()
                            */
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
                            /*
                            onedriveBridge.hideSettingsMessage()
                            onedriveBridge.hideSynchronizeMessage()
                            */
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
                            /*
                            onedriveBridge.hideSettingsMessage()
                            onedriveBridge.hideSynchronizeMessage() 
                            */
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
                            /*
                            onedriveBridge.hideSettingsMessage()
                            onedriveBridge.hideSynchronizeMessage()
                            */       
                        }
                    }
                }

                
            }
        }
    }

    StackLayout {
        id: manageLayout
        currentIndex:onedriveBridge.manageCurrentOption
        implicitHeight: 450
        Layout.alignment:Qt.AlignHCenter

        AccountInfo{
            id:accountInfo
        }
        
        Synchronize{
            id:synchronize
        }
        Settings{
            id:settings
        }
        Tools{
            id:tools
        }
        

    }
}

