const ctx = document.getElementById("chart");
const table = document.getElementById("tableBody");



function api_get_update() {
  jQuery.get("../api/cmn", function( data ) {
    let dataLabels = []
    let dataColors = ['#b84d4d', '#8f4db8', '#4f4db8', '#4d7fb8', '#4da4b8',
      '#4db891', '#4db86b', '#96b84d', '#b8a64d', '#b8864d', '#bd6d3e']

    for (let i=0; i < data['cmn_ais'][0].length; i++) {
      dataLabels.push(i+1);
    }

    let myChart = new Chart(ctx, {
      type: 'line',
      data: {
        labels: dataLabels,
        datasets: [
        {
          data: [25.8, 25.8, 25.7, 25.7, 25.7, 25.7, 25.6, 25.6, 25.6, 23.9, 23.9, 23.9, 23.9, 23.9, 23.9],
          lineTension: 0,
          backgroundColor: 'transparent',
          borderColor: dataColors[0],
          borderWidth: 2,
          pointBackgroundColor: '#007bff'
        }, {
          data: data['cmn_ais'][1],
          lineTension: 0,
          backgroundColor: 'transparent',
          borderColor: dataColors[1],
          borderWidth: 2,
          pointBackgroundColor: '#007bff'
        }, {
          data: data['cmn_ais'][2],
          lineTension: 0,
          backgroundColor: 'transparent',
          borderColor: dataColors[2],
          borderWidth: 2,
          pointBackgroundColor: '#007bff'
        }, {
          data: data['cmn_ais'][3],
          lineTension: 0,
          backgroundColor: 'transparent',
          borderColor: dataColors[3],
          borderWidth: 2,
          pointBackgroundColor: '#007bff'
        }, {
          data: data['cmn_ais'][4],
          lineTension: 0,
          backgroundColor: 'transparent',
          borderColor: dataColors[4],
          borderWidth: 2,
          pointBackgroundColor: '#007bff'
        }, {
          data: data['cmn_ais'][5],
          lineTension: 0,
          backgroundColor: 'transparent',
          borderColor: dataColors[5],
          borderWidth: 2,
          pointBackgroundColor: '#007bff'
        }, {
          data: data['cmn_ais'][6],
          lineTension: 0,
          backgroundColor: 'transparent',
          borderColor: dataColors[6],
          borderWidth: 2,
          pointBackgroundColor: '#007bff'
        }, {
          data: data['cmn_ais'][7],
          lineTension: 0,
          backgroundColor: 'transparent',
          borderColor: dataColors[7],
          borderWidth: 2,
          pointBackgroundColor: '#007bff'
        }, {
          data: data['cmn_ais'][8],
          lineTension: 0,
          backgroundColor: 'transparent',
          borderColor: dataColors[8],
          borderWidth: 2,
          pointBackgroundColor: '#007bff'
        }, {
          data: data['cmn_ais'][9],
          lineTension: 0,
          backgroundColor: 'transparent',
          borderColor: dataColors[9],
          borderWidth: 2,
          pointBackgroundColor: '#007bff'
        }
        ]
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

    // let innerHtml = '';
    // for (const item in data['cmn_ais']) {
    //   innerHtml += '<tr><td>' + item[0] + '</td>';
    //   innerHtml += '<td>' + item[1] + '</td></tr>';
    // }
    // table.innerHTML = innerHtml;
  });
}

jQuery( document ).ready(function() {
  api_get_update();
});
