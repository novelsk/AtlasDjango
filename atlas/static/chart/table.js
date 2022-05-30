const ctx = document.getElementById("chart");
const table = document.getElementById("tableBody");
const buttons = document.getElementById("board-buttons");
const button1 = buttons.children[0];
const button2 = buttons.children[1];
const button3 = buttons.children[2];
button1.addEventListener("click", function () {draw_chart('60');ctx.className = '60';});
button2.addEventListener("click", function () {draw_chart('240');ctx.className = '240';});
button3.addEventListener("click", function () {draw_chart('600');ctx.className = '600';});


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


function draw_chart(count='') {
    let request = "../api/cmn";
    if (count !== '') {
        request = request + '/' + count;
    }
    jQuery.get(request, function (data) {
        mainChart.data.labels = [];
        for (let i = 0; i < data['cmn_ais'][0].length; i++) {
            mainChart.data.labels.push(i + 1);
        }
        for (let i = 0; i < data['cmn_ais'].length; i++) {
            mainChart.data.datasets[i] = {
                label: 'Ai' + (i + 1),
                data: data['cmn_ais'][i],
                lineTension: 0,
                backgroundColor: 'transparent',
                borderColor: dataColors[i],
                borderWidth: 2,
                pointRadius: 0,
            }
        }
        mainChart.update('none');
    });
}


jQuery( document ).ready(function() {
    draw_chart(ctx.className);
});


let timerId = setInterval(function () {
    draw_chart(ctx.className);
}, 60000);



// let innerHtml = '';
        // for (const item in data['cmn_ais']) {
        //   innerHtml += '<tr><td>' + item[0] + '</td>';
        //   innerHtml += '<td>' + item[1] + '</td></tr>';
        // }
        // table.innerHTML = innerHtml;
