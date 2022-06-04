import requests
from bs4 import BeautifulSoup

class MiscJobsProvider:
	def __init__(self, query):
		self.query = query
	def getJobs(self):
		jc=""
		nc=""
		html=""
		try:
			req=requests.get(url='https://indeed.com/jobs?q={}&l&from=searchOnHP&vjk=b6a83fffa19901da'.format(self.query))
			soup=BeautifulSoup(req.text,"html.parser")
			jc=soup.find("div",attrs={"id":"searchCountPages"})
			html=req.text
			return {
				'indeedJobs':''.join(filter(str.isdigit,jc.text.strip().split()[3]))
			}
		except Exception as e:
			return {'indeedJobs':0,'error': str(e), 'jc':jc, 'nc':nc, 'jobhtml':html}