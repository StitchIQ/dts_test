$(function() {
    $('a#page1').bind('click', function() {
      $.getJSON($SCRIPT_ROOT + '/myjson', {
        page: $('a[name="page1"]').val(),
      }, function(json) {
        $("#result3").text(json.posts[0].url);
        $('#buglist').empty();
        for(var i=0;i< json.count;i++){
            $('#buglist').append(
            '<tr>'+
            '<td><input type="checkbox"></input></td>'+
            '<td>'+(i+1)+'</td>'+
            '<td>'+'<a href='+json.posts[i].url+'>'+json.posts[i].id+'</a></td>'+
            '<td>'+json.posts[i].product_name+'</td>'+
            '<td>'+json.posts[i].product_version+'</td>'+
            '<td>'+json.posts[i].software_version+'</td>'+
            '<td>'+json.posts[i].bug_level+'</td>'+
            '<td>'+json.posts[i].bug_show_times+'</td>'+
            '<td>'+json.posts[i].bug_title+'</td>'+
            '<td>'+json.posts[i].author+'</td>'+
            '<td>'+json.posts[i].bug_status+'</td>'+
            '<td>'+json.posts[i].bug_owner+'</td>'+
            '<td>'+json.posts[i].timestamp+'</td>'+
            '</tr>');
        }
      });
      return false;
    });
  });


$(function() {
    $('a#calculate2').bind('click', function() {
      $.getJSON($SCRIPT_ROOT + '/myjson?page=2', {
        a: $('input[name="a1"]').val(),
        b: $('input[name="b1"]').val()
      }, function(json) {
        $("#result3").text(json.posts[0].url);
        $('#buglist').empty();
        for(var i=0;i< json.count;i++){
            $('#buglist').append(
            '<tr>'+
            '<td><input type="checkbox"></input></td>'+
            '<td>'+(i+1)+'</td>'+
            '<td>'+'<a href='+json.posts[i].url+'>'+json.posts[i].id+'</a></td>'+
            '<td>'+json.posts[i].product_name+'</td>'+
            '<td>'+json.posts[i].product_version+'</td>'+
            '<td>'+json.posts[i].software_version+'</td>'+
            '<td>'+json.posts[i].bug_level+'</td>'+
            '<td>'+json.posts[i].bug_show_times+'</td>'+
            '<td>'+json.posts[i].bug_title+'</td>'+
            '<td>'+json.posts[i].author+'</td>'+
            '<td>'+json.posts[i].bug_status+'</td>'+
            '<td>'+json.posts[i].bug_owner+'</td>'+
            '<td>'+json.posts[i].timestamp+'</td>'+
            '</tr>');
        }
      });
      return false;
    });
  });


$.getJSON("/myjson", function(json){
  alert("JSON Data count: " + json.pages);
  alert("JSON Data: " + json.posts[0].author);
  $("#result").text(json.posts[0].product_name);
  for(var i=0;i< json.count;i++){
    $('#buglist').append(
    '<tr>'+
    '<td><input type="checkbox"></input></td>'+
    '<td>'+(i+1)+'</td>'+
    '<td>'+'<a href='+json.posts[i].url+'>'+json.posts[i].id+'</a></td>'+
    '<td>'+json.posts[i].product_name+'</td>'+
    '<td>'+json.posts[i].product_version+'</td>'+
    '<td>'+json.posts[i].software_version+'</td>'+
    '<td>'+json.posts[i].bug_level+'</td>'+
    '<td>'+json.posts[i].bug_show_times+'</td>'+
    '<td>'+json.posts[i].bug_title+'</td>'+
    '<td>'+json.posts[i].author+'</td>'+
    '<td>'+json.posts[i].bug_status+'</td>'+
    '<td>'+json.posts[i].bug_owner+'</td>'+
    '<td>'+json.posts[i].timestamp+'</td>'+
    '</tr>');
}
});


