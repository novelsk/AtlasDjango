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

const custom_points = document.getElementById("custom_points");
const points = custom_points.children[0].firstChild;
const accept_points_button = custom_points.children[1];
accept_points_button.addEventListener('click', function () {
    draw_chart(points.value);
    ctx.setAttribute('data-count', points.value);
});


const dataColorsOld = ['#b84d4d', '#8f4db8', '#4f4db8', '#4d7fb8', '#4da4b8',
    '#4db891', '#4db86b', '#96b84d', '#b8a64d', '#b8864d', '#bd6d3e']

const dataColors = {
    'ai_max': 'rgba(119, 136, 153, 0.5)',
    'ai_min': 'rgba(119, 136, 153, 0.5)',
    'ai_mean': '#4d7fb8',
    'stat_min': 'rgba(205, 164, 52, 0.3)',
    'stat_max': 'rgba(205, 164, 52, 0.3)',
    'ml_min': 'rgba(207, 84, 81, 0.3)',
    'ml_max': 'rgba(207, 84, 81, 0.3)',
    'status': '#96b84d',
    'mode': '#8ccb5e',
    'sp_ll': '#4d7fb8',
    'sp_l': '#4da4b8',
    'sp_h': '#4da4b8',
    'sp_hh': '#4d7fb8',
}
const dataLabels = {
    'ai_max': 'Измерение (H)',
    'ai_min': 'Измерение (L)',
    'ai_mean': 'Измерения',
    'stat_min': 'ST(L)',
    'stat_max': 'ST(H)',
    'ml_min': 'ML(L)',
    'ml_max': 'ML(H)',
    'mode': 'режим работы',
    'sp_ll': 'SP(LL)',
    'sp_l': 'SP(L)',
    'sp_h': 'SP(H)',
    'sp_hh': 'SP(HH)',
}
const dataDash = {
    'ai_max': [],
    'ai_min': [],
    'ai_mean': [],
    'stat_min': [],
    'stat_max': [],
    'ml_min': [],
    'ml_max': [],
    'mode': [],
    'sp_ll': [6, 2],
    'sp_l': [6, 2],
    'sp_h': [6, 2],
    'sp_hh': [6, 2],
}
let datasetCount = 0;
let datasetState = [];
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
    for (let i = 0; i < datasetCount; i++) {datasetState[i] = mainChart.getDatasetMeta(i).hidden;}
    jQuery.get(request, {'count': count}, function (data) {
        mainChart.data.labels = data['date'];
        delete data['date'];
        let num_col = 0;
        for (const dataKey in data) {
            mainChart.data.datasets[num_col] = {
                    label: dataLabels[dataKey],
                    data: data[dataKey],
                    lineTension: 0,
                    backgroundColor: 'rgba(62, 95, 138, 0.1)',
                    borderColor: dataColors[dataKey],
                    borderWidth: 2,
                    pointRadius: 0,
                    borderDash: dataDash[dataKey],
                }
            mainChart.setDatasetVisibility(num_col, !datasetState[num_col]);
            num_col++;
        }
        mainChart.update('none');
        datasetCount = num_col;
    });
}


jQuery(document).ready(function () {
    draw_chart(ctx.getAttribute( 'data-count'));
});


let timerId = setInterval(function () {
    draw_chart(ctx.getAttribute( 'data-count'));
}, 60000);
