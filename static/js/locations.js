var LOCATIONS = {

  elementId: "#locations-inner table",
  elementWrapperId: "#locations-inner",
  queryURL: '/map/locations', // where to get our data
  data: null,
  table: null, // reference to the DataTables object

  // initializes the table when the DOM is ready
  onLoad: function() {
    LOCATIONS.initTable();
    LOCATIONS.update(); // triggers a magical update chain
  },

  update: function() {
    // aliases getData, since calling update makes more sense
    LOCATIONS.getData();
  },

  // makes an ajax call to get data
  getData: function() {
    $.ajax({
      url: LOCATIONS.queryURL,
      type: "GET",
      success: LOCATIONS.storeData,
      error: console.log
    });
  },

  // after a successful AJAX query, cleans and stores the data,
  // then triggers a table render
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
    LOCATIONS.draw(); // actually update the table
  },

  // re-render the table
  draw: function() {
    LOCATIONS.table.clear();
    LOCATIONS.table.rows.add(LOCATIONS.data);
    LOCATIONS.table.draw();
  },

  // do initial setup on the table
  initTable: function() {
    LOCATIONS.table = $(LOCATIONS.elementId).DataTable( {
      'autoWidth': false,
      'paging': false,
      'scrollX': false,
      'scrollY': $(LOCATIONS.elementWrapperId).height()-60,
      'scrollCollapse': true,
      'data':LOCATIONS.data,
      'columns': [
        { name: 'name',
          title: 'Name',
          data: 'name',
          width: '50%'
        },
        { name: 'latitude',
          title: 'Latitude',
          data: 'latitude',
          width: '1%'
            // it won't actually go any less wide than its contents
        },
        { name: 'longitude',
          title: 'Longitude',
          data: 'longitude',
          width: '10px'
        },
        { name: 'radius',
          title: 'Radius',
          data: 'radius',
          width: '10px'
        },
        { name: 'date',
          title: 'Created',
          data: 'date',
          type: 'date',
          width: '40%',
          render: function(data, type, full, meta){
            if(type == "display"){
              var date = new Date(data);
              var options = {year: "numeric", month: "short", day: "numeric"};
              return date.toLocaleDateString('en-US',options);
            }
            return data;
          }
        }
      ],
      'rowCallback': function( row, data ) {
        $(row).on('click',
            function() {
              document.location = '/map/location/' + encodeURIComponent(data.name);
            });
        },
    });
  },
};
