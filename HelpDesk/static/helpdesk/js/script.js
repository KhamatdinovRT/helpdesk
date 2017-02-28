$(document).ready(function () {

});

function load_request_form(sender) {
    url = $(sender).attr('data-url');
    request_id = parseInt(url.replace(/[^0-9\.]/g, ''), 10);
    console.log(url)
    $.ajax({
        url: url,
        type: 'get',
        dataType: 'json',
        beforeSend: function () {
            $("#myModal .modal-header #modal-title").text('Заявка №' + request_id)
            $("#myModal").modal("show");
        },
        success: function (data) {
            $("#myModal .modal-body ").html(data.html_form);
            $("#edit_form").on("submit", saveForm);
        },
    });
}

var saveForm = function () {
    var form = $(this);
    console.log(this)
    $.ajax({
        url: form.attr("action"),
        data: form.serialize(),
        type: form.attr("method"),
        dataType: 'json',
        success: function (data) {
            if (data.form_is_valid) {
                $("#table tbody").html(data.html_book_list);
                $("#myModal").modal("hide");
                $("#successMessage").show();
                $("#successMessage").fadeTo(1000, 500).slideUp(500, function () {
                    $("#successMessage").slideUp(500);
                });
            } else {
                $("#myModal .modal-content").html(data.html_form);
            }
        }
    });
    return false;
};