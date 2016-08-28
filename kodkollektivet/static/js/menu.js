$(document).ready(function(){
    $(".menu-button a").click(function(){
        $(".menu").fadeToggle(200);
       $(this).toggleClass('btn-open').toggleClass('btn-close');
    });
});
$('.overlay').on('click', function(){
    $(".menu").fadeToggle(200);
    $(".menu-button a").toggleClass('btn-open').toggleClass('btn-close');
    open = false;
});