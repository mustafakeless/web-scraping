from enum import unique
from flask import Flask,render_template,request,redirect,url_for,session 
import sqlite3
from email import header
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine,Column, Integer, String,and_, or_, not_
from sqlalchemy.orm import declarative_base,sessionmaker
import requests
from bs4 import BeautifulSoup
import re
app = Flask(__name__)
app.secret_key = "secretkey"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////Users/muste/Desktop/PY/laptops.db"
db = SQLAlchemy(app)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
engine = create_engine("sqlite:////Users/muste/Desktop/PY/laptops.db", echo=True,connect_args={'check_same_thread': False})
Base = declarative_base()
header={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"}

with app.app_context():
    db.init_app(app)

@app.route("/",methods=['GET','POST'])     
def index():
    laptops = session.query(Laptop).order_by(Laptop.ModelNo.asc()).order_by(Laptop.Fiyat.asc())   
    return render_template('laptops.html',laptops=laptops)

@app.route("/fiyat_sırala",methods=['GET','POST'])                         
def fiyatsıralama():
    if request.form.get("fscheck")=="1":
        laptops=session.query(Laptop).order_by(Laptop.Fiyat.desc())
    if request.form.get("fscheck")=="2":
        laptops=session.query(Laptop).order_by(Laptop.Fiyat.asc())  
              
    return render_template('laptops.html',laptops=laptops)      
@app.route("/ara",methods=['GET','POST'])     
def arama():
    src0=request.form.get("srcc")
    if src0=="Apple" or src0=="Monster" or src0=="MSI" or src0=="Casper" or src0=="Acer" or src0=="Asus" or src0=="HP" or src0=="Lenovo" or src0=="Dell":
        src=session.query(Laptop).filter(Laptop.Marka.contains(src0)) 
    elif src0=="Hepsiburada" or src0=="Vatan"or src0=="Trendyol"or src0=="Teknosa":
        src=session.query(Laptop).filter(Laptop.Site.contains(src0))     
    else: 
        src=session.query(Laptop).filter(Laptop.ModelNo.contains(src0)) 
    return render_template('laptops.html',laptops=src)                    
@app.route("/site_filtrele",methods=['GET','POST'])                         
def sitefiltre():
    if request.form.get("sfcheck")=="1":
        sırala=session.query(Laptop).filter(Laptop.Site=="Trendyol")
    if request.form.get("sfcheck")=="2":
        sırala=session.query(Laptop).filter(Laptop.Site=="Vatan")
    if request.form.get("sfcheck")=="3":
        sırala=session.query(Laptop).filter(Laptop.Site=="Hepsiburada")
    if request.form.get("sfcheck")=="4":
        sırala=session.query(Laptop).filter(Laptop.Site=="Teknosa")   
    return render_template('laptops.html',laptops=sırala)   
@app.route("/fiyat_filtrele",methods=['GET','POST'])                         
def fiyatfiltre():
    if request.form.get("ffcheck")=="1":
        sırala=session.query(Laptop).filter(and_(Laptop.Fiyat>0, Laptop.Fiyat<5.000))
    if request.form.get("ffcheck")=="2":
        sırala=session.query(Laptop).filter(and_(Laptop.Fiyat>5.000, Laptop.Fiyat<10.000))
    if request.form.get("ffcheck")=="3":
        sırala=session.query(Laptop).filter(and_(Laptop.Fiyat>10.000, Laptop.Fiyat<15.000))
    if request.form.get("ffcheck")=="4":
        sırala=session.query(Laptop).filter(and_(Laptop.Fiyat>15.000, Laptop.Fiyat<20.000))
    if request.form.get("ffcheck")=="5":
        sırala=session.query(Laptop).filter(not_(Laptop.Fiyat<20.000))     
    return render_template('laptops.html',laptops=sırala)    
@app.route("/marka_filtrele",methods=['GET','POST'])                         
def markafiltre():
    if request.form.get("mfcheck")=="1":
        sırala=session.query(Laptop).filter(or_(Laptop.Marka=="Apple", Laptop.Marka=="APPLE"))
    if request.form.get("mfcheck")=="2":
        sırala=session.query(Laptop).filter(or_(Laptop.Marka=="Asus", Laptop.Marka=="ASUS"))
    if request.form.get("mfcheck")=="3":
        sırala=session.query(Laptop).filter(or_(Laptop.Marka=="Acer", Laptop.Marka=="ACER"))
    if request.form.get("mfcheck")=="4":
        sırala=session.query(Laptop).filter(or_(Laptop.Marka=="Casper", Laptop.Marka=="CASPER"))
    if request.form.get("mfcheck")=="5":
        sırala=session.query(Laptop).filter(Laptop.Marka=="HP")
    if request.form.get("mfcheck")=="6":
        sırala=session.query(Laptop).filter(or_(Laptop.Marka=="Lenovo", Laptop.Marka=="LENOVO"))
    if request.form.get("mfcheck")=="7":
        sırala=session.query(Laptop).filter((Laptop.Marka=="MSI"))
    if request.form.get("mfcheck")=="8":
        sırala=session.query(Laptop).filter(or_(Laptop.Marka=="Monster", Laptop.Marka=="MONSTER"))
    if request.form.get("mfcheck")=="9":
        sırala=session.query(Laptop).filter(or_(Laptop.Marka=="Dell", Laptop.Marka=="DELL"))        
    return render_template('laptops.html',laptops=sırala)         
    
class Laptop(Base):
    __tablename__ = "laptop"
    id = Column(Integer , primary_key = True , nullable=False)
    Marka= Column(String(50)) 
    ModelAdı= Column(String(50)) 
    ModelNo= Column(String(50)) 
    İşletimsistemi= Column(String(50)) 
    İşlemcitipi= Column(String(50)) 
    İşlemcinesli= Column(String(50)) 
    RAM= Column(String(50)) 
    DiskBoyutu= Column(String(50)) 
    DiskTürü= Column(String(50)) 
    EkranBoyutu= Column(String(50)) 
    Puan= Column(String(50)) 
    Fiyat= Column(Integer) 
    Site= Column(String(50)) 
    def __repr__(self):
        return "<Laptop(Marka='%s', ModelAdı='%s',ModelNo='%s', İşletimsistemi='%s',İşlemcitipi='%s', İşlemcinesli='%s',RAM='%s', DiskBoyutu='%s',DiskTürü='%s', EkranBoyutu='%s',Puan='%s', Fiyat='%s', Site='%s')>" % (
            self.Marka, 
            self.ModelAdı, 
            self.ModelNo,
            self.İşletimsistemi,
            self.İşlemcitipi,
            self.İşlemcinesli,
            self.RAM,
            self.DiskBoyutu,
            self.DiskTürü,
            self.EkranBoyutu,
            self.Puan,
            self.Fiyat, 
            self.Site, 
         ) 
class TitleNoLink(Base):
    __tablename__ = "titlenolink"
    id2 = Column(Integer , primary_key = True , nullable=False)
    ModelNo= Column(String(50),unique=True) 
    Title= Column(String(150)) 
    Link= Column(String(150)) 
    def __repr__(self):
        return "<TitleNoLink(ModelNo='%s', Title='%s',Link='%s')>" % (
            self.ModelNo, 
            self.Title, 
            self.Link,
         ) 
Base.metadata.create_all(engine) 
Session = sessionmaker(bind=engine)
Session.configure(bind=engine)
session = Session()

@app.route("/<Modell>",methods=['GET','POST'])
def ayrıntı(Modell):
    laptops=session.query(Laptop).filter(Laptop.ModelNo==f"{Modell}") 
    return render_template('ayrıntı.html',laptops=laptops) 

def Trendyol():
    for page in range(1,20): 
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
            try:
                fiyat=s1.find("span",attrs={"class":"prc-dsc"}).text
            except:
                pass    
            title=s1.find("h1",attrs={"class":"pr-new-br"}).text
            marka=s1.find("h1",attrs={"class":"pr-new-br"}).text.split(" ")
            model=""
            print(marka[0])
            fiyats=re.search(r"\d?\d?\d.0?\d0?\d0?\d",fiyat)
            modelno=""
            if marka[0]=="LENOVO":
                try:   
                    model=re.search(r"\d\d[a-zA-Z]\w\w?0\w?\w\w\w\w?\d?\d?",title)
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
                    model=re.search(r"[A-Z]\d\d\d.\d\d\d\d-\w\w\w0\w-?\w?-?\w?\d?\d?",title)
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
                        newlap=Laptop(Marka=marka[0],ModelAdı=modeladi,ModelNo=modelno.upper(),İşletimsistemi=isletimsistemi,İşlemcitipi=islemcitipi,İşlemcinesli=islemcinesli.replace(". Nesil",""),RAM=ram,DiskBoyutu=diskboyutu,DiskTürü=diskturu,EkranBoyutu=ekranboyutu,Puan="",Fiyat=fiyats.group(),Site="Trendyol")
                        session.add(newlap)
                        session.commit()
                        newlap1=Laptop(ModelNo=modelno.upper(),Title=title,Link=l)
                        session.add(newlap1)
                        session.commit()
                        
            except:
                pass


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
                        
                try:
                    newlap=Laptop(Marka=marka,ModelAdı=modeladi,ModelNo=model.upper(),İşletimsistemi=isletimsistemi,İşlemcitipi=islemcitipi,İşlemcinesli=islemcinesli.replace(". Nesil",""),RAM=ram,DiskBoyutu=diskboyutu,DiskTürü=diskturu,EkranBoyutu=ekranboyutu,Puan=puan,Fiyat=fiyatt,Site="Vatan")
                    session.add(newlap)
                    session.commit()
                    newlap1=Laptop(ModelNo=model.upper(),Title=title1,Link=l)
                    session.add(newlap1)
                    session.commit()
                except:
                    pass    





def Hepsiburada():
    for page in range(1,20):
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
                        model=re.search(r"\d\d[a-zA-Z]\w\w?0\w?\w\w\w\w?\d?\d?",title)
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
                        newlap=Laptop(Marka=marka[0],ModelAdı=modeladi,ModelNo=modelno.upper(),İşletimsistemi=isletimsistemi,İşlemcitipi=islemcitipi,İşlemcinesli=islemcinesli.replace(". Nesil","").replace(".Nesil",""),RAM=ram,DiskBoyutu=diskboyutu,DiskTürü=diskturu,EkranBoyutu=ekranboyutu,Puan=puan,Fiyat=fiyats.group(),Site="Hepsiburada")
                        session.add(newlap)
                        session.commit()
                        newlap1=Laptop(ModelNo=modelno.upper(),Title=title,Link=l)
                        session.add(newlap1)
                        session.commit()
            except:
                pass
            modelno=""
            modeladi=""




def Teknosa():
    for page in range(0,20): 
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
            title0=s1.find("h1",attrs={"class":"pdp-title"})
            marka=title0.find("b").text
            print(marka)
            title=s1.find("h1",attrs={"class":"pdp-title"}).text
            title1=s1.find("h1",attrs={"class":"pdp-title"}).text.split(" ")
            modelno=""

            if marka=="Lenovo":
                try:
                    model=re.search(r"\d\d[a-zA-Z]\w\w?0\w?\w\w\w\w?\d?\d?",title)
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
                    model=re.search(r"[A-Z]\d\d\d.\d\d\d\d-\w\w\w0\w-?\w?-?\w?\d?\d?",title)
                    modelno=model.group()
                except:
                    pass 
            
            if marka=="Monster":
                try:
                    model=re.search(r"V\d\d?.\d.?\d?",title)
                    modelno=model.group()
                except:
                    pass
                
            
            
            #rating=s1.find("span",attrs={"class":"avg-rt-txt-tltp"})
            #puan=rating.find("span",attrs={"class":"tltp-avg-cnt"}).text
            #print(puan)
            
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
                    modeladi0=re.search(r"IdeaPad|Legion|ThinkPad|ThinkBook|Yoga|Elitebook|Envy|Omen|Pavilion|ZBook|Spectre|Victus|ProBook|OmniBook|MacBook Air|MacBook Pro|MacBook|Aspire|Enduro|Extensa|Ferrari|Nitro|Predator|Swift|Spin|Switch|TravelMate|ProArt|Zenbook|Vivobook|Chromebook|ROG|TUF|ZEPHYRUS|Experbook|Nirvana|Excalibur|Raider|Stealth|Delta|Katana|Leopard|Alpha|Modern|Abra|Tulpar|Huma|Semruk|Markut",title)
                    modeladi=modeladi0.group()
            except: 
                    modeladi=title1[1]
            try:
                if modelno!="":
                    newlap=Laptop(Marka=marka,ModelAdı=modeladi,ModelNo=modelno,İşletimsistemi=isletimsistemi,İşlemcitipi=islemcitipi.group(),İşlemcinesli=islemcineslis.group(),RAM=ram.group().replace(" RAM",""),DiskBoyutu=diskboyutu.replace(" SSD","").replace(" HDD","").replace(" NVMe",""),DiskTürü=diskturu,EkranBoyutu=ekranboyutu.group(),Puan="",Fiyat=fiyats.group(),Site="Teknosa")
                    session.add(newlap)
                    session.commit()
                    newlap1=Laptop(ModelNo=modelno,Title=title,Link=l)
                    session.add(newlap1)
                    session.commit()
            except:
                pass
            modelno=""
            modeladi=""    



def run():
    Trendyol()
    Vatan()
    Hepsiburada()
    Teknosa()
if __name__=="__main__":
    #run()
    app.run()       







