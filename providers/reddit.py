import requests
from bs4 import BeautifulSoup

class RedditProvider:
  def __init__(self, query):
    self.query = query
  def getCommunities(self):
    try:
      req=requests.get(url='https://www.reddit.com/search/?q={}&type=sr'.format(self.query))
      soup=BeautifulSoup(req.text,"html.parser")
      nq=soup.find_all("h6",class_="_2torGbn_fNOMbGw3UAasPl")
      mm=soup.find_all("p",class_="_3CUjJH8t2eFynKUAv1ER7C")
      hr=soup.find_all("a",attrs={"data-testid":"subreddit-link"})
      return {"communities":[(i.text,j.text[1:].replace(' Members', '').upper(), k['href']) for i,j,k  in zip(nq, mm, hr)]}
    except Exception as e:
      return {"communities":[], 'redditError': str(e)}