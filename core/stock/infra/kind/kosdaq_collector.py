import pandas as pd
from .helpers import mapper

KOSDAQ_STOCK_LIST = 'http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13&marketType=kosdaqMkt'


class KosdaqCollector:
    def collect(self):
        df = pd.read_html(KOSDAQ_STOCK_LIST)[0]
        return [mapper(row) for _, row in df.iterrows()]
