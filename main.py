from fastapi import FastAPI, Request
from typing import Union
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from providers.gtrends import GoogleTrendsPovider
from providers.github import GitHubProvider
from providers.stackoverflow import StackOverflowPovider

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

    gitprovider = GitHubProvider(req['query'])
    gitData = gitprovider.getData()

    stackoverflow = StackOverflowPovider(req['query'])
    stackoverflowTotalQns = stackoverflow.getTotalQuestions()

    return {
        "req": req,
        "GTPTime": GTPTime,
        "GTPRegn": GTPRegn,
        **gitData,
        **stackoverflowTotalQns
    }