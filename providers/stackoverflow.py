import pandas as pd
import requests
from bs4 import BeautifulSoup

class StackOverflowPovider:
  def __init__(self, query):
    self.query = query
  def getTotalQuestions(self):
    try:
      req=requests.get(url='https://stackoverflow.com/questions/tagged/'+self.query)
      soup=BeautifulSoup(req.text,"html.parser")
      nq=soup.find_all("div",class_="fs-body3 flex--item fl1 mr12 sm:mr0 sm:mb12")
      count = ''.join(filter(str.isdigit,nq[0].text.strip()))
      return {'questionsCount': count}
    except:
      return {'questionsCount': 0}