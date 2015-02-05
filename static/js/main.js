$(document).ready( function() {
  // set up facebox, the overlay library
  $.facebox.settings.closeImage = GLOBAL.faceboxCloseImage;
  $.facebox.settings.loadingImage = GLOBAL.faceboxLoadingImage;
  $('a[rel*=facebox]').facebox();
  $('#delete-location').on('click', deleteLocation);

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

  TIMELINE.createTimeline(pins); // creates the d3.js timeline
}

/* Called when the submit button on the new location form is clicked.
 */
function newLocationSubmit(e) {
  event.preventDefault();
  $.ajax({
    url: $(event.srcElement).attr('action'),
    type: "POST",
    data: $(event.srcElement).serialize(),
    success: newLocationSuccess,
    error: newLocationFail
  });
  return false;
}

/* Callback if the new location request succeeds. Updates the locations module.
 */
function newLocationSuccess(d) {
  var message = "Success! " + d.message;
  $("#facebox .content").append(message);
  $("#facebox .content").append("<br>It will take a minute or two to get data for this new location; it will appear on a refresh.");

  LOCATIONS.update();

  setTimeout(function() { $.facebox.close; }, 2000);
  return false;
}

/* Callback if the new location request fails. Displays error message.
 */
function newLocationFail(d) {
  var message = "Failure. " + d.message;
  $("#facebox .content").append(message);
}

/* Fires when the "delete location" button is clicked
 */
function deleteLocation(e) {
  event.preventDefault();
  var csrftoken = getCookie('csrftoken');

  $.ajax({
    url: window.location.pathname + '/delete/',
    headers: {"X-CSRFToken":csrftoken},
    type: "POST",
    data: {},
    success: deleteLocationSuccess,
    error: deleteLocationFail
  });
}

/* Callback upon successful removal of a location
 */
function deleteLocationSuccess(d) {
  $("#delete-location").html("Location Removed");
  // remove the click handler
  $("#delete-location").off();
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
