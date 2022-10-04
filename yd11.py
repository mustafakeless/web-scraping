from email import header
import requests
from bs4 import BeautifulSoup
"""header={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"
}"""

r=requests.get("https://www.n11.com/bilgisayar/dizustu-bilgisayar")
#print(r.status_code)
s=BeautifulSoup(r.content,"lxml")
laptops=s.find_all("li",attrs={"class":"column"})
#print(laptops)
for laptop in laptops:
    link=laptop.find_all("div",attrs={"class":"pro"})
    for f in link:
        a=list(map(lambda lap: lap.find("a").get("href"),link)) 
        print(a[0])
