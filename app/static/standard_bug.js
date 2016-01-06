function initPro() {
    var option1 = '';
    $.getJSON("/get_product",function(jsonData) {
    $.each(jsonData, function(index, indexItems) {
        alert(indexItems)
        option1 += "<option id=" + indexItems.name + ">" + indexItems.name + "</option>";
        alert(indexItems.name)
    });
    $("#product_name").append(option1);
    $("#product_name").bind("change", function() {
        selectCity(jsonData);
    })
    });

    function selectCity(data) {
        var option2 = '';
        var option3 = '';
        var selectedIndex = $("#product_name :selected").text();
        $("#product_version").empty();
        if($("#product_name :selected").val() == -1){
            $("#product_version").append("<option id=\"-1\">请选择城市</option>");
        }
        $.each(data, function(index, indexItems) {
        var proName = indexItems.name;
        $.each(indexItems.items, function(index, indexItems) {
        if (indexItems.parentNode != selectedIndex) {
            return;
        } else {
            option2 += "<option id=" + indexItems.name + ">"+ indexItems.name + "</option>";
        }
        })
        });
        $("#selectCity").append(option2);
    };
};

$(function() {
 initPro();
});