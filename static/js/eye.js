// $(document).ready(function () {
//     $('.icon').mousedown(function () {
//         $('.password').attr('type', 'text');
//         $('#eye').removeClass('fa-eye-slash').addClass('fa-eye');
//     });
//     $('.icon').mouseup(function () {
//         $('.password').attr('type', 'password');
//         $('#eye').removeClass('fa-eye').addClass('fa-eye-slash');
//     });
// });

$(".eye-show").on("keyup", function () {
    if ($(this).val())
        $(".show").show();
    else
        $(".show").hide();
});

$(".show").mousedown(function () {
    $(".eye-show").attr('type', 'text');
    $('#eye').removeClass('fa-eye-slash').addClass('fa-eye');
}).mouseup(function () {
    $(".eye-show").attr('type', 'password');
    $('#eye').removeClass('fa-eye').addClass('fa-eye-slash');
}).mouseout(function () {
    $(".eye-show").attr('type', 'password');
    $('#eye').removeClass('fa-eye').addClass('fa-eye-slash');
});