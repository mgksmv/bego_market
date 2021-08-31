$(document).ready(function () {
    $('.add-to-wishlist').on('click', function () {
        var _pid = $(this).attr('data-product');
        var _vm = $(this);

        // Ajax
        $.ajax({
            url: '/account/wishlist/add-to-wishlist/',
            data: {
                product: _pid
            },
            dataType: 'json',
            success: function (res) {
                if (res.bool == true) {
                    _vm.addClass('btn-outline-gray').removeClass('btn-outline-primary');

                    a = document.getElementById('wishlist-counter').innerText;
                    b = parseInt(a) + 1;
                    c = document.getElementById('wishlist-counter').innerText = b;

                    console.log(b);

                    document.getElementById('button-text').innerText = 'Убрать из желаемого  ';
                } else {
                    _vm.addClass('btn-outline-primary').removeClass('btn-outline-gray');

                    a = document.getElementById('wishlist-counter').innerText;
                    b = parseInt(a) - 1;
                    c = document.getElementById('wishlist-counter').innerText = b;

                    console.log(b);

                    document.getElementById('button-text').innerText = 'В список желаемого  ';
                }

            }
        });
    });
});
