(function() {
  
  var reverse = []; // Store the nodes to restore for each changed property (2-levels array)
  
  function eventManagerInit() {

    chrome.extension.onMessage.addListener(function(e) {
        switch (e.action) {
          case "blanketStyleSet": blanketStyleSet(e.property, e.from, e.to); break;
          case "blanketStyleRestore": blanketStyleRestore(e.property); break;
        }
    });
  }
  eventManagerInit(); // Init
  
  function blanketStyleSet(property, from, to) {
    /**
     * Convert a CSS property value to a specific value for every DOM node
     * From a function by @guille
     */
    var els = document.getElementsByTagName('*');
    var el;
    var styles;
    
    // ****** Store the Restores
    if (property in reverse) {
      // This property was already reset!
      // Switch back before applying...
      blanketStyleRestore(property);
    }
    reverse[property] = [];
    
    // ****** Iterate the DOM
    for (var i = 0, l = els.length; i < l; i++) {
      el = els[i];
      
      if (from == el.style[property]) {
        // *** Check for node style:
        el.style[property] = to;
        reverse[property].push(function() {
          this.style[property] = from;
        }.bind(el));
      } else {
        // *** Check for computed style:
        styles = getComputedStyle(el);
        if (from == styles.getPropertyValue(property)) {
          el.style[property] = to;
          reverse[property].push(function(){
            this.style[property] = from;
          }.bind(el));
        }
      }
    }
  }
  
  function blanketStyleRestore(property) {
    /**
     * Convert back
     * From a function by @guille
     */
    var fx;
    
    while (fx = reverse[property].shift()) {
      fx();
    }
    delete reverse[property];
  };
  
})();