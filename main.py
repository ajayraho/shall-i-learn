from fastapi import FastAPI, Request
from typing import Union
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from providers.gtrends import GoogleTrendsPovider
from providers.github import GitHubProvider
from providers.stackoverflow import StackOverflowProvider
from providers.reddit import RedditProvider
from providers.linkedin import LinkedinProvider
from providers.jobs import MiscJobsProvider
from urllib import parse
app = FastAPI()

templates = Jinja2Templates(directory = "templates")
app.mount("/assets", StaticFiles(directory="assets"), name="assets")
@app.get("/")
async def read_root(request: Request):
	return templates.TemplateResponse("index.html", {"request": request})

@app.post("/sil/")
async def sil(info: Request):
	req = await info.json()

	gtprovider = GoogleTrendsPovider(req['query'])
	GTPTime = gtprovider.getOverTime()
	GTPRegn = gtprovider.getOverRegion()

	urlencodedQuery = parse.quote_plus(req['query'])

	gitprovider = GitHubProvider(urlencodedQuery)
	gitData = gitprovider.getData()

	stackoverflow = StackOverflowProvider(req['query'].replace(' ','-'))
	stackoverflowTotalQns = stackoverflow.getTotalQuestions()
	stackoverflowTagsTime = stackoverflow.getTagsAndTimeDistribution()
	
	redditprovider = RedditProvider(urlencodedQuery)
	redditCommunities = redditprovider.getCommunities()
	
	linkedinprovider = LinkedinProvider(urlencodedQuery)
	linkedinJobs = linkedinprovider.getJobs()

	miscprovider = MiscJobsProvider(urlencodedQuery)
	miscJobs = miscprovider.getJobs()

	return {
		"req": req,
		"GTPTime": GTPTime,
		"GTPRegn": GTPRegn,
		**gitData,
		**stackoverflowTotalQns,
		**redditCommunities,
		**linkedinJobs,
		**miscJobs,
		**stackoverflowTagsTime
	}