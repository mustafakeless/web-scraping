from email import header
from pyexpat import model
from time import sleep
import requests
from bs4 import BeautifulSoup
import sqlite3

con = sqlite3.connect("laptops.db")
cursor = con.cursor()
p=1
for page in range(1,4):
    url="https://www.n11.com/bilgisayar/dizustu-bilgisayar?ipg={}".format(page)
    print(url)
    r=requests.get(url).text
    s=BeautifulSoup(r,"lxml")
    laptops=s.find_all("li",attrs={"class":"column"})
    linklist=[]
    for laptop in laptops:
        link=laptop.find_all("div",attrs={"class":"pro"})
        for f in link:
                a=list(map(lambda lap: lap.find("a").get("href"),link))
                for u in a:
                    new_string = u.replace("['","").replace("']","")
                    linklist.append(new_string)  
    #print(linklist)
    for a in linklist:
        r1=requests.get(a)
        s1=BeautifulSoup(r1.content,"lxml")
        ayr=s1.find_all("div",attrs={"class":"unf-prop-context"})
        #fiyat=s1.find("div",attrs={"class":"newPrice"}).text.replace("TL","").replace(",99","")
        #marka=s1.find("h1",attrs={"class":"proName"}).text.split(" ")
        #print(marka[0])
        
        """try:
            puan=s1.find("strong").text
        except:
            puan="NR"
        print(float(puan))"""
        
        for ayr2 in ayr:
            detay=ayr2.find_all("li",attrs={"class":"unf-prop-list-item"})
            list=[]
            list1=[]
        for i in detay:
            list.append(i.find("p",attrs={"class":"unf-prop-list-title"}).text)
            list1.append(i.find("p",attrs={"class":"unf-prop-list-prop"}).text)
        def tabloolustur():
            cursor.execute("CREATE TABLE IF NOT EXISTS laptop (Marka TEXT, ModelAdı TEXT, ModelNo TEXT, İşletimsistemi TEXT,İşlemcitipi TEXT,İşlemcinesli TEXT,RAM INT,DiskBoyutu INT,DiskTürü TEXT,EkranBoyutu FLOAT,Puanı FLOAT,Fiyat INT,Site TEXT)")
        tabloolustur() 

        a=0    
        for j1 in list:
        
            if j1=="İşlemci":
                islemcitipi=list1[a]
            a=a+1                 
        a=0
        for j3 in list:
                if j3=="İşletim Sistemi":
                    isletimsistemi=list1[a]
                a=a+1    
        a=0            
        for j4 in list:
                if j4=="Bellek Kapasitesi":
                    ram=list1[a]
                a=a+1                     
        a=0
        for j5 in list:
                if j5=="Ekran Boyutu":
                    ekranboyutu=list1[a]
                a=a+1                
        a=0
        for j6 in list:
                if j6=="İşlemci Modeli":
                    islemcinesli=list1[a]
                a=a+1                 
        a=0
        for j7 in list:
                if j7=="Disk Türü":
                    diskturu=list1[a]
                a=a+1                 
        a=0
        for j8 in list:
                if j8=="Disk Kapasitesi":
                    diskboyutu=list1[a]     
                a=a+1                 
        a=0
        for j9 in list:
                if j9=="Marka":
                    marka=list1[a]     
                a=a+1                 
        a=0
        for j2 in list:
                if j2=="Model":
                    model=list1[a]     
                a=a+1                 
        a=0
        print(islemcitipi,isletimsistemi,diskturu,ram,diskboyutu,ekranboyutu,islemcinesli)
        def degerekle():
                cursor.execute("INSERT INTO laptop VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)", (marka,marka,model,isletimsistemi,islemcitipi,islemcinesli,ram,diskboyutu,diskturu,ekranboyutu,9.0,0.0,'n11'))
                con.commit()
                #con.close()      
        degerekle()
    p=p+1


                 
       