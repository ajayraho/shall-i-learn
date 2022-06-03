window.onload = function () {
  const input = document.querySelector("#silInput");
  const button = document.querySelector("#silSubmit");
  const form = document.querySelector("#silForm");
  const linechartDiv = document.getElementById("chart_div");
  const regionschartDiv = document.getElementById("region_chart_div");
  const gitReposDiv = document.getElementById("git_repos");
  const gitTopicsDiv = document.getElementById("git_topics");
  const stackoverflowQuestionsDiv = document.getElementById("stackoverflowQuestions_div");
  const redditDiv = document.getElementById("reddit_div");
  const linkedinjobsDiv = document.getElementById("linkedinjobs_div");
  const linkedinnewjobsDiv = document.getElementById("linkedinnew_div");


  function turnOnLoaders(){
    linechartDiv.innerHTML="Loading...";
    regionschartDiv.innerHTML="Loading...";
    gitReposDiv.innerHTML="Loading...";
    gitTopicsDiv.innerHTML="Loading...";
    stackoverflowQuestionsDiv.innerHTML = "Loading...";
    linkedinjobsDiv.innerHTML = "Loading...";
    linkedinnewjobsDiv.innerHTML = "Loading...";
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
      var resp = await res.json();
      console.log(resp)
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

      //GitHub
      gitReposDiv.innerHTML = "<abbr title='"+resp.repos+"'>"+SILUtilAbbreviate(resp.repos)+"</abbr>";
      gitTopicsDiv.innerHTML = "<abbr title='"+resp.topics+"'>"+SILUtilAbbreviate(resp.topics)+"</abbr>";

      //stackoverflow
      stackoverflowQuestionsDiv.innerHTML = "<abbr title='"+resp.questionsCount+"'>"+SILUtilAbbreviate(resp.questionsCount)+"</abbr>";
    
      console.log(resp.communities)
      var reddithtml="<table><tr><td>Community</td><td>Members</td></tr>";
      for(let i=0; i<resp.communities.length; i++){
        var coArr = resp.communities[i];
        reddithtml+="<tr><td><a href=\'https://www.reddit.com"+coArr[2]+"\'>"+coArr[0]+"</a></td><td>"+coArr[1]+"</td></tr>";
      }
      redditDiv.innerHTML = reddithtml;
      
      linkedinjobsDiv.innerHTML = SILUtilAbbreviate(resp.liJobs);
      linkedinnewjobsDiv.innerHTML = SILUtilAbbreviate(resp.liNewJobs);

    });
  };
  button.onclick = SHALLILEARN;
  form.onsubmit = SHALLILEARN;
};
