import QtQuick 2.6
import QtQuick.Window 2.2
import QtWebEngine 1.10

Rectangle {
    width: 725
    height: 615
    visible: true
    WebEngineView {
        id:webEngine
        anchors.fill:parent
        url: "https://login.microsoftonline.com/common/oauth2/v2.0/authorize?client_id=d50ca740-c83f-4d1b-b616-12c519384f0c&scope=Files.ReadWrite%20Files.ReadWrite.all%20Sites.Read.All%20Sites.ReadWrite.All%20offline_access&response_type=code&redirect_uri=https://login.microsoftonline.com/common/oauth2/nativeclient"
        profile.persistentCookiesPolicy:WebEngineProfile.NoPersistentCookies
        onLoadingChanged:{
            var ret=loadRequest.url.toString()
            if (ret.indexOf("nativeclient?code=")===48){
                onedriveBridge.createAccount(ret);

            }
        }
        
    }

    function closeConnection(){
        webEngine.action(webEngine.Stop)

    }
}
