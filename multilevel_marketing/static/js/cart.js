$(function () {
        $(document).on('click', '.btn-increment, .btn-decrement, .btn, .delete-product', function (event) {
            event.preventDefault()
            console.log('it is ', $(this).attr("class"))
            var quantity = 1, price = 0, product;
            if ($(this).hasClass('btn')) {
                price = parseInt($(this).parent().children('.prix2n').text())
                product = $(this).parent().find('h4').text()
            } else if ($(this).hasClass('delete-product')) {
                quantity = -1 * parseInt($(this).parents('li').find('.input-quantity').val());
                product = $(this).parents('li').find('.title').text()
            } else {
                if ($(this).hasClass('btn-decrement')) {
                    quantity = -1
                }
                product = $(this).parent().siblings('.cart-info.title').text()
            }

            console.log("in js: ", product, quantity, price);
            var URL = {% url 'accounts:cart' %}
                $.ajax({
                    method: "POST",
                    url: URL,
                    data: {
                        'price': price,
                        'product': product,
                        'quantity': quantity,
                        'csrfmiddlewaretoken': '{{ csrf_token }}',
                    },
                    success: handleFormSuccess,
                    error: handleFormError,
                })
        });
        $(document).on('focus', '.input-quantity', function (event) {
            $(this).attr('oldValue', parseInt($(this).val()));
        });

        $(document).on('change', '.input-quantity', function (event) {
            console.log("the old val : ", $(this).attr('oldValue'))
            var quantity = parseInt($(this).val() - $(this).attr('oldValue'))
            var product = $(this).parents('li').children('.title.cart-info').text()
            console.log("updating ", product, quantity)
            var URL = {% url 'accounts:cart' %}
                $.ajax({
                    method: "POST",
                    url: URL,
                    data: {
                        'product': product,
                        'quantity': quantity,
                        'csrfmiddlewaretoken': '{{ csrf_token }}',
                    },
                    success: handleFormSuccess,
                    error: handleFormError,
                })
        });

        function handleFormSuccess(data, textStatus, jqXHR) {
            console.log(data);
            $('.badge-panier').html(data.items);
            $("#cd-cart").html(data.cart)
                .append('<a href="" class="checkout-btn" name="checkout">Checkout</a>')
            $("#cdd-cart").html(data.cart)

        }

        function handleFormError(jqXHR, textStatus, errorThrown) {
        }
    })