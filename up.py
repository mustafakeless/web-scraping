from email import header
import requests
from bs4 import BeautifulSoup
import sqlite3

con = sqlite3.connect("laptops.db")
cursor = con.cursor()
p=1
while p<=3:
    url=("https://www.trendyol.com/laptop-x-c103108?pi="+str(p)+"")
    print(url)
    r=requests.get(url)
    #print(r.status_code)
    s=BeautifulSoup(r.content,"lxml")
    laptops=s.find_all("div",attrs={"class":"p-card-wrppr with-campaign-view"})
    linklist=[]
    for laptop in laptops:
        link=laptop.find_all("div",attrs={"class":"p-card-chldrn-cntnr card-border"})
        for f in link:
                l=list(map(lambda lap:"https://www.trendyol.com" + lap.find("a").get("href"),link))
                for u in l:
                    new_string = u.replace("['","").replace("']","")
                    linklist.append(new_string)  
    #print(linklist)
    for l in linklist:
        r1=requests.get(l)
        s1=BeautifulSoup(r1.content,"lxml")
        ayr=s1.find_all("ul",attrs={"class":"detail-attr-container"})
        fiyat=s1.find("span",attrs={"class":"prc-dsc"}).text.replace("TL","")
        marka=s1.find("h1",attrs={"class":"pr-new-br"}).text.split(" ")
        print(marka[0])

        """puan=s1.find("span",attrs={"class":"tltp-avg-cnt"}).text
        print(puan)"""
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

            
        for j1 in list:
            a=0
            if j1=="İşlemci Tipi":
                islemcitipi=list1[a]
            a=a+1                 
        a=0
        for j3 in list:
                if j3=="İşletim Sistemi":
                    isletimsistemi=list1[a]
                a=a+1    
        a=0            
        for j4 in list:
                if j4=="Ram (Sistem Belleği)":
                    ram=list1[a]
                a=a+1                     
        a=0
        for j5 in list:
                if j5=="Ekran Boyutu":
                    ekranboyutu=list1[a]
                a=a+1                
        a=0
        for j6 in list:
                if j6=="İşlemci Nesli":
                    islemcinesli=list1[a]
                a=a+1                 
        a=0
        for j7 in list:
                if j7=="İşlemci Nesli":
                    islemcinesli=list1[a]
                a=a+1                 
        a=0
        for j8 in list:
                if j8=="SSD Kapasitesi":
                    ssdiskboyutu=list1[a]
                    if ssdiskboyutu=="SSD Yok":
                        ssdiskboyutu=""     
                a=a+1                 
        a=0
        for j8 in list:
                if j8=="Hard Disk Kapasitesi":
                    hddiskboyutu=list1[a]
                    if hddiskboyutu=="HDD Yok":
                        hddiskboyutu=""         
                a=a+1                 
        a=0
        for j2 in list1:
                if j2=="SSD Yok":
                    diskturu="HDD"
                    diskboyutu=hddiskboyutu
                    break 
                elif j2=="HDD Yok":
                    diskturu="SSD"
                    diskboyutu=ssdiskboyutu
                    break
                else:
                    diskturu="HDD+SSD"
                    diskboyutu=hddiskboyutu+"+"+ssdiskboyutu        
                a=a+1           
        a=0
        print(islemcitipi,isletimsistemi,diskturu,ram,diskboyutu,ekranboyutu,islemcinesli)
        def degerekle():
                cursor.execute("INSERT INTO laptop VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)", (marka[0],marka[1]+" "+marka[2],marka[3],isletimsistemi,islemcitipi,islemcinesli,ram,diskboyutu,diskturu,ekranboyutu,9.0,fiyat,'Trendyol'))
                con.commit()
                #con.close()      
        degerekle()
    p=p+1
        #print(l)



                 
       