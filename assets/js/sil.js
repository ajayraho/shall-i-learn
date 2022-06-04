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
  const SILBody = document.getElementById("SILBody")


  const turnOnLoaders = () => {
    const loader = "<div class=\"lcon\"><div class=\"lds-ellipsis\"><div></div><div></div><div></div><div></div></div></div>";
    linechartDiv.innerHTML = loader;
    regionschartDiv.innerHTML = loader;
    gitReposDiv.innerHTML = loader;
    gitTopicsDiv.innerHTML = loader;
    stackoverflowQuestionsDiv.innerHTML = loader;
    redditDiv.innerHTML = loader;
    linkedinjobsDiv.innerHTML = loader;
    linkedinnewjobsDiv.innerHTML = loader;
  }
  const SHALLILEARN = async function (e) {
    e.preventDefault();
    if(input.value != "") {
    turnOnLoaders();
    SILBody.style.display = "block";
    
    window.scrollTo(0, 450);
    const serverURL = "https://shallilearn.herokuapp.com/sil/"
    const localURL = "http://127.0.0.1:8000/sil/"
    
    await fetch(localURL, {
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
        var data = google.visualization.arrayToDataTable([["Day", "Interest"], ...arr]);
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
      var reddithtml="";
      for(let i=0; i<resp.communities.length; i++){
        var coArr = resp.communities[i];
        reddithtml+="<tr><td style=\'width:50%\'><a target=\'_blank\' href=\'https://www.reddit.com"+coArr[2]+"\'>"+coArr[0]+"</a></td><td>"+coArr[1]+"</td></tr>";
      }
      redditDiv.innerHTML = reddithtml;
      
      linkedinjobsDiv.innerHTML = "<abbr title='"+resp.liJobs+"'>"+SILUtilAbbreviate(resp.liJobs)+"</abbr>";
      linkedinnewjobsDiv.innerHTML = "<abbr title='"+resp.liNewJobs+"'>"+SILUtilAbbreviate(resp.liNewJobs)+"</abbr>";

    });
  } else {
    input.style.border = "1px solid red";
    setTimeout(() => {
      input.style.border = "1px solid #ced4da";
    }, 1000);
  }
}
  button.onclick = SHALLILEARN;
  form.onsubmit = SHALLILEARN;

};
