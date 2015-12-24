$SCRIPT_ROOT = {{ request.script_root|tojson|safe }};

$(function() {
    $('a#calculate').bind('click', function() {
      $.getJSON($SCRIPT_ROOT + '/_add_numbers', {
        a: $('input[name="a"]').val(),
        b: $('input[name="b"]').val()
      }, function(data) {
        $("#result").text(data.result);
      });
      return false;
    });
  });

$(function() {
    function submit_form2(e) {
        $.getJSON("/myjson", {
        page: 2,
        },
        function(data) {
            $('#result5').text(data.posts[0].url);
        });
    };
    // 绑定click事件
    $('#test').bind('click', submit_form);
});


<script src="js/jquery.pagination.js" type="text/javascript"></script>

<script language="javascript" type="text/javascript">
 var pageIndex =0;     //页索引
 var pageSize =20;    //每页显示的条数
    $(function() {
    Init(0);
        $("#Pagination").pagination(<%=pageCount %>, {
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
            type: "POST",
            dataType: "text",
            url: 'SqlPage.aspx',
            data: "pageIndex=" + (pageIndex + 1) + "&pageSize=" + pageSize,
            success: function(data) {
                if(data!=""){
                 $("#tblData tr:gt(0)").remove();//移除所有的数据行
                 data=$.parseJSON(data);
                        $.each(data.News,function(index,news){
                       $("#tblData").append("<tr bgcolor='white'><td>"+news.NewsID+"</td><td algin='left'>"+news.Title+"</td><td>"+news.SmallClassName+"</td><td>"+news.Author+"</td><td>"+news.Updatetime+"</td></tr>");  //将返回的数据追加到表格
                    });
                }
            }
        });

    }
</script>