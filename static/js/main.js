$(document).ready( function() {
  // set up facebox, the overlay library
  $.facebox.settings.closeImage = GLOBAL.faceboxCloseImage;
  $.facebox.settings.loadingImage = GLOBAL.faceboxLoadingImage;
  $('a[rel*=facebox]').facebox();
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
}

function newLocationFail(d) {
  var message = "Failure. " + d.message;
  $("#facebox .content").append(message);
}
