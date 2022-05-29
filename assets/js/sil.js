window.onload = function() {
  var input = document.querySelector("#silInput");
  var button = document.querySelector('#silSubmit');
  var form = document.querySelector('#silForm');
  const SHALLILEARN = async function(e) {
    e.preventDefault();
    await fetch('http://127.0.0.1:8000/sil/', {
      method: 'POST',
      headers: {
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
      },
      body: JSON.stringify({"query":input.value})
    }).then(async(res)=>{
      var resp = await res.json()
      var arr = resp.data.map(i=>[new Date(new Date(i[0]).toDateString()),i[1]])
      google.charts.load('current', {'packages':['corechart']});
      google.charts.setOnLoadCallback(drawChart);
      function drawChart() {
        var data = google.visualization.arrayToDataTable([
          ['Day', 'Searches'],
          ...arr
        ]);

        var options = {
          curveType: 'function',
          vAxis: {
        scaleType: 'log'
  },
          animation: {
            "startup": true,
            duration: 1000,
        easing: 'out',
          }
        };

        var chart = new google.visualization.LineChart(document.getElementById('chart_div'));

        chart.draw(data, options);
      }
    })
  }
  button.onclick = SHALLILEARN;
  form.onsubmit = SHALLILEARN;

}