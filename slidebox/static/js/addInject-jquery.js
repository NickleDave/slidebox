$(document).ready(function(){

//    $('#id_animalID').keyup(function() {
//        var IDstring = $(this).val();
//        $.get(
//    }

    $('#id_injectionMethod').on('change', function() {
        if ( $('#id_injectionMethod').val() == ""){
            $('.option_1_fields').hide();
            $('.option_2_fields').hide();
            }         
        else if ( $('#id_injectionMethod').val() == "1"){
            $('.option_1_fields').show();
            $('.option_2_fields').hide();
            }
        else if ( $('#id_injectionMethod').val() == "2"){
            $('.option_2_fields').show();
            $('.option_1_fields').hide();
            }
    });

});
