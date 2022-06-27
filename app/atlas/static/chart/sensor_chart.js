const ctx = document.getElementById("chart");
const table = document.getElementById("tableBody");
const chart_buttons = Array.from(document.getElementById("board-buttons").children);
chart_buttons.forEach((item) => {
    item.addEventListener('click', function () {
        draw_chart(item.innerHTML);
        ctx.className = item.innerHTML;
        chart_buttons.forEach((temp) => {
            jQuery(temp).removeClass('disabled');
        });
        jQuery(item).addClass('disabled');
    });
});


let dataColors = ['#b84d4d', '#8f4db8', '#4f4db8', '#4d7fb8', '#4da4b8',
    '#4db891', '#4db86b', '#96b84d', '#b8a64d', '#b8864d', '#bd6d3e']
let mainChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: [],
        datasets: [],
    },
    options: {
        legend: {
            display: false,
        }
    }
});


function draw_chart(count = '') {
    let request = window.location.origin + "/api/chart" + window.location.pathname;
    jQuery.get(request, {'count': count}, function (data) {
        mainChart.data.labels = data['date'];
        delete data['date'];
        let num_col = 0;
        for (const dataKey in data) {
            if (data[dataKey][0] !== 0) {
                mainChart.data.datasets[num_col] = {
                    label: dataKey,
                    data: data[dataKey],
                    lineTension: 0,
                    backgroundColor: 'transparent',
                    borderColor: dataColors[num_col],
                    borderWidth: 2,
                    pointRadius: 0,
                }
            }
            num_col++;
        }
        mainChart.update('none');
    });
}


jQuery(document).ready(function () {
    draw_chart(ctx.className);
    // table_upd();
});


let timerId = setInterval(function () {
    draw_chart(ctx.className);
    // table_upd();
}, 60000);


function table_upd() {
    let request = "../api/ai";
    jQuery.get(request, function (data) {
        let innerHtml = '';
        for (let i = 0; i < data.length; i++) {
            innerHtml += '<tr><td>' + data[i]['datain'] + '</td>';
            innerHtml += '<td>' + data[i]['cmnt'] + '</td>';
            innerHtml += '<td><button type="button" class="btn btn-outline-secondary" onclick="change_sts(' +
                data[i]['id'] + ')">квитировать</button></td></tr>';
        }
        table.innerHTML = innerHtml;
    });
}
