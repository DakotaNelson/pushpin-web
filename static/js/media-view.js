$(document).ready( function() {
  $('#media-table').searchable({
    selector: 'tbody tr',
    childSelector: 'td',
    searchField: '#media-search',
  });
});
