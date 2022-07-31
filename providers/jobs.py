import requests
from bs4 import BeautifulSoup
from lxml import etree
class MiscJobsProvider:
	def __init__(self, query):
		self.query = query
		self.logs = f"Initialized MiscJobsProvider({self.query})<br/>"
	def getJobs(self):
		jc=""
		html=""
		response = {}
		self.logs += "Initiating data fetch sequence...<br/>"
		try:
			self.logs += "Fetching indeed jobs...<br/>"
			req=requests.get(url='https://indeed.com/jobs?q={}&l&from=searchOnHP&vjk=b6a83fffa19901da'.format(self.query),timeout=5)
			self.logs += "Processing...<br/>"
			soup=BeautifulSoup(req.text,"html.parser")
			jc=soup.find("div",attrs={"id":"searchCountPages"})
			html=req.text
			response.update({'indeedJobs':''.join(filter(str.isdigit,jc.getText().strip().split()[3]))})
			self.logs += "Fetched indeed jobs.<br/>"
		except Exception as e:
			self.logs += f"Error while fetching indeed jobs. <i>{e}</i><br/>"
			response.update({'indeedJobs':0,'flexJobs':0,'indeedJobsError': str(e), 'injc':jc, 'indeedhtml':html})

		try:
			self.logs += "Fetching FlexJobs jobs...<br/>"
			req1 = requests.get(url="https://www.flexjobs.com/search?search={}&location=".format(self.query),timeout=5)
			self.logs += "Processing...<br/>"
			dom = etree.HTML(req1.text)			
			response.update({'flexJobs':''.join(filter(str.isdigit,dom.xpath('//*[@id="content-main"]/div[2]/div/div/div[1]/div[2]/div[1]/h4')[0].text.strip().split()[4]))})		
			self.logs += "Fetched FlexJobs jobs.<br/>"
		except Exception as e:
			self.logs += f"Error while fetching FlexJobs jobs. <i>{e}</i><br/>"
			response.update({'flexJobs':0,'flexJobsError': str(e)})
		self.logs += "MiscJobsProvider data fetch sequence finished.<br/>Waiting for next provider...<br/>"
		response.update({'logs':self.logs})
		return response