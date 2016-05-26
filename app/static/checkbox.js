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