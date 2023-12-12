if (!$) {
    $ = django.jQuery;
}

$(document).ready(function () {
    function change() {
        var password = $('#id_user_password');
        var confirm_password = $('#id_confirm_password');

        if (password.attr("type") === "text") {
            password.attr("type", "password");
        }
        if (confirm_password.attr("type") === "text") {
            confirm_password.attr("type", "password");
        }
    }

    $("#id_user_password").focus(function () {
        change();
    });

    $("#id_confirm_password").focus(function () {
        change();
    });

    $("#id_user_password").change(function () {
        change();
    });

    $("#id_confirm_password").change(function () {
        change();
    });

    $("#id_user_password").mouseover(function () {
        change();
    });

    $("#id_confirm_password").mouseover(function () {
        change();
    });

    $("#id_user_password").click(function () {
        change();
    });

    $("#id_confirm_password").click(function () {
        change();
    });

    

});