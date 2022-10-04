from email import header
import requests
from bs4 import BeautifulSoup
header={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"
}

r=requests.get("https://www.trendyol.com/laptop-x-c103108",headers=header)
#print(r.status_code)
s=BeautifulSoup(r.content,"lxml")
laptops=s.find_all("div",attrs={"class":"p-card-wrppr with-campaign-view"})
#print(laptops)
for laptop in laptops:
    link=laptop.find_all("div",attrs={"class":"p-card-chldrn-cntnr card-border"})
    a=list(map(lambda lap:"https://www.trendyol.com" +lap.find("a").get("href"),link)) 
    print(a)

    """for j in a:
        r1=requests.get(a[j])
        p=BeautifulSoup(r1.content,"lxml")
        ayr=p.find_all("ul",attrs={"class":"detail-attr-container"})
        for ayr2 in ayr:
            detay=ayr2.find_all("li")
            for i in detay:
                son=i.find("span").text
                son2=i.find("b").text
        
                print(f"{son}={son2}")"""


   