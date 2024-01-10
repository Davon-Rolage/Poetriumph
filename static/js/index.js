const urlGetTranslation = $("#url-get-translation").text();
const characterLimit = $("#character_limit").text();
const buttonTranslate = $("#btn-translate");
const buttonTranslateInitialText = buttonTranslate.text();
const languageEngineDropdown = $("#language-engine-dropdown");
const targetLanguageDropdown = $('#target-language-dropdown');
const loadingButtonText = $("#loading_button_text").text();
const tooltipLoadingGPT = new bootstrap.Tooltip($("#btn-translate"), {
    title: $("#tt-loading-text-chatgpt").text(),
    placement: "top",
    trigger: "manual"
});

$(document).ready(function() {
    // Update character counter on page load
    $("#character_count").text($("#original-text").val().length);
    
    // Update the target language dropdown when the language engine dropdown changes
    languageEngineDropdown.change(function() {
        updateTargetLanguageDropdown();
    });
    
    
    updateTargetLanguageDropdown();
    
    // Activate "Sign in to save to library" tooltip
    activateTooltipSaveToLibrary();


    // Listen for changes in the dropdown
    $('.language-engine select').on('change', function() {
        const selectedValue = $(this).val();
        $('.tt').tooltip('hide');
        
        switch (selectedValue) {
          case 'GoogleTranslator':
            $('#tt-google-translator').tooltip('show');
            break;
          case 'ChatGptTranslator':
            $('#tt-chatgpt-translator').tooltip('show');
            break;
          case 'ChatGpt_Poet':
            $('#tt-chatgpt-poet').tooltip('show');
            break;
          case 'MyMemoryTranslator':
            $('#tt-mymemory-translator').tooltip('show');
            break;
          default:
            break;
        }
      })
});

// Activate "Sign in to save to library" tooltip for unauthenticated users
function activateTooltipSaveToLibrary() {
    if (!$("#btn-save-to-library").prop("disabled")) {
        $("#tt-save-to-library").parent().html($("#tt-save-to-library").html());
    }
};

// Activate loading tooltip for ChatGPT
function activateTooltipLoadingGPT() {
  setTimeout(() => tooltipLoadingGPT.show(), 5000);
  setTimeout(() => tooltipLoadingGPT.hide(), 12000);
}

// Update character counter when user types
$("#original-text").on('input', function() {
    updateCounter($(this));
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
    };
}

// Start loading spinner and show loading tooltip when translate button is clicked
$("#btn-translate").click(function () {
    const originalText = $("#original-text").val();
    if (!originalText.trim()) {
        return false;
    }
    
    const withinLimit = updateCounter($("#original-text"));
    if (!withinLimit) {
        return false;
    } else {
        $('.tt').tooltip('hide');
        buttonTranslate.prop("disabled", true);
        // $("#button-translate-text").text(loadingButtonText);
        $("#spinner").css("display", "inline-block");
        if (languageEngineDropdown.val().includes('ChatGpt')) {
            activateTooltipLoadingGPT();
        }
        $.ajax({
            url: urlGetTranslation,
            type: "POST",
            data: $("#save-form").serialize(),
            success: function (data) {
                $("#spinner").css("display", "none");
                $("#button-translate-text").text(buttonTranslateInitialText);
                $("#translation-text").val(data.translation);
                $("#translation-text").trigger("input");
                buttonTranslate.prop("disabled", false);
            }
        })
    }
});

// Download button
$("#btn-download").click(function () {
    const translation = $("#translation-text").val().trim();
    if (translation) {
        let filename = translation.slice(0, 20);
        const element = document.createElement('a');
        element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(translation));
        element.setAttribute('download', filename + ".txt");
        element.style.display = 'none';
        document.body.appendChild(element);
        element.click();
        document.body.removeChild(element);
    }
});

// Save to library button
$("#btn-save-to-library").click(function() {
    if ($("#translation-text").val() != "") {
        e.target.submit();
    }
})

// Update the target language dropdown when selected language engine is "ChatGpt_Poet"
function updateTargetLanguageDropdown() {
    if (languageEngineDropdown.val() == "ChatGpt_Poet") {
        targetLanguageDropdown.find("option:gt(1)").hide();
        targetLanguageDropdown.find("option:first").prop("selected", true);
    } else {
        targetLanguageDropdown.find("option:gt(1)").show();
    }
};

