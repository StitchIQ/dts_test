
$("#table").on("click", "button.btn-warning", function(){
    //给tbody元素，所有tr添加事件
    //修改bug状态，设置禁止的bug不在显示
    //获取当前点击的元素
    var pic = $(this);
    var lable_status = pic.parents("td").prev().children();
    console.log(lable_status.val());
    $.post(pic.attr("name"),{
            manager:lable_status.val()
        },
        function(data){
            console.log(data.status);
            if(data.status == '0'){
                //console.log(pic.parents("tr"));
                //console.log(pic.parents("td").prev().children().addClass("btn btn-danger"));
                //console.log(pic.parents("td").next());
                lable_status.removeClass();
                lable_status.addClass("btn btn-success");
                lable_status.val(data.status);
                lable_status.text("正常");
            }
            else{
                lable_status.removeClass();
                lable_status.addClass("btn btn-danger");
                lable_status.text("锁定");
                lable_status.val(data.status);
            }
        }
    ).error(function() { alert("修改失败！"); });
});


$("#table").on("click", "button#delete", function(){
    //给tbody元素，所有tr添加事件
    //修改bug状态，设置禁止的bug不在显示
    //获取当前点击的元素
    var pic = $(this);
    var lable_status = pic.parents("td").prev().children();
    console.log(lable_status.val());
    $.post(pic.attr("name"),{
            manager:lable_status.val()
        },
        function(data){
            console.log(data.status);
            console.log(pic.parents("tr"));
            pic.parents("tr").remove();
            //alert("删除成功");
        }
    ).error(function() { alert("修改失败！"); });
});