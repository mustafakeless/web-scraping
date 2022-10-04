from email import header
import requests
from bs4 import BeautifulSoup
"""header={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"
}"""

r=requests.get("https://www.trendyol.com/laptop-x-c103108")
#print(r.status_code)
s=BeautifulSoup(r.content,"lxml")
laptops=s.find_all("div",attrs={"class":"p-card-wrppr with-campaign-view"})
#print(laptops)
for laptop in laptops:
    link=laptop.find_all("div",attrs={"class":"p-card-chldrn-cntnr card-border"})
    a=list(map(lambda lap:"https://www.trendyol.com" +lap.find("a").get("href"),link)) 
    print(a)




   