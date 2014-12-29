var BACKEND = {
  pins: null, // the full list of pins from the server
  sources: null, // list of sources the pins came from
  loc: null, // the currently active location

  getData: function() {
    $.ajax({
      url: window.location.pathname + "/data",
      type: "GET",
      dataType: "json",
      success: BACKEND.cleanData,
      error: console.log
    });
    // location/locName/data
  },

  /* Takes raw data directly from an AJAX call and turns it into a usable format.
   */
  cleanData: function(e) {
    jsonpins = JSON.parse(e.pushpins);
    BACKEND.pins = jsonpins.map(function(pin){ return pin["fields"]; });
    BACKEND.sources = e.sources;
    initializeAll(BACKEND.pins, BACKEND.loc);
  },

};
