
from belgenetUser import username, password
from selenium import webdriver
from selenium.webdriver.common.by import By

from CED_TCO import ExcelDosya

import os
import shutil
import time
import glob
from datetime import datetime



class Belgenet:
    def __init__(self, username, password):
        self.browser=webdriver.Chrome("C:/Users/tugbacanan.oguz/Desktop/python_temelleri_iş/PROJECT/chromedriver.exe")
        self.username=username
        self.password=password
        
             
    
    def signIn(self):
        self.browser.get("https://e-belge.tarim.gov.tr/edys-web/sistemeGiris.xhtml")
        self.browser.implicitly_wait(60)

        self.browser.find_element(By.XPATH,"//*[@id='parolaSertifikaAccordion:uForm:txtUKullaniciAdi']").send_keys(self.username)
        self.browser.find_element(
            By.XPATH, "//*[@id='loginUSifre']").send_keys(self.password)

        self.browser.implicitly_wait(60)

        self.browser.find_element(
            By.XPATH, "/html/body/div[5]/div[2]/div/div[2]/div/div[2]/div[2]/div/form/button/span").click()

        self.browser.implicitly_wait(60)

        # Takibimdekileri tıklar
        self.browser.find_element(
            By.XPATH, "//*[@id='esm_246802192_emi_1689528046']/span").click()

        self.browser.implicitly_wait(60)

        

        #print(yazisec)



    def letter(self):
        
        print("****YAZI SEÇİM İŞLEMİ****")

        takipyazi=self.browser.find_element(By.XPATH,"/html/body/div[9]/div[2]/form/div[3]/ul/li[9]/a/span").text
        takipyazisayi=takipyazi.split()
        takipyazisayim=int(takipyazisayi[2].rstrip(")").lstrip("("))
        print(takipyazisayim)

        while True:
            yazisec=input("İşlem yapılacak yazıları seç ve ardından y/n girişi yap: ")
            if yazisec=="y":
                print("yazılar seçildi")
                break
            elif yazisec=="n":
                print(yazisec)
                continue
            break
                
        
        time.sleep(1)
        #bakYaziOdd=self.browser.find_elements(By.CLASS_NAME,f"ui-chkbox-icon ui-icon ui-icon-blank ui-c") 
        bakYazi=self.browser.find_elements(By.CSS_SELECTOR,f".ui-chkbox-icon.ui-icon.ui-c.ui-icon-check") 
        self.browser.implicitly_wait(60)

        time.sleep(2)


        trlistesi=self.browser.find_elements(By.XPATH,"//*[@id='mainInboxForm:inboxDataTable_data']/tr")
        #print(trlistesi)
        self.browser.implicitly_wait(60)
        time.sleep(1)
        print("seçilen yazı sayısı")
        print(len(bakYazi))
        # yaziSatir=self.browser.find_element(By.XPATH, f"//*[@id='mainInboxForm:inboxDataTable_data']/tr[1]")
        time.sleep(2)
        # print(yaziSatir.get_attribute("class"))
        secilenTrNo=[]
        for y in range(len(trlistesi)):          
            yaziSatir=self.browser.find_element(By.XPATH, f"/html/body/div[10]/div[2]/div/form[2]/div/div[3]/table/tbody/tr[{y+1}]").get_attribute("class")     
            self.browser.implicitly_wait(60)
            time.sleep(2)

            
            if yaziSatir=="ui-widget-content ui-datatable-odd ui-datatable-selectable ui-inbox-read ui-state-highlight":          
                secilenTrNo.append(y+1)   
            elif yaziSatir=="ui-widget-content ui-datatable-even ui-datatable-selectable ui-inbox-read ui-state-highlight": 
                secilenTrNo.append(y+1)   
            elif yaziSatir=="ui-widget-content ui-datatable-odd ui-datatable-selectable ui-inbox-read":           
                secilenTrNo.append(y+1)   
            elif yaziSatir=="ui-widget-content ui-datatable-even ui-datatable-selectable ui-inbox-read": 
                secilenTrNo.append(y+1)   
                
        print(secilenTrNo)  

        time.sleep(2)

        for sec in secilenTrNo:  
            time.sleep(1)
            print(sec)
            trlist=self.browser.find_element(By.XPATH,f"/html/body/div[10]/div[2]/div/form[2]/div/div[3]/table/tbody/tr[{sec}]").get_attribute("aria-selected") 
            self.browser.implicitly_wait(120)
                            
            if trlist=="false":
                print("not selected")               
                
            elif trlist=="true":
                print("selected")
                time.sleep(1)            
                konuYazi=self.browser.find_element(By.XPATH,f"/html/body/div[10]/div[2]/div/form[2]/div/div[3]/table/tbody/tr[{sec}]/td[2]/table/tbody/tr[1]/td[2]/div[1]/h3").text   #yazının konusunu text halinde veriyor   
                print(konuYazi)
                
                time.sleep(1) 
                if "Toplantı Tarihleri" in konuYazi:         
                    joinKonuSon=(str(konuYazi.replace("Toplantı Tarihleri",""))).lstrip("Konu: ")
                elif "İDK Toplantısı" in konuYazi:         
                    joinKonuSon=(str(konuYazi.replace("İDK Toplantısı",""))).lstrip("Konu: ")
                else:
                    joinKonuSon=(str(konuYazi)).lstrip("Konu: ")
                print(joinKonuSon)      #nihai konuyu verir       
                print("OKEYİM-konu")
                gidYerYazi=self.browser.find_element(By.XPATH,f"/html/body/div[10]/div[2]/div/form[2]/div/div[3]/table/tbody/tr[{sec}]/td[2]/table/tbody/tr[2]/td/div").text
                time.sleep(1)
                gidYerYazim=str(gidYerYazi).lstrip("Gideceği Yer:").strip()
                gidYerList=str(gidYerYazim).split("/")
                gidYerSon=str(gidYerList[0]).strip()
                print(gidYerSon)

                time.sleep(3)

                self.browser.find_element(By.XPATH,f"/html/body/div[10]/div[2]/div/form[2]/div/div[3]/table/tbody/tr[{sec}]/td[2]/table").click()
            
                time.sleep(5)
                self.browser.switch_to.frame("ustYaziOnizlemeId1")  # en sağdaki frame'e iframe id'si ile gitme
                print("OK-frame")


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


                self.browser.find_element_by_xpath("//*[@id='j_username']").send_keys("username")
                self.browser.find_element_by_xpath("//*[@id='j_password']").send_keys("password")

                self.browser.implicitly_wait(60)

                self.browser.find_element_by_xpath("/html/body/header/nav/ul/div/form/div/span[5]/input").click()   # şifre giriş butonununa tıklama
                self.browser.implicitly_wait(60)
                
                yazinom=""
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
                        self.browser.implicitly_wait(60) 

                        kayit3=self.browser.find_element(By.XPATH,"//*[@id='main']/span[1]").text   #...kayıt bulundu,

                    
                        time.sleep(2)
                        self.browser.implicitly_wait(60) 
                        print(kayit)
                        # print(kayit2)
                        


                        if "Bir kayıt bulundu." in kayit:
                            self.browser.find_element(By.CSS_SELECTOR,".b > td:nth-child(12) > input:nth-child(1)").click()   #ced satırındaki "Ayrıntılar" butonu

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
                                    #self.browser.find_element(By.XPATH,"//*[@id='pr']/tbody/tr/td[12]/input").click()   #ced satırındaki "Ayrıntılar" butonu
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
                    ilAdison=""
                    if kunyeAdı=="İl":
                        ilAdi=self.browser.find_element(By.XPATH,f"//*[@id='main']/table/tbody/tr[{kunye}]/td[2]").text.strip(":")
                        
                        
                        if re.search('[,]', str(ilAdi).strip()):    
                            textList=str(ilAdi).split(",")
                            print(textList)
                            textil=str(textList[0]).strip(":")
                            ilAdison=textil.strip()

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
                    ilceAdison=""
                    if kunyeAdı=="İlçe":
                        ilceAdi=self.browser.find_element(By.XPATH,f"//*[@id='main']/table/tbody/tr[{kunye}]/td[2]").text.strip(":")
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
                                
                    if kunyeAdı=="Ruhsat Numarası":
                        
                        ruhsatNo=self.browser.find_element(By.XPATH,f"//*[@id='main']/table/tbody/tr[{kunye}]/td[2]").text.strip(":")
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
                        if yazinom!="":
                            ruhsatNoNoson=yazinom
                        else:
                            ruhsatNoNoson=ilAdison
                    print(ruhsatNoNoson)


        # ÇED KLASÖRÜ İÇİNDE KLASÖR OLUŞTURMA

                print(ruhsatNoNoson)
                print(ilAdison)
                print(ilceAdison)


                FileName=""
                if len(listemson)==0:           #yazının konusundaki numaraların atıldığı listenin boş olması halinde  
                    FileNamee=((f"{ruhsatNoNoson}_"+f"{ilAdison}_"+f"{ilceAdison}"))     #yeni klasörün adını oluşturma
                    #newFileName=newFileNames
                    FileName=FileNamee
                    print(FileNamee)            

                            
                elif len(listemson)!=0:    #yazının konusundaki numaraların atıldığı listenin dolu olması halinde 
                    for num in listemson:  
                        print(num)

                        if int(num)<2500:   #yazının konusundaki numaraların atıldığı listedeki numaraların 2500'den küçük olması halinde proje adı inputuyla kullanıcıya sorar
                            FileNamee=((f"{ruhsatNoNoson}_"+f"{ilAdison}_"+f"{ilceAdison}"))     #yeni klasörün adını oluşturma
                            #newFileName=newFileNames
                            FileName=FileNamee
                            print(FileNamee)                                
                                    

                        else:
                            FileName=((f"{num}_"+f"{ilAdison}_"+f"{ilceAdison}")) 
                            print(FileName)
                        break
                print(FileName)
                dosyaListem=os.listdir("C:/Users/tugbacanan.oguz/Desktop/CED")    #ÇED kaydedilen klasörün listesini alıyor, yeni klasör numarasını tespit etmek için
                print(dosyaListem)

                dosyaListem2=[]
                for i in dosyaListem:
                    print(i)
                    klasorAdi=(i.split("-"))[1]
                    dosyaListem2.append(klasorAdi)
                print(dosyaListem2)

                klasorKayıt=""
                if FileName in dosyaListem2:
                    indexDosya=(dosyaListem2.index(FileName))+181
                    klasorKayıt2=dosyaListem2[dosyaListem2.index(FileName)]
                    klasorKayıtt=dosyaListem[dosyaListem2.index(FileName)]
                    klasorKayıt=klasorKayıtt
                    print(klasorKayıt2)
                    print(klasorKayıtt)
                    print(klasorKayıt)
                    print(f"klasorKayıt {klasorKayıt}")
                    indexDosya=int((klasorKayıt.split("-"))[0])
                    print(indexDosya)
                    print("OK-doğru dosya bulundu")
                    
                    time.sleep(1)
                
                self.browser.switch_to.window(self.browser.window_handles[0]) 
                self.browser.implicitly_wait(60)
                sizeWindow=self.browser.get_window_size()
                self.browser.implicitly_wait(60) 
                self.browser.switch_to.frame("ustYaziOnizlemeId1")
                self.browser.implicitly_wait(60)
                self.browser.maximize_window()
                self.browser.implicitly_wait(60)
                self.browser.find_element(By.CSS_SELECTOR,"#download").click() # pencere max iken "download" tıklar üst yazıyı indirir
                self.browser.implicitly_wait(60)
                #self.browser.find_element(By.XPATH,"//*[@id='secondaryDownload']").click()  # açılan menüden "indir" seçeneğini tıklayarak yazıyı indirir                    
                self.browser.implicitly_wait(60)
                time.sleep(3)
                
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

                list_of_files_ust = glob.glob('C:/Users/tugbacanan.oguz/Downloads/*') # * means all if need specific format then *.csv
                latest_file_ust = max(list_of_files_ust, key=os.path.getctime)
                print(latest_file_ust)
                dosyaAdi=str(latest_file_ust).lstrip(f"C:/Users/tugbacanan.oguz/Downloads/")
                time.sleep(1) 
                ustYazipath=f"C:/Users/tugbacanan.oguz/Desktop/CED/{klasorKayıt}/document.pdf"
                time.sleep(1) 
                shutil.move(f"C:/Users/tugbacanan.oguz/Downloads/{dosyaAdi}", ustYazipath) 
                sizeWindowwidth=sizeWindow["width"]
                sizeWindowheight=sizeWindow["height"]
                time.sleep(2)  
                self.browser.set_window_size(sizeWindowwidth,sizeWindowheight)
                time.sleep(2)  
                self.browser.implicitly_wait(60)  
                print(sizeWindow)
                print("size-OK")
                self.browser.implicitly_wait(60)            
                time.sleep(3) 


                    
                self.browser.execute_script("window.open()")
                print(self.browser.window_handles)
                self.browser.switch_to.window(self.browser.window_handles[2])   # yeni pencere/sekme
                self.browser.get("https://pdfmerge.w69b.com/") 
                self.browser.implicitly_wait(60)
                time.sleep(30)


