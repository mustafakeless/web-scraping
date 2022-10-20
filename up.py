from email import header
from turtle import title
import requests
from bs4 import BeautifulSoup
import sqlite3
import re
from flask import Flask , render_template
from flask_sqlalchemy import SQLAlchemy
con = sqlite3.connect("laptops.db")
cursor = con.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS laptop (Marka TEXT, ModelAdı TEXT, ModelNo TEXT UNIQUE, İşletimsistemi TEXT,İşlemcitipi TEXT,İşlemcinesli TEXT,RAM INT,DiskBoyutu INT,DiskTürü TEXT,EkranBoyutu FLOAT,Puanı FLOAT,Fiyat INT,Site TEXT)")
header={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"}

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////C:/Users/cagla/Desktop/web-scraping-main/laptops.db"
db = SQLAlchemy(app)

with app.app_context():
    db.init_app(app)


def Teknosa():
    for page in range(0,2): 
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
            model=""
            if marka=="Lenovo":
                try:
                    model=re.search(r"\d\d[A-Z]\w\w?0\w?\w?\w?\w?\w?\d?\d?",title)
                except:
                    pass    
            if marka=="Acer":
                try:
                    model=re.search(r"A[a-z]?\d\d\d-\d\d",title)
                except:
                        pass
            if marka=="Asus":
                try:
                    model=re.search(r"[a-zA-Z][a-zA-Z]?\d\d\d\w\w\w?-[a-zA-Z][a-zA-Z]\w\w\w\w?\w?\w?",title)
                except:
                    pass   
            if marka=="Apple":      
                try:
                    model=re.compile(r"M\w\w\w\dTU\WA",title)
                except:
                    pass     

            if marka=="HP":
                try:
                    model=re.compile(r"\d\w\w\w\wE\w\w?\w?\w?",title)
                except:
                    pass  
            if marka=="Dell":
                try:
                    model=re.search(r"X?P?[A-Z]\d\d\d\d\w\w\w\w\w\w\w\w\w\w",title)
                except:
                    pass 
            if marka=="MSI":
                try:
                    model=re.search(r"\w\d\w?[A-Z]?[A-Z]\w?\w?-\d\d\d\w?TR",title)
                except:
                    pass 
            if marka=="Casper":
                try:
                    model=re.search(r"[A-Z]\d\d\d.\d\d\d\d-\w\w00\w-?G?-?F?",title)
                except:
                    pass 
            
            if marka=="Monster":
                try:
                    model=re.search(r"V\d\d?.\d.?\d?",title)
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
                ssdiskboyutu=re.search(r"\d?\d\d GB ?\w?\w?\w?\w? ?SSD|\d TB ?\w?\w?\w?\w? ?SSD",title)
                print(ssdiskboyutu.group())
                p=p+1
            except:
                pass
            try:
                hddiskboyutu=re.search(r"\d?\d\d GB ?\w?\w?\w?\w? ?HDD|\d TB ?\w?\w?\w?\w? ?HDD",title)
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
            
            def degerekle():
                        cursor.execute("INSERT INTO laptop VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)", (marka,titleparse[1],model.group(),isletimsistemi,islemcitipi.group(),islemcineslis.group(),ram.group().replace(" RAM",""),diskboyutu.replace(" NVMe","").replace(" SSD","").replace(" HDD",""),diskturu,ekranboyutu.group(),9.0,fiyats.group(),'Teknosa'))
                        con.commit()
            try:
                degerekle()
            except:
                pass    

#Teknosa()        

def Trendyol():
    for page in range(1,4): 
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
            fiyats=re.search(r"\d?\d?\d.\d\d\d",fiyat)

            if marka[0]=="LENOVO":
                try:   
                    model=re.search(r"\d\d[a-zA-Z]\w\w?0\w?\w?\w?\w?\w?\d?\d?",title)
                except:
                    pass
            if marka[0]=="MSI":
                try:
                    model=re.search(r"\w\d\w?[A-Z]?[A-Z]\w?\w?-\d\d\d\w?TR",title)  
                except:
                    pass
                
            if marka[0]=="ASUS":
                try:
                    model=re.search(r"[a-zA-Z][a-zA-Z]?\d\d\d\w\w\w?-[a-zA-Z][a-zA-Z]\w\w\w\w?\w?\w?",title)
                except:
                    pass
            if marka[0]=="ACER":
                try:
                    model=re.search(r"A?S?[a-z]?\d\d\d-\d\d",title)
                except:
                    pass
            if marka[0]=="Apple":      
                try:
                    model=re.compile(r"M\w\w\w\dTU\WA",title)
                except:
                    pass    
            if marka[0]=="HP":        
                try:
                    model=re.search(r"\d\w\w\w\wEA?\w?\w?",title)
                except:
                    pass 
            if marka[0]=="Dell":    
                try:
                    model=re.search(r"X?P?[a-zA-Z]\d\d\d\d\w\w\w\w\w\w\w\w\w\w",title)
                except:
                    pass
            if marka[0]=="Casper":     
                try:
                    model=re.search(r"[A-Z]\d\d\d.\d\d\d\d-\w\w\w0\w-?\w?G?g?-?F?f?",title)
                except:
                    pass 
            if marka[0]=="Monster":
                try:
                    model=re.search(r"V\d\d?.\d.?\d?",title)
                except:
                        pass     
        
            for ayr2 in ayr:
                detay=ayr2.find_all("li")
                list=[]
                list1=[]
            for i in detay:
                list.append(i.find("span").text)
                list1.append(i.find("b").text)
                
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
                        islemcinesli=islemcinesli.replace(". Nesil","")
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
                    if j8=="Hard Disk Kapasitesi":
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
                    db=re.search(r"\d ?tb Ssd|\d\d\d ?gb Ssd|\d ?tb Hdd|\d\d\d ?gb Hdd",title)
                    diskboyutu=db.group()
                    if diskboyutu=="1tb Ssd":
                        diskboyutu="1 TB"
                        diskturu="SSD"
                    elif diskboyutu=="2tb Ssd":
                        diskboyutu="2 TB"
                        diskturu="SSD"
                    elif diskboyutu=="6tb Ssd":
                        diskboyutu="6 TB"
                        diskturu="SSD"
                    elif diskboyutu=="256gb Ssd":
                        diskboyutu="256 GB"
                        diskturu="SSD" 
                    elif diskboyutu=="512gb Ssd":
                        diskboyutu="512 GB"
                        diskturu="SSD" 
                    elif diskboyutu=="1tb Hdd":
                        diskboyutu="1 TB"
                        diskturu="HDD"
                    elif diskboyutu=="500gb Ssd":
                        diskboyutu="500 GB"
                        diskturu="SSD"        
            except:
                pass

            print(islemcitipi,isletimsistemi,diskturu,ram,diskboyutu,ekranboyutu,islemcinesli)
            def degerekle():
                    cursor.execute("INSERT INTO laptop VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)", (marka[0],marka[1],model.group().upper(),isletimsistemi,islemcitipi,islemcinesli.replace(". Nesil",""),ram,diskboyutu,diskturu,ekranboyutu,9.0,fiyats.group(),'Trendyol'))
                    con.commit()
            try:
                if model !="":
                        degerekle()
            except:
                pass            
           
#Trendyol()

def n11():
    for page in range(1,4):
        url="https://www.n11.com/bilgisayar/dizustu-bilgisayar?ipg={}".format(page)
        print(url)
        r=requests.get(url)
        s=BeautifulSoup(r.content,"lxml")
        laptops=s.find_all("li",attrs={"class":"column"})
        
        links=[]       
        for laptop in laptops:
            link=laptop.find_all("div",attrs={"class":"pro"})
            links.append(laptop.a.get("href"))
        
        for a in links:
            r1=requests.get(a)
            s1=BeautifulSoup(r1.content,"lxml")
            ayr=s1.find_all("div",attrs={"class":"unf-prop-context"})
            try:
                title0=s1.find("section",attrs={"class":"uni-content"})
                title=title0.find("h2",attrs={"class":"sub-title"}).text
            except:
                pass
            
            try:
                fiyat=s1.find("div",attrs={"class":"price"}).text
            except:
                pass    
            
            fiyats=re.search(r"\d?\d?\d.\d\d\d",fiyat)     
            rating=s1.find("div",attrs={"class":"ratingCont"})
            
            try:
                puan=rating.find("strong").text
            except:
                puan=""
            
            for ayr2 in ayr:
                detay=ayr2.find_all("li",attrs={"class":"unf-prop-list-item"})
                list=[]
                list1=[]
            for i in detay:
                list.append(i.find("p",attrs={"class":"unf-prop-list-title"}).text)
                list1.append(i.find("p",attrs={"class":"unf-prop-list-prop"}).text)
            def tabloolustur():
                cursor.execute("CREATE TABLE IF NOT EXISTS laptop (Marka TEXT, ModelAdı TEXT, ModelNo TEXT, İşletimsistemi TEXT,İşlemcitipi TEXT,İşlemcinesli TEXT,RAM INT,DiskBoyutu INT,DiskTürü TEXT,EkranBoyutu FLOAT,Puanı TEXT,Fiyat INT,Site TEXT)")
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
                        modelno=list1[a]  

                    a=a+1                 
            a=0
            print(marka)
            print(islemcitipi,isletimsistemi,diskturu,ram,diskboyutu,ekranboyutu,islemcinesli)
            
            if marka==" Lenovo":
                try:   
                    model=re.search(r"\d\d[a-zA-Z]\w\w?0\w?\w?\w?\w?\w?\d?\d?",modelno)

                except:
                    pass
            if marka==" Msi":
                try:
                    model=re.search(r"\w\d\w?[A-Z]?[A-Z]\w?\w?-\d\d\d\w?TR",modelno)  

                except:
                    pass
                
            if marka==" Asus":
                try:
                    model=re.search(r"[a-zA-Z][a-zA-Z]?\d\d\d\w\w\w?-[a-zA-Z][a-zA-Z]\w\w\w\w?\w?\w?",modelno)

                except:
                    pass
            if marka==" Acer":
                try:
                    model=re.search(r"A?S?[a-z]?\d\d\d-\d\d",modelno)

                except:
                    pass

            if marka==" Apple":      
                try:
                    model=re.compile(r"M\w\w\w\dTU\WA",modelno)

                except:
                    pass     
            if marka==" HP":        
                try:
                    model=re.search(r"\d\w\w\w\wEA?\w?\w?",modelno)

                except:
                    pass 

            if marka==" Dell":    
                try:
                    model=re.search(r"X?P?[a-zA-Z]\d\d\d\d\w\w\w\w\w\w\w\w\w\w",modelno)

                except:
                    pass
            if marka==" Casper":     
                try:
                    model=re.search(r"[A-Z]\d\d\d.\d\d\d\d-\w\w\w0\w-?\w?G?g?-?F?f?",modelno)

                except:
                    pass 
            if marka==" Monster":
                try:
                    model=re.search(r"V\d\d?.\d.?\d?",modelno)

                except:
                        pass     
            titles=title.split(" ")
            def degerekle():
                    cursor.execute("INSERT INTO laptop VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)", (marka,titles[1],model.group(),isletimsistemi,islemcitipi,islemcinesli,ram,diskboyutu,diskturu,ekranboyutu,puan,fiyats.group(),'n11'))
                    con.commit()    
            try:
                degerekle()
            except:
                pass
          
#n11()       

def Hepsiburada():
    for page in range(1,3):
        r=requests.get("https://www.hepsiburada.com/laptop-notebook-dizustu-bilgisayarlar-c-98?sayfa={}".format(page),headers=header)
        s=BeautifulSoup(r.content,"lxml")
        st1=s.find("div",attrs={"class":"productListContent-tEA_8hfkPU5pDSjuFdKG"})
        st4=st1.find_all("li",attrs={"class":"productListContent-zAP0Y5msy8OHn5z7T_K_"})
        links=[]

        for laptop in st4:
            link=laptop.find_all("div",attrs={"class":"p-card-chldrn-cntnr card-border"})
            links.append("https://www.hepsiburada.com"+laptop.a.get("href"))

        p=0
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
            ayr=s1.find("div",attrs={"id":"productTechSpecContainer"}).findChildren()[7]
            ayr5=ayr.find("tbody")
            detay=ayr5.find_all("tr")
            list=[]
            list1=[]

            for i in detay:
                list.append(i.find("th").text.replace("\n",""))
                list1.append(i.find("td").text.replace("\n",""))
            print(list)
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
            for j7 in list:
                    if j7=="İşlemci Nesli":
                        islemcinesli=list1[a]
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
            print(fiyats.group())

            if marka[0]=="Lenovo":
                    try:   
                        model=re.search(r"\d\d[a-zA-Z]\w\w?0\w?\w?\w?\w?\w?\d?\d?",title)
                        
                    except:
                        pass
            if marka[0]=="MSI":
                try:
                    model=re.search(r"\w\d\w?[A-Z]?[A-Z]\w?\w?-\d\d\d\w?TR",title)  
                except:
                    pass
                    
            if marka[0]=="Asus":
                try:
                    model=re.search(r"[a-zA-Z][a-zA-Z]?\d\d\d\w\w\w?-[a-zA-Z][a-zA-Z]\w\w\w\w?\w?\w?",title)
                except:
                    pass
            if marka[0]=="Acer":
                try:
                    model=re.search(r"A?S?[a-z]?\d\d\d-\d\d",title)
                except:
                    pass
            if marka[0]=="Apple":      
                try:
                    model=re.search(r"M\w\w\w\dTU\WA",title)
                except:
                    pass     
            if marka[0]=="HP":        
                try:
                    model=re.search(r"\d\w\w\w\wEA?\w?\w?",title)
                except:
                    pass 
            if marka[0]=="Dell":    
                try:
                    model=re.search(r"X?P?[a-zA-Z]\d\d\d\d\w\w\w\w\w\w\w\w\w\w",title)
                except:
                    pass
            if marka[0]=="Casper":     
                try:
                    model=re.search(r"[A-Z]\d\d\d.\d\d\d\d-\w\w\w0\w-?\w?G?g?-?F?f?",title)
                except:
                    pass 
            if marka[0]=="Monster":
                try:
                    model=re.search(r"V\d\d?.\d.?\d?",title)
                except:
                        pass     
            isletimsistemi=re.search(r"Windows|macOS|Linux|Free Dos|Ubuntu",isletimsistemi)
            isletimsistemi=isletimsistemi.group()        
            print(islemcitipi,isletimsistemi,diskturu,ram,diskboyutu,ekranboyutu,islemcinesli)
            def degerekle():
                        cursor.execute("INSERT INTO laptop VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)", (marka[0],marka[1],model.group().upper(),isletimsistemi,islemcitipi,islemcinesli.replace(".Nesil","").replace(". Nesil",""),ram,diskboyutu,diskturu,ekranboyutu,puan,fiyats.group(),'Hepsiburada'))
                        con.commit()
            try:
                degerekle()
            except:
                pass  
#Hepsiburada()

@app.route("/")
def index():
    laptopss = laptops.query.all()
    return render_template("index.html",laptopss=laptopss)

def run():
    Teknosa()
    Trendyol()
    n11()
    Hepsiburada()

if __name__ == "__main__":
    run()