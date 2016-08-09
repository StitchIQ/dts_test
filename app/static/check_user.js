$(function(){
   $("#bug_owner_id").blur(function(){
        var reg = /^\w+((-\w+)|(\.\w+))*\@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z0-9]+$/;
        if (reg.test($("#bug_owner_id").val())){
            $.ajax({
                url: "/check_user",
                type: 'GET',
                data: {username:$("#bug_owner_id").val()},
                success: function(response,status,xhr){
                    console.log(status);
                    console.log(response);
                    console.log(xhr);

                    $("#bug_owner_id").parent().css({"color":"#555555","border":"0px solid #cccccc"});
                },
                error: function(){
                    $("#bug_owner_id").parent().css({"color":"red","border":"2px solid red"})
                    alert("邮箱地址未找到，请检查");
                },
            });
        }
        else{alert("邮箱地址不正确，请检查");}
    });
});


