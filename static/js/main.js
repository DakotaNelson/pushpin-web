$(document).ready( function() {
  // set up facebox, the overlay library
  $.facebox.settings.closeImage = GLOBAL.faceboxCloseImage;
  $.facebox.settings.loadingImage = GLOBAL.faceboxLoadingImage;
  $('a[rel*=facebox]').facebox();
});
