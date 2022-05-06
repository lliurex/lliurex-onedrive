import QtQuick 2.6
import QtWebEngine 1.10
import QtQuick.Controls 2.6
import QtQuick.Layouts 1.12
import QtQuick.Dialogs 1.3


Rectangle {
    width: 725
    height: 615
    visible: true
    property alias authUrl:webEngine.url

    WebEngineView {
        id:webEngine
        anchors.fill:parent
        url: authUrl
        profile.persistentCookiesPolicy:WebEngineProfile.NoPersistentCookies
        onLoadingChanged:{
            var ret=loadRequest.url.toString()
            if (ret.indexOf("nativeclient?code=")===48){
                console.log("hecho");
                onedriveBridge.getToken(ret);
                profile.clearHttpCache();
                webEngine.action(webEngine.Stop);
            }
        }
        
    }

    function closeConnection(){
        webEngine.action(webEngine.Stop)

    }

}
