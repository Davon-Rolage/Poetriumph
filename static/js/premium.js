const inspiringAudio = $("#inspiring-audio")[0];
const isPremium = $("#is-premium").text();

// Toggle visibility of 'has premium' and 'no premium' containers
if (isPremium == 'true') {
    $("#container-no-premium").hide();
    $("#container-has-premium").attr("hidden", false);
}

// AJAX to make the user a premium user
$('#form-premium').on('submit', function(event) {
    event.preventDefault();

    $.ajax({
        type: "POST",
        url: $(this).attr('action'),
        data: $(this).serialize(),
        dataType: "json",
        encode: true,
        success: function(data) {
            if (data.success) {
                inspiringAudio.play();
                $("#container-no-premium").fadeOut(1470);
                setTimeout(function() {
                    $("#container-has-premium").attr("hidden", false);
                }, 1470);
            }
        }
    });
});

// Toggle fun
$("#dance-speaker").click(function() {
    if (inspiringAudio.paused) {
        inspiringAudio.play();
    } else {
        inspiringAudio.pause();
    }
});
