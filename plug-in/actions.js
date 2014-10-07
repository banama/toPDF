
var UI = {
  status: function(color, text, timed) {
    if (color == null) {
      return;
    } else if (color == 'green') {
      chrome.browserAction.setBadgeBackgroundColor({ color: [0, 255, 0, 255] });
    } else if (color == 'red') {
      chrome.browserAction.setBadgeBackgroundColor({ color: [255, 0, 0, 255] });
    } else if (color == 'orange' ) {
      chrome.browserAction.setBadgeBackgroundColor({ color: [255, 128, 0, 255] });
    } else if (color == 'azure' ) {
      chrome.browserAction.setBadgeBackgroundColor({ color: [0, 128, 255, 255] });
    }
    chrome.browserAction.setBadgeText({ text: text });
    
    if (timed > 0) {
      setTimeout(function() {
        chrome.browserAction.setBadgeText({ text: "" });
      }, timed);
    }
  }
}

chrome.browserAction.onClicked.addListener(function(tab) {
  UI.status('red', "grab");
  Screenshotter.grab();
});