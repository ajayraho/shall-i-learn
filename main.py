from fastapi import FastAPI, Request
from typing import Union
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from gtrends import GoogleTrendsPovider
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
    return {
        "req": req,
        "GTPTime": GTPTime,
        "GTPRegn": GTPRegn
    }