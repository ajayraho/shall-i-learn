import urllib.request, json 

class GitHubProvider:
  def __init__(self, query):
    self.query = query
  def getData(self):
    ls = {}
    rc = 0
    try:
      with urllib.request.urlopen("https://api.github.com/search/repositories?q=language:"+self.query) as url:
        data = json.loads(url.read().decode())
        rc = rc + data['total_count']
    except:
      print("Error1")
      rc = 0

    try:
      with urllib.request.urlopen("https://api.github.com/search/repositories?q="+self.query) as url:
        data = json.loads(url.read().decode())
        rc = rc + data['total_count']
    except:
      print("Error2")
      rc = 0

    ls['repos'] = rc

    try:
      with urllib.request.urlopen("https://api.github.com/search/topics?q="+self.query) as url:
        data = json.loads(url.read().decode())
        ls['topics'] = data['total_count']
    except:
      ls['topics'] = 0
    return ls