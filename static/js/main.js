$(document).ready( function() {
  // set up facebox, the overlay library
  $.facebox.settings.closeImage = GLOBAL.faceboxCloseImage;
  $.facebox.settings.loadingImage = GLOBAL.faceboxLoadingImage;
  $('a[rel*=facebox]').facebox();
  $('#delete-location').on('click', deleteLocation);
});

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

function newLocationSuccess(d) {
  var message = "Success! " + d.message;
  $("#facebox .content").append(message);
  $("#facebox .content").append("<br>It will take a minute or two to get data for this new location; it will appear on a refresh.");
}

function newLocationFail(d) {
  var message = "Failure. " + d.message;
  $("#facebox .content").append(message);
}

function deleteLocation(e) {
  event.preventDefault();
  var csrftoken = getCookie('csrftoken');

  $.ajax({
    url: './delete/',
    headers: {"X-CSRFToken":csrftoken},
    type: "POST",
    data: {},
    success: deleteLocationSuccess,
    error: deleteLocationFail
  });
}

function deleteLocationSuccess(d) {
  $("#delete-location").html("Location Removed");
  // remove the click handler
  $("#delete-location").off();
}

function deleteLocationFail(d) {
  console.log(d);
}

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
