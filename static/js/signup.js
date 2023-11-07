// AJAX for checking if the username is already taken
const usernameInput = $("#floatingInputGroupUsername");
const usernameTakenError = $("#username-taken-error");

usernameInput.on("change", function() {
    $.ajax({
        type: "GET",
        url: $("#url-check-username").val(),
        data: {
        username: usernameInput.val(),
        },
        success: function(exists) {
        if (exists == 'true') {
            usernameInput.addClass("is-invalid");
            usernameTakenError.show();
        }
        else {
            usernameInput.removeClass("is-invalid");
            usernameTakenError.hide();
        }
        }
    })
})