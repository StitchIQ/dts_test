$(document).ready(function() {
        $("#datatable").dataTable({
            "processing": true,
            "serverSide": true,
            "bFilter": true,
            "ordering": true,
            "ajax" : "myjson2",
            "columns": [
                {"data":"id", 'render':function(data, type, full, meat){
                    return '<input type="checkbox"></input>'
                }
                },
                {"data": "id", "bSortable": true},
                {
                    "data": "url",'render': function (data, type, full, meta) {
                     return '<a herf="' + data +'">'+"id"+'</a>';
                 }},
                {"data": "product_name"},
                {"data": "product_version"},
                {"data": "software_version"},
                {"data": "bug_level"},
                {"data": "bug_show_times"},
                {"data": "bug_title"},
                {"data": "user_name"},
                {"data": "bug_status"},
                {"data": "bug_owner_id"},
                {"data": "timestamp"}
            ],
            "pagingType": "full_numbers",


        });
    });


