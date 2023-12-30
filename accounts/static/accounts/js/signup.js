// AJAX for checking whether the username is already taken
const usernameInput = $("#floatingInputGroupUsername");
const usernameTakenError = $("#username-taken-error");

usernameInput.on("change", function() {
    const usernameInputValue = usernameInput.val();

    if (usernameInputValue.trim() === "") {
        usernameInput.addClass("is-invalid");
        usernameTakenError.hide();
        return;
    }
    
    $.ajax({
        type: "GET",
        url: $("#url-check-username").val(),
        data: {
        username: usernameInputValue,
        },
        success: function(username) {
        if (username.exists) {
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