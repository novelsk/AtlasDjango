const ctx = document.getElementById("chart");
const table = document.getElementById("tableBody");
const updateButton = document.getElementById('plotUpdate');
const changeStsButton = document.getElementById('stsChange');


function api_get_update() {
  jQuery.get("../api/", function( data ) {
    let newData = [[], [], []];
    if (jQuery(changeStsButton).hasClass('sts-1')) {
      for (const item in data) {
        if (data[item]['sts'] ===  1) {
          newData[0].push(data[item]['id']);
          newData[1].push(data[item]['current']);
        }
      }
    } else {
      for (const item in data) {
        if (data[item]['sts'] ===  2) {
          newData[0].push(data[item]['id']);
          newData[1].push(data[item]['current']);
        }
      }
    }
    let myChart = new Chart(ctx, {
      type: 'line',
      data: {
        labels: newData[0],
        datasets: [{
          data: newData[1],
          lineTension: 0,
          backgroundColor: 'transparent',
          borderColor: '#007bff',
          borderWidth: 4,
          pointBackgroundColor: '#007bff'
        }]
      },
      options: {
        scales: {
          yAxes: [{
            ticks: {
              beginAtZero: false
            }
          }]
        },
        legend: {
          display: false,
        }
      }
    });

    let innerHtml = '';
    for (const item in data) {
      innerHtml += '<tr><td>' + data[item]['id'] + '</td>';
      innerHtml += '<td>' + data[item]['current'] + '</td>';
      innerHtml += '<td>' + data[item]['sts'] + '</td></tr>';
    }
    table.innerHTML = innerHtml;
  });
}

jQuery( document ).ready(function() {
  api_get_update();
});

updateButton.onclick = function () {
  api_get_update();
}

changeStsButton.onclick = function () {
  let jQButton = jQuery(changeStsButton);
  if (jQButton.hasClass('sts-1')) {
    jQButton.removeClass('sts-1').addClass('sts-2');
  } else {
    jQButton.removeClass('sts-2').addClass('sts-1');
  }
  api_get_update();
}
