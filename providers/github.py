import urllib.request, json 

class GitHubProvider:
  def __init__(self, query):
    self.query = query
    self.logs = f"Initialized GitHubProvider({self.query})<br/>";
  def getData(self):
    ls = {}
    rc = 0
    self.logs += "Initiating data fetch sequence...<br/>"
    try:
      self.logs += "Fetching repositories count 1/2...<br/>"
      with urllib.request.urlopen("https://api.github.com/search/repositories?q=language:"+self.query) as url:
        data = json.loads(url.read().decode())
        self.logs += "Fetched repositories count.<br/>"
        rc = data['total_count']
    except Exception as e:
      self.logs += f"Error while fetching repositories count. <i>LANG</i><br/>"
      rc = 0

    try:
      self.logs += "Fetching repositories count 2/2...<br/>"
      with urllib.request.urlopen("https://api.github.com/search/repositories?q="+self.query) as url:
        data = json.loads(url.read().decode())
        self.logs += "Fetched repositories count.<br/>"
        rc = rc + data['total_count']
    except Exception as e:
      self.logs += f"Error while fetching repositories count. <i>{e}</i><br/>"
      ls.update({'gitReposError': str(e)})
    ls['repos'] = rc


    try:
      self.logs += "Fetching topics count...<br/>"
      with urllib.request.urlopen("https://api.github.com/search/topics?q="+self.query) as url:
        self.logs += "Fetched topics.<br/>"
        data = json.loads(url.read().decode())
        ls['topics'] = data['total_count']
    except:
      self.logs += f"Error while fetching topics count. <i>{e}</i><br/>"
      ls.update({'gitTopicsError': str(e)})
      ls['topics'] = 0
    
    self.logs += "GitHubProvider data fetch sequence finished.<br/>Waiting for next provider...<br/>"
    ls['logs'] = self.logs
    
    return ls