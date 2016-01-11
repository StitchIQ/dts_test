function initPro() {
    var option1 = "<option id=-1>-----</option>";
    $.getJSON("/get_product",function(jsonData) {
    $.each(jsonData, function(index, indexItems) {
        option1 += "<option id=" + indexItems.name + ">" + indexItems.name + "</option>";
        //alert(indexItems.name)
    });
    $("#product_name").append(option1);
    $("#product_name").bind("change", function() {
        $("#product_name :selected").text()
        selectSoftware($("#product_name :selected").text());
    })
    });

    function selectSoftware(data) {
        var option2 = "<option id=-1>-----</option>";
        var selectedIndex = $("#product_name :selected").text();

        $("#product_version").empty();
        if($("#product_name :selected").val == -1){
            option2 = "<option id=-1>-----</option>";
            return;
        };
        $.getJSON("/get_software",{
            product: data,
            },function(jsonData) {
        $.each(jsonData, function(index, indexItems) {
            option2 += "<option id=" + indexItems.name + ">" + indexItems.name + "</option>";
                //alert(indexItems.name)
        });
        $("#product_version").append(option2);
        $("#product_version").bind("change", function() {
            $("#product_version :selected").text()
            selectVersion($("#product_version :selected").text());
        })
        });
    };

    //此处有bug，选择第一级菜单，会导致此函数执行多次
    function selectVersion(data) {
        var option3 = "";
        option3 = "<option id=-1>-----</option>";
        var selectedIndex = $("#product_version :selected").text();

        $("#software_version").empty();
        if($("#product_version :selected").val == -1){
            option3 = "<option id=-1>-----</option>";
            return;
        };

        $.getJSON("/get_version",{
            version: data,
            },function(jsonData) {
        $.each(jsonData, function(index, indexItems) {
            option3 += "<option id=" + indexItems.name + ">" + indexItems.name + "</option>";
                //alert(indexItems.name)
        });
        $("#software_version").empty();
        $("#software_version").append(option3);
        });
    };

};

$(function() {
 initPro();
});