import pandas as pd                        
from pytrends.request import TrendReq
from datetime import datetime

class GoogleTrendsPovider:
  def __init__(self, query):
    self.query = query
  def getOverTime(self):
    pytrend = TrendReq()
    pytrend.build_payload(kw_list=[self.query])
    df = pytrend.interest_over_time()
    df = df.drop('isPartial', axis=1)
    df = df.reset_index()
    df.rename(columns={df.columns[1]:"value"}, inplace=True)

    da = []
    da += [i.strftime("%Y-%m-%d") for i in df['date']]
    df['date'] = da
    ls = df[['date', 'value']].values.tolist()
    return ls