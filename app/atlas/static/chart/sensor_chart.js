const ctx = document.getElementById("chart");
const table = document.getElementById("tableBody");
const chart_buttons = Array.from(document.getElementById("board-buttons").children);
chart_buttons.forEach((item) => {
    item.addEventListener('click', function () {
        draw_chart(item.getAttribute('data-count'));
        ctx.setAttribute('data-count', item.getAttribute( 'data-count'));
        chart_buttons.forEach((temp) => {
            jQuery(temp).removeClass('disabled');
        });
        jQuery(item).addClass('disabled');
    });
});


const dataColorsOld = ['#b84d4d', '#8f4db8', '#4f4db8', '#4d7fb8', '#4da4b8',
    '#4db891', '#4db86b', '#96b84d', '#b8a64d', '#b8864d', '#bd6d3e']

const dataColors = {
    'ai_max': '#808080',
    'ai_min': '#808080',
    'ai_mean': '#4d7fb8',
    'stat_min': '#b8a64d',
    'stat_max': '#b8a64d',
    'ml_min': '#b84d4d',
    'ml_max': '#b84d4d',
    'status': '#96b84d',
    'mode': '#8ccb5e',
}
const dataLabels = {
    'ai_max': 'максимальное отклонение измерения',
    'ai_min': 'минимальное отклонение измерения',
    'ai_mean': 'измерение датчика',
    'stat_min': 'ST(в.ур-нь)',
    'stat_max': 'ST(н.ур-нь)',
    'ml_min': 'ML(в.ур-нь)',
    'ml_max': 'ML(н.ур-нь)',
    'mode': 'режим работы',
}
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
            // if (data[dataKey][0] !== 0) {
            //     mainChart.data.datasets[num_col] = {
            //         label: dataLabels[dataKey],
            //         data: data[dataKey],
            //         lineTension: 0,
            //         backgroundColor: 'transparent',
            //         borderColor: dataColors[dataKey],
            //         borderWidth: 1,
            //         pointRadius: 0,
            //     }
            //}
            mainChart.data.datasets[num_col] = {
                    label: dataLabels[dataKey],
                    data: data[dataKey],
                    lineTension: 0,
                    backgroundColor: 'transparent',
                    borderColor: dataColors[dataKey],
                    borderWidth: 2,
                    pointRadius: 0,
                }
            num_col++;
        }
        mainChart.update('none');
    });
}


jQuery(document).ready(function () {
    draw_chart(ctx.getAttribute( 'data-count'));
    // table_upd();
});


let timerId = setInterval(function () {
    draw_chart(ctx.getAttribute( 'data-count'));
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
