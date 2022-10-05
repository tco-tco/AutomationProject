#ÇED-ÖNCE GELEN KUTUSUNDAKİ YAZILARIN KONUSUNU VE GELDİĞİ YERİ LİSTE YAPAR VE EĞER ARŞİV KLASÖRÜNDEKİ YAZI BU LİSTEDEYSE DÖNGÜYE GİRER

from belgenetUser import username, password
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select


from CED_TCO import ExcelDosya
import konuCharHarf


import os
import shutil
import time
import glob
import time

import warnings
warnings.filterwarnings("ignore")



class Belgenet:
    
    def __init__(self, username, password):
        self.browser=webdriver.Chrome("C:/Users/tugbacanan.oguz/Desktop/python_temelleri_iş/PROJECT_1/chromedriver.exe")
        self.username=username
        self.password=password
        
             
    
    def signIn(self):
        self.browser.get("https://e-belge.tarim.gov.tr/edys-web/sistemeGiris.xhtml")
        self.browser.implicitly_wait(60)
        
        self.browser.find_element(By.XPATH,"//*[@id='parolaSertifikaAccordion:uForm:txtUKullaniciAdi']").send_keys(self.username)
        self.browser.find_element(By.XPATH,"//*[@id='loginUSifre']").send_keys(self.password)

        self.browser.implicitly_wait(60)

        self.browser.find_element(By.XPATH,"/html/body/div[5]/div[2]/div/div[2]/div/div[2]/div[2]/div/form/button/span").click()

        self.browser.implicitly_wait(60)





    def letter(self):
        ####GELEN KUTUSUNDAKİ İLK 10 YAZIYI GELDİĞİ YER VE KONUSUNU ALIP DICT'YE ATAR
       
        self.browser.switch_to.window(self.browser.window_handles[0])
        self.browser.implicitly_wait(60)
        WebDriverWait(self.browser, 60).until(EC.element_to_be_clickable((By.XPATH,"//*[@id='esm_246802192_emi_286053589']"))).click()      # gelen kutusunu tıklar

        # identify dropdown with Select class
        time.sleep(4)
        self.browser.implicitly_wait(60)
        sel100 = Select(self.browser.find_element(By.XPATH,"//div[@class='ui-paginator ui-paginator-top ui-widget-header']//select[@name='mainInboxForm:inboxDataTable_rppDD']"))   #sayfada görünen yazı sayısını 100'e çıkarır
        time.sleep(2)
        #select by select_by_visible_text() method
        sel100.select_by_visible_text("100")
        self.browser.implicitly_wait(60)
        time.sleep(5)
        print("OK-100")
        
        

        gelenReadevenList=self.browser.find_elements(By.CSS_SELECTOR,f".ui-widget-content.ui-datatable-even.ui-datatable-selectable.ui-inbox-read[data-ri]")    #aşağıdaki satırlarla beraber tüm gelen yazı listesini alır (sayı olarak)
        self.browser.implicitly_wait(60)

        gelenReadoddList=self.browser.find_elements(By.CSS_SELECTOR,f".ui-widget-content.ui-datatable-odd.ui-datatable-selectable.ui-inbox-read[data-ri]")
        self.browser.implicitly_wait(60)
        
        gelenUnreadevenList=self.browser.find_elements(By.CSS_SELECTOR,f".ui-widget-content.ui-datatable-even.ui-datatable-selectable.ui-inbox-unread[data-ri]")
        self.browser.implicitly_wait(60)
        
        gelenUnreadoddList=self.browser.find_elements(By.CSS_SELECTOR,f".ui-widget-content.ui-datatable-odd.ui-datatable-selectable.ui-inbox-unread[data-ri]")
        self.browser.implicitly_wait(60)
        

        gelenList=gelenUnreadevenList+gelenUnreadoddList+gelenReadevenList+gelenReadoddList #tüm gelen yazı listesini tek liste yapar(okunmuş-okunmamış-tek-çift)
                
        print(len(gelenList))
        time.sleep(2)

        gelenYaziCokluList=[]


        for i in gelenList:
            sira=int(i.get_attribute("data-ri"))
            self.browser.implicitly_wait(60)
            h3Konu=(i.find_element_by_tag_name("h3")).text
            self.browser.implicitly_wait(60)
            print(h3Konu)


            h3KonuJoin=konuCharHarf.konuJoin(h3Konu)    #return gelenKonuJoin


            gelYer=(i.find_element(By.XPATH,"td[2]/table[1]/tbody[1]/tr[2]")).text                                                                            
            self.browser.implicitly_wait(60)
            if gelYer=="Geldiği Yer: Su Yönetimi Genel Müdürlüğü / İzleme ve Su Bilgi Sistemi Daire Başkanlığı":
                geldigiYerD="izleme"
                
            elif gelYer=="Geldiği Yer: Su Yönetimi Genel Müdürlüğü / Havza Yönetimi Daire Başkanlığı":
                geldigiYerD="havza"
                
            elif gelYer=="Geldiği Yer: Su Yönetimi Genel Müdürlüğü / Taşkın ve Kuraklık Yönetimi Daire Başkanlığı":
                
                geldigiYerD="taşkın"
                
            elif gelYer=="Geldiği Yer: Su Yönetimi Genel Müdürlüğü / Su Kalitesi Daire Başkanlığı":
                geldigiYerD="kalite"
                
            else:
                geldigiYerD="diğer"              
        



            if geldigiYerD=="diğer":                                 
                
                 
                print("value diğermiş")       

            else:
                gelenYaziCokluList.append((int(sira), h3KonuJoin, geldigiYerD))
                print("OKK")
                print(h3KonuJoin)


        print(gelenYaziCokluList)
        if len(gelenYaziCokluList)==0:
            print("""
            *************************************************
            YENİ GELEN GÖRÜŞ YAZISI YOK, PROGRAM ÇALIŞTIRILMAYACAK
            *************************************************
            """)
        elif len(gelenYaziCokluList)!=0:

            


###            #KİŞİSEL ARŞİV

            WebDriverWait(self.browser, 60).until(EC.element_to_be_clickable((By.XPATH,"//*[@id='leftMenuForm:kisiselArsivPanel:kisiselArsivKlasoruTab_header']"))).click() #kişisel arşiv
            
            WebDriverWait(self.browser, 60).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[9]/div[2]/form/div[2]/div[2]/div/ul/li/span/span[1]"))).click()  #altmenü kişisel arşiv

            WebDriverWait(self.browser, 60).until(EC.element_to_be_clickable((By.XPATH,"//*[@id='leftMenuForm:kisiselArsivPanel:kisiselArsivKlasoruTree:0_2']"))).click()   # 3. sıradaki klasörü seçme
            
            
            self.browser.implicitly_wait(60)
            time.sleep(2)
