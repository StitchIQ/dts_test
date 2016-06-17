
$("#submit").click(function(){
    var  arr  = [];
    $("tbody tr").each(function(){
        if($(this).hasClass('selected')){
            var text = $(this).children("td:nth-child(3)").text();
            arr.push(text);
        }
    })
    if(arr.length == 0){
        alert("请至少选择一行数据！");
        return 0;
    };
    //console.log(JSON.stringify(arr));
    $.ajax({
        url: '/daochu',
        type: 'POST',
        data: JSON.stringify(arr),
        contentType: 'application/json',
        dataType: 'json',
        processData: false,
        success: function(fileinfo){
            //alert(fileinfo.filename);
            window.open("/daochu2/"+fileinfo.filename,"_blank");
        },
        error: function(){
            alert("该文件大小超过 16M！");
        },
    });
})