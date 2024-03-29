const charts_controls = Array.from(document.getElementsByClassName('chart-control'));
const div_chart = document.getElementById('chart-hide');
charts_controls[1].hidden = true;
div_chart.hidden = true;
charts_controls[0].addEventListener('click', function () {
    charts_controls[0].hidden = true;
    charts_controls[1].hidden = false;
    charts_controls[2].hidden = true;
    div_chart.hidden = false;
});
charts_controls[1].addEventListener('click', function () {
    charts_controls[0].hidden = false;
    charts_controls[1].hidden = true;
    charts_controls[2].hidden = false;
    div_chart.hidden = true;
});

const chart_buttons = Array.from(document.getElementById("board-buttons").children);
chart_buttons.forEach((item) => {
    item.addEventListener('click', function () {
        pointCount = item.getAttribute( 'data-count');
        draw_chart(pointCount);
        chart_buttons.forEach((temp) => {
            jQuery(temp).removeClass('disabled');
        });
        jQuery(item).addClass('disabled');
        item.parentNode.parentNode.firstElementChild.innerHTML = item.innerHTML;
    });
});


const dataColorsOld = ['#b84d4d', '#8f4db8', '#4f4db8', '#4d7fb8', '#4da4b8',
    '#4db891', '#4db86b', '#96b84d', '#b8a64d', '#b8864d', '#bd6d3e']
let datasetCount = 0;
let datasetState = [];
let histogramAxis = [null, null]
let pointCount = 60;
let mainChart = new Chart(charts_controls[2], {
    type: 'line',
    data: {
        labels: [],
        datasets: [],
    },
    options: {
        plugins: {
            legend: {
                display: true,
            }
        }
    }
});
let scatterChart = new Chart(charts_controls[3], {
    type: 'scatter',
    data: {
        labels: [],
        datasets: [],
    },
    options: {
        plugins: {
            legend: {
                display: false,
            }
        }
    }
});


function draw_chart(count) {
    let request = window.location.origin + "/new/api/object/chart";
    const urlParams = new URLSearchParams(window.location.search);

    for (let i = 0; i < datasetCount; i++) {datasetState[i] = mainChart.getDatasetMeta(i).hidden;}
    jQuery.get(request,
        {'count': count, 'object_id': urlParams.get('object_id')},
        function (data) {
            let dates = [];
            for (const key in data['labels']) {
                dates.push(data['labels'][key].split(':').slice(0, 2).join(':'))
            }
            mainChart.data.labels = dates;
            delete data['labels'];
            for (const i in data['data']) {
                mainChart.data.datasets[i] = {
                    label: data['sensors'][i],
                    data: data['data'][i],
                    lineTension: 0,
                    backgroundColor: 'transparent',
                    borderColor: dataColorsOld[i],
                    borderWidth: 2,
                    pointRadius: 0,
                }
                mainChart.setDatasetVisibility(i, !datasetState[i]);
            }
        mainChart.update('none');
        datasetCount = data['data'].length;
    });
    request = window.location.origin + "/api/setter";
    if (histogramAxis[0] !== null && histogramAxis[1] !== null) {
        jQuery.get(request, {
        'count': count,
        'sensor_x': histogramAxis[0],
        'sensor_y': histogramAxis[1],
        },
        function (data) {
            scatterChart.data.datasets[0] = {
                data: data,
                backgroundColor: 'rgba(114, 103, 239, 0.2)',
                borderColor: 'transparent',
            }
            scatterChart.update('none');
        });
    }
}


jQuery(document).ready(function () {
    draw_chart(pointCount);
});

setInterval(function () {
    draw_chart(pointCount);
}, 60000);


function set_scale(button, axis) {
    if (axis === 'x') {
        histogramAxis[0] = button.getAttribute( 'data-sensor');
    } else if (axis === 'y') {
        histogramAxis[1] = button.getAttribute( 'data-sensor');
    }
    draw_chart(pointCount);
    button.parentNode.parentNode.firstElementChild.innerHTML = button.innerHTML;
}
