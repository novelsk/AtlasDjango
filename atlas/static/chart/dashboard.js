const ctx = document.getElementById("chart");
const table = document.getElementById("tableBody");
const buttons = document.getElementById("board-buttons");
const button1 = buttons.children[0];
const button2 = buttons.children[1];
const button3 = buttons.children[2];
button1.addEventListener("click", function () {draw_chart('60');ctx.className = '60';});
button2.addEventListener("click", function () {draw_chart('240');ctx.className = '240';});
button3.addEventListener("click", function () {draw_chart('600');ctx.className = '600';});

let num_group = null;
const num_buttons = Array.from(document.getElementById("num-buttons").children);
if (num_buttons.length === 1) {jQuery(num_buttons[0]).addClass('disabled');}
num_buttons.forEach((item) => {
    item.addEventListener('click', function () {
        num_group = item.innerHTML;
        num_buttons.forEach((temp) => {jQuery(temp).removeClass('disabled');});
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


function draw_chart(count='') {
    let request = "../api/cmn";
    if (count !== '') {
        request = request + '/' + count;
    }
    jQuery.get(request, {'num': num_group}, function (data) {
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
    table_upd();
});


let timerId = setInterval(function () {
    draw_chart(ctx.className);
    table_upd();
}, 60000);



function table_upd() {
    let request = "../api/ai";

    jQuery.get(request, function (data) {
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
            innerHtml += '<td><button type="button" class="btn btn-outline-secondary" onclick="change_sts(' +
                data[i]['id'] + ')">квитировать</button></td></tr>';
        }
        table.innerHTML = innerHtml;
    });
}


function change_sts(sts=-1) {
    let request = "../api/ai";
    if (sts !== -1) {
        request = request + '/' + sts;
        jQuery.get(request, function (data) {
            table_upd();
        });
    }
}
