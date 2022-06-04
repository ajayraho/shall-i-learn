import requests
from bs4 import BeautifulSoup

class LinkedinProvider:
  def __init__(self, query):
    self.query = query
  def getJobs(self):
    jc=""
    nc=""
    html=""
    try:
      req=requests.get(url='https://www.linkedin.com/jobs/search?keywords={}&location=&geoId=&trk=homepage-jobseeker_jobs-search-bar_search-submit&position=1&pageNum=0'.format(self.query))
      soup=BeautifulSoup(req.text,"html.parser")
      html=req.text
      jc=soup.find("span",class_="results-context-header__job-count")
      nc=soup.find("span",class_="results-context-header__new-jobs")
      return {
        'liJobs':''.join(filter(str.isdigit,jc.text.strip())),
        'liNewJobs':''.join(filter(str.isdigit,nc.text.strip()))
      }
    except Exception as e:
      return {'liJobs':0,'liNewJobs':0, 'linkedinError': str(e), 'jc':jc, 'nc':nc, 'linkedinhtml':html}