var MAP = {
  map: null,
  markers: [],
  lat: null,
  lon: null,
  center: null, // lat/lon as a google LatLng object
  radius: null,
  data: null,
  icon: {
           'Twitter':"http://maps.google.com/mapfiles/ms/icons/blue-dot.png",
           'Flickr':"http://maps.google.com/mapfiles/ms/icons/orange-dot.png"
        },
  elementId: 'map',

  createMap: function(lat,lon,radius,data) {
    MAP.lat = lat;
    MAP.lon = lon;
    MAP.radius = radius;

    MAP.data = data;

    MAP.renderMap();
  },

  renderMap: function() {
    MAP.center = new google.maps.LatLng(MAP.lat,MAP.lon);

    var mapOptions = {
        zoom: 15,
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

    MAP.data.forEach(function(pin) {
      MAP.addMarker({position: new google.maps.LatLng(pin.latitude, pin.longitude) , title: pin.screen_name, icon: MAP.icon[pin.source] , map:MAP.map}, {details: pin.message}, pin.source);
      // TODO fill out details in to HTML template
    });
    MAP.showMarkers('Twitter');

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
    for (var i = 0; i < window[source].length; i++) {
        MAP.marker[source][i].setMap(place);
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
        TIMELINE.addActive(source);
        // TODO move timeline functionality out of here
    } else {
        MAP.hideMarkers(source);
        TIMELINE.removeActive(source);
    }
  },
};
