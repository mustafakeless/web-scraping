from email import header
import requests
from bs4 import BeautifulSoup
import sqlite3

con = sqlite3.connect("laptops.db")
cursor = con.cursor()

r=requests.get("https://www.trendyol.com/monster/abra-a5-v16-7-3-intel-core-i5-11400h-16gb-ram-500gb-ssd-4gb-gtx1650-freedos-15-6-fhd-144hz-p-133966690")
r=requests.get("https://www.trendyol.com/acer/an515-57-i5-11400h-8gb-ram-512ssd-4gb-3050-15-6-fhd144hz-windows-11-siyah-laptop-nh-qeley-002-p-356799756")
r=requests.get("https://www.trendyol.com/asus/rog-strix-g15-4-nesil-ryzen-7-4800h-16gb-512gb-ssd-15-6inc-rtx3050-4gb-w11-p-349603138?boutiqueId=613344&merchantId=624588")
r=requests.get("https://www.trendyol.com/lenovo/ideapad-gaming-3-82k100cltx-i7-11370h-16gb-1tb-256ssd-rtx3050-15-6-full-hd-freedos-tasinabili-p-294614443?boutiqueId=613344&merchantId=105013")
r=requests.get("https://www.trendyol.com/msi/katana-gf66-11-nesil-core-i7-11800h-16gb-1tb-ssd-15-6inc-rtx3060-6gb-freedos-p-349585157?boutiqueId=613344&merchantId=624588")
s=BeautifulSoup(r.content,"lxml")

ayr=s.find_all("ul",attrs={"class":"detail-attr-container"})
fiyat=s.find("span",attrs={"class":"prc-dsc"}).text.replace("TL","").replace(",99","")

marka=s.find("h1",attrs={"class":"pr-new-br"}).text.split(" ")
print(marka[0])

print(fiyat)
for ayr2 in ayr:
    detay=ayr2.find_all("li")
    list=[]
    list1=[]
    
for i in detay:
    list.append(i.find("span").text)
    list1.append(i.find("b").text)

def tabloolustur():
    cursor.execute("CREATE TABLE IF NOT EXISTS laptop (Marka TEXT, ModelAdı TEXT, ModelNo TEXT, İşletimsistemi TEXT,İşlemcitipi TEXT,İşlemcinesli TEXT,RAM INT,DiskBoyutu INT,DiskTürü TEXT,EkranBoyutu FLOAT,Puanı FLOAT,Fiyat INT,Site TEXT)")
tabloolustur() 
def degerekle1():
        cursor.execute("INSERT INTO laptop VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)", (marka[0],marka[1]+" "+marka[2],marka[3],list1[2],list1[0],list1[30],list1[5],list1[1],"SSD",list1[15],9.0,fiyat,'Trendyol'))
        con.commit()
def degerekle2():
        cursor.execute("INSERT INTO laptop VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)", (marka[0],marka[1]+" "+marka[2],marka[3],list1[1],list1[0],list1[14],list1[3],list1[4],"HDD",list1[19],9.0,fiyat,'Trendyol'))
        con.commit()
        
for j in list1:
    if j=="HDD Yok":
        degerekle1()
        con.close()  
    elif j=="SSD Yok":
        degerekle2()
        con.close()          
      
print(list)
print(list1)


                 
       