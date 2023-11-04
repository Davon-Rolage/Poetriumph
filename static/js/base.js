// Execute when page is loaded
$(document).ready(function () {
    changeDataTableLanguage();
    activateCopyToClipboard();
    activateTooltips();
    
    $(".poem-textarea").on("input", function() {
        adjustTextareaHeight(this);
    });
});

// Adjust textarea's height based on its content
function adjustTextareaHeight(textarea) {
    let rowsNum = textarea.value.split("\n").length;
    if (rowsNum > 10) {
        $(textarea).attr("rows", $(textarea).val().split("\n").length);
    }
}

// Activate bootstrap tooltips
function activateTooltips() {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
      return new bootstrap.Tooltip(tooltipTriggerEl)
    })
}
    
function changeDataTableLanguage() {
    let userLanguage = window.location.pathname.split('/')[1];
    if (userLanguage === 'es') {
        userLanguage = 'es_es';
    }
    if (userLanguage !== 'en') {
        $('.table').DataTable({
            'language': {
                'url': '//cdn.datatables.net/plug-ins/1.11.3/i18n/' + userLanguage + '.json'
            },
        });
    } else {
        $('.table').DataTable();
    }
}

// Copy to clipboard
function activateCopyToClipboard() {
    $(".copy-to-clipboard").each(function() {
        $(this).click(function() {
            const textToCopy = $(this).siblings(".text-to-copy").val();
            navigator.clipboard.writeText(textToCopy);
            let checkIcon = $(this).children("#check-icon");
            checkIcon.css("display", "inline");
            setTimeout(function() {
                checkIcon.hide();
            }, 2000);
        })
    })
}

// Clickable row to redirect to the poem
$(".clickable-td").click(function() {
    window.location=$(this).find("a").attr("href");
});
