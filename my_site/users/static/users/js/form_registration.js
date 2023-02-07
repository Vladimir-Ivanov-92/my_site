$(function ($) {
    $('#form_registration_ajax').submit(function (e) {
        e.preventDefault()
        $.ajax({
            type: this.method,
            url: this.action,
            data: $(this).serialize(),
            dataType: 'json',
            success: function (response) {
                $('.alert-danger').addClass('d-none')
                $('.modal-footer').addClass('d-none')
                $('.modal-header').html(
                    '<h1 class="modal-title fs-5" id="exampleModalLabel">Успешная регистрация!</h1>\n' +
                    ' <button type="button" class="btn-close" data-bs-dismiss="modal"\n' +
                    '           aria-label="Close"></button>')
                $('.modal-body').html(
                    '<div class="text-center"><text>' +
                    'На указанную вами электронную почту направлено письмо, ' +
                    'для подтверждения электронного адреса.</text></div>');
                $(document).click(function (e) {
                    e.preventDefault()
                    window.location.reload()
                })
            },
            error: function (response) {
                if (response.status === 400) {
                    $('.alert-danger').text(response.responseJSON.error).removeClass('d-none')
                }
            }
        })
    })
})