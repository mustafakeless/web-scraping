

from email import header
from turtle import title
from unittest import result
import requests
from bs4 import BeautifulSoup
import sqlite3
import re
from flask import Flask , render_template
from flask_sqlalchemy import SQLAlchemy

con = sqlite3.connect("laptops.db")
cursor = con.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS laptop (laptop_id INTEGER PRIMARY KEY AUTOINCREMENT,Marka TEXT, ModelAdi TEXT, ModelNo TEXT UNIQUE, IsletimSistemi TEXT,IslemciTipi TEXT,IslemciNesli TEXT,RAM INT,DiskBoyutu INT,DiskTuru TEXT,EkranBoyutu FLOAT,Puan FLOAT,Fiyat INT,Site TEXT)")
header={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"}

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////C:/Users/cagla/Desktop/web-scraping-main/laptops.db"
db = SQLAlchemy(app)

with app.app_context():
    db.init_app(app)



def Teknosa():
    for page in range(0,10): 
        url="https://www.teknosa.com/laptop-notebook-c-116004?s=%3Arelevance&page={}".format(page) 
        print(url)
        r=requests.get(url)
        s=BeautifulSoup(r.content,"lxml")
        laptops=s.find_all("div",attrs={"id":"product-item"})
        links=[]       
        for laptop in laptops:
            links.append("https://www.teknosa.com"+laptop.a.get("href"))
        p=0
        for l in links:
            r1=requests.get(l)
            s1=BeautifulSoup(r1.content,"lxml")
            ayr=s1.find_all("div",attrs={"class":"ptf-body"})
            try:
                title=s1.find("h1",attrs={"class":"pdp-title"}).text
            except:
                pass
            marka0=s1.find("h1",attrs={"class":"pdp-title"})
            marka=marka0.find("b").text
            titleparse=s1.find("h1",attrs={"class":"pdp-title"}).text.split(" ")
            print(marka)
            modelno=""
            if marka=="Lenovo":
                try:
                    model=re.search(r"\d\d[a-zA-Z]\w\w?0\w?\w?\w?\w?\w?\d?\d?",title)
                    modelno=model.group()
                except:
                    pass    
            if marka=="Acer":
                try:
                    model=re.search(r"\w\w.\w\w\w\w\w.\d\d\d\w?\w?",title)
                    modelno=model.group()
                except:
                        pass
            if marka=="Asus":
                try:
                    model=re.search(r"[a-zA-Z][a-zA-Z]?\d\d\d\w\w\w?-[a-zA-Z][a-zA-Z]\w\w\w\w?\w?\w?",title)
                    modelno=model.group()
                except:
                    pass   
            if marka=="Apple":      
                try:
                    model=re.search(r"M\w\w\w\dTU\WA",title)
                    modelno=model.group()
                    isletimsistemi="macOS"
                except:
                    pass     

            if marka=="HP":
                try:
                    model=re.search(r"\d\w\w\w\wE\w\w?\w?\w?",title)
                    modelno=model.group()
                except:
                    pass  
            if marka=="Dell":
                try:
                    model=re.search(r"X?P?\w?\d\d\w?\w?\w\w\w\w\w?\w?\w?\w?\w?\w?",title)
                    modelno=model.group()
                except:
                    pass 
            if marka=="MSI":
                try:
                    model=re.search(r"\w\d\w?[A-Z]?[A-Z]\w?\w?-\d\d\d\w?TR",title)
                    modelno=model.group()
                except:
                    pass 
            if marka=="Casper":
                try:
                    model=re.search(r"[A-Z]\d\d\d.\d\d\d\d-\w\w\w0\w-?\w?-?w?\d?\d?",title)
                    modelno=model.group()
                except:
                    pass 
            
            if marka=="Monster":
                try:
                    model=re.search(r"V\d\d?.\d.?\d?",title)
                    modelno=model.group()
                except:
                    pass
                
            
            
            """rating=s1.find("span",attrs={"class":"avg-rt-txt-tltp"})
            puan=rating.find("span",attrs={"class":"tltp-avg-cnt"}).text
            print(puan)"""
            
            try:
                fiyat=s1.find("div",attrs={"class":"prd-prc2"}).text
                fiyats=re.search(r"\d?\d?\d.\d\d\d",fiyat)
                print(fiyats.group())
            except:
                pass
            try:
                islemcitipi=re.search(r"Intel Core i?I?\d|Intel Celeron|Ryzen \d|AMD Ryzen \d",title)
                print(islemcitipi.group())
            except:
                pass
            
            try:
                isletimsistemi=re.search(r"FreeDOS|W11|W10|Windows \d\d?|Ubuntu|Linux",title)
                if isletimsistemi.group()=="FreeDOS":
                    isletimsistemi="Free Dos"
                elif isletimsistemi.group()=="W11" or "W10" or "Windows 11" or "Windows 10":
                    isletimsistemi="Windows"
                else:
                    isletimsistemi=isletimsistemi.group()     
                
            except:
                pass
            print(isletimsistemi) 
            try:
                ram=re.search(r"\d?\d GB RAM",title)
                print(ram.group())
            except:
                pass
            diskboyutu=""
            
            try:
                ssdiskboyutu=re.search(r"\d?\d\d ?GB ?\w?\w?\w?\w? ?SSD|\d ?TB ?\w?\w?\w?\w? ?SSD",title)
                print(ssdiskboyutu.group())
                p=p+1
            except:
                pass
            try:
                hddiskboyutu=re.search(r"\d?\d\d ?GB ?\w?\w?\w?\w? ?HDD|\d ?TB ?\w?\w?\w?\w? ?HDD",title)
                print(hddiskboyutu.group())
                p=p+2
            except:
                pass
            diskturu=""
            if p==1:
                diskturu="SSD"
                diskboyutu=ssdiskboyutu.group()
            if p==2:
                diskturu="HDD"
                diskboyutu=hddiskboyutu.group()
            if p==3:
                diskturu="HDD+SSD"
                diskboyutu=hddiskboyutu.group()+" "+ssdiskboyutu.group()
            
            print(diskboyutu)    
            print(diskturu)
            p=0

            try:
                ekranboyutu=re.search(r'\d\d.?\d?"',title)
                print(ekranboyutu.group())
            except:
                pass

            try:
                islemcinesli=re.search(r'Intel Core i?I?\d ?-?\d\d|Intel Celeron|Ryzen \d \d\d\d\dU|AMD Ryzen \d \d\d\d\dU"',title)
                print(islemcinesli.group())
                islemcineslis=re.search(r'\d\d\d\dU|\d\d',islemcinesli.group())
                print(islemcineslis.group())
            except:
                pass        
            
            try:
                if modelno!="":
                        cursor.execute("INSERT INTO laptop VALUES (Marka,ModelAdi,ModelNo,IsletimSistemi,IslemciTipi,IslemciNesli,RAM,DiskBoyutu,DiskTuru,EkranBoyutu,Puan,Fiyat,Site) (?,?,?,?,?,?,?,?,?,?,?,?,?)", (marka,titleparse[1],modelno,isletimsistemi,islemcitipi.group(),islemcineslis.group(),ram.group().replace(" RAM",""),diskboyutu.replace(" NVMe","").replace(" SSD","").replace(" HDD",""),diskturu,ekranboyutu.group(),"",fiyats.group(),'Teknosa'))
                        con.commit()
            except:
                pass
            modelno=""
            modeladi=""    


#Teknosa()        

def Trendyol():
    for page in range(1,10): 
        url="https://www.trendyol.com/laptop-x-c103108?pi={}".format(page)
        print(url)
        r=requests.get(url)
        s=BeautifulSoup(r.content,"lxml")
        laptops=s.find_all("div",attrs={"class":"p-card-wrppr with-campaign-view"})
        links=[]
        for laptop in laptops:
            link=laptop.find_all("div",attrs={"class":"p-card-chldrn-cntnr card-border"})
            links.append("https://www.trendyol.com"+laptop.a.get("href"))
        for l in links:
            r1=requests.get(l)
            s1=BeautifulSoup(r1.content,"lxml")
            ayr=s1.find_all("ul",attrs={"class":"detail-attr-container"})
            fiyat=s1.find("span",attrs={"class":"prc-dsc"}).text
            title=s1.find("h1",attrs={"class":"pr-new-br"}).text
            marka=s1.find("h1",attrs={"class":"pr-new-br"}).text.split(" ")
            model=""
            print(marka[0])
            fiyats=re.search(r"\d?\d?\d.0?\d0?\d0?\d",fiyat)
            modelno=""
            if marka[0]=="LENOVO":
                try:   
                    model=re.search(r"\d\d[a-zA-Z]\w\w?0\w?\w?\w?\w?\w?\d?\d?",title)
                    modelno=model.group()
                except:
                    pass
            if marka[0]=="MSI":
                try:
                    model=re.search(r"\w\d\w?[A-Z]?[A-Z]\w?\w?-\d\d\d\w?TR",title)  
                    modelno=model.group()

                except:
                    pass
                
            if marka[0]=="ASUS":
                try:
                    model=re.search(r"[a-zA-Z][a-zA-Z]?\d\d\d\w\w\w?-[a-zA-Z][a-zA-Z]\w\w\w\w?\w?\w?",title)
                    modelno=model.group()
                except:
                    pass
            if marka[0]=="ACER":
                try:
                    model=re.search(r"\w\w.\w\w\w\w\w.\d\d\d\w?\w?",title)
                    modelno=model.group()
                except:
                    pass
            if marka[0]=="Apple":      
                try:
                    model=re.search(r"M\w\w\w\dTU\WA",title)
                    modelno=model.group()
                except:
                    pass    
            if marka[0]=="HP":        
                try:
                    model=re.search(r"\d\w\w\w\wEA?\w?\w?",title)
                    modelno=model.group()
                except:
                    pass 
            if marka[0]=="Dell":    
                try:
                    model=re.search(r"X?P?\w?\d\d\w?\w?\w\w\w\w\w?\w?\w?\w?\w?\w?",title)
                    modelno=model.group()
                except:
                    pass
            if marka[0]=="Casper":     
                try:
                    model=re.search(r"[A-Z]\d\d\d.\d\d\d\d-\w\w\w0\w-?\w?-?w?\d?\d?",title)
                    modelno=model.group()
                except:
                    pass 
            if marka[0]=="Monster":
                try:
                    model=re.search(r"V\d\d?.\d.?\d?",title)
                    modelno=model.group()
                except:
                        pass     
        
            for ayr2 in ayr:
                detay=ayr2.find_all("li")
                list=[]
                list1=[]
            for i in detay:
                list.append(i.find("span").text)
                list1.append(i.find("b").text)
            a=0     
            for j1 in list:
            
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
            for j7 in list:
                    if j7=="İşlemci Nesli":
                        islemcinesli=list1[a]
                    a=a+1                 
            a=0
            ssdiskboyutu="" 
            hddiskboyutu="" 
            diskboyutu=""
            diskturu=""
            
            t=0
            for j8 in list:
                    if j8=="SSD Kapasitesi":
                        ssdiskboyutu=list1[a]
                        if ssdiskboyutu=="SSD Yok":
                            ssdiskboyutu="" 
                            diskturu="HDD"
                            diskboyutu=hddiskboyutu
                        elif ssdiskboyutu=="Yok":
                            ssdiskboyutu="" 
                            diskturu="HDD" 
                            diskboyutu=hddiskboyutu 
                        else:
                            t=t+1 
                    a=a+1                 
            a=0
            
            for j9 in list:
                    if j9=="Hard Disk Kapasitesi":
                        hddiskboyutu=list1[a]
                        if hddiskboyutu=="HDD Yok":
                            hddiskboyutu=""
                            diskturu="SSD"
                            diskboyutu=ssdiskboyutu
                        elif hddiskboyutu=="Yok":
                            hddiskboyutu=""
                            diskturu="SSD"
                            diskboyutu=ssdiskboyutu 
                        else:
                            t=t+1         
                    a=a+1                 
            a=0
            
            if t==2:
                diskturu="HDD+SSD"
                if hddiskboyutu=="":
                    diskboyutu=ssdiskboyutu
                else:
                    diskboyutu=hddiskboyutu+" "+ssdiskboyutu  
            try:
                if diskboyutu=="":
                    db=re.search(r"\d ?tb Ssd|\d\d\d ?gb Ssd",title)
                    db1=re.search(r"\d\d\d|\d",db.group())
                    diskboyutu=db1.group()
                    if db.group() != "None":
                        diskturu="SSD"
                    db2=re.search(r"\d ?tb Hdd|\d\d\d ?gb Hdd",title)
                    db3=re.search(r"\d\d\d|\d",db2.group())
                    diskboyutu=db3.group()
                    if db2.group() != "None":
                        diskturu="HDD"               
            except:
                pass 
            try:    
                modeladi0=re.search(r"IdeaPad|Legion|ThinkPad|ThinkBook|Yoga|Elitebook|Envy|Omen|Pavilion|ZBook|Spectre|Victus|ProBook|OmniBook|MacBook Air|MacBook Pro|MacBook|Aspire|Enduro|Extensa|Ferrari|Nitro|Predator|Swift|Spin|Switch|TravelMate|ProArt|Zenbook|Vivobook|Chromebook|ROG|TUF|ZEPHYRUS|Experbook|Nirvana|Excalibur|Raider|Stealth|Delta|Katana|Leopard|Alpha|Modern|Abra|Tulpar|Huma|Semruk|Markut",title)
                modeladi=modeladi0.group()
            except: 
                modeladi=marka[1]   
                
            print(islemcitipi,isletimsistemi,diskturu,ram,diskboyutu,ekranboyutu,islemcinesli)
            try:
                if modelno!="":
                        cursor.execute("INSERT INTO laptop (Marka,ModelAdi,ModelNo,IsletimSistemi,IslemciTipi,IslemciNesli,RAM,DiskBoyutu,DiskTuru,EkranBoyutu,Puan,Fiyat,Site) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)", (marka[0],modeladi,modelno.upper(),isletimsistemi,islemcitipi,islemcinesli.replace(". Nesil",""),ram,diskboyutu,diskturu,ekranboyutu," ",fiyats.group(),'Trendyol'))
                        con.commit()
            except:
                pass
            modelno=""
                

           
# Trendyol()

def Vatan():
    for page in range(1,10): 
        url="https://www.vatanbilgisayar.com/laptop/?page={}".format(page)
        print(url)
        r=requests.get(url).text
        s=BeautifulSoup(r,"lxml")
        laptops=s.find_all("div",attrs={"class":"product-list product-list--list-page"})
        links=[]       
        for laptop in laptops:
            link=laptop.find_all("div",attrs={"class":"wrapper-star"})
            links.append("https://www.vatanbilgisayar.com"+laptop.a.get("href"))
        print(links)
        for l in links:
                r1=requests.get(l)
                s1=BeautifulSoup(r1.content,"lxml")
                ayr=s1.find_all("tr",attrs={"data-count":"0"})
                fiyat=s1.find("div",attrs={"class":"product-list__cost product-list__description"})
                fiyatt=fiyat.find("span",attrs={"class":"product-list__price"}).text
                title=s1.find("h1",attrs={"class":"product-list__product-name"}).text.split(" ")
                title1=s1.find("h1",attrs={"class":"product-list__product-name"}).text

                marka=s1.find("ul",attrs={"class":"breadcrumb"}).findChildren()[7].text
                print(marka)
                model2=s1.find("ul",attrs={"class":"breadcrumb"}).findChildren()[9].text
                rating0=s1.find("div",attrs={"class":"rank-star"})
                puan=""
                ra=str(rating0)

                try:
                    rating=re.search(r"\d?\d?\d",ra)
                    puan=rating.group()
                    puan=int(puan)/20
                except:
                    puan=""
                                
                    
                print(puan)
                print(fiyatt)
                list=[]
                list1=[]    
                for i in ayr:
                    list.append(i.find("td").text)
                    list1.append(i.find("p").text)
                a=0
                for j1 in list:
                    
                    if j1=="İşlemci Teknolojisi":
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
                        if j9=="Üretici Part Numarası":
                            model=list1[a]
                        a=a+1                 
                a=0
                if marka=="ASUS":
                    model=model2
                print(model,islemcitipi,isletimsistemi,diskturu,ram,diskboyutu,ekranboyutu,islemcinesli)
                try:
                    islemcineslis=re.search(r"\d?\d|\d|Belirtilmemiş",islemcinesli)
                    islemcinesli=islemcineslis.group()
                except:
                    pass 
                try:
                    isletimsistemis=re.search(r"Windows|FreeDOS|macOS|Win",isletimsistemi)
                    isletimsistemi=isletimsistemis.group()
                    if isletimsistemis.group()=="Win":
                        isletimsistemi="Windows"
                except:
                    pass     
                try:    
                    modeladi0=re.search(r"IdeaPad|Legion|ThinkPad|ThinkBook|Yoga|Elitebook|Envy|Omen|Pavilion|ZBook|Spectre|Victus|ProBook|OmniBook|MacBook Air|MacBook Pro|MacBook|Aspire|Enduro|Extensa|Ferrari|Nitro|Predator|Swift|Spin|Switch|TravelMate|ProArt|Zenbook|Vivobook|Chromebook|ROG|TUF|ZEPHYRUS|Experbook|Nirvana|Excalibur|Raider|Stealth|Delta|Katana|Leopard|Alpha|Modern|Abra|Tulpar|Huma|Semruk|Markut",title1)
                    modeladi=modeladi0.group()
                except: 
                    modeladi=title[1]
                    if marka=="APPLE":
                        modeladi=title[0]+title[1]
                        
                if marka != "HUAWEI":
                    #insert into çalışmadı ve sqlite3.IntegrityError: UNIQUE constraint failed: laptop.ModelNo hatasını verdi
                    #yerine INSERT OR REPLACE INTO ya da INSERT OR IGNORE INTO yazarak sorun çözüldü
                    cursor.execute("INSERT OR REPLACE INTO laptop (Marka,ModelAdi,ModelNo,IsletimSistemi,IslemciTipi,IslemciNesli,RAM,DiskBoyutu,DiskTuru,EkranBoyutu,Puan,Fiyat,Site) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)", (marka,modeladi,model.upper(),isletimsistemi,islemcitipi,islemcinesli,ram,diskboyutu,diskturu,ekranboyutu,puan,fiyatt,'Vatan'))
                    con.commit() 
                 
          
# Vatan()       

def Hepsiburada():
    for page in range(1,10):
        r=requests.get("https://www.hepsiburada.com/laptop-notebook-dizustu-bilgisayarlar-c-98?sayfa={}".format(page),headers=header)
        s=BeautifulSoup(r.content,"lxml")
        st1=s.find("div",attrs={"class":"productListContent-tEA_8hfkPU5pDSjuFdKG"})
        st4=st1.find_all("li",attrs={"class":"productListContent-zAP0Y5msy8OHn5z7T_K_"})
        links=[]

        for laptop in st4:
            link=laptop.find_all("div",attrs={"class":"p-card-chldrn-cntnr card-border"})
            links.append("https://www.hepsiburada.com"+laptop.a.get("href"))

        for l in links:
            try:
                r1=requests.get(l,headers=header)
                s1=BeautifulSoup(r1.content,"lxml")
            except:
                pass

            print(l)
        
        
            title0=s1.find("header",attrs={"class":"title-wrapper"})
            title=title0.find("span",attrs={"itemprop":"name"}).text
            marka=title0.find("span",attrs={"itemprop":"name"}).text.split(" ")
            
            print(title)  
            
            try:
                puan=s1.find("span",attrs={"class":"rating-star"}).text.replace(",",".")
            except:
                pass

            print(puan)
            try:
                ayr=s1.find("div",attrs={"id":"productTechSpecContainer"}).findChildren()[7]
            except:
                break   
            ayr5=ayr.find("tbody")
            detay=ayr5.find_all("tr")
            list=[]
            list1=[]

            for i in detay:
                list.append(i.find("th").text.replace("\n",""))
                list1.append(i.find("td").text.replace("\n",""))
            a=0
            for j1 in list:
                    
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
                        islemcinesli=islemcinesli.replace(". Nesil","")
                    a=a+1                 
            a=0
            ssdiskboyutu=""
            hddiskboyutu=""
            diskturu=""
            diskboyutu=""
            t=0 
            for j8 in list:
                        if j8=="SSD Kapasitesi":
                            ssdiskboyutu=list1[a]
                            if ssdiskboyutu=="Yok":
                                ssdiskboyutu="" 
                                diskturu="HDD"
                                diskboyutu=hddiskboyutu
                            else:
                                t=t+1 
                        a=a+1                 
            a=0
                
            for j9 in list:
                    if j9=="Harddisk Kapasitesi":
                        hddiskboyutu=list1[a]
                        if hddiskboyutu=="Yok":
                            hddiskboyutu=""
                            diskturu="SSD"
                            diskboyutu=ssdiskboyutu
                        

                        else:
                            t=t+1         
                    a=a+1                 
            a=0
            
            if ssdiskboyutu !="" and hddiskboyutu !="":
                diskturu="HDD+SSD"
                if hddiskboyutu=="":
                    diskboyutu=ssdiskboyutu
                else:
                    diskboyutu=hddiskboyutu+" "+ssdiskboyutu   
            
            fiyat=s1.find("span",attrs={"id":"offering-price"}).text
            fiyats=re.search(r"\d?\d?\d.\d\d\d",fiyat)
            if marka[0]=="Lenovo":
                    try:   
                        model=re.search(r"\d\d[a-zA-Z]\w\w?0\w?\w?\w?\w?\w?\d?\d?",title)
                        modelno=model.group()
                    except:
                        modelno=""
            if marka[0]=="MSI":
                try:
                    model=re.search(r"\w\d\w?[A-Z]?[A-Z]\w?\w?-\d\d\d\w?TR",title) 
                    modelno=model.group() 
                except:
                    modelno=""
                    
            if marka[0]=="Asus":
                try:
                    model=re.search(r"[a-zA-Z][a-zA-Z]?\d\d\d\w\w\w?-[a-zA-Z][a-zA-Z]\w\w\w\w?\w?\w?",title)
                    modelno=model.group()
                except:
                    modelno=""
            if marka[0]=="Acer":
                try:
                    model=re.search(r"\w\w.\w\w\w\w\w.\d\d\d\w?\w?",title)
                    modelno=model.group()
                except:
                    modelno=""
            if marka[0]=="Apple":      
                try:
                    model=re.search(r"M\w\w\w\dTU\WA",title)
                    modelno=model.group()
                except:
                    modelno=""     
            if marka[0]=="HP":        
                try:
                    model=re.search(r"\d\w\w\w\wEA?\w?\w?",title)
                    modelno=model.group()
                except:
                    modelno="" 
            if marka[0]=="Dell":    
                try:
                    model=re.search(r"X?P?[a-zA-Z]\d\d\d\d\w\w\w\w\w\w\w\w\w\w",title)
                    modelno=model.group()
                except:
                    modelno=""
            if marka[0]=="Casper":     
                try:
                    model=re.search(r"[A-Z]\d\d\d.\d\d\d\d-\w\w\w0\w-?\w?G?g?-?F?f?",title)
                    modelno=model.group()
                except:
                    modelno="" 
            if marka[0]=="Monster":
                try:
                    model=re.search(r"V\d\d?.\d.?\d?",title)
                    modelno=model.group()
                except:
                    modelno="" 
            try:    
                modeladi0=re.search(r"IdeaPad|Legion|ThinkPad|ThinkBook|Yoga|Elitebook|Envy|Omen|Pavilion|ZBook|Spectre|Victus|ProBook|OmniBook|MacBook Air|MacBook Pro|MacBook|Aspire|Enduro|Extensa|Ferrari|Nitro|Predator|Swift|Spin|Switch|TravelMate|ProArt|Zenbook|Vivobook|Chromebook|ROG|TUF|ZEPHYRUS|Experbook|Nirvana|Excalibur|Raider|Stealth|Delta|Katana|Leopard|Alpha|Modern|Abra|Tulpar|Huma|Semruk|Markut",title)
                modeladi=modeladi0.group()
            except: 
                modeladi=marka[1]
            try:             
                isletimsistemi=re.search(r"Windows|macOS|Linux|Free Dos|Ubuntu",isletimsistemi)
                isletimsistemi=isletimsistemi.group()    
            except:
                pass    
            print(islemcitipi,isletimsistemi,diskturu,ram,diskboyutu,ekranboyutu,islemcinesli)
            try:
                if modelno!="":
                        cursor.execute("INSERT INTO laptop (Marka,ModelAdi,ModelNo,IsletimSistemi,IslemciTipi,IslemciNesli,RAM,DiskBoyutu,DiskTuru,EkranBoyutu,Puan,Fiyat,Site) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)", (marka[0],modeladi,modelno.upper(),isletimsistemi,islemcitipi,islemcinesli.replace(".Nesil","").replace(". Nesil",""),ram,diskboyutu,diskturu,ekranboyutu,puan,fiyats.group(),'Hepsiburada'))
                        con.commit()
            except:
                pass
            modelno=""
            modeladi=""


# Hepsiburada()

@app.route("/")
def index():
      data=title()
    #   data1=getmarka()
      return render_template("index.html", resultList=data)


def title():
     con=sqlite3.connect('laptops.db')
     cursor = con.cursor()
     cursor.execute("SELECT laptop_id  FROM laptop ORDER BY laptop_id ASC;")
     laptopid=cursor.fetchall()
     
     print(laptopid)
     new_strings=[]
     # virgülü almaması için i[0] yazılıgit
     for i in laptopid:
        new_strings.append(i[0])

     resultList = []
     for i in new_strings:
        cursor.execute("SELECT Marka, ModelAdi , ModelNo, IsletimSistemi, IslemciTipi, IslemciNesli, RAM, DiskBoyutu, DiskTuru, EkranBoyutu  FROM laptop WHERE laptop_id="+ str(i) +";")
        result=cursor.fetchall()
        resultList.append(result)

     print(resultList) 
     return resultList

def fiyat():
     con=sqlite3.connect('laptops.db')
     cursor = con.cursor()
     laptopid=[]
     cursor.execute("SELECT laptop_id  FROM laptop ORDER BY laptop_id ASC;")
     laptopid=cursor.fetchall()
     cursor.execute("SELECT Marka, ModelAdi , ModelNo, IsletimSistemi, IslemciTipi, IslemciNesli, RAM, DiskBoyutu, DiskTuru, EkranBoyutu  FROM laptop WHERE laptop_id=13 ;")
     result=cursor.fetchall()
     print(laptopid[1])
     return result



def run():
    Teknosa()
    Trendyol()
    Vatan()
    Hepsiburada()

if __name__ == "__main__":
    #run()
    app.run()