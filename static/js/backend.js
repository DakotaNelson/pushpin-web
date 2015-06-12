var BACKEND = {
  pins: null, // the full list of pins from the server
  sources: null, // list of sources the pins came from
  loc: null, // the currently active location

  getData: function() {
    if(BACKEND.loc === null) {
      // we're not in a specific location
      return;
    }
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

  addLocation: function(successBack, failBack) {
    $.ajax({
      url: $(event.srcElement).attr('action'),
      type: "POST",
      data: $(event.srcElement).serialize(),
      success: successBack,
      error: failBack
    });
    return false;
  },

  deleteLocation: function(successBack, failBack) {
    if(BACKEND.loc === null) {
      // we're not in a specific location
      return;
    }
    var csrftoken = getCookie('csrftoken');

    $.ajax({
      url: window.location.pathname + '/delete/',
      headers: {"X-CSRFToken":csrftoken},
      type: "POST",
      data: {},
      success: successBack,
      error: failBack
    });
  },
};
