$(document).ready( function() {
  // calls the init function in the embedded js on the page
  // this is a dirty hack, TODO
  init();

  // creates the media table
  $('#media').DataTable( {
    'autoWidth': true,
    'paging': true,
    'lengthMenu':  [ [10, 25, 50, 100, -1], [10, 25, 50, 100, "All"] ],
    'scrollX': false,
    'scrollY': $(document).height()-200,
    'scrollCollapse': true,
    'data':window.cleanData,
    'order': [3, 'desc'],
    'columns': [
      { name: 'image',
        title: 'Image',
        data: 'thumb_url',
        render: function(d, type, full, meta){
          var a_open = "<a href='" + full.media_url + "' target='_blank'>";
          var image = "<img class='prof_img rounded' src='" + d +"' />";
          var a_close = "</a>";
          return a_open + image + a_close;
        }
      },
      { name: 'name',
        title: 'Username',
        data: 'profile_name',
        render: function(d, type, full, meta){
          var a_open = "<a href='" + full.profile_url + "' target='_blank'>";
          var a_close = "</a>";
          return a_open + d + a_close;
        }
      },
      { name: 'message',
        title: 'Content',
        data: 'message',
      },
      { name: 'source',
        title: 'Source',
        data: 'source',
      },
      { name: 'date',
        title: 'Created',
        data: 'date',
        type: 'date',
        render: function(data, type, full, meta){
          if(type == "display"){
            var date = new Date(data);
            var options = {year: "numeric", month: "short", day: "numeric", hour:"numeric", minute:"numeric"};
            return date.toLocaleString('en-US',options);
          }
          return data;
        }
      }
    ],
  });
});
