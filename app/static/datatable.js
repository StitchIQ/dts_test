$(document).ready(function() {
        $("#datatable").dataTable({
            initComplete: function () {
                    var api = this.api();
                    api.columns().indexes().flatten().each( function ( i ) {
                        var column = api.column( i );
                        var select = $('<select><option value=""></option></select>')
                            .appendTo( $(column.footer()).empty() )
                            .on( 'change', function () {
                                var val = $.fn.dataTable.util.escapeRegex(
                                    $(this).val()
                                );
                                column
                                    .search( val ? '^'+val+'$' : '', true, false )
                                    .draw();
                            } );
                        column.data().unique().sort().each( function ( d, j ) {
                            select.append( '<option value="'+d+'">'+d+'</option>' )
                        } );
                    } );
                },


            "processing": true,
            "serverSide": true,
            "Filter": true,
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
            "aaSorting": [[ 1, "desc" ]],
            "pagingType": "full_numbers",
            "sScrollX": "100%",
            "sScrollXInner": "110%",
            "bScrollCollapse": true
        });




    });


