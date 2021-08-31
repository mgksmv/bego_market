$(document).ready(function () {
    $('#add-to-cart').on('click', function () {
        var _pid = $(this).attr('data-product');
        var _vm = $(this);

        // Ajax
        $.ajax({
            url: '/cart/add_cart/' + _pid + '/',
            success: function (res) {
                _vm.addClass('btn-success').removeClass('btn-primary');
                document.getElementById('to-cart-display').style.display = 'block';
                document.getElementById('add-to-cart').style.display = 'none';

                cartCounter = document.getElementById('cart-counter');

                a = cartCounter.innerText;
                b = parseInt(a) + 1;
                c = cartCounter.innerText = b;

                console.log(b);

                document.getElementById('cart-text').innerText = 'В корзине ';
            }
        });
    });
});
