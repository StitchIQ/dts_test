$(document).ready(function() {
        var t = $("#datatable").DataTable({
            initComplete: function () {
                var api = this.api();
                api.columns().indexes().flatten().each( function ( i ) {
                    var column = api.column( i );
                    var select = $('<select><option value=""></option></select>')
                        .appendTo( $(column.header()).empty() )
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
            //"serverSide": true,
            "Filter": true,
            "search": true,
            "ordering": true,
            "ajax" : "myjson2",
            "columns": [
                {"data":"id", 'render':function(data, type, full, meat){
                    return '<input type="checkbox"></input>'
                }
                },
                {"data": "id"},
                {"data": "id","searchable":true},
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
            "bScrollCollapse": true,


            "columnDefs": [{
                // "visible": false,
                //"targets": 0
            },
            {
                "render": function(data, type, row, meta) {
                    //渲染 把数据源中的标题和url组成超链接
                    return '<a href="bug_process/' + data + '" target="_blank">' + row.id + '</a>';
                },
                //指定是第三列
                "targets": 2
            }]
        });
        //前台添加序号
        t.on('order.dt search.dt',
        function() {
            t.column(1, {
                "search": 'applied',
                "order": 'applied'
            }).nodes().each(function(cell, i) {
                cell.innerHTML = i + 1;
            });
        }).draw();
    });


