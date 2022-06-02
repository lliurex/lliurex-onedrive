import QtQuick 2.6
import QtWebEngine 1.10
import QtQuick.Controls 2.6
import QtQuick.Layouts 1.12


Rectangle {
    visible: true
    property alias authUrl:webEngine.url

    Component.onDestruction:{
        console.log("destruyendo")
        closeConnection()
    }


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
