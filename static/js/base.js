// Adjust textarea's height based on its content
$('textarea').each(function () {
    this.setAttribute('style', 'height:' + (this.scrollHeight) + 'px;overflow-y:hidden;');
  }).on('input', function () {
    this.style.height = 'auto';
    this.style.height = (this.scrollHeight) + 5 + 'px';
  });

// Activate bootstrap tooltips
const tooltips = document.querySelectorAll('.tt')
tooltips.forEach(t => {
    new bootstrap.Tooltip(t)
})

// Change table's language
$(document).ready(function () {
    let user_language = window.location.pathname.split('/')[1];
    user_language = user_language === 'es' ? 'es_es' : user_language;
    let table = $('#poems-table').DataTable({
        'language': {
        'url': '//cdn.datatables.net/plug-ins/1.11.3/i18n/' + user_language + '.json'
        },
    });

    // Reload the table when the language parameter changes
    $(window).on('popstate', function() {
        user_language = window.location.pathname.split('/')[1];
        user_language = user_language === 'es' ? 'es_es' : user_language;
        table.ajax.reload();
    });
});

// Copy to clipboard
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

// Clickable row to redirect to the poem
$(".clickable-td").click(function() {
    window.location=$(this).find("a").attr("href");
});

