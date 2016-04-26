<script>
$('#bug_owner_id').autocomplete({
    serviceUrl: '/autocomplete',
    dataType: 'json',
    deferRequestBy:300,
    minChars: 2,
    lookupLimit:10,
    autoSelectFirst:true,
    onSelect: function (suggestion) {
        //alert('You selected: ' + suggestion.value + ', ' + suggestion.data);
    }
});
</script>