$(function(){
   $("#bug_owner_id").blur(function(){
        $.get("check_user",{
            username:$("#bug_owner_id").val()
        },function(data,status){
            if(data == 'Not Found'){
                alert("输入的邮件地址找不到");
            };
        });
    });
});


