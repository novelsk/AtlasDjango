const table = document.getElementById("tableBody");

function table_upd() {
    jQuery.get("../api/archive", function (data) {
        let innerHtml = '';
        for (let i = 0; i < data.length; i++) {
            innerHtml += '<tr><td>' + data[i]['id'] + '</td>';
            innerHtml += '<td>' + data[i]['idobj'] + '</td>';
            innerHtml += '<td>' + data[i]['idai'] + '</td>';
            innerHtml += '<td>' + data[i]['datain'] + '</td>';
            innerHtml += '<td>' + data[i]['mode'] + '</td>';
            innerHtml += '<td>' + data[i]['aimax'] + '</td>';
            innerHtml += '<td>' + data[i]['aimean'] + '</td>';
            innerHtml += '<td>' + data[i]['aimin'] + '</td>';
            innerHtml += '<td>' + data[i]['statmin'] + '</td>';
            innerHtml += '<td>' + data[i]['statmax'] + '</td>';
            innerHtml += '<td>' + data[i]['mlmin'] + '</td>';
            innerHtml += '<td>' + data[i]['mlmax'] + '</td>';
            innerHtml += '<td>' + data[i]['err'] + '</td>';
            innerHtml += '<td>' + data[i]['sts'] + '</td>';
            innerHtml += '<td>' + data[i]['dataout'] + '</td>';
            innerHtml += '<td>' + data[i]['datacheck'] + '</td>';
            innerHtml += '<td>' + data[i]['cmnt'] + '</td>';
        }
        table.innerHTML = innerHtml;
    });
}


jQuery( document ).ready(function() {
    table_upd();
});
