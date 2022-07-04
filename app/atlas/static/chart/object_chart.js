const ctx = document.getElementById("chart");
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
        mainChart.data.labels = data['labels'];
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
        }
        mainChart.update('none');
    });
}


jQuery(document).ready(function () {
    draw_chart(ctx.getAttribute( 'data-count'));
});


let timerId = setInterval(function () {
    draw_chart(ctx.getAttribute( 'data-count'));
}, 60000);
