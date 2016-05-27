<script type="text/javascript">
    $(function(){
        $('tbody>tr').click(function(){
            if($(this).hasClass('selected')){
                $(this).removeClass('selected').find(':checkbox').attr('checked',false);
            }else{
                $(this).addClass('selected').find(':checkbox').attr('checked',true);
            }
        })
    })
</script>

$(function(){
    $("#all").click(function(){
        $('[name=items]:checkbox').attr("checked",true);
    })
    $("#no").click(function(){
        $('[name=items]:checkbox').attr("checked",false);
    })
    $("#other").click(function(){
        $('[name=items]:checkbox').each(function(){
        this.checked=!this.checked;
        });
    })
    $("#submit").click(function(){
        var send="选中了："
        $('[name=items]:checkbox:checked').each(function(){
            send+=$(this).val();
        });
        alert(send);
    })
})