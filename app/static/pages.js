var pageIndex =0;     //页索引
var pageSize =20;    //每页显示的条数

    $(function() {
    Init(0);
        $("#Pagination").pagination(43, {
             callback: PageCallback,
             prev_text: '上一页',
             next_text: '下一页',
             items_per_page: pageSize,
             num_display_entries: 5,
             current_page: pageIndex,
             num_edge_entries: 1
         });
         function PageCallback(index, jq) {
              Init(index);
         }
    });

    function Init(pageIndex) {
        $.ajax({
            type: "GET",
            dataType: "json",
            url: 'myjson',
            data: "pageIndex=" + (pageIndex + 1) + "&pageSize=" + pageSize,
            success: function(json) {
                if(json!=""){

                 $("#result").text(json.posts[0].product_name);
                 $("#buglist").empty();//移除所有的数据行
                 $.each(json.posts,function(i,item){
                $("#buglist").append(
                    '<tr>'+json.pages+'</tr>'+
                    '<tr>'+
                    '<td><input type="checkbox"></input></td>'+
                    '<td>'+(i+1)+'</td>'+
                    '<td>'+'<a href='+item.url+'>'+item.id+'</a></td>'+
                    '<td>'+item.product_name+'</td>'+
                    '<td>'+item.product_version+'</td>'+
                    '<td>'+item.software_version+'</td>'+
                    '<td>'+item.bug_level+'</td>'+
                    '<td>'+item.bug_show_times+'</td>'+
                    '<td>'+item.bug_title+'</td>'+
                    '<td>'+item.author+'</td>'+
                    '<td>'+item.bug_status+'</td>'+
                    '<td>'+item.bug_owner+'</td>'+
                    '<td>'+item.timestamp+'</td>'+
                    '</tr>');
                    });
                }
            }
        });

    }
