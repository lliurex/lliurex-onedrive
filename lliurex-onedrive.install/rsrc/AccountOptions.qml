import QtQuick 2.6
import QtQuick.Controls 2.6
import QtQuick.Layouts 1.12


GridLayout{
    id: optionsGrid
    columns: 2
    flow: GridLayout.LeftToRight
    columnSpacing:10

    Rectangle{
        width:120
        height:515
        border.color: "#d3d3d3"

        GridLayout{
            id: menuGrid
            rows:5 
            flow: GridLayout.TopToBottom
            rowSpacing:0

            MenuOptionBtn {
                id:infoItem
                optionText:i18nd("lliurex-onedrive","Account")
                optionIcon:"/usr/share/icons/breeze/actions/16/actor.svg"
                Connections{
                    function onMenuOptionClicked(){
                        optionsLayout.currentIndex=0;
                        onedriveBridge.hideSettingsMessage()
                        onedriveBridge.hideSynchronizeMessage()
                    }
                }
            }

            MenuOptionBtn {
                id:synchronizeItem
                optionText:i18nd("lliurex-onedrive","Synchronize")
                optionIcon:"/usr/share/icons/breeze/actions/16/view-refresh.svg"
                Connections{
                    function onMenuOptionClicked(){
                        optionsLayout.currentIndex=1;
                        onedriveBridge.hideSettingsMessage()
                        onedriveBridge.hideSynchronizeMessage()
                        synchronize.structModel=onedriveBridge.model
                    }
                }
            }
            MenuOptionBtn {
                id:settingsItem
                optionText:i18nd("lliurex-onedrive","Settings")
                optionIcon:"/usr/share/icons/breeze/actions/16/configure.svg"
                Connections{
                    function onMenuOptionClicked(){
                        optionsLayout.currentIndex=2;
                        onedriveBridge.hideSettingsMessage()
                        onedriveBridge.hideSynchronizeMessage() 
                    }
                }
            }

            MenuOptionBtn {
                id:toolsItem
                optionText:i18nd("lliurex-onedrive","Tools")
                optionIcon:"/usr/share/icons/breeze/actions/16/tools.svg"
                Connections{
                    function onMenuOptionClicked(){
                        optionsLayout.currentIndex=3;
                        onedriveBridge.hideSettingsMessage()
                        onedriveBridge.hideSynchronizeMessage()       
                    }
                }
            }

            MenuOptionBtn {
                id:helpItem
                optionText:i18nd("lliurex-onedrive","Help")
                optionIcon:"/usr/share/icons/breeze/actions/16/help-contents.svg"
                Connections{
                    function onMenuOptionClicked(){
                        onedriveBridge.openHelp();
                        onedriveBridge.hideSettingsMessage()
                    }
                }
            }
        }
    }

    StackLayout {
        id: optionsLayout
        currentIndex:onedriveBridge.currentOptionsStack
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

