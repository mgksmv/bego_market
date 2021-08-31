$(".dropdown-checkbox-main dt a").on('click', function () {
    $(".dropdown-checkbox-main dd ul").slideToggle('fast');
});

$(".dropdown-checkbox-main dd ul li a").on('click', function () {
    $(".dropdown-checkbox-main dd ul").hide();
});

function getSelectedValue(id) {
    return $("#" + id).find("dt a span.value").html();
}

$(document).bind('click', function (e) {
    var $clicked = $(e.target);
    if (!$clicked.parents().hasClass("dropdown-checkbox-main")) $(".dropdown-checkbox-main dd ul").hide();
});

$('.mutliSelect input[type="checkbox"]').on('click', function () {

    var title = $(this).closest('.mutliSelect').find('input[type="checkbox"]').val(),
        title = $(this).val() + ",";

    if ($(this).is(':checked')) {
        var html = '<span title="' + title + '">' + title + '</span>';
        $('.multiSel').append(html);
        $(".hida").hide();
    } else {
        $('span[title="' + title + '"]').remove();
        var ret = $(".hida");
        $('.dropdown-checkbox-main dt a').append(ret);

    }
});