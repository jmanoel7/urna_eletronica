$(document).ready(function(){
    var base = '_';
    $("#dig1").click(function(){
        if ( $('#num1').text() == base ) {
            $('#num1').text( $('#dig1').text() );
            $('#num1').removeClass('pisca');
            $('#num2').text( base );
            $('#num2').addClass('pisca');
        } 
    });
});