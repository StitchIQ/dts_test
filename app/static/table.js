
$(function() {
    $('a#calculate').bind('click', function() {
      $.getJSON($SCRIPT_ROOT + '/_add_numbers', {
        a: $('input[name="a1"]').val(),
        b: $('input[name="b1"]').val()
      }, function(data) {
        $("#result").text(data.result);
      });
      return false;
    });
  });

$(function() {
    function submit_form(e) {
        $.getJSON($SCRIPT_ROOT + '/add', {
            a: $('input[name="a"]').val(),
            b: $('input[name="b"]').val(),
            now: new Date().getTime()
        },
        function(data) {
            $('#result5').text(data.result);

        });
    };
    // 绑定click事件
    $('#test').bind('click', submit_form);
});

$(function() {
    function submit_form2(e) {
        $.getJSON($SCRIPT_ROOT + '/myjson', {
            a: $('input[name="a"]').val(),
            b: $('input[name="b"]').val(),
            now: new Date().getTime()
        },
        function(data) {
            $("#clients_list").dataTable({
             serverSide: true,
             processing: true,
             ajax: "/api/v1/overtime",
             columns: [
                 {
                     data: "author", 'render': function (data, type, full, meta) {
                     return '<div class="text-right">' + Math.round(data * 10) / 10 + '</div>';
                 }
                 },
                 {
                     data: "bug_descrit", 'render': function (data, type, full, meta) {
                     return '<div class="text-right">' + Math.round(data * 10) / 10 + '</div>';
                 }
                 },
                 {
                     data: "bug_level", 'render': function (data, type, full, meta) {
                     return '<div class="text-right">' + Math.round(data * 10) / 10 + '</div>';
                 }
                 },
                 {
                     data: "bug_show_times", 'render': function (data, type, full, meta) {
                     return '<div class="text-right">' + Math.round(data * 10) / 10 + '</div>';
                 }
                 },
                 {
                     data: "bug_title", 'render': function (data, type, full, meta) {
                     return '<div class="text-right">' + Math.round(data * 100) / 100 + '</div>';
                 }
                 },
                 {
                     data: "timestamp", 'render': function (data, type, full, meta) {
                     return '<div class="text-right">' + Math.round(data * 10) / 10 + '</div>';
                 }
                 }
                {
                     data: "url", 'render': function (data, type, full, meta) {
                     return '<div class="text-right">' + Math.round(data * 10) / 10 + '</div>';
                 }
                 }
             ],
             "paging": true,
             "lengthChange": false,
             "searching": false,
             "ordering": true,
             "info": true,
             "autoWidth": true,
             language: {
                 "sProcessing": "处理中...",
                 "sLengthMenu": "显示 _MENU_ 项结果",
                 "sZeroRecords": "没有匹配结果",
                 "sInfo": "显示第 _START_ 至 _END_ 项结果，共 _TOTAL_ 项",
                 "sInfoEmpty": "显示第 0 至 0 项结果，共 0 项",
                 "sInfoFiltered": "(由 _MAX_ 项结果过滤)",
                 "sInfoPostFix": "",
                 "sSearch": "搜索:",
                 "sUrl": "",
                 "sEmptyTable": "表中数据为空",
                 "sLoadingRecords": "载入中...",
                 "sInfoThousands": ",",
                 "oPaginate": {
                     "sFirst": "首页",
                     "sPrevious": "上页",
                     "sNext": "下页",
                     "sLast": "末页"
                 },
                 "oAria": {
                     "sSortAscending": ": 以升序排列此列",
                     "sSortDescending": ": 以降序排列此列"
                 }
             }
         });

        });
     };
    // 绑定click事件
    $('#get_json').bind('click', submit_form2);
});
