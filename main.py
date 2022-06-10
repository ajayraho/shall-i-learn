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
@app.post("/sil/googleTrends")
async def googleTrends(info: Request):
	req = await info.json()
	gtprovider = GoogleTrendsPovider(req['query'])
	GTPTime = gtprovider.getOverTime()
	GTPRegn = gtprovider.getOverRegion()
	return {
		"GTPTime": GTPTime,
		"GTPRegn": GTPRegn,
	}
@app.post("/sil/gitHub")
async def gitHub(info: Request):
	req = await info.json()
	gitprovider = GitHubProvider(parse.quote_plus(req['query']))
	gitData = gitprovider.getData()
	return {
		**gitData
	}
@app.post("/sil/stackoverflow")
async def stackoverflow(info: Request):
	req = await info.json()
	stackoverflow = StackOverflowProvider(req['query'].replace(' ','-'))
	stackoverflowTotalQns = stackoverflow.getTotalQuestions()
	stackoverflowTagsTime = stackoverflow.getTagsAndTimeDistribution()
	return {
		**stackoverflowTotalQns,
		**stackoverflowTagsTime
	}
@app.post("/sil/reddit")
async def reddit(info: Request):
	req = await info.json()
	redditprovider = RedditProvider(parse.quote_plus(req['query']))
	redditCommunities = redditprovider.getCommunities()
	return {
		**redditCommunities
	}
@app.post("/sil/linkedin")
async def linkedin(info: Request):
	req = await info.json()
	linkedinprovider = LinkedinProvider(parse.quote_plus(req['query']))
	linkedinJobs = linkedinprovider.getJobs()
	return {
		**linkedinJobs
	}
@app.post("/sil/miscjobs")
async def miscjobs(info: Request):
	req = await info.json()
	miscprovider = MiscJobsProvider(parse.quote_plus(req['query']))
	miscJobs = miscprovider.getJobs()
	return {
		**miscJobs
	}