############################

                # self.browser.find_element(By.CSS_SELECTOR,"#dnd_container > div > div > div.mb-ui-filedropper > input[type=file]").send_keys(ustYazipath)
                # self.browser.implicitly_wait(120)
                # time.sleep(5)
                # print(f"klasorKayıt {klasorKayıt}")

                # self.browser.find_element(By.XPATH,"//*[@id='dnd_container']/div/div/div[3]/input").send_keys(f"C:/Users/tugbacanan.oguz/Desktop/CED/{klasorKayıt}/SYGM Görüş_.pdf")
                # self.browser.implicitly_wait(120)
                # time.sleep(3)


                # self.browser.find_element(By.XPATH,"//*[@id='dnd_container']/div/div/button[2]").click()
                # self.browser.implicitly_wait(120)
                # time.sleep(5)
                # self.browser.find_element(By.XPATH,"//*[@id='dnd_container']/div/div/div[1]/button[1]").click()
                # self.browser.implicitly_wait(60)
                # time.sleep(1)
                # # self.browser.find_element(By.XPATH,"/html/body/div[4]/div[2]/input").send_keys("SYGM Görüş.pdf")
                # # self.browser.implicitly_wait(60)
                # # time.sleep(1)
                # self.browser.find_element(By.XPATH,"/html/body/div[4]/div[3]/button[2]").click()
                # self.browser.implicitly_wait(60)
                # time.sleep(2)

