import requests
from bs4 import BeautifulSoup
from lxml import etree
class MiscJobsProvider:
	def __init__(self, query):
		self.query = query
	def getJobs(self):
		jc=""
		html=""
		response = {}
		try:
			req=requests.get(url='https://indeed.com/jobs?q={}&l&from=searchOnHP&vjk=b6a83fffa19901da'.format(self.query))
			soup=BeautifulSoup(req.text,"html.parser")
			jc=soup.find("div",attrs={"id":"searchCountPages"})
			html=req.text
			response.update({'indeedJobs':''.join(filter(str.isdigit,jc.text.strip().split()[3]))})
		except Exception as e:
			response.update({'indeedJobs':0,'flexJobs':0,'indeedJobsError': str(e), 'injc':jc, 'indeedhtml':html})

		try:
			req1=requests.get(url="https://www.flexjobs.com/search?search={}&location=".format(self.query))
			soup1 = BeautifulSoup(req1.text, "html.parser")
			dom = etree.HTML(req1.text)			
			response.update({'flexJobs':''.join(filter(str.isdigit,dom.xpath('//*[@id="content-main"]/div[2]/div/div/div[1]/div[2]/div[1]/h4')[0].text.strip().split()[4]))})
		except Exception as e:
			response.update({'flexJobs':0,'flexJobsError': str(e)})
		return response