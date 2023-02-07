// Удаление товаров из модальной корзины:
$(function ($) {
    $(document).on('click', '.remove', function (e) {
        e.preventDefault()

        // Получение id продукта
        var cardfooter_id ='#' + 'cardfooter' + this.id
        var cardfooterdiv_id = '#' + 'cardfooterdiv' + this.id

        $.get(this.href, function (response){
            var page_content_body = $('#ajaxbasketcardbody',response).get(0);
            var page_content_footer = $('#ajaxbasketcardfooter', response).get(0);
            var page_content_badge = $('#basket_button', response).get(0);
            $('.offcanvas-body').html(page_content_body);
            $('#cardfooterall').html(page_content_footer);
            $('#basket_button_div').html(page_content_badge);

            // Обновление в футере карточки продукта информации
            var id = $(cardfooterdiv_id, response).get(0);
            $(cardfooter_id).html(id);

        })
    })
})


// Добавление товаров в корзину без перезагрузки страницы:
$(function ($) {
    $(document).on('click', '.plus_or_minus_to_basket', function (e) {
        e.preventDefault()
        var cardfooter_id ='#' + 'cardfooter' + this.id
        var cardfooterdiv_id = '#' + 'cardfooterdiv' + this.id
        $.get(this.href, function (response){
            var page_content_badge = $('#basket_button', response).get(0);
            var id = $(cardfooterdiv_id, response).get(0);
            $('#basket_button_div').html(page_content_badge);
            $(cardfooter_id).html(id);

            // Обновление данных в корзине:
            var page_content_body = $('#ajaxbasketcardbody',response).get(0);
            var page_content_footer = $('#ajaxbasketcardfooter', response).get(0);
            $('.offcanvas-body').html(page_content_body);
            $('#cardfooterall').html(page_content_footer);
        })
    })
})