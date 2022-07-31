import requests
from bs4 import BeautifulSoup

class LinkedinProvider:
  def __init__(self, query):
    self.query = query
    self.logs = f"Initialized LinkedinProvider({self.query})<br/>"
  def getJobs(self):
    jc=""
    nc=""
    html=""
    try:
      self.logs += "Fetching LinkedIn jobs...<br/>"
      req=requests.get(url='https://www.linkedin.com/jobs/search?keywords={}&location=&geoId=&trk=homepage-jobseeker_jobs-search-bar_search-submit&position=1&pageNum=0'.format(self.query),timeout=5)
      self.logs += "Processing...<br/>"
      soup=BeautifulSoup(req.text,"html.parser")
      html=req.text
      jc=soup.find("span",class_="results-context-header__job-count")
      nc=soup.find("span",class_="results-context-header__new-jobs")
      self.logs += "Fetched LinkedIn jobs...<br/>LinkedInProvider data fetch sequence finished.<br/>Waiting for next provider...<br/>"

      return {
        'liJobs':''.join(filter(str.isdigit,jc.text.strip())),
        'liNewJobs':''.join(filter(str.isdigit,nc.text.strip())),
        'logs': self.logs
      }
    except Exception as e:
      self.logs += f"Error while fetching LinkedIn jobs. <i>{e}</i><br/>"
      return {'liJobs':0,'liNewJobs':0, 'linkedinError': str(e), 'jc':jc, 'linkedinhtml':html, 'logs':self.logs}