$(function(){
   $("#bug_owner_id").blur(function(){
        $.get("check_user",{
            username:$("#bug_owner_id").val()
        },function(data,status){
            if(status != '0'){
                $("#result").text(data);
                alert(data);
            }
            else{
            $("#result").text(data);
            alert('NOT');
            alert(data);
            };

        });
    });
});

  $(function() {
    $('a#calculate').bind('click', function() {
      $.getJSON('/_add_numbers', {
        a: $('input[name="a"]').val(),
        b: $('input[name="b"]').val()
      }, function(data) {
        $("#result").text(data.result);
      });
      return false;
    });
  });


