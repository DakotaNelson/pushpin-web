var MAP = {
  map: null,
  markers: [],
  lat: null,
  lon: null,
  center: null, // lat/lon as a google LatLng object
  radius: null,
  data: null,
  icon: {
          'Flickr': 'http://maps.google.com/mapfiles/ms/icons/orange-dot.png',
          'Picasa': 'http://maps.google.com/mapfiles/ms/icons/purple-dot.png',
          'Shodan': 'http://maps.google.com/mapfiles/ms/icons/yellow-dot.png',
          'Twitter': 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png',
          'Youtube': 'http://maps.google.com/mapfiles/ms/icons/red-dot.png',
        },
  elementId: 'map',

  createMap: function(lat,lon,radius,zoom,data) {
    MAP.lat = lat;
    MAP.lon = lon;
    MAP.radius = radius;
    MAP.zoom = zoom;

    MAP.data = data;

    MAP.renderMap();
  },

  renderMap: function() {
    MAP.center = new google.maps.LatLng(MAP.lat,MAP.lon);

    var mapOptions = {
        zoom: MAP.zoom,
        center: MAP.center,
        disableDefaultUI: true,
        mapTypeControl: true,
        mapTypeControlOptions: {
            style: google.maps.MapTypeControlStyle.DROPDOWN_MENU,
            position: google.maps.ControlPosition.RIGHT_TOP
        },
        panControl: true,
        panControlOptions: {
            position: google.maps.ControlPosition.RIGHT_BOTTOM
        },
        streetViewControl: true,
        streetViewControlOptions: {
            position: google.maps.ControlPosition.RIGHT_BOTTOM
        },
        zoomControl: true,
        zoomControlOptions: {
            position: google.maps.ControlPosition.RIGHT_BOTTOM
        }
    };

    MAP.map = new google.maps.Map(document.getElementById(MAP.elementId), mapOptions);

    var populationOptions = {
        strokeColor: "gray",
        strokeOpacity: 0.8,
        strokeWeight: 1,
        fillColor: "gray",
        fillOpacity: 0.1,
        map: MAP.map,
        center: MAP.center,
        radius: MAP.radius * 1000
    };

    var cityCircle = new google.maps.Circle(populationOptions);

    MAP.addMarker(
      {
        position:MAP.center,
        title:"Epicenter",
        icon:"http://maps.google.com/mapfiles/ms/icons/green-dot.png",
        map:MAP.map
      },
      {
        details:"Epicenter:<br />" + MAP.lat + "," + MAP.lon + "<br />Radius: " + MAP.radius + "km"
      }
    );

    // get template from the page, and load it in to the underscore.js template function
    var pinTemplate = _.template($('#pushpinTemplate').html());
    MAP.data.forEach(function(pin) {
      MAP.addMarker({
          position: new google.maps.LatLng(pin.latitude, pin.longitude),
          title: pin.screen_name, icon: MAP.icon[pin.source] ,
          map:MAP.map
        },
        {
          details: pinTemplate(pin)
        },
        pin.source
      );
    });
    // TODO linkify the messages (jQuery linkify already included)
  },

  addMarker: function(opts, place, source) {
    var marker = new google.maps.Marker(opts);

    var infowindow = new google.maps.InfoWindow({
        autoScroll: false,
        content: place.details
    });

    google.maps.event.addListener(marker, 'click', function() {
        infowindow.open(MAP.map,marker);
    });

    if(MAP.markers[source] == undefined) {
      MAP.markers[source] = [];
    }

    MAP.markers[source].push(marker);
  },

  setMarkers: function(place, source) {
    for (var i = 0; i < MAP.markers[source].length; i++) {
        MAP.markers[source][i].setMap(place);
    }
  },

  showMarkers: function(source) {
    MAP.setMarkers(MAP.map, source);
  },

  hideMarkers: function(source) {
    MAP.setMarkers(null, source);
  },

  toggleMarkers: function(source) {
    if(document.getElementById(source).checked) {
        MAP.showMarkers(source);
        //TIMELINE.addActive(source);
        // TODO move timeline functionality out of here
    } else {
        MAP.hideMarkers(source);
        //TIMELINE.removeActive(source);
    }
  },
};

  /*
     example marker input here:
     add_marker(
     {position: new google.maps.LatLng(42.297276,-71.26462),title:"preschang",icon:"http://maps.google.com/mapfiles/ms/icons/orange-dot.png",map:map},
     {details:"<table><tr><td class='prof_cell'><a href='https://farm4.staticflickr.com/3929/15391622816_6e1b496075.jpg' target='_blank'><img class='prof_img rounded' src='https://farm4.staticflickr.com/3929/15391622816_6e1b496075_t.jpg' /></a></td><td class='data_cell'>[<a href='http://flickr.com/photos/99579729@N06' target='_blank'>preschang</a>] Add #Babson College this week as a member of the #Goldman Sachs 10k small business program. Learning how to be a better #business man!<br /><span class='time'>2014-10-01 12:05:41</span></td></tr></table>"},
     "flickr"
     );
  */

