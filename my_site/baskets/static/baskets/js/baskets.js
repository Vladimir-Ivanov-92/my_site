// Удаление товаров из модальной корзины:
$(function ($) {
    $(document).on('click', '.remove', function (e) {
        e.preventDefault()
        console.log('111', this)
        $.get(this.href, function (response){
            console.log('222', response)
            var page_content_body = $('#ajaxbasketcardbody',response).get(0);
            var page_content_footer = $('#ajaxbasketcardfooter', response).get(0);
            console.log('333',page_content_body);
            console.log('444',page_content_footer);
            $('.offcanvas-body').html(page_content_body);
            $('#cardfooterall').html(page_content_footer);
        })
    })
})