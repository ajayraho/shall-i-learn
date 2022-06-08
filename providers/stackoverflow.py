import requests
from bs4 import BeautifulSoup
from datetime import date
from collections import Counter

class StackOverflowProvider:
	def __init__(self, query):
		self.query = query
		self.totalPossiblePages = 0
	def getTotalQuestions(self):
		try:
			req=requests.get(url='https://stackoverflow.com/questions/tagged/'+self.query)
			soup=BeautifulSoup(req.text,"html.parser")
			nq=soup.find_all("div",class_="fs-body3 flex--item fl1 mr12 sm:mr0 sm:mb12")
			count = ''.join(filter(str.isdigit,nq[0].text.strip()))
			nq=soup.find("div",class_="s-pagination site1 themed pager float-left")
			self.totalPossiblePages = int(nq.find_all("a")[-2].text)			
			return {'questionsCount': count}
		except Exception as e:
			return {'questionsCount': 0, 'stackoverflowError': str(e)}
	def getTagsAndTimeDistribution(self):
		try:
			ls=[]
			tar=[]
			rangevar=61
			if rangevar > self.totalPossiblePages:
				rangevar = self.totalPossiblePages
			for page in range(1,rangevar):
				req=requests.get(url='https://stackoverflow.com/questions/tagged/{}?tab=active&page={}&pagesize=50'.format(self.query,page))
				soup=BeautifulSoup(req.text,"html.parser")
				nq=soup.find_all("div",class_="s-post-summary--meta")
				for i in nq:
					a = i.find_all("a", href=True)
					ts = [j.text for j in a][1:-3]
					tm = [[j.text for j in a][-1]]
					ls+=ts
					tar+=tm
			currYr = date.today().year
			yrs = [str(currYr-i) for i in range(1, 100) if currYr-i>2007] #WORKS UNTIL YEAR 3022 :)
			tdic = {'min':0, 'hour': 0, 'day': 0, 'month':0, 'year':0}

			for i in tar:
				if "min" in i:
					tdic['min'] += 1
				if "hour" in i:
					tdic['hour'] += 1
				if "day" in i:
					tdic['day'] += 1
				if any(mo in i for mo in ["year", *yrs]):
					tdic['year'] += 1
				elif any(mo in i for mo in ["month", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov"]):
					tdic['month'] += 1
			tgSrtar = Counter(ls).most_common()
			ms = [i[0] for i in tgSrtar]
			lim = 10
			if lim>len(ms):
				lim = len(ms)
			ms = tgSrtar[:lim]
			return {"timeDistribution": tdic,"tags": ms}
		except Exception as e:
			return {"timeDistribution": {}, "tags": [], "stackoverflowTagTimeError": str(e)}