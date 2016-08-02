$("#table").on("click", "button#usermodify", function(){
    //给tbody元素，所有tr添加事件
    //获取当前点击的元素
    var pic = $(this);
    console.log(pic.val());
    var r=confirm("确认修改人员权限 ？")
    if (r == false){ return };
    $.post(pic.attr("name"),{
            manager:pic.val()
        },
        function(data){
            console.log(data.status);
            if(data.status == 'ADMINISTER'){
                //console.log(pic.parents("tr"));
                //console.log(pic.parents("td").prev().children().addClass("btn btn-danger"));
                //console.log(pic.parents("td").next());
                pic.removeClass();
                pic.addClass("btn btn-success");
                pic.val(data.status);
                pic.text("普通用户");
            }
            if(data.status == 'default'){
                pic.removeClass();
                pic.addClass("btn btn-danger");
                pic.text("管理员");
                pic.val(data.status);
            }
        }
    ).error(function() { alert("修改失败！"); });
});


$("#table").on("click", "button#modify", function(){
    //给tbody元素，所有tr添加事件
    //修改bug状态，设置禁止的bug不在显示
    //获取当前点击的元素
    var pic = $(this);
    //var lable_status = pic.parents("td").prev().children();
    console.log(pic.val());
    $.post(pic.attr("name"),{
            manager:pic.val()
        },
        function(data){
            console.log(data.status);
            if(data.status == '0'){
                //console.log(pic.parents("tr"));
                //console.log(pic.parents("td").prev().children().addClass("btn btn-danger"));
                //console.log(pic.parents("td").next());
                pic.removeClass();
                pic.addClass("btn btn-success");
                pic.val(data.status);
                pic.text("正常");
            }
            else{
                pic.removeClass();
                pic.addClass("btn btn-danger");
                pic.text("锁定");
                pic.val(data.status);
            }
        }
    ).error(function() { alert("修改失败！"); });
});


$("#table").on("click", "button#delete", function(){
    //给tbody元素，所有tr添加事件
    //修改bug状态，设置禁止的bug不在显示
    //获取当前点击的元素
    var pic = $(this);
    var lable_status = pic.parents("tr").find("td:eq(2)").text();
    console.log(lable_status);
    var r=confirm("删除后无法恢复！确认删除 ？")
    console.log(r);
    if (r == true){
        $.post(pic.attr("name"),
            function(data){
                console.log(data.status);
                //console.log(pic.parents("tr"));
                pic.parents("tr").remove();
                //alert("删除成功");
            }
        ).error(function() { alert("修改失败！"); });
    };
});