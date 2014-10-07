var Screenshotter = {
  
  imageDataURL: [],
  
  shared: {
    imageDataURLPartial: [],
    imageDirtyCutAt: 0,
    imageDataURL: 0,
    
    originalScrollTop: 0,
    
    tab: {
      id: 0,
      url: "",
      title: "",
      hasVscrollbar: false
    }
  },

  grab: function(e) {

    var self = this;
    
    this.imageDataURLPartial = [];
    
    chrome.windows.getCurrent(function(win) {
      chrome.tabs.getSelected(win.id, function(tab) {
        self.shared.tab = tab;
        
        var parts = tab.url.match(/https?:\/\/chrome.google.com\/?.*/);
        if (parts !== null) {
          alert("\n\n\nI'm sorry.\n\nDue to security restrictions \non the Google Chrome Store, \nBlipshot can't run here.\n\nTry on any other page. ;)\n\n\n");
          return false;
        }
        
        chrome.tabs.sendMessage(self.shared.tab.id, { action: 'blanketStyleSet', property: 'position', from: 'fixed', to: 'absolute' });
        self.screenshotBegin(self.shared);
      });
    });
  },
  
  // 1
  screenshotBegin: function(shared) { chrome.tabs.sendMessage(this.shared.tab.id, { action: 'screenshotBegin', shared: shared }); },
  
  // 2
  screenshotVisibleArea: function(shared) {
    var self = this;
    chrome.tabs.captureVisibleTab(null, { format: "png" /* png, jpeg */, quality: 100 }, function(dataUrl) {
      if (dataUrl) {
        // Grab successful
        self.imageDataURLPartial.push(dataUrl);
        self.screenshotScroll(shared);
      } else {
        // Grab failed, warning
        // To handle issues like permissions - https://github.com/folletto/Blipshot/issues/9
        alert("\n\n\nI'm sorry.\n\nIt seems Blipshot wasn't able to grab the screenshot of the active tab.\n\nPlease check the extension permissions.\n\nIf the problem persists contact me at \nhttp://github.com/folletto/Blipshot/issues\n\n\n");
        return false;
      }
    });
  },
  
  // 3
  screenshotScroll: function(shared) { chrome.tabs.sendMessage(this.shared.tab.id, { action: 'screenshotScroll', shared: shared }); },
  
  // 4
  screenshotEnd: function(shared) {
    var self = this;
    UI.status('azure', "make");
    
    this.recursiveImageMerge(this.imageDataURLPartial, shared.imageDirtyCutAt, shared.tab.hasVscrollbar, function(image) {
      shared.imageDataURL = image;
      self.screenshotReturn(shared);
    });
  },
  
  // 5
  screenshotReturn: function(shared) {
    UI.status('green', "done", 3000);
    chrome.tabs.sendMessage(this.shared.tab.id, { action: 'blanketStyleRestore', property: 'position' });
    chrome.tabs.sendMessage(this.shared.tab.id, { action: 'screenshotReturn', shared: shared });
  },
  
  // ****************************************************************************************** EVENT MANAGER / HALF
  eventManagerInit: function() {
    /****************************************************************************************************
     * This function prepares the internal plugin callbacks to bounce between the plugin and DOM side.
     * It's initialized at the end of this file.
     */
    var self = this;
    chrome.extension.onMessage.addListener(function(e) {
        switch (e.action) {
          case "grab": self.grab(); break;
          case "screenshotVisibleArea": self.screenshotVisibleArea(e.shared); break;
          case "screenshotEnd": self.screenshotEnd(e.shared); break;
        }
    });
  },
  

  recursiveImageMerge: function(imageDataURLs, imageDirtyCutAt, hasVscrollbar, callback, images, i) {
    /**
     * This function merges together all the pieces gathered during the scroll, recursively.
     * Returns a single data:// URL object from canvas.toDataURL("image/png") to the callback.
     */
    var fx = arguments.callee;
    i = i || 0;
    images = images || [];
    
    if (i < imageDataURLs.length) {
      images[i] = new Image();
      images[i].onload = function() {
        imageDataURLs[i] = null; // clear for optimize memory consumption (not sure)
        if (i == imageDataURLs.length - 1) {
          // ****** We're at the end of the chain, let's have fun with canvas.
          var canvas = window.document.createElement('canvas');
          
          // NOTE: Resizing a canvas is destructive, we can do it just now before stictching
          canvas.width = images[0].width - (hasVscrollbar ? 15 : 0); // <-- manage V scrollbar
          
          if (images.length > 1) canvas.height = (imageDataURLs.length - 1) * images[0].height + imageDirtyCutAt;
          else canvas.height = images[0].height;
          
          // ****** Stitch
          for (var j = 0; j < images.length; j++) {
            var cut = 0;
            if (images.length > 1 && j == images.length - 1) cut = images[j].height - imageDirtyCutAt;
            
            var height = images[j].height - cut;
            var width = images[j].width;
            //alert("[i:" + i + ", j:" + j + "]" + width + "x" + height + "(cut:" + cut + ") --- images:" + imageDataURLs.length);
            
            canvas.getContext("2d").drawImage(images[j], 0, cut, width, height, 0, j * images[0].height, width, height);
          }
          
          callback(canvas.toDataURL("image/png")); // --> CALLBACK (note that the file type is used also in the drag function)
        } else {
          // ****** Down!
          fx(imageDataURLs, imageDirtyCutAt, hasVscrollbar, callback, images, ++i);
        }
      }
      images[i].src = imageDataURLs[i]; // Load!
    }
  }
}

Screenshotter.eventManagerInit();