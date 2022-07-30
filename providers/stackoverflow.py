import requests
from bs4 import BeautifulSoup
from datetime import date
from collections import Counter

class StackOverflowProvider:
	def __init__(self, query):
		self.query = query
		self.totalPossiblePages = 0
		self.logs = f"Initialized StackOverflowProvider({self.query})<br/>"
	def getTotalQuestions(self):
		try:
			self.logs += "Fetching total questions count...<br/>"
			req=requests.get(url='https://stackoverflow.com/questions/tagged/'+self.query)
			self.logs += "Processing...<br/>"
			soup=BeautifulSoup(req.text,"html.parser")
			nq=soup.find_all("div",class_="fs-body3 flex--item fl1 mr12 sm:mr0 sm:mb12")
			count = ''.join(filter(str.isdigit,nq[0].text.strip()))
			nq=soup.find("div",class_="s-pagination site1 themed pager float-left")
			self.totalPossiblePages = int(nq.find_all("a")[-2].text)
			self.logs += "Fetched total questions count.<br/>"
			return {'questionsCount': count, 'logs':self.logs}
		except Exception as e:
			self.logs += f"Error while fetching total questions count. <i>{e}</i><br/>"
			return {'questionsCount': 0, 'stackoverflowError': str(e), 'logs':self.logs}
	def getTagsAndTimeDistribution(self):
		try:
			ls=[]
			tar=[]
			rangevar=61
			if rangevar > self.totalPossiblePages:
				rangevar = self.totalPossiblePages
			self.logs += "Fetching tags and time distribution of questions...<br/>"
			count=0
			for page in range(1,rangevar):
				count = count+1
				self.logs += f"Batch {count}/{rangevar-1}: "
				try:
					self.logs += " Fetching... "
					req=requests.get(url='https://stackoverflow.com/questions/tagged/{}?tab=active&page={}&pagesize=50'.format(self.query,page))
					self.logs += " Processing... "
					soup=BeautifulSoup(req.text,"html.parser")
					nq=soup.find_all("div",class_="s-post-summary--meta")
					for i in nq:
						a = i.find_all("a", href=True)
						ts = [j.text for j in a][1:-3]
						tm = [[j.text for j in a][-1]]
						ls+=ts
						tar+=tm
					self.logs += " Done.<br/>"
				except Exception as e:
					self.logs += f"Batch {count}/{rangevar-1} failed. <i>{e}</i><br/>Continuing with data obtained so far.<br/>"
			self.logs += "Processing data...<br/>"
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
			if ms[0] == self.query:
				ms = tgSrtar[1:lim+1]
			else:
				ms = tgSrtar[:lim]

			self.logs += "Done.<br/>"
			self.logs += "StackoverflowProvider data fetch sequence finished.<br/><b>Finished.</b>"
			return {"timeDistribution": tdic, "tags": ms, "logs": self.logs, "qpages": rangevar}
		except Exception as e:
			self.logs += f"Error while fetching tags and time distribution of questions. <i>{e}</i><br/><b>Finished.</b>"
			return {"timeDistribution": {}, "tags": [], "stackoverflowTagTimeError": str(e), "logs":self.logs}