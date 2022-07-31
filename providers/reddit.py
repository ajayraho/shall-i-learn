import requests
from bs4 import BeautifulSoup

class RedditProvider:
  def __init__(self, query):
    self.query = query
    self.logs = "Initialized RedditProvider<br/>"
  def getCommunities(self):
    try:
      self.logs += "Fetching data...<br/>"
      req = requests.get(
          url='https://www.reddit.com/search/?q={}&type=sr'.format(self.query), timeout=5)
      self.logs += "Processing...<br/>"
      soup=BeautifulSoup(req.text,"html.parser")
      nq=soup.find_all("h6",class_="_2torGbn_fNOMbGw3UAasPl")
      mm=soup.find_all("p",class_="_3CUjJH8t2eFynKUAv1ER7C")
      hr=soup.find_all("a",attrs={"data-testid":"subreddit-link"})
      self.logs += "Done.<br/>"
      self.logs += "RedditProvider data fetch sequence finished.<br/>Waiting for next provider...<br/>"
      return {"communities":[(i.text,j.text[1:].replace(' Members', '').upper(), k['href']) for i,j,k  in zip(nq, mm, hr)], "logs":self.logs}
    except Exception as e:
      self.logs += f"Error while fetching data. <i>{e}</i><br/>"
      return {"communities":[], 'redditError': str(e), "logs":self.logs}