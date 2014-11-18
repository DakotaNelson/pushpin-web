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
  console.log(d);
  console.log("VICTORY!");
}

function newLocationFail(d) {
  console.log(d);
  console.log("FAILURE.");
}
