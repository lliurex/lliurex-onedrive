import QtQuick 2.6
import QtQuick.Controls 2.6
import QtQuick.Layouts 1.15


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
            rows:4 
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
                    }
                }
            }

            MenuOptionBtn {
                id:settingsItem
                optionText:i18nd("lliurex-onedrive","Settings")
                optionIcon:"/usr/share/icons/breeze/actions/16/configure.svg"
                Connections{
                    function onMenuOptionClicked(){
                        optionsLayout.currentIndex=1;
                        onedriveBridge.hideSettingsMessage()
                    }
                }
            }

            MenuOptionBtn {
                id:toolsItem
                optionText:i18nd("lliurex-onedrive","Tools")
                optionIcon:"/usr/share/icons/breeze/actions/16/tools.svg"
                Connections{
                    function onMenuOptionClicked(){
                        optionsLayout.currentIndex=2;
                        onedriveBridge.hideSettingsMessage()
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
        currentIndex:0
        implicitHeight: 450
        Layout.alignment:Qt.AlignHCenter

        AccountInfo{
            id:accountInfo
        }

        Settings{
            id:settings
        }

        Tools{
            id:tools
        }

    }
}

