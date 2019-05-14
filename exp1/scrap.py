import json
import requests
from bs4 import BeautifulSoup
class Scraper(object):
	def __init__(self):
		self.url = “https://www.standardmedia.co.ke"
 
	def scrape_site(self):
		res = requests.get(self.url)
		html = BeautifulSoup(res.content, ‘html.parser’)
		if html:
		div = html.find(“div”, class_=”col-xs-6 col-md-6 zero”)
		ul = div.find_all(“ul”, class_=”sub-stories-2")
		data = []
		for item in ul:
			img_url = item.find(“img”).get(“src”)
			text = item.find(“img”).get(“alt”)
			link = item.find(“li”).find(“a”).get(“href”)
			data.append({
			‘title’: text,
			‘link’: link,
			‘img’: img_url
			})
		return json.dumps(data, indent=2)
scraper = Scraper()
print(scraper.scrape_site())