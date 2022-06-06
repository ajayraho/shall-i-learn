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
	const flexjobsDiv = document.getElementById("flexjobs_div");
	// const linkedinnewjobsDiv = document.getElementById("linkedinnew_div");
	const indeedjobsDiv = document.getElementById("indeed_div");
	const tagsChartDiv = document.getElementById("tags_chart_div");
	const tagsLegends = document.getElementById("tags_legends");
	const timeDistributionDiv = document.getElementById("timeDistribution_div");
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
		//linkedinnewjobsDiv.innerHTML = loader;
		indeedjobsDiv.innerHTML = loader;
		flexjobsDiv.innerHTML = loader;
		tagsChartDiv.innerHTML = loader;
		timeDistributionDiv.innerHTML = loader;
	}
	const SHALLILEARN = async function (e) {
		e.preventDefault();
		if(input.value != "") {
		turnOnLoaders();
		SILBody.style.display = "block";
		
		window.scrollTo(0, 450);
		const serverURL = "https://shallilearn.herokuapp.com/sil/"
		const localURL = "http://127.0.0.1:8000/sil/"
		
		await fetch(serverURL, {
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
				drawTagsPieChart();
				drawTimeDistrubutionBarChart();
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
					height: 250,
					chartArea:{
						width:'90%', 
						height:'90%' 
					},
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
			const colors = ["#3464c3","#dc3912","#fb9b05","#14941c","#990099","#0099c6","#dd4477","#66aa00","#b82e2e","#316395" ]
			const pieColors = ()=>{
				var obj={}
				for(var i=0; i<10;i++){
					obj[i] = {color:colors[i]}
				}
				return obj
			}

			function drawTagsPieChart(){
				var data = google.visualization.arrayToDataTable([
					["Tag","Use"],
					...resp.tags
				]);
				var options = {
					width: 250,
					height: 250,
					is3d:true,
					pieHole:0.4,
					legend:{
						position:"none"
					},
					chartArea:{
						width:"75%",
						height:"75%",
					},
					animation: {
						startup: true,
						duration: 750,
						easing: "out",
					},
					slices:pieColors()
				};
				var chart = new google.visualization.PieChart(tagsChartDiv);
				chart.draw(data, options);
			}
			var tagsHTML=""
			for(let i=0; i<resp.tags.length; i++){
				tagsHTML+="<tr><td style=\"width:12px;padding:4px;\"><div style=\"background-color:"+colors[i]+";width:10px;height:10px;border-radius:50%;margin-left:auto;\"></div></td><td style=\"padding-top:4px;padding-bottom:4px;padding-right:4px;\">"+resp.tags[i][0]+"</td></tr>";
			}
			tagsLegends.innerHTML=tagsHTML


			function drawTimeDistrubutionBarChart() {
				var rawData = Object.keys(resp.timeDistribution).map(i=>[i,resp.timeDistribution[i]])
				rawData = [
					['Minutes', rawData[0][1]],
					['Hours', rawData[1][1]],
					['Months', rawData[2][1]],
					['Years', rawData[3][1]]
				]
				var dataArr=[]
				for(var i=0; i<rawData.length;i++){
				    if(rawData[i][1]!=0){
				        dataArr.push(rawData[i]);
				    }
				}
				var data = google.visualization.arrayToDataTable([
					["Time", "Questions asked"],
					...dataArr
				]);
				var options = {
					width: 300,
					height: 300,
					legend:{
						position:'none'
					},
					chartArea:{
						width:'80%', 
						height:'80%' 
					},
					animation: {
						startup: true,
						duration: 750,
						easing: "out",
					},
				};
				var chart = new google.visualization.ColumnChart(timeDistributionDiv);
				chart.draw(data, options);
			}



			//GitHub
			gitReposDiv.innerHTML = "<abbr title='"+resp.repos+"'>"+SILUtilAbbreviate(resp.repos)+"</abbr>";
			gitTopicsDiv.innerHTML = "<abbr title='"+resp.topics+"'>"+SILUtilAbbreviate(resp.topics)+"</abbr>";

			//stackoverflow
			stackoverflowQuestionsDiv.innerHTML = "<abbr title='"+resp.questionsCount+"'>"+SILUtilAbbreviate(resp.questionsCount)+"</abbr>";
		
			var reddithtml="";
			for(let i=0; i<resp.communities.length; i++){
				var coArr = resp.communities[i];
				reddithtml+="<tr><td style=\'width:50%\'><a target=\'_blank\' href=\'https://www.reddit.com"+coArr[2]+"\'>"+coArr[0]+"</a></td><td>"+coArr[1]+"</td></tr>";
			}
			redditDiv.innerHTML = reddithtml;
			
			linkedinjobsDiv.innerHTML = "<abbr title='"+resp.liJobs+"'>"+SILUtilAbbreviate(resp.liJobs)+"</abbr>";
			//linkedinnewjobsDiv.innerHTML = "<abbr title='"+resp.liNewJobs+"'>"+SILUtilAbbreviate(resp.liNewJobs)+"</abbr>";
			
			indeedjobsDiv.innerHTML = "<abbr title='"+resp.indeedJobs+"'>"+SILUtilAbbreviate(resp.indeedJobs)+"</abbr>";
			
			flexjobsDiv.innerHTML = "<abbr title='"+resp.flexJobs+"'>"+SILUtilAbbreviate(resp.flexJobs)+"</abbr>";

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
