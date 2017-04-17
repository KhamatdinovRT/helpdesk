$(document).ready(function (e) {
    $(".modal-body").on('click', "#buttonDelete", function (e) {
        e.preventDefault();
        var btn = $(this);
        console.log();
        $.ajax({
            url: btn.attr("data-url"),
            type: 'DELETE',
            beforeSend: function (xhr) {
                xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
            },
            dataType: 'json',
            success: function (data) {
                if (data.form_is_valid) {
                    $("#table tbody").html(data.html_book_list);
                    $("#myModal").modal("hide");
                    $("#successMessage").show();
                    $("#successMessage").fadeTo(1000, 500).slideUp(500, function () {
                        $("#successMessage").slideUp(500);
                    });
                }
            },

        });

    });
});

function load_request_form(sender) {
    console.log(sender);
    var url = $(sender).attr('data-url');
    var request_id = parseInt(url.replace(/[^0-9\.]/g, ''), 10); // получаем номер заявки
    console.log(url);
    $.ajax({
        url: url,
        type: 'GET',
        dataType: 'json',
        beforeSend: function () {
            $("#myModal .modal-header #modal-title").text('Заявка №' + request_id);
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
    var page_number = $("#myModal .modal-body").data("page"); // получаем номер страницы 
    console.log(this);
    $.ajax({
        url: form.attr("action"),
        data: form.serialize() + page_number,
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
                $( "#errors" ).html(data.form_errors);
            }
        },
        error: function () {
            $("#myModal").modal("hide");
            $("#errorMessage").show();
            $("#errorMessage").fadeTo(1000, 500).slideUp(500, function () {
                $("#errorMessage").slideUp(500);
            });
        }

    });
    return false;
};

function getCookie(name) {
    var matches = document.cookie.match(new RegExp(
        "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
    ));
    return matches ? decodeURIComponent(matches[1]) : undefined;
}