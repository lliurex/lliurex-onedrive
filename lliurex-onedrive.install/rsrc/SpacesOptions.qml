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
            rows:2 
            flow: GridLayout.TopToBottom
            rowSpacing:0

            MenuOptionBtn {
                id:spaceItem
                optionText:i18nd("lliurex-onedrive","Spaces")
                optionIcon:"/usr/share/icons/breeze/places/16/folder-cloud.svg"
                Connections{
                    function onMenuOptionClicked(){
                        onedriveBridge.moveToSpaceOption(0);
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
                    }
                }
            }
        }
    }

    StackLayout {
        id: optionsLayout
        currentIndex:onedriveBridge.spacesCurrentOption
        implicitHeight: 450
        Layout.alignment:Qt.AlignHCenter

        SpacesSettings{
            id:spaceSettings
        }

        SpaceForm{
            id:spaceForm
            email:""
            onedriveRb:true
            sharePoint:""
        }

        OnedriveAuth{
            id:oneDriveAuth
            authUrl:onedriveBridge.authUrl
        }

    }
}

