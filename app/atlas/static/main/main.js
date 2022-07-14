let elements = document.querySelectorAll('input');
for (let elem of elements) {
    if (elem.type !== 'checkbox') { jQuery(elem).addClass('form-control'); }
}
function confirm_error(error_log_id, button) {
    jQuery.get(window.location.origin + "/api/confirm_error", {'error_log_id': error_log_id },
        function (data) { if (data['']) {jQuery(button).addClass('disabled');} }
    );
}

function confirm_error_all() {
    let table = Array.from(document.getElementById('table-errors').children);
    for (const temp in table) {
        let line = table[temp];
        jQuery.get(window.location.origin + "/api/confirm_error", {'error_log_id': line.getAttribute('data-id') },
            function (data) { if (data['']) {jQuery(line.lastElementChild.firstElementChild).addClass('disabled');} }
        );
    }
}
