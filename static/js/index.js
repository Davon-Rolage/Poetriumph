const characterLimit = $("#character_limit").text();

// Update character counter in the lower right corner of the textbox
function updateCounter(textbox) {
    const characterCount = textbox.val().length;
    $("#character_count").text(characterCount);

    const buttonTranslate = $("#button_translate");
    
    if (characterCount > characterLimit) {
        $("#character_counter").css("color", "red");
        buttonTranslate.prop("disabled", true);
        buttonTranslate.removeClass("btn-primary").addClass("btn-outline-danger");
        return false;
    }
    else {
        $("#character_counter").css("color", "black");
        buttonTranslate.prop("disabled", false);
        buttonTranslate.removeClass("btn-outline-danger").addClass("btn-primary");
        return true;
    }
}

// Update character counter when user types
$("#original").on('input', function() {
    updateCounter($("#original"));
});

const loadingButtonText = $("#loading_button_text").text();
const loading_tooltip = new bootstrap.Tooltip($("#button_translate"), {
    title: $("#loading_tooltip_text").text(),
    placement: "top",
    trigger: "manual"
})

function showLoadingTooltip() {
    setTimeout(function() {
        loading_tooltip.show();
    }, 5000);
    
    setTimeout(function() {
        loading_tooltip.hide();
    }, 12000);
}

// Start loading spinner and show loading tooltip when translate button is clicked
$("#form-translate").on("submit", function (event) {
    event.preventDefault();
    const withinLimit = updateCounter($("#original"));
    if (!withinLimit) {
        return
    } else {
        $("#button_translate").prop("disabled", true);
        $("#button_translate_text").text(loadingButtonText);
        $("#spinner").show();
        event.target.submit();
        showLoadingTooltip();
    }});

// Download button
$("#button_download").click(function () {
    const translation = $("#translation-text").val();
    if (!translation.trim()) {
        return false;
    }
    let filename = translation.slice(0, 20);

    if (translation) {
        let element = document.createElement('a');
        element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(translation));
        element.setAttribute('download', filename);
        element.style.display = 'none';
        document.body.appendChild(element);
        element.click();
        document.body.removeChild(element);
    }
});

// Submit save-form only if translation text is not empty
$("#save-form").submit(function(e) {
    e.preventDefault();
    if ($("#translation-text").val() != "") {
        e.target.submit();
    }
});

// // Set target_lang options to English and Spanish if language engine is ChatGpt_Poet
const languageEngineDropdown = document.querySelector('select[name="language_engine"]');
const targetLanguageDropdown = document.querySelector('select[name="target_lang"]');

// Store the original options when the page loads
const originalOptions = Array.from(targetLanguageDropdown.options);

function updateTargetLanguageDropdown() {
    if (languageEngineDropdown.value === 'ChatGpt_Poet') {
        const options = targetLanguageDropdown.options;
        const slicedOptions = Array.from(options).slice(0, 2);
        targetLanguageDropdown.innerHTML = '';
        slicedOptions.forEach((option) => {
        targetLanguageDropdown.appendChild(option);
        });
    } else {
        targetLanguageDropdown.innerHTML = '';
        originalOptions.forEach((option) => {
        targetLanguageDropdown.appendChild(option);
        });
    }
}
// Call the function on page load
updateTargetLanguageDropdown();

// Call the function when languageEngineDropdown changes
languageEngineDropdown.addEventListener('change', updateTargetLanguageDropdown);

$(document).ready(function() {
    $("#character_count").text($("#original").val().length);
})
