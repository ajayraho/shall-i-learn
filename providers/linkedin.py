import requests
from bs4 import BeautifulSoup

class LinkedinProvider:
  def __init__(self, query):
    self.query = query
  def getJobs(self):
    try:
      req=requests.get(url='https://www.linkedin.com/jobs/search?keywords={}&location=&geoId=&trk=homepage-jobseeker_jobs-search-bar_search-submit&position=1&pageNum=0'.format(self.query))
      soup=BeautifulSoup(req.text,"html.parser")
      jc=soup.find_all("span",class_="results-context-header__job-count")
      nc=soup.find_all("span",class_="results-context-header__new-jobs")
      return {
        'liJobs':''.join(filter(str.isdigit,jc[0].text.strip())),
        'liNewJobs':''.join(filter(str.isdigit,nc[0].text.strip()))
      }
    except:
      return {'liJobs':0,'liNewJobs':0}