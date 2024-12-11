import QtQuick
import QtWebEngine
import QtQuick.Controls
import QtQuick.Layouts


Rectangle {
    visible: true
    property alias authUrl:webEngine.url

    Component.onDestruction:{
        closeConnection()
    }


    WebEngineView {
        id:webEngine
        anchors.fill:parent
        url: authUrl
        profile.persistentCookiesPolicy:WebEngineProfile.NoPersistentCookies
        onLoadingChanged:{
            var ret=loadingInfo.url.toString()
            if (ret.indexOf("nativeclient?code=")===48){
                addSpaceStackBridge.getToken(ret);
                profile.clearHttpCache();
                webEngine.action(webEngine.Stop);
            }
        }
        
    }

    function closeConnection(){
        webEngine.action(webEngine.Stop)

    }

}
