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
                        if (!onedriveBridge.requiredMigration){
                            onedriveBridge.moveToSpaceOption(0);
                        }
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

    StackView {
        id: optionsView
        property int currentIndex:onedriveBridge.spacesCurrentOption
        implicitHeight: 450
        Layout.fillWidth:true
        Layout.fillHeight:true
        initialItem:spacesInfoView

        onCurrentIndexChanged:{
            switch(currentIndex){
                case 0:
                    optionsView.replace(spacesInfoView)
                    break;
                case 1:
                    optionsView.replace(spaceFormView)
                    break;
                case 2:
                    optionsView.replace(oneDriveAuthView)
                    break;
                case 3:
                    optionsView.replace(migrationView)
                    break;
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
            id:spacesInfoView
            SpacesInfo{
                id:spaceInfo
            }
        }
        Component{
            id:spaceFormView
            SpaceForm{
                id:spaceForm
            }
        }
        Component{
            id:oneDriveAuthView
            OnedriveAuth{
                id:oneDriveAuth
                authUrl:onedriveBridge.authUrl
            }
        }
        Component{
            id:migrationView
            SpaceMigration{
                id:spaceMigration
            }
        }

    }
}
