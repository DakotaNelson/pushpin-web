var LOCATIONS = {

  //elementId: "#locations-inner table",
  //elementWrapperId: "#locations-inner",
  queryURL: '/map/locations/', // where to get our data
  data: null,
  //table: null, // reference to the DataTables object

  // initializes the table when the DOM is ready
  onLoad: function() {
    LOCATIONS.update(); // triggers a magical update chain
  },

  update: function() {
    // aliases getData, since calling update makes more sense
    LOCATIONS.getData();
  },

  // makes an ajax call to get data (imagine that)
  getData: function() {
    $.ajax({
      url: LOCATIONS.queryURL,
      type: "GET",
      success: LOCATIONS.storeData,
      error: console.log
    });
  },

  // after a successful AJAX query, cleans and stores the data,
  // then triggers a render
  storeData: function(d) {
    LOCATIONS.data = d.map(function(datum) {
      var date = new Date(datum.date);
      var day = date.getDate();
      var month = date.getMonth();
      var year = date.getYear();
      // ew.
      datum.dateDisplay = day + "/" + month + "/" + year;
      datum.date = date;
      return datum;
    });
    LOCATIONS.draw(); // actually update the DOM
  },

  // re-render using super-advanced templating methods
  draw: function() {
    var linkStart = '<li><a href="'
    var linkEnd = '">';
    var endcap = '</a></li>';
    var divider = '<li class="divider"></li>';
    var header = '<li class="dropdown-header">Locations</li>';

    // first, remove any locations that are already there
    $("#navbar ul li.dropdown-header").nextAll().remove();

    // then, loop through each location and add it (they'll end up being reverse chronological)
    if(LOCATIONS.data.length > 0) {
      _.each(LOCATIONS.data, function(datum) {
        // start appending links to locations
        var link = '/map/location/' + datum.name;
        var html = linkStart + link + linkEnd + datum.name + endcap;
        $("#navbar ul li.dropdown-header").after(html);
      });
    }
    else {
      // delete the header and divider
      $("#navbar ul li.dropdown-header").remove();
      $("#navbar ul li.divider").remove();
    }
  },
};
