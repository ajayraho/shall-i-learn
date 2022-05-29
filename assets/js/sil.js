window.onload = function () {
  const input = document.querySelector("#silInput");
  const button = document.querySelector("#silSubmit");
  const form = document.querySelector("#silForm");
  const linechartDiv = document.getElementById("chart_div");
  const regionschartDiv = document.getElementById("region_chart_div");
  function turnOnLoaders(){
    linechartDiv.innerHTML="Loading...";
    regionschartDiv.innerHTML="Loading...";
  }
  function turnOffLoaders(){
    linechartDiv.innerHTML="";
    regionschartDiv.innerHTML="";
  }
  const SHALLILEARN = async function (e) {
    e.preventDefault();
    turnOnLoaders();
    await fetch("http://127.0.0.1:8000/sil/", {
      method: "POST",
      headers: {
        Accept: "application/json, text/plain, */*",
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
      },
      body: JSON.stringify({ query: input.value }),
    }).then(async (res) => {
      turnOffLoaders();
      var resp = await res.json();
      google.charts.load("current", { packages: ["corechart", "geochart"] });
      google.charts.setOnLoadCallback(() => {
        drawChart();
        drawRegionsMap();
      });
      function drawChart() {
        var arr = resp.GTPTime.map((i) => [
          new Date(new Date(i[0]).toDateString()),
          i[1],
        ]);
        var data = google.visualization.arrayToDataTable([["Day", ""], ...arr]);
        var options = {
          curveType: "function",
          hAxis: {
            format: "yyyy",
          },
          legend: { position: "none" },
          animation: {
            startup: true,
            duration: 750,
            easing: "out",
          },
          width: 1000,
          height: 250,
        };
        var chart = new google.visualization.LineChart(linechartDiv);
        chart.draw(data, options);
      }

      function drawRegionsMap() {
        var data = google.visualization.arrayToDataTable([
          ["Country", "Popularity"],
          ...resp.GTPRegn,
        ]);
        var options = {
          width: 400,
          height: 300,
        };
        var chart = new google.visualization.GeoChart(regionschartDiv);
        chart.draw(data, options);
      }
    });
  };
  button.onclick = SHALLILEARN;
  form.onsubmit = SHALLILEARN;
};
