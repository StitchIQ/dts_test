
$(document).ready(function () {
    //要请求的一级机构JSON获取页面
    var url="/get_product";
    $.getJSON(url,function (data) {
        alert(data);
        //对请求返回的JSON格式进行分解加载
        $(data).each(function () {
            $("#product_name").append($("<option/>").text(this.name).attr("value",this.id));
            alert(this.name);
        });
    });

        //一级下拉联动二级下拉

        $("#product_name").change(function () {

            //清除二级下拉列表

            $("#product_version").empty();

            $("#product_version").append($("<option/>").text("--请选择--").attr("value","-1"));

            //要请求的二级下拉JSON获取页面

            var url="/get_software";

            //将选中的一级下拉列表项的id传过去

            $.getJSON(url, { id:$(this).attr("value") },function (data) {

                //对请求返回的JSON格式进行分解加载

                $(data).each(function () {

                    $("#product_version").append($("<option/>").text(this.name).attr("value",this.id));

                });

            });

        });

    //二级下拉联动三级下拉

    $("#product_version").change(function () {

        //清除三级下拉列表

        $("#software_version").empty();

        $("#software_version").append($("<option/>").text("--请选择--").attr("value","-1"));

        //要请求的三级下拉JSON获取页面

        var url="/get_version";

        //将选择的二级下拉列表项的id传过去

        $.getJSON(url, { id:$(this).attr("value") },function (data) {

            //对请求返回的JSON格式进行分解加载

            $(data).each(function () {

                $("#software_version").append($("<option/>").text(this.name).attr("value",this.id));

            });

        });

    });

});
