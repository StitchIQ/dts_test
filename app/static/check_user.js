$(function(){
   $("#bug_owner_id").blur(function(){
        $.get("/check_user",{
            username:$("#bug_owner_id").val()
        },function(data,status){
            if(data == 'Not Found'){
                //$("#bug_owner_id").append("<p>This field is required.</p>");
                $("#bug_owner_id").parent().css({"color":"red","border":"2px solid red"})
                //alert($("#bug_owner_id").html());
            }
            else
            {
                //alert($("#bug_owner_id").html());
                $("#bug_owner_id").parent().css({"color":"#555555","border":"0px solid #cccccc"});
            }
        });
    });
});


