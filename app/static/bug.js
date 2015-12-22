$("#clients_list").dataTable({
    serverSide: true,
    processing: true,
    ajax: "/api/v1/overtime",
    columns: [
     {
         data: "overtime_total", 'render': function (data, type, full, meta) {
         return '<div class="text-right">' + Math.round(data * 10) / 10 + '</div>';
     }
     },
     {
         data: "overtime_avail", 'render': function (data, type, full, meta) {
         return '<div class="text-right">' + Math.round(data * 10) / 10 + '</div>';
     }
     },
     {
         data: "overtime_holiday", 'render': function (data, type, full, meta) {
         return '<div class="text-right">' + Math.round(data * 10) / 10 + '</div>';
     }
     },
     {
         data: "overtime_expense", 'render': function (data, type, full, meta) {
         return '<div class="text-right">' + Math.round(data * 10) / 10 + '</div>';
     }
     },
     {
         data: "overtime_shared", 'render': function (data, type, full, meta) {
         return '<div class="text-right">' + Math.round(data * 100) / 100 + '</div>';
     }
     },
     {
         data: "invoice_lack_amount", 'render': function (data, type, full, meta) {
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