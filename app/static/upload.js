
$("#attachment").change(function(){
    //var form_data = new FormData($('#form1')[0]);
    //form_data.append('bugs_id', $('#bugs_id').val());
    var form_data = new FormData();
    form_data.append('bugs_id',$('#bugs_id').val());
    form_data.append('attachment',$('#attachment')[0].files[0]);
    //alert($("#bugs_id").val());
    //alert(form_data);
    //$('#form1')是个list，所以要得到form必须用下标取
    $.ajax({
        url: '/upload',
        type: 'POST',
        data: form_data,
        contentType: false,
        processData: false,
        success: function(fileinfo){
            ss = '<p><span id=' + fileinfo.symlink + '>' +
                 '<input type="text" class="form-control" name=' +
                 fileinfo.filename + ' value='+fileinfo.filename +
                 ' readonly="readonly">' +
                 '<a href=#' + fileinfo.filehash + ' name='+ fileinfo.filehash +
                    '>删除</a></span>' +
                 '</p>'

            $('#attachmentdiv').append(ss)
        },
        error: function(){
            alert("该文件无法上传。文件大小超过 16M！");
        },
    });
});

$("#attachmentdiv").delegate("a","click",function(){
    //$("p").append('click');
    alert($(this).attr('name'));
    $.ajax({
        url: '/delete/'+$(this).attr('name'),
        type: 'get',
        //data: $(this).attr('id'),
        contentType: false,
        processData: false,
        success: function(){
            alert('rmmmmmm');

        },
    });
    $(this).parent().remove();

});