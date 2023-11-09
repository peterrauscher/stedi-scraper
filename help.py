from bs4 import BeautifulSoup
from requests_ratelimiter import LimiterSession
import json

session = LimiterSession(per_minute=45)


def grab_next_data(url):
    html = session.get(url).text
    soup = BeautifulSoup(html)
    jsonstr = soup.find(id="__NEXT_DATA__").string
    return json.loads(jsonstr)
