(function() {
  
  var shared = {};

  // 1
  function screenshotBegin(shared) {
    shared.originalScrollTop = window.document.body.scrollTop; // ->[] save user scrollTop
    shared.tab.hasVscrollbar = (window.innerHeight < window.document.body.scrollHeight);
    window.document.body.scrollTop = 0;
    setTimeout(function() { screenshotVisibleArea(shared); }, 100);
  }
  
  // 2
  function screenshotVisibleArea(shared) { chrome.extension.sendMessage({ action: 'screenshotVisibleArea', shared: shared }); }
  
  // 3
  function screenshotScroll(shared) {
    var scrollTopCurrent = window.document.body.scrollTop;
    
    window.document.body.scrollTop += window.innerHeight; // scroll!
    
    if (window.document.body.scrollTop == scrollTopCurrent) {
      
      shared.imageDirtyCutAt = scrollTopCurrent % window.document.documentElement.clientHeight;
      window.document.body.scrollTop = shared.originalScrollTop; // <-[] restore user scrollTop
      screenshotEnd(shared);
    } else {

      setTimeout(function() { screenshotVisibleArea(shared); }, 100);
    }
  }
  
  // 4
  function screenshotEnd(shared) { chrome.extension.sendMessage({ action: 'screenshotEnd', shared: shared }); }
  
  // 5
  function screenshotReturn(shared) {
    function pad2(str) { if ((str + "").length == 1) return "0" + str; return "" + str; }
    
    var d = new Date();
    var timestamp = '' + d.getFullYear() + '-' + pad2(d.getMonth() + 1) + '-' + pad2(d.getDay()) + '-' + pad2(d.getHours()) + '' + pad2(d.getMinutes()) + '';
    var filename = "pageshot of '" + normalizeFileName(shared.tab.title) + "' @ " + timestamp;
    var blobURL = dataToBlobURL(shared.imageDataURL);
    var new_image = new Image();
    new_image.src = shared.imageDataURL;

    var xhr = new XMLHttpRequest();;
    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4) {
            if ((xhr.status >= 200 && xhr.status < 300) || xhr.status == 304) {
                alert(xhr.responseText);
            } else {
              //success
            }
        }
    };
    console.log(encodeURIComponent(shared.imageDataURL))
    //xhr.open("post", "http://1.topdfs.sinaapp.com/", true);
    xhr.open("post", "http://127.0.0.1:8888", true);
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded ");
    xhr.send("img="+encodeURIComponent(shared.imageDataURL)+"&width="+new_image.width+"&height="+new_image.height);
    // ****** Add DOM Elements to Page
    var div = window.document.createElement('div');
    div.id = "blipshot";
    div.innerHTML = '<div id="blipshot-dim" style="position: absolute !important; height: ' + window.document.body.scrollHeight + 'px !important; width: 100% !important; top: 0px !important; left: 0px !important; background: #000000 !important; opacity: 0.66 !important; z-index: 666666 !important;"> </div>';
    div.innerHTML += '<p style="-webkit-box-shadow: 0px 5px 10px #000000; margin: 20px; background: #ffffff; position: absolute; top: 0; right: 0; z-index: 666667 !important;"><img id="blipshot-img" alt="' + filename + '" src="' +  blobURL + '" width= "400" /></p>';
    window.document.body.appendChild(div);
    
    // ****** Add Event Listeners
    function actionRemoveDiv() {
      // Closes the extension overlays.
      var blipshotdiv = window.document.getElementById('blipshot');
      if (blipshotdiv) blipshotdiv.parentElement.removeChild(blipshotdiv);
      
      // Cleanup
      window.webkitURL.revokeObjectURL(blobURL);
    }
    function actionDrag(e) {
      e.dataTransfer.setData("DownloadURL", "image/jpeg:" + filename + ".jpeg:" + blobURL);
    }
    window.document.getElementById('blipshot-dim').addEventListener("click", actionRemoveDiv);
    window.document.getElementById('blipshot-img').addEventListener("dragstart", actionDrag);
  }
  
  function eventManagerInit() {

    var self = this;
    chrome.extension.onMessage.addListener(function(e) {
        switch (e.action) {
          case "screenshotBegin": screenshotBegin(e.shared); break;
          case "screenshotScroll": screenshotScroll(e.shared); break;
          case "screenshotReturn": screenshotReturn(e.shared); break;
        }
    });
  }
  eventManagerInit(); // Init
  
  function dataToBlobURL(dataURL) {

    var parts = dataURL.match(/data:([^;]*)(;base64)?,([0-9A-Za-z+/]+)/);
    
    // Assume base64 encoding
    var binStr = atob(parts[3]);
    
    // Convert to binary in ArrayBuffer
    var buf = new ArrayBuffer(binStr.length);
    var view = new Uint8Array(buf);
    for(var i = 0; i < view.length; i++)
      view[i] = binStr.charCodeAt(i);

    // Create blob with mime type, create URL for it
    var blob = new Blob([view], {'type': parts[1]});
    var URL = webkitURL.createObjectURL(blob)
    console.log(URL)
    return URL;
  }
  
  function normalizeFileName(string) {
    out = string;
    //out = out.replace(/"/, '\''); // To avoid collision with DOM attribute
    //out = out.replace(/\/\?<>\\:\*\|/, '-'); // Windows safe
    out = out.replace(/[^a-zA-Z0-9_\-+,;'!?$£@&%()\[\]=]/g, " ").replace(/ +/g, " "); // Hard replace
    return out;
  }
})();
