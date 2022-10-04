from email import header
import requests
from bs4 import BeautifulSoup

r=requests.get("https://www.trendyol.com/monster/abra-a5-v16-7-3-intel-core-i5-11400h-16gb-ram-500gb-ssd-4gb-gtx1650-freedos-15-6-fhd-144hz-p-133966690")
s=BeautifulSoup(r.content,"lxml")

ayr=s.find_all("ul",attrs={"class":"detail-attr-container"})
for ayr2 in ayr:
    detay=ayr2.find_all("li")
    for i in detay:
        son=i.find("span").text
        son2=i.find("b").text
        
        print(f"{son}={son2}")
        
       