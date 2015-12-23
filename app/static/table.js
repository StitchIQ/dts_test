
$(function() {
    $('a#calculate').bind('click', function() {
      $.getJSON($SCRIPT_ROOT + '/_add_numbers', {
        a: $('input[name="a1"]').val(),
        b: $('input[name="b1"]').val()
      }, function(data) {
        $("#result").text(data.result);
      });
      return false;
    });
  });

$(function() {
    function submit_form(e) {
        $.getJSON($SCRIPT_ROOT + '/add', {
            a: $('input[name="a"]').val(),
            b: $('input[name="b"]').val(),
            now: new Date().getTime()
        },
        function(data) {
            $('#result5').text(data.result);

        });
    };
    // 绑定click事件
    $('#test').bind('click', submit_form);
});

$.getJSON("/myjson", function(json){
  alert("JSON Data: " + json.next);
  alert("JSON Data: " + json.posts[0].author);
  $("#result").text(json.posts[0].bug_descrit);
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

