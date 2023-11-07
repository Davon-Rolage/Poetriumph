const characterLimit = $("#character_limit").text();
const buttonTranslate = $("#btn-translate");
const languageEngineDropdown = $("#language-engine-dropdown");
const targetLanguageDropdown = $('select[name="target_lang"]');
const languageOptions = targetLanguageDropdown.find('option').map(function() {return $(this).text();}).get();
const loadingButtonText = $("#loading_button_text").text();
const tooltipLoadingGPT = new bootstrap.Tooltip($("#btn-translate"), {
    title: $("#tt-loading-text-chatgpt").text(),
    placement: "top",
    trigger: "manual"
});

$(document).ready(function() {
    // Update character counter on page load
    $("#character_count").text($("#original").val().length);
    
    // Update the target language dropdown when the language engine dropdown changes
    languageEngineDropdown.change(updateTargetLanguageDropdown);
    updateTargetLanguageDropdown();

    // Activate "Sign in to save to library" tooltip
    activateTooltipSaveToLibrary();
})

// Update character counter in the lower right corner of the textbox
function updateCounter(textbox) {
    const characterCount = textbox.val().length;
    $("#character_count").text(characterCount);

    
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

function activateTooltipLoadingGPT() {
    setTimeout(function() {
        tooltipLoadingGPT.show();
    }, 5000);
    
    setTimeout(function() {
        tooltipLoadingGPT.hide();
    }, 12000);
}

// Start loading spinner and show loading tooltip when translate button is clicked
$("#form-translate").submit(function (event) {
    event.preventDefault();
    const withinLimit = updateCounter($("#original"));
    if (!withinLimit) {
        return
    } else {
        buttonTranslate.prop("disabled", true);
        $("#button-translate-text").text(loadingButtonText);
        $("#spinner").css("display", "inline-block");
        event.target.submit();
        if (languageEngineDropdown.val().includes('ChatGpt')) {
            activateTooltipLoadingGPT();
        }
    }
});

// Download button
$("#button-download").click(function () {
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

// Update character counter when user types
$("#original").on('input', function() {
    updateCounter($("#original"));
});

function updateTargetLanguageDropdown() {
    targetLanguageDropdown.empty();
    const gptPoetLanguages = languageOptions.slice(0, 2);
    const options = languageEngineDropdown.val() === 'ChatGpt_Poet' ? gptPoetLanguages : languageOptions;
    options.forEach((language) => {
        targetLanguageDropdown.append(`<option value="${language}">${language}</option>`);
    });
};

function activateTooltipSaveToLibrary() {
    if (!$("#btn-save-to-library").prop("disabled")) {
        $("#tt-save-to-library").parent().html($("#tt-save-to-library").html());
    }
};
