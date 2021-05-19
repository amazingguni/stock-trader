import urllib
import re
from datetime import date, timedelta

import requests


class HolidayCrawler:
    def crawl(self, year):
        otp = self.__get_opt(year)
        return self.__get_holidays(otp)

    def __get_opt(self, year):
        res_otp = requests.get(
            'https://open.krx.co.kr/contents/COM/GenerateOTP.jspx',
            params={
                'name': 'fileDown',
                'filetype': 'csv',
                'url': 'MKD/01/0110/01100305/mkd01100305_01',
                'search_bas_yy': year,
            },
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        return res_otp.text

    def __get_holidays(self, otp):
        res_csv = requests.post(
            'http://file.krx.co.kr/download.jspx',
            headers={
                'User-Agent': 'Mozilla/5.0',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Referer': 'http://marketdata.krx.co.kr/mdi',
            },
            data=urllib.parse.urlencode({'code': otp})
        )

        result = res_csv.text
        match = re.findall(
            r'.*?\,(\d+)-(\d+)-(\d+)(?:\s\(.*?\))?\,(.*?)\s*\,(.*)',
            result
        )
        return [date(int(each[0]), int(each[1]), int(each[2]))
                for each in match]


def is_weekend(d: date):
    SAT = 5
    SUN = 6
    return d.weekday() in [SAT, SUN]


def get_last_market_opening_day(from_date: date = None):
    holidays = HolidayCrawler().crawl(from_date.year)
    holidays += HolidayCrawler().crawl(from_date.year - 1)
    last_opening_day = from_date if from_date else date.today()
    while True:
        if is_weekend(last_opening_day) or last_opening_day in holidays:
            last_opening_day -= timedelta(days=1)
            continue
        return last_opening_day