####################################################

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

                list_of_files_pdf = glob.glob('C:/Users/tugbacanan.oguz/Downloads/*') # * means all if need specific format then *.csv
                latest_file_pdf = max(list_of_files_pdf, key=os.path.getctime)
                print(latest_file_pdf)
                time.sleep(1)
                dosyaAdi=str(latest_file_pdf).lstrip(f"C:/Users/tugbacanan.oguz/Downloads/")
                time.sleep(1)
                mergedpath=f"C:/Users/tugbacanan.oguz/Desktop/CED/{klasorKayıt}/SYGM_Görüs.pdf"
                time.sleep(1)
                shutil.move(f"C:/Users/tugbacanan.oguz/Downloads/{dosyaAdi}", f"C:/Users/tugbacanan.oguz/Desktop/CED/{klasorKayıt}/SYGM_Görüs.pdf") 
                time.sleep(1)

                
                self.browser.switch_to.window(self.browser.window_handles[1])
                self.browser.implicitly_wait(60)

                liNum=self.browser.find_elements(By.XPATH,"/html/body/div/div[2]/div[1]/div/ul[1]/li")
                time.sleep(2)
                print(len(liNum))
                
                if len(liNum)<=6:
                    for i in range(1,(len(liNum)+1)): 
                        ek2Gorus=self.browser.find_element(By.XPATH,f"//*[@id='home']/li[{i}]/a")
                        self.browser.implicitly_wait(60)
                        print(ek2Gorus.text)
                        # formatGorus=self.browser.find_element(By.XPATH,"//*[@id='home']/li[5]/a")
                        # self.browser.implicitly_wait(60)
                        # print(formatGorus.text)
                        if (ek2Gorus.text)=="EK2 Projesine Görüş Bildir":
                            ek2Gorus.click()
                            self.browser.implicitly_wait(60)
                            break
                        elif (ek2Gorus.text)=="Formata İlişkin Görüş Bildir":
                            ek2Gorus.click()
                            self.browser.implicitly_wait(60)
                            break
                elif len(liNum)>6: 
                    for i in range(1,(len(liNum)+1)):    
                        idkGorus=self.browser.find_element(By.XPATH,f"//*[@id='home']/li[{i}]")     
                        self.browser.implicitly_wait(60)
                        if (idkGorus.text)=="İDK Görüşü Gir":
                            idkGorus.click()
                            #self.browser.find_element(By.XPATH, "//*[@id='idk']/tbody/tr/td[2]/a").click()
                            self.browser.implicitly_wait(60)
                            print("İDK Görüşü Gir")

                            idkList=self.browser.find_elements(By.XPATH, "/html/body/div/div[2]/div[2]/table/tbody/tr")
                            self.browser.implicitly_wait(60)
                            print(len(idkList))
                            idkListem=[]
                            for i in range(1,(len(idkList)+1)):
                                idkTarih=self.browser.find_element(By.XPATH, f"/html/body/div/div[2]/div[2]/table/tbody/tr[{i}]/td[1]").text
                                print(idkTarih)
                                dateTimeConv= datetime. strptime(idkTarih, '%d/%m/%Y')
                                print(dateTimeConv)
                                idkListem.append(dateTimeConv)
                                self.browser.implicitly_wait(60)      
                                print(idkListem)                         

                            print(idkListem)
                            maxListem=max(idkListem)
                            print(maxListem)
                            indexLatest=idkListem.index(maxListem)
                            print(indexLatest)
                            self.browser.find_element(By.XPATH, (f"/html/body/div/div[2]/div[2]/table/tbody/tr[{indexLatest+1}]/td[2]")).click()
                            self.browser.implicitly_wait(60)
                            

                
                self.browser.implicitly_wait(60)
                self.browser.find_element(By.XPATH,"//*[@id='dosya']").send_keys(f"C:/Users/tugbacanan.oguz/Desktop/CED/{klasorKayıt}/SYGM_Görüs.pdf")
                self.browser.implicitly_wait(60)

                
                #self.browser.find_element(By.XPATH,"//*[@id=@aciklama']").send_keys("SYGM Görüş")??
                self.browser.find_element(By.XPATH,"//*[@id='aciklama']").send_keys("SYGM Görüş")
                #self.browser.find_element(By.CSS_SELECTOR,"html body div.wrap div#content div#main form#projeSurecForm table tbody tr td textarea#aciklama").send_keys("SYGM Görüş")
                self.browser.implicitly_wait(60)
                self.browser.find_element(By.XPATH,"//*[@id='submitButton1']").click()  #kaydet butonununa basar
                self.browser.implicitly_wait(60)
                print("KAYDET")

                time.sleep(2)
                ale = self.browser.switch_to.alert  # ced sayfasında çıkan uyarıyı kaldırma
                ale.accept()
                self.browser.implicitly_wait(60)
                #time.sleep(2)
                print("kaydet-alert1")
                #ale = self.browser.switch_to_alert()    #ced sayfasında çıkan uyarıyı kaldırma
                ale.accept()
                self.browser.implicitly_wait(60)
                #time.sleep(2)
                print("kaydet-alert2")
    
                ale.accept()
                self.browser.implicitly_wait(60)
                time.sleep(2)
                print("kaydet-alert3")

                self.browser.close()
                time.sleep(2)

                
                import locale
                locale.setlocale(locale.LC_ALL, '') # local dili ayarlar, böylece aşağıdaki datetime çıktılarını türkçe verir

                simdi= datetime.today()
                result=datetime.strftime(simdi, "%d.%m.%Y %A") # gün.ay.yıl gün adı formatında bugünün tarihini verir
                print(result)

                file=open(f"C:/Users/tugbacanan.oguz/Desktop/ECED Yükleme Listesi.txt","a", encoding="utf-8") # türkçe karakterler de dahil pek çok karakteri tanıması için encoding yapıyoruz
                time.sleep(1)
                file.write(f"{result}.....{indexDosya}-{FileName}.........{klasorKayıt}\n")
                time.sleep(1)
                file.close()
                time.sleep(2)

                self.browser.switch_to.window(self.browser.window_handles[0])
                time.sleep(4)
                

                excel=ExcelDosya((int(indexDosya)+2),17, "OK")
                excel.oOkYaz()
                print( "OK-excel")
                time.sleep(4)


        self.browser.find_element(By.XPATH,f"/html/body/div[10]/div[2]/div/form[2]/div/div[1]/div[2]/div[2]/div/button[1]").click()
        self.browser.implicitly_wait(60)
        time.sleep(3)
        self.browser.find_element(By.XPATH,f"/html/body/div[86]/div[2]/div/button[1]").click()
        self.browser.implicitly_wait(60)

        print("seçili yazılar takipten çıkarıldı")

belge = Belgenet(username,password)
belge.signIn()
belge.letter()

