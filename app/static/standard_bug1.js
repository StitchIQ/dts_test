
$(document).ready(function () {
    //要请求的一级机构JSON获取页面
    var url="/get_product";
    $.getJSON(url, function (data) {
        //alert(data);
        //对请求返回的JSON格式进行分解加载
        //$("#product_name").append($("<option/>").text("--请选择 产品名称--").attr("value","-1"));
        //$("#product_version").append($("<option/>").text("--请选择 产品版本--").attr("value","-1"));
       // $("#software_version").append($("<option/>").text("--请选择 软件版本--").attr("value","-1"));
        //$("#version_features").append($("<option/>").text("--请选择 软件特性--").attr("value","-1"));
        //alert(data.product_info[0].name);

        $.each(data.product_info, function (i,item) {
            //alert(item.name);
            //$("#product_name").append($("<option/>").text(item.name).attr("value",item.name));
            //alert(this.name);
        });
    });

        //一级下拉联动二级下拉
        var temp = "";
        var temp2 = "";
        $("#product_name").change(function () {

            //清除二级下拉列表
            $("#product_version").empty();
            $("#product_version").append($("<option/>").text("--请选择--").attr("value","-1"));
            //清除三级下拉列表
            $("#software_version").empty();
            $("#software_version").append($("<option/>").text("--请选择--").attr("value","-1"));
            $("#version_features").empty();
            $("#version_features").append($("<option/>").text("--请选择--").attr("value","-1"));

            //要请求的二级下拉JSON获取页面
            //将选中的一级下拉列表项的id传过去
            $.getJSON("/get_software", { product:$("#product_name :selected").text() },function (data) {

            //对请求返回的JSON格式进行分解加载
            //alert(data.soft_info[0].software);
            temp = data;
            $(data.soft_info).each(function () {
                //alert(this.software);
                $("#product_version").append($("<option/>").text(this.software).attr("value",this.software));
            });

            });
        });

    //二级下拉联动三级下拉
    $("#product_version").change(function () {

        //清除三级下拉列表
        $("#software_version").empty();
        $("#software_version").append($("<option/>").text("--请选择--").attr("value","-1"));
        $("#version_features").empty();
        $("#version_features").append($("<option/>").text("--请选择--").attr("value","-1"));
        //要请求的三级下拉JSON获取页面
        $(temp.soft_info).each(function () {
                //alert(this.software);
                if(this.software == $("#product_version :selected").text()){
                    $.each((this.version.split(";")),function (i,item) {
                        //alert(item);
                        $("#software_version").append($("<option/>").text(item).attr("value", item));
                    });
                    $.each((this.features.split(";")),function (i,item) {
                        //alert(item);
                        $("#version_features").append($("<option/>").text(item).attr("value", item));
                    });
                    //$("#software_version").append($("<option/>").text(this.software).attr("value",this.index));
                };
        });

        /*
        var url="/get_version";
        //将选择的二级下拉列表项的id传过去
        alert($("#product_version:selected").text());
        $.getJSON(url, { version:$("#product_version :selected").text() },function (data) {
            //对请求返回的JSON格式进行分解加载
            $(data).each(function () {
                $("#software_version").append($("<option/>").text(this.name).attr("value",this.id));
            });
        });*/
    });

});
