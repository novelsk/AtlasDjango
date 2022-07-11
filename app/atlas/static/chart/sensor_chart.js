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
    'ai_max': 'Измерение (H)',
    'ai_min': 'Измерение (L)',
    'ai_mean': 'Измерения',
    'stat_min': 'ST(L)',
    'stat_max': 'ST(H)',
    'ml_min': 'ML(L)',
    'ml_max': 'ML(H)',
    'mode': 'режим работы',
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
                    backgroundColor: 'transparent',
                    borderColor: dataColors[dataKey],
                    borderWidth: 2,
                    pointRadius: 0,
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
