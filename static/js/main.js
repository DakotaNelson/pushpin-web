$(document).ready( function() {
  // set up facebox, the overlay library
  $.facebox.settings.closeImage = GLOBAL.faceboxCloseImage;
  $.facebox.settings.loadingImage = GLOBAL.faceboxLoadingImage;
  $('a[rel*=facebox]').facebox();
  $('.delete-location').on('click', deleteLocation);
  $("img.lazy").lazyload({
                  failure_limit: 20,
                  threshold: 200,
                  effect: "fadeIn"
  });

  BACKEND.getData();
  LOCATIONS.onLoad();
});

/* Called when data has been fetched to initialize all elements that need the data.
 */
function initializeAll(pins,loc) {
  MAP.createMap(loc.lat,
                loc.lon,
                loc.rad,
                14, // zoom level
                pins
               ); // creates the map

  //TIMELINE.createTimeline(pins); // creates the d3.js timeline
  // TODO what to do with this
}

/* Called when the submit button on the new location form is clicked.
 */
function newLocationSubmit(e) {
  event.preventDefault();
  BACKEND.addLocation(newLocationSuccess, newLocationFail);
}

/* Callback if the new location request succeeds. Updates the locations module.
 */
function newLocationSuccess(d) {
  if(d.result === "failed") {
    var message = d.message;
  }
  else{
    var message = "Success! " + d.message;
    message += "<br>It will take a minute or two to get data for this new location; it will appear on a refresh.";
  }
  $("#facebox #result-message").html(message);

  LOCATIONS.update();

  setTimeout(function() { $.facebox.close; }, 2000);
  return false;
}

/* Callback if the new location request fails. Displays error message.
 */
function newLocationFail(d) {
  console.log(d);
  var message = "Server error. Sorry about that. Refresh and try again?"
  $("#facebox #result-message").html(message);
}

/* Fires when the "delete location" button is clicked
 */
function deleteLocation(e) {
  event.preventDefault();
  BACKEND.deleteLocation(deleteLocationSuccess, deleteLocationFail);
}

/* Callback upon successful removal of a location
 */
function deleteLocationSuccess(d) {
  //$("#delete-location").html("Location Removed");
  // remove the click handler
  //$("#delete-location").off();
  LOCATIONS.update();
  window.location = '/'
}

function deleteLocationFail(d) {
  console.log(d);
}

/* Used to grab CSRF cookies
 */
function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie != '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
      var cookie = jQuery.trim(cookies[i]);
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) == (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
