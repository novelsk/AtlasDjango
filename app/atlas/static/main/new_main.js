for (let elem of document.querySelectorAll('input')) {
    if (elem.type !== 'checkbox') { jQuery(elem).addClass('form-control'); }
}
for (let elem of document.querySelectorAll('select')) {
    jQuery(elem).addClass('form-control');
}

let buttons = Array.from(document.getElementsByClassName('confirm-button'));
buttons.forEach((item) => {
    item.onmouseover="this.setAttribute('style', 'cursor: pointer;')";
    item.onmouseout="this.removeAttribute('style')";
});

function confirm_error(error_log_id, button) {
    jQuery.get(window.location.origin + "/api/confirm_error", {'error_log_id': error_log_id},
        function (data) {
            if (data['']) {
                button.hidden = true;
            }
            else {
                alert('Ошибка');
            }
        }
    );
}

function confirm_errors_all() {
    const urlParams = new URLSearchParams(window.location.search);

    jQuery.get(window.location.origin + "/new/api/sensor/confirm_errors_all",
        {'sensor_id': urlParams.get('sensor_id') },
        function (data) {
            if (data['']) {
                let table = Array.from(document.getElementById('table-errors').children);
                table.forEach((item) => {
                    item.hidden = true
                });
            } else {
                alert('Ошибка');
            }
        }
    );
}
