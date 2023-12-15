$(document).ready(function() {
    // Load the image for each achievement
    $(".achievement_badge").each(function() {
        const poemId = $(this).attr("id");
        const poemSource = "/static/images/badges/" + poemId + ".png";
        $(this).attr("src", poemSource);
    });
})