$(document).ready(function(){

    $('#id_extend_same_result').on('change', function() {
        if ( $('#id_extend_same_result').is(':checked')){
            $('.extend_result_fields').show();
            }         
        else {
            $('.extend_result_fields').hide();
            }
    });

});
