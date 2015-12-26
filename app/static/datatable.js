$(document).ready(function() {
        $("#datatable").dataTable({
            "processing": true,
            "serverSide": true,
            "bFilter": true,
            "ordering": true,
            "ajax" : "myjson2",
            "columns": [
                {"data": "id", "orderSequence": [ "asc" ]},
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
                {"data": "author"},
                {"data": "bug_status"},
                {"data": "bug_owner"},
                {"data": "timestamp"}
            ],
            "pagingType": "full_numbers",


        });
    });