###            


            
            time.sleep(1)
            bakYaziEven=self.browser.find_elements(By.CSS_SELECTOR,f".ui-widget-content.ui-datatable-even.ui-datatable-selectable.ui-inbox-read[data-ri]") 
            self.browser.implicitly_wait(60)
            time.sleep(1)
            bakYaziOdd=self.browser.find_elements(By.CSS_SELECTOR,f".ui-widget-content.ui-datatable-odd.ui-datatable-selectable.ui-inbox-read[data-ri]") 
            self.browser.implicitly_wait(60)
            time.sleep(1)
            bakYaziListe=bakYaziOdd+bakYaziEven
            print(len(bakYaziListe))
            
            for y in range(len(bakYaziListe)):
                time.sleep(1)
                self.browser.switch_to.window(self.browser.window_handles[0])
                self.browser.implicitly_wait(60)           
                konuYaz=self.browser.find_element(By.XPATH,f"//*[@id='mainInboxForm:inboxDataTable:{y}:evrakTable']/tbody/tr[1]/td[2]/div[1]/h3").text   #yazının konusunu text halinde veriyor   
                self.browser.implicitly_wait(60)
                time.sleep(1) 

                gelenKonuJoin=konuCharHarf.konuJoin(konuYaz)

                konuYazim=str(konuYaz).split()
                konuYazim.remove("Konu:")
                konuYazi=" ".join(konuYazim)
                joinKonuSon=(str(konuYazi))
                #print(joinKonuSon) 
                print("OKEYİM-konu") 


                for nestedTuple in gelenYaziCokluList:
                    #if gelenKonuJoin != nestedTuple[1]:  
    
                    if gelenKonuJoin in nestedTuple:        
                    
                        geldYerYazi=self.browser.find_element(By.XPATH,f"//*[@id='mainInboxForm:inboxDataTable:{y}:evrakTable']/tbody/tr[2]/td/div").text
                        self.browser.implicitly_wait(60)
                        time.sleep(1)
                        geldYerYazim=str(geldYerYazi).lstrip("Geldiği Yer:").strip()
                        geldYerList=str(geldYerYazim).split("/")
                        geldYerSon=str(geldYerList[0]).strip()
                        print(geldYerSon)

                        time.sleep(3)

                        sayiYazi=self.browser.find_element(By.XPATH,f"//*[@id='mainInboxForm:inboxDataTable:{y}:evrakTable']/tbody[1]/tr[3]/td[1]/div[1]/span").text
                        self.browser.implicitly_wait(60)
                        time.sleep(1)
                        print(sayiYazi)

                        self.browser.find_element(By.XPATH,f"//*[@id='mainInboxForm:inboxDataTable:{y}:evrakTable']").click()
                        self.browser.implicitly_wait(60)
                        time.sleep(5)
                        self.browser.switch_to.frame("ustYaziOnizlemeId1")  # en sağdaki frame'e iframe id'si ile gitme
                        print("OK-frame")
                        self.browser.implicitly_wait(60)


                        textimDaireYazi=self.browser.find_elements(By.XPATH,"//*[@id='viewer']/div[1]/div[2]/div")
                        self.browser.implicitly_wait(120)
                        time.sleep(5)

                        yaziIcerikListem=[]
                        for text in textimDaireYazi:
                            yaziIcerikListem.append(text.text)
                        print(yaziIcerikListem)
                        time.sleep(2)

                        yaziIlgiIndex=(yaziIcerikListem.index("İlgi"))+2
                        
                        yaziIlgiicerik=yaziIcerikListem[yaziIlgiIndex]
                        print(yaziIlgiicerik)
                        print("OK-yazitext")


                        time.sleep(1)
                        ilgiYaziList=str(yaziIlgiicerik).split()
                        indexilgiTarih=ilgiYaziList.index("tarihli")
                        indexilgiSayi=ilgiYaziList.index("sayılı")
                        ilgiYaziTarihson=ilgiYaziList[indexilgiTarih-1]
                        print(ilgiYaziTarihson)             # gelen yazı (giden yazı ilgi) TARİH
                        yaziilgiSayison=ilgiYaziList[indexilgiSayi-1].split("-")[-1]
                        print(yaziilgiSayison)           # gelen yazı (giden yazı ilgi) SAYI
                                


                        ####

                        import re
                        listem=re.findall(r'\d+', joinKonuSon)    # yazının konusu içindeki sayıları extract ediyor
                        print(listem)
                        listemson=[]
                        listem2=[]
                        for i in listem:
                            if int(max(listem))<2100:          
                                listem.clear()
                                listemson=listem
                                print(listemson)

                            elif int(i)>2100:
                                listem2.append(i)
                                listemson=listem2
                                print(listemson)
                        
                        print(listemson)

                    
                        self.browser.execute_script("window.open()")
                        print(self.browser.window_handles)
                        self.browser.switch_to.window(self.browser.window_handles[1])   # yeni pencere/sekme
                        self.browser.get("http://eced.csb.gov.tr/ced/jsp/portal/main2.htm") 
                        self.browser.implicitly_wait(60)
                        
                        ale = self.browser.switch_to.alert  # ced sayfasında çıkan uyarıyı kaldırma
                        ale.accept()


                        self.browser.find_element(By.XPATH,"//*[@id='j_username']").send_keys("username")
                        self.browser.find_element(By.XPATH,"//*[@id='j_password']").send_keys("password")

                        self.browser.implicitly_wait(60)

                        self.browser.find_element(By.XPATH,"/html/body/header/nav/ul/div/form/div/span[5]/input").click()   # şifre giriş butonununa tıklama

                        self.browser.implicitly_wait(60)
                    
                        if len(listemson)==0:           #yazının konusundaki numaraların atıldığı listenin boş olması halinde  
                            print(joinKonuSon)
                            while True:  
                                print("bu mu acaba")                   
                                projeAdi=input("""
                                
                                ***************************************
                                Proje adını/adının bir kısmını giriniz: 
                                ***************************************
                                
                                
                                """)
                                self.browser.find_element(By.XPATH,"//*[@id='ad']").clear()
                                self.browser.implicitly_wait(60)
                                self.browser.find_element(By.XPATH,"//*[@id='ad']").send_keys(projeAdi)  # kullanıcıdan alınan proje adını ced sisteminde arama
                                self.browser.implicitly_wait(60)
                                self.browser.find_element(By.XPATH,"//*[@id='ara']").click()   
                                self.browser.implicitly_wait(60)       

                                kayit=self.browser.find_element(By.XPATH,"/html/body/div[1]/div[2]/div[2]").text    # arama sonunda kayıt bulunursa duruyor, yoksa sonraki numaraya geçiyor. 
                                
                                self.browser.implicitly_wait(60) 
                                time.sleep(2)
                                kayit2=self.browser.find_element(By.XPATH,"//div[@id='main']").text   #kayıt bulunamadı


                                
                                kayit3=self.browser.find_element(By.XPATH,"//*[@id='main']/span[1]").text   #...kayıt bulundu,

                            
                                time.sleep(2)
                                self.browser.implicitly_wait(60) 
                                print(kayit)
                                # print(kayit2)
                                


                                if "Bir kayıt bulundu." in kayit:
                                    self.browser.implicitly_wait(60)
                                    #self.browser.find_element(By.XPATH,"//*[@id='pr']/tbody/tr/td[12]/input").click()   #ced satırındaki "Ayrıntılar" butonu
                                    self.browser.find_element(By.CSS_SELECTOR,".b > td:nth-child(12) > input:nth-child(1)").click()   #ced satırındaki "Ayrıntılar" butonu
                                    #html body div.wrap div#content div#main table#pr.app tbody tr.b td input
                                    self.browser.implicitly_wait(60) 
                                    break                   
                                elif kayit2=="Kayıt Bulunamadı":  
                                                    
                                    print(f"Kayıt yok- {projeAdi}") 

                                elif "tane kayıt bulundu;" in kayit:
                                    cedSecimInput=input("""
                                    
                                    
                                    ******************************
                                    Projeyi listeden sen seç(y/n): 
                                    ******************************
                                    
                                    
                                    """)
                                    print(cedSecimInput)
                                    if cedSecimInput=="y":
                                        print("OK- ÇED seçimi tamamlandı")
                                    elif cedSecimInput=="n":
                                        print("Seçim yapılmadı, proje adına geri dönülecek...")
                                        continue
                                elif "kayıt bulundu," in kayit:
                                    cedSecimInput=input("""
                                    
                                    ******************************
                                    Projeyi listeden sen seç(y/n): 
                                    ******************************
                                    
                                    """)
                                    print(cedSecimInput)
                                    if cedSecimInput=="y":
                                        print("OK- ÇED seçimi tamamlandı")
                                    elif cedSecimInput=="n":
                                        print("Seçim yapılmadı, proje adına geri dönülecek...")
                                        continue
                                    
                                break       
                            
                        
                        elif len(listemson)!=0:    #yazının konusundaki numaraların atıldığı listenin dolu olması halinde 
                            for num in listemson:  
                                print(num)
                                
                                self.browser.find_element(By.XPATH,"//*[@id='ad']").send_keys(num)  # eğer yazının konusu içindeki numara uygunsa bu numarayı ced sisteminde aratır
                                self.browser.implicitly_wait(60)
                                self.browser.find_element(By.XPATH,"//*[@id='ara']").click()
                                self.browser.implicitly_wait(60)

                                kayit=self.browser.find_element(By.XPATH,"/html/body/div[1]/div[2]/div[2]").text    # arama sonunda kayıt bulunursa duruyor, yoksa sonraki numaraya geçiyor. 

                                self.browser.implicitly_wait(60)
                                print(kayit)

                                
                                if "Bir kayıt bulundu" in kayit:
                                    print(kayit)
                                    self.browser.implicitly_wait(60)
                                    self.browser.find_element(By.XPATH,"//*[@id='pr']/tbody/tr/td[12]/input").click()   #ced satırındaki "Ayrıntılar" butonu

                                    self.browser.implicitly_wait(60)
                                    break
                                elif "Kayıt Bulunamadı" in kayit :  
                                                    
                                    print(f"Kayıt yok") 
                                    
                                    while True:    
                                        print("yoksa bu mu acaba") 
                                        kayit=self.browser.find_element(By.XPATH,"/html/body/div[1]/div[2]/div[2]").text    # arama sonunda kayıt bulunursa duruyor, yoksa sonraki numaraya geçiyor.
                                        self.browser.implicitly_wait(60)
                                        print(kayit)
                                        #print(nihaiYaziIc)
                                        print(joinKonuSon)                 
                                        projeAdi=input("""
                                        
                                        ********************************
                                        Proje adını/bir kısmını giriniz: 
                                        ********************************

                                        
                                        """)
                                        self.browser.find_element(By.XPATH,"//*[@id='ad']").clear()
                                        self.browser.implicitly_wait(60)
                                        self.browser.find_element(By.XPATH,"//*[@id='ad']").send_keys(projeAdi)  # kullanıcıdan alınan proje adını ced sisteminde arama
                                        self.browser.implicitly_wait(60)
                                        self.browser.find_element(By.XPATH,"//*[@id='ara']").click()   
                                        self.browser.implicitly_wait(60)
                                        
                                        kayit=self.browser.find_element(By.XPATH,"/html/body/div[1]/div[2]/div[2]").text    # arama sonunda kayıt bulunursa duruyor, yoksa sonraki numaraya geçiyor.
                                        self.browser.implicitly_wait(60)
                                        time.sleep(2)
                                        print(kayit)
                                        if "Bir kayıt bulundu." in kayit:
                                            print("kayıt bulunmuş olması lazım")
                                            self.browser.implicitly_wait(60)
                                            
                                            self.browser.find_element(By.CSS_SELECTOR,".b > td:nth-child(12) > input:nth-child(1)").click()   #ced satırındaki "Ayrıntılar" butonu

                                            self.browser.implicitly_wait(60) 
                                            break    
                                        elif "tane kayıt bulundu;" in kayit:
                                            cedSecimInput=input("""
                                            
                                            *****************************
                                            Projeyi listeden sen seç(y/n): 
                                            ******************************
                                            
                                            
                                            """)
                                            print(cedSecimInput)
                                            if cedSecimInput=="y":
                                                print("OK- ÇED seçimi tamamlandı")
                                            elif cedSecimInput=="n":
                                                print("Seçim yapılmadı, proje adına geri dönülecek...")
                                                
                                        elif "kayıt bulundu," in kayit:
                                            cedSecimInput=input("""
                                            

                                            ******************************
                                            Projeyi listeden sen seç(y/n): 
                                            ******************************

                                            
                                            """)
                                            print(cedSecimInput)
                                            if cedSecimInput=="y":
                                                print("OK- ÇED seçimi tamamlandı")
                                                break
                                            elif cedSecimInput=="n":
                                                print("Seçim yapılmadı, proje adına geri dönülecek...")
                                                continue
                                        elif kayit=="Kayıt Bulunamadı":  
                                                    
                                            print(f"Kayıt yok- {projeAdi}") 
                                        else:
                                            print("hata mı var acaba")
                                        break
                                            
                                    break               

                                elif "kayıt bulundu," in kayit:
                                    cedSecimInput=input("""
                                    
                                    
                                    *****************************
                                    Projeyi listeden sen seç(y/n): 
                                    *****************************
                                    
                                    
                                    """)
                                    print(cedSecimInput)
                                    if cedSecimInput=="y":
                                        print("OK- ÇED seçimi tamamlandı")
                                        break
                                    elif cedSecimInput=="n":
                                        print("Seçim yapılmadı, proje adına geri dönülecek...")
                                        

                                
                                break

                        time.sleep(3) 

                        for kunye in range(1,13):    
                            kunyeAdı=self.browser.find_element(By.XPATH,f"//*[@id='main']/table/tbody/tr[{kunye}]/td[1]").text
                            self.browser.implicitly_wait(120)
                            ilAdison=""
                            if kunyeAdı=="İl":
                                ilAdi=self.browser.find_element(By.XPATH,f"//*[@id='main']/table/tbody/tr[{kunye}]/td[2]").text.strip(":")
                                self.browser.implicitly_wait(120)
                                
                                
                                if re.search('[,]', str(ilAdi).strip()):    
                                    textList=str(ilAdi).split(",")
                                    print(textList)
                                    textil=str(textList[0]).strip(":")
                                    ilAdison=textil.strip()
                                    #print(ilAdison)
                                    break
                                else:    
                                    textList=str(ilAdi).strip().split(" ")
                                    #print(textList)
                                    textil=(textList[0]).strip(":")
                                    ilAdison=textil.strip()
                                    #print(ilAdison)                    
                                    break
                        print(ilAdison)


                        for kunye in range(1,13):    
                            kunyeAdı=self.browser.find_element(By.XPATH,f"//*[@id='main']/table/tbody/tr[{kunye}]/td[1]").text
                            self.browser.implicitly_wait(120)
                            ilceAdison=""
                            if kunyeAdı=="İlçe":
                                ilceAdi=self.browser.find_element(By.XPATH,f"//*[@id='main']/table/tbody/tr[{kunye}]/td[2]").text.strip(":")
                                self.browser.implicitly_wait(120)
                                if re.search('[,]', str(ilceAdi).strip()):    
                                    textList=str(ilceAdi).split(",")
                                    #print(textList)
                                    textilce=str(textList[0]).strip(":")
                                    ilceAdison=textilce.strip()
                                    #print(ilceAdison)
                                    break
                                else:    
                                    textList=str(ilceAdi).strip().split(" ")
                                    #print(textList)
                                    textilce=str(textList[0]).strip(":")
                                    ilceAdison=textilce.strip()
                                    #print(ilceAdison)
                                    break
                        print(ilceAdison)

                        ruhsatNoNoson=""    
                        for kunye in range(1,13):    
                            kunyeAdı=self.browser.find_element(By.XPATH,f"//*[@id='main']/table/tbody/tr[{kunye}]/td[1]").text
                            self.browser.implicitly_wait(120)
                                        
                            if kunyeAdı=="Ruhsat Numarası":
                                
                                ruhsatNo=self.browser.find_element(By.XPATH,f"//*[@id='main']/table/tbody/tr[{kunye}]/td[2]").text.strip(":")
                                self.browser.implicitly_wait(120)
                                #print(ruhsatNo)
                                ruhsatNom=re.findall(r'\d+', ruhsatNo)

                                for i in ruhsatNom:
                                    if int(i)<2150:
                                        ruhsatNom.remove(i) 
                                        print(ruhsatNom)

                                    if len(ruhsatNom)==0:                    
                                        ruhsatNoNoson=ilAdison
                                    elif len(ruhsatNom)!=0:
                                        ruhsatNoNo=str(ruhsatNom[0]) 
                                        ruhsatNoNoson=ruhsatNoNo   #çedin ruhsat nosunu alma 
                                    break               
                                
                                print(ruhsatNoNoson) 
                                break
                                    

                            elif kunyeAdı!="Ruhsat Numarası":
                                ruhsatNoNoson=ilAdison
                            print(ruhsatNoNoson)


                # ÇED KLASÖRÜ İÇİNDE KLASÖR OLUŞTURMA


                        print(ruhsatNoNoson)
                        print(ilAdison)
                        print(ilceAdison)



                        if len(listemson)==0:           #yazının konusundaki numaraların atıldığı listenin boş olması halinde  
                            FileName=((f"{ruhsatNoNoson}_"+f"{ilAdison}_"+f"{ilceAdison}"))     #yeni klasörün adını oluşturma
                            #newFileName=newFileNames
                            print(FileName)            

                                    
                        elif len(listemson)!=0:    #yazının konusundaki numaraların atıldığı listenin dolu olması halinde 
                            for num in listemson:  
                                print(num)

                                if int(num)<2500:   #yazının konusundaki numaraların atıldığı listedeki numaraların 2500'den küçük olması halinde proje adı inputuyla kullanıcıya sorar
                                    FileName=((f"{ruhsatNoNoson}_"+f"{ilAdison}_"+f"{ilceAdison}"))     #yeni klasörün adını oluşturma
                                    #newFileName=newFileNames
                                    print(FileName)                                  
                                         

                                else:
                                    FileName=((f"{num}_"+f"{ilAdison}_"+f"{ilceAdison}")) 
                                    print(FileName)
                                    
                                    break
                                
                        dosyaListem=os.listdir("C:/Users/tugbacanan.oguz/Desktop/CED")    #ÇED kaydedilen klasörün listesini alıyor, yeni klasör numarasını tespit etmek için
                        print(dosyaListem)

                        dosyaListem2=[]
                        for i in dosyaListem:
                            klasorAdi=(i.split("-"))[1]
                            dosyaListem2.append(klasorAdi)
                        print(dosyaListem2)
                        klasorKayıt=""
                        indexDosya=""
                        if FileName in dosyaListem2:
                            indexDosyaa=(dosyaListem2.index(FileName))+301
                            klasorKayıt2=dosyaListem2[dosyaListem2.index(FileName)]
                            klasorKayıtt=dosyaListem[dosyaListem2.index(FileName)]
                            klasorKayıt=klasorKayıtt
                            indexDosya=indexDosyaa
                            print(klasorKayıt2)
                            print(klasorKayıt)
                            print(indexDosya)
                            print("OK-doğru dosya bulundu")



                            self.browser.implicitly_wait(60)
                            self.browser.switch_to.window(self.browser.window_handles[0])
                            self.browser.implicitly_wait(120)
                            WebDriverWait(self.browser, 120).until(EC.element_to_be_clickable((By.XPATH,"//*[@id='esm_246802192_emi_286053589']"))).click()      # gelen kutusunu tıklar

                            self.browser.implicitly_wait(60)
                            time.sleep(10)


                            WebDriverWait(self.browser, 160).until(EC.element_to_be_clickable((By.XPATH,"//*[@id='esm_246802192_emi_286053589']"))).click()      # gelen kutusunu tıklar
                            self.browser.implicitly_wait(120)
                            time.sleep(7)
                            gelYaziNo=self.browser.find_element(By.CSS_SELECTOR,"a[id='esm_246802192_emi_286053589'] span[class='ui-menuitem-text']").text
                            #gelYaziNo=self.browser.find_element(By.XPATH,"//a[@class='ui-menuitem-link ui-corner-all ui-menuitem-default ui-menuitem-unread ui-menuitem-selected ui-state-highlight']").text
                            self.browser.implicitly_wait(60)
                            time.sleep(2)        
                            gelYaziNoList=str(gelYaziNo).lstrip("Gelen Evraklar ").split("/")
                            gelYaziNom=int(gelYaziNoList[1].rstrip(")"))
                            print(gelYaziNom) 



                            daireListe=["Geldiği Yer: Su Yönetimi Genel Müdürlüğü / İzleme ve Su Bilgi Sistemi Daire Başkanlığı","Geldiği Yer: Su Yönetimi Genel Müdürlüğü / Havza Yönetimi Daire Başkanlığı","Geldiği Yer: Su Yönetimi Genel Müdürlüğü / Taşkın ve Kuraklık Yönetimi Daire Başkanlığı","Geldiği Yer: Su Yönetimi Genel Müdürlüğü / Su Kalitesi Daire Başkanlığı"]
                            for i in range(0,gelYaziNom-4):
                                time.sleep(0.5)
                                gelenKonu=self.browser.find_element(By.XPATH,f"//*[@id='mainInboxForm:inboxDataTable:{i}:evrakTable']/tbody/tr[1]/td[2]/div[1]/h3").text        # tüm gelen yazıların konusunu alır
                                self.browser.implicitly_wait(120)
                                print(gelenKonu)

                                gorusKonuJoin=konuCharHarf.konuJoin(gelenKonu)


                                time.sleep(0.5)
                                geldigiYer=self.browser.find_element(By.XPATH,f"//*[@id='mainInboxForm:inboxDataTable:{i}:evrakTable']/tbody/tr[2]/td/div").text        # tüm gelen yazıların geldiği yeri alır
                                self.browser.implicitly_wait(120)
                                print(geldigiYer)
                                time.sleep(0.5)
                                
                                if geldigiYer=="Geldiği Yer: Su Yönetimi Genel Müdürlüğü / İzleme ve Su Bilgi Sistemi Daire Başkanlığı":
                                    geldigiYerD="izleme"
                                elif geldigiYer=="Geldiği Yer: Su Yönetimi Genel Müdürlüğü / Havza Yönetimi Daire Başkanlığı":
                                    geldigiYerD="havza"
                                elif geldigiYer=="Geldiği Yer: Su Yönetimi Genel Müdürlüğü / Taşkın ve Kuraklık Yönetimi Daire Başkanlığı":
                                    geldigiYerD="taşkın"
                                elif geldigiYer=="Geldiği Yer: Su Yönetimi Genel Müdürlüğü / Su Kalitesi Daire Başkanlığı":
                                    geldigiYerD="kalite"
                                else:
                                    geldigiYerD="diğer"
                                    
                                
                                print(geldigiYerD)
                                time.sleep(1)


                                print(gorusKonuJoin)
                                print(gelenKonuJoin)

                                if ((gorusKonuJoin in gelenKonuJoin) or (gelenKonuJoin in gorusKonuJoin)) and (geldigiYer in daireListe):       # kişisel arşivde işlem yapılması istenen yazı konusu ile gelen kutusundaki yazıların konusunu karşılaştırır
                                    #if ((harfListemTrue>=2) or ((konuYazi in gelenKonumm) or (gelenKonumm in konuYazi))) and (geldigiYer in daireListe):       # kişisel arşivde işlem yapılması istenen yazı konusu ile gelen kutusundaki yazıların konusunu karşılaştırır
                                    self.browser.find_element(By.XPATH,f"//table[@id='mainInboxForm:inboxDataTable:{i}:evrakTable']").click() 
                                    self.browser.implicitly_wait(120)
                                    time.sleep(3)
                                    print("OK")
                                    self.browser.switch_to.frame("ustYaziOnizlemeId1")  # en sağdaki frame'e iframe id'si ile gitme
                                    self.browser.implicitly_wait(120)
                                    time.sleep(2)
                                    print("OK-frame")                                    
                                    
                                    textim=self.browser.find_elements(By.XPATH,"//*[@id='viewer']/div[1]/div[2]/div")
                                    self.browser.implicitly_wait(120)
                                    time.sleep(4)

                                    print("OK-textyazi")

                                    

                                    cedMetinListem=[]
                                    for text in textim:
                                        print(text.text)
                                        cedMetinListem.append(text.text)  
                                    time.sleep(2)                 
                                    print(cedMetinListem)

                                            
                                    ilgiIndex=(cedMetinListem.index("İlgi"))+2  #ilgi yazının sayısını alıp karşılaştırır

                                    time.sleep(2)
                                    ilgiListe=cedMetinListem[ilgiIndex].split()
                                    ilgiSayiIndexim=""
                                    for z in ilgiListe: # ilgi yazının tarih indexini alır
                                        while z=="tarihli":
                                            tarihIndex=ilgiListe.index("tarihli")-1
                                            print(tarihIndex)
                                            break
                                        while z=="sayılı":  #ilgi yazının sayı indexini alır                        
                                            sayiIndex=ilgiListe.index("sayılı")-1
                                            print(sayiIndex)                    
                                            ilgiSayiIndex=ilgiListe[sayiIndex].split("-")[3]
                                            ilgiSayiIndexim=ilgiSayiIndex
                                            break

                                        print(ilgiSayiIndexim)                        
                                    

                                    if sayiYazi==ilgiSayiIndexim:   # görüş yazısının sayısı ile cevabi yazının ilgisinin sayısını karşılaştırır, aynıysa  
                                        self.browser.implicitly_wait(60)
                                        self.browser.find_element(By.XPATH,"//*[@id='secondaryToolbarToggle']").click() # pencere max değilken sağdaki >> menüyü tıklar
                                        self.browser.implicitly_wait(60)
                                        self.browser.find_element(By.XPATH,"//*[@id='secondaryDownload']").click()  # açılan menüden "indir" seçeneğini tıklayarak yazıyı indirir                    
                                        self.browser.implicitly_wait(60)

                                        try:
                                            os.mkdir(f'C:/Users/tugbacanan.oguz/Desktop/CED/{klasorKayıt}/{geldigiYerD}')  
                                            time.sleep(1)
                                            print("OK-mkdir")
                                            hata=""
                                        except FileExistsError as FEE:
                                            print(FEE)
                                            print("""
                                            ********************************************************
                                            KLASÖR ZATEN MEVCUT, KLASÖRÜ BAŞKA YERE TAŞIYIN...
                                            ********************************************************
                                            """)
                                            hata="klasör mevcut"

                                        if hata=="klasör mevcut":
                                            print(input("""
                                            ********************************************************
                                            KLASÖRÜ BAŞKA YERE KALDIRDIYSANIZ 'y' TUŞUNA BASIP ENTER'A TIKLAYINIZ...
                                            ********************************************************

                                            """))
                                            os.mkdir(f'C:/Users/tugbacanan.oguz/Desktop/CED/{klasorKayıt}/{geldigiYerD}')  
                                            time.sleep(1)
                                            print("OK-mkdir")
                                                                        
                                        
                                        time.sleep(1)

                                        
                                        while True:
                                            list_of_files_rapor = glob.glob('C:/Users/tugbacanan.oguz/Downloads/*') # * means all if need specific format then *.csv
                                            latest_file_rapor = max(list_of_files_rapor, key=os.path.getctime)
                                            print(latest_file_rapor)
                                            dosyaAdi=str(latest_file_rapor).lstrip("C:/Users/tugbacanan.oguz/Downloads/")
                                            if dosyaAdi.endswith("crdownload"):
                                                print("daha yüklenmedi, yüklemeye devam edilecek...")
                                                time.sleep(2)
                                            else:
                                                print("yükleme tamamlandı")
                                                break


                                        list_of_files = glob.glob('C:/Users/tugbacanan.oguz/Downloads/*') # * means all if need specific format then *.csv
                                        latest_file = max(list_of_files, key=os.path.getctime)
                                        print(latest_file)
                                        dosyaAdi=str(latest_file).lstrip("C:/Users/tugbacanan.oguz/Downloads/")

                                        ustYazipath=f'C:/Users/tugbacanan.oguz/Desktop/CED/{klasorKayıt}/{geldigiYerD}/{geldigiYerD}.pdf'
                                        shutil.move(f"C:/Users/tugbacanan.oguz/Downloads/{dosyaAdi}", ustYazipath)  
                                        time.sleep(1)                  

                                        print("OK")
                                        

                                    self.browser.implicitly_wait(60)
                                    time.sleep(1)
                                    self.browser.execute_script("window.open()")
                                    self.browser.switch_to.window(self.browser.window_handles[1])   # yeni sekmede belgenet
                                    self.browser.get("https://e-belge.tarim.gov.tr/edys-web/sistemeGiris.xhtml") 
                                    self.browser.implicitly_wait(60)
                                    self.browser.switch_to.window(self.browser.window_handles[0])
                                    self.browser.implicitly_wait(60)
                                    time.sleep(5)
                                    x=self.browser.find_element(By.XPATH,"//form[@name='mainPreviewForm']//li[5]").text        
                                    self.browser.implicitly_wait(60)
                                    time.sleep(1)
                                    print(x)
                                    if x=="Evrak Ekleri":
                                        self.browser.find_element(By.XPATH,"//form[@name='mainPreviewForm']//li[5]").click()
                                        self.browser.implicitly_wait(60)
                                        ek=self.browser.find_elements(By.XPATH,"//div[@class='ui-datatable ui-widget myLovGrid']//table[@role='grid']//tbody//tr")
                                        self.browser.implicitly_wait(60)
                                        print(len(ek))
                                        for i in range(1,len(ek)+1):
                                            
                                            dosyaText=self.browser.find_element(By.XPATH,f"//div[@class='ui-datatable ui-widget myLovGrid']//table[@role='grid']//tbody//tr[{i}]/td[4]/div[1]/span[1]").text
                                            self.browser.implicitly_wait(60)
                                            self.browser.find_element(By.XPATH,f"//div[@class='ui-datatable ui-widget myLovGrid']//table[@role='grid']//tbody//tr[{i}]/td[5]/button[1]/span[1]").click()
                                            self.browser.implicitly_wait(60)
                                            time.sleep(3)
                                            print(dosyaText)  
                                            list_of_files2 = glob.glob('C:/Users/tugbacanan.oguz/Downloads/*') # * means all if need specific format then *.csv
                                            latest_file2 = max(list_of_files2, key=os.path.getctime)
                                            print(latest_file2)
                                            dosyaAdi2=str(latest_file2).lstrip("C://Users//tugbacanan.oguz//Downloads//")
                                            print(dosyaAdi2)

                                            ekPath=f'C://Users//tugbacanan.oguz//Desktop//CED//{klasorKayıt}//{geldigiYerD}//{dosyaAdi2}'
                                            #print(ekPath)
                                            time.sleep(1)
                                            shutil.move(f"C://Users//tugbacanan.oguz//Downloads//{dosyaAdi2}", ekPath)                                                  
                                            time.sleep(1)  
                                                
                                        print("OK-tüm ekler")  
                                    

                                    else:
                                        print("ek yok")     

                                    self.browser.implicitly_wait(60)         
                                    self.browser.find_element(By.XPATH,f"//*[@id='mainPreviewForm:onizlemeRightTab:uiRepeat:5:cmdbutton'] ").click() # evrak kapat sekmesini tıklar   
                                    self.browser.implicitly_wait(60)
                                    time.sleep(3)
                                    self.browser.find_element(By.XPATH,f"//*[@id='mainPreviewForm:klasorLov_id:favoriteTreeButton']").click()  #favori(yıldız butonu) klasör seç 
                                    self.browser.implicitly_wait(60)
                                    time.sleep(3)
                                    self.browser.find_element(By.XPATH,f"//*[@id='mainPreviewForm:klasorLov_id:lovTree:0']/span/span[3]/div").click()      # klasörü tıkla
                                    self.browser.implicitly_wait(60)
                                    time.sleep(3)
                                    self.browser.find_element(By.XPATH,f"//*[@id='mainPreviewForm:onaysizKapatId']").click()   #evrak kapat butonunu tıklar
                                    self.browser.implicitly_wait(60)  
                                    time.sleep(8) 
                                    print("OK-x")

                                    from datetime import datetime
                                    import locale
                                    locale.setlocale(locale.LC_ALL, '') # local dili ayarlar, böylece aşağıdaki datetime çıktılarını türkçe verir

                                    simdi= datetime.today()
                                    result=datetime.strftime(simdi, "%d.%m.%Y %A") # gün.ay.yıl gün adı formatında bugünün tarihini verir
                                    print(result)

                                    daireListesiKısa=["havza","izleme","taşkın","kalite"]
                                    klasorKayitList=os.listdir(f'C:/Users/tugbacanan.oguz/Desktop/CED/{klasorKayıt}')

                                    a_set = set(daireListesiKısa)
                                    b_set = set(klasorKayitList)

                                    ortakDaire=(a_set & b_set)

                                    if ortakDaire:
                                        print(len(ortakDaire))                        

                                    gorusSayi=len(ortakDaire)
                                    if gorusSayi==4:                          
                                        file=open(f"C:/Users/tugbacanan.oguz/Desktop/Kapatma Listesi.txt","a", encoding="utf-8") # türkçe karakterler de dahil pek çok karakteri tanıması için encoding yapıyoruz
                                        file.write(f"{result}.....{indexDosya}-{FileName}.........{klasorKayıt}/{geldigiYerD}\n****{gorusSayi} YAZI TAMAMLANDI, cevap yazılabilir...****\n")
                                        file.close()
                                        time.sleep(3)  
                                                        
                                    else: 
                                        file=open(f"C:/Users/tugbacanan.oguz/Desktop/Kapatma Listesi.txt","a", encoding="utf-8") # türkçe karakterler de dahil pek çok karakteri tanıması için encoding yapıyoruz
                                        file.write(f"{result}.....{indexDosya}-{FileName}.........{klasorKayıt}/{geldigiYerD} (*{gorusSayi})\n")
                                        file.close()
                                        time.sleep(3)
                                    time.sleep(2)

                                    print("x'i sil")
                                    print(f"indexDosya {indexDosya}")

                                    if geldigiYerD=="izleme":
                                        print("izleme")
                                        excel=ExcelDosya((int(indexDosya)+2),10, "")
                                        excel.xSil()
                                        print("izleme x silindi")

                                    elif geldigiYerD=="havza":
                                        print("havza")
                                        excel=ExcelDosya((int(indexDosya)+2),11, "")
                                        excel.xSil()
                                        print("havza x silindi")

                                    elif geldigiYerD=="taşkın":
                                        print("taşkın")
                                        excel=ExcelDosya((int(indexDosya)+2),12, "")
                                        excel.xSil()
                                        print("taşkın x silindi")

                                    elif geldigiYerD=="kalite":
                                        print("kalite")
                                        excel=ExcelDosya((int(indexDosya)+2),13, "")
                                        excel.xSil()
                                        print("kalite x silindi")

                                    else:
                                        print("hata var")

                                    if gorusSayi==4:
                                        excel=ExcelDosya((int(indexDosya)+2),17, "")
                                        excel.fillYellow()


                                    time.sleep(2)                                


                        else:
                            self.browser.switch_to.window(self.browser.window_handles[0])
                            self.browser.implicitly_wait(60)
                            WebDriverWait(self.browser, 60).until(EC.element_to_be_clickable((By.XPATH,"//*[@id='esm_246802192_emi_286053589']"))).click()      # gelen kutusunu tıklar
                            
                            # identify dropdown with Select class
                            time.sleep(4)
                            self.browser.implicitly_wait(60)
                            sel100 = Select(self.browser.find_element(By.XPATH,"//div[@class='ui-paginator ui-paginator-top ui-widget-header']//select[@name='mainInboxForm:inboxDataTable_rppDD']"))   #sayfada görünen yazı sayısını 100'e çıkarır
                            time.sleep(2)
                            #select by select_by_visible_text() method
                            sel100.select_by_visible_text("100")
                            self.browser.implicitly_wait(60)
                            print("OK-100")
                            time.sleep(4)
                            

                            gelenReadevenList=self.browser.find_elements(By.CSS_SELECTOR,f".ui-widget-content.ui-datatable-even.ui-datatable-selectable.ui-inbox-read[data-ri]")    #aşağıdaki satırlarla beraber tüm gelen yazı listesini alır (sayı olarak)
                            self.browser.implicitly_wait(60)
                            time.sleep(2)
                            gelenReadoddList=self.browser.find_elements(By.CSS_SELECTOR,f".ui-widget-content.ui-datatable-odd.ui-datatable-selectable.ui-inbox-read[data-ri]")
                            self.browser.implicitly_wait(60)
                            time.sleep(2)
                            gelenUnreadevenList=self.browser.find_elements(By.CSS_SELECTOR,f".ui-widget-content.ui-datatable-even.ui-datatable-selectable.ui-inbox-unread[data-ri]")
                            self.browser.implicitly_wait(60)
                            time.sleep(2)
                            gelenUnreadoddList=self.browser.find_elements(By.CSS_SELECTOR,f".ui-widget-content.ui-datatable-odd.ui-datatable-selectable.ui-inbox-unread[data-ri]")
                            self.browser.implicitly_wait(60)
                            time.sleep(2)
                            #gelenList=gelenUnreadevenList+gelenUnreadoddList
                            gelenList=gelenReadevenList+gelenReadoddList+gelenUnreadevenList+gelenUnreadoddList #tüm gelen yazı listesini tek liste yapar(okunmuş-okunmamış-tek-çift)
                            time.sleep(1)

                            print(len(gelenList))
                            time.sleep(2)

                            time.sleep(1)

                            daireListe=["Geldiği Yer: Su Yönetimi Genel Müdürlüğü / İzleme ve Su Bilgi Sistemi Daire Başkanlığı","Geldiği Yer: Su Yönetimi Genel Müdürlüğü / Havza Yönetimi Daire Başkanlığı","Geldiği Yer: Su Yönetimi Genel Müdürlüğü / Taşkın ve Kuraklık Yönetimi Daire Başkanlığı","Geldiği Yer: Su Yönetimi Genel Müdürlüğü / Su Kalitesi Daire Başkanlığı"]
                            for i in range(0,int(len(gelenList))-2):
                                time.sleep(1)
                                gelenKonular=self.browser.find_element(By.XPATH,f"//*[@id='mainInboxForm:inboxDataTable:{i}:evrakTable']/tbody/tr[1]/td[2]/div[1]/h3").text        # tüm gelen yazıların konusunu alır
                                #print(gelenKonular)
                                gelenKonularim=gelenKonular.lstrip("Konu: ")
                                print(gelenKonularim)
                                time.sleep(1)
                                geldigiYer=self.browser.find_element(By.XPATH,f"//*[@id='mainInboxForm:inboxDataTable:{i}:evrakTable']/tbody/tr[2]/td/div").text        # tüm gelen yazıların geldiği yeri alır
                                print(geldigiYer)
                                time.sleep(1)
                                
                                if geldigiYer=="Geldiği Yer: Su Yönetimi Genel Müdürlüğü / İzleme ve Su Bilgi Sistemi Daire Başkanlığı":
                                    geldigiYerD="izleme"
                                elif geldigiYer=="Geldiği Yer: Su Yönetimi Genel Müdürlüğü / Havza Yönetimi Daire Başkanlığı":
                                    geldigiYerD="havza"
                                elif geldigiYer=="Geldiği Yer: Su Yönetimi Genel Müdürlüğü / Taşkın ve Kuraklık Yönetimi Daire Başkanlığı":
                                    geldigiYerD="taşkın"
                                elif geldigiYer=="Geldiği Yer: Su Yönetimi Genel Müdürlüğü / Su Kalitesi Daire Başkanlığı":
                                    geldigiYerD="kalite"
                                else:
                                    geldigiYerD="diğer"
                                    
                                
                                print(geldigiYerD)
                                time.sleep(1)

                                if ((konuYazi in gelenKonularim) or (gelenKonularim in konuYazi)) and (geldigiYer in daireListe):       # kişisel arşivde işlem yapılması istenen yazı konusu ile gelen kutusundaki yazıların konusunu karşılaştırır
                                    self.browser.find_element(By.XPATH,f"//table[@id='mainInboxForm:inboxDataTable:{i}:evrakTable']").click() 
                                    self.browser.implicitly_wait(60)
                                    time.sleep(2)
                                    print("OK")
                                    self.browser.switch_to.frame("ustYaziOnizlemeId1")  # en sağdaki frame'e iframe id'si ile gitme
                                    self.browser.implicitly_wait(60)
                                    time.sleep(3)
                                    print("OK-frame")
                                    textim=self.browser.find_elements(By.XPATH,"//*[@id='viewer']/div[1]/div[2]/div")
                                    self.browser.implicitly_wait(60)
                                    time.sleep(2)
                                    print("OK-textyazi")

                                    cedMetinListem=[]
                                    for text in textim:
                                        print(text.text)
                                        cedMetinListem.append(text.text)  
                                                    

                                            
                                    ilgiIndex=(cedMetinListem.index("İlgi"))+2  #ilgi yazının sayısını alıp karşılaştırır

                                    ilgiListe=cedMetinListem[ilgiIndex].split()
                                    ilgiSayiIndexim=""
                                    for z in ilgiListe: # ilgi yazının tarih indexini alır
                                        while z=="tarihli":
                                            tarihIndex=ilgiListe.index("tarihli")-1
                                            print(tarihIndex)
                                            break
                                        while z=="sayılı":  #ilgi yazının sayı indexini alır                        
                                            sayiIndex=ilgiListe.index("sayılı")-1
                                            print(sayiIndex)                    
                                            ilgiSayiIndex=ilgiListe[sayiIndex].split("-")[3]
                                            ilgiSayiIndexim=ilgiSayiIndex
                                            break

                                        print(ilgiSayiIndexim)                        
                                    

                                    if sayiYazi==ilgiSayiIndexim:   # görüş yazısının sayısı ile cevabi yazının ilgisinin sayısını karşılaştırır, aynıysa  
                                        self.browser.implicitly_wait(60)
                                        self.browser.find_element(By.XPATH,"//*[@id='secondaryToolbarToggle']").click() # pencere max değilken sağdaki >> menüyü tıklar
                                        self.browser.implicitly_wait(60)
                                        self.browser.find_element(By.XPATH,"//*[@id='secondaryDownload']").click()  # açılan menüden "indir" seçeneğini tıklayarak yazıyı indirir                    
                                        self.browser.implicitly_wait(60)     


                                        try:
                                            os.mkdir(f'C:\\Users\\tugbacanan.oguz\\Desktop\\CEDgorus\\{klasorKayıt}\{geldigiYerD}')
                                            print("OK-mkdir")
                                            time.sleep(1)  
                                            hata=""
                                        except FileExistsError as FEE:
                                            print(FEE)
                                            print("""
                                            ********************************************************
                                            KLASÖR ZATEN MEVCUT, KLASÖRÜ BAŞKA YERE TAŞIYIN...
                                            ********************************************************
                                            """)
                                            hata="klasör mevcut"

                                        if hata=="klasör mevcut":
                                            print(input("""
                                            ********************************************************
                                            KLASÖRÜ BAŞKA YERE KALDIRDIYSANIZ 'y' TUŞUNA BASIP ENTER'A TIKLAYINIZ...
                                            ********************************************************
                                                
                                            """))
                                            os.mkdir(f'C:/Users/tugbacanan.oguz/Desktop/CEDgorus/{klasorKayıt}/{geldigiYerD}')  
                                            time.sleep(1)
                                            print("OK-mkdir")
                                                                        
                                        
                                        time.sleep(1)                            

                                        while True:
                                            list_of_files_rapor = glob.glob('C:/Users/tugbacanan.oguz/Downloads/*') # * means all if need specific format then *.csv
                                            latest_file_rapor = max(list_of_files_rapor, key=os.path.getctime)
                                            print(latest_file_rapor)
                                            dosyaAdi=str(latest_file_rapor).lstrip("C:/Users/tugbacanan.oguz/Downloads/")
                                            if dosyaAdi.endswith("crdownload"):
                                                print("daha yüklenmedi, yüklemeye devam edilecek...")
                                                time.sleep(2)
                                            else:
                                                print("yükleme tamamlandı")
                                                break
                                        


        
                                        list_of_files = glob.glob('C:/Users/tugbacanan.oguz/Downloads/*') # * means all if need specific format then *.csv
                                        latest_file = max(list_of_files, key=os.path.getctime)
                                        print(latest_file)
                                        dosyaAdi=str(latest_file).lstrip("C:/Users/tugbacanan.oguz/Downloads/")

                                        ustYazipath=f'C:/Users/tugbacanan.oguz/Desktop/CEDgorus/{klasorKayıt}/{geldigiYerD}/{geldigiYerD}.pdf'
                                        time.sleep(1)  
                                        shutil.move(f"C:/Users/tugbacanan.oguz/Downloads/{dosyaAdi}", ustYazipath)                    
                                        time.sleep(3)
                                        print("OK")
                                        
                                    self.browser.implicitly_wait(60)
                                    time.sleep(1)
                                    self.browser.execute_script("window.open()")
                                    self.browser.switch_to.window(self.browser.window_handles[1])   # yeni sekmede belgenet
                                    self.browser.get("https://e-belge.tarim.gov.tr/edys-web/sistemeGiris.xhtml") 
                                    self.browser.implicitly_wait(60)
                                    self.browser.switch_to.window(self.browser.window_handles[0])
                                    self.browser.implicitly_wait(60)
                                    time.sleep(5)
                                    x=self.browser.find_element(By.XPATH,"//form[@name='mainPreviewForm']//li[5]").text        
                                    self.browser.implicitly_wait(60)
                                    time.sleep(1)
                                    print(x)
                                    if x=="Evrak Ekleri":
                                        self.browser.find_element(By.XPATH,"//form[@name='mainPreviewForm']//li[5]").click()
                                        self.browser.implicitly_wait(60)
                                        ek=self.browser.find_elements(By.XPATH,"//div[@class='ui-datatable ui-widget myLovGrid']//table[@role='grid']//tbody//tr")
                                        print(len(ek))
                                        for i in range(1,len(ek)+1):
                                            
                                            dosyaText=self.browser.find_element(By.XPATH,f"//div[@class='ui-datatable ui-widget myLovGrid']//table[@role='grid']//tbody//tr[{i}]/td[4]/div[1]/span[1]").text
                                            self.browser.implicitly_wait(60)
                                            self.browser.find_element(By.XPATH,f"//div[@class='ui-datatable ui-widget myLovGrid']//table[@role='grid']//tbody//tr[{i}]/td[5]/button[1]/span[1]").click()
                                            
                                            self.browser.implicitly_wait(60)
                                            time.sleep(4)
                                            print(dosyaText)  
                                            time.sleep(1)
                                            list_of_files2 = glob.glob('C:/Users/tugbacanan.oguz/Downloads/*') # * means all if need specific format then *.csv
                                            latest_file2 = max(list_of_files2, key=os.path.getctime)
                                            print(latest_file2)
                                            dosyaAdi2=str(latest_file2).lstrip("C:/Users/tugbacanan.oguz/Downloads/")

                                            ekPath=f'C:/Users/tugbacanan.oguz/Desktop/CEDgorus/{klasorKayıt}/{geldigiYerD}/{dosyaAdi2}'
                                            time.sleep(1)  
                                            shutil.move(f"C:/Users/tugbacanan.oguz/Downloads/{dosyaAdi2}", ekPath)    
                                            time.sleep(3)          
                                                
                                        print("OK-tüm ekler")  
                                    

                                    else:
                                        print("ek yok")      
                                    self.browser.implicitly_wait(60)         
                                    self.browser.find_element(By.XPATH,f"//*[@id='mainPreviewForm:onizlemeRightTab:uiRepeat:5:cmdbutton'] ").click() # evrak kapat sekmesini tıklar   
                                    self.browser.implicitly_wait(60)
                                    time.sleep(3)
                                    self.browser.find_element(By.XPATH,f"//*[@id='mainPreviewForm:klasorLov_id:favoriteTreeButton']").click()  #favori(yıldız butonu) klasör seç 
                                    self.browser.implicitly_wait(60)
                                    time.sleep(3)
                                    self.browser.find_element(By.XPATH,f"//*[@id='mainPreviewForm:klasorLov_id:lovTree:0']/span/span[3]/div").click()      # klasörü tıkla
                                    self.browser.implicitly_wait(60)
                                    time.sleep(3)
                                    self.browser.find_element(By.XPATH,f"//*[@id='mainPreviewForm:onaysizKapatId']").click()   #evrak kapat butonunu tıklar
                                    self.browser.implicitly_wait(60)  
                                    time.sleep(10) 
                                    print("OK-x")
                                    
                                    

                                    from datetime import datetime
                                    import locale
                                    locale.setlocale(locale.LC_ALL, '') # local dili ayarlar, böylece aşağıdaki datetime çıktılarını türkçe verir

                                    simdi= datetime.today()
                                    result=datetime.strftime(simdi, "%d.%m.%Y %A") # gün.ay.yıl gün adı formatında bugünün tarihini verir
                                    print(result)

                                    daireListesiKısa=["havza","izleme","taşkın","kalite"]
                                    klasorKayitList=os.listdir(f'C:/Users/tugbacanan.oguz/Desktop/CEDgorus/{klasorKayıt}')

                                    a_set = set(daireListesiKısa)
                                    b_set = set(klasorKayitList)

                                    ortakDaire=(a_set & b_set)

                                    if ortakDaire:
                                        print(len(ortakDaire))                        

                                    gorusSayi=len(ortakDaire)

                                    if gorusSayi==4:                          
                                        file=open(f"C:/Users/tugbacanan.oguz/Desktop/Kapatma Listesi.txt","a", encoding="utf-8") # türkçe karakterler de dahil pek çok karakteri tanıması için encoding yapıyoruz
                                        file.write(f"{result}.....{indexDosya}-{FileName}.........{klasorKayıt}/{geldigiYerD}\n****{gorusSayi} YAZI TAMAMLANDI, cevap yazılabilir...****\n")
                                        file.close()
                                        time.sleep(3) 
                                    else:
                                        file=open(f"C:/Users/tugbacanan.oguz/Desktop/Kapatma Listesi.txt","a", encoding="utf-8") # türkçe karakterler de dahil pek çok karakteri tanıması için encoding yapıyoruz
                                        time.sleep(1)
                                        file.write(f"{result}.....{indexDosya}-{FileName}.........{klasorKayıt}/{geldigiYerD}\n")
                                        time.sleep(1)
                                        file.close()
                                    time.sleep(3)
                                    print("x'i sil")
                                    print(f"indexDosya {indexDosya}")

                                    if geldigiYerD=="izleme":
                                        print("izleme")
                                        excel=ExcelDosya((int(indexDosya)+2),10, "")
                                        excel.xSil()
                                        print("izleme x silindi")

                                    elif geldigiYerD=="havza":
                                        print("havza")
                                        excel=ExcelDosya((int(indexDosya)+2),11, "")
                                        excel.xSil()
                                        print("havza x silindi")

                                    elif geldigiYerD=="taşkın":
                                        print("taşkın")
                                        excel=ExcelDosya((int(indexDosya)+2),12, "")
                                        excel.xSil()
                                        print("taşkın x silindi")

                                    elif geldigiYerD=="kalite":
                                        print("kalite")
                                        excel=ExcelDosya((int(indexDosya)+2),13, "")
                                        excel.xSil()
                                        print("kalite x silindi")

                                    else:
                                        print("hata var")

                                    if gorusSayi==4:
                                        excel=ExcelDosya((int(indexDosya)+2),17, "")
                                        excel.fillYellow()


                                    time.sleep(2)



    
                            time.sleep(2)
                                


                        time.sleep(2)           
                        WebDriverWait(self.browser, 50).until(EC.element_to_be_clickable((By.XPATH,"//*[@id='leftMenuForm:kisiselArsivPanel:kisiselArsivKlasoruTree:0_2']"))).click()   # 3. sıradaki klasörü seçme
                        self.browser.implicitly_wait(60)
                        time.sleep(2)  
                        print("*********YENİ YAZI*********")          















belge = Belgenet(username,password)
belge.signIn()
belge.letter()

